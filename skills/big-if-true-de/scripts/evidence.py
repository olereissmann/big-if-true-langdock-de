#!/usr/bin/env python3
"""evidence.py — keyless lookups against the primary records fact-checks
keep needing. Each subcommand prints a short, citable result and the
exact URL queried. Stdlib only. No keys.

  wayback URL [--at YYYYMMDD]   nearest archived snapshot of a page (Internet Archive)
  wayback-save URL              ask the Internet Archive to capture a page now
  crossref "title or query"     does a paper exist? DOI, journal, date, authors
  doi 10.xxxx/yyy               resolve a DOI to its record
  pubmed "query"                PubMed search: PMIDs, titles, journals, dates
  arxiv "query"                 arXiv search: ids, titles, dates
  edgar "phrase" [--from DATE]  SEC full-text search of filings since 2001
  wikidata "name"               entity lookup: description, Wikidata id
  courtlistener "query"         US court opinions (anonymous access, rate-limited)
  blocked URL                   the browser could not read this page: record it and move on
  blocked URL --settled         …the claim was settled elsewhere; the page is no longer needed
  blocked URL --unreachable     …nothing a person could do would open it
  blocked URL --needs-user "sign in"   …a login or a cleared check would open it: it goes in the ask
  blocked URL --opened / --skipped     …after the user replied: read, or left as is
  blocked --no-browser          no browser this session: every open entry becomes unreachable
  overlap source.txt page.txt   is this page a copy of the checked text or of the same agency
                                story? (save the page's text to a file first)

Everything printed is a lead to open and read, not a verdict.
"""
import argparse, json, os, re, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET

UA = "BigIfTrue/1.0 (fact-checking; +https://verso.ink)"


def get(url, headers=None, retries=2):
    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
            return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
        except Exception as e:  # noqa
            last = e
            time.sleep(2 * (i + 1))
    # URLs may carry logins; the exception text
    # can echo the URL. Keep the host, the path and the HTTP status only.
    u = urllib.parse.urlsplit(url)
    sys.exit(f"fetch failed: {u.hostname}{u.path}\n  {type(last).__name__} {getattr(last, 'code', '')}".rstrip())


def q(s):
    return urllib.parse.quote(s, safe="")


def out(url, lines):
    for l in lines:
        print(l)
    print(f"\nsource: {url}")


def cmd_wayback(a):
    url = f"https://archive.org/wayback/available?url={q(a.url)}" + (f"&timestamp={a.at}" if a.at else "")
    d = json.loads(get(url))
    snap = d.get("archived_snapshots", {}).get("closest")
    if not snap:
        return out(url, ["no snapshot found — try `wayback-save` to capture it now"])
    out(url, [f"snapshot: {snap['url']}", f"captured: {snap['timestamp']}  status: {snap['status']}"])


def cmd_wayback_save(a):
    url = f"https://web.archive.org/save/{a.url}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        r = urllib.request.urlopen(req, timeout=120)
        out(url, [f"saved: {r.headers.get('Content-Location') or r.geturl()}"])
    except Exception as e:  # noqa
        u = urllib.parse.urlsplit(a.url)
        out(url, [f"save request failed for {u.hostname}{u.path}: {type(e).__name__} {getattr(e, 'code', '')}".rstrip()
                  + "; open the URL in a browser to capture it"])


def _crossref_items(url):
    d = json.loads(get(url))
    return [i for i in d["message"].get("items", [d["message"]] if "items" not in d["message"] else [])]


def _paper_line(i):
    title = (i.get("title") or ["(untitled)"])[0]
    auth = ", ".join(f"{p.get('family','')}" for p in (i.get("author") or [])[:3])
    date = "-".join(str(x) for x in (i.get("issued", {}).get("date-parts") or [[""]])[0])
    return f"{i.get('DOI','')}  {date}  {i.get('container-title', [''])[0]}\n    {title}\n    {auth}"


def cmd_crossref(a):
    url = f"https://api.crossref.org/works?query.bibliographic={q(a.query)}&rows={a.n}&mailto=team@verso.ink"
    out(url, [_paper_line(i) for i in _crossref_items(url)] or ["no results"])


def cmd_doi(a):
    url = f"https://api.crossref.org/works/{q(a.doi)}"
    d = json.loads(get(url))["message"]
    out(url, [_paper_line(d), f"type: {d.get('type')}  publisher: {d.get('publisher')}  url: {d.get('URL')}"])


def cmd_pubmed(a):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    url = f"{base}esearch.fcgi?db=pubmed&term={q(a.query)}&retmax={a.n}&retmode=json&sort=relevance"
    ids = json.loads(get(url))["esearchresult"]["idlist"]
    if not ids:
        return out(url, ["no results"])
    s = json.loads(get(f"{base}esummary.fcgi?db=pubmed&id={','.join(ids)}&retmode=json"))["result"]
    lines = [f"PMID {i}  {s[i].get('pubdate','')}  {s[i].get('fulljournalname','')}\n    {s[i].get('title','')}"
             for i in ids]
    out(url, lines + ["\nopen: https://pubmed.ncbi.nlm.nih.gov/<PMID>/"])


def cmd_arxiv(a):
    url = f"https://export.arxiv.org/api/query?search_query=all:{q(a.query)}&max_results={a.n}"
    root = ET.fromstring(get(url))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    lines = []
    for e in root.findall("a:entry", ns):
        lines.append(f"{e.find('a:id', ns).text}  {e.find('a:published', ns).text[:10]}\n    "
                     f"{' '.join(e.find('a:title', ns).text.split())}")
    out(url, lines or ["no results"])


def cmd_edgar(a):
    url = (f"https://efts.sec.gov/LATEST/search-index?q={q(a.phrase)}&dateRange=custom"
           f"&startdt={a.frm}&enddt=2099-12-31")
    d = json.loads(get(url))
    hits = d.get("hits", {}).get("hits", [])
    lines = [f"total hits: {d.get('hits', {}).get('total', {}).get('value')}"]
    for h in hits[:a.n]:
        s = h["_source"]
        adsh, fname = h["_id"].split(":", 1)
        cik = (s.get("ciks") or [""])[0].lstrip("0")
        link = f"https://www.sec.gov/Archives/edgar/data/{cik}/{adsh.replace('-', '')}/{fname}"
        lines.append(f"{s.get('file_date')}  {s.get('form') or s.get('form_type')}  {'; '.join(s.get('display_names', []))[:80]}\n    {link}")
    out(url, lines)


def cmd_wikidata(a):
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={q(a.name)}&language={a.lang}&format=json&limit={a.n}"
    d = json.loads(get(url))
    out(url, [f"{e['id']}  {e.get('label','')} — {e.get('description','')}" for e in d.get("search", [])] or ["no match"])


def cmd_courtlistener(a):
    url = f"https://www.courtlistener.com/api/rest/v4/search/?q={q(a.query)}&type=o"
    d = json.loads(get(url))
    lines = [f"{r.get('dateFiled','')}  {r.get('court','')}  {r.get('caseName','')}\n    https://www.courtlistener.com{r.get('absolute_url','')}"
             for r in d.get("results", [])[:a.n]]
    out(url, lines or ["no results (anonymous access is rate-limited; try again later)"])


# The ledger lives in the working directory, next to source.txt and
# check.json; assemble.py looks for it in the same place.
LEDGER = "blocked.json"
FLAGS = ("settled", "unreachable", "needs_user", "opened", "skipped")


def cmd_blocked(a):
    """The ledger of pages the browser could not read. assemble.py refuses to
    build while an entry is still 'blocked' (not yet triaged) or
    'needs_user' (the ask has not been answered)."""
    led = json.load(open(LEDGER)) if os.path.exists(LEDGER) else []
    if a.no_browser:
        for e in led:
            if e["status"] == "blocked":
                e["status"] = "unreachable"
    elif a.url:
        e = next((e for e in led if e["url"] == a.url), None)
        if e is None:
            e = {"url": a.url, "status": "blocked"}
            led.append(e)
        for f in FLAGS:
            v = getattr(a, f)
            if v:
                e["status"] = f
                if f == "needs_user":
                    e["needs"] = v
    json.dump(led, open(LEDGER, "w"), indent=1)
    for e in led:
        print(f"{e['status']:<12} {e['url']}" + (f"  — {e['needs']}" if e.get("needs") else ""))
    if not led:
        print("no blocked pages recorded")


# ---- copies of the checked text and agency copy ----
# A search for a claim often lands on the checked text itself: the same
# article at another address, or the same news-agency story run by other
# outlets. Such a page proves nothing. `overlap` compares a page with
# source.txt, quotations stripped (two outlets may honestly quote the same
# words), and reports the longest run of identical words.

# Credits and datelines that mark news-agency copy. A hit is a lead, not proof.
WIRE_MARKERS = [
    (r"\((?:dpa|dpa-AFX|AFP|AP|Reuters|epd|KNA|dts|SID|APA|sda|SDA|Keystone-SDA|ANSA|EFE|Belga|ANP|TT|NTB|Ritzau)\)", "agency dateline"),
    (r"\b[a-zA-Z]{2,5}/(?:dpa|DPA|afp|AFP|rtr|Reuters|ap|AP|epd|kna|KNA|dts|sid)\b", "agency credit line"),
    (r"\b(?:dpa|dpa-AFX|Reuters|Agence France-Presse|Associated Press|AFP|epd|KNA)\b", "agency named"),
    (r"\b[Mm]it Material (?:von|der|des) ", "credit line (mit Material von)"),
    (r"\bQuelle: ?(?:dpa|AFP|Reuters|AP|epd|KNA)\b", "credit line (Quelle)"),
    (r"\b(?:[Ww]ith|[Aa]dditional) reporting (?:by|from)\b", "credit line (reporting by)"),
    (r"\b(?:[Ww]riting|[Ee]diting) by\b", "wire credit line (writing/editing by)"),
]

_QUOTED = re.compile(r'„[^“”"]{0,600}[“”"]|“[^”]{0,600}”|"[^"]{0,600}"|«[^»]{0,600}»|»[^«]{0,600}«')


def wire_markers(text):
    found = []
    for pat, kind in WIRE_MARKERS:
        for m in re.finditer(pat, text):
            hit = f"{kind}: {m.group(0).strip()}"
            if hit not in found:
                found.append(hit)
    return found


def _words(text):
    return re.findall(r"\w+", _QUOTED.sub(" ", text).lower())


def overlap_report(src_text, page_text, k=6):
    a, b = _words(src_text), _words(page_text)
    if len(b) < k or len(a) < k:
        return 0, "", 0.0
    index = {}
    for i in range(len(a) - k + 1):
        index.setdefault(tuple(a[i:i + k]), []).append(i)
    best, best_at = 0, None
    j = 0
    while j <= len(b) - k:
        starts = index.get(tuple(b[j:j + k]))
        if not starts:
            j += 1
            continue
        run_here = 0
        for i in starts:
            n = k
            while i + n < len(a) and j + n < len(b) and a[i + n] == b[j + n]:
                n += 1
            if n > run_here:
                run_here = n
            if n > best:
                best, best_at = n, (j, n)
        j += max(1, run_here - k + 1)
    grams_a = {tuple(a[i:i + 5]) for i in range(len(a) - 4)}
    grams_b = [tuple(b[i:i + 5]) for i in range(len(b) - 4)]
    share = sum(g in grams_a for g in grams_b) / max(1, len(grams_b))
    passage = " ".join(b[best_at[0]:best_at[0] + best_at[1]]) if best_at else ""
    return best, passage, share


def cmd_overlap(a):
    src = open(a.source, encoding="utf-8").read()
    page = open(a.page, encoding="utf-8").read()
    run, passage, share = overlap_report(src, page)
    print(f"longest identical run outside quotations: {run} words")
    if passage:
        print(f"  \"{passage[:200]}{'…' if len(passage) > 200 else ''}\"")
    print(f"share of the page's wording found in the checked text: {share:.0%}")
    marks = wire_markers(page)
    if marks:
        print("agency markers on the page: " + "; ".join(marks[:8]))
    if run >= 12 or share >= 0.30:
        print("COPY: this page is the checked text or the same agency copy. It proves nothing; "
              "never cite it for a verdict.")
    elif run >= 8 or share >= 0.10:
        print("SAME BASIS: this page most likely rewrites the same story or agency copy. It counts "
              "as the same source as the checked text, not as an independent one.")
    else:
        print("OWN WORDING: no sign of copying. It still counts as independent only if it shows its "
              "own reporting (its own quotes, correspondent or details).")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--n", type=int, default=5, help="results to show")
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("wayback"); x.add_argument("url"); x.add_argument("--at"); x.set_defaults(f=cmd_wayback)
    x = s.add_parser("wayback-save"); x.add_argument("url"); x.set_defaults(f=cmd_wayback_save)
    x = s.add_parser("crossref"); x.add_argument("query"); x.set_defaults(f=cmd_crossref)
    x = s.add_parser("doi"); x.add_argument("doi"); x.set_defaults(f=cmd_doi)
    x = s.add_parser("pubmed"); x.add_argument("query"); x.set_defaults(f=cmd_pubmed)
    x = s.add_parser("arxiv"); x.add_argument("query"); x.set_defaults(f=cmd_arxiv)
    x = s.add_parser("edgar"); x.add_argument("phrase"); x.add_argument("--from", dest="frm", default="2001-01-01"); x.set_defaults(f=cmd_edgar)
    x = s.add_parser("wikidata"); x.add_argument("name"); x.add_argument("--lang", default="en"); x.set_defaults(f=cmd_wikidata)
    x = s.add_parser("courtlistener"); x.add_argument("query"); x.set_defaults(f=cmd_courtlistener)
    x = s.add_parser("blocked"); x.add_argument("url", nargs="?")
    for f in ("settled", "unreachable", "opened", "skipped", "no-browser"):
        x.add_argument("--" + f, dest=f.replace("-", "_"), action="store_true")
    x.add_argument("--needs-user", dest="needs_user"); x.set_defaults(f=cmd_blocked)
    x = s.add_parser("overlap"); x.add_argument("source"); x.add_argument("page"); x.set_defaults(f=cmd_overlap)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
