# managed agents

managed agents 是百炼平台提供的托管式智能体运行与编排服务，开发者无需自行部署和运维 Agent 服务，即可通过声明式配置快速创建、调度和监控具备多步推理、工具调用、状态管理能力的智能体。其核心设计面向生产级任务编排，支持会话上下文持久化、异步任务委派及事件驱动集成。所有功能均基于百炼统一模型网关与权限体系，与平台其他能力（如 RAG、Function Calling）深度协同。

## 支持的模型与功能

- **模型支持**：当前仅支持百炼平台已接入的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列大模型；不支持自定义模型或第三方模型接入。  
- **核心功能**：  
  - 多轮会话上下文自动维护（含长周期记忆与 TTL 清理）  
  - 内置工具调用（如 HTTP 请求、数据库查询、代码执行沙箱）  
  - 异步任务委派与状态轮询（通过 `/session/{id}/status` 接口）  
  - Webhook 事件订阅（支持 `agent_started`、`tool_called`、`session_completed` 等 7 类事件）  
  - 环境变量隔离与 Secret 注入（用于敏感凭证管理）  

> **注意**：原始文档中“构建 Agent”章节提及支持自定义 Python 函数作为工具，但 [构建 Agent](../../raw/application-user-guide/managed-agents.md) 实际仅允许通过 YAML 声明标准工具集（如 `http_request`, `sql_query`），自定义函数需通过 Function Calling API 单独调用，二者不可混用——此为文档过时表述。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 模型 ID，必须为平台预置 Qwen 系列模型之一，例如 `"qwen-plus"` |
| `tools` | array | 否 | 工具列表，每个元素为 `{ "type": "http_request", "name": "fetch_data" }` 格式；未声明则禁用工具调用 |
| `session_timeout_ms` | integer | 否 | 会话空闲超时毫秒数，默认 `300000`（5 分钟）；超过后上下文自动释放 |
| `max_steps` | integer | 否 | 单次会话最大推理步数，默认 `15`，上限 `50`；超出将终止并返回 `error: step_limit_exceeded` |
| `webhook_url` | string | 否 | 事件回调地址，需支持 HTTPS 且响应 `2xx`；[Webhook 事件订阅](../../raw/application-user-guide/managed-agents.md) 中明确要求签名验证头 `X-Bailian-Signature` |

## 使用方式

1. **声明式创建**：通过 YAML 配置文件定义 Agent 行为（参考 [配置 Agent 环境](../../raw/application-user-guide/managed-agents.md) 中的 `environment.yaml` 示例）  
2. **启动会话**：调用 `POST /v1/agents/{agent_id}/sessions`，传入初始 `input` 和可选 `context_id`  
3. **获取结果**：轮询 `GET /v1/sessions/{session_id}` 或监听 Webhook 事件；同步模式下最多等待 `60s`，超时需切为异步流式消费  
4. **CLI 辅助**：`bailian agent create --config agent.yaml` 可完成注册与部署，详见 [使用 CLI](../../raw/application-user-guide/managed-agents.md)

## 限制和注意事项

- **并发限制**：单个 Agent 实例默认最大并发会话数为 10，可通过工单申请提升至 100  
- **上下文长度**：单次请求总 token（含 history + input + tools）不得超过模型 context window 的 80%，否则返回 `400 Bad Request`  
- **工具调用安全**：HTTP 工具默认禁止访问内网地址（`10.0.0.0/8`, `192.168.0.0/16` 等），该策略不可绕过  
- **计费粒度**：按实际消耗的模型 token + 工具调用次数计费，空闲会话不产生费用；详细规则见 [计费](../../raw/application-user-guide/managed-agents.md) 文档  
- **调试建议**：启用 `debug: true` 参数可返回完整 reasoning trace（含每步 tool input/output），但该字段仅在 `200 OK` 响应中返回，错误路径下不包含

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


