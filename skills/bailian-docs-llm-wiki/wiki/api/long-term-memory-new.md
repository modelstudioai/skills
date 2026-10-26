# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆存储与检索能力，支持在多轮对话中持久化保存和动态召回用户事实、偏好及行为画像。该能力通过 API 显式控制记忆的写入、查询与更新，不依赖模型内部隐式状态。其设计目标是提升应用在复杂业务场景下的上下文一致性与个性化能力，详见 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)。

## 支持的模型/功能

- **模型兼容性**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型原生支持 LTM 的自动记忆注入（即在 `messages` 中启用 `enable_long_term_memory: true` 后，系统自动关联相关记忆片段）。其他模型需手动构造记忆上下文。
- **核心功能模块**：
  - **事实记忆（Fragments）**：以键值对形式存储可验证的客观信息（如“用户手机号=138****1234”），支持模糊匹配与语义检索；参考 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)。
  - **用户画像（Profiles）**：结构化存储跨会话的用户属性（如 `age_group: "25-34"`, `preferred_language: "zh"`），支持字段级更新与条件查询；参考 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_id` | string | 否 | 记忆唯一标识，由系统生成或用户指定（仅限 Profiles）；若未提供，系统自动生成 |
| `fragment_key` | string | 是（Fragments） | 用于检索的事实记忆键，建议使用语义明确的命名（如 `"user_email"`） |
| `profile_id` | string | 是（Profiles） | 用户全局唯一 ID（如 OpenID 或 UUID），用于绑定画像 |
| `ttl_seconds` | integer | 否 | 过期时间（秒），默认 `31536000`（1 年），设为 `0` 表示永不过期 |
| `enable_long_term_memory` | boolean | 否 | 在 `/v1/chat/completions` 请求中启用自动记忆注入，默认 `false` |

> **注意**：`ttl_seconds` 在 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 文档中被描述为“最小单位为小时”，但实际 API 接收秒级整数，以接口行为为准。

## 使用方式

1. **写入记忆**：  
   - 事实记忆：`POST /v1/memory/fragments`，请求体含 `fragment_key`、`value`、`profile_id`（可选）；  
   - 用户画像：`POST /v1/memory/profiles`，请求体需含 `profile_id` 及结构化字段（如 `{"preferences": {"theme": "dark"}}`）。

2. **查询记忆**：  
   - 按键查事实：`GET /v1/memory/fragments/{fragment_key}?profile_id=xxx`；  
   - 查画像全量：`GET /v1/memory/profiles/{profile_id}`；  
   - 语义检索（实验性）：`POST /v1/memory/fragments/search`，传入自然语言 query。

3. **在对话中启用**：  
   在 `/v1/chat/completions` 请求的 `messages` 外层添加 `"enable_long_term_memory": true`，并确保 `profile_id` 已通过 `headers.x-profile-id` 或 `messages[0].profile_id` 传递。

## 限制和注意事项

- 单个 Profile 最多存储 1000 个字段（含嵌套），单个 Fragment 值长度上限 8192 字符；
- 事实记忆不支持事务性写入，高并发写同一 `fragment_key` 可能导致最终一致性延迟（约 1–3 秒）；
- 自动记忆注入（`enable_long_term_memory: true`）**仅在流式响应（`stream: true`）下生效**，非流式请求不会注入记忆上下文 —— 此行为与 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 文档中“所有模式均支持”的描述矛盾，以实际接口表现为准；
- 删除操作暂不开放，过期记忆自动清理，非过期记忆需联系技术支持清除。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


