from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import champions, regions, skins
from backend.config import settings

app = FastAPI(
    title="Runeterra Lore API",
    version="1.0.0",
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
API_PREFIX = "/api"
app.include_router(champions.router, prefix=API_PREFIX)
app.include_router(regions.router, prefix=API_PREFIX)
app.include_router(skins.router, prefix=API_PREFIX)


@app.get("/health")
def health_check():
    """Health endpoint for Docker/K8s probes."""
    return {"status": "ok"}
