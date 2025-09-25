# app/main.py

import logging
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from neomodel import db
from . import config

# Optional: import router
try:
    from .routes import router
except ImportError as e:
    logging.warning(f"⚠️ Could not import router: {e}")
    router = None

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db.cypher_query("RETURN 'Neo4j connection OK'")
        logging.info("✅ Connected to Neo4j successfully.")
    except Exception as e:
        logging.error(f"❌ Failed to connect to Neo4j: {e}")
    yield  # Startup complete
    # You can add shutdown logic here if needed

# Initialize FastAPI with lifespan
app = FastAPI(title="Simple Social API - Neo4j + FastAPI", lifespan=lifespan)

# Include router if available
if router:
    app.include_router(router)

@app.get("/")
def root():
    return {"message": "Simple Social API running."}

# For direct execution
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)