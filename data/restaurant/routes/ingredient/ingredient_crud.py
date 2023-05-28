from routes.ingredient import ingredient_schema
from models import Ingredients
from sqlalchemy.orm import Session

def get_ingredient_list(db:Session):
    
    ingredient_list = db.query(Ingredients).all()
    total = ingredient_list.count()
    
    return total,ingredient_list

def get_ingredient(db:Session, ingredient_id:int):
    ingredient = db.query(Ingredients).get(ingredient_id)
    return ingredient

def create_ingredient(db:Session, ingredient_create:ingredient_schema.IngredientCreate):
    db_ingredient = Ingredients(name=ingredient_create.name,
                                price=ingredient_create.price,
                                amount=ingredient_create.amount)
    db.add(db_ingredient)
    db.commit()
