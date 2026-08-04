import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import skincare_products, chat, orders
from app.core.config import settings
from app.core.database import connect_db, close_db
from app.services.skincare_seed import seed_skincare_database

app = FastAPI(
    title="Skincare AI E-Commerce & Voice Symptom Analyzer API",
    description="AI-powered Skincare E-Commerce Platform with Voice Assistance, Symptom Analysis & RAG Product Recommendations",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=os.path.abspath(settings.UPLOAD_DIR)), name="uploads")
app.mount("/api/uploads", StaticFiles(directory=os.path.abspath(settings.UPLOAD_DIR)), name="api_uploads")

# Core Routers: Skincare E-Commerce, AI Voice Advisor & Orders
app.include_router(skincare_products.router, prefix="/api/products", tags=["Skincare E-Commerce Products"])
app.include_router(chat.router, prefix="/api/chat", tags=["Skincare AI Voice & Symptom Advisor"])
app.include_router(orders.router, prefix="/api/orders", tags=["Skincare Orders (Chatbot COD)"])


@app.on_event("startup")
async def startup():
    await connect_db()
    await seed_skincare_database()


@app.on_event("shutdown")
async def shutdown():
    await close_db()


@app.get("/")
async def root():
    return {"message": "🌸 Skincare AI E-Commerce & Voice Symptom Analyzer API is running ✅"}