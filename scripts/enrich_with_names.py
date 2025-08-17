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

def safe_read_csv(path: Path) -> pd.DataFrame:
    """Return empty df if file missing/empty/unreadable."""
    try:
        if (not path.exists()) or path.stat().st_size == 0:
            return pd.DataFrame()
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

def explode_rosters(rosters_path: Path, pmap: pd.DataFrame) -> pd.DataFrame:
    df = safe_read_csv(rosters_path)
    if df.empty:
        return pd.DataFrame()
    # Common columns in Sleeper /rosters: roster_id, owner_id, players (list), reserve (list)
    if "players" not in df.columns:
        return pd.DataFrame()
    df["players"] = df["players"].apply(safe_list)
    long = df.explode("players").rename(columns={"players":"player_id"})
    long = long[~long["player_id"].isna()]
    out = long.merge(pmap, how="left", on="player_id")
    return out

def explode_starters_from_rosters(rosters_path: Path, pmap: pd.DataFrame) -> pd.DataFrame:
    df = safe_read_csv(rosters_path)
    if df.empty or "starters" not in df.columns:
        return pd.DataFrame()
    df["starters"] = df["starters"].apply(safe_list)
    long = df.explode("starters").rename(columns={"starters":"player_id"})
    long = long[~long["player_id"].isna()]
    return long.merge(pmap, how="left", on="player_id")

def explode_starters_from_matchups(matchups_path: Path, pmap: pd.DataFrame) -> pd.DataFrame:
    df = safe_read_csv(matchups_path)
    if df.empty or "starters" not in df.columns:
        return pd.DataFrame()
    df["starters"] = df["starters"].apply(safe_list)
    long = df.explode("starters").rename(columns={"starters":"player_id"})
    keep_cols = [c for c in ["matchup_id","roster_id","roster_id_a","roster_id_b","week"] if c in df.columns]
    cols = keep_cols + ["player_id"] if keep_cols else ["player_id"]
    long = long[cols]
    return long.merge(pmap, how="left", on="player_id")

def main():
    if not PMAP.exists():
        raise SystemExit("players_map.csv missing — run sleeper_players_map.py first")

    pmap = pd.read_csv(PMAP)

    # Prefer rosters_current.csv but support rosters.csv
    rosters_file = next((p for p in [DATA/"rosters_current.csv", DATA/"rosters.csv"] if p.exists()), None)

    if rosters_file:
        rosters_named = explode_rosters(rosters_file, pmap)
        if not rosters_named.empty:
            rosters_named.to_csv(DATA/"rosters_with_names.csv", index=False)
            print(f"Wrote data/rosters_with_names.csv ({len(rosters_named):,} rows)")

        starters_named = explode_starters_from_rosters(rosters_file, pmap)
        if not starters_named.empty:
            starters_named.to_csv(DATA/"starters_with_names.csv", index=False)
            print(f"Wrote data/starters_with_names.csv ({len(starters_named):,} rows)")

    # Enrich starters from any matchups file present; skip empty
    for mname in ["matchups.csv","matchups_1.csv","matchups_current.csv"]:
        mp = DATA / mname
        sn = explode_starters_from_matchups(mp, pmap)
        if not sn.empty:
            sn.to_csv(DATA/"starters_with_names.csv", index=False)
            print(f"Updated data/starters_with_names.csv from {mname} ({len(sn):,} rows)")

if __name__ == "__main__":
    main()
