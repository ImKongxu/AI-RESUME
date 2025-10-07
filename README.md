# AI简历生成器

一个基于FastAPI和DeepSeek API的智能简历生成系统，能够根据用户输入快速生成专业的Markdown格式简历，并支持转换为PDF文档。

## 🚀 功能特性

- **AI驱动的简历生成**：利用DeepSeek大语言模型根据用户提供的信息生成专业简历
- **Markdown格式输出**：所有生成的简历内容均以标准Markdown格式输出
- **PDF转换功能**：支持将Markdown格式的简历一键转换为PDF文件
- **简历修改功能**：支持对现有简历进行修改和优化
- **RESTful API设计**：采用标准RESTful API设计，便于集成到其他系统
- **异步处理**：使用FastAPI的异步特性，提高服务响应性能

## 🛠️ 技术栈

- **后端框架**：FastAPI
- **AI模型**：DeepSeek API (通过OpenAI兼容接口)
- **PDF生成**：Markdown + WeasyPrint
- **依赖管理**：pip
- **开发语言**：Python 3.12

## 📋 项目结构

## 🔧 安装指南

### 1. 克隆项目

```bash
# 克隆项目到本地
git clone <项目仓库地址>
cd AI-RESUME
```

### 2. 创建虚拟环境

```bash
# 创建Python虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
source .venv/Scripts/activate
# Linux/Mac
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录创建`.env`文件，并添加以下内容：

```env
# DeepSeek API密钥
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

> 注意：您需要从[DeepSeek官网](https://deepseek.com/)获取API密钥。

## 🚀 启动服务

```bash
# 开发模式启动（支持热重载）
uvicorn main:app --reload

# 或使用Python直接运行
python main.py
```

服务启动后，可访问以下地址：
- API文档：http://127.0.0.1:8000/docs
- 备用API文档：http://127.0.0.1:8000/redoc
- 首页：http://127.0.0.1:8000/

## 📖 API使用说明

### 1. 生成新简历

**请求**：

**请求体**：
```json
{
  "content_request": "请根据以下信息生成一份简历：姓名：张三，计算机科学专业毕业，有3年前端开发经验...",
  "system_prompt": "可选的自定义系统提示词"
}
```

**响应**：
```json
{
  "success": true,
  "generated_content": "# 张三的简历\n\n## 个人信息\n- 姓名：张三\n...",
  "message": "简历内容生成成功（Markdown格式）"
}
```

### 2. 修改现有简历

**请求**：

**请求体**：
```json
{
  "resume_content": "现有的Markdown格式简历内容...",
  "revision_request": "请将工作经验部分优化，突出我的项目成果..."
}
```

**响应**：
```json
{
  "success": true,
  "generated_content": "# 张三的简历\n\n## 个人信息\n- 姓名：张三\n...",
  "message": "简历内容修改成功（Markdown格式）"
}
```

### 3. 转换为PDF

**请求**：