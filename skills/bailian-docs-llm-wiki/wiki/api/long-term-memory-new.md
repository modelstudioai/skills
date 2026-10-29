# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持将对话、事件、技能和用户画像等信息持久化存储，并提供语义检索、分页查询与异步抽取能力。所有接口通过业务空间专属域名调用，需使用 `DASHSCOPE_API_KEY` 鉴权，适用于构建具备上下文感知能力的智能体应用。

## 支持的模型/功能

- **记忆类型**：支持三类结构化记忆节点：
  - `observation`（事实记忆）：从对话中抽取的用户意图、日程、偏好等事实性信息；
  - `skill`（技能记忆）：从工具调用或结构化指令中提取的可复用技能流程（含 `skill_name`、`skill_description`、`skill_tags`），可通过 [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md) 接口获取完整元数据；
  - `user_profile`（用户画像）：基于预定义模板（`profile_schema`）异步提取的用户属性，需配合 [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md) 系列接口使用。

- **抽取模式**：
  - 同步抽取（`/add`）：适合对实时性要求高、且内容较简短的场景；但文档明确提示在 `intelligent` 模式下可能超时，[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 文档推荐优先使用异步方式；
  - 异步抽取（`/add-async`）：主推方式，支持多项目并行、技能抽取与画像抽取，结果通过 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md) 获取。

> **注意**：文档 6（同步添加）与文档 5（异步添加）均指出 `extract_mode=profile_only` 仅在传入 `profile_schema` 和 `messages` 时有效，但文档 15（创建画像模板）示例未体现该约束，实际调用时须严格校验参数组合，否则画像提取将静默失败。

## 关键参数

| 参数 | 说明 | 必填 | 备注 |
|------|------|------|------|
| `user_id` | 子用户 ID，用于跨用户记忆隔离 | 是 | 所有写入/检索接口均强制要求 |
| `memory_library_id` | 记忆库 ID | 否 | 不传则使用默认记忆库；部分接口（如 `/add-async`）允许为空，但 `ListMemory` 等列表接口建议显式指定以提升性能 |
| `project_id` / `project_ids` | 项目 ID 或 ID 列表（最多 5 个） | 否 | 用于二级隔离；与 `custom_content` 互斥；决定抽取哪类记忆（`observation` 或 `skill`） |
| `profile_schema` | 画像模板 ID | 否（画像抽取必需） | 仅当需触发用户画像抽取时传入；未传则不执行画像任务 |
| `plan_version` | 计费计划：`pro` 或 `lite` | 否（默认 `pro`） | 影响 `SearchMemory` 的 `min_score` 过滤能力（仅 `pro` 生效）及 `AddMemory` 的抽取模型质量；[计费说明](../../raw/application-user-guide/agent-context/memory-library-overview/integration-overview/billing.md) 明确其商业生效时间为 2026 年 8 月 20 日 |
| `min_score` | 检索最小分数阈值 | 否（默认 `0.3`） | 仅 `plan_version=pro` 时生效；低于该值的结果被过滤 |

## 使用方式

1. **环境准备**：
   - 设置环境变量：`export DASHSCOPE_API_KEY="sk-..."` 和 `export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`（末尾无 `/`）；
   - `{WorkspaceId}` 从控制台 [业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace) 页面的 **API Host** 列复制，详见 [获取业务空间专属域名](../../raw/application-api-reference/long-term-memory-new/api-overview.md)。

2. **核心流程**：
   - **写入**：优先使用 `POST /add-async` 提交抽取任务，获取 `event_id`；再轮询 `GET /events/{event_id}` 直至 `status=SUCCEEDED`；
   - **检索**：使用 `POST /memory_nodes/search` 进行语义搜索，支持 `top_k`、`memory_types` 等筛选；
   - **管理**：通过 `GET /memory_nodes` 分页列出、`GET /memory_nodes/{id}` 查看详情、`PATCH /memory_nodes/{id}` 更新、`DELETE /memory_nodes/{id}` 删除；
   - **画像**：先调用 `POST /profile_schemas` 创建模板，再在 `AddMemory` 中传 `profile_schema` 触发抽取，最后用 `GET /profile_schemas/{id}/user_profile?user_id=...` 查询结果。

3. **SDK 调用**（Python 示例）：
   ```python
   from agentscope_runtime.tools.modelstudio_memory import AddMemoryAsync, SearchMemory
   # 异步写入
   await AddMemoryAsync().arun(AddMemoryInput(user_id="u1", messages=[...], project_ids=["p1"]))
   # 语义搜索
   result = await SearchMemory().arun(SearchMemoryInput(user_id="u1", messages=[{"role":"user","content":"明天提醒我？"}], top_k=5))
   ```

## 限制和注意事项

- **限流策略**：阿里云账号级别全局限流，`add` 接口 120 QPM，`search` 接口 300 QPM，总计不超过 3000 QPM；超出时返回 HTTP 429，需按指数退避（1s/2s/4s）重试，详见 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **计费变更**：`Add` 和 `Search` 接口将于 **2026 年 8 月 20 日** 正式区分 `Pro` 与 `Lite` 计费版本，当前为免费公测期；`Pro` 版本支持更高质量抽取与 Rerank，`Lite` 版本不支持 `min_score` 过滤，开发者应提前评估策略迁移成本。
- **关键约束**：
  - `custom_content` 与 `project_ids` / `project_id` 互斥，不可同时传入；
  - `skill_name`、`skill_description`、`skill_tags` 在 `custom_content` 场景下为条件必填（见 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）；
  - 删除操作不可逆，调用 `DELETE /memory_nodes/{id}` 前务必确认；
  - 用户画像提取为异步过程，首次 `GetUserProfile` 可能返回空值，需按业务逻辑重试（见 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）。
- **安全要求**：API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库；建议为不同应用分配独立 API Key 并定期轮转。

## 来源文档

- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
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
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)


