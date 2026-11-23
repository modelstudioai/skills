# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类数据的写入、检索、更新与生命周期管理。所有操作通过 RESTful API 或 `agentscope-runtime` SDK 完成，需使用业务空间专属域名和 `DASHSCOPE_API_KEY` 鉴权。记忆节点默认永不过期，但受账号级限流约束。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如“用户明天10点开会”）、`skill`（技能记忆，如“会议纪要整理流程”）两类结构化记忆节点；`user_profile` 为独立画像维度，需配合画像模板使用。
- **抽取能力**：
  - `AddMemory` 和 `AddMemoryAsync` 均支持基于对话消息（`messages`）自动抽取记忆，其中 `AddMemoryAsync` 支持多项目并行、技能抽取及画像联合提取 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)；
  - `custom_content` 模式可绕过抽取，直接写入原始内容（仅 `AddMemory` 和 `AddMemoryAsync` 支持）；
  - 技能记忆导出需调用专用接口 [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)，返回含 `skill_name`、`skill_description`、`skill_tags` 的完整结构。
- **用户画像**：需先创建画像模板（[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)），再在 `AddMemory` 或 `AddMemoryAsync` 中传入 `profile_schema` 参数触发抽取；画像结果通过 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询，注意该过程为异步，首次查询可能为空。

> **注意**：文档 6（同步添加）称 `AddMemory` 在 `intelligent` 模式下“可能超时”，而文档 7（异步添加）明确推荐其用于多项目并行与技能抽取——实践中应优先选用 `AddMemoryAsync`，尤其当涉及 `project_ids`、`skill_name` 或 `profile_schema` 时；`AddMemory` 仅适用于低延迟要求且无复杂抽取需求的场景。

## 关键参数

| 参数 | 说明 | 示例值 | 必填性 |
|------|------|--------|--------|
| `user_id` | 子用户 ID，用于跨用户记忆隔离 | `"user_001"` | 所有写入/检索接口必填 |
| `memory_library_id` | 记忆库 ID，不传则使用默认库 | `"memory_library_001"` | 可选（默认库） |
| `project_id` / `project_ids` | 项目 ID（单个）或项目 ID 数组（最多 5 个），用于二级隔离与抽取规则路由 | `["project_001", "project_002"]` | 写入时可选；`AddMemoryAsync` 与 `SearchMemory` 中二者互斥 |
| `profile_schema` | 画像模板 ID，传入后触发用户画像抽取 | `"50edf54eaa5842e891d959ae115205be"` | 仅画像抽取必填 |
| `plan_version` | 搜索/画像计费策略：`pro`（支持 `min_score` 过滤、Rerank）或 `lite`（基础检索） | `"pro"` | `SearchMemory` 默认 `pro`；`CreateProfileSchema` 等画像接口也支持该参数 |
| `memory_types` | `SearchMemory` 中指定检索的记忆类型，默认 `["observation"]` | `["observation", "skill"]` | 可选 |

## 使用方式

1. **准备凭证**：  
   - 获取 `DASHSCOPE_API_KEY`（控制台 → API Key 管理）和 `WorkspaceId`（控制台 → 业务空间管理 → API Host 列）；  
   - 设置环境变量：`export DASHSCOPE_API_KEY="sk-xxx"` 和 `export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`（SDK 使用）。

2. **写入记忆**：  
   - 同步写入（适合简单、实时性高场景）：调用 `POST /add`，传 `messages` 或 `custom_content`；  
   - 异步写入（推荐）：调用 `POST /add-async`，立即获得 `event_id`，再轮询 `GET /events/{event_id}` 获取结果 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)；  
   - 技能记忆需在 `AddMemoryAsync` 中同时传 `skill_name`、`skill_description`、`skill_tags`。

3. **检索与管理**：  
   - 语义搜索：`POST /memory_nodes/search`，支持 `top_k`、`min_score`（`pro` 版本）、`memory_types` 筛选；  
   - 分页列表：`GET /memory_nodes?user_id=xxx`；  
   - 单条查询/更新/删除：`GET`/`PATCH`/`DELETE /memory_nodes/{memory_node_id}`；  
   - 用户画像：创建模板 → 写入时传 `profile_schema` → 调用 `GET /profile_schemas/{schema_id}/user_profile?user_id=xxx` 查询。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；`/add` 接口单独限流 120 QPM，`/memory_nodes/search` 限流 300 QPM。超限返回 HTTP 429，需按指数退避重试（1s/2s/4s）[错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **商业化时间点**：所有 `Add` 和 `Search` 调用将于 **2026 年 8 月 20 日 10:00（北京时间）** 起正式计费，区分 `Pro` 与 `Lite` 版本 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **安全要求**：API Key 必须通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 传入 Header，严禁硬编码或提交至代码仓库；业务空间专属域名仅接受同空间 API Key 调用 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **软删除**：`DELETE /memory_nodes/{id}` 为逻辑删除（`status: "delete"`），历史记录仍可通过 `GetMemoryNode` 查询，但 `ListMemory` 和 `SearchMemory` 默认不返回已删除节点。
- **多模态支持**：仅部分项目支持图片解析（`messages[].content[].type = "image_url"`），其他项目会忽略图片字段；`media_desc` 和 `multimodal_medias` 字段在响应中存在即表示已处理多模态内容。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
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
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)


