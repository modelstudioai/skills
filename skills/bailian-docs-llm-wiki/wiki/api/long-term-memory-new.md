# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化用户状态持久化能力，用于跨会话保存和检索用户偏好、行为特征、历史交互等关键上下文。它通过语义索引与结构化字段结合的方式，支持低延迟、高精度的记忆召回。该能力需在应用配置中显式启用，并依赖模型对记忆内容的主动调用。

## 支持的模型/功能

- 当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 支持[长期记忆](../concepts/long-term-memory.md)的自动检索与注入（需开启 `enable_long_term_memory: true`）。其他模型调用将静默忽略记忆字段。
- 支持两类核心功能：**记忆片段（Fragments）** 用于存储非结构化对话上下文或事件快照；**用户画像（Profiles）** 用于维护结构化属性（如 `user_age`, `preferred_language`），支持字段级更新与条件查询。
- 所有功能均基于 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 定义的 REST 接口实现，开发者可直接调用或通过 SDK 封装使用。

## 关键参数

- `memory_id`: 必填，全局唯一标识符（建议使用 UUID v4），用于关联同一用户/会话的多条记忆。
- `ttl_seconds`: 可选，记忆存活时间（秒），默认 `2592000`（30 天），最小值 `3600`；设为 `0` 表示永不过期（不推荐生产环境使用）。
- `embedding_model`: 可选，指定用于向量化记忆片段的嵌入模型，默认 `text-embedding-v3`；若与主模型 embedding 不一致，可能导致语义召回偏差 —— 详见 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 文档说明。
- `profile_schema`: 仅 Profile 场景需提供 JSON Schema，定义允许字段、类型及校验规则；schema 变更不会自动迁移已有数据。

## 使用方式

1. **初始化**：在应用配置中设置 `long_term_memory.enabled = true`，并指定 `default_embedding_model`；
2. **写入记忆**：  
   - 片段：`POST /v1/applications/{app_id}/memories/fragments`，传入 `content` + `metadata`；  
   - 画像：`PUT /v1/applications/{app_id}/memories/profiles/{memory_id}`，传入符合 schema 的 JSON 对象；
3. **读取与注入**：在 `messages` 请求体中添加 `"long_term_memory": {"enable": true}`，平台将在推理前自动检索匹配记忆并注入 system [prompt](../guides/prompt.md)（具体策略见 [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)）。

## 限制和注意事项

- 单次请求最多注入 5 条记忆片段或 1 个完整画像，超出部分被截断；
- 记忆内容总大小（含 metadata）单条不得超过 8 KB，否则写入失败；
- > **注意**：原始文档中 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 提到“支持按时间范围批量删除”，但当前 API 实际仅支持按 `memory_id` 删除；该功能尚未上线，属文档过时，请以 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中 `/delete` 接口定义为准；
- 用户画像字段名禁止使用 `__` 开头（保留字段前缀），且不可与系统内置字段（如 `created_at`, `updated_at`）冲突；
- 所有记忆操作均受应用级配额限制，超限返回 `429 Too Many Requests`，详细配额请查阅 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md) 文档。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


