from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from routes.table import table_schema, table_crud

router = APIRouter(
    prefix="/api/table",
    tags=["table"]
)

@router.get("/list", response_model=table_schema.TableList)
def table_list(db: Session = Depends(get_db)):
    total,table_list = table_crud.get_table_list(db)
    return {
        'total table': total,
        'table_list': table_list
    }
    
@router.get("/detail/{table_id}", response_model=table_schema.Table)
def table_detail(table_id: int, db: Session = Depends(get_db)):
    table = table_crud.get_table(db, table_id=table_id)
    return table

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def table_create(_table_create: table_schema.TableCreate,
                db: Session = Depends(get_db)):
    
    for menu in _table_create.menu:
        _table_create.total_price += menu.price * menu.amount
        
    total_price = _table_create.menu.price
    table_crud.create_table(db=db, table_create=_table_create)
    

@router.put("/update/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def table_update(table_id: int, _table_update: table_schema.TableUpdate,
                db: Session = Depends(get_db)):
    table_crud.update_table(db=db, table_id=table_id, table_update=_table_update)
    
@router.delete("/delete/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def table_delete(table_id: int, db: Session = Depends(get_db)):
    table_crud.delete_table(db=db, table_id=table_id)
    