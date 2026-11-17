"""Bewertung Phase 4 – Ausschreibungen (A+B) und Signale (C). Gewichte gemäß Auftrag; Region nach Stufenplan 02a."""
import datetime as dt
HEUTE = dt.date(2026, 11, 16)
REGION = {1: 15, 2: 10, 3: 5}
def werktage(bis):
    d, n = HEUTE, 0
    while d < bis:
        d += dt.timedelta(days=1)
        if d.weekday() < 5: n += 1
    return n
def klasse(p): return "A" if p >= 75 else ("B" if p >= 50 else "C")
def score_ausschreibung(a):
    """a: dict mit leistungs_fit(0-30), stufe, eignung(0-20), groesse(0-15), cpv_match(bool), frist(date|None), zugang(0-5)"""
    zeit = 0; ko = []
    if a.get("frist"):
        wt = werktage(a["frist"])
        zeit = 10 if wt >= 10 else (4 if wt >= 5 else 0)
        if wt < 5: ko.append(f"Frist < 5 Werktage ({wt})")
        if a["frist"] < HEUTE: ko.append("Frist abgelaufen")
    p = a["leistungs_fit"] + REGION.get(a.get("stufe"), 0) + a["eignung"] + a["groesse"] + (5 if a.get("cpv_match") else 0) + zeit + a["zugang"]
    if not a.get("stufe"): ko.append("außerhalb Suchraum")
    return p, klasse(p), ko
def score_signal(s):
    """s: segment_fit(0-25), phase, beleg(0-15), zeitnaehe(0-15), volumen(0-15), zugang(0-10), bestandskunde, frische"""
    phase = {"Planung": 20, "Genehmigung": 18, "Bau": 12, "Eröffnung": 4, "Gerücht": 10}.get(s.get("projektphase"), 8)
    if s.get("monate_bis") is not None and s["monate_bis"] > 24: phase = min(phase, 10)
    p = s["segment_fit"] + phase + s["beleg"] + s["zeitnaehe"] + s["volumen"] + s["zugang"]
    p += 10 if s.get("bestandskunde") else 0
    p += 5 if s.get("frische") else 0
    return min(p, 100), klasse(min(p, 100))
