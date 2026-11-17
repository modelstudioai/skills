# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的结构化、跨会话用户状态持久化能力，用于安全、可控地保存和检索用户偏好、行为特征、历史交互等关键上下文信息。它以「片段（Fragment）」为基本单元，支持语义与属性混合检索，并通过显式配置与 API 调用实现细粒度生命周期管理。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agent 场景**：在 `Session` 级别启用后，长期记忆自动注入模型输入（作为系统提示词的一部分），支撑多轮对话中的状态一致性；开发者可通过 `memory_id` 关联用户身份，结合 `memory_filter` 按标签/时间等条件精准召回历史片段。  
- **Agent Context 机制中**：作为 `context_sources: ["memory"]` 的核心数据源之一，与 RAG、Connector、ParseX 等上下文动态融合，统一注入模型 [prompt](../guides/prompt.md) 头部，提升 Agent 的事实准确性与个性化推理能力。  
- **Flow Agent 场景**：虽不直接暴露 LTM 原生接口，但可通过 `tool_calls` 调用封装了 `/v1/memory/get` 和 `/v1/memory/upsert` 的自定义 Skill，或在 Flow 节点中显式调用长期记忆 API 实现流程级记忆读写。  
- **纯 API 对话调用（非 Agent）**：需在请求 `messages` 中手动传入 `memory_id` 字段，平台将自动加载匹配的 fragments 并注入系统提示；若需主动控制，可独立调用 `/v1/memory/get` 或 `/v1/memory/upsert` 接口。  
- **模型侧能力差异**：仅 `qwen-max-20240919`、`qwen-plus-20240919` 及后续标注 `ltm_enabled: true` 的模型支持完整读写；`qwen-turbo` 等基础模型仅支持只读（`get_memory`），且不触发自动更新。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_id` | string | 是 | 全局唯一标识符，建议使用 UUIDv4 或业务主键哈希值（如 `sha256(user_id + salt)`） |
| `fragments` | array | 否 | 片段数组，每个 fragment 包含 `type`（字符串，如 `"preference"`）、`content`（任意 JSON 结构）、`ttl_seconds`（整数，0 表示永不过期，最小有效值为 3600） |
| `enable_auto_update` | boolean | 否 | 默认 `false`；设为 `true` 后，支持模型在输出中嵌入 `<ltm type="...">...</ltm>` 标签自动触发 `upsert_fragment`（仅限 `ltm_enabled: true` 模型） |
| `retrieval_strategy` | string | 否 | 取值为 `"semantic"`（向量相似度）、`"attribute"`（字段精确匹配）或 `"hybrid"`（两者加权），影响 `/v1/memory/get` 的召回逻辑 |
| `memory_filter` | object | 否 | 用于过滤 memory 条目的条件对象（如 `{ "type": "order_history", "created_after": "2024-01-01" }`），常用于 Agent Context 或主动查询 |

> ⚠️ 注意：单个 `memory_id` 最多存储 100 个 fragment，总内容大小 ≤ 2MB；所有写操作为最终一致性，读取可能存在秒级延迟。

## 面向开发者，简洁实用

- ✅ **快速启用**：在应用配置页开启「长期记忆」开关，并选择 `ltm_enabled: true` 模型（如 `qwen-max-20240919`）。  
- ✅ **写入记忆**：调用 `POST /v1/memory/upsert`，传入 `memory_id` 和 `fragments` 数组；避免在高频请求中频繁写入，推荐批量合并后更新。  
- ✅ **读取记忆**：在对话请求 `messages` 中添加 `"memory_id": "xxx"`，平台自动注入；或调用 `GET /v1/memory/get?memory_id=xxx&retrieval_strategy=hybrid` 主动查询。  
- ✅ **调试技巧**：使用 `curl -H "Authorization: Bearer $API_KEY" "https://dashscope.aliyuncs.com/api/v1/memory/get?memory_id=xxx"` 快速验证数据是否存在。  
- ❌ **避坑提醒**：  
  - 不要混用长期记忆（Fragment）与用户画像（Profile）——后者需走 `/v1/profiles/*` 独立接口；  
  - `qwen-turbo` 等模型无法响应 `<ltm>` 标签，`enable_auto_update: true` 对其无效；  
  - `ttl_seconds: 0` 表示永不过期，但文档中“最小值 3600”为过时描述，请以实际 API 行为为准。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)


