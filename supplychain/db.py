# Placeholder for DB logic
from .models import SupplyChainQuery, SupplyChainResponse

def get_db():
    return {"queries": [], "responses": []}

def add_supplychain_query(db, query: SupplyChainQuery):
    db["queries"].append(query)

def add_supplychain_response(db, response: SupplyChainResponse):
    db["responses"].append(response)
