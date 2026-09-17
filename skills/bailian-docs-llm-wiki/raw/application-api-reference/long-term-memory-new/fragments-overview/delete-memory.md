# 删除记忆

删除一条事实记忆，删除后不可恢复

删除指定的事实记忆条目。删除后不可恢复。

**警告**删除操作不可逆，请谨慎操作。

## 请求参数

参数

类型

必填

说明

`memory_node_id`

string

是

记忆节点 ID（路径参数）

## 代码示例

cURL

```
curl -X DELETE "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json"
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    DeleteMemory, DeleteMemoryInput,
)
import asyncio

async def main():
    delete_memory = DeleteMemory()
    try:
        await delete_memory.arun(DeleteMemoryInput(
            user_id="user_001",
            memory_node_id="MEMORY_NODE_ID"
        ))
        print("删除成功")
    finally:
        await delete_memory.close()

asyncio.run(main())
```

## 响应示例

```
{
  "request_id": "8e7bf48d-91ea-9ed1-a2b3-6266e3071e44"
}
```

**重要**用户画像 API 参见 [CreateProfileSchema](raw/application-api-reference/long-term-memory-new/profiles-overview/create-schema.md)。
