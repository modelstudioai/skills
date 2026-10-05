# long term memory new

[长期记忆](../concepts/memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（Observation/Skill）与用户画像（Profile）两类核心能力。通过统一 API 接口，开发者可编程式写入、检索、更新和删除记忆，并支持多模态内容解析、异步抽取、语义搜索与画像建模。服务基于 DashScope 网关提供，所有调用需通过 API Key 鉴权。

## 支持的模型/功能

- **事实记忆**：支持两种类型  
  - `observation`：从对话中自动提取用户行为、意图、计划等客观事实（如“每天上午11点提醒我点外卖”），由 `AddMemory` 或 `AddMemoryAsync` 接口触发；  
  - `skill`：结构化封装可复用的操作流程（含 `skill_name`、`skill_description`、`skill_tags`），需在 `AddMemoryAsync` 中显式传入相关字段，或通过 `/skill/export/{id}` 查询详情 [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)。  
- **用户画像**：基于预定义模板（`profile_schema`）抽取用户属性（如年龄、职业、爱好）。需先调用 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)，再在 `AddMemory` 或 `AddMemoryAsync` 中传入 `profile_schema` 参数触发抽取，最终通过 `GetUserProfile` 获取结果。  
- **多模态支持**：`messages[].content` 可包含 `text` 和 `image_url` 类型内容，但仅限启用多模态能力的项目解析图片；其他项目将忽略图片字段 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。

> **注意**：文档 5（同步 AddMemory）称其“在 `intelligent` 模式下可能超时”，而文档 6（异步 AddMemoryAsync）明确支持 `intelligent` 场景下的技能与画像抽取。实际生产环境应优先使用异步接口，避免同步超时风险。

## 关键参数

| 参数 | 说明 | 必填性 | 备注 |
|------|------|--------|------|
| `user_id` | 子用户唯一标识，用于记忆隔离 | 是（所有写入/检索接口） | 同一 `user_id` 下的记忆默认互通 |
| `memory_library_id` | 记忆库 ID | 否 | 不传则使用默认库；所有接口均支持该参数实现跨库操作 |
| `project_id` / `project_ids` | 项目 ID（单个或数组） | 否 | 用于二级隔离；`project_ids` 最多 5 个，与 `custom_content` 互斥 |
| `profile_schema` | 用户画像模板 ID | 条件必填 | 仅当需触发画像抽取时必须传入，否则不生效 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) |
| `extract_mode` | 抽取模式 | 否 | `profile_only` 表示仅抽取画像，此时 `messages` 和 `profile_schema` 均为必填 |
| `plan_version` | 计费策略版本 | 否（默认 `pro`） | `search` 接口：`pro` 支持 `min_score` 过滤；`lite` 忽略该参数。`profile_schema` 创建/更新时也支持该字段 |

## 使用方式

1. **鉴权准备**：获取 `DASHSCOPE_API_KEY` 并通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头传递 [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。  
2. **写入记忆**：  
   - 实时性要求高且内容简单 → 使用 `POST /add`（同步）；  
   - 需支持技能抽取、多项目并行、画像联合抽取 → 使用 `POST /add-async`（异步），再通过 `GET /events/{event_id}` 轮询状态 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。  
3. **检索记忆**：  
   - 精确匹配或分页浏览 → `GET /memory_nodes?user_id=xxx`；  
   - 语义相似度搜索 → `POST /memory_nodes/search`，传入 `messages` 作为查询向量，支持 `top_k` 和 `min_score`（`plan_version=pro` 时生效）。  
4. **管理画像**：  
   - 定义字段 → `POST /profile_schemas`；  
   - 提取数据 → 在 `AddMemory` 中传 `profile_schema`；  
   - 查询结果 → `GET /profile_schemas/{id}/user_profile?user_id=xxx`（注意：首次查询可能为空，需重试）。

## 限制和注意事项

- **限流规则**（阿里云账号级别）：  
  - 全部接口总计 ≤ 3000 QPM；  
  - `add` 接口 ≤ 120 QPM；  
  - `search` 接口 ≤ 300 QPM。  
  超限返回 HTTP 429，建议采用指数退避（1s/2s/4s）重试 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。  
- **计费时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化，Add/Search 调用按 `Pro`/`Lite` 版本计费，详见[计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **异步任务状态**：`AddMemoryAsync` 返回 `status: PENDING` 或 `RUNNING` 时，必须轮询 `GetEvent` 接口获取最终结果；`SUCCEEDED` 状态下 `result` 字段才包含有效记忆节点。  
- **删除不可逆**：`DELETE /memory_nodes/{id}` 操作无回收机制，调用前须严格校验 `memory_node_id`。  
- **画像提取延迟**：`GetUserProfile` 返回空值时，需确认：① `AddMemory` 是否传入了正确的 `profile_schema`；② 是否已等待足够时间（异步抽取存在延迟）。

## 来源文档

- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
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
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)


