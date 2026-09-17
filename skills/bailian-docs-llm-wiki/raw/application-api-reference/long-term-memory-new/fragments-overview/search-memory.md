# 搜索记忆

基于语义检索返回与查询最相关的历史记忆

基于语义检索返回与当前查询最相关的历史记忆。支持查询改写、结果重排和相似度过滤。

## 请求参数

参数

类型

必填

说明

`user_id`

string

是

记忆实体 ID

`messages`

array

是

对话消息列表，每条含 `role`（user/assistant）和 `content`

`top_k`

number

否

最大召回数量（1~100，默认 10）

`min_score`

number

否

最小相似度阈值（0.0~1.0，默认 0.3）

`enable_rerank`

boolean

否

是否开启结果重排（默认 false）。`plan_version` 优先级更高

`enable_judge`

boolean

否

是否开启意图判别（默认 false）

`enable_rewrite`

boolean

否

是否开启查询改写（默认 false）

`plan_version`

string

否

`Pro`（默认，开启 Rerank）或 `Lite`（关闭 Rerank），大小写不敏感。传入后忽略 `enable_rerank`

`project_ids`

array

否

事实记忆规则 ID 数组，传入多个可混合检索。不传使用默认规则

**说明**Pro 版开启 Rerank，检索质量更高，但可能过滤掉低相关结果；Lite 版关闭 Rerank，成本更低。详见[计费说明](raw/application-user-guide/memory-library-overview/overview/billing.md)。

## 代码示例

cURL

```
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "messages": [{"role": "user", "content": "我需要做什么？"}],
    "top_k": 10,
    "min_score": 0.3,
    "plan_version": "Lite"
  }'
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    SearchMemory, SearchMemoryInput, Message,
)
import asyncio

async def main():
    search_memory = SearchMemory()
    try:
        result = await search_memory.arun(SearchMemoryInput(
            user_id="user_001",
            messages=[Message(role="user", content="我需要做什么？")],
            top_k=10,
            min_score=0.6
        ))
        for node in result.memory_nodes:
            print(f"记忆: {node.content}")
    finally:
        await search_memory.close()

asyncio.run(main())
```

## 响应示例

```
{
  "memory_nodes": [
    {
      "content": "用户需要明天10点提醒整理会议纪要",
      "created_at": 1789614241,
      "memory_node_id": "56d43a6ec74548bcb0ad59fdedd28569",
      "memory_type": "observation",
      "meta_data": {},
      "project_id": "774b2f671e3c447ab7f5d02b1e2b9453",
      "score": 0.731,
      "status": "valid",
      "timestamp": 1789696800,
      "updated_at": 1789614241
    },
    {
      "content": "用户每天上午9点需要喝水提醒",
      "created_at": 1789614241,
      "memory_node_id": "91e628e811134e5598154a1719791a68",
      "memory_type": "observation",
      "meta_data": {},
      "project_id": "774b2f671e3c447ab7f5d02b1e2b9453",
      "score": 0.5,
      "status": "valid",
      "timestamp": 1789606800,
      "updated_at": 1789614241
    }
  ],
  "plan_version": "lite",
  "request_id": "a8fc5647-6ed6-9b4e-ae08-e2252b688655"
}
```

**重要**查看所有记忆使用 [ListMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/list-memory.md)。
