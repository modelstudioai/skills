# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 将底层模型调度、状态管理、环境隔离与安全凭证等复杂性封装为声明式资源（如 `Agent`、`Environment`、`Memory Store`），开发者可通过 RESTful 接口或 SDK 快速构建生产级智能体应用。详细设计原则与架构约束见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型；其他模型（如 `qwen2.5`）暂未开放接入，相关说明以 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md) 文档为准。
- **核心功能**：
  - 基于 `Environment` 的沙箱化执行上下文（含预置工具链与网络策略）
  - 持久化 `Memory Store`（支持向量+结构化混合存储）
  - 多会话生命周期管理（通过 `Session` 资源隔离用户对话流）
  - 可插拔 `Skill` 注册与 `Vault` 加密凭证管理
  - 全链路事件通知（通过 `Webhook` 接收 `session_started`、`tool_executed` 等事件）

> **注意**：原始文档中 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 提到支持自定义 Docker 镜像，但该能力已于 v2.3 版本下线；实际仅允许使用平台预置的 `env-qwen-base` 及其衍生环境，最新兼容列表请以 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 中的 `supported_environments` 字段为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 必须为平台白名单模型 ID，如 `"qwen-max"`；非法值将返回 `400 Bad Request` |
| `environment_id` | string | 否 | 若不指定，自动绑定默认环境 `env-qwen-base`；显式传入时需确保与 `model_id` 兼容 |
| `memory_store_id` | string | 否 | 指定已有 Memory Store ID；若为空，系统自动创建临时 store（72 小时 TTL） |
| `skills` | array[string] | 否 | 技能 ID 列表，必须已通过 [Skill](../../raw/application-api-reference/managed-agents-api/skills-api.md) 接口注册并启用 |

## 使用方式

1. **初始化 Agent**：`POST /v1/agents`，传入基础配置（`model_id`、`name`、`description`）  
2. **启动 Session**：`POST /v1/agents/{agent_id}/sessions`，可携带初始 `input` 和 `user_id`  
3. **流式交互**：对 `/v1/sessions/{session_id}/messages` 发起 `POST`，支持 `stream=true` 获取 SSE 流  
4. **状态查询**：通过 `GET /v1/sessions/{session_id}` 获取当前 `status`（`running`/`completed`/`failed`）及最后 `event_log`  

完整端点与请求示例详见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)。

## 限制和注意事项

- 单次 `message` 请求最大输入长度为 32768 token（含 system prompt + history + user input）  
- 每个 `Agent` 实例默认最多并发 5 个活跃 `Session`；如需提升，请提交配额申请工单  
- `File` 上传仅支持 `multipart/form-data`，且单文件 ≤ 100 MB；元数据（如 `file_type`）必须显式声明，否则解析失败 —— 具体规则参见 [File](../../raw/application-api-reference/managed-agents-api/files-api.md)  
- 所有 `Credential` 必须通过 [Credential](../../raw/application-api-reference/managed-agents-api/credential-api.md) 接口注入，禁止在 `Skill` 或 `Agent` 配置中硬编码密钥  
- `Deployment` 接口（`/v1/deployments`）目前仅支持 `status=active` 查询，创建与更新功能暂未开放（计划 Q3 上线）

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


