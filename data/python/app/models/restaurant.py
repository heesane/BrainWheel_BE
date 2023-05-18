from pydantic import BaseModel


class Food(BaseModel):
    name: str = None
    price: int = None
    Ingredients: dict = None


class Ingredient(BaseModel):
    name: str = None
    price: int = None
    amount: int = None


class Table(BaseModel):
    table_number: int = None
    people: int = 0
    food: dict = None
    total_price: int = 0
    is_empty: bool = True


class Call(BaseModel):
    content: str = None
    table_id: int = None
    amount: int = 1
