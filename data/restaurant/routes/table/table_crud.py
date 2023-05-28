from routes.table import table_schema
from models import Tables
from sqlalchemy.orm import Session  

def get_table_list(db:Session):
    table_list = db.query(Tables).all()
    total = table_list.count()
    
    return total,table_list

def get_table(db:Session, table_id:int):
    table = db.query(Tables).get(table_id)
    return table

def create_table(db:Session, table_create:table_schema.TableCreate):
    db_table = Tables(customer_count=table_create.customer_count,
                      total_price=table_create.total_price,
                      menu=table_create.menu)
    db.add(db_table)
    db.commit()
    
def update_table(db:Session, table_id:int, table_update:table_schema.TableUpdate):
    db_table = db.query(Tables).get(table_id)
    db_table.customer_count = table_update.customer_count
    db_table.total_price = table_update.total_price
    db_table.menu = table_update.menu
    db.commit()
        

def delete_table(db:Session,table_id:int):
    db_table = db.query(Tables).get(table_id)
    db.delete(db_table)
    db.commit()