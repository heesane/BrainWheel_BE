from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from routes.food import food_schema, food_crud
from routes.ingredient import ingredient_schema

router = APIRouter(
    prefix="/api/food",
    tags=["food"]
)

@router.get("/list", response_model=food_schema.Food)
def get_food_list(db: Session = Depends(get_db)):
    cnt, db_result = food_crud.get_food_list(db)
    if cnt ==0:
        return []
    else:
        return {
            'total': cnt,
            'food_list': db_result
        }

@router.get("/detail/{food_id}", response_model=food_schema.Food)
def get_food(db:Session=Depends(get_db), food_id:int=0):
    db_result = food_crud.get_food(db, food_id=food_id)
    if  db_result is None:
        return []
    else:
        return db_result

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create_food(food_create: food_schema.FoodCreate,db: Session = Depends(get_db)):
    food_crud.create_food(db=db, food_create=food_create)
    
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def update_food(food_update: food_schema.FoodUpdate, db: Session = Depends(get_db)):
    db_food = food_crud.get_food(db, food_id=food_update.food_id)
    
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    food_crud.update_food(db=db, food_update=food_update)