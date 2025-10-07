#!/bin/bash

# 设置脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR/.."

# 定义C程序路径
DB_EXEC="$PROJECT_DIR/db"

# 检查C程序是否存在
if [ ! -x "$DB_EXEC" ]; then
    echo "错误：找不到可执行的C程序 $DB_EXEC"
    exit 1
fi

# 准备测试数据（完整basic_info + 空数组）
TEST_USER_ID=7
TEST_DATA='{"basic_info": {"id": 7, "name": "测试用户", "email": "test@example.com", "phone": "13800000007", "address": "地址A", "linkedin": "l", "github": "g"}, "educations": [], "experiences": [], "skills": [], "projects": []}'

# 打印测试信息
echo "=== 直接测试C程序数据库功能（v2）==="
echo "C程序路径: $DB_EXEC"
echo "测试用户ID: $TEST_USER_ID"
echo "测试数据: $TEST_DATA"

# 切换到项目根目录
echo -e "\n1. 保存数据到C程序数据库："
cd "$PROJECT_DIR"
mkdir -p resume_data

# 调用C程序保存数据
SAVE_OUTPUT=$(echo "$TEST_DATA" | "$DB_EXEC" save)
SAVE_EXIT_CODE=$?

# 检查保存结果
echo "保存命令输出: $SAVE_OUTPUT"
echo "保存退出码: $SAVE_EXIT_CODE"

if [ $SAVE_EXIT_CODE -eq 0 ]; then
    echo "保存成功！"
    
    # 调用C程序读取数据
    echo -e "\n2. 从C程序数据库读取数据："
    LOAD_OUTPUT=$("$DB_EXEC" load $TEST_USER_ID)
    LOAD_EXIT_CODE=$?
    
    # 检查读取结果
    echo "读取命令输出: $LOAD_OUTPUT"
    echo "读取退出码: $LOAD_EXIT_CODE"
    
    # 验证读取到的完整结构和关键字段
    if [ $LOAD_EXIT_CODE -eq 0 ] \
       && echo "$LOAD_OUTPUT" | grep -q '"basic_info"' \
       && echo "$LOAD_OUTPUT" | grep -q '"name":"测试用户"' \
       && echo "$LOAD_OUTPUT" | grep -q '"email":"test@example.com"' \
       && echo "$LOAD_OUTPUT" | grep -q '"educations":\[' \
       && echo "$LOAD_OUTPUT" | grep -q '"experiences":\[' \
       && echo "$LOAD_OUTPUT" | grep -q '"skills":\[' \
       && echo "$LOAD_OUTPUT" | grep -q '"projects":\['; then
        echo -e "\n✅ 测试成功！数据保存和读取功能正常工作。"
        echo "完整读取数据: $LOAD_OUTPUT"
    else
        echo -e "\n❌ 测试失败！读取的数据不正确或结构不完整。"
        exit 1
    fi
else
    echo -e "\n❌ 测试失败！保存数据失败。"
    exit 1
fi