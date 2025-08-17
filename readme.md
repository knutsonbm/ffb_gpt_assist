# Fantasy Football GPT Assist 🏈🤖

This repository automates fantasy football insights by combining:
- **Sleeper API data** (rosters, transactions, matchups, waivers)
- **Custom analytics & simulations** (waiver backtests, lineup optimizations, matchup projections)
- **GitHub Actions workflows** to run analyses on a schedule and store results as artifacts

The goal: deliver **twice-daily league-specific recommendations** (waivers, start/sit, trade targets) and **national context** (injury fallout, weather, matchup previews).

---

## 📂 Repo Structure


---

## ✅ Setup Checklist

- [ ] **0.1** Fork or clone this repo
- [ ] **0.2** Enable GitHub Actions  
  - Go to: `Settings → Actions → General → Allow all actions`
- [ ] **1.1** Add repo secret **LEAGUE_ID**  
  - Set this to your Sleeper league ID (example: `1257452477297479680`)
- [ ] **1.2** Add repo secret **SEASON**  
  - Example: `2025`
- [ ] **1.3** (Optional) Add repo secrets for other APIs  
  - e.g., FantasyPros, SportsDataIO, etc.
- [ ] **2.1** Verify first workflow run under **Actions** tab
- [ ] **2.2** Check artifacts output (CSV logs, results in `Actions → Artifacts`)
- [ ] **3.0** Begin integrating analytics/insights  
  - roster scans, waiver recs, lineup optimizations

---

## ⚙️ Workflows

This repo includes GitHub Actions that run scheduled or manual analyses.

### Example: Waiver Backtests
File: `.github/workflows/backtest.yml`

- Runs simulations across multiple strategies (`safe`, `upside`, `adaptive`)
- Produces CSV + log artifacts
- Stores results under **Actions → Artifacts**

### Example: Twice-Daily League Pull
File: `.github/workflows/league_pull.yml`

- Scheduled to run at **9am** and **5pm ET** daily
- Fetches Sleeper league data (rosters, waivers, matchups)
- Stores structured CSVs in artifacts

---

## 📊 Planned Data Sources

| Type of Data              | Current Source | Notes / Better Options |
|---------------------------|----------------|-------------------------|
| Rosters & Matchups        | Sleeper API    | ✅ Best source (public) |
| Waivers & Transactions    | Sleeper API    | ✅ Real-time and complete |
| Projections (weekly/ROS)  | FantasyPros    | Manual scrape or API proxy |
| Injury Reports            | Subvertadown   | Supplement with NFL injury feeds |
| Weather Impact            | OpenWeather API | Free tier likely sufficient |
| Advanced Stats            | SportsDataIO   | Paid, but powerful (consider later) |

---

## 🚀 Usage

1. Trigger workflows manually:
   - Go to **Actions → Workflow → Run workflow**
2. Or wait for scheduled runs (daily at 9am & 5pm ET)
3. Download results from **Actions → Artifacts**
4. Use outputs (CSVs/logs) for:
   - Waiver recommendations
   - Start/sit optimization
   - Trade ideas
   - Matchup projections

---

## 🔒 Secrets & Security

- **Do not** hardcode your league ID or API keys in scripts.
- Instead, set them under **Repo → Settings → Secrets and variables → Actions**.
- This keeps your private data safe, while still allowing workflows to access it securely.

---

## 📌 Next Steps

- [ ] Add first Sleeper API pull (rosters, matchups, waivers)
- [ ] Validate outputs in artifacts
- [ ] Expand into FantasyPros / Subvertadown data pulls
- [ ] Integrate analytics (waiver rankings, lineup optimization, trade targets)

---

## 🤝 Contributing

This repo is experimental and built for automation of personal fantasy league insights.  
Contributions, forks, and suggestions welcome.

---

## 📄 License

MIT License — free to use and adapt.
