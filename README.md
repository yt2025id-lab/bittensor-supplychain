# AI Supply Chain Subnet

**Subnet #6 — Bittensor Ideathon**

A decentralized supply chain analytics and optimization platform on Bittensor. Miners compete to build accurate logistics prediction models using IoT, ERP, and shipping data. Validators verify predictions against actual delivery outcomes. Rewards ($TAO) are distributed via Yuma Consensus.

## Quick Start (For Judges)

```bash
# 1. Clone & enter directory
git clone https://github.com/yt2025id-lab/bittensor-supplychain.git
cd bittensor-supplychain

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload --port 8000

# 4. Open in browser
open http://localhost:8000
```

### What You'll See

- **Interactive Web UI** at `http://localhost:8000` — click any of the 3 demo scenarios
- **Swagger API Docs** at `http://localhost:8000/docs` — test all endpoints interactively
- **ReDoc** at `http://localhost:8000/redoc` — clean API reference

### Demo Scenarios

| # | Scenario | Task Type |
|---|----------|-----------|
| 1 | Shanghai-Rotterdam container shipment ETA | Delivery Prediction |
| 2 | Suez Canal disruption — reroute risk analysis | Disruption Risk |
| 3 | Semiconductor supply chain — 90-day demand forecast | Demand Forecast |

Each demo broadcasts a supply chain challenge to 6 simulated miners, scores their predictions through 3-4 validators, and distributes TAO rewards via Yuma Consensus.

## Features

- 6 specialized logistics AI miners (RouteOptim, SupplyForecaster, DisruptionNet, etc.)
- 3-4 validators with shipping data verification pipelines
- ETA prediction, disruption risk scoring, demand forecasting
- Real-time scoring: ETA accuracy, risk prediction, coverage, latency
- TAO reward distribution via Yuma Consensus
- Full miner/validator CRUD, leaderboard, and network status APIs

## Folder Structure

```
main.py                  # FastAPI entry point
supplychain/
  __init__.py
  ai.py                  # AI analytics engine (3 demo scenarios, 6 miners)
  db.py                  # In-memory DB (miners, validators, challenges)
  models.py              # Pydantic data models
  routes.py              # 20+ API endpoints
static/
  index.html             # Interactive demo UI
  app.js                 # Frontend logic
  style.css              # Dark theme styling
overview.md              # Full technical documentation
pitchdeck/               # Pitch deck materials
SUBNET_PROPOSAL.md       # Detailed subnet design proposal
```

## Scoring Formula

```
final_score = (0.40 × eta_accuracy + 0.25 × risk_accuracy
             + 0.15 × coverage + 0.10 × latency + 0.10 × consistency)
             × 1.5 if disruption correctly predicted
```

## Subnet Parameters

- **Subnet ID:** 6 | **Tempo:** 360 blocks (~72 min) | **Max UIDs:** 256
- **Emission Split:** Owner 18% | Miners 41% | Validators+Stakers 41%

## Miner Tasks

| Task | Weight | Description |
|------|--------|-------------|
| Delivery Prediction | 50% | ETA prediction for shipments and cargo |
| Disruption Risk | 30% | Supply chain disruption detection and risk scoring |
| Demand Forecast | 20% | 30-90 day demand and inventory prediction |

## License

MIT

## Documentation

- [`SUBNET_PROPOSAL.md`](SUBNET_PROPOSAL.md) — Full technical subnet design proposal
- [`overview.md`](overview.md) — Problem/solution, architecture, mechanism design
- [`pitchdeck/`](pitchdeck/) — Pitch deck and demo video script
