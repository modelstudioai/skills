# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持开发者以编程方式将对话、事件或自定义内容持久化为可检索的记忆节点，并自动抽取事实（`observation`）、技能（`skill`）及用户画像（`user_profile`）。该服务基于业务空间隔离，提供同步/异步写入、语义搜索、多类型记忆管理与画像模板定制能力，适用于构建具备上下文感知能力的智能体应用。

## 支持的模型/功能

- **记忆类型**：支持三类记忆节点：
  - `observation`（事实记忆）：如“用户每天上午11点提醒点外卖”；
  - `skill`（技能记忆）：含 `skill_name`、`skill_description` 和 `skill_tags`，用于沉淀可复用的操作流程；
  - `user_profile`（用户画像）：需配合画像模板（`profile_schema`）提取结构化属性（如年龄、职业），详见[创建画像模板](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。
- **抽取模式**：支持 `efficient`（低延迟）和 `intelligent`（高精度）两种提取场景；`intelligent` 模式下同步接口可能超时，推荐使用异步接口 [AddMemoryAsync](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。
- **多模态支持**：当项目配置支持多模态时，`messages[].content` 可包含 `image_url` 类型内容，系统将解析图片语义并参与记忆抽取。

> **注意**：文档 5 明确指出同步接口在 `intelligent` 模式下“可能超时”，而文档 6 强调异步接口“支持多项目并行抽取、技能抽取和用户画像抽取”。二者功能定位存在明确分工，**不应在 `intelligent` 场景下依赖同步接口保障稳定性**。

## 关键参数

| 参数 | 说明 | 示例值 | 必填性 |
|------|------|--------|--------|
| `user_id` | 子用户 ID，用于跨用户记忆隔离 | `"user_001"` | ✅ 所有写入/检索接口均需 |
| `project_id` / `project_ids` | 项目级二级隔离标识；`project_ids` 最多支持 5 个，与 `project_id` 互斥 | `["project_001"]` | ❌（但强烈建议设置以实现逻辑分组） |
| `profile_schema` | 画像模板 ID，触发用户画像抽取；未传则不生成画像 | `"50edf54eaa5842e891d959ae115205be"` | ⚠️ 仅当需画像时必填（见[获取用户画像](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)说明） |
| `plan_version` | 计费策略版本：`pro`（支持 `min_score` 过滤、Rerank）或 `lite`（基础检索） | `"pro"` | ❌ 默认 `pro`，但 `search` 接口需显式指定以启用高级能力 |
| `memory_types` | 检索时限定记忆类型，默认 `["observation"]` | `["observation", "skill"]` | ❌ |

## 使用方式

### 1. 准备凭证
- 获取 `DASHSCOPE_API_KEY`（`sk-` 开头）和业务空间 ID（`llm-xxxxxxxxxxxx`），详见[认证](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。
- 设置环境变量：`export DASHSCOPE_API_KEY="sk-..."`，并在请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。

### 2. 写入记忆
- **同步写入（实时反馈）**：调用 `/add`，适合 `efficient` 模式或对延迟敏感的场景。示例：
  ```bash
  curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/add' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{"user_id":"user_001","messages":[{"role":"user","content":"明天提醒我开会"}]}'
  ```
- **异步写入（高可靠）**：调用 `/add-async`，立即返回 `event_id`，再通过 `/events/{event_id}` 查询结果。适用于 `intelligent` 模式、多项目批量处理或技能/画像联合抽取。

### 3. 检索与管理
- **语义搜索**：`POST /memory_nodes/search`，传入 `messages` 作为查询向量，支持 `top_k` 和 `min_score`（`pro` 版本）。
- **列表查询**：`GET /memory_nodes?user_id=xxx`，支持分页（`page_num`/`page_size`）。
- **画像操作**：先创建模板（`POST /profile_schemas`），写入时传 `profile_schema`，再调用 `GET /profile_schemas/{id}/user_profile?user_id=xxx` 获取结果。

## 限制和注意事项

- **限流规则**（阿里云账号级别）：
  - 全部接口总计 ≤ 3000 QPM；
  - `/add` 接口 ≤ 120 QPM；
  - `/memory_nodes/search` 接口 ≤ 300 QPM。
  超限时返回 HTTP 429，需按指数退避（1s/2s/4s）重试，详见[错误码](raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **记忆生命周期**：当前生成的记忆片段与用户画像**无自动失效日期**，需自行管理生命周期（如定期清理）。
- **删除操作**：`DELETE /memory_nodes/{id}` 为软删除（`status: "delete"`），历史记录仍可查询，但不可用于检索。
- **安全要求**：API Key 具有账号级权限，**严禁硬编码或提交至代码仓库**，应使用环境变量并按应用拆分密钥，详见[认证](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)中的安全建议。

## 来源文档

- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)


