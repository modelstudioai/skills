# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理服务，支持事实记忆（`observation`）、技能记忆（`skill`）和用户画像（`user_profile`）三类记忆的写入、检索与生命周期管理。所有操作均通过 RESTful API 或 `agentscope-runtime` SDK 完成，需使用业务空间专属域名与 `DASHSCOPE_API_KEY` 鉴权。记忆节点默认永不过期，但受限流与存储策略约束。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如用户偏好、日程）、`skill`（可复用的流程化能力，如“会议纪要整理”）两类结构化记忆节点；用户画像需配合独立的画像模板（`profile_schema`）使用。
- **抽取模式**：
  - `efficient`：低延迟、轻量级抽取，适用于实时性要求高的场景；
  - `intelligent`：高精度抽取，支持更复杂的语义理解，但可能超时（[添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 文档明确建议在 `intelligent` 模式下优先使用异步接口）。
- **多模态支持**：当项目配置支持多模态能力时，`messages[].content` 中的 `image_url` 可被解析并参与记忆抽取；否则图片信息将被忽略。
- **画像提取**：需先创建画像模板（[创建画像模板](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)），再在 `AddMemory` 或 `AddMemoryAsync` 请求中传入 `profile_schema` ID 才能触发抽取。

> **注意**：文档 6（同步 AddMemory）称 `intelligent` 模式下可能超时，而文档 7（异步 AddMemory）明确支持 `intelligent` 场景下的技能与画像抽取。因此，**对 `intelligent` 模式或含 `tool_calls`/`profile_schema` 的请求，必须使用 `AddMemoryAsync`**，否则可能失败或丢失抽取结果。

## 关键参数

| 参数 | 说明 | 示例值 | 必填性 |
|------|------|--------|--------|
| `user_id` | 子用户唯一标识，用于跨记忆库/项目隔离 | `"user_001"` | 所有写入与检索接口必填 |
| `project_id` / `project_ids` | 记忆二级隔离维度；`project_ids` 最多 5 个，与 `project_id` 互斥 | `["project_001"]` | 写入时推荐指定，检索时可选 |
| `memory_library_id` | 记忆库 ID；不传则使用默认库 | `"memory_library_001"` | 可选，但建议显式指定以避免混淆 |
| `profile_schema` | 用户画像模板 ID；仅当需抽取画像时传入 | `"50edf54eaa5842e891d959ae115205be"` | 条件必填（见画像章节） |
| `plan_version` | 计费策略：`pro`（启用 Rerank、`min_score` 过滤）或 `lite`（基础检索） | `"pro"` | `SearchMemory` 默认 `pro`；`CreateProfileSchema` 等接口也支持该参数 |
| `extract_mode` | 抽取控制：`profile_only` 表示仅抽取画像（此时 `messages` 必须存在） | `"profile_only"` | 条件必填 |

## 使用方式

### 1. 准备凭证
- 获取 `DASHSCOPE_API_KEY`（[鉴权](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）；
- 获取业务空间 ID（`WorkspaceId`），格式为 `llm-xxxxxxxxxxxx`，来自控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace) 页面；
- 设置环境变量：`export DASHSCOPE_API_KEY="sk-..."` 和 `export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`（SDK 使用）。

### 2. 写入记忆
- **同步写入（适合简单 `observation`）**：调用 `POST /add`，传入 `messages` 或 `custom_content`；
- **异步写入（推荐，支持 `skill`/`profile`/`intelligent`）**：调用 `POST /add-async`，立即返回 `event_id`，再用 `GET /events/{event_id}` 轮询结果（[查询事件](raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)）；
- **技能记忆专用字段**：若写入 `skill` 类型，`AddMemoryAsync` 请求中需提供 `skill_name`、`skill_description`、`skill_tags`；`UpdateMemory` 更新时同样需携带这三项。

### 3. 检索与管理
- **语义搜索**：`POST /memory_nodes/search`，传入 `messages` 作为查询向量，支持 `top_k`、`min_score`（`pro` 版本）、`memory_types` 筛选；
- **列表浏览**：`GET /memory_nodes?user_id=...&page_num=1&page_size=10`；
- **单条查询**：`GET /memory_nodes/{memory_node_id}`；
- **技能导出**：`GET /skill/export/{memory_node_id}`（仅限 `skill` 类型节点）；
- **用户画像获取**：`GET /profile_schemas/{schema_id}/user_profile?user_id=...`，首次调用可能为空，需按业务逻辑重试（[获取用户画像](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）。

## 限制和注意事项

- **限流**：全接口总计 3000 QPM（阿里云账号级别）；其中 `add` 接口 120 QPM，`search` 接口 300 QPM。超限返回 HTTP 429，应实现指数退避重试（[错误码](raw/application-api-reference/long-term-memory-new/api-overview/errors.md)）。
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，`Add` 和 `Search` 接口区分 `Pro`/`Lite` 版本（[长期记忆API 参考](raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。
- **软删除**：`DELETE /memory_nodes/{id}` 为逻辑删除，`status` 变为 `"delete"`，仍可通过 `GetMemoryNode` 查询历史快照，但 `ListMemory` 和 `SearchMemory` 默认不返回已删除节点。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；建议按应用拆分 Key 并定期轮转（[认证](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）。
- **多模态兼容性**：`image_url` 解析能力取决于项目配置，未开启多模态的项目会静默忽略图片内容，不报错也不参与抽取。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)


