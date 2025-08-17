#!/usr/bin/env python3
import os, time, requests, pandas as pd
from pathlib import Path

DATA_DIR = Path("data"); DATA_DIR.mkdir(exist_ok=True)
BASE = "https://api.sleeper.app/v1"

def jget(url, tries=3, pause=0.4):
    last = None
    for _ in range(tries):
        r = requests.get(url, timeout=45)
        if r.status_code == 200:
            return r.json()
        last = r
        time.sleep(pause)
    raise RuntimeError(f"GET {url} failed ({getattr(last,'status_code',None)})")

def normalize_players(pm: dict) -> pd.DataFrame:
    rows = []
    for pid, p in pm.items():
        if not pid: 
            continue
        first = (p.get("first_name") or "").strip()
        last  = (p.get("last_name")  or "").strip()
        full  = (p.get("full_name")  or f"{first} {last}".strip()).strip()
        rows.append({
            "player_id": pid,
            "full_name": full,
            "first_name": first,
            "last_name": last,
            "position": p.get("position") or "",
            "team": p.get("team") or "",
            "status": p.get("status") or "",
            "injury_status": p.get("injury_status") or "",
            "depth_chart_order": p.get("depth_chart_order"),
            "college": p.get("college") or "",
            "years_exp": p.get("years_exp"),
            "age": p.get("age"),
        })
    return pd.DataFrame(rows)

def main():
    pm = jget(f"{BASE}/players/nfl") or {}
    df = normalize_players(pm)
    out = DATA_DIR / "players_map.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out} with {len(df):,} rows")

if __name__ == "__main__":
    main()
