# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化用户状态持久化能力，用于跨会话保存和检索用户偏好、行为特征、历史交互等关键上下文。它通过分片（Fragment）机制实现细粒度控制，并支持基于语义与元数据的混合检索。该能力需配合支持 LTM 的模型及 SDK 使用，当前处于稳定可用阶段。

## 支持的模型/功能

- **模型支持**：仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo`（v202409 及之后版本）原生支持 LTM 上下文注入；其他模型需显式启用 `enable_long_term_memory: true` 并依赖服务端自动降级策略。  
- **核心功能**：包括记忆片段（Fragment）的增删查改、用户画像（Profile）自动聚合、跨会话上下文自动注入（默认开启）、基于向量+属性的混合检索。完整能力列表见 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)。  
- **SDK 支持**：Python SDK v1.12.0+、Web SDK v2.8.0+ 提供 `memory_fragment`、`user_profile` 等封装接口；旧版 SDK 需手动构造请求体，详见 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `fragment_id` | string | 否 | 用户自定义唯一标识，若为空则由服务端生成；建议使用业务主键（如 `user:123:settings`）便于管理 |
| `ttl_seconds` | integer | 否 | 过期时间（秒），默认 `2592000`（30 天），最小值 `3600`，最大值 `31536000`（1 年） |
| `metadata` | object | 否 | 键值对，支持字符串/数字/布尔值，用于过滤检索；单个 fragment 最多 16 个 key，总大小 ≤ 4KB |
| `enable_auto_injection` | boolean | 否 | 控制是否在本次请求中自动注入匹配的 fragment，默认 `true`；设为 `false` 时需手动调用 `/v1/memory/retrieve` |

> **注意**：`ttl_seconds` 在 [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 中标注为“可为 0 表示永不过期”，但实际 API 会拒绝 `0` 值并返回 `400`；此为文档过时，以 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 中的约束为准。

## 使用方式

1. **写入记忆片段**：调用 `POST /v1/memory/fragments`，传入 `content`（文本或 JSON 字符串）、`fragment_id`、`metadata` 等字段；  
2. **触发自动注入**：在 `/v1/chat/completions` 请求中设置 `enable_long_term_memory: true`，服务端将根据 `user_id` 和当前 `session_id` 自动检索并注入相关 fragment；  
3. **手动检索**：调用 `POST /v1/memory/retrieve` 指定 `filter`（如 `{"category": "preference", "version": 2}`）和 `top_k`；结果按相关性排序，最多返回 20 条。详细流程参见 [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)。

## 限制和注意事项

- 单个用户（`user_id`）最多存储 **5000 个 fragment**，超出后写入失败（`429 Too Many Fragments`）；  
- 单个 fragment `content` 最大长度为 **65536 字符**，超长内容需预处理截断或分片；  
- 用户画像（Profile）为只读聚合视图，由系统基于 fragment 自动更新，不可直接写入；其字段定义与更新逻辑详见 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)；  
- 启用 LTM 后，请求延迟平均增加 80–200ms（取决于 fragment 数量与检索复杂度），高并发场景建议预热常用 `user_id` 的缓存。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


