# 列出 Item

分页查询根 Agent 跨 Turn 的 Item 历史，用于结果核对和断线恢复。

## 接口

`GET /agents/sessions/{session_id}/items`

返回根 Agent 跨 Turn 的 Item，不混入子 Agent 自己的历史。成功返回 `200`。查询不启动模型、不恢复执行，也不创建资源。

## 路径参数

**session\_id** `string` **（必选）**

Session ID，例如 `sess_xxx`

## 查询参数

**limit** `integer` **（可选）**

每页数量，默认 20，范围 1–100

**order** `string` **（可选）**

排序方向，`asc` 或 `desc`，默认 `desc`

**after** `string` **（可选）**

上一页的 `last_id`；不包含游标项

## 请求示例

curl

```
curl --get "$BASE_URL/agents/sessions/sess_xxx/items" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --data-urlencode "limit=20" \
  --data-urlencode "order=asc"
```

Python

```
items = client.beta.agents.sessions.items.list(
    "sess_xxx", limit=20, order="asc"
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

## Item 类型

每个 Item 都有 `id`、`turn_id` 和 `type`，业务字段平铺在对象顶层。

`type`

字段

`message`

`status`（output 状态）、`role`（`user` / `assistant`）、`phase`（`commentary` / `final_answer` / `null`）、`content`（内容片段数组）

`reasoning`

`status`、`summary`（`type=summary_text` 的片段数组）

`function_call`

`status`、`call_id`、`name`、`arguments`（任意 JSON，可省略）

`function_call_output`

`status`、`call_id`、`output`（内容数组或 `null`；以字符串提交工具结果时，读取时会归一化为数组）、`error`（`string / null`）

`command_execution`

`status`、`command`、`cwd`、`duration_ms`、`exit_code`、`output`

`mcp_call`

`status`、`server_label`、`name`、`arguments`、`output`、`error`

`web_search_call`

`status`、`action`（`search`、`open_page`、`find_in_page` 或 `other`）

`agent_message`

`sender_agent_id`、`recipient_agent_id`、`content`

`create_subagent_call`

`status`、`agent_id`、`content`、`model`、`reasoning_effort`

`send_subagent_input_call`

`status`、`sender_agent_id`、`recipient_agent_id`、`content`

`resume_subagent_call`

`status`、`sender_agent_id`、`recipient_agent_id`

`wait_for_subagents_call`

`status`、`sender_agent_id`、`recipient_agent_ids`

`interrupt_subagent_call`

`status`、`sender_agent_id`、`recipient_agent_id`

`close_subagent_call`

`status`、`sender_agent_id`、`recipient_agent_id`

内容片段按 `type` 区分：`input_text`、`output_text` 包含 `text`；`input_image` 包含 `image_url`；`encrypted_content` 不是可展示文本。

持久 Item 采用终结内容。SSE 的 `item.added` 可展示进行中状态，实时未完成 Item 不保证可在列表查询到。列表可能有短暂延迟，刚创建的数据可能暂时不可见。

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按查询参数说明修正 `limit`、`order`；使用本集合上一页返回的 `last_id` 作为 `after`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且未删除的 Session ID

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id`
