# agent-im-server-ykwang0809
⼀个⽀持⼯具调⽤的 Agent 会话服务

# 项⽬简介
本项目是一个完整的 Agent 智能会话服务，集成了即时通讯（IM）基础能力与 Agent 执行引擎，提供会话管理、消息收发、实时流式推送、LLM 工具调用等核心功能。
服务支持多轮对话、自动工具调用、流式响应输出、会话历史持久化，可作为智能助手、AI 客服、任务执行 Agent 的后端服务使用。

# 技术选型理由
1. **FastAPI**：高性能异步 Web 框架，支持 RESTful API 与 WebSocket，开发效率高，适合快速构建 AI 服务。
2. **Uvicorn**：ASGI 服务器，支持高并发、热重载，满足服务稳定运行与实时推送需求。
3. **SQLite + SQLAlchemy**：轻量级文件数据库，无需额外部署；ORM 简化数据操作，满足会话与消息持久化。
4. **WebSocket**：实现 Agent 响应流式推送、多端实时广播，符合即时通讯与流式输出场景。
5. **Python**：AI 生态完善，LLM 对接、工具函数开发便捷，快速实现 Agent Loop 逻辑。

# 架构说明
1. **API 层**
   - RESTful API：会话管理、消息发送与查询
   - WebSocket：实时连接、流式响应推送、多端广播
2. **Agent 引擎层**
   - Agent Loop：自动解析 LLM 返回，循环执行工具直到生成最终回答
   - 工具注册中心：统一管理工具元信息与执行函数
   - 预置工具：get_weather、search_knowledge、create_task
3. **数据存储层**
   - 会话表：管理会话生命周期
   - 消息表：记录用户/Agent 消息、创建时间
   - 工具调用表：记录工具名称、参数、结果、执行耗时
4. **实时推送层**
   - 流式事件：text_delta（文本片段）、tool_call（工具调用）、tool_result（工具结果）、done（结束）
   - 同一会话多端自动广播

# 启动步骤
python main.py
