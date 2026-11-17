"""HTTP-Abruf mit Rohdatenablage. Nutzung: python3 fetch.py <modul> <quelle> <url> [maxchars]  -> druckt Text."""
import sys, re, time, hashlib, pathlib, subprocess, urllib.request, urllib.parse, datetime as dt
from bs4 import BeautifulSoup
BASE = pathlib.Path(__file__).resolve().parent.parent / "raw"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36", "Accept-Language": "de-DE,de;q=0.9"}
def fetch(modul, quelle, url, maxchars=20000):
    u = urllib.parse.quote(url, safe=":/?&=%#+,;@!$'()*~")
    req = urllib.request.Request(u, headers=UA)
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r: data = r.read(); ctype = r.headers.get("Content-Type", "")
            break
        except Exception as e:
            err = e; time.sleep(2 * (i + 1))
    else:
        return f"FEHLER {err}"
    d = BASE / modul / quelle; d.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha1(url.encode()).hexdigest()[:10]; ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    ext = "pdf" if ("pdf" in ctype or data[:4] == b"%PDF") else "html"
    p = d / f"{ts}_{h}.{ext}"; p.write_bytes(data)
    with open(d / "_index.tsv", "a") as f: f.write(f"{ts}\t{url}\t{p.name}\n")
    if ext == "pdf":
        txt = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True).stdout
    else:
        s = BeautifulSoup(data, "html.parser")
        for t in s(["script", "style", "noscript", "svg"]): t.decompose()
        txt = re.sub(r"\n\s*\n+", "\n", s.get_text("\n"))
    return txt[:maxchars]
if __name__ == "__main__":
    print(fetch(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 20000))
