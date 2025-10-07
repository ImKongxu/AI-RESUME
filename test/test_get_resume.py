import requests
import json

# API端点URL
get_resume_url = "http://127.0.0.1:8081/api/resume/get-resume/1"

try:
    print("正在发送get-resume请求...")
    response = requests.get(get_resume_url)
    
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