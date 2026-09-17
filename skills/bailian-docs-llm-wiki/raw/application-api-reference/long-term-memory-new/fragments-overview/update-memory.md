# 更新记忆

更新一条事实记忆的内容

修改已有事实记忆的内容。通过 `memory_node_id` 指定要更新的记忆。

## 请求参数

参数

类型

必填

说明

`memory_node_id`

string

是

记忆节点 ID（路径参数）

`user_id`

string

是

记忆实体 ID

`custom_content`

string

否

更新后的记忆内容

## 代码示例

cURL

```
curl -X PATCH "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/{memory_node_id}" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "user_id": "user_001",
    "custom_content": "还要提醒我上午10点吃药。"
  }'
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import UpdateMemory
import asyncio

async def main():
    update_memory = UpdateMemory()
    try:
        await update_memory.arun(
            memory_node_id="MEMORY_NODE_ID",
            user_id="user_001",
            custom_content="还要提醒我上午10点吃药。"
        )
        print("更新成功")
    finally:
        await update_memory.close()

asyncio.run(main())
```

## 响应示例

```
{
  "request_id": "e7954ee7-f0df-9895-9b44-39b4b395eac1"
}
```

**重要**删除记忆使用 [DeleteMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/delete-memory.md)。
