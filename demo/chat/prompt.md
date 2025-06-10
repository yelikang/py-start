# 实现一个chat对话机器人
## 前端
### 框架
vite + vue3 + vue-router + ts
### 功能
1. 查询历史记录
2. 进行询问


## 后端
### 框架
python + mysql + ollama本地模型
### 功能
1. 使用本地模型进行用户query对话
2. 每次的query和回复保存到mysql数据库
3. 模型能够查询历史对话，增强上下文能力
4. 可以扩展RAG、知识库、对接MCP等功能