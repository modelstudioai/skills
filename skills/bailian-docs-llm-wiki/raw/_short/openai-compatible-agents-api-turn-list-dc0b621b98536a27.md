# 列出 Turn

分页查询根 Agent 的 Turn 列表，核对执行状态和 Token 用量。

<a id="接口"></a>

<a id="h-oa-turn-list-endpoint"></a>

## 接口

`GET /agents/sessions/{session_id}/turns`

返回根 Agent 的 Turn 列表。成功返回 `200`。查询不启动模型、不恢复执行，也不创建资源。

<table><tbody><tr><td><a id="h-oa-turn-list-path"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Session ID，例如 <code>sess_xxx</code></p><a id="h-oa-turn-list-query"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，范围 1–100，默认 20</p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code>；结果不包含游标项</p><p><code>before</code> 会被忽略，不用于反向分页。使用 <code>order</code> 和 <code>after</code> 翻页。</p></td><td><a id="h-oa-turn-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl --get &quot;$BASE_URL/agents/sessions/sess_xxx/turns&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  --data-urlencode &quot;limit=20&quot; \
  --data-urlencode &quot;order=asc&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>turns = client.beta.agents.sessions.turns.list(
    &quot;sess_xxx&quot;, limit=20, order=&quot;asc&quot;
)
for turn in turns.data:
    print(turn.id, turn.status)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-turn-list-response"></a><h3>响应字段</h3><p>列表信封： <code>usage</code> 包含 <code>input_tokens</code>、<code>input_tokens_details.cached_tokens</code>、<code>output_tokens</code>、<code>output_tokens_details.reasoning_tokens</code> 和 <code>total_tokens</code>。相关计数不齐时，整个 <code>usage</code> 为 <code>null</code>。</p><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array&lt;Turn&gt;</code></p><p>当页 Turn；空时为 <code>[]</code></p><p><strong>first_id</strong> <code>string / null</code></p><p>当页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当页末项 ID。空页为 <code>null</code>。后续 <code>after</code> 使用该值</p><p><strong>has_more</strong> <code>boolean</code></p><p>当前检索方向是否还有下一页</p><p>Turn 字段：</p><p><code>waiting</code> 不是成功终态。<code>completed</code>、<code>failed</code>、<code>cancelled</code> 才是终态。SSE 的 <code>turn.created</code> 事件中可能出现 <code>queued</code>，持久 Turn 从 <code>in_progress</code> 开始。</p><a id="accordion-data-项"></a><section><p>data 项</p><div><p><strong>id</strong> <code>string</code></p><p>公开 Turn ID</p><p><strong>object</strong> <code>string</code></p><p>Turn 对象类型，固定为 <code>agent.session.turn</code></p><p><strong>session_id</strong> <code>string</code></p><p>所属 Session</p><p><strong>agent_id</strong> <code>string</code></p><p>执行 Agent</p><p><strong>subagent_id</strong> <code>string / null</code></p><p>子 Agent ID，根 Turn 为 <code>null</code></p><p><strong>status</strong> <code>string</code></p><p>Turn 状态：<code>in_progress</code>、<code>waiting</code>、<code>completed</code>、<code>failed</code>、<code>cancelled</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>started_at<code>/</code>completed_at</strong> <code>integer / null</code></p><p>开始时间和完成时间，Unix 秒。未到边界时为 <code>null</code></p><p><strong>error</strong> <code>object / null</code></p><p>Turn 级错误。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>code</strong> <code>string</code></p><p>错误码</p><p><strong>message</strong> <code>string</code></p><p>错误说明</p></div></section><p><strong>usage</strong> <code>object / null</code></p><p>Token 用量。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数</p><p><strong>input_tokens_details</strong> <code>object</code></p><p>输入 Token 明细。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的输入 Token 数</p></div></section><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数</p><p><strong>output_tokens_details</strong> <code>object</code></p><p>输出 Token 明细。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>推理 Token 数</p></div></section><p><strong>total_tokens</strong> <code>integer</code></p><p>总 Token 数</p></div></section></div></section></td><td><a id="h-oa-turn-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;turn_xxx&quot;,
      &quot;object&quot;: &quot;agent.session.turn&quot;,
      &quot;session_id&quot;: &quot;sess_xxx&quot;,
      &quot;agent_id&quot;: &quot;agent_xxx&quot;,
      &quot;subagent_id&quot;: null,
      &quot;status&quot;: &quot;completed&quot;,
      &quot;created_at&quot;: 1794118835,
      &quot;started_at&quot;: 1794118836,
      &quot;completed_at&quot;: 1794118840,
      &quot;error&quot;: null,
      &quot;usage&quot;: {
        &quot;input_tokens&quot;: 1024,
        &quot;input_tokens_details&quot;: {&quot;cached_tokens&quot;: 0},
        &quot;output_tokens&quot;: 256,
        &quot;output_tokens_details&quot;: {&quot;reasoning_tokens&quot;: 64},
        &quot;total_tokens&quot;: 1280
      }
    }
  ],
  &quot;first_id&quot;: &quot;turn_xxx&quot;,
  &quot;last_id&quot;: &quot;turn_xxx&quot;,
  &quot;has_more&quot;: false
}
</code></pre><a id="code-block-2"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [],
  &quot;first_id&quot;: null,
  &quot;last_id&quot;: null,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-turn-list-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order` |
| `404` | `not_found_error` / `not_found_error` | 使用有效的 Session ID；使用本集合上一页返回的 `last_id` 作为 `after` |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id` |
