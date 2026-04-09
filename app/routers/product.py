import os
import uuid
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Request
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category
from app.models.user import User
from app.database import get_db
from app.schemas.product import ProductResponse, CreateProductRequest, CreateProductResponse, UpdateProductRequest
from app.utils.dependencies import require_role
from app.limiter import limiter

UPLOAD_DIR = "static/images"
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("/all", response_model=list[ProductResponse])
@limiter.limit("50/minute")
async def get_all_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return products

@router.get("/{product_id}", response_model=ProductResponse)
@limiter.limit("50/minute")
async def get_product_details(request: Request, product_id: int, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return existing

@router.post("/create", response_model=CreateProductResponse)
@limiter.limit("25/minute")
async def create_product(request: Request, product: CreateProductRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product_data = Product(
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock,
        category_id = product.category_id,
    )

    db.add(product_data)
    db.commit()
    db.refresh(product_data)

    return product_data

@router.post("/{product_id}/upload-image", response_model=ProductResponse)
@limiter.limit("25/minute")
async def upload_product_image(request: Request, product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WEBP files are allowed")

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    # Eski resmi sil
    if product.image_url:
        old_path = product.image_url.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)

    product.image_url = f"/static/images/{filename}"
    db.commit()
    db.refresh(product)

    return product


@router.delete("/delete/{product_id}")
@limiter.limit("25/minute")
async def delete_product(request: Request, product_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(existing_product)
    db.commit()

    return {"message": "Product deleted successfully"}

@router.put("/update/{product_id}", response_model=ProductResponse)
@limiter.limit("25/minute")
async def update_product(request: Request, product_id: int, product: UpdateProductRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    product_query = db.query(Product).filter(Product.id == product_id)
    existingProduct = product_query.first()

    if not existingProduct:
        raise HTTPException(status_code=404, detail="Product not found")
    
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    product_query.update(product.model_dump(), synchronize_session=False)
    db.commit()

    return existingProduct