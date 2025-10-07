import requests
import json

# 定义API地址
save_api_url = "http://127.0.0.1:8081/api/resume/save-resume"
get_api_url = "http://127.0.0.1:8081/api/resume/get-resume/6"

# 准备测试数据
test_resume_data = {
    "basic_info": {
        "id": 6,  # 改为整数类型
        "name": "孙七",
        "email": "sunqi@example.com",
        "phone": "13800138005",
        "address": "深圳市南山区",
        "linkedin": "linkedin.com/in/sunqi",
        "github": "github.com/sunqi"
    },
    "educations": [
        {
            "id": "1",
            "user_id": 6,  # 改为整数类型
            "school": "深圳大学",
            "degree": "硕士",
            "major": "人工智能",
            "start_date": "2021-09-01",
            "end_date": "2024-06-30",
            "gpa": "3.8"
        }
    ]
}

print("=== 测试简历数据保存和读取流程 ===")

# 测试保存功能
print(f"\n1. 发送保存请求到 {save_api_url}")
print(f"发送的数据: {json.dumps(test_resume_data, ensure_ascii=False)}")

try:
    # 发送POST请求保存简历数据
    save_response = requests.post(save_api_url, json=test_resume_data)
    
    # 打印保存结果
    print(f"保存响应状态码: {save_response.status_code}")
    print(f"保存响应内容: {save_response.text}")
    
    if save_response.status_code == 200:
        # 测试读取功能
        print(f"\n2. 发送读取请求到 {get_api_url}")
        get_response = requests.get(get_api_url)
        
        # 打印读取结果
        print(f"读取响应状态码: {get_response.status_code}")
        print(f"读取响应内容: {get_response.text}")
        
        # 检查是否成功读取到数据
        get_data = get_response.json()
        if get_data.get("success") and "data" in get_data and "error" not in get_data["data"]:
            print("\n✅ 测试成功！数据保存和读取功能正常工作。")
            print(f"读取到的数据: {json.dumps(get_data['data'], ensure_ascii=False)}")
        else:
            print("\n❌ 测试失败！数据保存成功但读取失败。")
    else:
        print("\n❌ 测试失败！保存请求失败。")
        
except Exception as e:
    print(f"\n❌ 测试过程中发生错误: {str(e)}")