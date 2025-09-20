from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import champions, regions, skins

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(champions.router, prefix="/api")
app.include_router(regions.router, prefix="/api")
app.include_router(skins.router, prefix="/api")
