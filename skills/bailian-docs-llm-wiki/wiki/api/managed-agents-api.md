# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理可编程智能体（Agent）的 RESTful 接口集合，支持环境隔离、会话状态管理、技能编排、文件与记忆存储等核心能力。该 API 采用标准 HTTP 协议，需通过 Bearer Token 认证，适用于需要细粒度控制 Agent 生命周期与运行时行为的开发者场景。完整功能覆盖从开发调试到生产部署的全链路需求。

## 支持的模型与功能

Managed Agents API **不直接调用大模型**，而是提供对 Agent 运行时基础设施的编排能力；底层模型由用户在 `Agent` 配置中指定（如 `qwen-max`、`qwen-plus` 等），并受 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中定义的模型兼容性约束。支持的核心功能包括：  
- Agent 实例的创建、更新与生命周期管理（含 `status` 查询与强制终止）  
- 独立 `Environment` 隔离（支持多租户、多版本配置）  
- 基于 `Session` 的有状态交互与事件流订阅（`event_type=agent_step`, `agent_finish`）  
- `Memory Store` 提供结构化记忆持久化（键值对 + TTL）  
- `Skill` 注册与动态绑定（支持 HTTP Webhook 和内置工具）  
- `Vault` 与 `Credential` 安全管理敏感凭证  

> **注意**：原始文档中 `skills-api.md` 描述的“本地 Python 函数注册”能力已在 v2.3 版本中移除，当前仅支持 Webhook 类型 Skill；请以 [Skill API](../../raw/application-api-reference/managed-agents-api/skills-api.md) 的最新修订版为准。

## 关键参数

所有写操作（如 `POST /v1/agents`）均需在请求体中包含以下必需字段：  
- `name`: 字符串，长度 1–64，仅限字母、数字、下划线、短横线  
- `environment_id`: 关联的 Environment 唯一标识（非空）  
- `model`: 指定模型 ID（例如 `"qwen-max"`），必须在当前 Region 可用且已授权  
- `prompt_template`: Jinja2 格式字符串，至少包含 `{{input}}` 占位符  

通用查询参数：  
- `page_size` / `page_number`：分页控制（默认 `page_size=20`）  
- `status_filter`：支持 `active`, `inactive`, `error`（仅部分端点支持）  

认证凭据通过 `Authorization: Bearer <token>` 传递，Token 有效期为 24 小时，详情见 [Managed Agent API 认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)。

## 使用方式

1. **初始化环境**：先调用 `POST /v1/environments` 创建隔离环境，获取 `environment_id`  
2. **创建 Agent**：使用该 `environment_id` 调用 `POST /v1/agents`，传入模型、prompt 和技能列表  
3. **启动会话**：调用 `POST /v1/sessions` 获取 `session_id`，再向 `POST /v1/sessions/{id}/messages` 发送用户输入  
4. **监听事件（可选）**：通过 `GET /v1/sessions/{id}/events?stream=true` 建立 SSE 连接，实时接收执行步骤  

快速上手示例见 [Managed Agents 快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)，含 cURL 与 Python SDK 调用片段。

## 限制和注意事项

- 单个 Environment 最多承载 50 个活跃 Agent 实例  
- Session 生命周期默认 24 小时，超时后自动清理关联 Memory 和 Event 日志  
- 文件上传（`POST /v1/files`）单文件上限 100 MB，总存储配额由 Environment 级别控制  
- 所有 API 响应均遵循统一错误格式，常见错误码含义详见 [Managed Agent API 错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)  
- `Deployment` 和 `Webhook` 接口仅对白名单用户开放，申请路径见对应子文档说明

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


