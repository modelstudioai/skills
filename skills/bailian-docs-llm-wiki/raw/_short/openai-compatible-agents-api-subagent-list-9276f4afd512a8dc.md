# 列出 Subagent

分页查询 Session 的子 Agent 列表，查看名称、状态和生命周期时间。

## 接口

`GET /agents/sessions/{session_id}/subagents`

返回 Session 的子 Agent 列表。根 Agent 不作为子 Agent 返回。成功返回 `200`。查询不启动或恢复子 Agent，也不创建资源。

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
curl --get "$BASE_URL/agents/sessions/sess_xxx/subagents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --data-urlencode "limit=20" \
  --data-urlencode "order=asc"
```

Python

```
subagents = client.beta.agents.sessions.subagents.list(
    "sess_xxx", limit=20, order="asc"
)
for subagent in subagents.data:
    print(subagent.id, subagent.status)
```

### 响应字段

列表信封：

**object** `string`

列表对象类型，固定为 `list`

**data** `array<Subagent>`

当页子 Agent；空时为 `[]`

**first\_id** `string / null`

当页首项 ID。空页为 `null`

**last\_id** `string / null`

当页末项 ID。空页为 `null`。后续 `after` 使用该值

**has\_more** `boolean`

当前检索方向是否还有下一页

Subagent 字段：

`active` 可以空闲等待，不表示持续运行。历史查询不自行启动或恢复子 Agent。

data 项

**id** `string`

稳定的子 Agent ID

**object** `string`

Subagent 对象类型，固定为 `agent.session.subagent`

**session\_id** `string`

所属 Session

**parent\_agent\_id** `string`

父 Agent

**name** `string / null`

展示名

**instructions** `array / null`

公开指令内容

**status** `string`

Subagent 状态：`active` 或 `closed`

**opened\_at** `integer`

打开时间，Unix 秒

**closed\_at** `integer / null`

关闭时间，Unix 秒；未关闭时为 `null`

## 响应示例

```
{
  "object": "list",
  "data": [
    {
      "id": "subagent_xxx",
      "object": "agent.session.subagent",
      "session_id": "sess_xxx",
      "parent_agent_id": "agent_xxx",
      "name": "researcher",
      "instructions": null,
      "status": "active",
      "opened_at": 1794118835,
      "closed_at": null
    }
  ],
  "first_id": "subagent_xxx",
  "last_id": "subagent_xxx",
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

使用当前工作空间中存在且未删除的 Session ID

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id`
