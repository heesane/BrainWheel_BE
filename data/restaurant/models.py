from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# 음식에 대한 기본적인 테이블
class Foods(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    ingredients_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    ingredients = relationship("Ingredients", backref="foods")
    orders = relationship("Orders", backref="foods")
# 음식을 만들 때 필요한 재료의 정보 저장 테이블
class Ingredients(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"))
    name = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    orders = relationship("Orders", backref="ingredients")

# 현재 가게 내에 저장된 재료의 정보 저장 테이블
class Stocks(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    

class Tables(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, nullable=False)
    customer_count = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    orders_id = Column(Integer, ForeignKey("orders.id"))
    orders = relationship("Orders", backref="tables")


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    
    table_id = Column(Integer, ForeignKey("tables.id"))
    food_id = Column(Integer, ForeignKey("foods.id"))
    ingredients_id = Column(Integer, ForeignKey("ingredients.id"))
    
    amount = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
