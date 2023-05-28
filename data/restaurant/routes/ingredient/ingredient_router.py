from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from routes.ingredient import ingredient_schema, ingredient_crud

router = APIRouter(
    prefix="/api/ingredient",
    tags=["ingredient"]
)

@router.get("/list", response_model=ingredient_schema.IngredientList)
def ingredient_list(db: Session = Depends(get_db)):
    total,ingredient_list = ingredient_crud.get_ingredient_list(db)
    return {
        'total': total,
        'ingredient_list': ingredient_list
    }
    
@router.get("/detail/{ingredient_id}", response_model=ingredient_schema.Ingredient)
def ingredient_detail(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = ingredient_crud.get_ingredient(db, ingredient_id=ingredient_id)
    return ingredient

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def ingredient_create(_ingredient_create: ingredient_schema.IngredientCreate,
                    db: Session = Depends(get_db)):
    ingredient_crud.create_ingredient(db=db, ingredient_create=_ingredient_create)
    