from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import user_db_service

router = APIRouter()

class UserIn(BaseModel):
    user_id: str
    credential: int

class UserOut(BaseModel):
    user_id: str
    credential: int

@router.post('/user', response_model=UserOut)
def create_user(user: UserIn):
    success = user_db_service.add_user(user.user_id, user.credential)
    if not success:
        raise HTTPException(status_code=400, detail='User ID already exists')
    return user

@router.get('/user/{user_id}', response_model=UserOut)
def read_user(user_id: str):
    credential = user_db_service.get_user(user_id)
    if credential is None:
        raise HTTPException(status_code=404, detail='User not found')
    return UserOut(user_id=user_id, credential=credential)
