"""FastAPI REST API."""
from fastapi import FastAPI

app = FastAPI(title="Crochet Pattern Checker API")

@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Crochet Pattern Checker API"}
