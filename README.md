# AI Supply Chain Subnet

## Overview
A decentralized supply chain analytics and optimization platform powered by Bittensor. Logistics experts and AI models collaborate to deliver real-time tracking, predictive analytics, and disruption risk assessments with on-chain transparency.

## Features
- Real-time supply chain tracking and analytics
- Predictive disruption risk assessment
- IoT data aggregation and integration
- Route optimization recommendations
- Bittensor subnet integration with $TAO rewards

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python main.py`
3. Submit tracking queries via `/track` endpoint

## Folder Structure
- `main.py`: Entry point (FastAPI)
- `supplychain/`: Core logic
  - `ai.py`: AI analytics engine
  - `models.py`: Data models (SupplyChainQuery, SupplyChainResponse)
  - `routes.py`: API routes
  - `db.py`: Database operations
- `overview.md`: Full project documentation
- `pitchdeck/`: Presentation materials
- `requirements.txt`: Dependencies

## Bittensor Subnet Design
- **Miner:** Aggregates IoT/ERP data, runs prediction models for delivery and disruption risk
- **Validator:** Verifies prediction accuracy against actual shipment data, scores coverage
- **Incentive:** $TAO rewards based on prediction accuracy and data coverage

## License
MIT

## Full Documentation
See `overview.md` for detailed problem/solution, architecture, and mechanism design.
See `pitchdeck/` for pitch deck, demo video script, and visual guide.
