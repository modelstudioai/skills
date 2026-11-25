# 订阅 Event stream

通过 Server-Sent Events 订阅 Session 的实时事件流，接收 Turn、Item、文本增量和状态变更。

<a id="接口"></a>

<a id="h-oa-event-stream-endpoint"></a>

## 接口

`GET /agents/sessions/{session_id}/events`

成功返回 `200 text/event-stream`。订阅不创建 Turn，也不启动模型。

推荐先建立 SSE 连接并确认就绪，再 `POST` 事件。

<table><tbody><tr><td><a id="h-oa-event-stream-params"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Session ID，例如 <code>sess_xxx</code></p><a id="h-oa-event-stream-params-query"></a><h2>查询参数</h2><p><strong>Accept</strong> <code>string</code> <strong>（必选）</strong></p><p>请求头，固定为 <code>text/event-stream</code></p><p><strong>OpenAI-Beta</strong> <code>string</code> <strong>（必选）</strong></p><p>兼容客户端可以发送 <code>agents=v1</code></p></td><td><a id="h-oa-event-stream-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -N &quot;$BASE_URL/agents/sessions/sess_xxx/events&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  -H &quot;Accept: text/event-stream&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>with client.beta.agents.sessions.events.stream(&quot;sess_xxx&quot;) as stream:
    for event in stream:
        print(event.type)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-event-stream-response"></a><h3>响应字段</h3><p>连接建立后先收到注释行 <code>: connected</code>，它不是 JSON 事件。</p><p><strong>type</strong> <code>string</code></p><p>事件类型</p><p><strong>event_id</strong> <code>string</code></p><p>事件身份</p><p><strong>session_id</strong> <code>string</code></p><p>Session 身份</p><p><strong>turn_id</strong> <code>string / null</code></p><p>涉及 Turn 时存在</p><p>每个事件包含公共字段：</p></td><td><a id="h-oa-event-stream-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-text"><code>: connected

data: {&quot;type&quot;:&quot;agent.session.turn.output_text.delta&quot;,&quot;event_id&quot;:&quot;evt_xxx&quot;,&quot;session_id&quot;:&quot;sess_xxx&quot;,&quot;turn_id&quot;:&quot;turn_xxx&quot;,&quot;item_id&quot;:&quot;msg_xxx&quot;,&quot;output_index&quot;:0,&quot;content_index&quot;:0,&quot;delta&quot;:&quot;你好&quot;}
</code></pre></td></tr></tbody></table>

<a id="常用事件"></a>

<a id="h-oa-event-stream-events"></a>

## 常用事件

事件按所属对象分组，展开查看事件名称和负载。

<a id="accordion-session-事件"></a>

Session 事件

| 事件 | 含义 |
| --- | --- |
| `agent.session.created` | Session 创建，`session` 为完整快照 |
| `agent.session.in_progress` | Session 进入执行中 |
| `agent.session.idle` | Session 回到空闲 |
| `agent.session.failed` | Session 失败 |
| `agent.session.requires_action` | Session 需要客户端处理，`session` 为完整快照 |

事件携带 `session` 完整快照。

<a id="accordion-环境事件"></a>

环境事件

| 事件 | 含义 |
| --- | --- |
| `agent.session.environment.ready` / `failed` | 环境状态变化，`environment` 为安全状态摘要 |

事件携带 `environment` 安全状态摘要。

<a id="accordion-turn-事件"></a>

Turn 事件

| 事件 | 含义 |
| --- | --- |
| `agent.session.turn.created` | Turn 创建，`turn.status` 可为 `queued` |
| `agent.session.turn.in_progress` | Turn 执行中 |
| `agent.session.turn.completed` | Turn 完成 |
| `agent.session.turn.failed` | Turn 失败 |
| `agent.session.turn.cancelled` | Turn 已取消 |

事件携带 `turn` 完整公开对象；`turn.created` 中 `turn.status` 可为 `queued`，持久 Turn 从 `in_progress` 开始；`turn.completed` 可能包含 `usage`。

<a id="accordion-item-事件"></a>

Item 事件

| 事件 | 含义 |
| --- | --- |
| `agent.session.turn.item.added` | Item 加入 |
| `agent.session.turn.item.done` | Item 完成 |

事件携带 `item` 和 `output_index`；`item.added` 可能是进行中状态，`item.done` 是完成状态。

<a id="accordion-内容片段事件"></a>

内容片段事件

| 事件 | 含义 |
| --- | --- |
| `agent.session.turn.content_part.added` | 内容片段开始 |
| `agent.session.turn.content_part.done` | 内容片段完成 |

事件携带 `item_id`、`output_index`、`content_index` 和 `part`。

<a id="accordion-文本事件"></a>

文本事件

| 事件 | 含义 |
| --- | --- |
| `agent.session.turn.output_text.delta` | 输出文本增量 |
| `agent.session.turn.output_text.done` | 输出文本完成 |

增量事件携带 `delta`；完成事件携带完整 `text`。

<a id="accordion-推理摘要事件"></a>

推理摘要事件

| 事件 | 含义 |
| --- | --- |
| `agent.session.turn.reasoning_summary_part.added` / `done` | 推理摘要片段开始或完成 |
| `agent.session.turn.reasoning_summary_text.delta` | 推理摘要增量 |
| `agent.session.turn.reasoning_summary_text.done` | 推理摘要完成 |

事件携带 `summary_index`；`part` 为摘要片段。

<a id="断线重连"></a>

<a id="h-oa-event-stream-reconnect"></a>

## 断线重连

SSE 不重放断线期间的增量。连接中断后，重新获取 Session、Turns 和 Items 补齐已持久化结果；不要依赖 `Last-Event-ID` 恢复。GET 订阅不会因 Session idle 或单个 Turn 终态自动结束。`[DONE]` 不是成功判据。

<a id="错误码"></a>

<a id="h-oa-event-stream-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Session ID |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 重新建立 SSE 连接；持续失败时提交工单并提供 `x-request-id` |

连接中断时 HTTP 流直接结束，重新订阅不会补发离线期间的事件。
