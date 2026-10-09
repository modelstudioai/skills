# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化用户状态持久化能力，用于在多轮对话或跨会话场景中维护事实性知识、用户偏好与行为画像。它通过语义索引与向量检索实现低延迟读写，支持开发者构建具备上下文连续性的智能体应用。该能力需配合兼容模型与特定 API 调用方式使用，详见 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)。

## 支持的模型与功能

- **模型支持**：当前仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo`（v202409 及以上版本）原生支持 LTM 的自动注入与更新；其他模型需显式调用 `/v1/memory/query` 与 `/v1/memory/upsert` 接口管理记忆。
- **核心功能模块**：
  - **事实记忆（Fragments）**：存储结构化短文本片段（如“用户住址：杭州市西湖区”），支持语义检索与去重合并，详见 [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)。
  - **用户画像（Profiles）**：维护键值对形式的用户属性（如 `age: 28`, `preferred_language: zh`），支持类型校验与 TTL 过期，详见 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_type` | string | 是 | 取值为 `"fragment"` 或 `"profile"` |
| `namespace` | string | 是 | 命名空间，用于隔离不同业务域（如 `"customer_service"`） |
| `ttl_seconds` | integer | 否 | 记忆存活时间（秒），`0` 表示永不过期；`profile` 默认 30 天，`fragment` 默认 7 天 |
| `embedding_model` | string | 否 | 指定嵌入模型（如 `"text-embedding-v3"`），未指定时使用平台默认模型 |

> **注意**：原始文档 [通用](../../raw/application-api-reference/long-term-memory-new/api-overview.md) 中提及 `ttl_seconds` 对 `profile` 默认为永久，但实测 v202410 版本 API 返回的 `profile` 默认 TTL 为 2592000 秒（30 天），以实际接口响应为准。

## 使用方式

1. **启用记忆注入**：在 `/v1/chat/completions` 请求中设置 `enable_memory: true`，并确保 `model` 在支持列表内；
2. **手动管理记忆**：
   - 查询：`POST /v1/memory/query`，传入 `query_text` 与 `filter`；
   - 写入：`POST /v1/memory/upsert`，按 `memory_type` 提交结构化 payload；
3. **调试建议**：首次集成时，务必调用 `/v1/memory/query?namespace=xxx&limit=5` 验证数据可见性，避免因命名空间拼写错误导致静默失败。

## 限制和注意事项

- 单次 `upsert` 最多写入 50 条记忆；单个 `fragment` 文本长度上限 2048 字符，`profile` 键名长度 ≤ 64 字符、值长度 ≤ 1024 字符；
- 记忆检索不保证强一致性：写入后最多 2 秒内可被查到，高并发场景下可能出现短暂延迟；
- 所有记忆按 `app_id` + `namespace` + `user_id` 三级隔离，**跨 app_id 的记忆不可见**，即使 namespace 相同；
- 删除操作仅支持按 `id` 或 `filter` 批量删除，不支持清空整个 namespace —— 如需重置，须在 [长期记忆](../../raw/application-api-reference/long-term-memory-new.md) 文档指引下使用 `delete_by_filter` 并谨慎构造条件。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


