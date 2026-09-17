# 长期记忆 API

AI 在长对话中会遗忘关键信息，且跨会话没有记忆，导致上下文丢失、体验不连贯。长期记忆 API 可自动从历史对话中提炼并结构化存储事实记忆与用户画像，在后续对话或新会话中检索这些记忆并注入 Prompt，赋能 AI 实现真正的持续性理解。

记忆库（长期记忆）提供完整的开放 API，覆盖事实记忆的写入、检索、更新、删除，以及用户画像模板管理和画像获取。所有接口通过 DashScope 网关提供服务，服务地址为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，采用 API Key 鉴权，详见[鉴权](raw/application-api-reference/long-term-memory-new/overview/authentication.md)。

## 接口一览

**事实记忆**：

接口

方法

路径

说明

[AddMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md)

POST

`/add`

添加记忆，自动提取关键信息

[SearchMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md)

POST

`/memory_nodes/search`

基于语义检索历史记忆

[ListMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)

GET

`/memory_nodes`

分页列出记忆

[UpdateMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)

PATCH

`/memory_nodes/{memory_node_id}`

更新记忆内容

[DeleteMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)

DELETE

`/memory_nodes/{memory_node_id}`

删除记忆

**用户画像**：

接口

方法

路径

说明

[CreateProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)

POST

`/profile_schemas`

创建画像模板

[ListProfileSchemas](raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md)

GET

`/profile_schemas`

列出画像模板

[GetProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/get-schema.md)

GET

`/profile_schemas/{profile_schema_id}`

获取画像模板详情

[UpdateProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/update-schema.md)

PATCH

`/profile_schemas/{profile_schema_id}`

更新画像模板

[DeleteProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/delete-schema.md)

DELETE

`/profile_schemas/{profile_schema_id}`

删除画像模板

[GetUserProfile](raw/application-api-reference/long-term-memory-new/profiles-overview/get-user-profile.md)

GET

`/profile_schemas/{profile_schema_id}/user_profile`

获取用户画像

## 最小调用示例

写入记忆（AddMemory）：

```
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
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

```
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "query": "我需要做什么？"
  }'
```

## 使用限制

全部接口总计不超过 3000 QPM（阿里云账号级别），事实记忆 add 接口 120 QPM，search 接口 300 QPM。详见[限流说明](raw/application-user-guide/memory-library-overview/overview/limits.md)。

**重要**按接口分页的参数、返回结果和 Python 示例，参见[长期记忆 API 参考](raw/application-api-reference/long-term-memory-new/overview.md)；端到端上手流程参见[快速开始](raw/application-user-guide/memory-library-overview/memory/quickstart.md)，功能与控制台操作参见[记忆库](raw/application-user-guide/memory-library-overview/memory-library.md)。
