# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆存储与检索能力，用于在多轮对话或跨会话场景中持久化关键信息。它支持事实性片段（Fragments）和用户画像（Profiles）两类记忆类型，通过向量化索引实现语义检索。该功能需配合支持记忆能力的模型使用，并在 API 请求中显式启用。

## 支持的模型/功能

- 当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 的 **v20240915 及之后版本**支持[长期记忆](../concepts/long-term-memory.md)读写（含自动注入与显式检索）。  
- 功能分为两类：**事实记忆**（存储非人格化、可验证的事实，如“用户公司成立于2020年”）和**用户画像**（存储人格化、聚合性属性，如“用户偏好技术类内容”）。二者底层共享同一向量索引，但元数据约束与生命周期策略不同。  
- 详细能力边界请参阅 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 文档中的分类说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_type` | string | 是 | 取值为 `"fragment"` 或 `"profile"`，决定记忆类型 |
| `memory_id` | string | 否 | 显式指定记忆 ID；若不提供，服务端自动生成 UUIDv4 |
| `ttl_seconds` | integer | 否 | 过期时间（秒），默认 `31536000`（1 年）；设为 `0` 表示永不过期（仅限 `profile`） |
| `enable_retrieval` | boolean | 否 | 默认 `true`；设为 `false` 可禁用本次请求中对 LTM 的自动检索 |

> **注意**：`ttl_seconds=0` 在 `fragment` 类型下将被强制忽略并重置为默认值，此行为与 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 中早期文档描述存在不一致，以当前 API 实际响应为准。

## 使用方式

1. **写入记忆**：调用 `POST /v1/applications/{app_id}/memories`，携带 `memory_type` 和内容字段（`content` 或 `profile_fields`）；  
2. **检索记忆**：在 `ChatCompletion` 请求的 `messages` 中添加 `role: "system"` 消息，内容为 `{"use_memory": true}`，或显式设置 `enable_retrieval: true`；  
3. **批量操作**：支持通过 `/memories/batch` 接口一次写入/删除最多 50 条记忆。  
完整接口定义与示例见 [长期记忆 API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 限制和注意事项

- 单条记忆 `content` 字段最大长度为 8192 字符；`profile_fields` 总键值对数不超过 100；  
- 每个应用默认配额为 **10 万条记忆**（按 `memory_id` 去重计数），超出后写入返回 `429 Too Many Requests`；  
- 记忆检索结果默认最多返回 5 条，且仅在 `temperature > 0` 时参与上下文构建（确定性模式下不注入）；  
- 用户画像更新具有幂等性，相同 `user_id` 的多次 `profile` 写入会自动合并字段；而 `fragment` 写入始终新建条目。  
更多设计原理与最佳实践，请参考 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 和 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 文档。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


