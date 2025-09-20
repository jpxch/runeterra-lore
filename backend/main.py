from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import champions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(champions.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Runeterra Lore API is live"}