# long term memory new

长期[记忆](../concepts/memory.md)（Long Term Memory, LTM）新版本是百炼平台提供的结构化[记忆](../concepts/memory.md)管理能力，支持事实[记忆](../concepts/memory.md)（observation/[skill](../guides/skill.md)）与用户画像（user profile）两类核心数据的写入、检索、更新与生命周期管理。所有操作通过统一的 RESTful API 接口完成，基于 DashScope 网关鉴权，适用于构建具备持续上下文理解能力的智能体应用。

## 支持的模型/功能

长期记忆新版本提供两类独立但可协同的数据模型：

- **事实记忆**：包括 `observation`（用户行为/意图片段）和 `skill`（可复用的执行流程），支持同步添加（`/add`）、异步批量抽取（`/add-async`）、语义搜索（`/memory_nodes/search`）、分页列表（`/memory_nodes`）及 CRUD 操作。异步接口支持多项目并行、工具消息解析与多模态内容处理（仅限启用多模态能力的项目）[原文标题](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)。
- **用户画像**：通过预定义模板（`profile_schema`）约束属性结构，支持创建、更新、查询模板，并基于对话自动提取属性值。画像提取为异步过程，需在 `AddMemory` 或 `AddMemoryAsync` 中显式传入 `profile_schema` 才会触发 [原文标题](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)。

> **注意**：文档 6（`add-memory.md`）称“同步接口适合在 `efficient` 模式下对实时性要求较高的场景”，但文档 14（`create-schema.md`）中 `extract_scene` 参数默认值为 `efficient`，且未说明该参数是否影响事实记忆抽取。实际调用中，`extract_scene` 仅作用于用户画像模板，与事实记忆无关；事实记忆的抽取质量由 `plan_version`（`pro`/`lite`）决定，而非 `extract_scene`。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 必填 |
|------|------|------|------|------|
| `user_id` | Body / Query | string | 子用户 ID，用于跨用户记忆隔离 | 是 |
| `messages` / `custom_content` | Body | array / string | 对话消息列表或自定义文本内容，二者至少传其一 | 二选一 |
| `memory_library_id` | Body / Query | string | 记忆库 ID，不传则使用默认库 | 否 |
| `project_id` / `project_ids` | Body | string / array | 项目 ID 或 ID 列表，用于二级隔离，互斥 | 否 |
| `profile_schema` | Body | string | 用户画像模板 ID，仅画像抽取时需传入 | 条件必填 |
| `plan_version` | Body | string | 收费策略：`pro`（支持 `min_score` 过滤、Rerank）或 `lite`（基础检索） | 否，默认 `pro` |
| `top_k`, `min_score`, `memory_types` | Body | integer / number / array | 搜索控制参数，仅 `SearchMemory` 接口有效 | 否 |

## 使用方式

1. **准备凭证**：在[百炼控制台](https://bailian.console.aliyun.com)获取 `DASHSCOPE_API_KEY`，并通过环境变量或 Header 传递：`Authorization: Bearer $DASHSCOPE_API_KEY` [原文标题](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
2. **写入记忆**：
   - 实时性要求高 → 用 `POST /add`（同步，响应含抽取结果）；
   - 高吞吐/多模态/技能抽取 → 用 `POST /add-async`（异步，返回 `event_id`，再调 `GET /events/{event_id}` 查询状态）。
3. **检索记忆**：用 `POST /memory_nodes/search`，传入 `messages` 和 `user_id`，按需设置 `top_k`、`min_score`（`plan_version=pro` 时生效）。
4. **管理画像**：
   - 先调 `POST /profile_schemas` 创建模板；
   - 写入时在 `AddMemory` 中传 `profile_schema`；
   - 查询用 `GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`。
5. **调试与排障**：所有响应均含 `request_id`，错误时参考 [错误码文档](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md) 处理（如 `429` 限流需指数退避重试）。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；`/add` 接口 120 QPM；`/memory_nodes/search` 接口 300 QPM。扩容需[提交工单](https://smartservice.console.aliyun.com/service/create-ticket) [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **计费**：服务将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化，`Add` 和 `Search` 均区分 `Pro`/`Lite` 版本，详见计费说明。
- **数据持久性**：生成的记忆片段与用户画像暂无自动失效机制，需业务侧自行管理生命周期。
- **安全**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；建议按应用拆分 Key 并定期轮转。
- **异步任务**：`/add-async` 返回 `PENDING` 或 `RUNNING` 时，需轮询 `/events/{event_id}` 获取最终结果；`/get-user-profile` 首次可能为空，需按业务逻辑重试。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)


