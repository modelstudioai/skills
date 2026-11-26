# long term memory new

[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）是百炼平台提供的结构化记忆管理服务，支持事实记忆（observation）、技能记忆（skill）和用户画像（user profile）三类记忆的写入、检索、更新与生命周期管理。所有操作均通过 RESTful API 或 `agentscope-runtime` SDK 完成，需基于业务空间专属域名和 API Key 鉴权。该服务将于 2026 年 8 月 20 日起正式商业化计费，Add 和 Search 接口区分 `pro` 与 `lite` 计费策略版本。

## 支持的模型/功能

[长期记忆](../concepts/long-term-memory.md)服务本身不直接暴露大模型调用，而是封装了基于百炼平台统一抽取模型的记忆生成能力，按使用场景分为两类：

- **记忆抽取模型**：由 `project_id` 关联的记忆规则决定抽取类型（`observation` 或 `skill`），`custom_content` 模式下可显式指定；`profile_schema` 参数触发用户画像抽取。
- **搜索重排模型**：仅在 `SearchMemory` 的 `plan_version=pro` 时启用 Rerank，提升语义召回质量；`lite` 版本仅执行基础向量检索。

> **注意**：文档 5（[添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)）指出同步接口在 `intelligent` 模式下“可能超时”，而文档 20（[异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)）明确推荐其为“主推”方式，且支持多项目并行抽取与技能/画像混合抽取。因此，对可靠性与扩展性要求高的生产场景，应优先选用异步接口。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | Query / Body | string | 是 | 子用户 ID，用于跨用户记忆隔离，所有读写接口均强制要求 |
| `memory_library_id` | Query / Body | string | 否 | 记忆库 ID，不传则使用默认记忆库；影响数据物理分区与配额归属 |
| `project_id` / `project_ids` | Body | string / array[string] | 否 | 项目级二级隔离标识；`project_ids` 最多支持 5 个，与 `project_id` 互斥；`custom_content` 模式下不可与 `project_ids` 共存 |
| `profile_schema` | Body | string | 否 | 用户画像模板 ID；传入后触发画像抽取，需配合 `messages` 使用（`extract_mode=profile_only` 时除外） |
| `plan_version` | Body | string | 否 | 计费策略版本，取值 `pro` 或 `lite`（不区分大小写）；`SearchMemory` 默认 `pro`，`CreateProfileSchema` 默认 `pro`；传入非法值将报错 |
| `extract_mode` | Body | string | 否 | 抽取模式，仅 `profile_only` 有效（此时必须同时传 `profile_schema` 和 `messages`） |

## 使用方式

### 1. 基础配置
- 设置环境变量：`export DASHSCOPE_API_KEY="sk-..."` 和 `export MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"`（末尾无 `/`）  
- `{WorkspaceId}` 从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面的 **API Host** 列复制，格式如 `llm-xxxxxxxxxxxx`

### 2. 核心流程示例（Python SDK）
```python
from agentscope_runtime.tools.modelstudio_memory import (
    AddMemoryAsync, SearchMemory, GetUserProfile,
    AddMemoryAsyncInput, SearchMemoryInput, GetUserProfileInput, Message,
)
import asyncio

async def main():
    # 1. 异步写入（推荐）
    add_async = AddMemoryAsync()
    event_resp = await add_async.arun(AddMemoryAsyncInput(
        user_id="user_001",
        project_ids=["project_001"],
        messages=[Message(role="user", content="明天10点提醒我开会")],
        profile_schema="50edf54eaa5842e891d959ae115205be"  # 触发画像抽取
    ))
    event_id = event_resp.event_id

    # 2. 轮询事件状态（见 [查询事件](../../raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md)）
    # 3. 语义搜索
    search = SearchMemory()
    result = await search.arun(SearchMemoryInput(
        user_id="user_001",
        messages=[Message(role="user", content="我明天有什么安排？")],
        top_k=5,
        plan_version="pro"
    ))

    # 4. 获取画像
    get_profile = GetUserProfile()
    profile = await get_profile.arun(GetUserProfileInput(
        schema_id="50edf54eaa5842e891d959ae115205be",
        user_id="user_001"
    ))
```

### 3. HTTP 直连（cURL）
```bash
# 添加记忆（异步）
curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/add-async' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "project_ids": ["project_001"],
    "messages": [{"role":"user","content":"每天喝水"}]
  }'

# 搜索记忆
curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/memory_nodes/search' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "messages": [{"role":"user","content":"我的日程"}],
    "top_k": 3,
    "plan_version": "pro"
  }'
```

## 限制和注意事项

- **限流**：阿里云账号级别总计 ≤ 3000 QPM；其中 `add` 接口 ≤ 120 QPM，`search` 接口 ≤ 300 QPM。超出时返回 HTTP 429，需按指数退避（1s/2s/4s）重试（见 [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)）。
- **记忆时效性**：当前生成的记忆片段与用户画像**暂无自动失效日期**，需业务侧自行管理生命周期（如定期清理）。
- **软删除**：`DeleteMemory` 为逻辑删除，`status` 变为 `delete`，仍可通过 `GetMemoryNode` 查询历史记录。
- **多模态支持**：仅当项目已开通多模态能力时，`messages[].content` 中的 `image_url` 才会被解析；否则图片信息被忽略。
- **画像异步性**：`GetUserProfile` 返回空值时，需确认 `AddMemory` 是否传入了正确的 `profile_schema`，并按业务逻辑重试（见 [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)）。
- **SDK 兼容性**：`agentscope-runtime` SDK 的 `ListMemory`、`SearchMemory` 等工具已封装分页、鉴权与错误处理，推荐优先使用。

## 来源文档

- [长期记忆API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)
- [概览](../../raw/application-api-reference/long-term-memory-new/api-overview.md)
- [错误码](../../raw/application-api-reference/long-term-memory-new/api-overview/errors.md)
- [认证](../../raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)
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
- [记忆管理](../../raw/application-api-reference/long-term-memory-new/fragments-overview.md)
- [获取用户画像](../../raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)
- [异步添加记忆](../../raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)


