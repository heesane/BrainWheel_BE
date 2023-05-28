from pydantic import BaseModel, validator

class Table(BaseModel):
    id:int
    table_id = int
    customer_count:int
    total_price:int
    orders_id:int
    class Config:
        orm_mode = True
        
class TableCreate(BaseModel):
    customer_count:int
    total_price:int
    menu:list[]
    
    @validator('customer_count', 'total_price', 'menu')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
    
class TableList(BaseModel):
    total:int = 0
    table_list : list[Table] = []
    
class TableUpdate(BaseModel):
    customer_count:int
    total_price:int
    menu:dict
    
    @validator('customer_count', 'total_price', 'menu')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v