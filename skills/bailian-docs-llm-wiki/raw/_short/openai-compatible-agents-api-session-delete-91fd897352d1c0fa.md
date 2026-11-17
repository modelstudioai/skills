# 删除 Session

删除 Session，停止执行并清理公开历史；清理未完成时返回 409。

## 接口

**DELETE** `/agents/sessions/{session_id}`

成功返回 `200` 和删除信封。删除会停止该 Session 的执行，关闭输入接纳并清理公开历史；

清理尚未完成时返回 `409 conflict_error`，使用同一请求重试。删除成功后再次 DELETE 仍返回 `200` 删除信封；再次 GET 返回 `404`。未知 Session ID 或跨工作空间的 DELETE 返回 `404`。

## 路径参数

**session\_id** `string` **（必选）**

Session ID，按不透明字符串使用

本接口没有请求体和 Query 参数。

## 请求示例

curl

```
curl -sS -X DELETE "$BASE_URL/agents/sessions/sess_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
client.beta.agents.sessions.delete("sess_xxx")
```

### 响应字段

**id** `string`

被删除的 Session ID

**object** `string`

Session 删除结果对象类型，固定为 `agent.session.deleted`

**deleted** `boolean`

是否删除成功，删除成功时为 `true`

## 响应示例

```
{
  "id": "sess_xxx",
  "object": "agent.session.deleted",
  "deleted": true
}
```

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按 Session ID 格式传入有效值

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中未归档的 Session ID

`409`

`conflict_error` / `conflict_error`

使用同一请求重试

`503`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供 `x-request-id`
