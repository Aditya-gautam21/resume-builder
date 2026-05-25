from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import generator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generator.router)