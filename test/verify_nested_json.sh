#!/bin/bash

# 简单验证脚本 - 重点测试嵌套JSON对象的解析和存储

# 设置颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 设置C程序路径
C_DB_PATH="/home/imkongxu/youjiankexun/AI-RESUME/db"
DATA_DIR="/home/imkongxu/youjiankexun/AI-RESUME/resume_data"

# 清理旧的数据文件
echo -e "${GREEN}=== 清理测试环境 ===${NC}"
if [ -d "$DATA_DIR" ]; then
    rm -f "$DATA_DIR"/*.dat
    echo "已删除所有数据文件"
else
    mkdir -p "$DATA_DIR"
    echo "已创建数据目录"
fi

echo -e "\n${GREEN}=== 测试嵌套JSON对象解析 ===${NC}"

# 测试数据 - 包含嵌套的basic_info对象
TEST_DATA='{"basic_info": {"id": 15, "name": "嵌套JSON测试用户", "email": "nested@example.com", "phone": "13900139000", "address": "上海市浦东新区"}, "educations": [{"school": "测试大学", "degree": "学士"}]}'

echo "测试数据: $TEST_DATA"

# 保存数据
echo -e "\n${GREEN}保存数据...${NC}"
SAVE_OUTPUT=$(echo "$TEST_DATA" | "$C_DB_PATH" save)
echo "保存命令输出: $SAVE_OUTPUT"

# 检查数据文件大小
echo -e "\n${GREEN}数据文件状态:${NC}"
ls -la "$DATA_DIR"/basic_info.dat

# 读取数据
echo -e "\n${GREEN}读取数据...${NC}"
LOAD_OUTPUT=$("$C_DB_PATH" load 15)
echo "读取命令输出: $LOAD_OUTPUT"

# 验证读取结果
if [[ $LOAD_OUTPUT == *"嵌套JSON测试用户"* ]] && [[ $LOAD_OUTPUT == *"nested@example.com"* ]] && [[ $LOAD_OUTPUT == *"13900139000"* ]] && [[ $LOAD_OUTPUT == *"上海市浦东新区"* ]]; then
    echo -e "\n${GREEN}✅ 验证成功！所有字段都被正确解析和存储！${NC}"
else
    echo -e "\n${RED}❌ 验证失败！某些字段没有被正确解析和存储。${NC}"
    echo "缺失的字段："
    if [[ $LOAD_OUTPUT != *"嵌套JSON测试用户"* ]]; then echo "- 用户名"; fi
    if [[ $LOAD_OUTPUT != *"nested@example.com"* ]]; then echo "- 邮箱"; fi
    if [[ $LOAD_OUTPUT != *"13900139000"* ]]; then echo "- 电话"; fi
    if [[ $LOAD_OUTPUT != *"上海市浦东新区"* ]]; then echo "- 地址"; fi
fi

echo -e "\n${GREEN}=== 测试完成 ===${NC}"