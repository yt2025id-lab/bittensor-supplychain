from pydantic import BaseModel

class SupplyChainQuery(BaseModel):
    user_id: str
    product: str
    location: str

class SupplyChainResponse(BaseModel):
    status: str
    prediction: str
    recommendation: str
