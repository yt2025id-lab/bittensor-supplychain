from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from supplychain.routes import router as supplychain_router

app = FastAPI(
    title="AI Supply Chain Subnet",
    description="""
## Decentralized Supply Chain Intelligence — Powered by Bittensor & Yuma Consensus

**AI Supply Chain** is a Bittensor subnet that creates a decentralized marketplace for supply chain prediction models.

### How It Works

- **Miners** compete to build AI models that accurately predict delivery times, disruption risks, and optimal shipping routes
- **Validators** verify predictions against actual shipment outcomes using ground truth data
- **Rewards** ($TAO) are distributed based on prediction accuracy via Yuma Consensus

### Miner Tasks

| Task | Weight | Description |
|------|--------|-------------|
| ETA Prediction | 50% | Predict delivery time given origin, destination, product, carrier |
| Disruption Risk | 30% | Predict probability and type of disruption |
| Route Optimization | 20% | Recommend optimal shipping route |

### Scoring Formula

```
final_score = (0.40 x ETA_accuracy + 0.25 x disruption_detection
             + 0.15 x risk_calibration + 0.10 x latency + 0.10 x consistency)
             x 1.5 if disruption correctly predicted
```

### Subnet Parameters
- **Subnet ID:** 6 | **Tempo:** 360 blocks (~72 min) | **Max UIDs:** 256
- **Emission Split:** Owner 18% | Miners 41% | Validators+Stakers 41%

---
*Subnet #6 — AI Supply Chain | Twitter: @Ozan_OnChain*
    """,
    version="1.0.0-beta",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Supply Chain API",
            "description": "User-facing endpoints. Query the subnet for supply chain predictions.",
        },
        {
            "name": "Miners",
            "description": "Miner management — register, list, and run predictions on individual miners.",
        },
        {
            "name": "Validators",
            "description": "Validator operations — generate challenges, dispatch to miners, and score predictions.",
        },
        {
            "name": "Network",
            "description": "Subnet network status, leaderboard, emission distribution, and hyperparameters.",
        },
        {
            "name": "Demo Simulation",
            "description": "Full simulation endpoints — run complete tempo cycles and compare miners side-by-side.",
        },
    ],
)

# API routes
app.include_router(supplychain_router)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse("static/index.html")
