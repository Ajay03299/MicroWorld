#!/usr/bin/env python3
"""
Rebuild the vendored 2008-crisis dataset for demo/hindcast_2008.py.

All four sources are public and keyless:
  ff_factors_0309.csv  Ken French daily research factors (Mkt-RF, SMB, HML, RF)
  ind10_0309.csv       Ken French 10 industry portfolios, value-weighted daily
  ted.csv              FRED TEDRATE  (3M LIBOR - 3M T-bill spread)
  vix.csv              FRED VIXCLS   (CBOE volatility index)

Output matches what hindcast_2008.py's loaders expect: one header row,
YYYYMMDD in column 0, numeric columns only, no preamble or trailing sections.

Usage:  python fetch_2008.py [output_dir]
"""

import io
import os
import re
import sys
import zipfile
import urllib.request

START, END = 20030101, 20091231

FF_ZIP = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
          "F-F_Research_Data_Factors_daily_CSV.zip")
IND_ZIP = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
           "10_Industry_Portfolios_daily_CSV.zip")
FRED = ("https://fred.stlouisfed.org/graph/fredgraph.csv"
        "?id={sid}&cosd=2003-01-01&coed=2009-12-31")

DATE_ROW = re.compile(r"^\s*(\d{8})\s*,")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read()


def unzip_one(blob):
    zf = zipfile.ZipFile(io.BytesIO(blob))
    return zf.read(zf.namelist()[0]).decode("latin-1")


def parse_french(text, stop_marker=None):
    """Keep the first section only; return (header, rows) inside the date window."""
    lines = text.splitlines()
    if stop_marker:
        for i, ln in enumerate(lines):
            if stop_marker in ln:
                lines = lines[:i]
                break
        else:
            raise SystemExit(f"stop marker {stop_marker!r} not found - format changed")

    header, rows = None, []
    for ln in lines:
        m = DATE_ROW.match(ln)
        if m:
            if header is None:
                raise SystemExit("data row before header - format changed")
            d = int(m.group(1))
            if START <= d <= END:
                cells = [c.strip() for c in ln.split(",")]
                if any(float(c) <= -99.0 for c in cells[1:]):
                    raise SystemExit(f"French missing-value sentinel on {d}")
                rows.append(",".join(cells))
        elif ln.lstrip().startswith(",") and header is None:
            header = "date" + ln.strip()

    if not rows:
        raise SystemExit("no rows in window - format or date range changed")
    return header, rows


def write_french(path, header, rows):
    with open(path, "w", newline="\n") as f:
        f.write(header + "\n")
        f.write("\n".join(rows) + "\n")
    print(f"  {os.path.basename(path):22s} {len(rows):5d} rows  "
          f"{rows[0].split(',')[0]} -> {rows[-1].split(',')[0]}")


def write_fred(path, blob):
    text = blob.decode("utf-8")
    if not text.lstrip().lower().startswith(("date", "observation_date")):
        raise SystemExit(f"unexpected FRED payload: {text[:80]!r}")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    with open(path, "w", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  {os.path.basename(path):22s} {len(lines) - 1:5d} rows")


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    os.makedirs(out, exist_ok=True)
    print(f"writing to {os.path.abspath(out)}")

    h, r = parse_french(unzip_one(get(FF_ZIP)))
    write_french(os.path.join(out, "ff_factors_0309.csv"), h, r)

    h, r = parse_french(unzip_one(get(IND_ZIP)),
                        stop_marker="Average Equal Weighted Returns")
    write_french(os.path.join(out, "ind10_0309.csv"), h, r)

    write_fred(os.path.join(out, "ted.csv"), get(FRED.format(sid="TEDRATE")))
    write_fred(os.path.join(out, "vix.csv"), get(FRED.format(sid="VIXCLS")))
    print("done.")


if __name__ == "__main__":
    main()
