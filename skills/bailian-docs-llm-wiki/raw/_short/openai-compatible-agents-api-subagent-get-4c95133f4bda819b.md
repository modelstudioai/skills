# 获取 Subagent

获取单个子 Agent 的详情，查看父 Agent、公开指令和生命周期状态。

## 接口

`GET /agents/sessions/{session_id}/subagents/{subagent_id}`

成功返回 `200`，响应体是单个 Subagent。查询不启动或恢复子 Agent，也不创建资源。

## 路径参数

**session\_id** `string` **（必选）**

Session ID，例如 `sess_xxx`

**subagent\_id** `string` **（必选）**

稳定的子 Agent ID，例如 `subagent_xxx`

路径上下级必须匹配。子 Agent 不属于该 Session，或跨工作空间时不会返回数据。

## 请求示例

curl

```
curl "$BASE_URL/agents/sessions/sess_xxx/subagents/subagent_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
subagent = client.beta.agents.sessions.subagents.retrieve(
    "subagent_xxx", session_id="sess_xxx"
)
print(subagent.status)
```

### 响应字段

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

`active` 可以空闲等待，不表示持续运行。`closed_at` 在未关闭时为 `null`。

## 响应示例

```
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
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`404`

`not_found_error` / `not_found_error`

确认 Session、Subagent 存在且属于同一工作空间，并使用匹配的路径层级

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id`
