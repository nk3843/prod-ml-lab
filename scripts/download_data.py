"""Download NYC TLC yellow taxi data into data/raw/.

Safe to re-run: files already complete are skipped, downloads go to a .part
file and are renamed only after the byte count matches the server's
Content-Length, so an interrupted run never leaves a truncated parquet that
looks valid.
"""
import sys
import urllib.request
from pathlib import Path

BASE = "https://d37ci6vzurychx.cloudfront.net"
MONTHS = [f"2024-{m:02d}" for m in range(1, 7)]
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def fetch(url: str, dest: Path) -> None:
    with urllib.request.urlopen(url, timeout=60) as r:
        expected = int(r.headers["Content-Length"])
        if dest.exists() and dest.stat().st_size == expected:
            print(f"skip   {dest.name} (already complete)")
            return
        part = dest.with_suffix(dest.suffix + ".part")
        got = 0
        with open(part, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)
                got += len(chunk)
        if got != expected:
            part.unlink(missing_ok=True)
            raise RuntimeError(f"{dest.name}: got {got} bytes, expected {expected}")
        part.replace(dest)
        print(f"fetched {dest.name} ({got / 1e6:.1f} MB)")


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    jobs = [(f"{BASE}/trip-data/yellow_tripdata_{m}.parquet", RAW / f"yellow_tripdata_{m}.parquet") for m in MONTHS]
    jobs.append((f"{BASE}/misc/taxi_zone_lookup.csv", RAW / "taxi_zone_lookup.csv"))
    for url, dest in jobs:
        fetch(url, dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
