# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化用户状态持久化能力，用于跨会话保存和检索用户偏好、行为特征、对话历史摘要等关键上下文。它通过分片（Fragment）机制实现细粒度控制，并支持基于语义与元数据的混合检索。该能力需配合兼容模型与特定 API 调用方式使用，不适用于所有基础模型。

## 支持的模型/功能

- **模型支持**：仅 `qwen-max-2025-03` 及后续标注为 `ltm-enabled` 的模型版本支持[长期记忆](../concepts/long-term-memory.md)的自动读写；`qwen-plus` 和 `qwen-turbo` 当前仅支持显式读取（需调用 `/v1/memory/retrieve`），不支持自动注入。  
- **核心功能**：包括记忆分片（Fragment）管理、用户画像（Profile）构建、语义检索（`retrieval_mode: "semantic"`）、关键词+过滤检索（`retrieval_mode: "hybrid"`），以及自动记忆更新（`auto_update: true`）。完整能力说明见 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `memory_id` | string | 否 | 用户级唯一标识，若未提供则由平台基于 `user_id` 自动生成；建议业务侧统一维护以保障一致性 |
| `fragment_type` | string | 是 | 取值为 `"profile"` 或 `"custom"`；`"profile"` 由系统自动归一化字段（如 `age`, `interests`），`"custom"` 需自行定义 schema（见 [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)） |
| `ttl_seconds` | integer | 否 | 分片存活时间，默认 `2592000`（30 天）；设为 `0` 表示永不过期（慎用） |
| `retrieval_mode` | string | 否 | 默认 `"hybrid"`；`"semantic"` 启用向量检索，对 query embedding 质量敏感；`"exact"` 仅匹配 `key` 字段 |

> **注意**：原始文档中 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 提到 `ttl_seconds` 最小值为 `3600`，但实测 `1800`（30 分钟）亦可生效；请以实际 API 响应为准，该差异已在内部 issue #LTM-427 中记录。

## 使用方式

1. **写入记忆**：调用 `POST /v1/memory/fragments`，携带 `fragment_type`、`content`（JSON 对象）及可选 `metadata`；  
2. **读取记忆**：在 `messages` 数组前插入 `{"role": "system", "content": "{memory}"}` 占位符，平台将自动注入匹配分片（需模型支持）；或显式调用 `/v1/memory/retrieve`；  
3. **更新/删除**：使用 `PUT /v1/memory/fragments/{fragment_id}` 或 `DELETE /v1/memory/fragments/{fragment_id}`；所有操作均需携带 `memory_id` 或 `user_id`。详细流程参见 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md) 中的典型用例。

## 限制和注意事项

- 单次请求最多返回 10 个分片，总内容长度上限 8192 字符（含 metadata）；  
- `profile` 类型分片字段名必须符合预定义白名单（如 `location`, `job_title`, `preferred_language`），否则写入失败；  
- 记忆检索不保证实时性：写入后最长 2 秒内可被检索到，高并发场景下可能延迟至 5 秒；  
- 不支持跨 `memory_id` 检索，即无法通过 A 用户的 `memory_id` 查询 B 用户的记忆——此设计为硬性隔离，[通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 文档中“共享记忆”描述已过时，实际不可用。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


