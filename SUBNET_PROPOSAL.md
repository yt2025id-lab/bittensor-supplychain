# AI Supply Chain — Subnet Design Proposal

> **Bittensor Subnet Ideathon 2026**
> Team: AI Supply Chain | Twitter: @Ozan_OnChain | Discord: ozan_onchain

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Incentive & Mechanism Design](#2-incentive--mechanism-design)
3. [Miner Design](#3-miner-design)
4. [Validator Design](#4-validator-design)
5. [Business Logic & Market Rationale](#5-business-logic--market-rationale)
6. [Go-To-Market Strategy](#6-go-to-market-strategy)

---

## 1. Executive Summary

**AI Supply Chain** is a Bittensor subnet that creates a decentralized marketplace for supply chain prediction models. Miners compete to build AI models that accurately predict delivery times, disruption risks, and optimal shipping routes by aggregating data from IoT sensors, shipping APIs, and logistics databases. Validators verify predictions against actual shipment outcomes. The most accurate predictive models earn $TAO emissions, producing a permissionless supply chain intelligence oracle for manufacturers, e-commerce platforms, and logistics providers.

**Digital Commodity Produced:** Accurate supply chain predictions (delivery ETAs, disruption risk scores, route optimizations).

**Proof of Effort:** Miners must produce verifiably accurate logistics predictions. Every prediction is eventually compared against real-world shipment outcomes — the only way to earn rewards is to build models that genuinely predict supply chain behavior.

---

## 2. Incentive & Mechanism Design

### 2.1 Emission and Reward Logic

| Recipient | Share | Description |
|-----------|-------|-------------|
| Subnet Owner | 18% | Funds data partnerships, development, and oracle infrastructure |
| Miners | 41% | Distributed via Yuma Consensus performance scores |
| Validators + Stakers | 41% | Proportional to stake and bond strength |

### 2.2 Incentive Alignment

**For Miners:**
- More accurate delivery predictions + better disruption detection = higher weights = more $TAO.
- Multi-dimensional scoring (ETA accuracy, risk prediction, route optimization) prevents single-metric gaming.
- Disruption detection bonus: 1.5x multiplier for correctly predicting disruptions before they occur.

**For Validators:**
- Bond growth tied to honest evaluation; commit-reveal prevents weight copying.
- Validators with access to actual shipment outcome data produce more accurate evaluations.

**For Stakers:**
- Supply chain analytics is a $22B+ market. API revenue from logistics companies drives alpha token value.

### 2.3 Mechanisms to Discourage Adversarial Behavior

| Threat | Defense Mechanism |
|--------|-------------------|
| **Miners returning average ETAs** | Challenges include diverse routes (local, international, expedited); averaging scores poorly on route-specific predictions |
| **Miners caching predictions** | Random origin-destination pairs with varied conditions; unique seed per challenge |
| **Miners querying public tracking APIs** | Historical challenges (past shipments) + strict 10s timeout |
| **Colluding validators** | Yuma Consensus clipping |
| **Weight-copying validators** | Commit-reveal + Consensus-Based Weights |
| **Model stagnation** | Anti-monopoly decay after 30 tempos |

### 2.4 Proof of Effort

1. **Data integration work:** Effective supply chain prediction requires aggregating and processing diverse data sources (weather, port congestion, geopolitical events).
2. **Verifiable outcomes:** Delivery times and disruption events are objectively measurable after the fact.
3. **Dynamic environment:** Supply chains change daily — models must continuously adapt to new disruptions, routes, and conditions.
4. **Multi-factor modeling:** Accurate prediction requires understanding shipping routes, customs delays, weather impacts, and carrier performance.

### 2.5 High-Level Algorithm

```
EVERY TEMPO (~72 minutes):

  VALIDATOR LOOP:
    1. GENERATE supply chain challenges:
       - HISTORICAL (70%): Past shipments with known outcomes
         - Origin, destination, product type, carrier, date shipped
         - Ground truth: actual delivery time, actual disruptions
       - NEAR-TERM (30%): Active shipments for forward prediction
         - Ground truth verified when shipment completes

    2. DISPATCH to miners via SupplyChainSynapse:
       - origin, destination, product_type, carrier, ship_date, conditions
       - timeout = 10 seconds

    3. COLLECT miner responses:
       - predicted_eta_days, disruption_risk, risk_factors, route_recommendation

    4. SCORE each response:
       - eta_accuracy = 1 - (|predicted_eta - actual_eta| / max_error)     [0-1]
       - disruption_accuracy = correctly_predicted_disruption               [0-1]
       - risk_calibration = 1 - |predicted_risk - actual_disruption_binary| [0-1]
       - latency_score = max(1 - elapsed/10, 0)                            [0-1]
       - consistency = EMA over last 100 rounds                             [0-1]

       - final_score = 0.40 * eta_accuracy
                     + 0.25 * disruption_accuracy
                     + 0.15 * risk_calibration
                     + 0.10 * latency_score
                     + 0.10 * consistency
                     (* 1.5 if correctly predicted disruption event)

    5. UPDATE EMA scores and SUBMIT weights (commit-reveal)

  MINER LOOP:
    1. RECEIVE SupplyChainSynapse
    2. RUN through supply chain prediction model
    3. RETURN predictions (ETA, risk, route recommendation)
    4. CONTINUOUSLY update model with new logistics data
```

---

## 3. Miner Design

### 3.1 Miner Tasks

| Mechanism | Weight | Description |
|-----------|--------|-------------|
| **Delivery ETA Prediction** | 50% | Predict delivery time given origin, destination, product, carrier |
| **Disruption Risk Assessment** | 30% | Predict probability and type of disruption (weather, port congestion, customs, strike) |
| **Route Optimization** | 20% | Recommend optimal shipping route considering cost, time, and risk |

### 3.2 Input → Output Format (Synapse Protocol)

```python
class SupplyChainSynapse(bt.Synapse):
    # ── Immutable Inputs (set by validator) ──
    task_type: str                    # "eta_prediction" | "disruption_risk" | "route_optimization"
    origin: str                       # Origin location (port/city/coordinates)
    destination: str                  # Destination location
    product_type: str                 # Product category (electronics, perishable, bulk, hazmat)
    carrier: Optional[str] = None     # Shipping carrier (if known)
    ship_date: str                    # Shipment date (ISO 8601)
    conditions: Optional[dict] = None # Current conditions (weather, port status, geopolitical)
    random_seed: int

    # ── Mutable Outputs (filled by miner) ──
    predicted_eta_days: Optional[float] = None         # Predicted delivery time in days
    disruption_risk: Optional[float] = None            # Risk score [0.0 - 1.0]
    risk_factors: Optional[List[dict]] = None          # [{factor, probability, impact}]
    route_recommendation: Optional[dict] = None        # {route, estimated_days, estimated_cost}
    confidence: Optional[float] = None                 # Model confidence [0.0 - 1.0]
    data_sources: Optional[List[str]] = None           # Data sources used for prediction
```

**Example Input:**
```json
{
  "task_type": "eta_prediction",
  "origin": "Shanghai, China",
  "destination": "Los Angeles, USA",
  "product_type": "electronics",
  "carrier": "COSCO",
  "ship_date": "2026-02-15",
  "conditions": {
    "weather": "typhoon_warning_western_pacific",
    "port_congestion": "shanghai_moderate",
    "geopolitical": "normal"
  },
  "random_seed": 83920174
}
```

**Example Output:**
```json
{
  "predicted_eta_days": 18.5,
  "disruption_risk": 0.45,
  "risk_factors": [
    {"factor": "typhoon_diversion", "probability": 0.35, "impact_days": 3},
    {"factor": "port_congestion_shanghai", "probability": 0.60, "impact_days": 1.5},
    {"factor": "customs_delay_la", "probability": 0.15, "impact_days": 2}
  ],
  "route_recommendation": {
    "route": "Shanghai → Busan (transship) → Los Angeles",
    "estimated_days": 16,
    "estimated_cost_usd": 3200,
    "rationale": "Transshipment via Busan avoids direct typhoon path"
  },
  "confidence": 0.78,
  "data_sources": ["AIS_vessel_tracking", "NOAA_weather", "port_congestion_API"]
}
```

### 3.3 Performance Dimensions

| Dimension | Weight | Metric | Description |
|-----------|--------|--------|-------------|
| **ETA Accuracy** | 40% | `1 - (abs(predicted - actual) / max_error)` | max_error = 7 days |
| **Disruption Detection** | 25% | Binary: correctly predicted disruption event | 1.5x bonus for correct disruption prediction |
| **Risk Calibration** | 15% | `1 - abs(risk_score - actual_outcome)` | Risk score should reflect actual disruption probability |
| **Response Latency** | 10% | `max(1 - elapsed/10s, 0)` | Speed of prediction |
| **Consistency** | 10% | EMA over 100 rounds | Sustained accuracy |

### 3.4 Miner Hardware & Data Requirements

| Tier | Hardware | Data Sources |
|------|----------|-------------|
| Entry | 8-core CPU, 32GB RAM, RTX 3060 | Public shipping APIs, weather data |
| Mid | 16-core CPU, 64GB RAM, A5000 | AIS vessel tracking, port APIs, historical logistics data |
| High | 32-core CPU, 128GB RAM, A100 | Real-time IoT feeds, ERP integrations, satellite imagery |

---

## 4. Validator Design

### 4.1 Scoring and Evaluation Methodology

**Ground Truth Sources:**

| Source | Data | Usage |
|--------|------|-------|
| Historical shipment databases | Actual delivery times, routes, delays | Primary ground truth for ETA challenges |
| AIS (Automatic Identification System) | Real-time vessel positions | Verify route predictions |
| Port authority data | Actual congestion levels, throughput | Verify disruption predictions |
| Carrier tracking APIs | Actual shipment milestones | ETA verification |
| Weather observation data | Actual weather events | Disruption event verification |

**Challenge Strategy:**
```
Historical Challenges (70%):
  - Past shipments with complete outcome data
  - Immediate scoring possible
  - Prevents miners from querying live tracking APIs

Near-Term Challenges (30%):
  - Active/recent shipments
  - Ground truth verified when shipment completes (3-30 days)
  - Tests actual predictive ability
  - Delayed scoring with deferred reward allocation
```

### 4.2 Evaluation Cadence

| Action | Frequency |
|--------|-----------|
| Historical challenges | Every tempo (2-3 per miner) |
| Near-term challenges | Every 6 tempos (1 per miner) |
| EMA update | After each scored challenge |
| Weight submission | Every 100 blocks |
| Commit-reveal | 1 tempo delay |
| Outcome verification | Daily (for completed near-term shipments) |

### 4.3 Validator Incentive Alignment

1. **Bond Growth:** Independent, honest evaluation builds stronger EMA bonds.
2. **Commit-Reveal:** 1-tempo encryption prevents weight copying.
3. **Data Quality:** Validators with better ground truth data produce more accurate scores, aligning with consensus.

---

## 5. Business Logic & Market Rationale

### 5.1 The Problem and Why It Matters

- Supply chain disruptions cost **$184B+ annually** globally.
- **65%** of supply chain leaders cite lack of real-time visibility as their top challenge.
- Enterprise supply chain analytics tools cost **$50,000-$500,000/year** — inaccessible for SMBs.
- Existing solutions (SAP, Oracle) are centralized, siloed, and slow to adapt.

**Market Size:**
- Supply chain analytics: **$22.3B by 2028** (MarketsandMarkets).
- Supply chain management software: **$30.9B by 2026**.
- IoT in logistics: **$40B+** and growing.

### 5.2 Competing Solutions

**Within Bittensor:**
- No direct supply chain subnet exists — **first-mover advantage**.

**Outside Bittensor:**

| Solution | Limitation | Our Advantage |
|----------|-----------|---------------|
| FourKites / Project44 | Enterprise-only, $50K+/year | Pay-per-query, permissionless |
| SAP Integrated Business Planning | Expensive, complex, vendor lock-in | Open, decentralized, API-first |
| Flexport | Proprietary, limited to their network | Network-agnostic, aggregates all carriers |
| Chainlink (supply chain oracle) | Relays data, no AI prediction | AI-powered predictions, not just data relay |

### 5.3 Why Bittensor Is Well-Suited

1. **Verifiable outcomes:** Shipment deliveries have definitive, measurable outcomes.
2. **Competitive improvement:** Multiple miners optimizing predictions beats any single provider.
3. **Data aggregation incentive:** Miners are financially motivated to integrate diverse data sources.
4. **Oracle-native design:** Predictions can feed directly into smart contracts (insurance, trade finance).

### 5.4 Path to Long-Term Adoption

**Phase 1 (Month 1-3):** Launch with ocean freight ETA prediction (Shanghai↔LA, Rotterdam↔NY top routes).
**Phase 2 (Month 4-6):** Add disruption risk mechanism; first logistics company API integration.
**Phase 3 (Month 7-12):** Multi-modal (air, rail, truck); enterprise tier; trade finance smart contract integration.
**Phase 4 (Year 2+):** Real-time IoT data marketplace; customs prediction; carbon footprint optimization.

---

## 6. Go-To-Market Strategy

### 6.1 Initial Target Users & Use Cases

| Segment | Use Case | Value Proposition |
|---------|----------|-------------------|
| **E-commerce platforms** | Delivery ETA for customers | Accurate ETAs improve customer satisfaction by 30% |
| **3PL providers** | Route optimization and risk assessment | Reduce costs 10-15% through better routing |
| **Trade finance / DeFi** | Smart contract triggers based on shipment status | Trustless, on-chain verified logistics data |
| **Insurance (parametric)** | Automated claims for supply chain disruptions | Real-time disruption detection triggers payouts |

### 6.2 Distribution & Growth Channels

- Oracle smart contract on EVM chains for DeFi/trade finance integration.
- Open-source SDK (Python, JavaScript) for logistics platforms.
- Partnership with shipping marketplaces (Freightos, Flexport API).
- Industry conferences (LogiMAT, CSCMP, Manifest).

### 6.3 Incentives for Early Participation

**For Early Miners:** Low competition, high per-miner emissions; pre-trained models and data source guides provided.
**For Early Validators:** Early bond accumulation; access to historical shipment datasets.
**For Early Users/Stakers:** Alpha token at lowest price; free tier during beta (10,000 queries/month).

**Bootstrapping Timeline:**
1. **Week 1-2:** Reference miner + validator; publish baseline ETA accuracy.
2. **Week 3-4:** Miner onboarding with shipping route datasets and model guides.
3. **Month 2:** Public API; first e-commerce integration pilot.
4. **Month 3:** Disruption risk mechanism; first logistics company partnership.

---

## Appendix

### A. Subnet Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `MaxAllowedUids` | 256 | Diverse route/region specialization |
| `MaxAllowedValidators` | 64 | Standard default |
| `ImmunityPeriod` | 5000 blocks | ~7 hours protection |
| `WeightsRateLimit` | 100 blocks | ~20 min between updates |
| `CommitRevealPeriod` | 1 tempo | Anti-weight-copying |
| `Tempo` | 360 blocks | ~72 min evaluation cycle |

### B. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Low miner participation | Subnet owner runs reference miners; provide pre-trained models + datasets |
| Delayed ground truth (near-term) | 70% historical challenges for immediate scoring; deferred rewards for near-term |
| Data source reliability | Multiple redundant sources; fallback to historical averages |
| Disruption over-prediction | Risk calibration metric penalizes consistently high risk scores |

---

*This proposal was prepared for the Bittensor Subnet Ideathon 2026.*
*GitHub: https://github.com/yt2025id-lab/bittensor-supplychain*
