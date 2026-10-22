# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（Observation/Skill）与用户画像（Profile）两类核心能力。通过 API 或 SDK 可以实现记忆的写入、异步抽取、语义检索、分页查询、更新删除及画像模板全生命周期管理。所有接口基于业务空间专属域名调用，需使用对应空间的 API Key 鉴权。

## 支持的模型/功能

- **事实记忆**：支持 `observation`（对话中提取的用户意图/事件）和 `skill`（可复用的工具型行为）两类记忆节点。抽取能力分为 `efficient`（低延迟）与 `intelligent`（高精度）两种场景模式，由 `extract_scene` 参数控制。
- **用户画像**：通过预定义的 `profile_schema` 模板驱动结构化属性抽取（如年龄、职业、爱好），支持 `pro`/`lite` 计费版本，不同版本影响抽取深度与 Rerank 能力。
- **多模态支持**：`messages` 中可传入 `image_url` 类型内容，但仅在启用多模态能力的项目中被解析；文本内容始终支持。
- **异步处理**：`/add-async` 接口支持并行任务提交与状态轮询，适用于批量导入或高负载场景，详见 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

> **注意**：文档 5（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）称同步 `/add` 接口“在 `intelligent` 模式下可能超时”，而文档 6（[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）明确指出异步接口“支持多项目并行抽取、技能抽取和用户画像抽取”。二者功能边界清晰，**不推荐在 `intelligent` 场景下使用同步 `/add`**，应优先选用 `/add-async`。

## 关键参数

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `user_id` | Body / Query | string | **必填**，用于记忆隔离的核心标识符，所有读写操作均需指定 |
| `memory_library_id` | Body / Query | string | 非必填，指定记忆库 ID；不传则使用默认库 |
| `project_id` / `project_ids` | Body / Query | string / array | 非必填，用于二级隔离；`project_ids` 最多 5 个，与 `project_id` 互斥 |
| `profile_schema` | Body | string | 非必填，传入后触发用户画像抽取；必须与已创建的模板 ID 一致 |
| `extract_mode` | Body | string | 非必填，值为 `profile_only` 时仅执行画像抽取（需同时传 `profile_schema` 和 `messages`） |
| `plan_version` | Body / Query | string | 非必填，`pro`（默认）或 `lite`，影响搜索过滤（`min_score`）、Rerank 及画像抽取质量；详见 [计费说明](../../raw/application-user-guide/agent-context/memory-library-overview/integration-overview/billing.md) |
| `top_k` / `min_score` | Body | integer / number | `SearchMemory` 专用：`top_k` 控制召回数量（默认 10）；`min_score` 仅 `plan_version=pro` 时生效（默认 0.3） |

## 使用方式

1. **准备凭证**：获取业务空间 ID（从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)复制 API Host）和 `DASHSCOPE_API_KEY`（控制台获取），设置环境变量：
   ```bash
   export DASHSCOPE_API_KEY="sk-..."
   export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"
   ```
2. **写入记忆**：
   - 实时性要求高且内容简单 → 用同步 `/add`（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）
   - 需技能抽取、画像抽取或批量处理 → 用 `/add-async` + `/events/{event_id}` 轮询（[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）
3. **检索记忆**：调用 `/memory_nodes/search`，传入 `user_id` 和 `messages`（查询语句），按需设置 `top_k`、`min_score` 和 `plan_version`。
4. **管理用户画像**：
   - 创建模板：`POST /profile_schemas`（[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)）
   - 写入时关联：`AddMemory` 请求中传 `profile_schema`
   - 查询结果：`GET /profile_schemas/{schema_id}/user_profile?user_id=...`（[获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）
5. **SDK 快速接入**：使用 `agentscope-runtime` 工具包（如 `AddMemory`, `SearchMemory`, `GetUserProfile`），示例见各接口文档的 Python 片段。

## 限制和注意事项

- **限流规则**（阿里云账号级别）：
  - 全部接口总计 ≤ 3000 QPM
  - `/add` 接口 ≤ 120 QPM
  - `/memory_nodes/search` 接口 ≤ 300 QPM  
  超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试，详见 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **计费时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化计费，Add/Search 调用区分 `pro`/`lite` 版本，策略差异直接影响功能可用性。
- **[异步任务](../concepts/asynchronous-task.md)状态**：`/add-async` 返回 `status=PENDING` 或 `RUNNING` 时，需主动轮询 `/events/{event_id}` 获取最终结果；`status=UNRECORDED` 表示任务未被记录，应检查参数合法性。
- **画像提取延迟**：`GetUserProfile` 首次调用可能返回空值，因画像抽取为异步过程；需按业务逻辑重试，且**必须确保 `AddMemory` 调用时传入了相同的 `profile_schema`**（[获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）。
- **安全要求**：API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转。

## 来源文档

- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)


