# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类数据的写入、检索与生命周期管理。所有操作通过 RESTful API 或 `agentscope-runtime` SDK 完成，需配合业务空间专属域名与 `DASHSCOPE_API_KEY` 鉴权。该服务将于 2026 年 8 月 20 日起正式商业化计费，当前处于公测阶段。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如用户偏好、日程）、`skill`（技能记忆，如工具调用流程）两类结构化记忆节点；通过 `profile_schema` 可额外抽取 `user_profile`（用户画像）。
- **抽取能力**：
  - 同步抽取：`AddMemory` 接口在响应中直接返回结果，适用于实时性要求高、内容较短的场景 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)；
  - 异步抽取：`AddMemoryAsync` 提交后台任务，支持多项目并行、多模态内容（文本+图片）解析及技能/画像联合抽取 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)；
- **检索能力**：`SearchMemory` 基于语义相似度召回，支持按 `memory_types`（默认仅 `["observation"]`）、`top_k`、`min_score`（仅 `plan_version=pro` 生效）筛选，返回带 `score` 的记忆节点列表 [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)；
- **画像管理**：提供完整的画像模板生命周期 API（创建、更新、列表、详情）及用户画像获取能力，画像提取依赖 `AddMemory`/`AddMemoryAsync` 调用时传入 `profile_schema` 参数 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)。

> **注意**：文档 15（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）明确指出“当前主推[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)”，而文档 1 中接口概览未强调此推荐策略，存在信息滞后。开发者应优先采用 `AddMemoryAsync` 以保障稳定性与多模态兼容性。

## 关键参数

- **认证参数**：必须在请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，且 `DASHSCOPE_API_KEY` 必须属于目标业务空间 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **路由参数**：
  - `{WorkspaceId}`：业务空间 ID，需从控制台“业务空间管理”页面复制 API Host 列内容（格式如 `llm-xxxxxxxxxxxx`），拼接至 Base URL `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/`。
- **核心业务参数**：
  - `user_id`：必填，用于跨用户记忆隔离；
  - `project_id` / `project_ids`：用于二级隔离（如按 Agent 或会话分组），与 `custom_content` 互斥；
  - `profile_schema`：传入画像模板 ID 以触发用户画像抽取；
  - `memory_types`：`SearchMemory` 中指定检索的记忆类型数组，可选 `["observation", "skill"]`；
  - `plan_version`：`SearchMemory` 和画像模板 API 中指定计费策略，值为 `"pro"`（支持 `min_score` 过滤、高级抽取）或 `"lite"`（基础能力），不区分大小写，传入非法值将报错。

## 使用方式

1. **初始化配置**：
   - 设置环境变量：`export DASHSCOPE_API_KEY="sk-..."` 和 `export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`（末尾无 `/`）；
2. **写入记忆**：
   - 同步：调用 `POST /add`，传入 `messages` 或 `custom_content` + `user_id`；
   - 异步：调用 `POST /add-async`，获取 `event_id` 后轮询 `GET /events/{event_id}` 查询状态与结果 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)；
3. **检索与管理**：
   - 检索：`POST /memory_nodes/search`，构造 `messages` 查询向量，指定 `user_id` 和 `memory_types`；
   - 列表：`GET /memory_nodes?user_id=xxx&page_size=10`；
   - 单查/更新/删除：分别使用 `GET /memory_nodes/{id}`、`PATCH /memory_nodes/{id}`、`DELETE /memory_nodes/{id}`；
4. **用户画像工作流**：
   - 创建模板：`POST /profile_schemas` 定义属性；
   - 写入时触发：在 `AddMemory` 或 `AddMemoryAsync` 请求中传入 `profile_schema`；
   - 查询结果：`GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`（注意首次查询可能为空，需重试）。

## 限制和注意事项

- **限流规则**（阿里云账号级别）：
  - 全部接口总计 ≤ 3000 QPM；
  - `add` 类接口（含同步/异步）≤ 120 QPM；
  - `search` 接口 ≤ 300 QPM；
  - 超限返回 HTTP 429，建议采用指数退避重试（1s/2s/4s）[错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **关键约束**：
  - `custom_content` 与 `project_id`/`project_ids` 互斥，不可同时传入；
  - `skill_name`、`skill_description`、`skill_tags` 在 skill 类型写入/更新时必须同时提供；
  - `extract_mode=profile_only` 时，`profile_schema` 和 `messages` 均为必填；
  - 删除操作不可逆，务必确认 `memory_node_id` 正确。
- **行为差异**：
  - `AddMemory` 在 `intelligent` 模式下可能超时，文档 15 明确建议优先使用异步接口；
  - `SearchMemory` 的 `min_score` 参数仅在 `plan_version="pro"` 时生效，`lite` 版本忽略该字段；
  - 画像模板的 `plan_version` 更新仅影响新写入的记忆，历史数据不受影响 [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)


