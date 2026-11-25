# long term memory new

长期记忆（Long Term Memory）是百炼平台提供的结构化[记忆管理](../concepts/memory.md)服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类记忆的写入、检索、更新与生命周期管理。所有操作均通过 RESTful API 或 `agentscope-runtime` SDK 完成，需基于业务空间专属域名和 API Key 进行鉴权。

## 支持的模型/功能

- **记忆类型**：支持 `observation`（事实记忆，如用户偏好、日程提醒）、`skill`（技能记忆，如[工具调用](../concepts/tool-calling.md)流程）和 `user_profile`（用户画像，需配合画像模板使用）。
- **抽取能力**：
  - 同步抽取（`AddMemory`）适用于实时性要求高的场景，但 `intelligent` 模式下可能超时；[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 文档明确推荐优先使用异步方式。
  - 异步抽取（`AddMemoryAsync`）支持多项目并行、技能抽取及画像联合提取，结果通过 `GetEvent` 查询；[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md) 是当前主推路径。
- **多模态支持**：`messages` 中可传入 `image_url` 类型内容，但仅在启用多模态能力的项目中被解析；其他项目将忽略图片字段。
- **用户画像**：需先创建画像模板（`CreateProfileSchema`），再在 `AddMemory` 或 `AddMemoryAsync` 中传入 `profile_schema` 才能触发抽取；[创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md) 提供了完整的 schema 定义方式。

> **注意**：  
> 文档 5（添加记忆）称“同步接口适合在 `efficient` 模式下对实时性要求较高的场景”，而文档 7（异步添加记忆）强调“该接口支持多项目并行抽取、技能抽取和用户画像抽取”，且两处均指出“当前主推异步添加”。这表明同步接口功能受限，不推荐用于复杂抽取场景，开发者应默认选用 `AddMemoryAsync`。

## 关键参数

| 参数 | 说明 | 示例值 | 是否必需 |
|------|------|--------|----------|
| `user_id` | 子用户 ID，用于跨用户记忆隔离 | `"user_001"` | ✅ 所有写入/检索接口必填 |
| `memory_library_id` | 记忆库 ID，不传则使用默认库 | `"memory_library_001"` | ❌（可选） |
| `project_id` / `project_ids` | 项目级二级隔离；`project_ids` 最多 5 个，与 `project_id` 互斥 | `["project_001", "project_002"]` | ❌（可选） |
| `profile_schema` | 用户画像模板 ID，仅当需抽取画像时传入 | `"50edf54eaa5842e891d959ae115205be"` | ❌（画像场景必需） |
| `extract_mode` | 抽取模式，`profile_only` 表示仅抽取画像（此时 `messages` 必须存在） | `"profile_only"` | ❌（条件必需） |
| `plan_version` | 计费策略版本：`pro`（支持 `min_score` 过滤、Rerank）或 `lite`（基础检索）；不区分大小写 | `"pro"` | ❌（默认 `pro`） |
| `top_k` | 检索最大返回数 | `10` | ❌（默认 `10`） |
| `min_score` | 最小相似度阈值，**仅 `plan_version=pro` 时生效** | `0.6` | ❌（默认 `0.3`） |

## 使用方式

### 1. 基础配置
- 设置环境变量：
  ```bash
  export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
  export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"
  ```
  其中 `{WorkspaceId}` 从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面的 **API Host** 列复制（格式如 `llm-xxxxxxxxxxxx`）。

### 2. 典型工作流
- **写入记忆**：调用 `AddMemoryAsync` 提交任务 → 用 `GetEvent` 轮询状态 → 状态为 `SUCCEEDED` 后获取 `memory_node_id`。
- **检索记忆**：调用 `SearchMemory`，传入 `user_id` 和 `messages`（如用户当前提问），按需指定 `memory_types`、`top_k` 和 `min_score`。
- **管理画像**：先 `CreateProfileSchema` 定义字段 → `AddMemoryAsync` 时传 `profile_schema` → 后续调用 `GetUserProfile` 获取结果。
- **CRUD 单个节点**：
  - 查：`GetMemoryNode`（通用）或 `GetSkillExport`（仅 skill 类型，含 `skill_name` 等字段）；
  - 改：`UpdateMemory`（PATCH，需 `custom_content`）；
  - 删：`DeleteMemory`（DELETE，不可逆）。

### 3. SDK 示例（Python）
```python
from agentscope_runtime.tools.modelstudio_memory import AddMemoryAsync, SearchMemory
import asyncio

async def main():
    # 异步写入
    add = AddMemoryAsync()
    event = await add.arun(user_id="user_001", messages=[...])
    
    # 检索
    search = SearchMemory()
    res = await search.arun(
        user_id="user_001",
        messages=[{"role": "user", "content": "我之前提过什么？"}],
        top_k=5,
        min_score=0.5,
        plan_version="pro"
    )
```

## 限制和注意事项

- **限流规则**（阿里云账号级别）：
  - 全部接口总计 ≤ 3000 QPM；
  - `add` 接口 ≤ 120 QPM；
  - `search` 接口 ≤ 300 QPM；
  - 超限返回 HTTP 429，需按 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md) 文档执行指数退避重试（1s/2s/4s）。

- **计费与版本**：
  - 服务将于 **2026 年 8 月 20 日 10:00（北京时间）正式商业化计费**，Add 和 Search 均区分 `Pro`/`Lite` 版本；
  - `SearchMemory` 的 `min_score` 参数仅在 `plan_version=pro` 时生效；`lite` 版本忽略该参数，可能导致低质量结果召回。

- **数据持久性与状态**：
  - 记忆片段与用户画像**暂无自动失效日期**，需自行管理生命周期；
  - 删除操作为软删除（`status: "delete"`），历史仍可通过 `ListMemory` 查询，但 `SearchMemory` 默认不返回已删节点。

- **安全与权限**：
  - API Key 具有账号级权限，**严禁硬编码或提交至代码仓库**，应使用环境变量管理；
  - RAM 子账号需显式授权才能调用，详见 [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md) 文档。

- **调试建议**：
  - 所有响应均含 `request_id`，排查问题时必须提供；
  - 异步任务状态为 `PENDING` 或 `RUNNING` 时需轮询 `GetEvent`，不可假设立即完成；
  - 若 `GetUserProfile` 返回空值，请确认 `AddMemory` 调用时传入了**完全匹配的 `profile_schema` ID**。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)
- [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)
- [搜索记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)
- [查询记忆节点](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md)
- [更新记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)
- [删除记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)
- [用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview.md)
- [创建画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)
- [列出画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)
- [获取画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)
- [更新画像模板](../../raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [列出记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)
- [导出技能记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md)


