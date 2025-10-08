from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.resume_router import router as resume_router
from app.api.user_router import router as user_router
import os
from dotenv import load_dotenv

load_dotenv()

app=FastAPI(
    title="AI简历生成器",
    version="1.0",
    description="一个基于AI的简历生成器，根据用户输入生成专业的简历"
)

# 添加CORS中间件配置
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加路由包含语句

app.include_router(resume_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"message":"AI简历生成器API启动成功"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
