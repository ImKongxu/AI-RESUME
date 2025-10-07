import asyncio
from app.services.db_service import DatabaseService

# 测试数据
test_resume_data = {
    "basic_info": {
        "id": 1,
        "name": "测试用户",
        "email": "test@example.com",
        "phone": "13800138000",
        "address": "北京市海淀区",
        "linkedin": "https://linkedin.com/in/test",
        "github": "https://github.com/test"
    },
    "educations": [
        {
            "id": 1,
            "school": "北京大学",
            "degree": "硕士",
            "major": "计算机科学与技术",
            "start_date": "2019-09-01",
            "end_date": "2022-06-30",
            "gpa": 3.9,
            "description": "主要研究方向为人工智能与机器学习"
        }
    ],
    "experiences": [],
    "skills": [],
    "projects": []
}

async def test_database_integration():
    print("开始测试Python与C数据库的集成...")
    
    # 初始化数据库服务
    db_service = DatabaseService()
    
    # 测试保存数据
    print("\n测试1: 保存数据到C数据库")
    save_result = await db_service.save_resume_data(test_resume_data)
    print(f"保存结果: {'成功' if save_result else '失败'}")
    
    # 测试读取数据
    print("\n测试2: 从C数据库读取数据")
    loaded_data = await db_service.load_resume_data(1)
    print(f"读取结果: {'成功' if loaded_data else '失败'}")
    
    if loaded_data:
        print(f"读取到的用户名: {loaded_data.get('name', '未找到')}")
        print(f"读取到的用户邮箱: {loaded_data.get('email', '未找到')}")
        print(f"读取到的用户电话: {loaded_data.get('phone', '未找到')}")
    
    # 测试不存在的用户ID
    print("\n测试3: 读取不存在的用户数据")
    non_existent_data = await db_service.load_resume_data(999)
    print(f"读取结果: {'成功获取到数据' if non_existent_data else '未找到数据'}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    asyncio.run(test_database_integration())