from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.review import Review
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User
from app.schemas.review import ReviewRequest, ReviewResponse
from app.utils.dependencies import isAuthentication
from app.limiter import limiter

router = APIRouter(prefix="/review", tags=["Reviews"])

def update_product_rating(db: Session, product_id: int):
    result = db.query(
        func.count(Review.id),
        func.coalesce(func.avg(Review.rating), 0),
    ).filter(Review.product_id == product_id).first()

    product = db.query(Product).filter(Product.id == product_id).first()
    product.review_count = result[0]
    product.average_rating = round(float(result[1]), 1)

@router.get("/product/{product_id}", response_model=list[ReviewResponse])
@limiter.limit("50/minute")
async def get_product_reviews(request: Request, product_id: int, db: Session = Depends(get_db)):
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.createdAt.desc())
        .all()
    )
    return reviews


@router.post("/product/{product_id}", response_model=ReviewResponse, status_code=201)
@limiter.limit("25/minute")
async def create_review(
    request: Request,
    product_id: int,
    data: ReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(isAuthentication),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    purchased = (
        db.query(OrderItem)
        .join(Order)
        .filter(Order.user_id == current_user.id)
        .filter(OrderItem.product_id == product_id)
        .first()
    )
    if not purchased:
        raise HTTPException(status_code=403, detail="Bu ürünü satın almadan yorum yapamazsınız")

    existing = (
        db.query(Review)
        .filter(Review.user_id == current_user.id, Review.product_id == product_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Bu ürüne zaten yorum yaptınız")

    review = Review(
        rating=data.rating,
        comment=data.comment,
        product_id=product_id,
        user_id=current_user.id,
    )
    db.add(review)
    db.flush()

    update_product_rating(db, product_id)

    db.commit()
    db.refresh(review)

    return review


@router.delete("/product/{product_id}", status_code=204)
@limiter.limit("25/minute")
async def delete_review(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(isAuthentication),
):
    review = (
        db.query(Review)
        .filter(Review.user_id == current_user.id, Review.product_id == product_id)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")

    db.delete(review)
    db.flush()

    update_product_rating(db, product_id)

    db.commit()
