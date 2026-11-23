# managed agents api

Managed Agents API 是百炼平台提供的托管式智能体服务接口，用于创建、配置和管理具备[长期记忆](../concepts/long-term-memory.md)、工具调用、多步推理能力的 AI Agent。该 API 抽象了底层运行时与基础设施细节，开发者可通过声明式方式定义 Agent 行为、环境依赖与数据访问策略。所有资源均支持 RESTful 操作，并与百炼统一认证体系集成。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类 Qwen 系列大模型；其他模型（如 `qwen2.5-*`）暂未开放接入，详见 [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md) 的子文档说明。
- **核心功能**：
  - Agent 生命周期管理（创建、更新、删除）
  - 环境隔离（Environment）与会话状态（Session）控制
  - 内置 Memory Store 实现跨会话上下文持久化
  - 文件上传/引用（Files API）、技能注册（Skills API）、密钥安全存储（Vault/Credential API）
  - Webhook 事件回调（如 `session.completed`、`agent.error`）

> **注意**：原始文档中 [概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 提到“支持自定义 LLM 接入”，但该能力尚未上线，实际仅限百炼内置 Qwen 模型；请以 [快速开始](../../raw/application-api-reference/managed-agents-api/managed-agents-quickstart.md) 中的模型列表为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 必须为 `qwen-max` / `qwen-plus` / `qwen-turbo` 之一 |
| `system_prompt` | string | 否 | 全局系统指令，长度 ≤ 4096 字符 |
| `tools` | array | 否 | 工具列表，每个元素含 `type`（如 `"file_search"`、`"web_search"`）及对应配置 |
| `memory_store_id` | string | 否 | 指向已创建的 Memory Store 资源 ID；不传则使用默认内存实例 |
| `environment_id` | string | 否 | 指定运行环境，影响网络策略与资源配额 |

## 使用方式

1. **认证**：使用 Bearer Token，通过 `Authorization: Bearer <access_token>` 传递；Token 需通过百炼 OAuth2 流程获取，详见 [认证](../../raw/application-api-reference/managed-agents-api/managed-agents-api-authentication.md) 文档。
2. **创建 Agent**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/agents \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "model_id": "qwen-plus",
           "system_prompt": "你是一个技术文档助手。",
           "tools": [{"type": "file_search", "file_ids": ["file-xxx"]}]
         }'
   ```
3. **启动会话**：调用 `/sessions` 创建会话后，通过 `POST /sessions/{session_id}/messages` 发送用户消息并流式接收响应。

## 限制和注意事项

- 单个 Agent 最多绑定 10 个 `tools`；单次会话最大上下文长度为 32k token（含 system prompt + history + input）。
- Memory Store 默认保留最近 100 条交互记录，TTL 为 7 天；如需更长保留期，需显式调用 `PATCH /memory-stores/{id}` 更新 `ttl_seconds`。
- 所有文件（via Files API）必须先上传并获得 `file_id`，再在 `tools.file_search` 中引用；直接传入本地路径或 URL 将被拒绝。
- 错误处理应基于 [错误码](../../raw/application-api-reference/managed-agents-api/managed-agents-api-errors.md) 文档中的 `error_code` 字段（如 `InvalidParameter.ModelIdNotSupported`），而非仅依赖 HTTP 状态码。

## 来源文档

- [Managed Agent API](../../raw/application-api-reference/managed-agents-api.md)


