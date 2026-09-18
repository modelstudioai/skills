# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持将对话自动提取为事实记忆（Memory Nodes）和用户画像（User Profile）两类数据。该能力通过统一的 RESTful API 提供服务，所有操作均需 API Key 鉴权，适用于智能体（Agent）状态持久化、个性化上下文构建等场景。记忆数据默认长期有效，无自动过期机制。

## 支持的模型/功能

[长期记忆](../concepts/memory.md)提供两类核心能力：

- **事实记忆（Fact Memory）**：从对话中自动抽取结构化、可检索的事实片段（如“用户每天上午9点需要喝水提醒”），支持添加（`/add`）、语义搜索（`/memory_nodes/search`）、列表查询（`/memory_nodes`）、更新（`PATCH /memory_nodes/{id}`）和删除（`DELETE /memory_nodes/{id}`）。详见 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 和 [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)。

- **用户画像（User Profile）**：基于预定义模板（Schema）从对话中提取用户属性（如年龄、职业、爱好）。需先调用 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)，再在 `AddMemory` 中传入 `profile_schema` 参数触发提取，最后通过 `GetUserProfile` 获取结果。

> **注意**：文档 10 和文档 11 均显示 `plan_version` 默认为 `"pro"`，但文档 13 明确说明更新模板时可设为 `"Lite"`；而文档 5 的 `AddMemory` 接口参数说明中未提及 `plan_version` 字段，仅在 `profile_schema` 存在时隐式关联其策略版本。因此，画像提取质量由所引用模板的 `plan_version` 决定，而非 `AddMemory` 请求本身携带该参数。

## 关键参数

| 类别 | 参数名 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| **通用** | `Authorization` | Header | 是 | `Bearer $DASHSCOPE_API_KEY`，获取方式见 [鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md) |
| **事实记忆写入** | `user_id` | string | 是 | 记忆归属实体 ID（最大 64 字符） |
| | `messages` 或 `custom_content` | array/string | 是（互斥） | 对话消息列表（最多 50 条）或自定义文本（最大 512 字符） |
| | `profile_schema` | string | 否 | 画像模板 ID；**不传则不触发画像提取**，仅写入事实记忆 |
| **事实记忆检索** | `top_k` | number | 否 | 最大召回数（1–100，默认 10） |
| | `min_score` | number | 否 | 相似度阈值（0.0–1.0，默认 0.3） |
| | `plan_version` | string | 否 | `"Pro"`（开启 Rerank，质量高）或 `"Lite"`（关闭 Rerank，成本低），大小写不敏感；优先级高于 `enable_rerank` |
| **用户画像** | `attributes`（创建模板时） | array | 是 | 每项含 `name`（字段名）和 `description`（提取提示） |

## 使用方式

1. **准备凭证**：在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)获取 `DASHSCOPE_API_KEY`，并配置为环境变量（见 [鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md)）。
2. **（可选）创建画像模板**：调用 `POST /profile_schemas` 定义字段，获取 `profile_schema_id`。
3. **写入记忆**：调用 `POST /add`，传入 `user_id` 和 `messages`（或 `custom_content`）；若需同步提取画像，**必须传入 `profile_schema`**。
4. **检索记忆**：
   - 语义搜索：`POST /memory_nodes/search`，传入 `user_id` 和当前 `messages`；
   - 全量查看：`GET /memory_nodes?user_id=xxx`（支持分页）。
5. **获取画像**：调用 `GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`；注意需等待约 3 秒待异步提取完成。

## 限制和注意事项

- **限流**：阿里云账号级别总计 ≤ 3000 QPM；其中 `Add` 接口 ≤ 120 QPM，`Search` 接口 ≤ 300 QPM。超限返回 HTTP 429，建议按 [错误码](../../raw/application-api-reference/long-term-memory-new/overview/errors.md) 文档实施指数退避重试。
- **数据生命周期**：生成的记忆片段与用户画像**暂无失效日期**，长期保留（除非主动删除）。
- **不可逆操作**：`DeleteMemory` 和 `DeleteProfileSchema` 均不可恢复，且后者会**一并清除已提取的画像数据**（见 [删除画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/delete-schema.md)）。
- **商业化时间点**：所有 `Add` 和 `Search` 调用将于 **2026 年 8 月 20 日 10:00（北京时间）起正式计费**，区分 `Pro`/`Lite` 版本策略（见 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。
- **调试关键**：所有响应均含 `request_id`，排查问题时务必提供此字段。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/overview.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [删除画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/delete-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/overview/errors.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)


