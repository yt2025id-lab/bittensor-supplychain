from fastapi import APIRouter
from .models import SupplyChainQuery, SupplyChainResponse
from .ai import get_supplychain_status

router = APIRouter()

@router.post("/track")
def track(query: SupplyChainQuery):
    result = get_supplychain_status(query)
    return SupplyChainResponse(**result)
