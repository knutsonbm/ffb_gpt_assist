#!/usr/bin/env python3
import ast, os, pandas as pd
from pathlib import Path

DATA = Path("data")
PMAP = DATA / "players_map.csv"

def safe_list(x):
    if isinstance(x, list): return x
    if pd.isna(x): return []
    try:
        return ast.literal_eval(x)
    except Exception:
        return []

def explode_rosters(rosters_path: Path, pmap: pd.DataFrame) -> pd.DataFrame:
    df = pd.read_csv(rosters_path)
    # Common columns in Sleeper /rosters: roster_id, owner_id, players (list), reserve (list)
    df["players"] = df["players"].apply(safe_list)
    long = df.explode("players").rename(columns={"players":"player_id"})
    long = long[~long["player_id"].isna()]
    out = long.merge(pmap, how="left", on="player_id")
    return out

def explode_starters_from_rosters(rosters_path: Path, pmap: pd.DataFrame) -> pd.DataFrame:
    df = pd.read_csv(rosters_path)
    if "starters" not in df.columns:  # many leagues don’t have starters here
        return pd.DataFrame(columns=["roster_id","player_id","full_name","position","team"])
    df["starters"] = df["starters"].apply(safe_list)
    long = df.explode("starters").rename(columns={"starters":"player_id"})
    long = long[~long["player_id"].isna()]
    return long.merge(pmap, how="left", on="player_id")

def explode_starters_from_matchups(matchups_path: Path, pmap: pd.DataFrame) -> pd.DataFrame:
    df = pd.read_csv(matchups_path)
    if "starters" not in df.columns:
        return pd.DataFrame(columns=["matchup_id","roster_id","player_id","full_name","position","team"])
    df["starters"] = df["starters"].apply(safe_list)
    long = df.explode("starters").rename(columns={"starters":"player_id"})
    keep_cols = [c for c in ["matchup_id","roster_id","roster_id_a","roster_id_b"] if c in df.columns]
    long = long[keep_cols + ["player_id"]] if keep_cols else long[["player_id"]]
    return long.merge(pmap, how="left", on="player_id")

def main():
    pmap = pd.read_csv(PMAP)
    # Find rosters file (support either naming convention)
    candidates = [DATA/"rosters_current.csv", DATA/"rosters.csv"]
    rosters_file = next((p for p in candidates if p.exists()), None)
    if rosters_file:
        rosters_named = explode_rosters(rosters_file, pmap)
        rosters_named.to_csv(DATA/"rosters_with_names.csv", index=False)
        print(f"Wrote data/rosters_with_names.csv ({len(rosters_named):,} rows)")
        # Try starters from this file
        starters_named = explode_starters_from_rosters(rosters_file, pmap)
        if not starters_named.empty:
            starters_named.to_csv(DATA/"starters_with_names.csv", index=False)
            print(f"Wrote data/starters_with_names.csv ({len(starters_named):,} rows)")

    # Try to enrich starters from matchups file if present
    for mname in ["matchups.csv","matchups_1.csv","matchups_current.csv"]:
        mp = DATA / mname
        if mp.exists():
            starters_named = explode_starters_from_matchups(mp, pmap)
            if not starters_named.empty:
                starters_named.to_csv(DATA/"starters_with_names.csv", index=False)
                print(f"Wrote data/starters_with_names.csv ({len(starters_named):,} rows)")

if __name__ == "__main__":
    main()
