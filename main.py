from fastapi import FastAPI
from supplychain.routes import router as supplychain_router

app = FastAPI(title="AI Supply Chain Subnet")
app.include_router(supplychain_router)

@app.get("/")
def root():
    return {"message": "Welcome to the AI Supply Chain Subnet powered by Bittensor!"}
