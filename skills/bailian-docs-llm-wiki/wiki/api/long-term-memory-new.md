# long term memory new

[长期记忆](../concepts/long-term-memory.md)（记忆库）是百炼平台提供的结构化记忆存储与检索服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类数据的写入、查询、更新与管理。所有操作均通过 HTTPS API 完成，需使用业务空间专属域名与 `DASHSCOPE_API_KEY` 鉴权。服务采用统一的 RESTful 接口设计，兼容同步与异步调用模式，并提供 SDK 封装（如 `agentscope-runtime`）简化集成。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如用户偏好、日程提醒）、`skill`（技能记忆，如工具调用流程）两类结构化记忆节点；通过 `profile_schema` 可额外抽取用户画像。
- **抽取能力**：
  - 同步抽取（`/add`）适用于实时性要求高、内容较短的场景，但 `intelligent` 模式下存在超时风险 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)；
  - 异步抽取（`/add-async`）推荐用于多项目并行、含工具调用或多模态内容的复杂对话，结果通过 `/events/{event_id}` 查询 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **用户画像**：需先创建画像模板（`CreateProfileSchema`），再在 `AddMemory` 或 `AddMemoryAsync` 中传入 `profile_schema` ID 触发抽取；画像提取为异步过程，首次查询可能为空，需重试 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。
- **多模态支持**：仅当项目配置支持多模态能力时，`messages[].content` 中的 `image_url` 才会被解析；否则图片信息被忽略。

> **注意**：文档中多次提及 `extract_scene` 参数（`efficient` / `intelligent`），但其实际生效逻辑未在接口参数定义中明确体现。例如 `CreateProfileSchema` 支持该字段，而 `AddMemory` 和 `SearchMemory` 的请求参数列表中均未包含它。建议以 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md) 文档为准，其他接口若需控制抽取精度，应优先通过 `plan_version` 和 `project_id` 关联的规则间接影响。

## 关键参数

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `user_id` | Body / Query | string | **必填**，子用户标识，用于跨用户记忆隔离 |
| `memory_library_id` | Body / Query | string | 记忆库 ID，不传则使用默认库 |
| `project_id` / `project_ids` | Body | string / array | 项目 ID（单个或最多 5 个），用于二级隔离与记忆类型路由（`observation`/`skill`） |
| `profile_schema` | Body | string | 用户画像模板 ID，传入后触发画像抽取 |
| `top_k`, `min_score`, `memory_types` | Body | integer / number / array | `SearchMemory` 专用：召回数量、最小相似度阈值（仅 `plan_version=pro` 生效）、记忆类型过滤 |
| `plan_version` | Body | string | `pro`（启用 Rerank、`min_score` 过滤）或 `lite`（基础检索），大小写不敏感，默认 `pro` |

## 使用方式

1. **准备凭证**：在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)获取 `DASHSCOPE_API_KEY`，并在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面复制 `API Host`（提取 `{WorkspaceId}`）。
2. **环境配置**（推荐）：
   ```bash
   export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
   export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"
   ```
3. **核心流程**：
   - **写入**：调用 `POST /add`（同步）或 `POST /add-async`（异步）。若需画像，务必传 `profile_schema`；若需技能记忆，确保 `messages` 包含 `tool_calls` 或显式指定 `skill_name` 等字段。
   - **检索**：调用 `POST /memory_nodes/search`，传入 `user_id` 和 `messages`（作为查询语义），按需设置 `top_k`、`min_score`。
   - **管理**：`GET /memory_nodes` 分页查全部记忆；`GET /memory_nodes/{id}` 查单个详情；`PATCH /memory_nodes/{id}` 更新内容；`DELETE /memory_nodes/{id}` 删除（软删除，状态为 `delete`）。
   - **画像**：`POST /profile_schemas` 创建模板 → `AddMemory` 传 `profile_schema` → `GET /profile_schemas/{id}/user_profile?user_id=xxx` 获取结果。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口 120 QPM，`search` 接口 300 QPM。超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **计费**：服务将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化，`Add` 和 `Search` 调用区分 `Pro` 与 `Lite` 版本，影响抽取质量与 Rerank 能力 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **安全**：API Key 具有账号级权限，严禁硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **数据持久性**：生成的记忆片段与用户画像暂无自动失效机制，需自行管理生命周期。
- **异步任务**：`/add-async` 返回 `event_id` 后，需轮询 `/events/{event_id}` 获取结果；`status` 为 `PENDING` 或 `RUNNING` 时需等待 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)。

## 来源文档

- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)


