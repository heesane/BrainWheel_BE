from pydantic import BaseModel, validator
from typing import List

####################################################################################################
# Ingredient
####################################################################################################
class Ingredient(BaseModel):
    id:int
    name: str
    amount: int
    class Config:
        orm_mode = True
        
class IngredientCreate(BaseModel):
    name:str
    amount:int
    
    @validator('name', 'amount')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class IngredientList(BaseModel):
    total:int = 0
    ingredient_list : list[Ingredient] = []

####################################################################################################
# Food
####################################################################################################
class Food(BaseModel):
    name: str
    price: int
    ingredients_id: int = 0
    
    class Config:
        orm_mode = True
        
class FoodCreate(BaseModel):
    name: str
    price: int
    ingredients :dict
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('가격은 0보다 커야 합니다.')
        return v

class FoodList(BaseModel):
    total: int = 0
    food_list: List[Food] = []
    
class FoodUpdate(FoodCreate):
    food_id: int
    ingredients_flag: bool = False

class FoodDelete(BaseModel):
    food_id: int

####################################################################################################
# Order
####################################################################################################


####################################################################################################
# Table
####################################################################################################

####################################################################################################
# Stock
####################################################################################################
class Stocks(BaseModel):
    name:str
    price:int
    amount:int
    
    class Config:
        orm_mode = True
        
class StocksCreate(BaseModel):
    name:str
    price:int
    amount:int
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('입력된 이름이 없습니다.')
        return v
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('가격은 0보다 커야 합니다.')
        return v
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('재고는 0보다 커야 합니다.')
        return v
    
class StocksList(BaseModel):
    total: int = 0
    stocks_list: List[Stocks] = []
    
class StocksUpdate(StocksCreate):
    stock_id : int

class StocksDelete(BaseModel):
    stock_id : int
    
