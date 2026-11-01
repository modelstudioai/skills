# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的结构化记忆管理服务，支持事实记忆（`observation`）与技能记忆（`skill`）的写入、检索、更新与删除，并可结合用户画像模板进行属性抽取。所有操作均基于业务空间隔离，通过统一 API 接口与 SDK 调用，适用于 Agent 场景下的上下文持久化与个性化能力构建。

## 支持的模型/功能

- **记忆类型**：支持两类核心记忆节点  
  - `observation`（事实记忆）：如“用户每天上午11点提醒点外卖”，由对话消息自动抽取；  
  - `skill`（技能记忆）：如“会议纪要整理”，需显式传入 `skill_name`/`skill_description`/`skill_tags`，支持导出为可复用技能模块（详见[导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)）。  
- **用户画像**：通过预定义的 `profile_schema` 模板驱动异步抽取，支持 `efficient`（低延迟）与 `intelligent`（高精度）两种提取场景，字段可动态增删改（参见[更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)）。  
- **多模态支持**：`messages` 中可包含 `image_url` 类型内容，但仅在启用多模态能力的项目中触发图片解析，其余项目将忽略图片字段（见[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)文档说明）。  
> **注意**：文档 5 和文档 6 均指出 `custom_content` 与 `project_ids` 互斥，但文档 6 的参数表明确标注 `custom_content` 与 `project_ids` 不能同时传入，而文档 5 未提及此限制；实际开发应以文档 6 的约束为准，避免因参数冲突导致 400 错误。

## 关键参数

| 参数 | 作用 | 必填性 | 说明 |
|------|------|--------|------|
| `user_id` | 用户级隔离标识 | 所有写入/检索接口必填 | 同一 `user_id` 下的记忆默认隔离，不可跨用户访问 |
| `project_id` / `project_ids` | 项目级二级隔离 | 可选 | `project_id`（单值）与 `project_ids`（数组，最多 5 个）互斥；用于按业务域分组记忆（如不同 Agent 应用） |
| `memory_library_id` | 记忆库 ID | 可选 | 不传则使用默认记忆库；需确保 API Key 所属业务空间已开通对应记忆库 |
| `profile_schema` | 画像模板 ID | 仅画像抽取时必填 | 传入后触发用户属性抽取，需提前通过[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)生成 |
| `plan_version` | 计费策略版本 | 可选（默认 `pro`） | `pro` 支持 `min_score` 过滤与 Rerank；`lite` 仅基础检索，不生效 `min_score`（见[搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)） |
| `extract_mode` | 抽取模式 | 可选 | `profile_only` 表示仅执行画像抽取，此时必须同时传入 `profile_schema` 和 `messages` |

## 使用方式

1. **认证准备**：  
   - 获取业务空间 ID（从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)复制 `API Host` 中的 `llm-xxxxxxxxxxxx` 部分）；  
   - 获取 `DASHSCOPE_API_KEY`（控制台 > API Key 管理），并设为环境变量 `export DASHSCOPE_API_KEY="sk-..."`；  
   - 请求 Header 必须包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`（见[认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)）。

2. **写入记忆**：  
   - **同步写入**（`/add`）：适合实时性要求高、内容简单场景，响应中直接返回抽取结果；  
   - **异步写入**（`/add-async`）：推荐用于复杂对话、多项目并行或需技能/画像联合抽取的场景，返回 `event_id` 后需轮询 [GetEvent](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md) 查询状态。

3. **检索与管理**：  
   - 检索：调用 `/memory_nodes/search`，传入 `messages` 作为查询向量，支持 `top_k`、`min_score`（`pro` 版本）、`memory_types` 等过滤；  
   - 列表：`/memory_nodes` 分页获取全部记忆，支持 `user_id` + `project_id` 组合筛选；  
   - 单条操作：`/memory_nodes/{id}` 查看、`PATCH /memory_nodes/{id}` 更新、`DELETE /memory_nodes/{id}` 删除（删除不可逆，需谨慎）。

4. **SDK 快速接入**：  
   - 安装 `agentscope-runtime`，设置环境变量 `MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`；  
   - 直接调用 `AddMemory`、`SearchMemory` 等封装工具（示例见[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)和[搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)）。

## 限制和注意事项

- **限流规则**（阿里云账号级别）：  
  - 全部接口总计 ≤ 3000 QPM；  
  - `add` 接口 ≤ 120 QPM；  
  - `search` 接口 ≤ 300 QPM；  
  - 超限返回 HTTP 429，需按指数退避（1s/2s/4s）重试（见[错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)）。
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，`Add` 与 `Search` 接口均区分 `Pro`/`Lite` 版本，策略差异影响抽取质量与检索能力（见[长期记忆API](../../raw/application-user-guide/agent-context/memory-library-overview/long-term-memory-2-0.md)）。
- **安全要求**：  
  - API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库；  
  - 建议为不同应用分配独立 API Key，便于权限管控与泄露溯源。
- **数据持久性**：当前生成的记忆片段与用户画像无自动失效机制，长期存储需自行设计 TTL 或定期清理逻辑。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)


