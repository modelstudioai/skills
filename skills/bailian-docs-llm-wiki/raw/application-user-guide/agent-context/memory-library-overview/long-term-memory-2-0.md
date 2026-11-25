# 长期记忆 API

AI 在长对话中会遗忘关键信息，且跨会话没有记忆，导致上下文丢失、体验不连贯。长期记忆 API 可自动从历史对话中提炼并结构化存储事实记忆与用户画像，在后续对话或新会话中检索这些记忆并注入 Prompt，赋能 AI 实现真正的持续性理解。

记忆库（长期记忆）提供完整的开放 API，覆盖记忆节点的写入、检索、更新、删除，以及用户画像模板管理和画像获取。所有接口通过业务空间专属域名提供服务，服务地址为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/`，调用时请将 `{WorkspaceId}` 替换为真实的[业务空间 ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。接口采用 API Key 鉴权，API Key 须属于同一业务空间，详见[鉴权](../../../application-api-reference/long-term-memory-new/api-overview/authentication.md)。

<a id="接口一览"></a>

## 接口一览

**记忆管理**：

| 接口 | 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| [AddMemory](../../../application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) | POST | `/add` | 添加记忆，自动提取关键信息 |
| [AddMemoryAsync](../../../application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md) | POST | `/add-async` | 异步提交记忆抽取任务 |
| [GetEvent](../../../application-api-reference/long-term-memory-new/fragments-overview/get-event.md) | GET | `/events/{event_id}` | 查询异步任务事件详情 |
| [ListMemory](../../../application-api-reference/long-term-memory-new/fragments-overview/list-memory.md) | GET | `/memory_nodes` | 分页列出记忆节点 |
| [SearchMemory](../../../application-api-reference/long-term-memory-new/fragments-overview/search-memory.md) | POST | `/memory_nodes/search` | 相似度检索记忆节点，默认仅检索事实记忆 |
| [GetMemoryNode](../../../application-api-reference/long-term-memory-new/fragments-overview/get-memory-node.md) | GET | `/memory_nodes/{memory_node_id}` | 获取单个记忆节点详情 |
| [GetSkillExport](../../../application-api-reference/long-term-memory-new/fragments-overview/get-skill-export.md) | GET | `/skill/export/{memory_node_id}` | 导出技能记忆节点 |
| [UpdateMemory](../../../application-api-reference/long-term-memory-new/fragments-overview/update-memory.md) | PATCH | `/memory_nodes/{memory_node_id}` | 更新记忆节点内容 |
| [DeleteMemory](../../../application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md) | DELETE | `/memory_nodes/{memory_node_id}` | 删除记忆节点 |

**用户画像**：

| 接口 | 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| [CreateProfileSchema](../../../application-api-reference/long-term-memory-new/profiles-overview/create-schema.md) | POST | `/profile_schemas` | 创建画像模板 |
| [ListProfileSchemas](../../../application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md) | GET | `/profile_schemas` | 列出画像模板 |
| [GetProfileSchema](../../../application-api-reference/long-term-memory-new/profiles-overview/get-schema.md) | GET | `/profile_schemas/{profile_schema_id}` | 获取画像模板详情 |
| [UpdateProfileSchema](../../../application-api-reference/long-term-memory-new/profiles-overview/update-schema.md) | PATCH | `/profile_schemas/{profile_schema_id}` | 更新画像模板 |
| [GetUserProfile](../../../application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md) | GET | `/profile_schemas/{profile_schema_id}/user_profile` | 获取用户画像 |

<a id="最小调用示例"></a>

## 最小调用示例

写入记忆（AddMemory）：

<a id="code-block"></a>

```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "messages": [
      {"role": "user", "content": "每天上午9点提醒我喝水"},
      {"role": "assistant", "content": "好的，已记录"}
    ],
    "user_id": "user_001"
  }'
```

检索记忆（SearchMemory）：

<a id="code-block-2"></a>

```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "messages": [
      {"role": "user", "content": "我需要做什么？"}
    ]
  }'
```

<a id="使用限制"></a>

## 使用限制

全部接口总计不超过 3000 QPM（阿里云账号级别），add 接口 120 QPM，search 接口 300 QPM。详见[限流说明](integration-overview/limits.md)。

> **重要**
>
> 按接口分页的参数、返回结果和 Python 示例，参见[长期记忆 API 参考](../../../application-api-reference/long-term-memory-new/api-overview.md)；端到端上手流程参见[快速开始](overview/quickstart.md)，功能与控制台操作参见[记忆库](memory-library.md)。
