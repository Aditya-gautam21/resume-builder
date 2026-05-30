from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.routes import generator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API routes (registered first so they take precedence) ──
app.include_router(generator.router)

# ── Serve built frontend ──
app.mount("/assets", StaticFiles(directory="frontend-dist/assets"), name="assets")


@app.get("/favicon.svg")
async def favicon():
    return FileResponse("frontend-dist/favicon.svg")


@app.get("/icons.svg")
async def icons():
    return FileResponse("frontend-dist/icons.svg")


@app.get("/")
async def serve_frontend():
    return FileResponse("frontend-dist/index.html")
