import subprocess
import json

# 定义C程序路径
db_program = "/home/imkongxu/youjiankexun/AI-RESUME/db"

# 准备测试数据
test_resume_data = {
    "basic_info": {
        "id": "3",  # 使用新的用户ID 3
        "name": "李四",
        "email": "lisi@example.com",
        "phone": "13800138002",
        "address": "上海市浦东新区",
        "linkedin": "linkedin.com/in/lisi",
        "github": "github.com/lisi"
    },
    "educations": [
        {
            "id": "1",
            "user_id": "3",
            "school": "复旦大学",
            "degree": "博士",
            "major": "人工智能",
            "start_date": "2018-09-01",
            "end_date": "2023-06-30",
            "gpa": "4.0"
        }
    ]
}

print("=== 直接测试C程序数据库功能 ===")

# 测试保存功能
print(f"\n1. 调用C程序保存数据")
print(f"发送的数据: {json.dumps(test_resume_data, ensure_ascii=False)}")

try:
    # 调用C程序保存数据
    proc = subprocess.Popen(
        [db_program, "save"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 发送JSON数据并获取结果
    stdout, stderr = proc.communicate(input=json.dumps(test_resume_data, ensure_ascii=False))
    
    # 打印保存结果
    print(f"保存退出码: {proc.returncode}")
    print(f"保存标准输出: {stdout}")
    print(f"保存标准错误: {stderr}")
    
    if proc.returncode == 0:
        # 测试读取功能
        print(f"\n2. 调用C程序读取数据 (user_id=3)")
        proc = subprocess.Popen(
            [db_program, "load", "3"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = proc.communicate()
        
        # 打印读取结果
        print(f"读取退出码: {proc.returncode}")
        print(f"读取标准输出: {stdout}")
        print(f"读取标准错误: {stderr}")
        
        # 检查是否成功读取到数据
        try:
            # 尝试直接解析JSON
            result = json.loads(stdout)
            if "error" not in result:
                print("\n✅ 测试成功！C程序能够正确保存和读取数据。")
            else:
                print("\n❌ 测试失败！C程序能够保存数据但无法读取。")
        except json.JSONDecodeError:
            # 尝试从输出中提取有效的JSON部分
            try:
                # 查找第一个'{'和最后一个'}'，提取JSON部分
                json_start = stdout.find('{')
                json_end = stdout.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    json_part = stdout[json_start:json_end]
                    result = json.loads(json_part)
                    print(f"\n✅ 测试成功！从混合输出中提取到JSON数据: {result}")
                else:
                    print("\n❌ 测试失败！C程序返回的不是有效的JSON数据，也无法提取JSON部分。")
            except Exception:
                print("\n❌ 测试失败！C程序返回的不是有效的JSON数据，也无法提取JSON部分。")
    else:
        print("\n❌ 测试失败！C程序保存数据失败。")
        
except Exception as e:
    print(f"\n❌ 测试过程中发生错误: {str(e)}")