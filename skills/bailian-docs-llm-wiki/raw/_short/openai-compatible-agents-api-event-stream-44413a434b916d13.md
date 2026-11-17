# 订阅 Event stream

通过 Server-Sent Events 订阅 Session 的实时事件流，接收 Turn、Item、文本增量和状态变更。

## 接口

`GET /agents/sessions/{session_id}/events`

成功返回 `200 text/event-stream`。订阅不创建 Turn，也不启动模型。

推荐先建立 SSE 连接并确认就绪，再 `POST` 事件。

## 路径参数

**session\_id** `string` **（必选）**

Session ID，例如 `sess_xxx`

## 查询参数

**Accept** `string` **（必选）**

请求头，固定为 `text/event-stream`

**OpenAI-Beta** `string` **（必选）**

兼容客户端可以发送 `agents=v1`

## 请求示例

curl

```
curl -N "$BASE_URL/agents/sessions/sess_xxx/events" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Accept: text/event-stream"
```

Python

```
with client.beta.agents.sessions.events.stream("sess_xxx") as stream:
    for event in stream:
        print(event.type)
```

### 响应字段

连接建立后先收到注释行 `: connected`，它不是 JSON 事件。

**type** `string`

事件类型

**event\_id** `string`

事件身份

**session\_id** `string`

Session 身份

**turn\_id** `string / null`

涉及 Turn 时存在

每个事件包含公共字段：

## 响应示例

```
: connected

data: {"type":"agent.session.turn.output_text.delta","event_id":"evt_xxx","session_id":"sess_xxx","turn_id":"turn_xxx","item_id":"msg_xxx","output_index":0,"content_index":0,"delta":"你好"}
```

## 常用事件

事件按所属对象分组，展开查看事件名称和负载。

Session 事件

事件

含义

`agent.session.created`

Session 创建，`session` 为完整快照

`agent.session.in_progress`

Session 进入执行中

`agent.session.idle`

Session 回到空闲

`agent.session.failed`

Session 失败

`agent.session.requires_action`

Session 需要客户端处理，`session` 为完整快照

事件携带 `session` 完整快照。

环境事件

事件

含义

`agent.session.environment.ready` / `failed`

环境状态变化，`environment` 为安全状态摘要

事件携带 `environment` 安全状态摘要。

Turn 事件

事件

含义

`agent.session.turn.created`

Turn 创建，`turn.status` 可为 `queued`

`agent.session.turn.in_progress`

Turn 执行中

`agent.session.turn.completed`

Turn 完成

`agent.session.turn.failed`

Turn 失败

`agent.session.turn.cancelled`

Turn 已取消

事件携带 `turn` 完整公开对象；`turn.created` 中 `turn.status` 可为 `queued`，持久 Turn 从 `in_progress` 开始；`turn.completed` 可能包含 `usage`。

Item 事件

事件

含义

`agent.session.turn.item.added`

Item 加入

`agent.session.turn.item.done`

Item 完成

事件携带 `item` 和 `output_index`；`item.added` 可能是进行中状态，`item.done` 是完成状态。

内容片段事件

事件

含义

`agent.session.turn.content_part.added`

内容片段开始

`agent.session.turn.content_part.done`

内容片段完成

事件携带 `item_id`、`output_index`、`content_index` 和 `part`。

文本事件

事件

含义

`agent.session.turn.output_text.delta`

输出文本增量

`agent.session.turn.output_text.done`

输出文本完成

增量事件携带 `delta`；完成事件携带完整 `text`。

推理摘要事件

事件

含义

`agent.session.turn.reasoning_summary_part.added` / `done`

推理摘要片段开始或完成

`agent.session.turn.reasoning_summary_text.delta`

推理摘要增量

`agent.session.turn.reasoning_summary_text.done`

推理摘要完成

事件携带 `summary_index`；`part` 为摘要片段。

## 断线重连

SSE 不重放断线期间的增量。连接中断后，重新获取 Session、Turns 和 Items 补齐已持久化结果；不要依赖 `Last-Event-ID` 恢复。GET 订阅不会因 Session idle 或单个 Turn 终态自动结束。`[DONE]` 不是成功判据。

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且未删除的 Session ID

`502`

`server_error` / `agents_api_upstream_unavailable`

重新建立 SSE 连接；持续失败时提交工单并提供 `x-request-id`

连接中断时 HTTP 流直接结束，重新订阅不会补发离线期间的事件。
