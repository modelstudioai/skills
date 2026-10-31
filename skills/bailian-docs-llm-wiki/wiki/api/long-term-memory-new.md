# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）新版本是百炼平台提供的结构化记忆管理服务，支持将对话、自定义内容自动抽取为事实记忆（`observation`）、技能记忆（`skill`）和用户画像（`user_profile`）三类结构化节点，并提供语义搜索、分页列表、[异步任务](../concepts/asynchronous-task.md)管理等能力。所有操作均基于业务空间（Workspace）隔离，通过 API Key 鉴权，适用于 Agent 应用中持久化上下文与个性化状态的构建。

## 支持的模型/功能

- **记忆类型**：支持三类结构化记忆节点：
  - `observation`（事实记忆）：如“用户每天上午11点提醒点外卖”，由对话消息自动抽取；
  - `skill`（技能记忆）：如“会议纪要整理”，需显式传入 `skill_name`/`skill_description`/`skill_tags`，支持导出完整技能元信息；
  - `user_profile`（用户画像）：需先创建画像模板（`ProfileSchema`），再通过 `AddMemory` 传入 `profile_schema` 触发抽取，结果通过 [GetUserProfile](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) 查询。
- **抽取模式**：支持 `efficient`（低延迟）和 `intelligent`（高精度）两种提取场景，可在画像模板或 `AddMemory` 请求中指定；同步接口在 `intelligent` 模式下可能超时，推荐使用异步接口。
- **多模态支持**：`messages` 中可包含 `image_url` 类型内容，但仅限已开通多模态能力的业务空间解析图片；文本内容始终支持。

> **注意**：文档 4（[添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）称同步接口“在 `intelligent` 模式下可能超时”，而文档 14（[创建画像模板](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)）示例中 `extract_scene` 默认值为 `efficient`，且未说明 `intelligent` 模式对同步写入的兼容性。实际开发中，若需 `intelligent` 抽取，请优先选用 [AddMemoryAsync](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)。

## 关键参数

- `user_id`：必填，用于跨接口记忆隔离的核心标识符，所有读写操作均需指定。
- `memory_library_id`：可选，指定记忆库；不传则使用默认记忆库。
- `project_id` / `project_ids`：用于二级隔离与记忆类型路由（如绑定 skill 规则），与 `custom_content` 互斥。
- `profile_schema`：用户画像抽取必需，必须为已创建的有效模板 ID；配合 `extract_mode: "profile_only"` 可仅触发画像抽取。
- `skill_name` / `skill_description` / `skill_tags`：写入 `skill` 类型记忆时条件必填（见 [异步添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）。
- `plan_version`：搜索（`SearchMemory`）和画像模板（`CreateProfileSchema`）支持 `pro`/`lite` 计费策略；`pro` 支持 `min_score` 过滤与 Rerank，`lite` 不生效。
- `min_score`：仅 `plan_version=pro` 时有效，默认 `0.3`，用于过滤低相关性搜索结果。

## 使用方式

1. **准备凭证**：在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)获取 `DASHSCOPE_API_KEY` 和业务空间 ID（`llm-xxxxxxxxxxxx`），并设置环境变量：
   ```bash
   export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
   export MEMORY_SERVICE_ENDPOINT="https://llm-xxxxxxxxxxxx.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"
   ```
   > **注意**：文档 1（[认证](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）强调 API Key 必须属于同一业务空间，且 `MEMORY_SERVICE_ENDPOINT` 末尾**不带 `/`**（见文档 20）。

2. **写入记忆**：
   - 实时性要求高 → 用 [AddMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)（同步，立即返回结果）；
   - 需多项目并行、技能/画像混合抽取 → 用 [AddMemoryAsync](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)（异步，返回 `event_id`），再调用 [GetEvent](raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md) 轮询结果。

3. **检索与管理**：
   - 语义搜索 → [SearchMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)，支持 `top_k`、`min_score`、`memory_types` 筛选；
   - 分页浏览 → [ListMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)；
   - 单节点操作 → [GetMemoryNode](raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)（查）、[UpdateMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)（改）、[DeleteMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)（删）；
   - Skill 专用导出 → [GetSkillExport](raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)。

4. **用户画像流程**：
   - 创建模板 → [CreateProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)；
   - 写入对话并指定 `profile_schema` → [AddMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)；
   - 查询结果 → [GetUserProfile](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)（注意：画像抽取异步，首次查询可能为空，需重试）。

## 限制和注意事项

- **限流**：阿里云账号级总限流 3000 QPM；其中 `add` 接口 120 QPM，`search` 接口 300 QPM。超出时返回 HTTP 429，需按指数退避（1s/2s/4s）重试（见 [错误码](raw/application-api-reference/long-term-memory-new/api-overview/errors.md)）。
- **不可逆操作**：`DeleteMemory` 删除后无法恢复，调用前务必确认 `memory_node_id`。
- **多模态约束**：`image_url` 仅被多模态能力项目解析，普通项目忽略图片字段；`messages[].content` 为字符串时，不触发多模态处理。
- **计费时间点**：服务将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式商业化，Add/Search 均区分 `pro`/`lite` 版本（见 [长期记忆API 参考](raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)）。
- **安全要求**：API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转（见 [认证](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）。

## 来源文档

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
- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)


