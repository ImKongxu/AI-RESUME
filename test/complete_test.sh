#!/bin/bash

# 完整测试脚本 - 验证C程序数据库的各项功能

# 设置颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 设置C程序路径
C_DB_PATH="/home/imkongxu/youjiankexun/AI-RESUME/db"
DATA_DIR="/home/imkongxu/youjiankexun/AI-RESUME/resume_data"

# 测试结果变量
TEST_PASSED=true

# 函数：打印测试标题
echo_test() {
    echo "\n${GREEN}=== $1 ===${NC}"
}

# 函数：检查命令是否成功执行
check_result() {
    if [ $1 -ne 0 ]; then
        echo "${RED}❌ 测试失败: $2${NC}"
        TEST_PASSED=false
    else
        echo "${GREEN}✅ 测试成功: $2${NC}"
    fi
}

# 清理旧的数据文件
echo_test "清理测试环境"
if [ -d "$DATA_DIR" ]; then
    rm -f "$DATA_DIR"/*.dat
    echo "已删除所有数据文件"
else
    mkdir -p "$DATA_DIR"
    echo "已创建数据目录"
fi

echo_test "测试1: 基本保存和读取功能（含完整basic_info与空数组）"
# 测试数据
TEST_DATA='{"basic_info": {"id": 10, "name": "测试用户", "email": "test@example.com", "phone": "13800138000", "address": "北京市海淀区", "linkedin": "lnk", "github": "gh"}, "educations": [], "experiences": [], "skills": [], "projects": []}'

# 保存数据
SAVE_OUTPUT=$(echo "$TEST_DATA" | "$C_DB_PATH" save)
SAVE_EXIT_CODE=$?
echo "保存命令输出: $SAVE_OUTPUT"

# 检查保存是否成功
if [[ $SAVE_OUTPUT == *"success"* ]] && [ $SAVE_EXIT_CODE -eq 0 ]; then
    check_result 0 "数据保存成功"
else
    check_result 1 "数据保存失败"
fi

# 读取数据
LOAD_OUTPUT=$("$C_DB_PATH" load 10)
LOAD_EXIT_CODE=$?
echo "读取命令输出: $LOAD_OUTPUT"

# 检查读取是否成功且包含完整basic_info键与值
if [[ $LOAD_OUTPUT == *"\"basic_info\""* ]] \
   && [[ $LOAD_OUTPUT == *"\"name\":\"测试用户\""* ]] \
   && [[ $LOAD_OUTPUT == *"\"email\":\"test@example.com\""* ]] \
   && [[ $LOAD_OUTPUT == *"\"phone\":\"13800138000\""* ]] \
   && [[ $LOAD_OUTPUT == *"\"address\":\"北京市海淀区\""* ]] \
   && [[ $LOAD_OUTPUT == *"\"linkedin\":\"lnk\""* ]] \
   && [[ $LOAD_OUTPUT == *"\"github\":\"gh\""* ]] \
   && [[ $LOAD_OUTPUT == *"\"educations\":["* ]] \
   && [[ $LOAD_OUTPUT == *"\"experiences\":["* ]] \
   && [[ $LOAD_OUTPUT == *"\"skills\":["* ]] \
   && [[ $LOAD_OUTPUT == *"\"projects\":["* ]] \
   && [ $LOAD_EXIT_CODE -eq 0 ]; then
    check_result 0 "读取返回完整结构并包含正确basic_info"
else
    check_result 1 "读取结果不完整或basic_info不匹配"
fi

echo_test "测试2: 读取不存在的用户ID"
LOAD_INVALID_OUTPUT=$("$C_DB_PATH" load 999)
LOAD_INVALID_EXIT_CODE=$?
echo "读取不存在用户输出: $LOAD_INVALID_OUTPUT"
if [[ $LOAD_INVALID_OUTPUT == *"未找到用户ID"* ]] && [ $LOAD_INVALID_EXIT_CODE -eq 0 ]; then
    check_result 0 "正确处理不存在的用户ID"
else
    check_result 1 "未正确处理不存在的用户ID"
fi

echo_test "测试3: 多用户数据保存和读取（核验不同用户的basic_info）"
TEST_DATA_2='{"basic_info": {"id": 11, "name": "用户二", "email": "user2@example.com", "phone": "", "address": "", "linkedin": "", "github": ""}, "educations": []}'
SAVE_OUTPUT_2=$(echo "$TEST_DATA_2" | "$C_DB_PATH" save)
LOAD_USER10=$("$C_DB_PATH" load 10)
LOAD_USER11=$("$C_DB_PATH" load 11)
if [[ $LOAD_USER10 == *"\"name\":\"测试用户\""* ]] && [[ $LOAD_USER11 == *"\"name\":\"用户二\""* ]]; then
    check_result 0 "多用户数据保存和读取正常工作"
else
    check_result 1 "多用户数据保存和读取出现问题"
fi

echo_test "测试4: 数据文件存在性与大小"
ls -la "$DATA_DIR"/basic_info.dat || true
[ -s "$DATA_DIR"/basic_info.dat ]
check_result $? "basic_info.dat 文件已创建且非空"

echo_test "测试总结"
if $TEST_PASSED; then
    echo "${GREEN}✅ 所有测试通过！C程序数据库功能正常工作。${NC}"
else
    echo "${RED}❌ 有测试失败！请检查C程序数据库的实现。${NC}"
fi