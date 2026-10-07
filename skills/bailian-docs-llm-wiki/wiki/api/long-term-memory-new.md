# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持事实记忆（Observation/Skill）与用户画像（User Profile）两类核心数据的写入、检索、更新与管理。所有接口通过统一的 DashScope 网关提供服务，采用 API Key 鉴权，适用于构建具备上下文感知与个性化能力的智能体应用。该能力将于 2026 年 8 月 20 日起正式商业化计费，Add 和 Search 接口区分 `pro` 与 `lite` 计划版本 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 支持的模型/功能

[长期记忆](../concepts/memory.md)不依赖外部大模型调用，而是由平台内置的记忆抽取引擎自动完成语义解析与结构化生成，按用途分为两类：

- **事实记忆**：基于对话消息（`messages`）或自定义文本（`custom_content`）提取可复用的事实片段（`observation`）或可执行技能（`skill`）。支持同步写入（`/add`）与异步批量处理（`/add-async`），后者适用于多项目并行、含工具调用或多模态内容的复杂场景 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **用户画像**：通过预定义的画像模板（`profile_schema`）对用户属性（如年龄、职业、偏好）进行结构化建模。画像提取为异步过程，需先创建模板，再在 `AddMemory` 中传入 `profile_schema` 触发抽取，最后通过 `GetUserProfile` 查询结果 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。

> **注意**：文档 7（添加记忆）称“当前主推异步添加”，而文档 6（异步添加记忆）未明确否定同步接口的可用性；但文档 7 同时指出同步接口在 `intelligent` 模式下“可能超时”。因此，**生产环境应优先使用 `/add-async` + `/events/{event_id}` 轮询机制**，避免同步阻塞风险。

## 关键参数

| 参数 | 位置/类型 | 说明 | 必填 |
|------|-----------|------|------|
| `user_id` | Query / Body | 子用户唯一标识，用于跨用户记忆隔离 | ✅（所有读写接口） |
| `memory_library_id` | Query / Body | 记忆库 ID，不传则使用默认库 | ❌（默认生效） |
| `project_id` / `project_ids` | Body | 项目级二级隔离标识，`project_ids` 最多 5 个 | ❌（但推荐使用以提升组织性） |
| `profile_schema` | Body | 用户画像模板 ID，仅在需触发画像抽取时传入 | ❌（但 `extract_mode=profile_only` 时必填） |
| `plan_version` | Body | `search-memory` 和 `profile_schema` 创建/更新时指定，取值 `pro` 或 `lite`；`pro` 支持 `min_score` 过滤与更细粒度策略 | ❌（默认 `pro`） |
| `min_score` | Body | `search-memory` 的分数阈值（0.0–1.0），仅 `plan_version=pro` 时生效 | ❌（默认 0.3） |

## 使用方式

1. **鉴权准备**：在[百炼控制台](https://bailian.console.aliyun.com/)获取 `DASHSCOPE_API_KEY`，通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头传递 [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
2. **写入记忆**：
   - 事实记忆：使用 `POST /add`（实时性要求高且内容简单）或 `POST /add-async`（推荐，支持多模态、工具调用、批量项目）。响应中返回 `event_id`，需轮询 `GET /events/{event_id}` 获取最终结果。
   - 用户画像：先 `POST /profile_schemas` 创建模板，再调用 `AddMemory` 时传入 `profile_schema`，最后 `GET /profile_schemas/{id}/user_profile?user_id=xxx` 查询。
3. **检索记忆**：`POST /memory_nodes/search`，传入 `messages` 作为查询向量，指定 `user_id`、`top_k`、`memory_types`（`["observation"]` 或 `["skill"]`）及 `plan_version`。
4. **管理记忆**：`GET /memory_nodes` 分页列表；`GET /memory_nodes/{id}` 查单条；`PATCH /memory_nodes/{id}` 更新内容；`DELETE /memory_nodes/{id}` 删除（不可逆）。

## 限制和注意事项

- **限流**：阿里云账号级别总计 ≤ 3000 QPM；其中 `add` 接口 ≤ 120 QPM，`search` 接口 ≤ 300 QPM。超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **计费时效**：所有记忆与画像数据**无自动失效日期**，长期存储；但商业化计费自 2026 年 8 月 20 日起生效，届时 `add` 和 `search` 调用将按 `pro`/`lite` 版本计费 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至代码仓库，建议按应用拆分并定期轮转 [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **异步可靠性**：`/add-async` 返回 `status=PENDING` 或 `RUNNING` 时，必须主动轮询 `/events/{event_id}`，不可假设立即完成；`status=FAILED` 时需检查 `request_id` 并联系支持。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)


