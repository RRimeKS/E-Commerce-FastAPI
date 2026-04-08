from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User
from app.database import get_db
from app.schemas.order import CreateOrderRequest, OrderResponse
from app.utils.dependencies import require_role, isAuthentication

router = APIRouter(prefix="/order", tags=["Order"])
@router.get("/all", response_model=list[OrderResponse])
async def get_all_orders(db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    orders = db.query(Order).all()
    return orders

@router.get("/detail/{order_id}", response_model=OrderResponse)
async def get_order_by_id(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/my-orders", response_model=list[OrderResponse])
async def get_orders_by_user_id(db: Session = Depends(get_db), current_user: User = Depends(isAuthentication)):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.post("/create", response_model=OrderResponse)
async def create_order(order_data: CreateOrderRequest, db: Session = Depends(get_db), current_user: User = Depends(isAuthentication)):
    total_price = 0.0
    order_items = []

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")

        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")

        product.stock -= item.quantity
        total_price += product.price * item.quantity
        order_item = OrderItem(product_id=item.product_id, quantity=item.quantity, price=product.price)
        order_items.append(order_item)

    new_order = Order(user_id=current_user.id, total_price=total_price, status="pending", items=order_items)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order