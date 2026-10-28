#!/usr/bin/env python3
"""Geocode official branch addresses with OpenStreetMap Nominatim.

One request per second. A pin is stored only when the result is a building,
a house number, or a named place that matches the official address line.
Street-only results are rejected. Coordinates are never invented.
"""
import json, os, re, time, urllib.parse, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "coords.json")
UA = "SmartIDAtTheBank/1.0 (https://sa-smart-id-bank-finder.vercel.app; branch map geocoder)"
PAUSE = 1.05

STREET_WORD = re.compile(
    r"\b(street|st|str|road|rd|drive|dr|avenue|ave|boulevard|blvd|lane|ln|crescent|cres|close|highway|straat|weg)\b",
    re.I,
)
PREMISE_WORD = re.compile(
    r"\b(mall|centre|center|plaza|building|waterfront|galleria|complex)\b",
    re.I,
)
STREET_PHRASE = re.compile(
    r"(\d{1,4})\s+((?:[A-Za-z0-9'’.\-]+\s+){0,5}?(?:street|st|str|road|rd|drive|dr|avenue|ave|boulevard|blvd|lane|ln|crescent|cres|close)\b)",
    re.I,
)
PREMISE_PHRASE = re.compile(
    r"((?:[A-Za-z0-9&'’.\-]+\s+){0,5}?(?:mall|centre|center|plaza|building|waterfront|galleria|complex)\b)",
    re.I,
)
GENERIC_PLACE = {"city", "town", "centre", "center", "shopping", "mall", "plaza", "building", "cape", "south", "park", "retail", "the"}
HOUSE_LEAD = re.compile(
    r"^\s*((?:\d{1,4}[a-zA-Z]?)(?:\s*[,&]\s*\d{1,4}[a-zA-Z]?)*)\s+(.+)$"
)
CORNER = re.compile(r"\b(cnr|corner|c/o|c\/o)\b", re.I)
STOP = {"the", "and", "of", "shop", "shops", "a", "at", "no"}
CITY_ALT = {
    "grahamstown": ["makhanda"],
    "port elizabeth": ["gqeberha"],
    "nelspruit": ["mbombela"],
    "umtata": ["mthatha"],
    "mthatha": ["umtata"],
    "witbank": ["emalahleni"],
    "emalahleni": ["witbank"],
    "pietersburg": ["polokwane"],
    "someset east": ["somerset east"],
    "vosloosrus": ["vosloorus"],
    "attridgeville": ["atteridgeville"],
    "king williams town": ["qonce"],
    "queenstown": ["komani"],
    "stanger": ["kwadukuza"],
    "port st johns": ["port saint johns"],
    "nylstroom": ["modimolle"],
}

NEDBANK = [
    ("nedbank", "Nedbank Arcadia Pretoria", "Shop 25, Nedbank Plaza, Beatrix Street", "Pretoria", "Gauteng", ""),
    ("nedbank", "Nedbank Sandown", "Shop L05, Lower Ground, Block, 135 Rivonia Road", "Sandown", "Gauteng", ""),
    ("nedbank", "Nedbank St Georges Mall", "Shop 3 The Box, St Georges Mall c/o Riebeeck Street", "Cape Town", "Western Cape", ""),
    ("nedbank", "Nedbank Nelspruit", "Shop 1, Nedbank Centre, 30 Brown Street", "Nelspruit", "Mpumalanga", ""),
    ("nedbank", "Nedbank Durban North", "57 Adelaide Tambo Drive", "Durban", "KwaZulu-Natal", ""),
    ("nedbank", "Nedbank Lakeview Office Park", "16 Constantia Blvd, Constantia Kloof", "Roodepoort", "Gauteng", ""),
]

_last = 0.0

def norm(s):
    s = (s or "").lower().replace("&", " and ")
    s = s.replace("’", "'")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def tokens(s):
    return [t for t in norm(s).split() if t not in STOP and len(t) > 1]

def name_match(query_name, result_name):
    qn, rn = norm(query_name), norm(result_name or "")
    if not qn or not rn:
        return False
    if "victoria" in qn and "alfred" in qn and "waterfront" in qn and "waterfront" in rn:
        return True
    qt = tokens(query_name)
    if not qt:
        return False
    # Every meaningful word in the official place name has to appear in the result name.
    return all(t in rn.split() or t in rn for t in qt)

def road_core(s):
    s = norm(s)
    s = re.sub(r"\b(street|st|road|rd|drive|dr|avenue|ave|boulevard|blvd|lane|ln|crescent|cres|close|highway)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def road_match(query_road, result_road):
    qc, rc = road_core(query_road), road_core(result_road or "")
    if not qc or not rc:
        return False
    return qc == rc or qc in rc or rc in qc

def span_m(bb):
    south, north, west, east = (float(x) for x in bb)
    import math
    lat = (south + north) / 2
    lat_m = abs(north - south) * 111_320
    lon_m = abs(east - west) * 111_320 * math.cos(math.radians(lat))
    return max(lat_m, lon_m)

def numbers_in(s):
    return re.findall(r"\d{1,4}", s or "")

def city_ok(addr, display, city):
    city_n = norm(city)
    names = [city_n] + CITY_ALT.get(city_n, [])
    blob_parts = [display or ""]
    for key in ("city", "town", "village", "hamlet", "suburb", "municipality", "city_district", "quarter", "neighbourhood", "county"):
        if addr.get(key):
            blob_parts.append(addr[key])
    blob = norm(" ".join(blob_parts))
    return any(n and n in blob for n in names)

def postal_ok(addr, postal):
    want = re.sub(r"\D", "", str(postal or ""))
    got = re.sub(r"\D", "", str(addr.get("postcode") or ""))
    if len(want) != 4 or len(got) != 4:
        return False
    return want == got

def province_ok(addr, province):
    state = norm(addr.get("state") or "")
    prov = norm(province)
    if not prov or not state:
        return False
    return prov == state or prov in state or state in prov

def locality_ok(addr, display, city, province, postal):
    if (addr.get("country_code") or "").lower() != "za":
        return False
    c_ok, p_ok, s_ok = city_ok(addr, display, city), postal_ok(addr, postal), province_ok(addr, province)
    if s_ok and (c_ok or p_ok):
        return True
    # City and postal agree, even when the published province does not match the town.
    if c_ok and p_ok:
        return True
    return False

def loc_key(bank, name, line, city, postal):
    return "|".join([bank, name.strip(), line.strip(), city.strip(), str(postal).strip()])

def wait():
    global _last
    now = time.monotonic()
    if _last:
        left = PAUSE - (now - _last)
        if left > 0:
            time.sleep(left)
    _last = time.monotonic()

def search(q):
    params = urllib.parse.urlencode({
        "q": q,
        "format": "jsonv2",
        "addressdetails": 1,
        "limit": 5,
        "countrycodes": "za",
    })
    url = "https://nominatim.openstreetmap.org/search?" + params
    wait()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return json.loads(resp.read().decode()), None
    except urllib.error.HTTPError as e:
        if e.code in (429, 503):
            time.sleep(8)
            wait()
            try:
                with urllib.request.urlopen(req, timeout=40) as resp:
                    return json.loads(resp.read().decode()), None
            except Exception as e2:
                return [], str(e2)
        return [], f"HTTP {e.code}"
    except Exception as e:
        return [], str(e)

def summarise(hit):
    addr = hit.get("address") or {}
    return {
        "lat": float(hit["lat"]),
        "lon": float(hit["lon"]),
        "display_name": hit.get("display_name") or "",
        "category": hit.get("category") or "",
        "type": hit.get("type") or "",
        "name": hit.get("name") or "",
        "place_rank": hit.get("place_rank"),
        "osm": f"{hit.get('osm_type')}/{hit.get('osm_id')}",
        "house_number": addr.get("house_number") or "",
        "road": addr.get("road") or "",
        "span_m": round(span_m(hit["boundingbox"]), 1) if hit.get("boundingbox") else None,
    }

def consider(hits, item):
    """Return (hit, reason) or (None, reason)."""
    ok = []
    notes = []
    for hit in hits:
        addr = hit.get("address") or {}
        if not locality_ok(addr, hit.get("display_name") or "", item["city"], item["province"], item["postal"]):
            notes.append("locality did not match")
            continue
        try:
            span = span_m(hit["boundingbox"]) if hit.get("boundingbox") else 9e9
        except Exception:
            span = 9e9
        cat = hit.get("category") or ""
        typ = hit.get("type") or ""
        if item["kind"] == "house":
            hn = str(addr.get("house_number") or "")
            hn_nums = set(numbers_in(hn))
            if not hn_nums & set(item["numbers"]):
                notes.append("no matching house number")
                continue
            if not road_match(item["road"], addr.get("road") or hit.get("name") or ""):
                notes.append("road did not match")
                continue
            if cat == "highway" or span > 250:
                notes.append("result was the street, not the building")
                continue
            ok.append(hit)
            continue
        if item["kind"] == "premise":
            if cat in ("highway", "boundary") or typ in ("city", "town", "suburb", "village", "municipality", "state"):
                notes.append("result was an area, not the named place")
                continue
            if cat == "place" and typ not in ("house", "building", "retail"):
                notes.append("result was a place area")
                continue
            if not name_match(item["premise"], hit.get("name") or ""):
                notes.append("place name did not match")
                continue
            if span > 2000:
                notes.append("named place was too large to pin")
                continue
            ok.append(hit)
            continue
        if item["kind"] == "corner":
            disp = norm(hit.get("display_name") or "")
            roads_ok = all(road_core(r) and road_core(r) in disp for r in item["roads"])
            junction = typ in ("junction", "crossing", "mini_roundabout") or (cat == "highway" and span <= 80 and roads_ok)
            if not roads_ok:
                notes.append("both street names were not in the result")
                continue
            if span > 120 or not junction:
                notes.append("corner was not a single junction")
                continue
            ok.append(hit)
            continue
        notes.append("not a supported address kind")
    if not ok:
        if not hits:
            return None, "Nominatim returned no result"
        return None, notes[0] if notes else "no confident result"
    if len(ok) == 1:
        return ok[0], "matched"
    # Keep one point only when the candidates sit on the same building.
    def dist(a, b):
        import math
        lat1, lon1, lat2, lon2 = float(a["lat"]), float(a["lon"]), float(b["lat"]), float(b["lon"])
        return math.hypot((lat1 - lat2) * 111_320, (lon1 - lon2) * 111_320 * math.cos(math.radians(lat1)))
    anchor = max(ok, key=lambda h: h.get("place_rank") or 0)
    if all(dist(anchor, h) <= 80 for h in ok):
        return anchor, "matched"
    return None, "several different results, so the point is ambiguous"

def shop_number(raw, start):
    return re.search(r"\bshops?\s*$", raw[:start], re.I) is not None

def premise_phrase(raw):
    found = None
    for m in PREMISE_PHRASE.finditer(raw):
        phrase = re.sub(r"^shops?\s*[0-9a-zA-Z]*\s*,?\s*", "", m.group(1), flags=re.I).strip(" ,")
        words = set(tokens(phrase))
        if not words or words <= GENERIC_PLACE:
            continue
        found = phrase
    return found

def house_phrase(raw):
    # "101, 103 & 107 Bok Street"
    multi = re.search(
        r"((?:\d{1,4}[a-zA-Z]?\s*(?:,|&|and)\s*)+\d{1,4}[a-zA-Z]?)\s+((?:[A-Za-z0-9'’.\-]+\s+){0,5}?(?:street|st|str|road|rd|drive|dr|avenue|ave|boulevard|blvd|lane|ln|crescent|cres|close)\b)",
        raw, re.I,
    )
    if multi and not shop_number(raw, multi.start()):
        nums = numbers_in(multi.group(1))
        road = multi.group(2).strip(" ,")
        if nums and STREET_WORD.search(road):
            return nums, road
    found = None
    for m in STREET_PHRASE.finditer(raw):
        if shop_number(raw, m.start()):
            continue
        found = ([m.group(1)], m.group(2).strip(" ,"))
    return found

def classify_line(line):
    raw = (line or "").strip().strip(",").strip()
    if not raw:
        return None
    if re.fullmatch(r"(no\.?\s*)?\d+(\s*-\s*\d+)?[a-zA-Z]?", raw, flags=re.I):
        return None
    if re.fullmatch(r"r\s?\d+[a-z]?", raw, flags=re.I):
        return None
    house = house_phrase(raw)
    premise = premise_phrase(raw)
    if house:
        nums, road = house
        item = {"kind": "house", "numbers": nums, "road": road, "query_core": f"{nums[0]} {road}"}
        if premise:
            item["fallback_premise"] = premise
        return item
    if premise and not (STREET_WORD.search(raw) and not PREMISE_WORD.search(raw)):
        # A shopping centre whose name contains "boulevard" is still the named place.
        if PREMISE_WORD.search(raw):
            return {"kind": "premise", "premise": premise, "query_core": premise}
    if CORNER.search(raw) and STREET_WORD.search(raw):
        bits = re.split(r"\b(?:cnr|corner|c/o|c\/o)\b|&|,|\band\b", raw, flags=re.I)
        roads = []
        for bit in bits:
            bit = bit.strip(" ,")
            if not bit or norm(bit) in ("cnr", "corner", "c o"):
                continue
            roads.append(bit)
        if len(roads) >= 2:
            return {"kind": "corner", "roads": roads[:2], "query_core": f"{roads[0]} and {roads[1]}"}
        return None
    if STREET_WORD.search(raw):
        road = re.sub(r"^shops?\s*[0-9a-zA-Z,&\- ]*?(?=[A-Za-z])", "", raw, flags=re.I).strip(" ,")
        return {"kind": "street", "road": road or raw, "query_core": road or raw}
    if re.fullmatch(r"(shop|shops)\b.*", raw, flags=re.I):
        return None
    return None

def load_branches():
    banks = [("capitec", "p1.json"), ("standard-bank", "p2.json"), ("fnb", "p3.json"), ("absa", "p4.json")]
    rows = []
    for bank, fn in banks:
        for b in json.load(open(os.path.join(HERE, fn)))["branches"]:
            rows.append((bank, b["branchName"], b["suburb"], b["city"], b.get("province") or "", str(b.get("postal_code") or "")))
    rows.extend(NEDBANK)
    return rows

def main():
    pins = {}
    attempted = []
    seen_q = {}
    for bank, name, line, city, province, postal in load_branches():
        key = loc_key(bank, name, line.strip(), city, postal)
        info = classify_line(line)
        if not info:
            attempted.append({"key": key, "bank": bank, "name": name, "line": line, "status": "unpinned", "reason": "The official line is not a street address or a named place."})
            continue
        if info["kind"] == "street":
            attempted.append({"key": key, "bank": bank, "name": name, "line": line, "status": "unpinned", "reason": "The official line names a street but not a building number, so the branch point on that street is not known."})
            continue
        city_n = norm(city)
        cores = [(info["kind"], info["query_core"])]
        if info.get("fallback_premise"):
            cores.append(("premise", info["fallback_premise"]))
        queries = []
        for kind, core in cores:
            queries.append((kind, f"{core}, {city}, {postal}, South Africa"))
            if city_n in CITY_ALT:
                queries.append((kind, f"{core}, {CITY_ALT[city_n][0]}, {postal}, South Africa"))
        chosen = None
        reason = "Nominatim returned no result"
        used_q = queries[0][1]
        for kind, q in queries:
            q = re.sub(r"\s+", " ", q).replace(" ,", ",").replace(", ,", ",").strip(" ,")
            used_q = q
            if q in seen_q:
                hits, err = seen_q[q]
            else:
                print("QUERY", q, flush=True)
                hits, err = search(q)
                seen_q[q] = (hits, err)
                print("  ", len(hits), err or (hits[0].get("display_name", "")[:110] if hits else ""), flush=True)
            if err:
                reason = f"Nominatim request failed ({err})"
                continue
            if not hits:
                reason = "Nominatim returned no result"
                continue
            item = dict(info)
            item["kind"] = kind
            if kind == "premise":
                item["premise"] = info.get("fallback_premise") or info.get("premise") or info["query_core"]
            item["city"] = city
            item["province"] = province
            item["postal"] = postal
            hit, reason = consider(hits, item)
            if hit:
                chosen = hit
                info = dict(info)
                info["kind"] = kind
                break
        if not chosen:
            attempted.append({"key": key, "bank": bank, "name": name, "line": line, "query": used_q, "status": "unpinned", "reason": reason})
            continue
        if info["kind"] == "house":
            name_nums = set(re.findall(r"\b\d{1,4}\b", name))
            if name_nums and name_nums.isdisjoint(set(info["numbers"])):
                attempted.append({"key": key, "bank": bank, "name": name, "line": line, "query": used_q, "status": "unpinned", "reason": "The branch name and the address line give different numbers, so the building was not pinned."})
                continue
        meta = summarise(chosen)
        if not (-35.5 <= meta["lat"] <= -21.5 and 16 <= meta["lon"] <= 33.5):
            attempted.append({"key": key, "bank": bank, "name": name, "line": line, "query": used_q, "status": "unpinned", "reason": "Result was outside South Africa."})
            continue
        meta.update({"query": used_q, "method": info["kind"], "bank": bank, "name": name, "line": line.strip(), "city": city, "province": province, "postal": postal})
        pins[key] = meta
        attempted.append({"key": key, "bank": bank, "name": name, "line": line, "query": used_q, "status": "pinned", "reason": f"Nominatim {info['kind']} match: {meta['display_name']}"})
        print("PIN", name, meta["lat"], meta["lon"], flush=True)
    doc = {
        "geocoder": "OpenStreetMap Nominatim",
        "endpoint": "https://nominatim.openstreetmap.org/search",
        "user_agent": UA,
        "rate": "1 request per second",
        "fetched": "2026-10-28",
        "rule": "A pin is stored only for a house number, a matching named place, or a single junction. Street-only results are left out. Coordinates are copied from Nominatim and are not estimated.",
        "pins": pins,
        "attempts": attempted,
    }
    json.dump(doc, open(OUT, "w"), ensure_ascii=False, indent=2)
    print("pins", len(pins), "attempts", len(attempted), "queries", len(seen_q))

if __name__ == "__main__":
    main()
