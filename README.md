# AI简历生成器

一个基于FastAPI和DeepSeek API的智能简历生成系统，能够根据用户输入快速生成专业的Markdown格式简历，并支持转换为PDF文档，以及简历数据的存储和检索。系统采用模块化设计，包含简历生成、修改、PDF转换和数据持久化等核心功能。

## 🚀 功能特性

- **AI驱动的简历生成**：利用DeepSeek大语言模型根据用户提供的信息生成专业简历
- **Markdown格式输出**：所有生成的简历内容均以标准Markdown格式输出，便于编辑和分享
- **PDF转换功能**：支持将Markdown格式的简历一键转换为PDF文件，支持自定义CSS样式
- **简历修改功能**：支持对现有简历进行修改和优化，提升简历质量
- **简历数据存储与检索**：通过轻量级C数据库实现简历数据的持久化存储和快速检索
- **RESTful API设计**：采用标准RESTful API设计，便于集成到其他系统
- **异步处理**：使用FastAPI的异步特性，提高服务响应性能和并发处理能力
- **CORS跨域支持**：配置了CORS中间件，允许跨域请求，便于前端应用集成
- **自动生成API文档**：集成Swagger UI和ReDoc，提供交互式API文档
- **全面的测试支持**：包含多套测试脚本，验证C程序与Python API的集成情况

## 🛠️ 技术栈

- **后端框架**：FastAPI（高性能异步Web框架）
- **AI模型**：DeepSeek API (通过OpenAI兼容接口)
- **PDF生成**：Markdown + WeasyPrint
- **数据存储**：自定义轻量级C语言数据库
- **依赖管理**：pip
- **开发语言**：Python 3.12
- **API文档**：Swagger UI和ReDoc
- **环境管理**：python-dotenv
- **数据验证**：Pydantic
- **HTTP服务器**：Uvicorn

## 📋 项目结构

```
AI-RESUME/
├── app/                   # 应用主目录
│   ├── api/               # API路由定义
│   │   └── resume_router.py # 简历相关API端点
│   ├── core/              # 核心配置和工具
│   ├── models/            # 数据模型
│   ├── schemas/           # 请求和响应模型
│   └── services/          # 业务逻辑服务
│       ├── db_service.py          # 数据库服务
│       ├── deepseek_service.py    # DeepSeek API服务
│       └── pdf_generator_service.py # PDF生成服务
├── resume_data/           # 简历数据存储目录
│   ├── basic_info.dat     # 基本信息数据文件
│   ├── education.dat      # 教育经历数据文件
│   ├── experience.dat     # 工作经验数据文件
│   ├── projects.dat       # 项目经历数据文件
│   ├── resumes.dat        # 简历数据索引文件
│   └── skills.dat         # 技能数据文件
├── test/                  # 测试脚本和文件
├── .env                   # 环境变量配置
├── main.py                # 应用入口文件
├── requirements.txt       # 项目依赖列表
├── db.cpp                 # C语言数据库实现
├── AI_resume.html         # Web前端界面
└── script.js              # JavaScript脚本
```

### 模块说明

- **app/api/**: 包含所有API路由定义，处理HTTP请求和响应
- **app/services/**: 包含核心业务逻辑，如AI交互、PDF生成和数据库操作
- **app/models/**: 定义数据模型，用于数据结构标准化
- **app/schemas/**: 定义请求和响应模型，用于API数据验证
- **resume_data/**: 存储简历数据的目录，包含多个数据文件
- **test/**: 包含多个测试脚本，用于验证系统功能

## 💾 C 数据库交互说明

后端通过调用可执行文件 `db` 与 C 实现的轻量数据库交互：

- **保存数据**：向 `db save` 的 stdin 写入 JSON 数据
- **读取数据**：执行 `db load <user_id>` 从 stdout 获取 JSON 数据

### 数据存储格式

系统采用多文件存储方式，将不同类型的简历数据存储在单独的文件中：
- **basic_info.dat**: 存储用户基本信息
- **education.dat**: 存储教育经历
- **experience.dat**: 存储工作经验
- **projects.dat**: 存储项目经历
- **skills.dat**: 存储技能信息
- **resumes.dat**: 存储简历数据索引

### 标准 JSON 结构

数据库交互使用的标准JSON结构如下（stdout仅输出JSON，调试信息在stderr）：

```json
{
  "basic_info": {
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com",
    "phone": "13800138000",
    "address": "北京市海淀区",
    "linkedin": "https://linkedin.com/in/zhangsan",
    "github": "https://github.com/zhangsan"
  },
  "educations": [
    {"id": 1, "school": "北京大学", "degree": "本科", "major": "计算机", "start_date": "2018-09-01", "end_date": "2022-06-30", "gpa": 3.8, "description": "描述"}
  ],
  "experiences": [
    {"id": 1, "company": "公司A", "position": "工程师", "start_date": "2022-07-01", "end_date": "2024-06-30", "is_current": 0, "description": "职责描述"}
  ],
  "skills": [
    {"id": 1, "skill_name": "C++", "proficiency": "高级", "category": "语言"}
  ],
  "projects": [
    {"id": 1, "project_name": "项目A", "project_url": "https://example.com", "start_date": "2023-01-01", "end_date": "2023-12-31", "description": "项目描述", "technologies": "C++;Python"}
  ]
}
```

注意：`basic_info.id` 字段为必填，其他数组字段（如educations、experiences等）可传空数组。

## 🧪 测试脚本使用指南

项目提供了多套测试脚本，便于验证 C 程序与 Python API 的集成情况。所有测试脚本位于 `test/` 目录下。

### 运行前置条件

- 已在项目根目录编译出可执行文件 `db`
- Python环境已配置完成

### 测试脚本分类

1. **直连 C 程序完整测试**

```bash
bash test/complete_test.sh
```

- **执行内容**：清理数据文件、保存一条示例数据、校验读取输出包含完整 `basic_info` 与数组键、验证不存在用户ID处理、多用户读写、检查数据文件存在性。
- **期望结果**：所有用例显示“测试成功”。

2. **调试脚本（便于快速定位问题）**

```bash
bash test/debug_test.sh
```

- **执行内容**：在 `resume_data` 下创建空文件、保存一条数据、用 `hexdump` 预览 `basic_info.dat`、读取并校验返回 JSON 结构完整。

3. **直接测试（v2）**

```bash
bash test/direct_c_test_v2.sh
```

- **执行内容**：以最小步骤直连保存/读取，校验返回是否包含完整结构与关键字段。

4. **Python集成测试**

```bash
python -m test.test_c_db
python -m test.test_db_integration
python -m test.test_get_resume
python -m test.test_save_resume
python -m test.test_resume_flow
```

### 问题排查

若任一脚本失败，请按以下步骤排查：
1. 查看脚本输出的“读取命令输出”
2. 检查末尾的调试信息（例如 stderr 中的 `[DEBUG]` 日志）
3. 根据错误定位到 `db.cpp` 或 `app/services/db_service.py` 进行排查
4. 运行 `bash test/verify_nested_json.sh` 验证JSON格式是否正确


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

### 编译C数据库（首次运行时）

```bash
g++ -o db db.cpp -std=c++11
```

### 启动FastAPI服务

```bash
# 开发模式启动（支持热重载，默认端口8000）
uvicorn main:app --reload

# 指定端口启动（例如使用端口8081）
uvicorn main:app --reload --port 8081

# 或使用Python直接运行（默认端口8080）
python main.py
```

服务启动后，可访问以下地址：
- **API文档**：http://127.0.0.1:8000/docs 或 http://127.0.0.1:8081/docs（取决于启动端口，建议使用python运行，默认端口8080，否则需要修改js接口参数）
- **备用API文档**：http://127.0.0.1:8000/redoc 或 http://127.0.0.1:8081/redoc
- **首页**：http://127.0.0.1:8000/ 或 http://127.0.0.1:8081/


## 📖 API使用说明

### 新增：用户ID与凭证API

系统内置了一个简单的用户数据库，支持通过API存储和查询用户自定义ID与int类型凭证。

#### 相关文件
- `app/services/user_db_service.py`：负责用户ID和凭证的数据库操作（基于SQLite），包含详细中文注释。
- `app/api/user_router.py`：提供用户数据的API接口，所有提示词均为中文，便于本地化开发。

#### API接口

- **新增用户**
    - 方法：POST
    - 路径：`/user`
    - 请求体：
      ```json
      {
        "user_id": "自定义ID（字符串）",
        "credential": 12345
      }
      ```
    - 响应：
      - 成功：返回用户信息
      - 失败：`{"detail": "用户ID已存在"}`

- **查询用户凭证**
    - 方法：GET
    - 路径：`/user/{user_id}`
    - 响应：
      - 成功：返回`{"user_id": "xxx", "credential": 12345}`
      - 失败：`{"detail": "用户不存在"}`

> 该功能适合用于用户身份校验、凭证管理等场景。


### 1. 生成新简历

**功能**：根据用户提供的信息生成一份专业的Markdown格式简历

**请求**：
- **方法**: POST
- **路径**: `/api/resume/generate`
- **权限**: 无需认证
- **请求体**：
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

**功能**：根据用户的修改要求优化现有简历内容

**请求**：
- **方法**: POST
- **路径**: `/api/resume/revise`
- **权限**: 无需认证
- **请求体**：
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

**功能**：将Markdown格式的简历内容转换为PDF文件

**请求**：
- **方法**: POST
- **路径**: `/api/resume/markdown-to-pdf`
- **权限**: 无需认证
- **请求体**：
```json
{
  "markdown_content": "# 张三的简历\n\n## 个人信息\n- 姓名：张三\n...",
  "custom_css": "可选的自定义CSS样式"
}
```

**响应**：
- 返回PDF文件，Content-Type为application/pdf，作为附件下载

### 4. 保存简历数据

**功能**：将完整的简历数据保存到数据库中

**请求**：
- **方法**: POST
- **路径**: `/api/resume/save-resume`
- **权限**: 无需认证
- **请求体**：
```json
{
  "basic_info": {
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com",
    "phone": "13800138000",
    "address": "北京市海淀区",
    "linkedin": "https://linkedin.com/in/zhangsan",
    "github": "https://github.com/zhangsan"
  },
  "educations": [
    {
      "id": 1,
      "school": "北京大学",
      "degree": "学士",
      "major": "计算机科学",
      "start_date": "2018-09",
      "end_date": "2022-06",
      "gpa": 3.8,
      "description": "主修课程：数据结构、算法分析、数据库系统等"
    }
  ],
  "experiences": [
    {
      "id": 1,
      "company": "科技有限公司",
      "position": "前端开发工程师",
      "start_date": "2022-07",
      "end_date": "2024-06",
      "is_current": 0,
      "description": "负责公司官网和产品前端开发，优化用户体验"
    }
  ],
  "skills": [
    {
      "id": 1,
      "skill_name": "JavaScript",
      "proficiency": "高级",
      "category": "编程语言"
    }
  ],
  "projects": [
    {
      "id": 1,
      "project_name": "企业官网重构",
      "project_url": "https://example.com",
      "start_date": "2023-01",
      "end_date": "2023-06",
      "description": "主导企业官网重构项目，提升页面加载速度50%",
      "technologies": "React;TypeScript;Webpack"
    }
  ]
}
```

**响应**：
```json
{
  "success": true,
  "message": "简历数据保存成功"
}
```

### 5. 获取简历数据

**功能**：根据用户ID获取完整的简历数据

**请求**：
- **方法**: GET
- **路径**: `/api/resume/get-resume/{user_id}`
- **权限**: 无需认证
- **路径参数**：
  - `user_id`: 用户ID

**响应**：
```json
{
  "success": true,
  "data": {
    "basic_info": {
      "id": 1,
      "name": "张三",
      "email": "zhangsan@example.com",
      "phone": "13800138000",
      "address": "北京市海淀区",
      "linkedin": "https://linkedin.com/in/zhangsan",
      "github": "https://github.com/zhangsan"
    },
    "educations": [],
    "experiences": [],
    "skills": [],
    "projects": []
  }
}
```

## 📊 数据模型说明

### 基本信息模型 (UserBasicInfo)
- **id**: 用户ID（必填）
- **name**: 姓名（必填）
- **email**: 电子邮箱（必填）
- **phone**: 电话号码（必填）
- **address**: 地址（可选）
- **linkedin**: LinkedIn个人资料链接（可选）
- **github**: GitHub个人资料链接（可选）

### 教育经历模型 (Education)
- **id**: 教育经历ID（必填）
- **school**: 学校名称（必填）
- **degree**: 学位（必填）
- **major**: 专业（必填）
- **start_date**: 开始日期（必填）
- **end_date**: 结束日期（必填）
- **gpa**: GPA成绩（可选）
- **description**: 描述信息（可选）

### 工作经验模型 (WorkExperience)
- **id**: 工作经验ID（必填）
- **company**: 公司名称（必填）
- **position**: 职位名称（必填）
- **start_date**: 开始日期（必填）
- **end_date**: 结束日期（必填）
- **is_current**: 是否当前工作（可选，0表示否，1表示是，默认0）
- **description**: 工作描述（可选）

### 技能模型 (Skill)
- **id**: 技能ID（必填）
- **skill_name**: 技能名称（必填）
- **proficiency**: 熟练程度（可选，如：初级、中级、高级）
- **category**: 技能类别（可选，如：编程语言、框架、工具等）

### 项目经历模型 (Project)
- **id**: 项目ID（必填）
- **project_name**: 项目名称（必填）
- **project_url**: 项目URL（可选）
- **start_date**: 开始日期（可选）
- **end_date**: 结束日期（可选）
- **description**: 项目描述（可选）
- **technologies**: 使用的技术栈（可选，多个技术用分号分隔）

## 🧪 测试

项目包含多个测试脚本，位于`test/`目录下，可以用于测试API功能和数据处理流程。

## ⚠️ 注意事项

### API使用
- 确保在环境变量文件 `.env` 中正确设置了 DeepSeek API 密钥（`DEEPSEEK_API_KEY`）
- 所有API调用需使用正确的请求格式和参数
- 当前API接口无需认证即可访问，请在生产环境中添加适当的安全机制

### 数据安全
- 系统使用自定义C语言数据库存储简历数据，请注意数据备份
- 敏感信息（如API密钥）请妥善保管在环境变量中，不要硬编码到代码中
- 建议在生产环境中添加用户认证和权限控制机制

### 系统要求
- Python 3.8+ 环境
- 支持C++11标准的编译器（用于编译数据库程序）
- 足够的磁盘空间存储简历数据和PDF文件

### 其他
- 首次运行前请确保编译C数据库：`g++ -o db db.cpp -std=c++11`
- 测试脚本需要在虚拟环境中运行，并确保所有依赖已安装
- 如有性能问题，可考虑优化数据库查询或增加缓存机制

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。在提交代码前，请确保代码符合项目的编码规范。

## 📄 许可证

[MIT License](LICENSE)
