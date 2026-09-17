# long term memory new

长期记忆（Long Term Memory）是百炼平台提供的结构化[记忆管理](../concepts/memory.md)能力，支持将对话历史自动提炼为事实记忆（Memory Nodes）并构建用户画像（User Profile）。该能力通过 RESTful API 提供，所有接口统一接入 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，需使用 `DASHSCOPE_API_KEY` 鉴权。记忆与画像两条链路逻辑解耦：事实记忆默认启用，用户画像需显式传入 `profile_schema_id` 才触发提取。

## 支持的模型/功能

- **事实记忆**：基于对话消息（`messages`）或自定义内容（`custom_content`）自动抽取结构化记忆片段，支持添加、搜索、列表、更新和删除全生命周期操作。检索支持语义匹配、查询改写（`enable_rewrite`）、意图判别（`enable_judge`）及重排（Rerank），其中 Rerank 由 `plan_version` 控制（`Pro` 启用，`Lite` 关闭）[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
- **用户画像**：通过预定义模板（`ProfileSchema`）描述期望提取的用户属性（如“年龄”“爱好”），在调用 `AddMemory` 时传入 `profile_schema` 即可触发画像提取；后续可通过 `GetUserProfile` 查询结果。模板支持 `Pro`/`Lite` 两种策略版本，影响提取精度与延迟 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。
- **双轨独立性**：事实记忆与用户画像使用不同模型链路，互不影响。不传 `profile_schema` 时，`AddMemory` 仅返回 `memory_nodes`，画像字段恒为空 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | body/path | string | 是 | 记忆/画像归属实体 ID，最大 64 字符 |
| `messages` / `custom_content` | body | array/string | 二选一 | 对话消息列表（最多 50 条）或纯文本内容（最大 512 字符），二者互斥 |
| `profile_schema_id` | body | string | 否（画像必需） | 画像模板 ID，缺失则跳过画像提取 |
| `plan_version` | body | string | 否 | `Pro`（默认，启用 Rerank/高精度提取）或 `Lite`（低成本/低延迟），大小写不敏感；`SearchMemory` 和 `CreateProfileSchema` 均支持此参数 |
| `top_k`, `min_score` | body | number | 否 | 搜索接口召回数量（1–100，默认 10）和最小相似度阈值（0.0–1.0，默认 0.3） |

> **注意**：文档 11 中 `CreateProfileSchema` 的 `plan_version` 默认值为 `Pro`，而文档 12 的响应示例中 `plan_version` 字段值为 `"pro"`（小写），实际服务端对大小写不敏感，但建议统一使用大写 `Pro`/`Lite` 以避免歧义。

## 使用方式

1. **鉴权准备**：在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)获取 `DASHSCOPE_API_KEY`（`sk-` 开头），并通过环境变量或请求 Header 传递：  
   `Authorization: Bearer $DASHSCOPE_API_KEY` [鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md)。
2. **基础流程**：
   - 创建画像模板（可选）：调用 `POST /profile_schemas` 定义字段；
   - 写入记忆：`POST /add`，传入 `user_id` + `messages`（或 `custom_content`）+ 可选 `profile_schema_id`；
   - 检索记忆：`POST /memory_nodes/search`，传入 `user_id` + `messages` + `plan_version`；
   - 查询画像：`GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`，需等待约 3 秒确保提取完成 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。
3. **SDK 调用**：推荐使用 `agentscope_runtime.tools.modelstudio_memory` 模块中的封装类（如 `AddMemory`, `SearchMemory`, `GetUserProfile`），自动处理序列化与错误重试。

## 限制和注意事项

- **限流**：阿里云账号级总 QPM ≤ 3000；`/add` 接口单独限 120 QPM；`/memory_nodes/search` 限 300 QPM。超限返回 `429`，需按指数退避（1s/2s/4s）重试 [错误码](../../raw/application-api-reference/long-term-memory-new/overview/errors.md)。
- **数据持久性**：生成的记忆片段与用户画像无自动失效机制，长期有效。
- **不可逆操作**：`DELETE /memory_nodes/{id}` 与 `DELETE /profile_schemas/{id}` 均不可恢复，删除画像模板将同时清除已提取的对应用户画像数据 [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)。
- **计费提示**：该服务将于 **2026 年 8 月 20 日 10:00（北京时间）起正式商业化计费**，`Add` 和 `Search` 接口均区分 `Pro`/`Lite` 版本，详情见计费文档 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/overview/errors.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/overview.md)
- [删除画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/delete-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)


