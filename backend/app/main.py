from fastapi import FastAPI
from app.routes import api_router

# Create the FastAPI app instance
app = FastAPI(
    title="FinHabit API",
    version="1.0.0",
    description="Net Worth Tracker & Financial APIs"
)

# Include your versioned API router
app.include_router(api_router, prefix="/v1/api")

# Root endpoint (health check or default)
@app.get("/", tags=["Health"])
async def root():
    return {"message": "FastAPI Net Worth API is running 🚀"}