from pydantic import BaseModel
from datetime import datetime


class ProductCategoryInfo(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    stock: int
    price: float
    isActive: bool
    image_url: str | None = None
    average_rating: float = 0
    review_count: int = 0
    category: ProductCategoryInfo | None = None
    createdAt: datetime

    class Config:
        from_attributes = True

class CreateProductRequest(BaseModel):
    name: str
    description: str
    stock: int
    price: float
    category_id: int

class CreateProductResponse(BaseModel):
    id: int
    name: str
    description: str
    stock: int
    price: float
    isActive: bool
    image_url: str | None = None
    category_id: int
    createdAt: datetime

    class Config:
        from_attributes = True

class UpdateProductRequest(BaseModel):
    name: str
    description: str
    stock: int
    price: float
    category_id: int
