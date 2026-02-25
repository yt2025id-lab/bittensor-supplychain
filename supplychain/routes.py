"""
API Routes for AI Supply Chain Subnet Demo.
Demonstrates full subnet functionality: Miners, Validators, Scoring, and Network.
"""

import random
import time
import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from .models import (
    TaskType, ProductType, MinerTier,
    ShipmentConditions, SupplyChainSynapse,
    RiskFactor, RouteRecommendation,
    MinerPrediction, ScoreBreakdown, MinerScoreResult,
    MinerRegister, MinerInfo,
    ValidatorRegister, ValidatorInfo,
    ChallengeResult, NetworkStatus, SubnetHyperparameters,
    LeaderboardEntry,
    SupplyChainQuery, SupplyChainResponse,
)
from .ai import run_miner_prediction, score_prediction, get_supplychain_status, run_demo_scenario, get_demo_scenarios_list
from . import db

router = APIRouter()


# ═══════════════════════════════════════════════════════════════
# 1. SUPPLY CHAIN QUERY (User-facing API)
# ═══════════════════════════════════════════════════════════════

@router.post(
    "/track",
    response_model=SupplyChainResponse,
    tags=["Supply Chain API"],
    summary="Track & Predict Shipment",
    description=(
        "User-facing endpoint. Submit a shipment query and receive AI-powered predictions "
        "from the decentralized miner network. Returns ETA prediction, disruption risk, "
        "risk factors, route recommendation, and confidence score."
    ),
)
def track(query: SupplyChainQuery):
    result = get_supplychain_status(query)
    return SupplyChainResponse(**result)


# ═══════════════════════════════════════════════════════════════
# 2. MINER ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get(
    "/miners",
    response_model=List[MinerInfo],
    tags=["Miners"],
    summary="List All Miners",
    description="Get list of all registered miners on the subnet with their stats and performance.",
)
def list_miners():
    miners = db.get_miners()
    return [MinerInfo(**m) for m in miners.values()]


@router.get(
    "/miners/{uid}",
    response_model=MinerInfo,
    tags=["Miners"],
    summary="Get Miner Details",
    description="Get detailed information about a specific miner by UID.",
)
def get_miner(uid: int):
    miner = db.get_miner(uid)
    if not miner:
        raise HTTPException(status_code=404, detail=f"Miner UID {uid} not found")
    return MinerInfo(**miner)


@router.post(
    "/miners/register",
    response_model=MinerInfo,
    tags=["Miners"],
    summary="Register New Miner",
    description=(
        "Register a new miner on the subnet. Requires hotkey, coldkey, and network info. "
        "New miners start with 0 stake and enter the immunity period (5000 blocks)."
    ),
)
def register_miner(miner: MinerRegister):
    # Check hotkey uniqueness
    for m in db.get_miners().values():
        if m["hotkey"] == miner.hotkey:
            raise HTTPException(status_code=400, detail="Hotkey already registered")

    result = db.add_miner(miner.dict())
    return MinerInfo(**result)


@router.post(
    "/miners/{uid}/predict",
    response_model=MinerPrediction,
    tags=["Miners"],
    summary="Run Miner Prediction",
    description=(
        "Simulate a miner processing a supply chain challenge. "
        "The miner runs its AI model and returns ETA prediction, disruption risk, "
        "risk factors, and route recommendation. Response varies by miner tier."
    ),
)
def miner_predict(uid: int, synapse: SupplyChainSynapse):
    miner = db.get_miner(uid)
    if not miner:
        raise HTTPException(status_code=404, detail=f"Miner UID {uid} not found")

    result = run_miner_prediction(synapse.dict(), miner["tier"])
    result["miner_uid"] = uid
    result["miner_hotkey"] = miner["hotkey"]

    return MinerPrediction(**result)


# ═══════════════════════════════════════════════════════════════
# 3. VALIDATOR ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get(
    "/validators",
    response_model=List[ValidatorInfo],
    tags=["Validators"],
    summary="List All Validators",
    description="Get list of all registered validators on the subnet.",
)
def list_validators():
    validators = db.get_validators()
    return [ValidatorInfo(**v) for v in validators.values()]


@router.get(
    "/validators/{uid}",
    response_model=ValidatorInfo,
    tags=["Validators"],
    summary="Get Validator Details",
    description="Get detailed information about a specific validator by UID.",
)
def get_validator(uid: int):
    validator = db.get_validator(uid)
    if not validator:
        raise HTTPException(status_code=404, detail=f"Validator UID {uid} not found")
    return ValidatorInfo(**validator)


@router.post(
    "/validators/register",
    response_model=ValidatorInfo,
    tags=["Validators"],
    summary="Register New Validator",
    description="Register a new validator on the subnet. Requires stake to participate.",
)
def register_validator(validator: ValidatorRegister):
    for v in db.get_validators().values():
        if v["hotkey"] == validator.hotkey:
            raise HTTPException(status_code=400, detail="Hotkey already registered")

    result = db.add_validator(validator.dict())
    return ValidatorInfo(**result)


@router.post(
    "/validators/{uid}/generate-challenge",
    response_model=SupplyChainSynapse,
    tags=["Validators"],
    summary="Generate Supply Chain Challenge",
    description=(
        "Validator generates a supply chain challenge (SupplyChainSynapse) to dispatch to miners. "
        "70% are historical challenges (past shipments with known outcomes), "
        "30% are near-term challenges (active shipments for forward prediction). "
        "Each challenge includes origin, destination, product type, conditions, and a random seed."
    ),
)
def generate_challenge(
    uid: int,
    task_type: TaskType = Query(default=TaskType.eta_prediction, description="Type of challenge"),
):
    validator = db.get_validator(uid)
    if not validator:
        raise HTTPException(status_code=404, detail=f"Validator UID {uid} not found")

    # Realistic challenge generation
    routes = [
        ("Shanghai, China", "Los Angeles, USA"),
        ("Rotterdam, Netherlands", "New York, USA"),
        ("Shenzhen, China", "Hamburg, Germany"),
        ("Tokyo, Japan", "Singapore"),
        ("Mumbai, India", "Dubai, UAE"),
        ("Busan, South Korea", "Long Beach, USA"),
    ]
    origin, destination = random.choice(routes)

    products = list(ProductType)
    carriers = ["COSCO", "Maersk", "MSC", "Evergreen", "ONE", "Hapag-Lloyd", "CMA CGM", "HMM"]

    weather_conditions = [
        "clear", "typhoon_warning_western_pacific", "north_atlantic_storm",
        "monsoon_indian_ocean", "normal",
    ]
    congestion_levels = [
        "normal", "shanghai_moderate", "shanghai_high", "la_moderate",
        "singapore_low", "low",
    ]

    synapse = SupplyChainSynapse(
        task_type=task_type,
        origin=origin,
        destination=destination,
        product_type=random.choice(products),
        carrier=random.choice(carriers),
        ship_date=f"2026-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        conditions=ShipmentConditions(
            weather=random.choice(weather_conditions),
            port_congestion=random.choice(congestion_levels),
            geopolitical=random.choice(["normal", "normal", "normal", "elevated"]),
        ),
        random_seed=random.randint(10000000, 99999999),
    )

    # Update validator stats
    validator["challenges_sent"] += 1

    return synapse


@router.post(
    "/validators/{uid}/run-challenge",
    response_model=ChallengeResult,
    tags=["Validators"],
    summary="Run Full Challenge Cycle",
    description=(
        "Execute a complete challenge cycle:\n"
        "1. Validator generates a challenge (SupplyChainSynapse)\n"
        "2. Challenge is dispatched to ALL active miners\n"
        "3. Each miner runs its prediction model (response within 10s timeout)\n"
        "4. Validator scores each miner's prediction against ground truth\n"
        "5. Miners are ranked and TAO rewards are distributed\n\n"
        "This simulates one full tempo cycle of the subnet."
    ),
)
def run_challenge(
    uid: int,
    task_type: TaskType = Query(default=TaskType.eta_prediction),
    synapse: Optional[SupplyChainSynapse] = None,
):
    validator = db.get_validator(uid)
    if not validator:
        raise HTTPException(status_code=404, detail=f"Validator UID {uid} not found")

    # Generate challenge if not provided
    if synapse is None:
        routes = [
            ("Shanghai, China", "Los Angeles, USA"),
            ("Rotterdam, Netherlands", "New York, USA"),
            ("Shenzhen, China", "Hamburg, Germany"),
        ]
        origin, dest = random.choice(routes)
        synapse = SupplyChainSynapse(
            task_type=task_type,
            origin=origin,
            destination=dest,
            product_type=random.choice(list(ProductType)),
            carrier=random.choice(["COSCO", "Maersk", "MSC", "Evergreen"]),
            ship_date="2026-02-15",
            conditions=ShipmentConditions(
                weather=random.choice(["clear", "typhoon_warning_western_pacific", "normal"]),
                port_congestion=random.choice(["normal", "shanghai_moderate"]),
                geopolitical="normal",
            ),
            random_seed=random.randint(10000000, 99999999),
        )

    # Determine challenge type (70% historical, 30% near-term)
    is_historical = random.random() < 0.7
    challenge_type = "historical" if is_historical else "near_term"

    # Generate ground truth for historical challenges
    rng = random.Random(synapse.random_seed if synapse.random_seed else int(time.time()))
    ground_truth = None
    if is_historical:
        base_eta = rng.uniform(5, 30)
        had_disruption = rng.random() < 0.3
        ground_truth = {
            "actual_eta_days": round(base_eta, 1),
            "had_disruption": had_disruption,
            "disruption_type": rng.choice(["weather_delay", "port_congestion", "customs_delay", None]) if had_disruption else None,
            "actual_route": f"{synapse.origin} → {synapse.destination}",
        }

    # Dispatch to all active miners and collect predictions
    miners = db.get_miners()
    predictions = []
    for miner_uid, miner in miners.items():
        if not miner["is_active"]:
            continue
        result = run_miner_prediction(synapse.dict(), miner["tier"])
        result["miner_uid"] = miner_uid
        result["miner_hotkey"] = miner["hotkey"]
        predictions.append(MinerPrediction(**result))

    # Score each prediction
    scores = []
    total_emission = db.get_state()["total_emission_per_tempo"] * 0.41  # miner share
    for i, pred in enumerate(predictions):
        if ground_truth:
            score_data = score_prediction(pred.dict(), ground_truth)
        else:
            # Near-term: use estimated scoring
            score_data = {
                "eta_accuracy": round(rng.uniform(0.5, 0.95), 4),
                "disruption_accuracy": round(rng.uniform(0.3, 0.9), 4),
                "risk_calibration": round(rng.uniform(0.4, 0.85), 4),
                "latency_score": round(rng.uniform(0.7, 0.99), 4),
                "consistency": round(rng.uniform(0.6, 0.92), 4),
                "disruption_bonus": False,
                "final_score": 0,
            }
            score_data["final_score"] = round(
                0.40 * score_data["eta_accuracy"]
                + 0.25 * score_data["disruption_accuracy"]
                + 0.15 * score_data["risk_calibration"]
                + 0.10 * score_data["latency_score"]
                + 0.10 * score_data["consistency"],
                4
            )

        scores.append({
            "miner_uid": pred.miner_uid,
            "miner_hotkey": pred.miner_hotkey,
            "score": ScoreBreakdown(**score_data),
            "rank": 0,  # Set below
            "tau_earned": 0,  # Set below
        })

    # Rank by final score
    scores.sort(key=lambda s: s["score"].final_score, reverse=True)
    total_scores = sum(s["score"].final_score for s in scores)
    for rank, s in enumerate(scores, 1):
        s["rank"] = rank
        if total_scores > 0:
            s["tau_earned"] = round(total_emission * (s["score"].final_score / total_scores), 6)
        else:
            s["tau_earned"] = 0

        # Update miner stats
        db.update_miner_score(s["miner_uid"], s["score"].final_score, s["tau_earned"])

    score_results = [MinerScoreResult(**s) for s in scores]

    # Update validator
    validator["challenges_sent"] += 1
    validator["last_weight_block"] = db.get_state()["block_height"]

    # Advance blocks
    db.advance_block(random.randint(1, 5))

    # Save challenge
    challenge_id = str(uuid.uuid4())[:8]
    challenge_record = {
        "challenge_id": challenge_id,
        "synapse": synapse,
        "challenge_type": challenge_type,
        "ground_truth": ground_truth,
        "miner_predictions": predictions,
        "scores": score_results,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tempo": db.get_state()["current_tempo"],
    }
    db.add_challenge(challenge_record)

    return ChallengeResult(**challenge_record)


@router.post(
    "/validators/{uid}/score-prediction",
    response_model=MinerScoreResult,
    tags=["Validators"],
    summary="Score a Single Miner Prediction",
    description=(
        "Validator scores a specific miner's prediction against ground truth.\n\n"
        "Scoring dimensions:\n"
        "- **ETA Accuracy (40%):** `1 - (|predicted - actual| / 7 days)`\n"
        "- **Disruption Detection (25%):** Binary correctness + 1.5x bonus\n"
        "- **Risk Calibration (15%):** `1 - |risk_score - actual_outcome|`\n"
        "- **Latency (10%):** `max(1 - elapsed/10s, 0)`\n"
        "- **Consistency (10%):** EMA over 100 rounds"
    ),
)
def score_single_prediction(
    uid: int,
    prediction: MinerPrediction,
    actual_eta_days: float = Query(..., description="Actual delivery time in days"),
    had_disruption: bool = Query(default=False, description="Whether a disruption actually occurred"),
):
    validator = db.get_validator(uid)
    if not validator:
        raise HTTPException(status_code=404, detail=f"Validator UID {uid} not found")

    ground_truth = {
        "actual_eta_days": actual_eta_days,
        "had_disruption": had_disruption,
    }

    score_data = score_prediction(prediction.dict(), ground_truth)
    tau_earned = round(db.get_state()["total_emission_per_tempo"] * 0.41 * score_data["final_score"] / 8, 6)

    # Update miner stats
    db.update_miner_score(prediction.miner_uid, score_data["final_score"], tau_earned)

    return MinerScoreResult(
        miner_uid=prediction.miner_uid,
        miner_hotkey=prediction.miner_hotkey,
        score=ScoreBreakdown(**score_data),
        rank=1,
        tau_earned=tau_earned,
    )


# ═══════════════════════════════════════════════════════════════
# 4. NETWORK & SUBNET ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get(
    "/network/status",
    response_model=NetworkStatus,
    tags=["Network"],
    summary="Subnet Network Status",
    description=(
        "Get the current status of the AI Supply Chain subnet including "
        "block height, tempo, miner/validator counts, stake, emissions, "
        "and top performing miners."
    ),
)
def network_status():
    state = db.get_state()
    miners = db.get_miners()
    validators = db.get_validators()

    active_miners = [m for m in miners.values() if m["is_active"]]
    active_validators = [v for v in validators.values() if v["is_active"]]
    total_stake = sum(m["stake"] for m in miners.values()) + sum(v["stake"] for v in validators.values())

    # Top 5 miners
    top = sorted(active_miners, key=lambda m: m["avg_score"], reverse=True)[:5]

    return NetworkStatus(
        block_height=state["block_height"],
        current_tempo=state["current_tempo"],
        total_miners=len(miners),
        active_miners=len(active_miners),
        total_validators=len(validators),
        active_validators=len(active_validators),
        total_stake=round(total_stake, 2),
        total_emission_per_tempo=state["total_emission_per_tempo"],
        hyperparameters=SubnetHyperparameters(),
        top_miners=[MinerInfo(**m) for m in top],
    )


@router.get(
    "/network/leaderboard",
    response_model=List[LeaderboardEntry],
    tags=["Network"],
    summary="Miner Leaderboard",
    description=(
        "Get the ranked leaderboard of all miners sorted by average score. "
        "Shows performance metrics, TAO earned, and tier classification."
    ),
)
def leaderboard():
    miners = db.get_leaderboard()
    rng = random.Random(42)
    entries = []
    for rank, m in enumerate(miners, 1):
        entries.append(LeaderboardEntry(
            rank=rank,
            miner_uid=m["uid"],
            miner_hotkey=m["hotkey"],
            tier=m["tier"],
            avg_score=m["avg_score"],
            total_challenges=m["total_challenges"],
            total_tau_earned=m["total_tau_earned"],
            eta_accuracy_avg=round(m["avg_score"] * rng.uniform(0.9, 1.1), 3),
            disruption_accuracy_avg=round(m["avg_score"] * rng.uniform(0.75, 1.0), 3),
            streak=max(0, int((m["avg_score"] - 0.5) * 20) + rng.randint(0, 5)),
        ))
    return entries


@router.get(
    "/network/challenges",
    response_model=List[ChallengeResult],
    tags=["Network"],
    summary="Recent Challenges",
    description="Get the most recent challenges and their results.",
)
def recent_challenges(limit: int = Query(default=10, ge=1, le=50)):
    challenges = db.get_challenges(limit)
    return [ChallengeResult(**c) for c in challenges]


@router.get(
    "/network/hyperparameters",
    response_model=SubnetHyperparameters,
    tags=["Network"],
    summary="Subnet Hyperparameters",
    description=(
        "Get the current subnet hyperparameters including max UIDs, "
        "immunity period, tempo length, and emission split."
    ),
)
def hyperparameters():
    return SubnetHyperparameters()


@router.get(
    "/network/emission-distribution",
    tags=["Network"],
    summary="Current Emission Distribution",
    description="Shows how TAO emissions are distributed among subnet participants this tempo.",
)
def emission_distribution():
    state = db.get_state()
    total = state["total_emission_per_tempo"]
    miners = db.get_miners()
    validators = db.get_validators()

    top_miners = sorted(miners.values(), key=lambda m: m["avg_score"], reverse=True)[:5]

    return {
        "tempo": state["current_tempo"],
        "total_emission_tao": total,
        "distribution": {
            "subnet_owner": {"share": "18%", "amount_tao": round(total * 0.18, 6)},
            "miners_total": {"share": "41%", "amount_tao": round(total * 0.41, 6)},
            "validators_stakers_total": {"share": "41%", "amount_tao": round(total * 0.41, 6)},
        },
        "top_miner_earnings": [
            {
                "uid": m["uid"],
                "hotkey": m["hotkey"][:16] + "...",
                "tier": m["tier"],
                "score": m["avg_score"],
                "estimated_tao_this_tempo": round(total * 0.41 * m["avg_score"] / max(1, sum(mm["avg_score"] for mm in miners.values())), 6),
            }
            for m in top_miners
        ],
    }


# ═══════════════════════════════════════════════════════════════
# 5. DEMO / SIMULATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.post(
    "/demo/full-tempo-cycle",
    tags=["Demo Simulation"],
    summary="Run Full Tempo Cycle",
    description=(
        "Simulates a complete tempo cycle (~72 minutes compressed into one API call):\n\n"
        "1. Validator generates 3 challenges (2 historical + 1 near-term)\n"
        "2. All miners receive and process each challenge\n"
        "3. Validator scores all predictions\n"
        "4. Weights are updated via Yuma Consensus\n"
        "5. TAO emissions are distributed\n"
        "6. Block height and tempo advance\n\n"
        "Returns complete results for all 3 challenges."
    ),
)
def full_tempo_cycle():
    state = db.get_state()
    validators = list(db.get_validators().values())
    if not validators:
        raise HTTPException(status_code=400, detail="No validators registered")

    active_validators = [v for v in validators if v["is_active"]]
    if not active_validators:
        raise HTTPException(status_code=400, detail="No active validators")

    # Pick lead validator (highest stake)
    lead_validator = max(active_validators, key=lambda v: v["stake"])

    results = []
    task_types = [TaskType.eta_prediction, TaskType.disruption_risk, TaskType.route_optimization]

    for i, task_type in enumerate(task_types):
        routes = [
            ("Shanghai, China", "Los Angeles, USA"),
            ("Rotterdam, Netherlands", "New York, USA"),
            ("Shenzhen, China", "Hamburg, Germany"),
            ("Tokyo, Japan", "Singapore"),
            ("Mumbai, India", "Dubai, UAE"),
            ("Busan, South Korea", "Long Beach, USA"),
        ]
        origin, dest = routes[i % len(routes)]

        synapse = SupplyChainSynapse(
            task_type=task_type,
            origin=origin,
            destination=dest,
            product_type=random.choice(list(ProductType)),
            carrier=random.choice(["COSCO", "Maersk", "MSC", "Evergreen", "ONE"]),
            ship_date="2026-02-15",
            conditions=ShipmentConditions(
                weather=random.choice(["clear", "typhoon_warning_western_pacific", "normal"]),
                port_congestion=random.choice(["normal", "shanghai_moderate", "low"]),
                geopolitical="normal",
            ),
            random_seed=random.randint(10000000, 99999999),
        )

        # Historical for first 2, near-term for last
        is_historical = i < 2
        challenge_type = "historical" if is_historical else "near_term"

        rng = random.Random(synapse.random_seed)
        ground_truth = None
        if is_historical:
            base_eta = rng.uniform(5, 30)
            ground_truth = {
                "actual_eta_days": round(base_eta, 1),
                "had_disruption": rng.random() < 0.3,
            }

        # Dispatch to miners
        miners = db.get_miners()
        predictions = []
        for miner_uid, miner in miners.items():
            if not miner["is_active"]:
                continue
            result = run_miner_prediction(synapse.dict(), miner["tier"])
            result["miner_uid"] = miner_uid
            result["miner_hotkey"] = miner["hotkey"]
            predictions.append(MinerPrediction(**result))

        # Score
        scores = []
        total_emission = state["total_emission_per_tempo"] * 0.41 / 3  # Split across 3 challenges
        for pred in predictions:
            if ground_truth:
                score_data = score_prediction(pred.dict(), ground_truth)
            else:
                score_data = {
                    "eta_accuracy": round(rng.uniform(0.5, 0.95), 4),
                    "disruption_accuracy": round(rng.uniform(0.3, 0.9), 4),
                    "risk_calibration": round(rng.uniform(0.4, 0.85), 4),
                    "latency_score": round(rng.uniform(0.7, 0.99), 4),
                    "consistency": round(rng.uniform(0.6, 0.92), 4),
                    "disruption_bonus": False,
                    "final_score": 0,
                }
                score_data["final_score"] = round(
                    0.40 * score_data["eta_accuracy"]
                    + 0.25 * score_data["disruption_accuracy"]
                    + 0.15 * score_data["risk_calibration"]
                    + 0.10 * score_data["latency_score"]
                    + 0.10 * score_data["consistency"],
                    4
                )

            scores.append({
                "miner_uid": pred.miner_uid,
                "miner_hotkey": pred.miner_hotkey,
                "score": ScoreBreakdown(**score_data),
                "rank": 0,
                "tau_earned": 0,
            })

        scores.sort(key=lambda s: s["score"].final_score, reverse=True)
        total_scores = sum(s["score"].final_score for s in scores)
        for rank, s in enumerate(scores, 1):
            s["rank"] = rank
            if total_scores > 0:
                s["tau_earned"] = round(total_emission * (s["score"].final_score / total_scores), 6)
            db.update_miner_score(s["miner_uid"], s["score"].final_score, s["tau_earned"])

        challenge_id = str(uuid.uuid4())[:8]
        challenge_record = {
            "challenge_id": challenge_id,
            "synapse": synapse,
            "challenge_type": challenge_type,
            "ground_truth": ground_truth,
            "miner_predictions": predictions,
            "scores": [MinerScoreResult(**s) for s in scores],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tempo": state["current_tempo"],
        }
        db.add_challenge(challenge_record)
        results.append(ChallengeResult(**challenge_record))

    # Advance tempo
    db.advance_tempo()

    # Update validator
    lead_validator["challenges_sent"] += 3
    lead_validator["last_weight_block"] = state["block_height"]

    return {
        "tempo_completed": state["current_tempo"] - 1,
        "new_tempo": state["current_tempo"],
        "block_height": state["block_height"],
        "lead_validator_uid": lead_validator["uid"],
        "challenges_run": len(results),
        "challenge_types": ["historical", "historical", "near_term"],
        "task_types": [str(t.value) for t in task_types],
        "total_tao_distributed": round(state["total_emission_per_tempo"], 6),
        "challenges": results,
        "updated_leaderboard": [
            {
                "rank": rank,
                "uid": m["uid"],
                "hotkey": m["hotkey"][:16] + "...",
                "tier": m["tier"],
                "avg_score": m["avg_score"],
                "total_tau": m["total_tau_earned"],
            }
            for rank, m in enumerate(sorted(db.get_miners().values(), key=lambda x: x["avg_score"], reverse=True), 1)
        ],
    }


@router.post(
    "/demo/compare-miners",
    tags=["Demo Simulation"],
    summary="Compare Miners on Same Challenge",
    description=(
        "Sends the same challenge to all miners and compares their predictions side-by-side. "
        "Shows how different miner tiers (entry/mid/high) produce different quality predictions."
    ),
)
def compare_miners(synapse: SupplyChainSynapse):
    miners = db.get_miners()
    comparisons = []

    for uid, miner in miners.items():
        if not miner["is_active"]:
            continue
        result = run_miner_prediction(synapse.dict(), miner["tier"])
        comparisons.append({
            "miner_uid": uid,
            "miner_hotkey": miner["hotkey"][:16] + "...",
            "tier": miner["tier"],
            "model": miner["model_name"] or "unknown",
            "predicted_eta_days": result["predicted_eta_days"],
            "disruption_risk": result["disruption_risk"],
            "confidence": result["confidence"],
            "response_time_ms": result["response_time_ms"],
            "risk_factors_count": len(result.get("risk_factors", [])),
            "data_sources": result["data_sources"],
            "route_recommendation": result.get("route_recommendation"),
        })

    comparisons.sort(key=lambda x: x["confidence"], reverse=True)

    return {
        "challenge": synapse.dict(),
        "total_miners_queried": len(comparisons),
        "comparisons": comparisons,
        "analysis": {
            "avg_eta": round(sum(c["predicted_eta_days"] for c in comparisons) / len(comparisons), 1) if comparisons else 0,
            "avg_disruption_risk": round(sum(c["disruption_risk"] for c in comparisons) / len(comparisons), 2) if comparisons else 0,
            "eta_spread": round(max(c["predicted_eta_days"] for c in comparisons) - min(c["predicted_eta_days"] for c in comparisons), 1) if comparisons else 0,
            "highest_confidence_miner": comparisons[0]["miner_uid"] if comparisons else None,
            "fastest_miner": min(comparisons, key=lambda c: c["response_time_ms"])["miner_uid"] if comparisons else None,
        },
    }


# ═══════════════════════════════════════════════════════════════
# 6. LANDING PAGE DEMO ENDPOINTS (Miner/Validator detail view)
# ═══════════════════════════════════════════════════════════════

@router.get(
    "/api/demo-scenarios",
    tags=["Demo Simulation"],
    summary="List Available Demo Scenarios",
    description="Returns metadata for all 3 pre-built demo scenarios.",
)
def list_demo_scenarios():
    return get_demo_scenarios_list()


@router.get(
    "/api/demo/{scenario_key}",
    tags=["Demo Simulation"],
    summary="Run Demo Scenario",
    description=(
        "Run one of 3 pre-built demo scenarios showing full subnet operation:\n\n"
        "- **demo1:** Ocean Freight ETA Prediction (Shanghai → LA, typhoon)\n"
        "- **demo2:** Disruption Risk Assessment (Shenzhen → Hamburg, Red Sea)\n"
        "- **demo3:** Route Optimization (Busan → Long Beach, Pacific storm)\n\n"
        "Returns full miner responses, validator verifications, consensus, and TAO rewards."
    ),
)
def run_demo(scenario_key: str):
    result = run_demo_scenario(scenario_key)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
