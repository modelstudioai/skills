# 添加记忆

将对话存储为事实记忆，自动提取关键信息

将用户对话存储为事实记忆，自动提取关键信息。也支持直接指定自定义内容存储。若需同时提取用户画像，需传入 `profile_schema`。

**说明**调用前请确保已获取 API Key，详见[鉴权](raw/application-api-reference/long-term-memory-new/api-overview/authentication.md)。

**重要**对话轮次多、提取耗时长的场景，可使用[异步添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)，后台执行提取，通过事件 ID 查询状态与结果。

## 请求参数

参数

类型

必填

说明

`user_id`

string

是

记忆实体 ID，用于标识归属对象，最大 64 字符

`messages`

array

是\*

对话消息列表，最多 50 条。每条含 `role`（user/assistant）和 `content`

`custom_content`

string

是\*

自定义内容，最大 512 字符。与 `messages` 互斥

`profile_schema`

string

否

画像模板 ID。**不传则不提取用户画像**，仅写入事实记忆

`memory_library_id`

string

否

记忆库 ID，不传则使用默认记忆库

`project_id`

string

否

事实记忆规则 ID，不传则使用默认规则

`meta_data`

object

否

用户自定义信息

**说明**`messages` 和 `custom_content` 互斥，填 `custom_content` 后会忽略 `messages`。

**警告****调用成功但用户画像属性为空？** 事实记忆与用户画像是两条独立的提取链路。不传 `profile_schema` 时，接口只会返回 `memory_nodes`，画像属性保持为空。请传入画像模板 ID 后重新调用，ID 可通过 [ListProfileSchemas](raw/application-api-reference/long-term-memory-new/profiles-overview/list-schemas.md) 获取，或在控制台记忆库详情页的**记忆规则 > 用户画像规则**中查看。

## 返回结果

字段

类型

说明

`request_id`

string

请求 ID

`memory_nodes`

array

变更的事实记忆列表

`memory_nodes[].memory_node_id`

string

事实记忆 ID

`memory_nodes[].content`

string

提取的记忆内容

`memory_nodes[].event`

string

操作类型：ADD / UPDATE / DELETE

`memory_nodes[].old_content`

string

更新前内容，仅 event 为 UPDATE 时有效

## 代码示例

cURL

```
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "messages": [
      {"role": "user", "content": "每天上午9点提醒我喝水"},
      {"role": "assistant", "content": "好的，已记录"},
      {"role": "user", "content": "明天10点提醒我整理会议纪要。"}
    ],
    "user_id": "user_001"
  }'
```

Python

```
from agentscope_runtime.tools.modelstudio_memory import (
    AddMemory, AddMemoryInput, Message,
)
import asyncio

async def main():
    add_memory = AddMemory()
    try:
        await add_memory.arun(AddMemoryInput(
            user_id="user_001",
            messages=[
                Message(role="user", content="每天上午9点提醒我喝水"),
                Message(role="assistant", content="好的，已记录"),
                Message(role="user", content="明天10点提醒我整理会议纪要。"),
            ]
        ))
        print("记忆写入成功")
    finally:
        await add_memory.close()

asyncio.run(main())
```

## 响应示例

```
{
  "memory_nodes": [
    {"content": "用户每天上午9点需要喝水提醒", "event": "ADD", "memory_node_id": "91e628e811134e5598154a1719791a68"},
    {"content": "用户需要明天10点提醒整理会议纪要", "event": "ADD", "memory_node_id": "56d43a6ec74548bcb0ad59fdedd28569"}
  ],
  "request_id": "d0917d55-6677-9be4-b7d3-caf347e572c0"
}
```

**重要**写入后，使用 [SearchMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/search-memory.md) 检索记忆。
