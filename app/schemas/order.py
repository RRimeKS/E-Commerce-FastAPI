from pydantic import BaseModel
from datetime import datetime

class OrderItemProductInfo(BaseModel):
    id: int
    name: str
    image_url: str | None = None

    class Config:
        from_attributes = True


class OrderItemInfo(BaseModel):
    product_id: int
    quantity: int
    price: float
    product: OrderItemProductInfo | None = None

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    items: list[OrderItemInfo]
    createdAt: datetime
    updatedAt: datetime | None = None

    class Config:
        from_attributes = True

class CreateOrderItemRequest(BaseModel):
    product_id: int
    quantity: int


class CreateOrderRequest(BaseModel):
    items: list[CreateOrderItemRequest]