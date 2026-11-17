# 列出 Turn

分页查询根 Agent 的 Turn 列表，核对执行状态和 Token 用量。

## 接口

`GET /agents/sessions/{session_id}/turns`

返回根 Agent 的 Turn 列表。成功返回 `200`。查询不启动模型、不恢复执行，也不创建资源。

## 路径参数

**session\_id** `string` **（必选）**

Session ID，例如 `sess_xxx`

## 查询参数

**limit** `integer` **（可选）**

每页数量，范围 1–100，默认 20

**order** `string` **（可选）**

排序方向，`asc` 或 `desc`，默认 `desc`

**after** `string` **（可选）**

上一页的 `last_id`；结果不包含游标项

`before` 会被忽略，不用于反向分页。使用 `order` 和 `after` 翻页。

## 请求示例

curl

```
curl --get "$BASE_URL/agents/sessions/sess_xxx/turns" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --data-urlencode "limit=20" \
  --data-urlencode "order=asc"
```

Python

```
turns = client.beta.agents.sessions.turns.list(
    "sess_xxx", limit=20, order="asc"
)
for turn in turns.data:
    print(turn.id, turn.status)
```

### 响应字段

列表信封： `usage` 包含 `input_tokens`、`input_tokens_details.cached_tokens`、`output_tokens`、`output_tokens_details.reasoning_tokens` 和 `total_tokens`。相关计数不齐时，整个 `usage` 为 `null`。

**object** `string`

列表对象类型，固定为 `list`

**data** `array<Turn>`

当页 Turn；空时为 `[]`

**first\_id** `string / null`

当页首项 ID。空页为 `null`

**last\_id** `string / null`

当页末项 ID。空页为 `null`。后续 `after` 使用该值

**has\_more** `boolean`

当前检索方向是否还有下一页

Turn 字段：

`waiting` 不是成功终态。`completed`、`failed`、`cancelled` 才是终态。SSE 的 `turn.created` 事件中可能出现 `queued`，持久 Turn 从 `in_progress` 开始。

data 项

**id** `string`

公开 Turn ID

**object** `string`

Turn 对象类型，固定为 `agent.session.turn`

**session\_id** `string`

所属 Session

**agent\_id** `string`

执行 Agent

**subagent\_id** `string / null`

子 Agent ID，根 Turn 为 `null`

**status** `string`

Turn 状态：`in_progress`、`waiting`、`completed`、`failed`、`cancelled`

**created\_at** `integer`

创建时间，Unix 秒

**started\_at`/`completed\_at** `integer / null`

开始时间和完成时间，Unix 秒。未到边界时为 `null`

**error** `object / null`

Turn 级错误。

属性

**code** `string`

错误码

**message** `string`

错误说明

**usage** `object / null`

Token 用量。

属性

**input\_tokens** `integer`

输入 Token 数

**input\_tokens\_details** `object`

输入 Token 明细。

属性

**cached\_tokens** `integer`

命中缓存的输入 Token 数

**output\_tokens** `integer`

输出 Token 数

**output\_tokens\_details** `object`

输出 Token 明细。

属性

**reasoning\_tokens** `integer`

推理 Token 数

**total\_tokens** `integer`

总 Token 数

## 响应示例

```
{
  "object": "list",
  "data": [
    {
      "id": "turn_xxx",
      "object": "agent.session.turn",
      "session_id": "sess_xxx",
      "agent_id": "agent_xxx",
      "subagent_id": null,
      "status": "completed",
      "created_at": 1794118835,
      "started_at": 1794118836,
      "completed_at": 1794118840,
      "error": null,
      "usage": {
        "input_tokens": 1024,
        "input_tokens_details": {"cached_tokens": 0},
        "output_tokens": 256,
        "output_tokens_details": {"reasoning_tokens": 64},
        "total_tokens": 1280
      }
    }
  ],
  "first_id": "turn_xxx",
  "last_id": "turn_xxx",
  "has_more": false
}
```
```
{
  "object": "list",
  "data": [],
  "first_id": null,
  "last_id": null,
  "has_more": false
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按查询参数说明修正 `limit`、`order`

`404`

`not_found_error` / `not_found_error`

使用有效的 Session ID；使用本集合上一页返回的 `last_id` 作为 `after`

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id`
