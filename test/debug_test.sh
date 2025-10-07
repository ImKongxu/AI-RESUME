#!/bin/bash

# 设置脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR/.."

# 定义C程序路径
DB_EXEC="$PROJECT_DIR/db"

# 测试用户ID
TEST_USER_ID=9

# 准备完整测试数据（包含basic_info全字段与空数组）
TEST_DATA='{"basic_info": {"id": 9, "name": "Debug User", "email": "debug@test.com", "phone": "13800000009", "address": "", "linkedin": "", "github": ""}, "educations": [], "experiences": [], "skills": [], "projects": []}'

# 打印测试信息
echo "=== 调试测试 ==="
echo "C程序路径: $DB_EXEC"
echo "测试用户ID: $TEST_USER_ID"
echo "测试数据: $TEST_DATA"

# 切换到项目根目录
cd "$PROJECT_DIR"

# 确保数据目录存在
echo "\n1. 准备数据目录："
mkdir -p resume_data
ls -la resume_data/ || true

# 先删除之前的basic_info.dat文件
echo "\n2. 删除旧的 basic_info.dat："
rm -f resume_data/basic_info.dat
ls -la resume_data/ || true

# 创建新的basic_info.dat文件
echo "\n3. 创建空的 basic_info.dat："
touch resume_data/basic_info.dat
ls -la resume_data/basic_info.dat || true

echo "\n4. 调试：使用hexdump查看文件初始状态："
hexdump -C resume_data/basic_info.dat | head -20 || true

# 调用C程序保存数据
echo "\n5. 保存数据到C程序数据库："
echo "$TEST_DATA" | "$DB_EXEC" save

echo "\n6. 查看保存后的数据文件大小："
ls -la resume_data/basic_info.dat || true

echo "\n7. 调试：使用hexdump查看文件内容（寻找用户ID）："
hexdump -C resume_data/basic_info.dat | head -20 || true

# 调用C程序读取数据
echo "\n8. 从C程序数据库读取数据："
LOAD=$( "$DB_EXEC" load $TEST_USER_ID )
echo "$LOAD"

# 校验完整JSON结构
echo "\n9. 校验读取到的JSON结构："
if echo "$LOAD" | grep -q '"basic_info"' \
   && echo "$LOAD" | grep -q '"name":"Debug User"' \
   && echo "$LOAD" | grep -q '"email":"debug@test.com"' \
   && echo "$LOAD" | grep -q '"educations":\[' \
   && echo "$LOAD" | grep -q '"experiences":\[' \
   && echo "$LOAD" | grep -q '"skills":\[' \
   && echo "$LOAD" | grep -q '"projects":\['; then
  echo "✅ JSON结构校验通过"
else
  echo "❌ JSON结构校验失败"
  exit 1
fi

# 函数代码片段参考
echo "\n10. 调试：查看load_basic_info函数的实现："
grep -A20 "load_basic_info" "$PROJECT_DIR/db.cpp" | head -20 || true

echo "\n11. 调试：查看save_basic_info函数的实现："
grep -A20 "save_basic_info" "$PROJECT_DIR/db.cpp" | head -20 || true