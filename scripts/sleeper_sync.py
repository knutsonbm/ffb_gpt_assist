#!/usr/bin/env python3
import os, requests, pandas as pd
from pathlib import Path

DATA = Path("data"); DATA.mkdir(exist_ok=True)
LEAGUE_ID = os.getenv("LEAGUE_ID")
BASE = "https://api.sleeper.app/v1"

def jget(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def save_json_csv(name: str, data):
    df = pd.json_normalize(data)
    out = DATA / f"{name}.csv"
    df.to_csv(out, index=False)
    print(f"Saved {out} ({len(df)} rows)")

def main():
    if not LEAGUE_ID:
        raise SystemExit("LEAGUE_ID env var required")

    # Pull basic league data
    rosters = jget(f"{BASE}/league/{LEAGUE_ID}/rosters")
    users   = jget(f"{BASE}/league/{LEAGUE_ID}/users")
    save_json_csv("rosters_current", rosters)
    save_json_csv("users", users)

    # Figure out current NFL week (may be None in preseason)
    state = jget(f"{BASE}/state/nfl")
    week = state.get("week")
    if week:
        try:
            week = int(week)
        except Exception:
            week = None

    # Fetch matchups & transactions for current week if available
    if week:
        matchups = jget(f"{BASE}/league/{LEAGUE_ID}/matchups/{week}")
        txs      = jget(f"{BASE}/league/{LEAGUE_ID}/transactions/{week}")
        save_json_csv(f"matchups_{week}", matchups)
        save_json_csv(f"transactions_{week}", txs)
        # also keep a "current" pointer for downstream scripts
        (DATA / "matchups_current.csv").write_text("")  # placeholder touch
    else:
        print("No current NFL week reported (preseason or off-season) — skipping matchups/transactions.")

if __name__ == "__main__":
    main()
