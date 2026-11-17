#!/usr/bin/env python3
"""scout.py – inkrementeller Lauf der SIGMA-Markterkundung mit Diff-Report "neu seit letztem Lauf".

Nutzung:
    python3 scout.py                 # Module A + C (wöchentlich)
    python3 scout.py --module A C D  # D (OSM-Accounts) monatlich, lädt ~6 GB

Voraussetzungen: Python 3.10+, pyyaml, beautifulsoup4, (für D) osmium.
Ergebnis: laeufe/JJJJ-MM-TT/{neu_ausschreibungen.jsonl, neu_signale.jsonl, diff_report.md}
"""
import argparse, datetime as dt, json, pathlib, subprocess, sys, time
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from relevanz import score as relevanz          # noqa: E402
from score import score_ausschreibung, klasse   # noqa: E402
import ted_harvest                              # noqa: E402
import ov_harvest                               # noqa: E402
from eforms_detail import detail                # noqa: E402

STUFE_NUTS = {}


def stufe_von_nuts(nuts, cfg):
    for s, codes in cfg["region"]["nuts"].items():
        if any((nuts or "").startswith(c) for c in codes):
            return int(s[-1])
    return None


def lade_zustand(p):
    return json.loads(p.read_text()) if p.exists() else {"ausschreibungen": [], "signale": [], "laeufe": []}


def modul_a(cfg, heute, outdir):
    ca = cfg["modul_a"]; neu = []
    if ca["ted"]["aktiv"]:
        seit = (heute - dt.timedelta(days=ca["ted"]["tage_rueckblick"])).strftime("%Y%m%d")
        nuts = " ".join(sum(cfg["region"]["nuts"].values(), []))
        ft = " OR ".join(f'"{t}"' for t in ca["ted"]["volltext"])
        q = (f"(classification-cpv IN ({' '.join(map(str, ca['ted']['cpv']))}) OR FT~({ft})) "
             f"AND place-of-performance IN ({nuts}) AND publication-date>={seit}")
        notices, _ = ted_harvest.harvest(q, maxn=2000)
        for n in map(ted_harvest.norm, notices):
            fit, *_ = relevanz(n)
            if fit < ca["min_leistungs_fit"]:
                continue
            st = stufe_von_nuts((n["nuts"] or "").split("; ")[0], cfg)
            neu.append({"id": f"TED-{n['pubnr']}", "quelle": "TED", "url": n["url"], "titel": n["titel"], "auftraggeber": n["auftraggeber"],
                        "frist": (n["frist"] or "")[:10], "stufe": st, "fit": fit, "typ": n["typ"]})
    if ca["oeffentlichevergabe"]["aktiv"]:
        tmp = outdir / "_ov"
        start = heute - dt.timedelta(days=ca["oeffentlichevergabe"]["tage_rueckblick"])
        ov_harvest.run(start, heute - dt.timedelta(days=1), tmp)
        for f in tmp.glob("????-??-??.jsonl"):
            for line in open(f):
                r = json.loads(line)
                if r.get("fit", 0) < ca["min_leistungs_fit"] or "tender" not in (r.get("tag") or []):
                    continue
                d = detail(r["id"])
                st = stufe_von_nuts((d.get("nuts_detail") or r["nuts"] or [""])[0], cfg)
                neu.append({"id": f"OV-{r['id']}", "quelle": "oeffentlichevergabe.de", "url": r["url"], "titel": r["titel"],
                            "auftraggeber": r["auftraggeber"], "frist": d.get("frist"), "stufe": st, "fit": r["fit"], "unterlagen": d.get("unterlagen")})
    # Bewertung (vereinfachtes Standard-Schema; Leistungs-Fit aus Relevanzfilter)
    for a in neu:
        fd = None
        try:
            fd = dt.date.fromisoformat((a.get("frist") or "")[:10])
        except ValueError:
            pass
        p, k, ko = score_ausschreibung({"leistungs_fit": min(30, a["fit"]), "stufe": a["stufe"], "eignung": 12, "groesse": 10,
                                        "cpv_match": True, "frist": fd, "zugang": 4})
        a.update({"score": p, "klasse": k, "ko": ko})
    return neu


def modul_c(cfg, outdir):
    cc = cfg["modul_c"]["neueroeffnung_info"]
    if not cc["aktiv"]:
        return []
    ziel = ROOT / "raw" / "C" / "neueroeffnung_info"
    vorher = {json.loads(l)["url"] for l in open(ziel / "_entries.jsonl")} if (ziel / "_entries.jsonl").exists() else set()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "neueroeffnung_snowball.py"), str(ziel), str(cc["max_seiten"])], check=False)
    neu = []
    for l in open(ziel / "_entries.jsonl"):
        r = json.loads(l)
        if r["url"] in vorher or not r.get("land"):
            continue
        neu.append({"id": f"NI-{r['url'].split('/', 3)[-1]}", "quelle": "neueroeffnung.info", "url": r["url"], "titel": r["titel"],
                    "typ": r["typ"], "termin": r["eroeffnung"], "adresse": r["adresse"], "land": r["land"], "stufe": r["stufe"]})
    return neu


def filter_stufe(rows, cfg):
    minimum = cfg["region"]["filter_klasse"]
    rang = {"A": 3, "B": 2, "C": 1}
    out = []
    for r in rows:
        st = r.get("stufe")
        if not st:
            continue
        if "klasse" in r and rang[r["klasse"]] < rang[minimum[f"stufe_{st}"]]:
            continue
        out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "config.yaml"))
    ap.add_argument("--module", nargs="+", default=["A", "C"])
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    heute = dt.date.today()
    base = (ROOT / cfg["ausgabe_ordner"]).resolve(); outdir = base / heute.isoformat(); outdir.mkdir(parents=True, exist_ok=True)
    zp = (ROOT / cfg["zustand_datei"]).resolve(); zustand = lade_zustand(zp)
    bekannt_a, bekannt_c = set(zustand["ausschreibungen"]), set(zustand["signale"])

    neu_a = filter_stufe(modul_a(cfg, heute, outdir), cfg) if "A" in args.module else []
    neu_c = modul_c(cfg, outdir) if "C" in args.module else []
    if "D" in args.module:
        print("Modul D: OSM-Extrakt laden und scripts/osm_extract.py + scripts/osm_accounts.py ausführen (siehe 04_qualitaet.md).")

    diff_a = [a for a in neu_a if a["id"] not in bekannt_a]
    diff_c = [c for c in neu_c if c["id"] not in bekannt_c]
    for name, rows in (("neu_ausschreibungen.jsonl", diff_a), ("neu_signale.jsonl", diff_c)):
        with open(outdir / name, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")

    lines = [f"# Diff-Report {heute.strftime('%d.%m.%Y')} – neu seit letztem Lauf "
             f"({zustand['laeufe'][-1] if zustand['laeufe'] else 'erster Lauf'})", "",
             f"## Ausschreibungen ({len(diff_a)})", "", "| Klasse | Score | Frist | Stufe | Auftraggeber | Titel | Link |", "|---|---|---|---|---|---|---|"]
    for a in sorted(diff_a, key=lambda r: -r["score"]):
        lines.append(f"| {a['klasse']} | {a['score']} | {a.get('frist') or ''} | {a['stufe']} | {(a['auftraggeber'] or '')[:40]} | {(a['titel'] or '')[:80]} | {a['url']} |")
    lines += ["", f"## Projekt-Signale ({len(diff_c)})", "", "| Termin | Typ | Stufe | Titel | Adresse | Link |", "|---|---|---|---|---|---|"]
    for c in diff_c:
        lines.append(f"| {c.get('termin') or ''} | {c['typ']} | {c['stufe']} | {c['titel'][:70]} | {(c.get('adresse') or '')[:50]} | {c['url']} |")
    (outdir / "diff_report.md").write_text("\n".join(lines) + "\n")

    zustand["ausschreibungen"] = sorted(bekannt_a | {a["id"] for a in neu_a})
    zustand["signale"] = sorted(bekannt_c | {c["id"] for c in neu_c})
    zustand["laeufe"].append(heute.isoformat())
    zp.parent.mkdir(parents=True, exist_ok=True); zp.write_text(json.dumps(zustand, ensure_ascii=False, indent=1))
    print(f"Fertig: {len(diff_a)} neue Ausschreibungen, {len(diff_c)} neue Signale -> {outdir / 'diff_report.md'}")


if __name__ == "__main__":
    main()
