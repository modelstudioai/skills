# 异步添加记忆

异步将对话存储为记忆，通过事件 ID 查询执行状态与结果

异步将用户对话存储为记忆。接口立即返回事件 ID，记忆提取在后台执行，通过 [GetEvent](raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md) 查询执行状态与结果。与同步的 [AddMemory](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory.md) 相比，异步接口不会在请求内等待提取完成，适合对话轮次多、提取耗时长的场景。

**说明**调用前请确保已获取 API Key，详见[鉴权](raw/application-api-reference/long-term-memory-new/overview/authentication.md)。

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

对话消息列表，最多 50 条。`role` 支持 user / assistant / **tool**；`content` 支持文本字符串或标准 OpenAI 格式的多模态数组；assistant 消息可携带 `tool_calls`；`role` 为 tool 的消息需携带对应的 `tool_call_id`

`custom_content`

string

是\*

自定义内容，最大 512 字符。与 `messages` 互斥，只能绑定到一个 `project_id`

`profile_schema`

string

否

画像模板 ID。**不传则不提取用户画像**

`memory_library_id`

string

否

记忆库 ID，不传则使用默认记忆库

`project_id`

string

否

自定义项目 ID，支持记忆二级隔离。与 `project_ids` 互斥

`project_ids`

array\[string\]

否

多个自定义项目 ID。与 `project_id` 互斥

`skill_name`

string

否

skill 内容名称

`skill_description`

string

否

skill 内容描述

`skill_tags`

array\[string\]

否

skill 内容标签

`meta_data`

object

否

用户自定义信息

**说明**`messages` 和 `custom_content` 互斥，填 `custom_content` 后会忽略 `messages`。

**警告**project 为 skill 的情况下，如果传入 `custom_content`，则必传 `skill_name`、`skill_description`、`skill_tags`，否则接口报错。

## 返回结果

字段

类型

说明

`request_id`

string

请求 ID

`event_id`

string

执行任务事件 ID

`events`

array

执行的任务列表。一次调用可能产生多个任务，例如事实记忆与用户画像各一个

`events[].event_id`

string

事件 ID

`events[].event_type`

string

事件类型，例如 ADD\_ASYNC

`events[].resource_type`

string

任务来源类型：observation / skill / profile

`events[].resource_id`

string

任务来源 ID，project 或 profile 相应 ID

`events[].memory_library_id`

string

任务对应的记忆库 ID

`events[].user_id`

string

任务对应的记忆实体 ID

`events[].status`

string

任务状态：PENDING / SUCCEEDED / FAILED / UNRECORDED

`events[].created_at`

integer

任务创建时间戳

`events[].updated_at`

integer

任务状态最后更新时间戳

## 代码示例

```
curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add-async \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "messages": [
      {"role": "user", "content": "每天上午11点提醒我点外卖，明天提醒我穿衣服。"},
      {"role": "assistant", "content": "没问题"},
      {"role": "assistant", "content": "", "tool_calls": [
        {"id": "call_1", "type": "function", "function": {"name": "update_memory", "arguments": "{\"text\":\"明天穿衣服\"}"}}
      ]},
      {"role": "tool", "tool_call_id": "call_1", "content": "{\"ok\":true}"}
    ],
    "project_ids": ["project_001"],
    "user_id": "user_001"
  }'

# response
{
  "event_id": "9d30e77a...",
  "events": [
    {
      "event_id": "9d30e77a...",
      "event_type": "ADD_ASYNC",
      "resource_type": "observation",
      "resource_id": "project_001",
      "status": "PENDING",
      "created_at": 1784638015,
      "updated_at": 1784638015,
      "user_id": "user_001"
    }
  ],
  "request_id": "048983ff-ed50-..."
}
```

**重要**返回的 `status` 为 PENDING 表示后台仍在提取，使用 [GetEvent](raw/application-api-reference/long-term-memory-new/fragments-overview/get-event.md) 查询执行结果。
