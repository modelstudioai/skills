# managed agents api

Managed Agents API 是百炼平台提供的用于构建、部署和管理可编程智能体（Agent）的 RESTful 接口集合，支持环境隔离、会话状态管理、技能编排、文件与记忆存储等核心能力。该 API 采用标准 HTTP 协议，需通过 Bearer [Token](../concepts/token.md) 认证，适用于需要细粒度控制 Agent 生命周期与运行时行为的开发者场景。完整功能覆盖从开发调试到生产部署的全链路需求。

## 支持的模型与功能

Managed Agents API **不直接调用大模型**，而是提供对 Agent 运行时基础设施的编排能力；底层模型由用户在 `Agent` 配置中指定（如 `qwen-max`、`qwen-plus` 等），并受 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中定义的模型兼容性约束。支持的核心功能包括：  
- Agent 实例的创建、更新与生命周期管理（含 `status` 查询与强制终止）  
- 独立 `Environment` 资源，用于隔离依赖、配置与权限上下文  
- 基于 `Session` 的有状态交互，支持事件流（`Event`）订阅与回溯  
- `File` 和 `Memory Store` 双通道持久化，分别面向临时文件上传与结构化记忆检索  
- `Skill` 注册与组合、`Vault` 密钥托管、`Credential` 安全注入，以及 `Webhook` 异步回调通知  

> **注意**：文档中提及的 `Deployment` 资源当前仅用于灰度发布控制，其 `scale` 字段在 [Deployment API](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 中声明为只读，与早期快速开始指南中的示例参数存在不一致，请以实际 API 响应为准。

## 关键参数

所有写操作（`POST`/`PUT`/`PATCH`）均需在请求头中携带：  
- `Authorization: Bearer <access_token>`（参见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md)）  
- `Content-Type: application/json`  

关键路径参数与请求体字段示例：  
- `agent_id`：全局唯一标识，由平台生成，不可自定义  
- `environment_id`：必须提前创建，`Agent` 创建时显式绑定  
- `session_id`：首次调用 `/v1/agents/{agent_id}/sessions` 时由服务返回，后续交互必需  
- `event_types`（在 `Session` 创建或 `Webhook` 配置中）：支持 `["agent_started", "tool_called", "agent_finished"]`，详见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)  

## 使用方式

1. **初始化环境**：先调用 `POST /v1/environments` 创建 `Environment`，获取 `environment_id`  
2. **部署 Agent**：`POST /v1/agents`，传入 `environment_id`、模型名称、技能列表及初始配置  
3. **启动会话**：`POST /v1/agents/{agent_id}/sessions`，可选携带 `input`（初始用户消息）与 `memory_id`  
4. **交互与监听**：  
   - 同步：`POST /v1/sessions/{session_id}/messages` 发送消息  
   - 异步：配置 `Webhook` 接收 `Event` 流（推荐用于长任务）  

完整流程示例见 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- 单个 `Environment` 最多关联 50 个 `Agent`；单个 `Agent` 最多支持 1000 个并发 `Session`  
- `File` 上传大小上限为 100 MB，`Memory Store` 单条记录最大 1 MB，总容量受项目配额限制  
- 所有 API 均遵循 60 秒超时，`Session` 消息处理若超过 30 秒未响应将自动标记为 `timeout` 状态  
- 错误响应统一返回标准结构，含 `code`（如 `INVALID_ARGUMENT`）、`message` 与 `request_id`，详细码表见 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md)  
- `Credential` 和 `Vault` 内容**不可被 Agent 运行时直接读取明文**，仅支持通过 Skill 插件安全注入至工具调用上下文

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


