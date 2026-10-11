# long term memory new

长期记忆（Long Term Memory）是百炼平台提供的结构化记忆管理能力，支持事实记忆（Observation/Skill）与用户画像（Profile）两类核心数据的写入、检索、更新与管理。所有操作通过统一的 RESTful API 提供，基于 DashScope 网关鉴权，适用于构建具备上下文感知与个性化能力的智能体应用。该能力将于 2026 年 8 月 20 日起正式商业化计费，当前处于公测阶段。

## 支持的模型/功能

长期记忆提供两类独立但可协同的数据模型：

- **事实记忆**：用于持久化用户行为、对话摘要、技能流程等结构化事实。支持三种子类型：
  - `observation`：通用场景下的事件/意图抽取（如“每天11点提醒点外卖”）；
  - `skill`：可复用的工具型能力描述，含 `skill_name`、`skill_description` 和 `skill_tags` 字段，需通过 [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md) 接口获取完整元信息；
  - `custom_observation` / `custom_skill`：由 `custom_content` 直接写入的非抽取型记忆。
- **用户画像**：基于预定义模板（`profile_schema`）对用户属性进行结构化建模。模板支持动态增删字段（`attributes_operations`），并区分 `efficient`（低延迟）与 `intelligent`（高精度）提取场景。画像提取为异步过程，需调用 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询结果。

> **注意**：文档 6（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）称同步接口在 `intelligent` 模式下“可能超时”，而文档 17（[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)）将 `extract_scene` 默认值设为 `efficient`，且未说明 `intelligent` 模式的同步兼容性。实际使用中，涉及画像提取的写入应优先选用 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)，以避免超时风险。

## 关键参数

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `user_id` | Query / Body | string | **必填**，子用户隔离标识，所有读写操作均以此为作用域边界 |
| `memory_library_id` | Query / Body | string | 可选，指定记忆库；不传则使用默认库 |
| `project_id` / `project_ids` | Query / Body | string / array | 可选，用于二级隔离（如按会话/任务分组），`project_ids` 最多支持 5 个 |
| `plan_version` | Body | string | 计费策略，`pro`（支持 `min_score` 过滤、Rerank）或 `lite`（基础检索），默认 `pro`；`pro` 亦为画像模板的默认 `plan_version`（见[列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)） |
| `extract_mode` | Body | string | 仅 `AddMemory`/`AddMemoryAsync` 支持，`profile_only` 表示跳过事实抽取，仅触发画像提取 |
| `min_score` | Body | number | 仅 `SearchMemory` 在 `plan_version=pro` 时生效，默认 `0.3`，低于此阈值的结果被过滤 |

## 使用方式

1. **鉴权准备**：通过百炼控制台获取 `DASHSCOPE_API_KEY`，并在请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`（详见[鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）；
2. **写入记忆**：
   - 实时性要求高且内容简单 → 用 `POST /add`（同步）；
   - 需多项目并行、含 Skill 或 Profile 提取 → 用 `POST /add-async`（异步），再通过 `GET /events/{event_id}` 轮询状态；
3. **检索记忆**：`POST /memory_nodes/search`，传入 `messages` 作为语义查询向量，支持 `top_k` 和 `min_score` 控制召回质量；
4. **管理画像**：
   - 先调用 `POST /profile_schemas` 创建模板；
   - 写入时在 `AddMemory` 请求中传入 `profile_schema` ID；
   - 查询时用 `GET /profile_schemas/{schema_id}/user_profile?user_id=xxx` 获取结构化属性；
5. **辅助操作**：`GET /memory_nodes` 分页列表、`GET /memory_nodes/{id}` 查单条、`PATCH /memory_nodes/{id}` 更新、`DELETE /memory_nodes/{id}` 删除。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口 120 QPM，`search` 接口 300 QPM（见[长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）；
- **异步任务**：`add-async` 返回 `status: PENDING` 后，需主动轮询 `GET /events/{event_id}`，`SUCCEEDED` 后 `result` 字段才包含有效记忆节点；
- **画像提取延迟**：`GetUserProfile` 首次调用可能返回空值，因画像提取为后台异步任务，需按业务逻辑重试（见[获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）；
- **安全规范**：API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库；
- **计费提示**：所有 `add` 和 `search` 调用均区分 `pro`/`lite` 版本，`plan_version` 参数直接影响计费项与功能可用性，务必显式指定。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [API 概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [鉴权](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [事实记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)


