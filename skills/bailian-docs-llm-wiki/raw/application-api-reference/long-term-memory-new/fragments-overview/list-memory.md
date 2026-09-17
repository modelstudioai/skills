# 列出记忆

分页查看用户的所有事实记忆

分页查看指定用户的所有事实记忆。支持通过 `user_id` 筛选。

## 请求参数

参数

类型

必填

说明

`user_id`

string

是

记忆实体 ID

`page_size`

number

否

每页数量

`page_num`

number

否

页码，从 1 开始

## 代码示例

cURL

```
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes?user_id=user_001&page_size=10&page_num=1" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    ListMemory, ListMemoryInput,
)
import asyncio

async def main():
    list_memory = ListMemory()
    try:
        result = await list_memory.arun(ListMemoryInput(
            user_id="user_001",
            page_size=10,
            page_num=1
        ))
        for node in result.memory_nodes:
            print(f"记忆: {node.content}")
    finally:
        await list_memory.close()

asyncio.run(main())
```

## 响应示例

```
{
  "memory_nodes": [
    {
      "content": "用户每天上午9点需要喝水提醒",
      "created_at": 1789614241,
      "media_desc": "",
      "memory_node_id": "91e628e811134e5598154a1719791a68",
      "memory_type": "observation",
      "meta_data": {},
      "project_id": "774b2f671e3c447ab7f5d02b1e2b9453",
      "status": "valid",
      "timestamp": 1789606800,
      "updated_at": 1789614241
    },
    {
      "content": "用户需要明天10点提醒整理会议纪要",
      "created_at": 1789614241,
      "media_desc": "",
      "memory_node_id": "56d43a6ec74548bcb0ad59fdedd28569",
      "memory_type": "observation",
      "meta_data": {},
      "project_id": "774b2f671e3c447ab7f5d02b1e2b9453",
      "status": "valid",
      "timestamp": 1789696800,
      "updated_at": 1789614241
    }
  ],
  "page_num": 1,
  "page_size": 10,
  "request_id": "1c1c41bf-a375-9ad0-b870-8d41b20a3a67",
  "total": 2
}
```

**重要**修改记忆使用 [UpdateMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/update-memory.md)。
