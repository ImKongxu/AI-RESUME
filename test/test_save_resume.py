import requests
import json

# API端点URL
save_resume_url = "http://127.0.0.1:8081/api/resume/save-resume"

# 准备符合ResumeData模型要求的测试数据
test_data = {
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
            "degree": "学士",
            "major": "计算机科学",
            "start_date": "2018-09",
            "end_date": "2022-06",
            "gpa": 3.8,
            "description": "主修计算机科学，辅修人工智能"
        }
    ]
}

try:
    print("正在发送save-resume请求...")
    response = requests.post(
        save_resume_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(test_data, ensure_ascii=False)
    )
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    # 尝试解析JSON响应
    try:
        response_json = response.json()
        print(f"JSON格式响应: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
    except json.JSONDecodeError:
        print("响应不是有效的JSON格式")
        
except Exception as e:
    print(f"请求发送失败: {str(e)}")