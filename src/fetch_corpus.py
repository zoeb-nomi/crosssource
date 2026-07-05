"""Fetch the CrossSource corpus from Caselaw Access Project static files.

Downloads a curated set of famous, public-domain US court opinions as plain
text into data/corpus/ and records provenance for every file in
data/sources.json. Judicial opinions are public domain (17 U.S.C. § 105 for
federal works; the edicts-of-government doctrine for state opinions). Text
comes from Harvard's Caselaw Access Project (https://case.law), served as
static JSON at https://static.case.law — no API key required.

Note: CourtListener's REST API was the first choice but now requires
authentication for opinion text; CAP static files are the documented
fallback (see README limitations).

Usage:  python src/fetch_corpus.py
"""

import json
import sys
import time
from pathlib import Path

import requests

CAP = "https://static.case.law"
HEADERS = {"User-Agent": "CrossSource/0.1 (open-source RAG eval harness)"}
CORPUS_DIR = Path(__file__).resolve().parent.parent / "data" / "corpus"
SOURCES_PATH = Path(__file__).resolve().parent.parent / "data" / "sources.json"

# slug, case name, official citation, CAP reporter slug, volume, first page,
# court label, year. No tax cases — see README scope.
CASES = [
    ("marbury_v_madison", "Marbury v. Madison", "5 U.S. 137", "us", 5, "137", "U.S. Supreme Court", 1803),
    ("brown_v_board", "Brown v. Board of Education", "347 U.S. 483", "us", 347, "483", "U.S. Supreme Court", 1954),
    ("gideon_v_wainwright", "Gideon v. Wainwright", "372 U.S. 335", "us", 372, "335", "U.S. Supreme Court", 1963),
    ("miranda_v_arizona", "Miranda v. Arizona", "384 U.S. 436", "us", 384, "436", "U.S. Supreme Court", 1966),
    ("ny_times_v_sullivan", "New York Times Co. v. Sullivan", "376 U.S. 254", "us", 376, "254", "U.S. Supreme Court", 1964),
    ("brandenburg_v_ohio", "Brandenburg v. Ohio", "395 U.S. 444", "us", 395, "444", "U.S. Supreme Court", 1969),
    ("tinker_v_des_moines", "Tinker v. Des Moines Independent Community School District", "393 U.S. 503", "us", 393, "503", "U.S. Supreme Court", 1969),
    ("terry_v_ohio", "Terry v. Ohio", "392 U.S. 1", "us", 392, "1", "U.S. Supreme Court", 1968),
    ("katz_v_united_states", "Katz v. United States", "389 U.S. 347", "us", 389, "347", "U.S. Supreme Court", 1967),
    ("mapp_v_ohio", "Mapp v. Ohio", "367 U.S. 643", "us", 367, "643", "U.S. Supreme Court", 1961),
    ("international_shoe_v_washington", "International Shoe Co. v. Washington", "326 U.S. 310", "us", 326, "310", "U.S. Supreme Court", 1945),
    ("erie_v_tompkins", "Erie Railroad Co. v. Tompkins", "304 U.S. 64", "us", 304, "64", "U.S. Supreme Court", 1938),
    ("mcdonnell_douglas_v_green", "McDonnell Douglas Corp. v. Green", "411 U.S. 792", "us", 411, "792", "U.S. Supreme Court", 1973),
    ("griggs_v_duke_power", "Griggs v. Duke Power Co.", "401 U.S. 424", "us", 401, "424", "U.S. Supreme Court", 1971),
    ("faragher_v_boca_raton", "Faragher v. City of Boca Raton", "524 U.S. 775", "us", 524, "775", "U.S. Supreme Court", 1998),
    ("ftc_v_colgate_palmolive", "FTC v. Colgate-Palmolive Co.", "380 U.S. 374", "us", 380, "374", "U.S. Supreme Court", 1965),
    ("us_v_carroll_towing", "United States v. Carroll Towing Co.", "159 F.2d 169", "f2d", 159, "169", "2d Cir.", 1947),
    ("williams_v_walker_thomas", "Williams v. Walker-Thomas Furniture Co.", "350 F.2d 445", "f2d", 350, "445", "D.C. Cir.", 1965),
    ("palsgraf_v_long_island", "Palsgraf v. Long Island Railroad Co.", "248 N.Y. 339", "ny", 248, "339", "N.Y. Court of Appeals", 1928),
    ("macpherson_v_buick", "MacPherson v. Buick Motor Co.", "217 N.Y. 382", "ny", 217, "382", "N.Y. Court of Appeals", 1916),
    ("jacob_youngs_v_kent", "Jacob & Youngs, Inc. v. Kent", "230 N.Y. 239", "ny", 230, "239", "N.Y. Court of Appeals", 1921),
    ("lucy_v_zehmer", "Lucy v. Zehmer", "196 Va. 493", "va", 196, "493", "Va. Supreme Court", 1954),
]

_volume_cache = {}


def get_json(url):
    for attempt in range(4):
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 200:
                return r.json()
            print(f"  HTTP {r.status_code} from {url}, retrying...")
        except requests.RequestException as e:
            print(f"  {e}, retrying...")
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"gave up on {url}")


def volume_metadata(reporter, volume):
    key = (reporter, volume)
    if key not in _volume_cache:
        _volume_cache[key] = get_json(f"{CAP}/{reporter}/{volume}/CasesMetadata.json")
    return _volume_cache[key]


def fetch_case(slug, name, citation, reporter, volume, page, court, year):
    records = [
        rec
        for rec in volume_metadata(reporter, volume)
        if any(c["cite"] == citation for c in rec["citations"]) and rec["first_page"] == page
    ]
    if not records:
        print(f"  !! no CAP record for {citation}")
        return None
    # Page collisions (e.g. a short order sharing the page) — take the longest span.
    rec = max(records, key=lambda r: int(r.get("last_page") or 0) - int(r.get("first_page") or 0))

    case_url = f"{CAP}/{reporter}/{volume}/cases/{rec['file_name']}.json"
    case = get_json(case_url)
    opinions = case["casebody"]["opinions"]
    majority = next((o for o in opinions if o["type"] == "majority"), None)
    if majority is None:
        majority = max(opinions, key=lambda o: len(o["text"]), default=None)
    if majority is None or len(majority["text"]) < 2000:
        print(f"  !! no usable opinion text for {name}")
        return None

    header = f"{name}, {citation} ({court} {year})"
    (CORPUS_DIR / f"{slug}.txt").write_text(header + "\n\n" + majority["text"].strip() + "\n", encoding="utf-8")
    return {
        "file": f"{slug}.txt",
        "case_name": name,
        "citation": citation,
        "court": court,
        "decision_date": case["decision_date"],
        "source": "Caselaw Access Project (Harvard Law School Library)",
        "url": case_url,
        "cap_id": case["id"],
        "opinion_type": majority["type"],
        "chars": len(majority["text"]),
    }


def main():
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    sources, failed = [], []
    for entry in CASES:
        slug, name, citation = entry[0], entry[1], entry[2]
        print(f"fetching {name} ({citation})...")
        try:
            record = fetch_case(*entry)
        except RuntimeError as e:
            print(f"  !! {e}")
            record = None
        if record:
            sources.append(record)
            print(f"  ok — {record['chars']:,} chars ({record['opinion_type']})")
        else:
            failed.append(name)
        time.sleep(0.5)

    SOURCES_PATH.write_text(json.dumps(sources, indent=2) + "\n", encoding="utf-8")
    total = sum(e["chars"] for e in sources)
    print(f"\n{len(sources)} fetched, {len(failed)} failed: {failed or 'none'}")
    print(f"total corpus: {total / 1e6:.2f} MB")
    if len(sources) < 15:
        sys.exit(1)


if __name__ == "__main__":
    main()
