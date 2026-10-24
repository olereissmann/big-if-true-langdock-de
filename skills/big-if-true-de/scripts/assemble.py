#!/usr/bin/env python3
"""Big If True: Assembler für den Bericht (deutsche Fassung ohne JavaScript).

Der geprüfte Text fließt als Daten durch dieses Skript: Er wird aus der
Quelldatei kopiert und geht nie durch das eigene Schreiben des Modells.
Das garantiert, dass der kommentierte Artikel wörtlich ist.

Aufruf:
  python3 assemble.py density SOURCE.txt CLAIMS.md
      Prüfung für Durchgang 1, VOR dem Verifizieren: Das Zitat jeder
      Aussage muss genau einmal im Text stehen, die Liste muss die
      Schwelle für Wörter pro Aussage erfüllen, und die Liste wird in
      pass1.json im Arbeitsordner festgehalten. Der Build lehnt eine
      check.json ab, die eine festgehaltene Aussage weglässt oder
      zusammenlegt: Jede braucht eine eigene Aussage, deren Zitat ihr
      Zitat aus Durchgang 1 überlappt. Ein neuer density-Lauf darf
      Aussagen hinzufügen, nie entfernen.
  python3 assemble.py build SOURCE.txt CHECK.json OUT.html
      (die Vorlage ist ../assets/template.html; ein vierter Pfad
      überschreibt sie: build SOURCE.txt CHECK.json TEMPLATE.html OUT.html)
      Die Seite wird vollständig hier geschrieben: reines HTML mit
      Fußnoten, kein JavaScript.
  python3 assemble.py export md|csv|json|comments SOURCE.txt CHECK.json OUT
      Dieselben Befunde in anderer Form, nur wenn die Nutzerin darum
      bittet: md  der Textbericht (die Ausweichform in SKILL.md), für
      Dokumente, E-Mail, Slack; csv  eine Zeile pro Aussage, für
      Tabellen und Korrekturlisten; json  die Befunde mit Nummern in
      Artikelreihenfolge und aufgelösten Quellen, für Werkzeuge;
      comments  die needs_review-Befunde als fertige
      Dokumentkommentare: `text` (schlicht, für Google Docs) und
      `markdown` (Inline-Links, für Notion), mit einem `find`-Stück und
      einer Anfang...Ende-`selection`, die die Stelle finden; siehe
      references/write-back.md. Gleiche Prüfung und Reihenfolge wie build.

SOURCE.txt  Der geprüfte Text, genau wie die Nutzerin ihn geliefert hat.
            Absätze durch Leerzeilen getrennt.

CLAIMS.md   Die Liste aus Durchgang 1 (references/extraction.md). Eine
            Aussage ist eine Zeile "- [fact] ..." oder "- [attribution] ...",
            gefolgt von einer Zeile "> " mit dem exakten Zitat. Alle
            anderen Zeilen (Absatzüberschriften, Ausschussprotokoll) sind
            freier Text.

CHECK.json  Eine Datei, jedes Feld benannt. Aussagen werden über Zitate
            verankert, nicht über IDs oder Satznummern; der Build sortiert
            sie nach der Position ihres Zitats in Artikelreihenfolge und
            vergibt daraus die Nummern, die Reihenfolge im Array ist also
            egal. Aussagen ("claim") und Begründungen ("why") auf Deutsch;
            "quote" immer wörtlich in der Sprache des Textes:
{
  "page_title": "<Thema>, geprüft",
  "title": Überschrift, "source": Medium, "byline": Autorin oder "",
  "published": angezeigtes Datum oder "", "checked": heute,
  "refs": {Schlüssel: [Bezeichnung der Quelle, url], ...},
  "thin_text": nur bei einem wirklich dünnen Text (viel Rhetorik, Listen,
               Bildunterschriften): eine Zeile, warum. Die Dichteschwelle
               verlangt das, bevor sie einen Bericht über 20 Wörtern pro
               Aussage baut,
  "claims": [
    {"verdict": "r"|"c"|"s",     r=needs_review (Nachprüfen) c=could_not_verify (Nicht verifizierbar) s=supported (Belegt)
     "claim":  der Aussagetext,
     "why":    Begründung in ein oder zwei Sätzen,
     "refs":   [Quellenschlüssel] (leer erlaubt, wenn "why" erklärt, warum),
     "quote":  die exakte Stelle des Quelltextes, aus der die Aussage
               stammt, wörtlich kopiert: eine Wendung, wenn die Aussage
               Teil eines Satzes ist, der Satz, wenn er ihr Kern ist. Meldet
               der Build, das Zitat sei mehrdeutig, verlängere es, bis es
               eindeutig ist.},
    ...
  ]
}
"""
import difflib, html, json, os, re, sys
from collections import Counter

# Scripts without word spaces (Chinese, Japanese, Thai, Khmer, Lao, Burmese)
# would count as a handful of "words" and wreck the density gate. Count a
# CJK/Thai character as half a word — the usual rough conversion — and
# whitespace tokens for everything else.
_NOSPACE = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f\u0e00-\u0e7f\u0e80-\u0eff\u1780-\u17ff\u1000-\u109f]')

def word_count(text):
    nospace = len(_NOSPACE.findall(text))
    rest = _NOSPACE.sub(' ', text)
    return len(rest.split()) + nospace // 2

VERDICTS = {"r", "c", "s"}
QUOTE_OPENERS = ('“', '"', '‘', "'", '„', '«')


def paragraphs(text):
    return [p for p in re.split(r'\n\s*\n', text.strip()) if p.strip()]


def closest(needle, hay):
    cands = [hay[i:i + len(needle) + 20] for i in range(0, max(1, len(hay) - 10), 25)]
    best = difflib.get_close_matches(needle, cands, n=1, cutoff=0.5)
    return best[0].strip() if best else None


DENSITY_FAIL = (
    "  Thorough extraction of assertive prose runs 12-15 words per claim;\n"
    "  above 20 almost always means Pass 1 was compressed. Re-open Pass 1:\n"
    "  re-walk the paragraphs with the fewest claims, discard log in hand,\n"
    "  and extract the quantifiers, definitions, premises, identity facts,\n"
    "  and background facts that were passed over.\n"
    "  Only if this text is genuinely thin (heavy rhetoric, lists, captions)\n"
    "  state why in check.json — \"thin_text\": \"<one-line reason>\" — and re-run."
)


def norm_map(t):
    """Whitespace-normalized view of a paragraph, mapped back to original
    offsets, so quotes tolerate line wraps and double spaces."""
    out, idx, i = [], [], 0
    while i < len(t):
        if t[i].isspace():
            while i < len(t) and t[i].isspace():
                i += 1
            if out and i < len(t):
                out.append(" "); idx.append(i - 1)
        else:
            out.append(t[i]); idx.append(i); i += 1
    return "".join(out), idx


def nq(quote):
    return " ".join(quote.split())


def locator(text):
    norm_paras = [norm_map(p) for p in paragraphs(text)]

    def locate(quote):
        q = nq(quote)
        hits = []
        for pi, (np, idx) in enumerate(norm_paras):
            for m in re.finditer(re.escape(q), np):
                a = m.start()
                hits.append((pi, idx[a], idx[a + len(q) - 1] + 1))
        return q, hits
    return locate, norm_paras


def quote_error(label, q, hits, norm_paras):
    if len(hits) == 0:
        hint = closest(q, " ".join(np for np, _ in norm_paras))
        return (f"{label}: quote not found in the source text: {q!r}"
                + (f" — closest passage: {hint!r}" if hint else ""))
    if len(hits) > 1:
        return f"{label}: quote appears {len(hits)} times — extend it until it is unique: {q!r}"
    return None


CLAIM_LINE = re.compile(r"^\s*[-*]\s*\[(fact|attribution)\]\s*(.+?)\s*$", re.I)
QUOTE_LINE = re.compile(r"^\s*>\s?(.*?)\s*$")
PASS1 = "pass1.json"


def read_claims(claims_f):
    """[(line number, claim, quote)] from a Pass 1 claims file."""
    lines = open(claims_f, encoding="utf-8").read().splitlines()
    claims, errs = [], []
    for i, line in enumerate(lines):
        m = CLAIM_LINE.match(line)
        if not m:
            continue
        nxt = QUOTE_LINE.match(lines[i + 1]) if i + 1 < len(lines) else None
        if not nxt or not nxt.group(1).strip():
            errs.append(f"line {i + 1}: claim has no quote line under it (\"> \" and the exact words): {m.group(2)[:70]!r}")
            continue
        claims.append((i + 1, m.group(2), nxt.group(1)))
    return claims, errs


def cmd_density(src_f, claims_f):
    text = open(src_f).read()
    claims, errs = read_claims(claims_f)
    locate, norm_paras = locator(text)
    for line, _, quote in claims:
        q, hits = locate(quote)
        err = quote_error(f"line {line}", q, hits, norm_paras)
        if err:
            errs.append(err)
    if not claims and not errs:
        errs.append("no claims found: each claim is a line \"- [fact] ...\" or \"- [attribution] ...\" "
                    "followed by a line \"> \" with its exact quote")
    if errs:
        sys.exit("ERRORS in the claims file — fix and re-run:\n  " + "\n  ".join(errs))
    quotes = [nq(q) for _, _, q in claims]
    if os.path.exists(PASS1):
        before = json.load(open(PASS1))["quotes"]
        dropped = list((Counter(before) - Counter(quotes)).elements())
        if dropped:
            sys.exit("The claims file has fewer claims than the list already recorded. Pass 1 can grow, "
                     "never shrink: restore these claims (split, never merged or removed):\n  "
                     + "\n  ".join(repr(q) for q in dropped))
    words = word_count(text)
    n = len(claims)
    wpc = words / max(1, n)
    json.dump({"claims": n, "quotes": quotes}, open(PASS1, "w"), indent=1)
    print(f"recorded {n} claims in {PASS1}: each needs its own verdict in check.json")
    print(f"density: {wpc:.0f} words per claim ({words} words, {n} claims)")
    if wpc > 20:
        sys.exit("THIN EXTRACTION — do not verify this list yet.\n" + DENSITY_FAIL)
    if wpc > 15:
        print("NOTE: passable but on the thin side — worth one re-walk of the"
              " paragraphs with the fewest claims before verifying.")
    else:
        print("OK: within the 12-15 words-per-claim band of thorough extraction.")


LEDGER_RESOLVED = {"settled", "unreachable", "opened", "skipped"}


def blocked_gate():
    """Pages the browser could not read live in blocked.json in the working
    directory, the same place evidence.py blocked writes it (the check's
    files all live where the scripts are run from). Before the report, each
    one is triaged: settled elsewhere, unreachable, or needs the user. A
    page that needs the user means the turn ends with an ask; a page not
    yet triaged means the check is not finished."""
    path = os.path.abspath("blocked.json")
    if not os.path.exists(path):
        sys.exit("No browser ledger (blocked.json in the working directory). Every page that "
                 "would not fetch goes to the browser, and every page the browser could not "
                 "read goes in the ledger:\n"
                 "  python3 scripts/evidence.py blocked URL\n"
                 "Go back over the pages that would not fetch. Then run\n"
                 "  python3 scripts/evidence.py blocked\n"
                 "from this directory to list the ledger (empty is fine if nothing was "
                 "blocked) and build again.")
    led = json.load(open(path))
    unknown = [f"{e.get('url')}: {e.get('status')!r}" for e in led
               if e.get("status") not in LEDGER_RESOLVED | {"blocked", "needs_user"}]
    if unknown:
        sys.exit("The ledger has entries with a status evidence.py never writes. Record pages only with\n"
                 "  python3 scripts/evidence.py blocked URL [--settled | --unreachable | --needs-user \"...\" | --opened | --skipped]\n  "
                 + "\n  ".join(unknown))
    untriaged = [e["url"] for e in led if e.get("status") == "blocked"]
    if untriaged:
        sys.exit("The ledger has pages not yet triaged. For each, decide what a verdict still needs:\n  "
                 + "\n  ".join(untriaged) +
                 "\n  python3 scripts/evidence.py blocked URL --settled      claim settled from another source\n"
                 "  python3 scripts/evidence.py blocked URL --unreachable  nothing a person could do would open it\n"
                 "  python3 scripts/evidence.py blocked URL --needs-user \"sign in\"   a login or a cleared check would open it\n"
                 "  python3 scripts/evidence.py blocked --no-browser       no browser in this session")
    need = [e for e in led if e.get("status") == "needs_user"]
    if need:
        lines = [f"  {i}. {e['url']} — {e.get('needs', 'sign in or clear the check')}"
                 for i, e in enumerate(need, start=1)]
        sys.exit("STOP — the report cannot be built yet: "
                 f"{len(need)} page(s) need the user. Open each in its own browser tab, then end the turn "
                 "with this message, and continue when they reply:\n\n"
                 f"  I need your help with {len(need)} page(s); each is open in its own tab:\n"
                 + "\n".join(lines) +
                 "\n  Say done when you're through, or skip for any you'd rather leave.\n\n"
                 "When they reply: read each tab, finish those claims, then mark each page\n"
                 "  python3 scripts/evidence.py blocked URL --opened   (or --skipped)\n"
                 "and build again.")


def unanswered(pass1_spans, check_spans):
    """Pass 1 claims left without a check.json claim of their own. Each
    Pass 1 claim needs a distinct check.json claim whose quote overlaps
    its quote in the text: a narrowed or widened quote still answers it,
    but one check.json claim cannot answer two Pass 1 claims, which is
    what a merge is. Maximum matching, so the assignment is never
    order-dependent."""
    adj = [[j for j, (cp, cs, ce) in enumerate(check_spans) if cp == pp and cs < pe and ps < ce]
           for pp, ps, pe in pass1_spans]
    owner = {}

    def assign(i, seen):
        for j in adj[i]:
            if j not in seen:
                seen.add(j)
                if j not in owner or assign(owner[j], seen):
                    owner[j] = i
                    return True
        return False
    return [i for i in range(len(pass1_spans)) if not assign(i, set())]


def pass1_gate(locate, anchors):
    """Every claim recorded at Pass 1 gets its own verdict."""
    if not os.path.exists(PASS1):
        sys.exit(f"No Pass 1 record ({PASS1} in the working directory). Run\n"
                 "  python3 scripts/assemble.py density source.txt claims.md\n"
                 "on the Pass 1 claims file first; it records the list every verdict answers to.")
    quotes = json.load(open(PASS1))["quotes"]
    spans = [locate(q)[1] for q in quotes]
    if any(len(h) != 1 for h in spans):
        sys.exit(f"{PASS1} does not match this source text. Run density again on the claims file for this text.")
    missing = unanswered([h[0] for h in spans], list(anchors.values()))
    if missing:
        sys.exit(f"{len(missing)} claim(s) on the Pass 1 list have no verdict of their own in check.json. "
                 "Each needs its own claim, anchored on a quote that overlaps its Pass 1 quote; one "
                 "claim cannot answer two, because a merged claim hides the verdict of the one it "
                 "swallowed. Split each back out, with its own verdict and rationale:\n  "
                 + "\n  ".join(repr(quotes[i]) for i in missing))


def prepare(src, check_f):
    """Validate CHECK.json against SOURCE.txt and put the claims in article
    order. Shared by build and export so every output agrees on numbering."""
    blocked_gate()
    text = open(src).read()
    check = json.load(open(check_f))
    refs = check.get("refs", {})
    claims_in = check.get("claims", [])
    paras_text = paragraphs(text)

    locate, norm_paras = locator(text)

    errs = []
    for field in ("title", "checked"):
        if not str(check.get(field, "") or "").strip():
            errs.append(f"missing '{field}' at the top of check.json")
    if not isinstance(refs, dict):
        errs.append("'refs' must be an object: {key: [publisher label, url]}")
        refs = {}
    for k, ref in refs.items():
        ok = (isinstance(ref, list) and len(ref) == 2 and all(isinstance(x, str) and x.strip() for x in ref)
              and re.match(r"https?://", ref[1]))
        if not ok:
            errs.append(f"ref {k!r} must be [publisher label, url] with an http(s) url")
    claims_out = []
    anchors = {}   # id -> (para_idx, start, end) within that paragraph
    for idx, c in enumerate(claims_in, start=1):
        for field in ("verdict", "claim", "why", "refs", "quote"):
            if field not in c:
                errs.append(f"claim {idx}: missing field '{field}'")
        v = c.get("verdict")
        if v not in VERDICTS:
            errs.append(f"claim {idx}: verdict must be 'r', 'c' or 's' (got {v!r})")
        for k in c.get("refs", []):
            if k not in refs:
                errs.append(f"claim {idx}: ref key {k!r} not in refs")
        if v == "s" and not c.get("refs"):
            errs.append(f"claim {idx}: supported needs at least one source in refs "
                        "(two independent, or one primary and definitive)")
        q = c.get("quote") or ""
        if q:
            _, hits = locate(q)
            err = quote_error(f"claim {idx}", q, hits, norm_paras)
            if err:
                errs.append(err)
            else:
                anchors[idx] = hits[0]
        elif "quote" in c:
            errs.append(f"claim {idx}: quote is empty")
        claims_out.append([idx, v, c.get("claim", ""), c.get("why", ""), c.get("refs", []), q])
    if errs:
        sys.exit("ERRORS in CHECK.json — fix and re-run:\n  " + "\n  ".join(errs))
    pass1_gate(locate, anchors)

    # Article order is derived, never trusted: sort claims by where their
    # quote sits in the text and assign ids from that, so margin numbers,
    # the claims list, and the spine always follow the article no matter
    # how check.json's array was ordered.
    order = sorted(anchors, key=lambda i: anchors[i])
    id_map = {old_id: new_id for new_id, old_id in enumerate(order, start=1)}
    claims_out = sorted(([id_map[c[0]]] + c[1:] for c in claims_out), key=lambda c: c[0])
    anchors = {id_map[i]: p for i, p in anchors.items()}

    # Pass 1 density gate — the only mechanical guard extraction has.
    # Thorough news/interview extraction runs 12-15 words per claim.
    words = word_count(text)
    wpc = words / max(1, len(claims_out))
    thin = str(check.get("thin_text", "") or "").strip()
    if wpc > 20 and not thin:
        sys.exit(
            f"DENSITY GATE: {wpc:.0f} words per claim ({words} words, {len(claims_out)} claims) — no report built.\n"
            + DENSITY_FAIL
        )
    return dict(text=text, check=check, refs=refs, claims=claims_out, anchors=anchors,
                paras_text=paras_text, words=words, wpc=wpc, thin=thin)


def cmd_build(src, check_f, tpl_f, out_f):
    d = prepare(src, check_f)
    text, check, refs, anchors = d["text"], d["check"], d["refs"], d["anchors"]
    paras_text, words, wpc, thin = d["paras_text"], d["words"], d["wpc"], d["thin"]
    claims_out = d["claims"]

    # partition each paragraph by the claim intervals covering it
    paras = []
    for pi, par in enumerate(paras_text):
        intervals = [(s, e, cid) for cid, (p2, s, e) in anchors.items() if p2 == pi]
        is_quote_graf = par.lstrip().startswith(QUOTE_OPENERS)
        if not intervals:
            paras.append([[par, 0, "q"] if is_quote_graf else [par, 0]])
            continue
        bounds = sorted({0, len(par), *[x for s, e, _ in intervals for x in (s, e)]})
        segs = []
        for a, b in zip(bounds, bounds[1:]):
            ids = sorted(cid for s, e, cid in intervals if s <= a and b <= e)
            seg = [par[a:b], ids if ids else 0]
            if segs and segs[-1][1] == seg[1]:
                segs[-1][0] += seg[0]
            else:
                segs.append(seg)
        if is_quote_graf:
            for seg in segs:
                seg.append("q")
        paras.append(segs)

    out = render_page(open(tpl_f, encoding="utf-8").read(), d, paras)
    open(out_f, "w", encoding="utf-8").write(out)
    print(f"OK: {out_f} · {len(claims_out)} claims · {len(paras)} paragraphs")

    # Pass 1 coverage report (the hard density gate already ran above)
    print(f"   density: {wpc:.0f} words per claim ({words} words)")
    if thin:
        print(f"   thin_text acknowledged: {thin}")
    elif wpc > 15:
        print("   NOTE: thorough extraction of assertive prose runs 12-15 words per"
              " claim. This is passable but on the thin side — worth one re-walk of"
              " the paragraphs with the fewest claims.")
    covered = {pi for pi, _, _ in anchors.values()}
    bare = [(pi, paras_text[pi]) for pi in range(len(paras_text)) if pi not in covered]
    # short paragraphs (headers, section labels, one-line questions) are
    # often legitimately claim-free; flag the substantial ones
    substantial = [(pi, p) for pi, p in bare if word_count(p) >= 25]
    if substantial:
        print(f"   NOTE: {len(substantial)} substantial paragraph(s) carry no anchored claims:")
        for pi, p in substantial[:6]:
            preview = " ".join(p.split())[:90]
            print(f"     - paragraph {pi + 1}: \"{preview}…\"")
        if len(substantial) > 6:
            print(f"     … and {len(substantial) - 6} more")
        print("     Confirm each was consciously judged (discard log), not skipped.")



# ---- the report page, rendered here: the page itself runs no JavaScript ----
# Every word the page shows that depends on the data comes from PAGE; the
# fixed labels live in assets/template.html. Translate both together.
PAGE = {
    "verdict": {"s": "Belegt", "r": "Nachprüfen", "c": "Nicht verifizierbar"},
    "sep": ": ",
    "published": "Veröffentlicht {}",
    "checked": "Geprüft {}",
    "jump": "Aussage {n}: {claim}",
    "fn_title": "Aussage {n}: {verdict}",
    "back": "zurück zum Text",
    "no_source_r": "keine Quelle angegeben",
    "no_source": "keine verlässliche unabhängige Quelle gefunden",
    "lede": ("{n} {w} im Live-Web geprüft: <b>{r} nachprüfen</b>, "
             "{c} nicht unabhängig verifizierbar, {s} belegt."),
    "review_list": "Nachprüfen: {}",
    "claim_word": ("Aussage", "Aussagen"),
    "slug_default": "faktencheck",
}

def _e(x):
    return html.escape(str(x), quote=True)


def _data_uri(mime, body):
    from urllib.parse import quote
    return f"data:{mime};charset=utf-8," + quote(body, safe="")


def render_page(tpl, d, paras):
    """Fill the template: header, spine, the article with a numbered
    footnote after each checked passage, the footnotes themselves (verdict,
    rationale, sources, a link back) and the export texts. Static HTML;
    the only interaction is following links."""
    check, refs, claims = d["check"], d["refs"], d["claims"]
    by_id = {c[0]: c for c in claims}
    rank = {"r": 0, "c": 1, "s": 2}

    def worst(ids):
        return min((by_id[i][1] for i in ids), key=rank.get)

    # a claim's footnote number goes after the last stretch of text it covers
    last_seg = {}
    for pi, para in enumerate(paras):
        for si, seg in enumerate(para):
            for i in (seg[1] or []):
                last_seg[i] = (pi, si)

    art = []
    for pi, para in enumerate(paras):
        body = []
        for si, seg in enumerate(para):
            t, ids = seg[0], seg[1]
            if ids:
                inner = f'<mark class="{worst(ids)}">{_e(t)}</mark>'
                ends = [i for i in ids if last_seg[i] == (pi, si)]
                if ends:
                    inner += '<sup class="fn">' + ",".join(
                        f'<a class="{by_id[i][1]}" id="r{i}" href="#c{i}" '
                        f'title="{_e(PAGE["fn_title"].format(n=i, verdict=PAGE["verdict"][by_id[i][1]]))}">{i}</a>'
                        for i in ends) + "</sup>"
            else:
                inner = _e(t)
            body.append(f'<span class="q">{inner}</span>' if len(seg) > 2 else inner)
        art.append(f'<p>{"".join(body)}</p>')

    notes = []
    for n, v, claim, why, keys, _ in claims:
        if keys:
            srcs = " &middot; ".join(
                f'<a href="{_e(refs[k][1])}" target="_blank" rel="noopener">{_e(refs[k][0])}</a>' for k in keys)
        else:
            srcs = f'<span class="none">{_e(PAGE["no_source_r"] if v == "r" else PAGE["no_source"])}</span>'
        ct = _e(re.sub(r"[.。]+\s*$", "", claim))
        notes.append(
            f'<p class="note v-{v}" id="c{n}"><span class="num">{n}</span> '
            f'<span class="verdict">{_e(PAGE["verdict"][v])}</span>{_e(PAGE["sep"])}'
            f'<span class="claimtext">{ct}.</span> <span class="why">{_e(why)}</span>'
            f' <span class="srcs">{srcs} <a class="back" href="#r{n}" aria-label="{_e(PAGE["back"])}">&#8617; {_e(PAGE["back"])}</a></span></p>')

    spine = "".join(
        f'<a class="{c[1]}" href="#c{c[0]}" title="{_e(PAGE["jump"].format(n=c[0], claim=c[2]))}" '
        f'aria-label="{_e(PAGE["jump"].format(n=c[0], claim=c[2]))}"></a>' for c in claims)

    counts = Counter(c[1] for c in claims)
    review = [c[0] for c in claims if c[1] == "r"]
    review_list = ""
    if review:
        review_list = ('<p class="reviewlist">' + _e(PAGE["review_list"]).format(
            " ".join(f'<a href="#c{n}">[{n}]</a>' for n in review)) + "</p>")
    meta = [check.get("source", ""), check.get("byline", ""),
            PAGE["published"].format(check["published"]) if check.get("published") else "",
            PAGE["checked"].format(check["checked"]) if check.get("checked") else ""]
    title = check.get("title", "")
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or PAGE["slug_default"]
    x = {fmt: export_body(fmt, d) for fmt in ("md", "csv", "json")}
    vals = {
        "REPORT_TITLE": _e(check.get("page_title", title or "Checked")),
        "TITLE": _e(title),
        "META": '<span class="dot">·</span>'.join(f"<span>{_e(m)}</span>" for m in meta if m),
        "SPINE": spine,
        "COUNT": str(len(claims)),
        "LEDE": PAGE["lede"].format(n=len(claims), w=PAGE["claim_word"][len(claims) != 1],
                                    r=counts["r"], c=counts["c"], s=counts["s"]),
        "REVIEW_LIST": review_list,
        "ARTICLE": "".join(art),
        "NOTES": "".join(notes),
        "SLUG": _e(slug),
        "X_MD": _e(x["md"]), "X_CSV": _e(x["csv"].lstrip("﻿")), "X_JSON": _e(x["json"]),
        "DL_MD": _e(_data_uri("text/markdown", x["md"])),
        "DL_CSV": _e(_data_uri("text/csv", x["csv"])),
        "DL_JSON": _e(_data_uri("application/json", x["json"])),
    }
    # one pass over the template, so text inside the article can never be
    # mistaken for a placeholder
    out = re.sub(r"__([A-Z_]+)__", lambda m: vals.get(m.group(1), m.group(0)), tpl)
    if re.search(r"<script|<[^>]*\son[a-z]+\s*=", out, re.I):
        sys.exit("The page would contain a script or an event handler; this edition must stay script-free.")
    return out

VERDICT_WORD = {"r": "needs_review", "c": "could_not_verify", "s": "supported"}
FOOTER = ("*Geprüft mit der Methode [Big If True](https://verso.ink/) von Verso. "
          "Langdock-Fassung auf Deutsch von [THEFUTURE](https://olereissmann.com/newsletter/). "
          "KI kann Fehler machen, beurteile die Belege über die Links.*")
# German labels for the md and csv exports and the document comments;
# the json export keeps the English verdict codes for tooling.
VERDICT_DE = {"needs_review": "Nachprüfen", "could_not_verify": "Nicht verifizierbar", "supported": "Belegt"}


def export_body(fmt, d):
    """The findings in prepare()'s output d as md, csv or json text."""
    check, refs = d["check"], d["refs"]
    rows = [{"n": n, "verdict": VERDICT_WORD[v], "claim": claim, "why": why, "quote": q,
             "sources": [{"label": refs[k][0], "url": refs[k][1]} for k in keys]}
            for n, v, claim, why, keys, q in d["claims"]]
    meta = {k: check.get(k, "") for k in ("title", "source", "byline", "published", "checked")}
    counts = {w: sum(r["verdict"] == w for r in rows) for w in VERDICT_WORD.values()}

    if fmt == "json":
        body = json.dumps({**meta, "counts": counts, "claims": rows}, ensure_ascii=False, indent=1) + "\n"
    elif fmt == "csv":
        import csv, io
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["Nr", "Urteil", "Aussage", "Zitat", "Begründung", "Quellen", "Quellen-URLs"])
        for r in rows:
            w.writerow([r["n"], VERDICT_DE[r["verdict"]], r["claim"], r["quote"], r["why"],
                        "; ".join(s["label"] for s in r["sources"]),
                        " ".join(s["url"] for s in r["sources"])])
        body = "﻿" + buf.getvalue()   # BOM so Excel reads UTF-8
    elif fmt == "md":
        def srcs(r):
            return " Quellen: " + ", ".join(f"[{s['label']}]({s['url']})" for s in r["sources"]) if r["sources"] else ""
        def full(r):
            return f"**{r['n']}. {r['claim']}** {r['why']}{srcs(r)}\n> {r['quote']}\n"
        def compact(r):
            return f"- **{r['n']}.** {r['claim']}{srcs(r)}"
        by = {w: [r for r in rows if r["verdict"] == w] for w in VERDICT_WORD.values()}
        line = " · ".join(x for x in (meta["source"], meta["byline"],
                                       f"Veröffentlicht {meta['published']}" if meta["published"] else "",
                                       f"Geprüft {meta['checked']}" if meta["checked"] else "") if x)
        parts = [f"## Faktencheck: {meta['title']}", line,
                 f"{len(rows)} {'Aussage' if len(rows) == 1 else 'Aussagen'} geprüft: {counts['supported']} belegt, "
                 f"{counts['needs_review']} nachprüfen, {counts['could_not_verify']} nicht verifizierbar.", ""]
        parts += [f"### ⚠️ Nachprüfen ({counts['needs_review']})", ""] + [full(r) for r in by["needs_review"]]
        parts += [f"### ❓ Nicht verifizierbar ({counts['could_not_verify']})", ""] + [full(r) for r in by["could_not_verify"]]
        parts += [f"### ✓ Belegt ({counts['supported']})", ""] + [compact(r) for r in by["supported"]]
        parts += ["", "---", "", FOOTER, ""]
        body = "\n".join(p for p in parts if p is not None)
    elif fmt == "comments":
        body = json.dumps({**meta, "comments": [comment_for(r, d["text"]) for r in rows if r["verdict"] == "needs_review"]},
                          ensure_ascii=False, indent=1) + "\n"
    else:
        sys.exit(f"unknown export format {fmt!r}: use md, csv, json or comments")
    return body


_CURLY = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u00a0": " "})


def _norm(t):
    return " ".join(t.translate(_CURLY).split())


def find_string(quote, text, min_words=5, max_words=12):
    """A short literal fragment of the quote for a document's find box:
    curly quotes straightened (editors match literally), starting after
    any opening punctuation, and extended word by word until it occurs
    exactly once in the text — so a find lands on the right passage."""
    q = _norm(quote).strip("\"' ")
    hay = _norm(text)
    ws = q.split(" ")
    for n in range(min(min_words, len(ws)), min(max_words, len(ws)) + 1):
        frag = " ".join(ws[:n]).rstrip(".;:!?,")
        if hay.count(frag) == 1:
            return frag
    return q


VERDICT_LABEL = VERDICT_DE


def sources_block(srcs, links):
    """links="plain": label and bare URL on separate lines, numbered when
    there are several (Google Docs comments, clipboard). links="markdown":
    inline links on one line (Notion)."""
    if not srcs:
        return ""
    if links == "markdown":
        items = " · ".join(f"[{s['label']}]({s['url']})" for s in srcs)
        return ("Quelle: " if len(srcs) == 1 else "Quellen: ") + items
    if len(srcs) == 1:
        return f"Quelle: {srcs[0]['label']}\n{srcs[0]['url']}"
    return "Quellen:\n" + "\n".join(f"{i}. {s['label']}\n   {s['url']}" for i, s in enumerate(srcs, 1))


def finding_text(r, posted_by_claude=False, links="plain"):
    """One finding as a margin note or a paste-ready snippet: the verdict,
    the rationale, the sources, a provenance line."""
    prov = "Faktencheck mit Big If True (verso.ink)." + (" Kommentar von einem KI-Assistenten gepostet." if posted_by_claude else "")
    return "\n\n".join(p for p in (f"Urteil: {VERDICT_LABEL[r['verdict']]}", r["why"],
                                    sources_block(r["sources"], links), prov) if p)


def comment_for(r, text):
    body = finding_text(r, posted_by_claude=True)
    md = finding_text(r, posted_by_claude=True, links="markdown")
    q = _norm(r["quote"]).strip("\"' ")
    selection = q if len(q) <= 24 else f"{q[:10]}...{q[-10:]}"
    return {"n": r["n"], "quote": r["quote"], "find": find_string(r["quote"], text),
            "selection": selection, "text": body, "markdown": md}


def cmd_export(fmt, src, check_f, out_f):
    d = prepare(src, check_f)
    open(out_f, "w", encoding="utf-8").write(export_body(fmt, d))
    print(f"OK: {out_f} · {fmt} · {len(d['claims'])} claims")


if __name__ == "__main__":
    DEFAULT_TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "template.html")
    if len(sys.argv) == 6 and sys.argv[1] == "build":
        cmd_build(*sys.argv[2:6])
    elif len(sys.argv) == 5 and sys.argv[1] == "build":
        cmd_build(sys.argv[2], sys.argv[3], DEFAULT_TPL, sys.argv[4])
    elif len(sys.argv) == 6 and sys.argv[1] == "export":
        cmd_export(*sys.argv[2:6])
    elif len(sys.argv) == 4 and sys.argv[1] == "density":
        cmd_density(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
