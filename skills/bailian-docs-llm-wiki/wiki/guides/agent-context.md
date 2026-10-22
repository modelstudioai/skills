# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息输入的关键机制，它决定了 Agent 在执行任务过程中可访问的知识、历史记忆、数据源及解析能力。通过合理配置上下文，开发者可显著提升 Agent 的准确性、连贯性与领域适应性。其设计遵循模块化原则，各组件（如 RAG、Memory、Connector）可独立启用或组合使用。

## 支持的模型/功能

agent context 本身不依赖特定大模型，但需与支持 `tool calling` 和 `context injection` 能力的模型协同工作，当前已验证兼容的模型包括：Qwen-Max、Qwen-Plus、Qwen-Turbo 及部分第三方接入模型（需开启 `enable_context` 标志）。核心功能模块包括：
- **RAG**：支持从知识库动态检索并注入上下文片段，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)；
- **Memory**：提供短期对话记忆（session-level）与长期用户画像记忆（user-level），其能力边界在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 中明确定义；
- **Connector**：用于对接外部系统（如 CRM、数据库），实现运行时数据拉取，参考 [Connector](../../raw/application-user-guide/agent-context/overview.md)；
- **ParseX**：专用于非结构化文档（PDF/Word/Excel）的语义解析与上下文化切片，用法见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)。

> **注意**：部分旧版 SDK 文档提及 `context_window_size` 参数对所有模型统一生效，但实测发现 Qwen-Turbo 在启用 RAG 后实际上下文窗口会因嵌入截断而缩小约 15%，该差异已在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的 v2.3.1 补丁说明中修正。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `knowledge_base_ids` | string[] | 否 | 指定启用的 RAG 知识库 ID 列表；为空则禁用 RAG |
| `memory_type` | `"session"` \| `"user"` \| `"none"` | 否 | 默认 `"session"`；设为 `"user"` 时需传入 `user_id` |
| `connector_config` | object | 否 | 包含 `connector_id`、`params`（如认证 token）、`timeout_ms`；结构见 [Connector](../../raw/application-user-guide/agent-context/overview.md) |
| `parsex_enabled` | boolean | 否 | 默认 `false`；启用后自动解析 `input_files` 中的附件并注入上下文 |

## 使用方式

1. 在创建 Agent 实例时，通过 `context` 字段传入配置对象（非字符串）：
   ```json
   {
     "context": {
       "knowledge_base_ids": ["kb-xxx"],
       "memory_type": "session",
       "connector_config": {
         "connector_id": "conn-crm-001",
         "params": {"auth_token": "${{ secrets.CRM_TOKEN }}"},
         "timeout_ms": 5000
       }
     }
   }
   ```
2. 若需动态覆盖上下文（如单次请求指定不同知识库），可在调用 `/v1/agents/{id}/chat` 时于 `messages` 外层传入 `context_override` 对象；
3. ParseX 解析结果默认以 `<doc>` 标签包裹注入，无需额外模板指令——该行为在 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 中明确约定。

## 限制和注意事项

- 单次请求中，RAG 检索 + Memory + Connector 返回内容总长度不得超过模型最大上下文长度的 80%（预留 20% 给 prompt 和 output），否则触发静默截断；
- `memory_type: "user"` 要求 `user_id` 为非空字符串且符合 `/^[a-zA-Z0-9_-]{4,64}$/` 正则，否则降级为 `"session"`；
- Connector 调用失败时默认返回空上下文（不中断 Agent 执行），如需失败即终止，须在 `connector_config` 中显式设置 `"fail_fast": true` —— 此字段未在 [Connector](../../raw/application-user-guide/agent-context/overview.md) 的基础示例中体现，但已在 v2.4.0 API 文档中补充说明。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


