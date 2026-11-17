# 列出 Subagent Turn 的 Item

分页查询指定子 Agent Turn 的 Item，核对消息、工具调用和推理摘要。

## 接口

`GET /agents/sessions/{session_id}/subagents/{subagent_id}/turns/{turn_id}/items`

返回指定子 Agent Turn 的 Item。成功返回 `200`。查询不启动或恢复子 Agent，也不创建资源。

## 路径参数

**session\_id** `string` **（必选）**

Session ID，例如 `sess_xxx`

**subagent\_id** `string` **（必选）**

稳定的子 Agent ID，例如 `subagent_xxx`

**turn\_id** `string` **（必选）**

公开 Turn ID，例如 `turn_xxx`

路径上下级必须匹配。Turn 不属于该子 Agent 或该 Session 时不返回数据。

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
curl --get "$BASE_URL/agents/sessions/sess_xxx/subagents/subagent_xxx/turns/turn_xxx/items" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --data-urlencode "limit=20" \
  --data-urlencode "order=asc"
```

Python

```
items = client.beta.agents.sessions.subagents.turns.items.list(
    "turn_xxx",
    session_id="sess_xxx",
    subagent_id="subagent_xxx",
    limit=20,
    order="asc",
)
for item in items.data:
    print(item.type, item.id)
```

### 响应字段

列表信封：

**object** `string`

列表对象类型，固定为 `list`

**data** `array<Item>`

当页 Item；空时为 `[]`

**first\_id** `string / null`

当页首项 ID。空页为 `null`

**last\_id** `string / null`

当页末项 ID。空页为 `null`。后续 `after` 使用该值

**has\_more** `boolean`

当前检索方向是否还有下一页

每个 Item 都有 `id`、`turn_id` 和 `type`，业务字段平铺在对象顶层。Item 类型和内容片段说明见[列出 Item](raw/_short/openai-compatible-agents-api-item-list-f6132444f11ece8f.md)。

持久 Item 采用终结内容。SSE 的 `item.added` 可展示进行中状态，实时未完成 Item 不保证可在列表查询到。

## 响应示例

```
{
  "object": "list",
  "data": [
    {
      "id": "msg_xxx",
      "turn_id": "turn_xxx",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "phase": "final_answer",
      "content": [{"type": "output_text", "text": "完成"}]
    }
  ],
  "first_id": "msg_xxx",
  "last_id": "msg_xxx",
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

按查询参数说明修正 `limit`、`order`；使用本集合上一页返回的 `last_id` 作为 `after`

`404`

`not_found_error` / `not_found_error`

确认 Session、Subagent、Turn 存在且属于同一工作空间，并使用匹配的路径层级

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id`
