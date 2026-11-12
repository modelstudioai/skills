# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多轮会话与环境隔离能力的 AI Agent。该 API 以 RESTful 形式提供，支持细粒度资源控制（如 Environment、Session、Memory Store）和可扩展能力（如 Skill、Vault、Webhook）。开发者可通过它构建生产级自动化工作流，无需自行维护底层推理与状态管理逻辑。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 系统模型；自定义模型暂不支持接入 Managed Agents —— 此限制在 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的概览章节中明确说明。
- **核心功能**：
  - 多会话生命周期管理（Session + Event）
  - 持久化记忆存储（Memory Store，支持向量+结构化混合索引）
  - 安全凭证与密钥管理（Credential + Vault）
  - 可插拔技能注册与编排（Skill API）
  - 文件上传与上下文注入（Files API）
  - 部署与扩缩容控制（Deployment API）

> **注意**：原始文档中 [Environment](../../raw/application-api-reference/managed-agents-api/environment-api.md) 描述其支持“跨区域部署”，但最新 [Deployment API](../../raw/application-api-reference/managed-agents-api/deployment-api.md) 明确限定为单可用区部署，且不支持跨 region 调度。请以 Deployment API 文档为准。

## 关键参数

所有 Agent 创建请求必须包含以下字段：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | ✓ | 必须为 `qwen-max` / `qwen-plus` / `qwen-turbo` 之一；其他值将返回 `400 Bad Request` |
| `name` | string | ✓ | 长度 1–64 字符，仅支持字母、数字、下划线、短横线 |
| `environment_id` | string | ✓ | 必须引用已存在的 Environment 资源 ID（通过 [Environment API](../../raw/application-api-reference/managed-agents-api/environment-api.md) 创建） |
| `memory_store_id` | string | ✗（默认自动创建） | 若指定，需确保该 Memory Store 已存在且归属同一 Environment |

## 使用方式

1. **认证**：使用 Bearer [Token](../concepts/token.md)，通过 `Authorization: Bearer <api_key>` 传入；API Key 需具备 `managed_agents:full_access` 权限（参见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 中的认证章节）。
2. **快速启动**：参考 [Managed Agents Quickstart](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 可在 5 分钟内完成 Agent 创建、Session 初始化与首条消息发送。
3. **典型流程**：  
   `POST /v1/agents` → 获取 `agent_id`  
   `POST /v1/environments/{env_id}/sessions` → 获取 `session_id`  
   `POST /v1/sessions/{session_id}/messages` → 发起交互  

## 限制和注意事项

- 单个 Agent 最多关联 100 个 Skill；超出需先解绑。
- Session 生命周期默认 24 小时，超时后自动清理内存与事件日志（可配置，详见 [Session and Event](../../raw/application-api-reference/managed-agents-api/session-api.md)）。
- 文件上传大小上限为 100 MB，且仅支持 `text/plain`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` 等白名单 MIME 类型。
- 所有 API 均遵循百炼平台统一配额策略：默认 QPS 为 10，突发容量 50；如需提升，请提交工单申请。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


