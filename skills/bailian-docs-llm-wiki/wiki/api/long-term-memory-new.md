# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持开发者以编程方式写入、检索、更新和删除用户级记忆节点，并可同步抽取事实记忆（observation）、技能记忆（skill）及用户画像（user profile）。所有操作基于业务空间隔离，通过统一 API 网关提供 HTTPS 接口，兼容同步与异步两种写入模式。该能力已于 2024 年全面上线，将于 2026 年 8 月 20 日起正式商业化计费。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如“用户明天要出差”）、`skill`（技能记忆，如“会议纪要整理流程”）两类核心记忆节点；传入 `profile_schema` 时可额外触发用户画像抽取。
- **抽取模式**：
  - `efficient`（默认）：低延迟、轻量级抽取，适用于实时性要求高的场景；
  - `intelligent`：高精度多轮推理抽取，可能超时，需配合异步接口使用。
- **多模态支持**：当项目配置支持多模态能力时，`messages[].content` 中的 `image_url` 可被解析并参与记忆抽取；否则图片信息将被忽略 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
- **画像模板驱动**：用户画像非固定字段，由开发者通过 `CreateProfileSchema` 定义属性（如“年龄”“爱好”），抽取结果严格遵循模板结构 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。

> **注意**：文档中多次出现 `extract_scene` 参数（见 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md) 和 [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)），但其在 `AddMemory` 同步接口的参数列表中未被声明为合法字段——实际生效仅依赖画像模板自身的 `extract_scene` 配置，调用方无需在 Add 请求中重复指定。

## 关键参数

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `user_id` | Query / Body | string | **必填**，子用户 ID，用于跨用户记忆隔离；所有读写接口均需提供。 |
| `memory_library_id` | Query / Body | string | 可选，指定记忆库；不传则使用默认库。 |
| `project_id` / `project_ids` | Body | string / string[] | 可选，用于二级隔离（如按 Agent 或 Session 分组）；`project_ids` 最多 5 个，与 `project_id` 互斥。 |
| `profile_schema` | Body | string | 可选，画像模板 ID；传入后触发画像抽取（需搭配 `messages`）。 |
| `plan_version` | Body (Search) / Body (Schema) | string | 搜索时控制是否启用 `min_score` 过滤（`pro` 生效，`lite` 忽略）；画像模板中控制收费策略。 |
| `min_score` | Body (Search) | number | 可选，默认 `0.3`；仅 `plan_version=pro` 时生效，用于过滤低相关性结果 [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)。 |

## 使用方式

1. **认证准备**：  
   设置环境变量 `DASHSCOPE_API_KEY` 和 `MEMORY_SERVICE_ENDPOINT`（格式为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`），其中 `{WorkspaceId}` 从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面复制 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。

2. **写入记忆**：  
   - **同步写入**（`/add`）：适合 `efficient` 场景，响应中直接返回 `memory_nodes`；不推荐在 `intelligent` 模式下使用，易超时 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。  
   - **异步写入**（`/add-async`）：推荐主用方式，立即返回 `event_id`，后续通过 `/events/{event_id}` 轮询状态；支持多项目并行、技能抽取与画像联合抽取 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

3. **检索与管理**：  
   - 检索：使用 `POST /memory_nodes/search`，传入 `messages` 和 `user_id`，支持 `top_k`、`memory_types` 等筛选；默认只查 `observation`，查 `skill` 需显式指定。  
   - 查询单条：`GET /memory_nodes/{memory_node_id}` 获取完整节点详情；`GET /skill/export/{memory_node_id}` 专用于 skill 类型，返回 `skill_name`/`skill_description` 等字段。  
   - 用户画像：先创建模板 → 写入时传 `profile_schema` → 调用 `GET /profile_schemas/{id}/user_profile?user_id=xxx` 获取结果；首次查询可能为空，需重试 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。

## 限制和注意事项

- **限流规则**（阿里云账号级别）：  
  - 全部接口总计 ≤ 3000 QPM；  
  - `add` 接口 ≤ 120 QPM；  
  - `search` 接口 ≤ 300 QPM；  
  超限返回 HTTP 429，建议采用指数退避重试（1s/2s/4s）[错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。

- **软删除机制**：`DELETE /memory_nodes/{id}` 为逻辑删除，`status` 置为 `delete`，仍可通过 `ListMemory` 或 `GetMemoryNode` 查询历史记录，但 `SearchMemory` 默认不返回已删除节点。

- **画像提取延迟**：画像抽取为异步过程，`AddMemory` 返回成功不代表画像已就绪；`GetUserProfile` 首次调用可能返回空值，需按业务逻辑重试 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。

- **商业化时间点**：所有 `Add` 和 `Search` 调用自 **2026 年 8 月 20 日 10:00（北京时间）** 起区分 `Pro`/`Lite` 版本计费，`Pro` 支持 Rerank 与 `min_score` 过滤，`Lite` 仅基础检索 [长期记忆API](../../raw/application-user-guide/agent-context/memory-library-overview/long-term-memory-2-0.md)。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)


