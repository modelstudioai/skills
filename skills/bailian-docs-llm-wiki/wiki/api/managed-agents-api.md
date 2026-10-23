# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理可编程智能体（Agent）的 RESTful 接口集合，支持环境隔离、会话状态管理、技能编排、文件与记忆存储等核心能力。该 API 采用标准 HTTP 协议，需通过 Bearer Token 认证，适用于需要细粒度控制 Agent 生命周期与运行时行为的开发者场景。完整功能覆盖从开发调试到生产部署的全链路需求。

## 支持的模型与功能

Managed Agents API **不直接调用大模型**，而是提供对 Agent 运行时基础设施的编排能力；底层模型由用户在 `Agent` 配置中指定（如 `qwen-max`、`qwen-plus` 等），并受 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中定义的模型兼容性约束。支持的核心功能包括：  
- Agent 实例的创建、更新与生命周期管理（含 `deploy` / `undeploy`）  
- 独立的 Environment 隔离（含依赖注入与资源配额）  
- Session 级别状态管理与事件流订阅（`session_id` 绑定）  
- 文件上传/引用（支持临时上传与 Vault 持久化）、Memory Store 键值存储、Skill 注册与调用  
- Webhook 回调配置，用于异步事件通知（如 `session.completed`）

> **注意**：原始文档中 `skills-api.md` 描述的 Skill 注册方式与 [Managed Agent API 快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 示例中使用的 `POST /v1/skills` 路径不一致（后者为 `/v1/agents/{agent_id}/skills`），请以 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的路径为准，前者已过时。

## 关键参数

所有请求需携带以下通用头信息：  
- `Authorization: Bearer <access_token>`（参见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)）  
- `Content-Type: application/json`（除文件上传外）  

关键路径参数与请求体字段示例：  
- `agent_id`：Agent 唯一标识，由 `POST /v1/agents` 返回，用于后续所有子资源操作  
- `session_id`：会话标识，必须在 `POST /v1/sessions` 创建后传入 `POST /v1/sessions/{session_id}/messages`  
- `environment_id`：Environment 创建后返回，用于绑定 Agent 运行上下文  
- `file_id` 或 `vault_id`：文件或密钥引用需显式声明来源，不可混用  

## 使用方式

1. **初始化环境**：先调用 `POST /v1/environments` 创建隔离环境  
2. **定义 Agent**：`POST /v1/agents` 提交配置（含 model、skills、memory_store_enabled 等）  
3. **部署 Agent**：`POST /v1/agents/{agent_id}/deploy` 启动实例（需指定 `environment_id`）  
4. **交互**：`POST /v1/sessions` 创建会话 → `POST /v1/sessions/{session_id}/messages` 发送用户输入  
5. **扩展能力**：按需调用 `/files`、`/memory-store`、`/webhooks` 等子接口集成外部系统  

详细步骤与 cURL 示例见 [Managed Agent API 快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- 单个 Agent 最多关联 100 个 Skill，单次会话消息历史上限为 100 条（超出将触发截断）  
- Memory Store 单 key 值最大 1MB，总容量受 Environment 配额限制  
- 文件上传仅支持 `multipart/form-data`，且临时文件 24 小时后自动清理；持久化需显式调用 `/vaults/{vault_id}/files`  
- 所有 API 均遵循 [错误码规范](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)，常见错误如 `400 BAD_REQUEST`（参数校验失败）、`404 NOT_FOUND`（`agent_id` 或 `session_id` 无效）  
- Webhook 事件投递最多重试 3 次，超时时间为 10 秒；建议接收端实现幂等处理

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


