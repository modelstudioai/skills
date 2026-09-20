# 查询事件

查询异步添加记忆事件的执行状态与结果

查询[异步添加记忆](raw/application-api-reference/long-term-memory-new/fragments-overview/add-memory-async.md)所生成事件的执行状态与结果。

## 请求参数

参数

类型

必填

说明

`event_id`

string

是

事件 ID（路径参数）

## 返回结果

字段

类型

说明

`request_id`

string

请求 ID

`events`

array

事件列表

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

任务来源 ID

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

`events[].result`

array

执行结果，`status` 为 SUCCEEDED 后出现

`events[].result[].memory_type`

string

记忆类型：observation / skill / user\_profile

`events[].result[].content`

string

event 为 ADD 时为添加内容，UPDATE 时为新内容，DELETE 时为旧内容

`events[].result[].event`

string

操作类型：ADD / UPDATE / DELETE

`events[].result[].memory_node_id`

string

记忆节点 ID。memory\_type 为 user\_profile 时不存在

`events[].result[].old_content`

string

更新前内容，仅 event 为 UPDATE 时存在

## 代码示例

```
curl -X GET "https://dashscope.aliyuncs.com/api/v2/apps/memory/events/{event_id}" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"

# response
{
  "events": [
    {
      "event_id": "07c054c4...",
      "event_type": "ADD_ASYNC",
      "resource_type": "profile",
      "resource_id": "profile_schema_001",
      "status": "PENDING",
      "created_at": 1784602119,
      "updated_at": 1784602161,
      "user_id": "user_001"
    },
    {
      "event_id": "07c054c4...",
      "event_type": "ADD_ASYNC",
      "resource_type": "observation",
      "resource_id": "project_001",
      "status": "SUCCEEDED",
      "result": [
        {"content": "用户想去非洲", "event": "DELETE", "memory_node_id": "3127d744..."}
      ],
      "created_at": 1784602119,
      "updated_at": 1784602150,
      "user_id": "user_001"
    }
  ],
  "request_id": "bb499327-79c6-..."
}
```

**重要**`status` 为 PENDING 时后台仍在执行，稍后重新查询即可。
