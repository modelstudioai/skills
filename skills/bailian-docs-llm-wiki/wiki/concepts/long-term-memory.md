# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的结构化用户状态持久化能力，用于跨会话、跨请求地保存与检索用户偏好、行为特征、对话历史摘要等关键上下文信息。它以分片（Fragment）为基本单位，支持语义检索与元数据过滤的混合查询，并通过 `memory_id` 实现严格的用户级数据隔离。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 直接调用**：通过 `/v1/memory/fragments` 系列接口显式写入、读取、更新或删除记忆分片；适用于需要精细控制生命周期或与外部系统（如 CRM）同步的场景。  
- **Agent 开发（Managed / Flow）**：在 Agent 配置中启用 `enable_memory: true` 后，平台自动将匹配的长期记忆片段注入 prompt 上下文（需模型支持）；也可在 `context.memory_ids` 中指定记忆库 ID，由 Agent 运行时按需加载。  
- **Agent 上下文（[agent context](../guides/agent-context.md)）机制**：在 API 请求的 `context` 字段中传入 `memory_ids` 数组，即可将对应用户的长期记忆片段（按时间倒序）注入当前推理上下文，与其他 context 类型（如知识库、Connector）协同工作。  
- **Managed Agents API**：通过 `session_id` 关联的 Memory Store 实现会话延续，但注意：该 Memory Store 是短期会话缓存（默认 TTL 7 天），**不等同于 LTM**；如需长期、跨会话复用，必须使用独立的 LTM 接口管理 `memory_id` 对应的记忆。

> ⚠️ 关键区分：`session_id` 绑定的是临时会话状态（短期记忆），而 `memory_id` 标识的是用户级长期记忆实体——二者独立存在，不可混用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `memory_id` | string | 否 | 用户级唯一标识；未提供时平台基于 `user_id` 自动生成，但**强烈建议业务侧统一维护并复用**，确保记忆一致性 |
| `fragment_type` | string | 是 | `"profile"`（系统预定义字段，如 `location`, `preferred_language`）或 `"custom"`（需自行定义 schema） |
| `ttl_seconds` | integer | 否 | 分片存活时间，默认 `2592000`（30 天）；最小有效值为 `1800`（30 分钟）；设为 `0` 表示永不过期（慎用） |
| `retrieval_mode` | string | 否 | 默认 `"hybrid"`（关键词 + 元数据过滤 + 语义向量）；可选 `"semantic"`（纯向量检索，对 query 质量敏感）或 `"exact"`（仅匹配 `key` 字段） |

- **模型兼容性**：  
  - ✅ 自动读写（写入后自动注入 prompt）：仅 `qwen-max-2025-03` 及后续标注 `ltm-enabled` 的模型  
  - ⚠️ 显式读取（需调用 `/v1/memory/retrieve`）：`qwen-plus`、`qwen-turbo` 支持，但**不支持自动注入**  
  - ❌ 不支持：所有非 Qwen 系列模型、Qwen-VL 多模态模型（不支持 memory 类型 context）

- **限制**：  
  - 单次检索最多返回 10 个分片，总内容长度 ≤ 8192 字符（含 metadata）  
  - 写入后检索延迟：通常 ≤ 2 秒，高并发下最长 ≤ 5 秒  
  - 严格隔离：无法通过一个 `memory_id` 访问另一个用户的记忆（无共享记忆）  

## 面向开发者：快速上手建议

- **首次集成**：优先使用 `fragment_type: "profile"` 快速沉淀用户基础属性（如 `age`, `interests`, `location`），避免自定义 schema 复杂度。  
- **调试技巧**：调用 `/v1/memory/retrieve` 时带上 `debug: true` 查询参数，可返回检索过程的向量相似度、匹配字段等诊断信息。  
- **生产注意**：  
  - 永不过期（`ttl_seconds: 0`）的记忆需配合定期清理策略，否则可能触发配额告警；  
  - 所有写入操作必须携带 `memory_id` 或 `user_id`，否则将被拒绝；  
  - `profile` 类型字段名必须在白名单内，否则返回 `400 Bad Request` —— 建议先查 [Profile 字段规范](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent development](../guides/agent-development.md)
- [agent context](../guides/agent-context.md)
- [managed agents api](../api/managed-agents-api.md)


