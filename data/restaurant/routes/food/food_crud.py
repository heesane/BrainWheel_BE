from routes.food import food_schema
from routes.ingredient import ingredient_schema
from models import Foods,Ingredients
from sqlalchemy.orm import Session

def get_food_list(db: Session):
    # 모든 Food 정보 출력
    food_list = db.query(Foods).all()
    count = len(food_list)
    
    # return
    return [count, food_list]

# 해당 번호의 음식에 대한 detail 정보 출력
def get_food(db: Session, food_id: int):
    return db.query(Foods).get(food_id)

# 새로운 음식/식재료 추가
def create_food(food_create: food_schema.FoodCreate,
                db: Session):
    
    # 현재 음식 목록 전체 조회
    count, food_list = get_food_list(db)
    
    # 음식 종류만큼 ID 부여
    db_food = Foods(name=food_create.name,
                   price=food_create.price,
                   ingredients_id=count+1)
    db.add(db_food)

    
    food_id = db_food.ingredients_id
    
    # 해당 ID로 식재료를 추가
    for ingredient in food_create.ingredients:
        # 식재료 추가
        db_ingredient = Ingredients(
            food_id = food_id,
            name=ingredient["name"],
            amount=ingredient["amount"]
            )
        db.add(db_ingredient)
    db.commit()
    
# 음식 정보 수정
def update_food(db:Session, food_update: food_schema.FoodUpdate):
    db_food = db.query(Foods).get(food_update.food_id)
    db_food.name = food_update.name
    db_food.amount = food_update.amount
    db.add(db_food)

    # 해당 음식의 식재료 정보 수정
    # 식재료 수정 여부 확인
    if food_update.ingredients_flag:
        for ingredient in food_update.ingredients:
            db_ingredient = db.query(Ingredients).get(ingredient["id"])
            db_ingredient.name = ingredient["name"]
            db_ingredient.amount = ingredient["amount"]
            db.add(db_ingredient)
    db.commit()
    
# 음식 정보 삭제
def delete_food(db:Session, food_id:food_schema.FoodDelete):
    db_food = db.query(Foods).get(food_id)
    db.delete(db_food)
    db.commit()
    
# 식재료 정보 삭제
def delete_ingredient(db:Session, food_id:ingredient_schema.IngredientDelete):
    db_ingredient = db.query(Ingredients).get(food_id)
    db.delete(db_ingredient)
    db.commit()
    
    