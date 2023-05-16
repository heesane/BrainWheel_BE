from pydantic import BaseModel
# Path: models\user.py
# Python Class for API Request Body

class UserInfo(BaseModel):
    created_at: str = None
    username: str = None
    password: str = None
    target_accurate: int = None