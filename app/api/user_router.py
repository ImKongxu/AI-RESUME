
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import user_db_service

# 创建路由器对象
router = APIRouter()

# 请求体模型：用于接收用户数据
class UserIn(BaseModel):
    user_id: str  # 用户自定义ID
    credential: int  # 用户凭证

# 响应体模型：返回用户数据
class UserOut(BaseModel):
    user_id: str
    credential: int

@router.post('/user', response_model=UserOut)
def create_user(user: UserIn):
    """
    新增用户接口。
    请求体：user_id（字符串），credential（整数）
    返回：用户信息
    """
    success = user_db_service.add_user(user.user_id, user.credential)
    if not success:
        # 用户ID已存在
        raise HTTPException(status_code=400, detail='用户ID已存在')
    return user

@router.get('/user/{user_id}', response_model=UserOut)
def read_user(user_id: str):
    """
    查询用户接口。
    路径参数：user_id（字符串）
    返回：用户信息
    """
    credential = user_db_service.get_user(user_id)
    if credential is None:
        # 用户不存在
        raise HTTPException(status_code=404, detail='用户不存在')
    return UserOut(user_id=user_id, credential=credential)
