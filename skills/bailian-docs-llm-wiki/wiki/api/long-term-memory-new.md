# long term memory new

长期记忆（Long Term Memory, LTM）是百炼平台提供的结构化[记忆管理](../concepts/memory.md)能力，用于在多轮对话或跨会话场景中持久化存储和检索用户相关事实、偏好与行为画像。它通过语义索引与向量检索实现高效召回，并支持开发者按需配置记忆类型与生命周期。该能力当前处于新架构迭代阶段，部分接口与旧版不兼容，详见 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)。

## 支持的模型/功能

- **模型支持**：仅限 `qwen-max`、`qwen-plus` 及后续标注为 `ltm-enabled` 的模型版本；`qwen-turbo` 和 `qwen-14b-chat` 等轻量模型暂不支持。
- **核心功能模块**：
  - **事实记忆（Fragments）**：存储离散、可验证的事实性信息（如“用户邮箱为 alice@example.com”），支持按 key 更新与条件查询；
  - **用户画像（Profiles）**：聚合多维度用户属性（如偏好、身份标签、历史意图），以结构化 schema 管理；
  - **自动记忆提取**：在启用 `auto_extract: true` 时，模型可从对话中识别并写入符合规则的事实（需配合 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md) 定义的 schema）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_type` | string | 是 | 取值为 `"fragment"` 或 `"profile"`，决定写入/查询目标类型 |
| `ttl_seconds` | integer | 否 | 记忆存活时间（秒），默认 `31536000`（1 年）；设为 `0` 表示永不过期 |
| `namespace` | string | 否 | 隔离作用域，默认为应用 ID；不同 namespace 的记忆互不可见 |
| `auto_extract` | boolean | 否 | 仅对 `fragment` 有效；启用后由模型自动解析并写入匹配 schema 的事实，详见 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) |

> **注意**：`ttl_seconds` 在 `profile` 类型下实际生效逻辑与文档描述存在偏差——实测中 profile 不受 ttl 控制，其更新仅依赖显式 `PUT /profiles/{id}` 调用。请以 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md) 中的运行时行为为准，而非 API 文档中的 TTL 描述。

## 使用方式

1. **初始化**：在应用配置中启用 `long_term_memory: true`，并指定 `memory_schema`（JSON Schema 格式，定义 fragment 或 profile 的字段约束）；
2. **写入记忆**：
   ```http
   POST /v1/memory/fragments
   {
     "key": "user_email",
     "value": "alice@example.com",
     "memory_type": "fragment",
     "ttl_seconds": 86400
   }
   ```
3. **检索记忆**：在 `messages` 中添加 `memory_context: { "include": ["fragment", "profile"] }`，系统将在推理前自动注入匹配的记忆片段；
4. **调试建议**：使用 `/v1/memory/debug` 接口查看当前会话已加载的记忆快照，避免依赖隐式行为。

## 限制和注意事项

- 单次请求最多加载 50 条记忆（按语义相似度排序截断），超出部分需通过 `filter` 参数主动筛选；
- `fragment` 的 `key` 必须全局唯一且不可含特殊字符（仅支持 `[a-zA-Z0-9_-]`）；
- 所有记忆写入均异步落库，`200 OK` 仅表示入队成功，不保证立即可查；
- 旧版 `short_term_memory` 与新版 `long_term_memory` **完全隔离**，迁移需手动重写 schema 与调用逻辑，参考 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 中的迁移指南。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


