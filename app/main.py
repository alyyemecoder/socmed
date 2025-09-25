# app/main.py
from fastapi import FastAPI
from .routes import router
import uvicorn
# ensure config imported to set up neomodel
from . import config

app = FastAPI(title="Simple Social API - Neo4j + FastAPI")
app.include_router(router)

@app.on_event("startup")
def startup_event():
    # neomodel connection is configured via config.py import
    print("App startup - Neo4j config loaded.")

@app.get("/")
def root():
    return {"message": "Simple Social API running."}

# for direct run: uvicorn app.main:app --reload
