from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


# ── Enums ──

class TaskType(str, Enum):
    eta_prediction = "eta_prediction"
    disruption_risk = "disruption_risk"
    route_optimization = "route_optimization"


class ProductType(str, Enum):
    electronics = "electronics"
    perishable = "perishable"
    bulk = "bulk"
    hazmat = "hazmat"
    general = "general"


class MinerTier(str, Enum):
    entry = "entry"
    mid = "mid"
    high = "high"


# ── Supply Chain Synapse (Challenge from Validator → Miner) ──

class ShipmentConditions(BaseModel):
    weather: str = Field(..., example="typhoon_warning_western_pacific")
    port_congestion: str = Field(..., example="shanghai_moderate")
    geopolitical: str = Field(..., example="normal")


class SupplyChainSynapse(BaseModel):
    """Challenge dispatched by Validator to Miners via Bittensor network."""
    task_type: TaskType = Field(..., description="Type of prediction task")
    origin: str = Field(..., example="Shanghai, China")
    destination: str = Field(..., example="Los Angeles, USA")
    product_type: ProductType = Field(default=ProductType.electronics)
    carrier: Optional[str] = Field(None, example="COSCO")
    ship_date: str = Field(..., example="2026-02-15")
    conditions: Optional[ShipmentConditions] = None
    random_seed: Optional[int] = Field(None, example=83920174)


# ── Risk Factor ──

class RiskFactor(BaseModel):
    factor: str = Field(..., example="typhoon_diversion")
    probability: float = Field(..., ge=0, le=1, example=0.35)
    impact_days: float = Field(..., example=3.0)


# ── Route Recommendation ──

class RouteRecommendation(BaseModel):
    route: str = Field(..., example="Shanghai → Busan (transship) → Los Angeles")
    estimated_days: float = Field(..., example=16.0)
    estimated_cost_usd: float = Field(..., example=3200.0)
    rationale: str = Field(..., example="Transshipment via Busan avoids direct typhoon path")


# ── Miner Response ──

class MinerPrediction(BaseModel):
    """Prediction returned by a Miner in response to a Validator challenge."""
    miner_uid: int = Field(..., description="Miner UID on the subnet")
    miner_hotkey: str = Field(..., description="Miner hotkey address")
    predicted_eta_days: Optional[float] = Field(None, example=18.5)
    disruption_risk: Optional[float] = Field(None, ge=0, le=1, example=0.45)
    risk_factors: Optional[List[RiskFactor]] = None
    route_recommendation: Optional[RouteRecommendation] = None
    confidence: Optional[float] = Field(None, ge=0, le=1, example=0.78)
    data_sources: Optional[List[str]] = Field(None, example=["AIS_vessel_tracking", "NOAA_weather", "port_congestion_API"])
    response_time_ms: Optional[float] = Field(None, description="Response latency in milliseconds")


# ── Validator Scoring ──

class ScoreBreakdown(BaseModel):
    eta_accuracy: float = Field(..., ge=0, le=1, description="ETA accuracy score (weight: 40%)")
    disruption_accuracy: float = Field(..., ge=0, le=1, description="Disruption detection score (weight: 25%)")
    risk_calibration: float = Field(..., ge=0, le=1, description="Risk calibration score (weight: 15%)")
    latency_score: float = Field(..., ge=0, le=1, description="Response latency score (weight: 10%)")
    consistency: float = Field(..., ge=0, le=1, description="Consistency EMA over 100 rounds (weight: 10%)")
    disruption_bonus: bool = Field(False, description="1.5x bonus for correct disruption prediction")
    final_score: float = Field(..., ge=0, description="Weighted final score")


class MinerScoreResult(BaseModel):
    miner_uid: int
    miner_hotkey: str
    score: ScoreBreakdown
    rank: int
    tau_earned: float = Field(..., description="Estimated TAO earned this tempo")


# ── Miner Registration & Info ──

class MinerRegister(BaseModel):
    hotkey: str = Field(..., example="5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty")
    coldkey: str = Field(..., example="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY")
    tier: MinerTier = Field(default=MinerTier.entry)
    ip: str = Field(..., example="192.168.1.100")
    port: int = Field(default=8091, example=8091)
    model_name: Optional[str] = Field(None, example="supply-chain-predictor-v2")


class MinerInfo(BaseModel):
    uid: int
    hotkey: str
    coldkey: str
    tier: MinerTier
    ip: str
    port: int
    model_name: Optional[str]
    stake: float = Field(0.0, description="TAO staked")
    is_active: bool = True
    total_challenges: int = 0
    avg_score: float = 0.0
    total_tau_earned: float = 0.0
    last_active_block: Optional[int] = None


# ── Validator Registration & Info ──

class ValidatorRegister(BaseModel):
    hotkey: str = Field(..., example="5DAAnrj7VHTznn2AWBemMuyBwZWs6FNFjdyVXUeYum3PTXFy")
    coldkey: str = Field(..., example="5HGjWAeFDfFCWPsjFQdVV2Msvz2XtMktvgocEZcCj68kUMaw")
    ip: str = Field(..., example="192.168.1.200")
    port: int = Field(default=8092, example=8092)
    stake: float = Field(default=1000.0, example=1000.0)


class ValidatorInfo(BaseModel):
    uid: int
    hotkey: str
    coldkey: str
    ip: str
    port: int
    stake: float
    is_active: bool = True
    challenges_sent: int = 0
    last_weight_block: Optional[int] = None
    bond_strength: float = 0.0


# ── Challenge Result ──

class ChallengeResult(BaseModel):
    challenge_id: str
    synapse: SupplyChainSynapse
    challenge_type: str = Field(..., description="historical (70%) or near_term (30%)")
    ground_truth: Optional[dict] = Field(None, description="Actual shipment outcome (for historical)")
    miner_predictions: List[MinerPrediction]
    scores: List[MinerScoreResult]
    timestamp: str
    tempo: int


# ── Network Status ──

class SubnetHyperparameters(BaseModel):
    max_allowed_uids: int = 256
    max_allowed_validators: int = 64
    immunity_period: int = 5000
    weights_rate_limit: int = 100
    commit_reveal_period: int = 1
    tempo: int = 360
    subnet_owner_cut: float = 0.18
    miner_cut: float = 0.41
    validator_cut: float = 0.41


class NetworkStatus(BaseModel):
    subnet_name: str = "AI Supply Chain Subnet"
    subnet_id: int = 6
    block_height: int
    current_tempo: int
    total_miners: int
    active_miners: int
    total_validators: int
    active_validators: int
    total_stake: float
    total_emission_per_tempo: float
    hyperparameters: SubnetHyperparameters
    top_miners: List[MinerInfo]


# ── Leaderboard ──

class LeaderboardEntry(BaseModel):
    rank: int
    miner_uid: int
    miner_hotkey: str
    tier: MinerTier
    avg_score: float
    total_challenges: int
    total_tau_earned: float
    eta_accuracy_avg: float
    disruption_accuracy_avg: float
    streak: int = Field(0, description="Consecutive tempos in top 10")


# ── Simple Track Query (backward compatible) ──

class SupplyChainQuery(BaseModel):
    user_id: str
    product: str
    origin: str = Field(..., example="Shanghai, China")
    destination: str = Field(..., example="Los Angeles, USA")
    carrier: Optional[str] = Field(None, example="COSCO")
    ship_date: Optional[str] = Field(None, example="2026-02-15")


class SupplyChainResponse(BaseModel):
    status: str
    predicted_eta_days: float
    disruption_risk: float
    risk_factors: List[RiskFactor]
    route_recommendation: RouteRecommendation
    recommendation: str
    confidence: float
    data_sources: List[str]
