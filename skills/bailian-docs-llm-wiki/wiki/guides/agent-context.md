# agent context

`agent context` 是百炼平台中用于为 Agent 提供运行时上下文信息的核心机制，它决定了 Agent 在执行任务时可访问的外部知识、历史记忆、数据源连接及结构化解析能力。该机制通过声明式配置与运行时注入结合，支持开发者灵活控制上下文范围与粒度。其设计目标是解耦业务逻辑与上下文供给，提升 Agent 的可复用性与可控性。

## 支持的模型/功能

`agent context` 当前**不依赖特定大模型**，而是作为通用上下文抽象层，适用于所有支持 `tool calling` 和 `context injection` 协议的百炼内置模型（如 Qwen-Max、Qwen-Plus、Qwen-Turbo）及已注册的自定义模型。它主要支撑四类上下文功能模块：
- **Knowledge（原RAG）**：对接知识库实现语义检索增强，详见 [Agent 上下文 (raw/application-user-guide/agent-context.md)](../../raw/application-user-guide/agent-context.md)；
- **Memory**：提供短期对话记忆与[长期记忆](../concepts/long-term-memory.md)库管理，其架构概览见 [Agent 上下文 (raw/application-user-guide/agent-context.md)](../../raw/application-user-guide/agent-context.md)；
- **Connector**：连接外部系统（如数据库、API、SaaS 应用），统一抽象认证与数据拉取逻辑；
- **ParseX**：对非结构化输入（PDF、Excel、网页等）进行预解析与字段提取，其快速入门指引位于 [Agent 上下文 (raw/application-user-guide/agent-context.md)](../../raw/application-user-guide/agent-context.md)。

> **注意**：文档中提及的 “Knowledge（原RAG）” 名称已正式统一为 `Knowledge`，旧版 RAG 相关 API 与控制台入口已下线，新项目请勿再引用 `rag_*` 前缀参数。

## 关键参数

在 Agent 配置 YAML 或 SDK 调用中，`context` 字段接受以下顶层键：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge` | object \| array | 否 | 指定知识库 ID 列表或带 `top_k`/`threshold` 的对象；单次最多绑定 5 个知识库 |
| `memory` | object | 否 | 含 `type: "short"` / `"long"`，`ttl_seconds`（仅 long），`max_history`（仅 short） |
| `connectors` | array | 否 | Connector 实例 ID 列表，每个 ID 需已在平台预注册并授权 |
| `parsex` | object | 否 | 含 `input_type: "file"` / `"url"` / `"text"` 及 `schema` 定义（JSON Schema 格式） |

所有参数均支持运行时覆盖（via `context_override`），但 `connectors` 的权限校验始终以配置时绑定为准。

## 使用方式

1. **控制台配置**：在 Agent 编辑页 → 「上下文」标签页勾选启用模块，填写对应参数；
2. **YAML 配置**（`agent.yaml`）：
   ```yaml
   context:
     knowledge:
       - id: "kb-xxx"
         top_k: 3
     memory:
       type: "short"
       max_history: 10
   ```
3. **SDK 调用时动态注入**（Python 示例）：
   ```python
   client.run(
       agent_id="agt-xxx",
       input={"query": "最新财报数据？"},
       context_override={
           "knowledge": [{"id": "kb-yyy", "top_k": 5}],
           "connectors": ["conn-zzz"]
       }
   )
   ```

## 限制和注意事项

- 单次请求总上下文 token 开销（含 knowledge 检索结果、memory 片段、ParseX 输出）不得超过所选模型的 `max_context_length` 的 80%，超限将触发截断并返回警告日志；
- `memory.type: "long"` 依赖用户级唯一标识（`user_id`），若调用未传 `user_id`，该模块自动降级为 `short`；
- Knowledge 检索结果默认按相关性排序，但**不支持跨知识库 merge 排序**，需自行聚合处理；
- Connector 调用受平台配额与目标系统速率限制双重约束，失败时不重试，需在 Agent 逻辑中显式处理 `connector_error` 工具调用结果。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


