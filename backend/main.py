from fastapi import FastAPI
from backend.routes import generator

app = FastAPI()

app.include_router(generator.router)