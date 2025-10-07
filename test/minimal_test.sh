#!/bin/bash

# 设置脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 定义C程序路径
DB_EXEC="$SCRIPT_DIR/db"

# 测试用户ID
TEST_USER_ID=8

# 准备简单的测试数据
TEST_DATA='{"basic_info": {"id": 8, "name": "Minimal User", "email": "minimal@test.com"}, "educations": []}'

# 打印测试信息
echo "=== 最小化测试 ==="
echo "C程序路径: $DB_EXEC"
echo "测试用户ID: $TEST_USER_ID"
echo "测试数据: $TEST_DATA"

# 切换到C程序所在目录
cd "$SCRIPT_DIR"

# 先删除之前的basic_info.dat文件（为了干净的测试环境）
echo "\n1. 删除旧的数据文件（如果存在）："
rm -f resume_data/basic_info.dat
ls -la resume_data/

# 创建新的basic_info.dat文件
echo "\n2. 创建空的basic_info.dat文件："
touch resume_data/basic_info.dat
ls -la resume_data/basic_info.dat

# 调用C程序保存数据
echo "\n3. 保存数据到C程序数据库："
SAVE_OUTPUT=$(echo "$TEST_DATA" | $DB_EXEC save)
SAVE_EXIT_CODE=$?

echo "保存命令输出: $SAVE_OUTPUT"
echo "保存退出码: $SAVE_EXIT_CODE"

# 检查文件大小变化
echo "\n4. 检查数据文件大小变化："
ls -la resume_data/basic_info.dat

echo "\n5. 查看数据文件内容（使用strings命令）："
strings resume_data/basic_info.dat

# 调用C程序读取数据
echo "\n6. 从C程序数据库读取数据："
LOAD_OUTPUT=$($DB_EXEC load $TEST_USER_ID)
LOAD_EXIT_CODE=$?

echo "读取命令输出: $LOAD_OUTPUT"
echo "读取退出码: $LOAD_EXIT_CODE"

# 总结测试结果
echo "\n=== 测试总结 ==="
if [ $LOAD_EXIT_CODE -eq 0 ] && echo "$LOAD_OUTPUT" | grep -q "Minimal User"; then
    echo "✅ 测试成功！数据保存和读取功能正常工作。"
else
    echo "❌ 测试失败！数据保存或读取功能有问题。"
fi