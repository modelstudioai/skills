# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类记忆的写入、检索、更新与生命周期管理。所有操作均通过 RESTful API 或 `agentscope-runtime` SDK 完成，需使用业务空间专属域名和 `DASHSCOPE_API_KEY` 鉴权。该服务将于 2026 年 8 月 20 日起正式商业化计费，Add 和 Search 接口区分 `pro` 与 `lite` 计划版本。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如用户偏好、日程提醒）、`skill`（技能记忆，如会议纪要整理流程）两类结构化记忆节点；通过 `profile_schema` 可额外抽取用户画像 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。
- **抽取能力**：
  - 同步抽取（`/add`）适用于实时性要求高的场景，但 `intelligent` 模式下可能超时；
  - 异步抽取（`/add-async`）支持多项目并行、技能抽取及画像联合提取，推荐用于生产环境 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **检索能力**：`/memory_nodes/search` 支持语义相似度检索，可按 `memory_types`（默认仅 `["observation"]`）筛选，并通过 `plan_version` 控制是否启用 `min_score` 过滤 [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)。
- **多模态支持**：当项目配置支持多模态时，`messages` 中的 `image_url` 类型内容可参与抽取；否则图片信息被忽略。

> **注意**：文档 6（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）称同步接口“在 `intelligent` 模式下可能超时”，而文档 7（[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）未明确说明其是否支持 `intelligent` 模式。实际使用中，`intelligent` 模式应仅与异步接口配合，避免同步调用失败。

## 关键参数

| 参数 | 说明 | 示例值 | 必填 |
|------|------|--------|------|
| `user_id` | 子用户 ID，用于记忆隔离 | `"user_001"` | ✅ |
| `project_id` / `project_ids` | 项目 ID（单个或数组），决定记忆抽取规则与类型 | `["project_001"]` | ⚠️（二选一，与 `custom_content` 互斥） |
| `profile_schema` | 用户画像模板 ID，传入后触发画像抽取 | `"50edf54eaa5842e891d959ae115205be"` | ❌（仅需画像时必填） |
| `extract_mode` | 抽取模式，`"profile_only"` 表示仅抽取画像 | `"profile_only"` | ❌（仅 `profile_schema` + `messages` 时有效） |
| `plan_version` | 计费计划，`"pro"`（支持 `min_score` 过滤）或 `"lite"`（基础检索） | `"pro"` | ❌（默认 `"pro"`） |
| `top_k` / `min_score` | 检索控制：最大召回数（默认 `10`）、最小分数阈值（仅 `pro` 生效，默认 `0.3`） | `5`, `0.5` | ❌ |

## 使用方式

1. **准备凭证**：获取业务空间 ID（从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)复制 API Host）和 `DASHSCOPE_API_KEY`（[获取 API Key](../../raw/model-api-reference/preparations/get-api-key.md)），设置环境变量：
   ```bash
   export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"
   export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
   ```

2. **写入记忆**：
   - 同步写入（适合简单事实）：调用 `/add`，传 `messages` 或 `custom_content`；
   - 异步写入（推荐）：调用 `/add-async`，获取 `event_id` 后轮询 `/events/{event_id}` 查询结果 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)。

3. **检索与管理**：
   - 语义搜索：`POST /memory_nodes/search`，传 `messages` + `user_id`；
   - 列表查看：`GET /memory_nodes?user_id=xxx`；
   - 单条查询/更新/删除：`GET`/`PATCH`/`DELETE /memory_nodes/{id}`；
   - 技能导出：`GET /skill/export/{id}`（仅限 `skill` 类型）。

4. **用户画像流程**：
   - 创建模板 → 调用 `/add` 时传 `profile_schema` → 调用 `/profile_schemas/{id}/user_profile?user_id=xxx` 获取结果。

## 限制和注意事项

- **限流**：全接口总计 ≤ 3000 QPM（阿里云账号级）；其中 `/add` ≤ 120 QPM，`/search` ≤ 300 QPM。超限返回 HTTP 429，需按指数退避重试（1s/2s/4s）[错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **时效性**：用户画像提取为异步过程，首次调用 `/user_profile` 可能返回空值，需业务侧重试 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。
- **数据持久性**：当前生成的记忆片段与用户画像无自动失效机制，长期存储需自行管理生命周期。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；建议为不同应用分配独立 Key 并定期轮转 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- **兼容性**：`/add-async` 不支持与 `custom_content` 同时传入 `project_ids`；`/update-memory` 对 `skill` 类型节点必须同时提供 `skill_name`、`skill_description` 和 `skill_tags`。

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
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)


