"""Holt eForms-XML einer Bekanntmachung von oeffentlichevergabe.de und extrahiert Frist, Unterlagen-URL, Eignung, Zuschlagskriterien."""
import re, sys, json, time, pathlib, urllib.request
RAW = pathlib.Path(__file__).resolve().parent.parent / "raw" / "A" / "oeffentlichevergabe" / "eforms"
def detail(nid):
    RAW.mkdir(parents=True, exist_ok=True); f = RAW / f"{nid}.xml"
    if not f.exists():
        for i in range(3):
            try:
                with urllib.request.urlopen(f"https://oeffentlichevergabe.de/api/notices/{nid}?format=eforms", timeout=60) as r: f.write_bytes(r.read()); break
            except Exception: time.sleep(3 * (i + 1))
        time.sleep(1.0)
    if not f.exists(): return {}
    x = f.read_text(errors="ignore")
    x = re.sub(r"<(/?)\w+:", r"<\1", x)  # Namespace-Präfixe entfernen
    def blk(tag): return re.findall(rf"<{tag}>(.*?)</{tag}>", x, re.S)
    dl = [re.search(r"<EndDate>([^<]+)", b).group(1)[:10] + " " + (re.search(r"<EndTime>([^<]+)", b).group(1)[:5] if re.search(r"<EndTime>", b) else "") for b in blk("TenderSubmissionDeadlinePeriod") if "<EndDate>" in b]
    uri = list(dict.fromkeys(re.findall(r"<URI>([^<]+)", x)))
    sel = re.findall(r"<SelectionCriterion.*?<Description[^>]*>([^<]{5,400})", x, re.S)
    crit = re.findall(r"<SubordinateAwardingCriterion>.*?<Name[^>]*>([^<]+)</Name>", x, re.S)
    desc = re.findall(r"<Description languageID=\"DEU\">([^<]{20,})</Description>", x)
    nuts = re.findall(r"<CountrySubentityCode listName=\"nuts\">([^<]+)", x)
    plz = re.findall(r"<PostalZone>([^<]+)", x)
    return {"frist": sorted(set(dl))[0] if dl else None, "unterlagen": [u for u in uri if not re.search(r"\.(de|com)/?$", u)][:3],
            "eignung": [s.strip() for s in sel][:6], "zuschlagskriterien": list(dict.fromkeys(c.strip() for c in crit))[:8],
            "nuts_detail": list(dict.fromkeys(nuts)), "plz": list(dict.fromkeys(plz))[:4], "langtext": " ".join(desc)[:3000]}
if __name__ == "__main__": print(json.dumps(detail(sys.argv[1]), ensure_ascii=False, indent=1))
