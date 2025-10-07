#!/bin/bash

# 定义C程序路径
DB_PROGRAM="db"
DB_DIR="/home/imkongxu/youjiankexun/AI-RESUME"

# 准备测试数据
TEST_DATA='{"basic_info":{"id":"5","name":"赵六","email":"zhaoliu@example.com","phone":"13800138004"}}'

# 创建临时文件存储测试数据
TEST_INPUT="/tmp/test_resume_input.json"
echo "$TEST_DATA" > "$TEST_INPUT"

# 确保在C程序的工作目录执行
cd "$DB_DIR"

# 测试保存功能
echo "=== 直接测试C程序数据库功能 ==="
echo "\n1. 调用C程序保存数据"
echo "发送的数据: $TEST_DATA"

# 调用C程序保存数据
SAVE_OUTPUT=$(cat "$TEST_INPUT" | "./$DB_PROGRAM" save)
SAVE_EXIT_CODE=$?

echo "保存退出码: $SAVE_EXIT_CODE"
echo "保存输出: $SAVE_OUTPUT"

if [ $SAVE_EXIT_CODE -eq 0 ]; then
    # 测试读取功能
    echo "\n2. 调用C程序读取数据 (user_id=5)"
    LOAD_OUTPUT=$(./"$DB_PROGRAM" load 5)
    LOAD_EXIT_CODE=$?
    
    echo "读取退出码: $LOAD_EXIT_CODE"
    echo "读取输出: $LOAD_OUTPUT"
    
    # 检查是否成功读取到数据
    if [[ $LOAD_OUTPUT != *"error"* ]]; then
        echo "\n✅ 测试成功！C程序能够正确保存和读取数据。"
    else
        echo "\n❌ 测试失败！C程序能够保存数据但无法读取。"
    fi
else
    echo "\n❌ 测试失败！C程序保存数据失败。"
fi

# 清理临时文件
rm "$TEST_INPUT"