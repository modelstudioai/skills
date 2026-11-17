# 获取 Turn

获取根 Agent 的单个 Turn，查看状态、时间边界、错误和 Token 用量。

## 接口

`GET /agents/sessions/{session_id}/turns/{turn_id}`

成功返回 `200`，响应体是单个 Turn。查询不启动模型、不恢复执行，也不创建资源。

## 路径参数

**session\_id** `string` **（必选）**

Session ID，例如 `sess_xxx`

**turn\_id** `string` **（必选）**

公开 Turn ID，例如 `turn_xxx`

路径上下级必须匹配。跨工作空间、其他调用方的 Turn，以及父资源不存在的请求不会返回数据。

## 请求示例

curl

```
curl "$BASE_URL/agents/sessions/sess_xxx/turns/turn_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
turn = client.beta.agents.sessions.turns.retrieve(
    "turn_xxx", session_id="sess_xxx"
)
print(turn.status)
```

### 响应字段

**id** `string`

公开 Turn ID

**object** `string`

对象类型，固定为 `agent.session.turn`

**session\_id** `string`

所属 Session

**agent\_id** `string`

执行 Agent

**subagent\_id** `string / null`

子 Agent ID。根 Turn 为 `null`

**status** `string`

Turn 状态：`in_progress`、`waiting`、`completed`、`failed`、`cancelled`

**created\_at** `integer`

创建时间，Unix 秒

**started\_at`/`completed\_at** `integer / null`

开始时间和完成时间，Unix 秒。未到边界时为 `null`

**error** `object / null`

Turn 级错误；`null` 表示无错误

属性

**code** `string`

错误码

**message** `string`

错误说明

**usage** `object / null`

Token 用量；相关计数不齐时为 `null`

属性

**input\_tokens** `integer`

输入 Token 数

input\_tokens\_details

**cached\_tokens** `integer`

命中缓存的输入 Token 数

**output\_tokens** `integer`

输出 Token 数

output\_tokens\_details

**reasoning\_tokens** `integer`

推理 Token 数

**total\_tokens** `integer`

总 Token 数

`usage` 包含 `input_tokens`、`input_tokens_details.cached_tokens`、`output_tokens`、`output_tokens_details.reasoning_tokens` 和 `total_tokens`。相关计数不齐时，整个 `usage` 为 `null`。

`waiting` 不是成功终态。`completed`、`failed`、`cancelled` 才是终态。SSE 的 `turn.created` 事件中可能出现 `queued`，持久 Turn 从 `in_progress` 开始。

## 响应示例

```
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
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`404`

`not_found_error` / `not_found_error`

确认 Session、Turn 存在且属于同一工作空间，并使用匹配的路径层级

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id`
