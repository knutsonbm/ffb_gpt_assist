import requests
import pandas as pd
import os
from pathlib import Path

LEAGUE_ID = os.getenv("LEAGUE_ID", "1257452477297479680")
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

ENDPOINTS = {
    "rosters": f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters",
    "matchups": f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/1",  # week 1 for now
    "users": f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users",
    "transactions": f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/transactions/1",  # week 1
}

def fetch_and_save(name, url):
    print(f"Fetching {name} from {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    df = pd.json_normalize(data)
    out_path = DATA_DIR / f"{name}.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {name} → {out_path}")

def main():
    for name, url in ENDPOINTS.items():
        try:
            fetch_and_save(name, url)
        except Exception as e:
            print(f"Error fetching {name}: {e}")

if __name__ == "__main__":
    main()
