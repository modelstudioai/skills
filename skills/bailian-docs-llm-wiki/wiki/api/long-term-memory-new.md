# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类数据的写入、检索与生命周期管理。所有操作通过 RESTful API 或 `agentscope-runtime` SDK 完成，采用业务空间专属域名与 API Key 鉴权。记忆数据默认持久化且无自动过期机制，适用于构建具备上下文延续能力的智能体应用。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如用户偏好、日程提醒）、`skill`（技能记忆，如工具调用流程、SOP）和 `user_profile`（结构化用户画像）三类节点，类型由 `project_id` 对应的记忆规则或显式参数决定。
- **抽取模式**：提供 `efficient`（低延迟，适合实时场景）与 `intelligent`（高精度，支持多步推理）两种提取场景；`extract_mode=profile_only` 可仅触发画像抽取（需配合 `profile_schema`）。
- **多模态支持**：当项目配置支持多模态时，`messages` 中的 `image_url` 会被解析并参与记忆抽取；否则图片内容被忽略 [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)。
- **异步能力**：`AddMemoryAsync` 支持并行提交多个项目（最多 5 个 `project_ids`）的记忆抽取任务，并通过 `GetEvent` 查询状态与结果，是生产环境推荐方式 [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

> **注意**：文档 4（同步 AddMemory）称“在 `intelligent` 模式下可能超时”，而文档 5（异步 AddMemoryAsync）明确支持 `intelligent` 场景且无超时风险。因此，对 `intelligent` 模式下的记忆写入，**必须使用异步接口**，同步接口仅适用于 `efficient` 模式下的轻量、实时写入。

## 关键参数

| 参数 | 说明 | 示例值 | 备注 |
|------|------|--------|------|
| `user_id` | 必填，子用户 ID，用于跨用户记忆隔离 | `"user_001"` | 所有读写接口均需传入 |
| `project_id` / `project_ids` | 记忆二级隔离标识；`project_ids` 最多 5 个，与 `custom_content` 互斥 | `["project_001"]` | 决定记忆类型（`observation`/`skill`）及抽取规则 |
| `profile_schema` | 用户画像模板 ID；传入后触发画像抽取 | `"50edf54eaa5842e891d959ae115205be"` | 需提前通过 [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md) 创建 |
| `plan_version` | 计费策略：`pro`（支持 `min_score` 过滤、Rerank）或 `lite`（基础检索） | `"pro"` | `search` 和 `profile_schema` 创建/更新时可指定；`pro` 为默认值 |
| `memory_types` | `SearchMemory` 中指定检索的记忆类型，默认 `["observation"]` | `["observation", "skill"]` | 不支持同时检索 `user_profile` |

## 使用方式

1. **准备凭证**：在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)获取 `DASHSCOPE_API_KEY` 和业务空间 ID（`llm-xxxxxxxxxxxx`），设置环境变量 `export DASHSCOPE_API_KEY="sk-..."` 和 `export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`。
2. **写入记忆**：
   - 同步写入（实时性要求高、`efficient` 模式）：调用 `AddMemory`，直接返回抽取结果。
   - 异步写入（推荐）：调用 `AddMemoryAsync` 获取 `event_id`，再轮询 `GetEvent` 直至 `status=SUCCEEDED`。
3. **检索记忆**：调用 `SearchMemory`，传入 `user_id` 和查询 `messages`，按 `top_k` 和 `min_score`（仅 `plan_version=pro` 生效）筛选结果。
4. **管理画像**：先创建 `profile_schema`，写入时传 `profile_schema`，再通过 `GetUserProfile` 查询结果。首次查询可能为空，需按业务逻辑重试 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)。
5. **SDK 调用**：推荐使用 `agentscope-runtime` 工具包（如 `AddMemory`, `SearchMemory`, `GetUserProfile`），自动处理 endpoint、鉴权与序列化。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口 120 QPM，`search` 接口 300 QPM。超限时返回 HTTP 429，需按指数退避（1s/2s/4s）重试 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)。
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，Add/Search 调用将区分 `pro`/`lite` 版本 [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- **软删除**：`DeleteMemory` 为逻辑删除（`status=delete`），节点仍可通过 `GetMemoryNode` 查询，但不参与 `SearchMemory` 和 `ListMemory` 默认结果。
- **技能导出**：`GetSkillExport` 仅适用于 `memory_type=skill` 的节点，返回 `skill_name`/`skill_description`/`skill_tags` 等专属字段，普通 `GetMemoryNode` 不返回这些字段。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)


