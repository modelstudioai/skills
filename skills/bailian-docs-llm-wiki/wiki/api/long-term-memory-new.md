# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类记忆的写入、检索、更新与生命周期管理。所有操作通过 RESTful API 或 `agentscope-runtime` SDK 完成，基于业务空间专属域名和 API Key 鉴权，适用于 Agent 场景下的上下文持久化与个性化能力构建。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如用户偏好、日程提醒）、`skill`（技能记忆，如工具调用流程、SOP）和 `user_profile`（结构化用户画像）三类记忆节点，类型由 `project_id` 对应的记忆规则或显式传入的 `profile_schema` 决定。
- **抽取模式**：提供 `efficient`（低延迟）与 `intelligent`（高精度）两种提取场景；`add-async` 接口支持多项目并行抽取、技能抽取及画像联合抽取，而 `add` 接口仅推荐在 `efficient` 模式下用于实时性敏感场景 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
- **多模态支持**：`messages` 中可传入 `image_url` 类型内容，但仅在启用多模态能力的项目中被解析；文本内容始终支持 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **画像模板**：通过 `CreateProfileSchema` 定义字段结构，支持动态增删改属性（`attributes_operations`），且 `plan_version`（`pro`/`lite`）控制抽取质量与计费策略 [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)。

> **注意**：文档 6（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）明确指出同步接口在 `intelligent` 模式下“可能超时”，而文档 7（[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）强调其为“主推”方式。二者存在明确的使用优先级差异，开发者应默认选用 `add-async`，仅在低延迟强实时需求且确认为 `efficient` 模式时考虑 `add`。

## 关键参数

| 参数 | 说明 | 示例值 | 必填性 |
|------|------|--------|--------|
| `user_id` | 子用户 ID，用于跨用户记忆隔离 | `"user_001"` | 所有写入/检索接口必填 |
| `memory_library_id` | 记忆库 ID，不传则使用默认库 | `"memory_library_001"` | 可选（默认库） |
| `project_id` / `project_ids` | 项目 ID，用于二级隔离；`project_ids` 最多 5 个，与 `project_id` 互斥 | `["project_001"]` | 可选（影响记忆分类与检索范围） |
| `profile_schema` | 用户画像模板 ID，传入后触发画像抽取 | `"50edf54eaa5842e891d959ae115205be"` | 仅画像抽取必填 |
| `extract_mode` | 抽取模式，`profile_only` 表示仅抽取画像 | `"profile_only"` | 条件必填（仅需画像时） |
| `plan_version` | 计费与能力版本，`pro`（支持 `min_score` 过滤、Rerank）或 `lite`（基础检索） | `"pro"` | `search` 和 `profile_schema` 相关接口可选，默认 `pro` |
| `top_k` / `min_score` | 检索参数：最大召回数（默认 10）、最小相似度阈值（仅 `plan_version=pro` 生效，默认 0.3） | `10`, `0.6` | 可选 |

## 使用方式

1. **认证准备**：获取业务空间 ID（从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)复制 API Host）和 `DASHSCOPE_API_KEY`（控制台获取），设置环境变量：
   ```bash
   export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"
   export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
   ```

2. **写入记忆**：
   - 同步写入（适合 `efficient` 模式）：调用 `/add`，响应中直接返回 `memory_nodes`；
   - 异步写入（推荐）：调用 `/add-async` 获取 `event_id`，再轮询 `/events/{event_id}` 查询状态与结果 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)。

3. **检索与管理**：
   - 语义搜索：`POST /memory_nodes/search`，传入 `messages` 和 `user_id`，按 `memory_types` 筛选（默认仅 `["observation"]`）；
   - 列表浏览：`GET /memory_nodes?user_id=xxx`，支持分页（`page_num`/`page_size`）；
   - 单条查询/更新/删除：`GET`/`PATCH`/`DELETE /memory_nodes/{id}`；
   - 技能导出：`GET /skill/export/{id}` 获取完整技能元信息（`skill_name`/`description`/`tags`）。

4. **用户画像**：
   - 创建模板：`POST /profile_schemas` 定义 `attributes`；
   - 写入画像：在 `add` 或 `add-async` 请求中传入 `profile_schema`；
   - 查询画像：`GET /profile_schemas/{id}/user_profile?user_id=xxx`（注意：首次查询可能为空，需重试）。

## 限制和注意事项

- **限流**：阿里云账号级别总计 3000 QPM；其中 `add` 接口 120 QPM，`search` 接口 300 QPM。超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **商业化时间点**：所有 `Add` 和 `Search` 调用将于 **2026 年 8 月 20 日 10:00（北京时间）** 起正式计费，`pro`/`lite` 版本区分模型质量与 Rerank 能力 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **软删除**：`DELETE /memory_nodes/{id}` 为逻辑删除（`status: "delete"`），历史仍可查询；操作不可逆，请谨慎执行。
- **多模态约束**：`image_url` 仅在配置了多模态能力的项目中被解析，其他项目将忽略图片内容。
- **画像提取延迟**：用户画像为异步过程，`GetUserProfile` 首次调用可能返回空值，需结合业务逻辑实现重试（文档 19 明确提示：“请按业务重试策略再次查询”）。

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
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)


