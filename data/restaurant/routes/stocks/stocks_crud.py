from sqlalchemy.orm import Session
from routes.stocks.stocks_schema import StocksCreate,StockUpdate
from models import Stocks

# 재고 전체 리스트 조회
def get_stocks_list(db:Session, skip:int = 0, limit:int = 10):
    stocks_list = db.query(Stocks).offset(skip).limit(limit).all()
    total = db.query(Stocks).count()
    return total, stocks_list

# 재고 상세 조회
def get_stock(db:Session, stock_id:int):
    stock = db.query(Stocks).get(stock_id)
    return stock

def create_stocks(db:Session, stock_create:StocksCreate):
    db_stock = Stocks(name=stock_create.name, price=stock_create.price, amount=stock_create.amount)
    db.add(db_stock)
    db.commit()
    
def update_stocks(db:Session,stock:Stocks, stock_update:StockUpdate):
    stock.name = stock_update.name
    stock.price = stock_update.price
    stock.amount = stock_update.amount
    db.add(stock)
    db.commit()
    
def delete_stocks(db:Session, stock:Stocks):
    db.delete(stock)
    db.commit()