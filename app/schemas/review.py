from pydantic import BaseModel, Field
from datetime import datetime


class ReviewRequest(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(max_length=500)


class ReviewUserInfo(BaseModel):
    id: int
    userName: str

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str
    product_id: int
    user: ReviewUserInfo
    createdAt: datetime

    class Config:
        from_attributes = True
