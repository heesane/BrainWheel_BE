from pydantic import BaseModel, validator

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