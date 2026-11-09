# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持开发者以编程方式写入、检索、更新和删除用户记忆节点及画像数据。其核心能力包括基于对话的自动记忆抽取（事实记忆 `observation` 和技能记忆 `skill`）、多项目隔离、用户画像模板驱动的属性提取，以及语义相似度搜索。所有接口通过业务空间专属域名调用，需配合 API Key 鉴权。

## 支持的模型/功能

- **记忆类型**：支持两类结构化记忆节点：  
  - `observation`（事实记忆）：如“用户每天上午11点提醒点外卖”，由对话内容自动抽取；  
  - `skill`（技能记忆）：如“会议纪要整理”，需显式传入 `skill_name`/`skill_description`/`skill_tags`，适用于可复用的行为流程。  
  详见 [添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 和 [异步添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

- **用户画像**：通过预定义的画像模板（`profile_schema`）驱动抽取，支持字段级描述、默认值与动态增删操作。画像提取为异步过程，需配合 [GetUserProfile](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询结果。

- **多模态支持**：`messages` 中可传入 `image_url` 类型内容，但仅在启用多模态能力的项目中被解析；其他项目将忽略图片字段。

> **注意**：文档 6（同步 AddMemory）明确指出“当前主推[异步添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)”，且在 `intelligent` 模式下同步接口可能超时；而文档 3 的接口概览未强调此推荐策略，存在表述不一致，建议优先使用异步接口。

## 关键参数

| 参数 | 说明 | 示例值 | 是否必填 |
|------|------|--------|----------|
| `user_id` | 子用户 ID，用于跨用户记忆隔离 | `"user_001"` | 是（所有写入/检索接口） |
| `project_id` / `project_ids` | 记忆二级隔离标识；`project_ids` 最多支持 5 个，与 `project_id` 互斥 | `["project_001"]` | 否（但影响记忆归属与检索范围） |
| `profile_schema` | 用户画像模板 ID；传入后触发画像抽取 | `"50edf54eaa5842e891d959ae115205be"` | 否（仅画像场景需） |
| `memory_types` | 搜索时指定记忆类型过滤，默认 `["observation"]` | `["observation", "skill"]` | 否 |
| `plan_version` | 计费策略：`pro`（支持 `min_score` 过滤、Rerank）或 `lite`（基础检索） | `"pro"` | 否（默认 `pro`） |
| `min_score` | `plan_version=pro` 时生效，过滤低分结果 | `0.6` | 否（默认 `0.3`） |

## 使用方式

1. **环境准备**：  
   - 设置 `DASHSCOPE_API_KEY` 环境变量（见 [认证](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）；  
   - 设置 `MEMORY_SERVICE_ENDPOINT` 为业务空间专属域名（格式：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`），末尾**不带 `/`**（见 [概览](raw/application-api-reference/long-term-memory-new/api-overview.md)）。

2. **典型工作流**：  
   - **写入**：调用 `POST /add-async` 提交对话，获取 `event_id`；再轮询 `GET /events/{event_id}` 获取抽取结果（含 `observation`/`skill`/`user_profile`）；  
   - **检索**：调用 `POST /memory_nodes/search`，传入查询 `messages` 和 `user_id`，返回带 `score` 的记忆列表；  
   - **画像**：先用 `POST /profile_schemas` 创建模板，再在 `AddMemoryAsync` 中传 `profile_schema`，最后用 `GET /profile_schemas/{id}/user_profile?user_id=...` 获取属性值（见 [获取用户画像](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）。

3. **SDK 调用**：推荐使用 `agentscope-runtime` 工具类（如 `AddMemoryAsync`, `SearchMemory`, `GetUserProfile`），避免手动拼接 URL 和 Header。

## 限制和注意事项

- **限流**：阿里云账号级别总限流 3000 QPM；其中 `add` 接口 120 QPM，`search` 接口 300 QPM（见 [长期记忆API 参考](raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。超限时返回 HTTP 429，需按指数退避（1s/2s/4s）重试。
- **计费时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化计费，Add 和 Search 调用均区分 `pro`/`lite` 版本（见 [概览](raw/application-api-reference/long-term-memory-new/api-overview.md) 和 [长期记忆API 参考](raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。
- **安全要求**：API Key 必须通过环境变量注入，禁止硬编码或提交至代码仓库（见 [认证](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）。
- **删除不可逆**：`DELETE /memory_nodes/{id}` 操作永久删除，无回收站（见 [删除记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)）。
- **画像延迟**：用户画像提取为异步过程，首次 `GetUserProfile` 可能返回空值，需按业务逻辑重试（见 [获取用户画像](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）。

## 来源文档

- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)


