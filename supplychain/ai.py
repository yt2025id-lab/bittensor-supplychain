"""
AI Supply Chain Prediction Engine
Simulates realistic miner AI models and validator scoring for supply chain subnet.
Each demo scenario has specialized miners and validators with unique analysis.
"""

import random
import hashlib
import time
from datetime import datetime


# ============================================================
# SPECIALIZED MINERS & VALIDATORS PER SCENARIO
# Each scenario has dedicated miners with unique names,
# specialties, and analysis patterns — just like a real subnet.
# ============================================================

SPECIALISTS = {
    "eta_prediction": {
        "miners": [
            {"name": "DeepLogistics-v3",     "hotkey": "5FHL7kQr", "tier": "high", "specialty": "Deep Learning ETA Model (Transformer)"},
            {"name": "SupplyNet-Transformer", "hotkey": "5FSnT9xP", "tier": "high", "specialty": "Multi-modal Transit Time Prediction"},
            {"name": "ShipPredict-LSTM",      "hotkey": "5FSPl3mK", "tier": "mid",  "specialty": "LSTM-based Shipping Time Forecasting"},
            {"name": "FreightForecaster-v2",  "hotkey": "5FFfV2nR", "tier": "mid",  "specialty": "Gradient Boosted ETA Prediction"},
            {"name": "LogiSense-RF",          "hotkey": "5FLsR4pT", "tier": "mid",  "specialty": "Random Forest Logistics Model"},
            {"name": "BasicETA-v1",           "hotkey": "5FBe1qUm", "tier": "entry","specialty": "Rule-based ETA Calculator"},
        ],
        "validators": [
            {"name": "GroundTruth-Oracle",     "hotkey": "5VgT1aXp", "specialty": "Historical shipment database cross-check"},
            {"name": "AIS-Verifier-Pro",       "hotkey": "5VaV2bYq", "specialty": "AIS vessel position verification"},
            {"name": "CarrierTrack-Validator",  "hotkey": "5VcT3cZr", "specialty": "Carrier tracking API milestone verification"},
            {"name": "PortData-Checker",        "hotkey": "5VpD4dAs", "specialty": "Port authority throughput data validation"},
        ],
        "check_labels": ["ETA Within Tolerance", "Route Verified via AIS", "Carrier Milestone Match"],
        "analyses": [
            "Transformer model analysis: Predicted ETA based on 14,832 historical shipments on this route. Applied attention weights to vessel speed (12.3 knots avg), port dwell time (Shanghai: 2.1 days), and seasonal weather patterns. Model accounts for Chinese New Year congestion surge (+1.8 days historical avg).",
            "Multi-modal prediction: Combined AIS vessel tracking data (current position: 32.1°N, 145.2°E, speed 13.1 kn) with real-time port queue data (LA berth utilization: 87%). Weather overlay from NOAA indicates clear Pacific crossing. ETA confidence interval: ±1.2 days at 90% CI.",
            "LSTM sequence model: Fed 180-day rolling window of transit times for this carrier-route pair. Detected upward trend in Shanghai dwell times (+0.4 days/month). Model captures weekly cyclicality — Monday departures historically 0.8 days faster than Friday. Factored carrier schedule reliability: 76%.",
            "Gradient boosted model: 847 features including port congestion indices, fuel prices, and carrier fleet utilization. Top feature importance: Shanghai TEU throughput (22%), Pacific weather index (18%), carrier on-time performance (15%). Ensemble of 500 trees with depth 8.",
            "Random forest analysis: Aggregated predictions from 200 decision trees. Key splits: carrier type (COSCO vs Maersk show 1.2 day difference on this route), product weight class, and booking lead time. Out-of-bag error: 1.4 days MAE.",
            "Rule-based calculation: Base transit time from port-to-port distance (6,380 nm ÷ 13 knots = 20.4 sailing days) + estimated port dwell (Shanghai: 2 days, LA: 1.5 days) + customs buffer (1 day). Applied seasonal adjustment factor: 1.05 for Q1.",
        ],
    },
    "disruption_risk": {
        "miners": [
            {"name": "RiskSense-AI",         "hotkey": "5FRs7kQr", "tier": "high", "specialty": "Multi-source Disruption Detection"},
            {"name": "TyphoonTracker-Pro",    "hotkey": "5FTtP9xP", "tier": "high", "specialty": "Weather & Natural Disaster Prediction"},
            {"name": "GeoPolitical-Monitor",  "hotkey": "5FGmL3mK", "tier": "mid",  "specialty": "Geopolitical Risk Intelligence"},
            {"name": "PortWatch-v3",          "hotkey": "5FPwV2nR", "tier": "mid",  "specialty": "Port Congestion & Strike Detection"},
            {"name": "SupplyRisk-Detector",   "hotkey": "5FSrR4pT", "tier": "mid",  "specialty": "Supply Chain Cascade Risk Analysis"},
            {"name": "AlertBasic-v1",         "hotkey": "5FAb1qUm", "tier": "entry","specialty": "Public Feed Risk Aggregator"},
        ],
        "validators": [
            {"name": "NOAA-WeatherVerifier",   "hotkey": "5VnW1aXp", "specialty": "NOAA/JMA weather observation cross-check"},
            {"name": "PortAuthority-Oracle",   "hotkey": "5VpA2bYq", "specialty": "Port authority real-time data validation"},
            {"name": "NewsCorrelation-Node",    "hotkey": "5VnC3cZr", "specialty": "News/Reuters event correlation verification"},
        ],
        "check_labels": ["Weather Data Confirmed", "Port Status Verified", "Risk Score Calibrated"],
        "analyses": [
            "Multi-source analysis: Detected Typhoon Gaemi (Category 3) forming at 18.2°N, 128.5°E — projected path crosses major Shanghai-LA shipping lane within 72 hours. AIS data shows 14 vessels already diverting via Busan. Historical analysis: similar typhoons caused average 3.2 day delays with 68% probability of port closure at Shanghai.",
            "Weather model: ECMWF ensemble (51 members) shows 78% probability of tropical storm force winds along direct route between Day 3-5 of transit. Wave height forecast: 4.5-6.2m significant wave height. Recommended departure delay: 48 hours or diversion via northern route (+2 days, -35% risk).",
            "Geopolitical intelligence: Red Sea security level elevated — 3 vessel incidents reported in last 14 days near Bab el-Mandeb strait. Suez Canal northbound queue: 47 vessels (normal: 25-30). EU sanctions package #14 adds new compliance requirements for electronics cargo — customs processing time increase estimated at +1.5 days.",
            "Port congestion alert: Shanghai Yangshan Phase 4 terminal operating at 94% capacity (normal: 75-80%). Berth waiting time: 3.2 days (48-hour trend: increasing). Contributing factors: post-holiday cargo surge, 2 gantry cranes offline for maintenance. Automated terminal (Phase 4) partially mitigating — throughput up 12% vs Phase 3.",
            "Cascade risk analysis: Suez Canal congestion (47-vessel queue) will propagate to Rotterdam in 18-22 days, increasing berth wait by estimated 1.8 days. Combined with Hamburg dockworkers' union negotiations (strike probability: 35% within 30 days), Europe-bound cargo faces compounding delay risk. Recommended: book alternative routing via Piraeus transshipment.",
            "Public feed aggregation: Reuters reports port congestion at major Chinese ports. OpenWeather API shows storm system developing in Western Pacific. MarineTraffic density index for East China Sea: HIGH. Combined risk flags: 3/5 sources indicate elevated disruption probability.",
        ],
    },
    "route_optimization": {
        "miners": [
            {"name": "RouteOptimus-AI",      "hotkey": "5FRo7kQr", "tier": "high", "specialty": "Multi-objective Route Optimization (Pareto)"},
            {"name": "CostMinimizer-Pro",     "hotkey": "5FCmP9xP", "tier": "high", "specialty": "Cost-optimized Route Selection"},
            {"name": "TransitPlanner-v4",     "hotkey": "5FTpL3mK", "tier": "mid",  "specialty": "Multi-modal Transit Planning"},
            {"name": "GreenRoute-Optimizer",  "hotkey": "5FGrV2nR", "tier": "mid",  "specialty": "Carbon-optimized Routing"},
            {"name": "SafeShip-Navigator",    "hotkey": "5FSsR4pT", "tier": "mid",  "specialty": "Risk-minimized Route Selection"},
            {"name": "DirectRoute-v1",        "hotkey": "5FDr1qUm", "tier": "entry","specialty": "Shortest Path Calculator"},
        ],
        "validators": [
            {"name": "FuelPrice-Verifier",    "hotkey": "5VfP1aXp", "specialty": "Real-time bunker fuel price verification"},
            {"name": "Schedule-Validator",     "hotkey": "5VsV2bYq", "specialty": "Carrier schedule and port slot verification"},
            {"name": "CostBenchmark-Oracle",   "hotkey": "5VcB3cZr", "specialty": "Freight rate benchmark cross-check"},
            {"name": "EmissionCalc-Checker",   "hotkey": "5VeC4dAs", "specialty": "CO2 emission calculation verification"},
        ],
        "check_labels": ["Cost Estimate Verified", "Schedule Feasible", "Route Exists in Network"],
        "analyses": [
            "Pareto-optimal analysis: Evaluated 12 candidate routes across 3 objectives (cost, time, risk). Pareto front contains 4 non-dominated solutions. Recommended route achieves 89th percentile on combined utility function. Key trade-off: transshipment via Busan adds $400 (+12.5% cost) but reduces typhoon exposure by 65% and saves 2 sailing days via great circle routing.",
            "Cost optimization: Current SCFI (Shanghai Containerized Freight Index) for USWC: $2,847/FEU. Spot rate via Busan transshipment: $3,210/FEU (+$363). However, insurance premium reduction for typhoon avoidance: -$180/FEU. Net cost difference: +$183/FEU. Break-even if delay probability >31% (current estimate: 45%). Recommendation: transship via Busan.",
            "Multi-modal planning: Ocean leg Shanghai → Long Beach (12 days) + rail Long Beach → Chicago (4 days) + truck Chicago → destination (1 day). Total door-to-door: 17 days. Alternative: all-water via Panama Canal to East Coast: 25 days, -$800 cost. Recommendation depends on time sensitivity of electronics cargo — ocean+rail for time-critical, all-water for cost-sensitive.",
            "Carbon-optimized routing: Direct route CO2: 847 kg/TEU (HFO, speed 14 kn). Slow-steaming option (11 kn): 612 kg/TEU (-28%) but +4 days. LNG-powered vessel via Busan: 534 kg/TEU (-37%), +1 day, +$150. Methanol-powered available Rotterdam→NY: 289 kg/TEU (-66%). Recommended for ESG-committed shippers: LNG via Busan (best time/emission trade-off).",
            "Risk-minimized routing: Evaluated 8 routes for cumulative risk exposure. Direct route risk index: 0.45 (typhoon + congestion). Northern great circle via Aleutians: 0.18 risk but +5 days and +$600. Busan transshipment: 0.22 risk, +2 days, +$400. Yokohama transshipment: 0.28 risk, +3 days, +$500. Recommendation: Busan route offers best risk/time ratio at 0.11 risk per day.",
            "Shortest path calculation: Direct Shanghai → Los Angeles via great circle: 5,654 nm. Via Busan: 6,120 nm (+466 nm, +1.5 days at 13 kn). Via Yokohama: 5,890 nm (+236 nm, +0.8 days). Direct route remains shortest but weather routing may add 200-400 nm for storm avoidance.",
        ],
    },
}


# ── 3 PRE-BUILT DEMO SCENARIOS ──

DEMO_SCENARIOS = {
    "demo1": {
        "title": "Ocean Freight ETA Prediction — Shanghai to Los Angeles",
        "subtitle": "Typhoon warning in Western Pacific, Shanghai port congestion moderate",
        "task_type": "eta_prediction",
        "synapse": {
            "task_type": "eta_prediction",
            "origin": "Shanghai, China",
            "destination": "Los Angeles, USA",
            "product_type": "electronics",
            "carrier": "COSCO",
            "ship_date": "2026-02-15",
            "conditions": {
                "weather": "typhoon_warning_western_pacific",
                "port_congestion": "shanghai_moderate",
                "geopolitical": "normal",
            },
            "random_seed": 42001,
        },
        "ground_truth": {
            "actual_eta_days": 18.0,
            "had_disruption": True,
            "disruption_type": "typhoon_diversion",
        },
    },
    "demo2": {
        "title": "Disruption Risk Assessment — Shenzhen to Hamburg via Suez",
        "subtitle": "Red Sea security elevated, Suez Canal congestion, EU customs changes",
        "task_type": "disruption_risk",
        "synapse": {
            "task_type": "disruption_risk",
            "origin": "Shenzhen, China",
            "destination": "Hamburg, Germany",
            "product_type": "electronics",
            "carrier": "Evergreen",
            "ship_date": "2026-03-01",
            "conditions": {
                "weather": "normal",
                "port_congestion": "shanghai_high",
                "geopolitical": "elevated",
            },
            "random_seed": 42002,
        },
        "ground_truth": {
            "actual_eta_days": 35.0,
            "had_disruption": True,
            "disruption_type": "suez_congestion_and_security",
        },
    },
    "demo3": {
        "title": "Route Optimization — Busan to Long Beach (Multi-option)",
        "subtitle": "Pacific storm developing, comparing direct vs transshipment routes",
        "task_type": "route_optimization",
        "synapse": {
            "task_type": "route_optimization",
            "origin": "Busan, South Korea",
            "destination": "Long Beach, USA",
            "product_type": "perishable",
            "carrier": "HMM",
            "ship_date": "2026-02-20",
            "conditions": {
                "weather": "pacific_storm",
                "port_congestion": "normal",
                "geopolitical": "normal",
            },
            "random_seed": 42003,
        },
        "ground_truth": {
            "actual_eta_days": 15.0,
            "had_disruption": False,
            "disruption_type": None,
        },
    },
}


# ── Route & condition data (kept from before) ──

ROUTE_DATABASE = {
    ("Shanghai, China", "Los Angeles, USA"): {"base_days": 14, "variance": 3, "base_cost": 2800, "risk_baseline": 0.20},
    ("Rotterdam, Netherlands", "New York, USA"): {"base_days": 10, "variance": 2, "base_cost": 2200, "risk_baseline": 0.12},
    ("Shenzhen, China", "Hamburg, Germany"): {"base_days": 28, "variance": 5, "base_cost": 4500, "risk_baseline": 0.25},
    ("Tokyo, Japan", "Singapore"): {"base_days": 7, "variance": 1, "base_cost": 1500, "risk_baseline": 0.10},
    ("Mumbai, India", "Dubai, UAE"): {"base_days": 4, "variance": 1, "base_cost": 900, "risk_baseline": 0.08},
    ("Busan, South Korea", "Long Beach, USA"): {"base_days": 12, "variance": 2, "base_cost": 2600, "risk_baseline": 0.15},
}

WEATHER_IMPACTS = {
    "typhoon_warning_western_pacific": {"delay_days": 3, "risk_increase": 0.25},
    "north_atlantic_storm": {"delay_days": 2, "risk_increase": 0.20},
    "monsoon_indian_ocean": {"delay_days": 2, "risk_increase": 0.15},
    "pacific_storm": {"delay_days": 2, "risk_increase": 0.18},
    "clear": {"delay_days": 0, "risk_increase": 0.0},
    "normal": {"delay_days": 0, "risk_increase": 0.0},
}

PORT_CONGESTION_IMPACTS = {
    "shanghai_moderate": {"delay_days": 1.5, "risk_increase": 0.10},
    "shanghai_high": {"delay_days": 3, "risk_increase": 0.20},
    "la_moderate": {"delay_days": 1, "risk_increase": 0.08},
    "normal": {"delay_days": 0, "risk_increase": 0.0},
    "low": {"delay_days": 0, "risk_increase": 0.0},
}

PRODUCT_RISK_MULTIPLIERS = {
    "electronics": 1.0, "perishable": 1.5, "bulk": 0.8, "hazmat": 1.3, "general": 0.9,
}


# ============================================================
# MAIN DEMO ENGINE
# ============================================================

def _generate_miner_responses(task_type, synapse, ground_truth, num_miners=6):
    """Generate specialized miner responses with unique analysis per miner."""
    spec = SPECIALISTS.get(task_type, SPECIALISTS["eta_prediction"])
    pool = spec["miners"]
    num = min(num_miners, len(pool))
    selected = pool[:num]  # Deterministic for demo consistency
    analyses = spec["analyses"]

    route_key = (synapse["origin"], synapse["destination"])
    route = ROUTE_DATABASE.get(route_key, {"base_days": 15, "base_cost": 3000, "risk_baseline": 0.20})

    conditions = synapse.get("conditions") or {}
    weather = conditions.get("weather", "normal")
    congestion = conditions.get("port_congestion", "normal")
    weather_delay = WEATHER_IMPACTS.get(weather, {}).get("delay_days", 0)
    congestion_delay = PORT_CONGESTION_IMPACTS.get(congestion, {}).get("delay_days", 0)

    actual_eta = ground_truth.get("actual_eta_days", route["base_days"] + weather_delay + congestion_delay)

    miners = []
    for i, miner in enumerate(selected):
        rng = random.Random(synapse.get("random_seed", 42) + i * 7)

        # Tier-based prediction quality
        tier = miner["tier"]
        if tier == "high":
            eta_error = rng.gauss(0, 0.8)
            score = round(rng.uniform(0.82, 0.97), 4)
            response_time = round(rng.uniform(0.3, 1.2), 2)
        elif tier == "mid":
            eta_error = rng.gauss(0, 1.5)
            score = round(rng.uniform(0.62, 0.82), 4)
            response_time = round(rng.uniform(0.8, 2.2), 2)
        else:
            eta_error = rng.gauss(0, 2.5)
            score = round(rng.uniform(0.40, 0.62), 4)
            response_time = round(rng.uniform(1.5, 3.5), 2)

        # Top miner gets best score
        if i == 0:
            score = round(rng.uniform(0.93, 0.99), 4)
            response_time = round(rng.uniform(0.2, 0.6), 2)
            eta_error = rng.gauss(0, 0.3)

        predicted_eta = round(actual_eta + eta_error, 1)
        predicted_eta = max(1.0, predicted_eta)

        base_risk = route["risk_baseline"]
        w_risk = WEATHER_IMPACTS.get(weather, {}).get("risk_increase", 0)
        c_risk = PORT_CONGESTION_IMPACTS.get(congestion, {}).get("risk_increase", 0)
        disruption_risk = round(min(1.0, base_risk + w_risk + c_risk + rng.gauss(0, 0.05)), 2)
        disruption_risk = max(0.0, disruption_risk)

        hk = miner["hotkey"]
        miners.append({
            "uid": i + 1,
            "hotkey": f"{hk}...{hashlib.md5(hk.encode()).hexdigest()[:6]}",
            "name": miner["name"],
            "tier": tier,
            "specialty": miner["specialty"],
            "predicted_eta_days": predicted_eta,
            "disruption_risk": disruption_risk,
            "confidence": round(rng.uniform(0.6, 0.95) if tier != "entry" else rng.uniform(0.4, 0.65), 2),
            "score": score,
            "response_time_s": response_time,
            "analysis": analyses[i] if i < len(analyses) else analyses[-1],
            "rank": i + 1,
        })

    # Sort by score descending
    miners.sort(key=lambda m: m["score"], reverse=True)
    for i, m in enumerate(miners):
        m["rank"] = i + 1

    return miners


def _generate_validator_results(task_type, num_validators=3):
    """Generate specialized validator verification results."""
    spec = SPECIALISTS.get(task_type, SPECIALISTS["eta_prediction"])
    pool = spec["validators"]
    num = min(num_validators, len(pool))
    selected = pool[:num]
    check_labels = spec["check_labels"]

    validators = []
    for j, val in enumerate(selected):
        rng = random.Random(42 + j * 13)
        hk = val["hotkey"]
        stake = round(rng.uniform(5000, 18000), 2)
        vtrust = round(rng.uniform(0.88, 0.99), 4)

        checks = {}
        checks_passed = 0
        for label in check_labels:
            passed = rng.random() < 0.85  # 85% pass rate
            checks[label] = passed
            if passed:
                checks_passed += 1

        validators.append({
            "uid": j + 1,
            "hotkey": f"{hk}...{hashlib.md5(hk.encode()).hexdigest()[:6]}",
            "name": val["name"],
            "specialty": val["specialty"],
            "stake_tao": stake,
            "vtrust": vtrust,
            "checks_passed": checks_passed,
            "checks_total": len(check_labels),
            "check_details": checks,
            "consensus": "Approved" if checks_passed >= 2 else "Disputed",
        })

    return validators


def run_demo_scenario(scenario_key: str) -> dict:
    """Run one of the 3 pre-built demo scenarios with full miner/validator output."""
    scenario = DEMO_SCENARIOS.get(scenario_key)
    if not scenario:
        return {"error": f"Unknown scenario: {scenario_key}"}

    task_type = scenario["task_type"]
    synapse = scenario["synapse"]
    ground_truth = scenario["ground_truth"]

    miner_responses = _generate_miner_responses(task_type, synapse, ground_truth, num_miners=6)
    validator_results = _generate_validator_results(task_type, num_validators=3)

    total_tao = round(random.Random(42).uniform(0.08, 0.42), 4)

    # Assign TAO to miners based on score
    total_score = sum(m["score"] for m in miner_responses)
    for m in miner_responses:
        m["tao_earned"] = round(total_tao * 0.41 * (m["score"] / total_score), 6) if total_score > 0 else 0

    return {
        "scenario": scenario_key,
        "title": scenario["title"],
        "subtitle": scenario["subtitle"],
        "task_type": task_type,
        "synapse": synapse,
        "ground_truth": ground_truth,
        "miner_responses": miner_responses,
        "miner_nodes_consulted": len(miner_responses),
        "validator_results": validator_results,
        "validator_nodes_consulted": len(validator_results),
        "tao_reward_pool": total_tao,
        "consensus_reached": all(v["consensus"] == "Approved" for v in validator_results),
        "block_number": random.randint(2_800_000, 3_200_000),
        "tempo": random.randint(7900, 8100),
        "timestamp": datetime.utcnow().isoformat(),
        "subnet_version": "1.0.0-beta",
    }


def get_demo_scenarios_list():
    """Return metadata for all 3 demo scenarios."""
    return [
        {
            "key": key,
            "title": s["title"],
            "subtitle": s["subtitle"],
            "task_type": s["task_type"],
            "origin": s["synapse"]["origin"],
            "destination": s["synapse"]["destination"],
            "product_type": s["synapse"]["product_type"],
            "carrier": s["synapse"]["carrier"],
            "conditions": s["synapse"]["conditions"],
        }
        for key, s in DEMO_SCENARIOS.items()
    ]


# ============================================================
# LEGACY FUNCTIONS (used by Swagger API endpoints)
# ============================================================

def run_miner_prediction(synapse_dict: dict, tier: str) -> dict:
    """Simulate a miner processing a supply chain challenge (for Swagger endpoints)."""
    rng = random.Random(synapse_dict.get("random_seed", int(time.time())))

    route_key = (synapse_dict.get("origin", ""), synapse_dict.get("destination", ""))
    route = ROUTE_DATABASE.get(route_key, {"base_days": 15, "variance": 3, "base_cost": 3000, "risk_baseline": 0.20})

    conditions = synapse_dict.get("conditions") or {}
    weather = conditions.get("weather", "normal")
    congestion = conditions.get("port_congestion", "normal")
    product = synapse_dict.get("product_type", "general")

    weather_impact = WEATHER_IMPACTS.get(weather, {"delay_days": 0, "risk_increase": 0})
    congestion_impact = PORT_CONGESTION_IMPACTS.get(congestion, {"delay_days": 0, "risk_increase": 0})
    product_mult = PRODUCT_RISK_MULTIPLIERS.get(product, 1.0)

    # Tier-based quality
    if tier == "high":
        noise = rng.gauss(0, route["variance"] * 0.3)
        confidence = round(rng.uniform(0.82, 0.96), 2)
        latency = round(rng.uniform(200, 800), 0)
        data_sources = rng.randint(8, 15)
    elif tier == "mid":
        noise = rng.gauss(0, route["variance"] * 0.6)
        confidence = round(rng.uniform(0.65, 0.82), 2)
        latency = round(rng.uniform(500, 2000), 0)
        data_sources = rng.randint(4, 9)
    else:
        noise = rng.gauss(0, route["variance"] * 1.2)
        confidence = round(rng.uniform(0.40, 0.65), 2)
        latency = round(rng.uniform(1500, 4000), 0)
        data_sources = rng.randint(1, 5)

    predicted_eta = round(route["base_days"] + weather_impact["delay_days"] + congestion_impact["delay_days"] + noise, 1)
    predicted_eta = max(1.0, predicted_eta)

    disruption_risk = round(min(1.0, (route["risk_baseline"] + weather_impact["risk_increase"] + congestion_impact["risk_increase"]) * product_mult + rng.gauss(0, 0.05)), 2)
    disruption_risk = max(0.0, disruption_risk)

    risk_factors = []
    if weather_impact["delay_days"] > 0:
        risk_factors.append({"factor": weather.replace("_", " ").title(), "severity": round(weather_impact["risk_increase"] * 5, 1), "description": f"Weather event may add {weather_impact['delay_days']} days"})
    if congestion_impact["delay_days"] > 0:
        risk_factors.append({"factor": congestion.replace("_", " ").title(), "severity": round(congestion_impact["risk_increase"] * 5, 1), "description": f"Port congestion may add {congestion_impact['delay_days']} days"})
    if product_mult > 1.1:
        risk_factors.append({"factor": f"{product.title()} cargo", "severity": round((product_mult - 1.0) * 3, 1), "description": "Product type adds handling risk"})

    return {
        "miner_uid": 0,
        "miner_hotkey": "",
        "predicted_eta_days": predicted_eta,
        "disruption_risk": disruption_risk,
        "confidence": confidence,
        "risk_factors": risk_factors,
        "route_recommendation": f"{'Direct route' if disruption_risk < 0.3 else 'Consider alternative routing'} — {synapse_dict.get('origin', '')} to {synapse_dict.get('destination', '')}",
        "response_time_ms": latency,
        "data_sources": data_sources,
    }


def score_prediction(prediction: dict, ground_truth: dict) -> dict:
    """Score a miner prediction against ground truth (for Swagger endpoints)."""
    rng = random.Random(hash(str(prediction.get("miner_hotkey", ""))) % 2**31)

    actual_eta = ground_truth.get("actual_eta_days", 15.0)
    predicted_eta = prediction.get("predicted_eta_days", 15.0)
    eta_accuracy = round(max(0, 1.0 - abs(predicted_eta - actual_eta) / 7.0), 4)

    had_disruption = ground_truth.get("had_disruption", False)
    predicted_risk = prediction.get("disruption_risk", 0.0)
    predicted_disruption = predicted_risk > 0.5
    disruption_correct = predicted_disruption == had_disruption
    disruption_accuracy = 1.0 if disruption_correct else 0.0
    disruption_bonus = disruption_correct and had_disruption

    risk_calibration = round(1.0 - abs(predicted_risk - (0.8 if had_disruption else 0.2)), 4)
    risk_calibration = max(0, risk_calibration)

    latency_ms = prediction.get("response_time_ms", 1000)
    latency_score = round(max(0, 1.0 - latency_ms / 10000), 4)

    consistency = round(rng.uniform(0.65, 0.95), 4)

    final = 0.40 * eta_accuracy + 0.25 * disruption_accuracy + 0.15 * risk_calibration + 0.10 * latency_score + 0.10 * consistency
    if disruption_bonus:
        final *= 1.5
    final = round(min(1.0, final), 4)

    return {
        "eta_accuracy": eta_accuracy,
        "disruption_accuracy": disruption_accuracy,
        "risk_calibration": risk_calibration,
        "latency_score": latency_score,
        "consistency": consistency,
        "disruption_bonus": disruption_bonus,
        "final_score": final,
    }


def get_supplychain_status(query) -> dict:
    """Process a user-facing supply chain query (for Swagger /track endpoint)."""
    synapse_dict = {
        "origin": query.origin,
        "destination": query.destination,
        "product_type": query.product_type,
        "carrier": query.carrier,
        "conditions": {
            "weather": "normal",
            "port_congestion": "normal",
            "geopolitical": "normal",
        },
    }

    result = run_miner_prediction(synapse_dict, "high")

    return {
        "origin": query.origin,
        "destination": query.destination,
        "product_type": query.product_type,
        "carrier": query.carrier or "Any",
        "predicted_eta_days": result["predicted_eta_days"],
        "disruption_risk": result["disruption_risk"],
        "confidence": result["confidence"],
        "risk_factors": result.get("risk_factors", []),
        "route_recommendation": result.get("route_recommendation", ""),
        "data_sources_used": result.get("data_sources", 0),
        "miners_consulted": 6,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
