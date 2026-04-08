from pydantic import BaseModel
from datetime import datetime


class CreateCategoryRequset(BaseModel):
    name: str

class CreateCategoryResponse(BaseModel):
    name: str

class UpdateCategoryRequest(BaseModel):
    name: str

class UpdateCategoryResponse(BaseModel):
    name: str

class CategoryResponse(BaseModel):

    id: int
    name: str
    createdAt: datetime