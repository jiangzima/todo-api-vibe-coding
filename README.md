Todo API（Vibe Coding 演示项目）
这是一个基于 FastAPI 和 SQLite 的可生产级待办事项 API，通过 Vibe coding 工作流（Ollama + CodeLlama）开发 —— 在 AI 生成代码的基础上进行优化，修复了潜在问题并增加了企业级特性。

📋 核心功能
完整的待办事项增删改查（CRUD）操作
自动 SQLite 数据表初始化（无需手动配置）
Pydantic 请求参数校验（防止非法输入）
HTTP 异常处理（如对不存在的待办事项返回 404）
自动生成交互式 API 文档（/docs）
数据库连接管理（避免连接泄漏）

🚀 快速开始（100% 可运行）
1. 安装依赖
pip install fastapi uvicorn
2. 启动 API 服务
uvicorn todo_api:app --reload
3. 测试 API
访问自动生成的文档：http://127.0.0.1:8000/docs
通过交互式 UI 测试所有接口（POST/GET/PUT/DELETE）

📸 API 测试截图
![Todo API Docs Test](https://github.com/jiangzima/todo-api-vibe-coding/raw/main/todo_api_test.png)

✨ Vibe Coding 开发流程
本项目完整展示了岗位所需的 Vibe coding 能力：
AI 代码生成：使用 Ollama（CodeLlama 模型）生成初始 FastAPI 代码
人工优化：修复 AI 生成代码中的关键问题：
添加自动数据库表创建（解决 “表不存在” 错误）
实现 Pydantic 数据校验（替代原生字典）
增加对不存在待办事项的异常处理
优化数据库连接管理
MVP 交付：短时间内完成可运行的最小可行产品

🛠️ 技术栈
后端：FastAPI（Python）
数据库：SQLite（基于文件，无需额外安装）
AI 编码工具：Ollama + CodeLlama（本地部署）
开发模式：Vibe coding

📞 联系方式
GitHub：[jiangzima](https://github.com/jiangzima)
