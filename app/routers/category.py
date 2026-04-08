from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryResponse, CreateCategoryRequset, CreateCategoryResponse, UpdateCategoryRequest, UpdateCategoryResponse
from app.database import get_db
from app.utils.dependencies import require_role

router = APIRouter(prefix="/category", tags=["Category"])

@router.get("/all", response_model=list[CategoryResponse])
async def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/create", response_model=CreateCategoryResponse)
async def create_category(category: CreateCategoryRequset, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    category_data = Category(
        name = category.name,
    )
     
    db.add(category_data)
    db.commit()
    db.refresh(category_data)

    return category_data

@router.delete("/delete/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}

@router.put("/update/{category_id}", response_model=UpdateCategoryResponse)
async def update_category(category_id: int, category: UpdateCategoryRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    category_query = db.query(Category).filter(Category.id == category_id)
    existing_data = category_query.first()

    if not existing_data:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_query.update(category.model_dump(), synchronize_session=False)
    db.commit()

    return category_query.first()