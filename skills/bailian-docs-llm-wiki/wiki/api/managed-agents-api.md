# [managed agents](../guides/managed-agents.md) api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和运行具备[长期记忆](../concepts/memory.md)、工具调用、多步推理能力的 AI Agent。该 API 将底层模型调度、状态管理、环境隔离与安全凭证等复杂性封装为声明式资源（如 `Agent`、`Environment`、`Memory Store`），开发者可通过 RESTful 接口按需编排。所有资源均支持细粒度权限控制与异步生命周期管理。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型；不支持自定义模型或第三方模型接入。  
- **核心功能**：包括会话管理（`Session`）、持久化记忆（`Memory Store`）、文件上传与上下文注入（`File`）、技能注册与调用（`Skill`）、密钥安全存储（`Vault`/`Credential`）、环境隔离（`Environment`）及事件驱动回调（`Webhook`）。完整能力矩阵详见 [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)。

## 关键参数

- `agent_id`：必填，全局唯一标识符，由平台生成或用户指定（需符合 `^[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?$` 正则）。  
- `model`：必填，值必须为 `qwen-max`、`qwen-plus` 或 `qwen-turbo`；其他值将返回 `400 Bad Request`。  
- `memory_store_id`：可选，若指定则自动启用[长期记忆](../concepts/memory.md)，且该 Memory Store 必须与 Agent 同属一个 `Environment`。  
- `tools`：数组，每个元素为已注册的 `skill_id`；未在 `Skill` 资源中显式启用的 [skill](../guides/skill.md) 将被忽略。详细参数说明见 [Agent](../../raw/application-api-reference/managed-agents-api/agent-api.md)。

## 使用方式

1. **初始化环境**：先调用 `POST /environments` 创建隔离运行环境（推荐每业务线一个 Environment）；  
2. **注册技能与凭证**：通过 `/skills` 和 `/credentials` 接口上传工具定义与敏感凭据；  
3. **创建 Agent**：`POST /agents`，传入 `model`、`environment_id`、`memory_store_id`（可选）及 `tools` 列表；  
4. **启动会话**：`POST /sessions` 获取 `session_id`，再以 `POST /sessions/{session_id}/messages` 发送用户消息。  
快速上手流程请参考 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md)。

## 限制和注意事项

- 单个 Environment 下最多创建 100 个 Agent，单个 Agent 最多关联 50 个 Skill；  
- Memory Store 默认 TTL 为 7 天，不可修改；若需更长保留期，须使用外部向量库并自行集成；  
- > **注意**：[API 总览与认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 中提及的 `X-Bailian-Region` 请求头已废弃，现统一使用 `X-Bailian-Endpoint` 指定区域（如 `https://dashscope.aliyuncs.com`），旧文档未同步更新；  
- 所有文件上传（`/files`）大小上限为 50 MB，且仅支持 `text/plain`、`application/json`、`text/csv`、`application/pdf` 四种 MIME 类型；  
- Webhook 事件投递失败后重试 3 次（间隔 1s/2s/4s），超时时间为 10 秒；若连续 5 次失败，该 Webhook 将被自动禁用。

## 来源文档

- [Managed Agents](../../raw/application-api-reference/managed-agents-api.md)


