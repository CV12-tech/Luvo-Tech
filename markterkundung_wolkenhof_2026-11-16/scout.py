#!/usr/bin/env python3
"""scout.py – inkrementeller Ausschreibungs-Scout für die Wolkenhof GmbH.

Fragt offizielle APIs ab (TED v3; optional oeffentlichevergabe.de), filtert nach
CPV, Region und Negativ-Keywords und schreibt einen Diff-Report "neu seit letztem Lauf".

Aufruf:
    python3 scout.py --config config.yaml            # Modul A (TED)
    python3 scout.py --config config.yaml --dry-run  # nur Query anzeigen

Voraussetzung: Netzwerkzugriff auf api.ted.europa.eu (im Cloud-Lauf vom 16.11.2026 blockiert).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
import yaml

TZ = ZoneInfo("Europe/Berlin")


def load_cfg(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def http_post(url: str, payload: dict, cfg: dict) -> dict:
    delay = cfg.get("rate_limit_sekunden_pro_domain", 1.0)
    for attempt in range(cfg.get("retries", 4) + 1):
        try:
            r = requests.post(url, json=payload, timeout=60)
            if r.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(f"HTTP {r.status_code}")
            r.raise_for_status()
            time.sleep(delay)
            return r.json()
        except requests.RequestException:
            if attempt == cfg.get("retries", 4):
                raise
            time.sleep(delay * cfg.get("backoff_faktor", 2.0) ** attempt)
    return {}


def ted_query(cfg: dict) -> str:
    days = cfg["quellen"]["ted"]["tage_rueckblick"]
    since = (dt.datetime.now(TZ) - dt.timedelta(days=days)).strftime("%Y%m%d")
    cpvs = sorted({c for lst in cfg["cpv"].values() for c in lst})
    nuts = cfg["regionen"]["kern_nuts"] + cfg["regionen"]["erweitert_nuts"]
    cloud_cpv = cfg["cpv"]["greencloud"]
    region_part = f"place-of-performance IN ({' '.join(nuts)})"
    cloud_part = f"(classification-cpv IN ({' '.join(cloud_cpv)}) AND buyer-country IN ({' '.join(cfg['regionen']['cloud_laender'])}))"
    return (f"publication-date >= {since} AND classification-cpv IN ({' '.join(cpvs)}) "
            f"AND ({region_part} OR {cloud_part})")


def fetch_ted(cfg: dict) -> list[dict]:
    tcfg = cfg["quellen"]["ted"]
    out, page = [], 1
    while True:
        payload = {"query": ted_query(cfg), "fields": tcfg["felder"], "page": page,
                   "limit": 100, "scope": "ALL", "paginationMode": "PAGE_NUMBER"}
        data = http_post(tcfg["endpoint"], payload, cfg)
        notices = data.get("notices", [])
        out.extend(notices)
        if len(notices) < 100:
            break
        page += 1
    return out


def _txt(v) -> str:
    if isinstance(v, dict):
        return " ".join(_txt(x) for x in v.values())
    if isinstance(v, list):
        return " ".join(_txt(x) for x in v)
    return str(v or "")


def normalize_ted(n: dict, cfg: dict) -> dict | None:
    title = _txt(n.get("notice-title"))
    if any(k.lower() in title.lower() for k in cfg["negativ_keywords"]):
        return None
    cpv = n.get("classification-cpv") or []
    cpv = cpv if isinstance(cpv, list) else [cpv]
    feld = [f for f, codes in cfg["cpv"].items() if any(str(c)[:5] in {x[:5] for x in codes} for c in cpv)]
    pub = n.get("publication-number")
    return {
        "id": f"TED-{pub}", "modul": "A", "sektor": "öffentlich",
        "geschaeftsfeld": "+".join(feld), "quelle": "TED",
        "url": [f"https://ted.europa.eu/de/notice/-/detail/{pub}"],
        "titel": title, "auftraggeber": _txt(n.get("buyer-name")),
        "ort": _txt(n.get("buyer-city")), "nuts": _txt(n.get("place-of-performance")),
        "cpv": cpv, "angebotsfrist": _txt(n.get("deadline-receipt-tender-date-lot")),
        "geschaetzter_wert": _txt(n.get("estimated-value-lot")),
        "verfahrensart": _txt(n.get("notice-type")),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cfg = load_cfg(args.config)
    if args.dry_run:
        print(ted_query(cfg))
        return

    today = dt.datetime.now(TZ).strftime("%Y-%m-%d")
    outdir = Path(cfg["ausgabe_basis"].format(date=today))
    (outdir / "raw" / "A" / "ted").mkdir(parents=True, exist_ok=True)

    raw = fetch_ted(cfg)
    (outdir / "raw" / "A" / "ted" / f"ted_{today}.json").write_text(
        json.dumps({"abgerufen": dt.datetime.now(TZ).isoformat(), "notices": raw}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    hits = [h for h in (normalize_ted(n, cfg) for n in raw) if h]

    state_path = Path(cfg["letzter_lauf_datei"])
    state = json.loads(state_path.read_text()) if state_path.exists() else {"seen": []}
    seen = set(state["seen"])
    new = [h for h in hits if h["id"] not in seen]

    with (outdir / "scout_treffer.jsonl").open("w", encoding="utf-8") as f:
        for h in hits:
            f.write(json.dumps(h, ensure_ascii=False) + "\n")
    lines = [f"# Diff-Report {dt.datetime.now(TZ).strftime('%d.%m.%Y')} – neu seit letztem Lauf ({len(new)} von {len(hits)})", ""]
    for h in new:
        lines.append(f"- **{h['titel']}** – {h['auftraggeber']} ({h['ort']}) · Frist {h['angebotsfrist'] or '?'} · {h['geschaeftsfeld']} · {h['url'][0]}")
    (outdir / "diff_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    state["seen"] = sorted(seen | {h["id"] for h in hits})
    state["letzter_lauf"] = dt.datetime.now(TZ).isoformat()
    state_path.write_text(json.dumps(state, indent=1), encoding="utf-8")
    print(f"{len(hits)} Treffer, davon {len(new)} neu → {outdir/'diff_report.md'}")


if __name__ == "__main__":
    main()
