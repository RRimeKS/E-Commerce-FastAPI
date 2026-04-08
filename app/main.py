import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.logging_config import setup_logging, logging
from app.exception_handlers import register_exception_handlers
from app.models.product import Product
from app.models.category import Category
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.review import Review
from app.routers import auth as auth_router
from app.routers import category as category_router
from app.routers import product as product_router
from app.routers import order as order_router
from app.routers import review as review_router

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Application started")
    yield
    logger.info("Application shutdown")

app = FastAPI(title="FastAPI E-Commerce API", description="A simple e-commerce API built with FastAPI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000)
    logger.info("%s %s → %s (%dms)", request.method, request.url.path, response.status_code, duration)
    return response

from fastapi.staticfiles import StaticFiles
import os
os.makedirs("static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(review_router.router)

@app.get("/")
def root():
    return {"message": "Products API is running"}
