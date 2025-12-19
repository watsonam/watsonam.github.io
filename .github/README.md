# Power Market Data Scrapers - GitHub Actions

This repository automatically scrapes UK power market data daily using GitHub Actions.

## What gets scraped:

### 🔌 Nord Pool
- UK electricity prices (£/MWh)
- Trading volumes (MWh)
- 24 hourly periods per day

### ⚡ EPEX SPOT
- GB continuous market data (30-min periods)
- GB auction data (IDA1, IDA2, IDA3)
- Baseload and peakload prices

### 📊 Elexon
- UK demand outturn stream
- Balancing costs analysis
- Generator acceptances with fuel types

## Automation

- **Schedule**: Runs daily at 6 AM UTC
- **Manual**: Can be triggered manually via GitHub Actions tab
- **Data**: Automatically committed to `power_research/data/` directories

## Local Development

```bash
# Setup virtual environment
uv venv .venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Run individual scrapers
python power_research/scrapers/nordpool.py
python power_research/scrapers/epexspot.py
python power_research/scrapers/elexon.py
```

## Data Structure

```
power_research/data/
├── nordpool/
│   ├── prices/
│   └── volumes/
├── epexspot/
│   └── GB/product_30/
├── epexspot_auction/
│   └── GB/GB-IDA1/product_30/
└── elexon/
    ├── *_demand_outturn.csv
    ├── *_balancing_costs.csv
    └── *_acceptances.csv
```

All files are named with ISO date format: `YYYY-MM-DD`