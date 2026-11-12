# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理服务，支持事实记忆（`observation`）、技能记忆（`skill`）和用户画像三类数据的写入、检索与生命周期管理。所有操作通过 RESTful API 或 `agentscope-runtime` SDK 完成，需使用业务空间专属域名和 `DASHSCOPE_API_KEY` 鉴权。服务将于 2026 年 8 月 20 日起正式商业化计费，Add 和 Search 接口区分 `pro` 与 `lite` 计划版本。

## 支持的模型/功能

- **记忆类型**：支持两类核心记忆节点：
  - `observation`（事实记忆）：如“用户每天上午11点提醒点外卖”，默认检索目标；
  - `skill`（技能记忆）：结构化封装可复用能力，含 `skill_name`、`skill_description`、`skill_tags` 字段，需通过 [导出技能记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md) 接口获取完整信息。
- **用户画像**：需先创建画像模板（[CreateProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)），再在 `AddMemory` 或 `AddMemoryAsync` 中传入 `profile_schema` 参数触发异步抽取；画像属性值通过 [GetUserProfile](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询。
- **多模态支持**：`messages` 中可传入 `image_url` 类型内容，但仅限已开通多模态能力的项目解析图片；其他项目将忽略图片字段。
- **抽取模式**：`AddMemory` 支持 `efficient`（低延迟）与 `intelligent`（高精度）两种模式，后者可能超时，推荐优先使用 [异步添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

> **注意**：文档 6（同步 AddMemory）称 `intelligent` 模式“可能超时”，而文档 7（异步 AddMemory）明确其“支持多项目并行抽取、技能抽取和用户画像抽取”。二者功能存在重叠但语义不一致——实际生产环境应以异步接口为首选，同步接口仅适用于对实时性要求极高且内容简单（如纯文本 `custom_content`）的场景。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | Query / Body | 是 | 子用户 ID，用于跨用户记忆隔离，所有读写接口均需提供 |
| `memory_library_id` | Query / Body | 否 | 记忆库 ID；不传则使用默认库；影响 `ListMemory`、`SearchMemory` 等接口范围 |
| `project_id` / `project_ids` | Query / Body | 否 | 项目级二级隔离标识；`project_ids` 最多支持 5 个，与 `project_id` 互斥；决定记忆抽取规则（如 `observation` 或 `skill`） |
| `profile_schema` | Body | 否（画像必需） | 用户画像模板 ID；仅当需抽取画像时传入，否则不触发画像流程 |
| `plan_version` | Body（SearchMemory） | 否 | `pro`（默认）或 `lite`；`pro` 支持 `min_score` 过滤，`lite` 不生效；详见[计费说明](raw/application-user-guide/agent-billing/billing.md) |
| `memory_types` | Body（SearchMemory） | 否 | 默认 `["observation"]`；显式传入 `["skill"]` 或 `["observation","skill"]` 才能检索技能记忆 |

## 使用方式

1. **准备凭证**：  
   - 获取 `DASHSCOPE_API_KEY`（[鉴权](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）；  
   - 获取业务空间 ID（`llm-xxxxxxxxxxxx`），拼接服务地址：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/`。

2. **写入记忆**：  
   - **同步写入**（适合简单、实时场景）：调用 `POST /add`，传 `messages` 或 `custom_content`；响应直接返回 `memory_nodes`。  
   - **异步写入**（推荐）：调用 `POST /add-async`，立即返回 `event_id`；后续用 `GET /events/{event_id}` 轮询状态与结果。

3. **检索与管理**：  
   - **语义搜索**：`POST /memory_nodes/search`，传 `messages` 作为查询向量，指定 `top_k` 和 `memory_types`；  
   - **列表查询**：`GET /memory_nodes`，支持 `page_num`/`page_size` 分页；  
   - **单条操作**：`GET /memory_nodes/{id}` 查详情，`PATCH /memory_nodes/{id}` 更新，`DELETE /memory_nodes/{id}` 删除（软删除，`status=delete`）。

4. **用户画像工作流**：  
   - 创建模板 → `POST /profile_schemas`；  
   - 写入带 `profile_schema` 的记忆 → `POST /add` 或 `/add-async`；  
   - 查询画像 → `GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`（首次可能为空，需重试）。

## 限制和注意事项

- **限流**：全接口总计 ≤3000 QPM（阿里云账号级别）；其中 `add` ≤120 QPM，`search` ≤300 QPM。超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试 [错误码](raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **时效性**：用户画像为异步抽取，`GetUserProfile` 首次调用可能无数据，需按业务逻辑重试；记忆节点与画像本身无自动过期机制。
- **ID 隔离**：`user_id` 是强制隔离维度，`project_id` 和 `memory_library_id` 为可选二级隔离，三者共同构成数据可见性边界。
- **安全要求**：API Key 必须通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 传入 Header，严禁硬编码或提交至仓库；建议为不同应用分配独立 Key 并定期轮转。
- **删除不可逆**：`DELETE /memory_nodes/{id}` 为软删除（标记 `status=delete`），但 `GetMemoryNode` 仍可查到该节点；若需彻底清除，需联系技术支持。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)


