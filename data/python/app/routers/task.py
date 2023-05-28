from fastapi import APIRouter
from starlette.responses import FileResponse
import os
from tool import login_admin_mysql,make_csv,training

router = APIRouter(prefix="/api/task", tags=["task"])

# Flag 수신 처리 함수
# /flag/hhs?flag=inf_success
@router.get("/flag/{user_name}")
async def ReceiveFlag(user_name: str, flag: str):
    conn = login_admin_mysql()
    
    with conn.cursor() as db:
        db.execute("Select * from `userinfo`.`users` where `username` = %s;", user_name)
            
        # Flag: inf_success -> csv_success -> h5_success
        if flag == "inf_success":
            
            db.execute("UPDATE `userinfo`.`users` SET `inf_success` = '1' WHERE (`username` = %s);", user_name)
            
            while make_csv(user_name) != True:
                continue
            
            db.execute("UPDATE `userinfo`.`users` SET `csv_success` = '1' WHERE (`username` = %s);", user_name)
            
            return {"flag": "Make CSV Success"}
        
        elif flag == "csv_success":
            first_csv = user_name + "_first.csv"
            second_csv = user_name + "_second.csv"
            weight_file = user_name + ".h5"
            
            while training(first_csv,second_csv,weight_file) != True:
                continue
            
            db.execute("UPDATE `userinfo`.`users` SET `h5_success` = '1' WHERE (`username` = %s);", user_name)
            return {"flag": "Make H5 Success"}

# h5 파일 다운로드 함수
# /download/1
@router.get("/download/{user_id}")
async def download_h5(user_id: int):    
    conn = login_admin_mysql()
    
    with conn.cursor() as db:
        db.execute("Select download_success from `userinfo`.`users` where `id` = %s;", user_id)
        
        if db.fetchone()[0] == 0:
            return {"message": "Flag not found."}
        
        else:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(current_dir, "tool", "h5_file", str(user_id) + ".h5")
            
            if os.path.exists(file_path):
                return FileResponse(file_path, media_type='routerlication/hdf5', filename=str(user_id) + ".h5")
            
            else:
                return {"message": "File not found."}

# 정확도 측정 결과
# http://localhost:8000/accurate?user_name=hhs&result=100
@router.post("/accurate")
async def end_result(user_name: str, result: int):
    conn =login_admin_mysql()
    cur = conn.cursor()
    cur.execute("Select target_accurate from `userinfo`.`users` where `username` = %s;", user_name)
    target_accurate = cur.fetchone()[0]
    if result > target_accurate:
        cur.execute("UPDATE `userinfo`.`users` SET `result`= %d ,`flag` = '1', `activation` = `True` WHERE (`username` = %s);", result,user_name)
        conn.commit()
        conn.close()
        return {"message": "You Can Use BrainWheel"}
    else:
        cur.execute("UPDATE `userinfo`.`users` SET `result`= %d ,`flag` = '0', `activation` = `False` WHERE (`username` = %s);", result,user_name)
        conn.commit()
        conn.close()
        return {"message": "You Can't Use BrainWheel"}

@router.get("/download")
async def download_python_file():
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, "func", "user.py")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='text/plain', filename="user.py")
    else:
        return {"message": "File not found."}