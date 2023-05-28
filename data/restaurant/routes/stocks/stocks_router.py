from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from database import get_db

from routes.stocks import stocks_schema, stocks_crud
from models import Stocks

router = APIRouter(
    prefix="/api/stocks",
    tags=["stocks"]
)

@router.get("/list",response_model = stocks_schema.StocksList)
def get_stocks_list(db:Session = Depends(get_db),
                    page:int = 0,
                    size:int = 10):
    
    total,_stock_list = stocks_crud.get_stocks_list(db,skip=page*size,limit=size)
    
    return {
        'total':total,
        'stock_list':_stock_list
    }
    
@router.get("/detail/{stock_id}",response_model = stocks_schema.Stocks)
def get_stock(stock_id:int,db:Session = Depends(get_db)):
    stock = stocks_crud.get_stock(db,stock_id=stock_id)
    return stock

@router.post("/create",status_code=status.HTTP_204_NO_CONTENT)
def create_stocks(_stock_create:stocks_schema.StocksCreate,
                  db:Session = Depends(get_db)):
    stocks_crud.create_stocks(db=db,stock_create=_stock_create)
    
@router.put("/update",status_code=status.HTTP_204_NO_CONTENT)
def update_stocks(_stock_update:stocks_schema.StocksUpdate,
                    db:Session = Depends(get_db)):
        
        db_stock = stocks_crud.get_stock(db,stock_id=_stock_update.stock_id)
        # 해당 번호의 재료가 없을 시, 400 에러를 반환
        if not db_stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="데이터를 찾을수 없습니다.")
        
        stocks_crud.update_stocks(db=db,db_stock=db_stock,stock_update=_stock_update)

@router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
def delete_stocks(_stock_delete:stocks_schema.StocksDelete,
                  db:Session=Depends(get_db)):
    db_stock = stocks_crud.get_stock(db,stock_id=_stock_delete.stock_id)
    if not db_stock:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    stocks_crud.delete_stocks(db=db,db_stock=db_stock)
    