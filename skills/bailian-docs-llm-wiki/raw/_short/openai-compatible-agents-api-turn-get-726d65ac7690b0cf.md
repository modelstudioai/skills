# 获取 Turn

获取根 Agent 的单个 Turn，查看状态、时间边界、错误和 Token 用量。

<a id="接口"></a>

<a id="h-oa-turn-get-endpoint"></a>

## 接口

`GET /agents/sessions/{session_id}/turns/{turn_id}`

成功返回 `200`，响应体是单个 Turn。查询不启动模型、不恢复执行，也不创建资源。

<table><tbody><tr><td><a id="h-oa-turn-get-path"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Session ID，例如 <code>sess_xxx</code></p><p><strong>turn_id</strong> <code>string</code> <strong>（必选）</strong></p><p>公开 Turn ID，例如 <code>turn_xxx</code></p><p>路径上下级必须匹配。跨工作空间、其他调用方的 Turn，以及父资源不存在的请求不会返回数据。</p></td><td><a id="h-oa-turn-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$BASE_URL/agents/sessions/sess_xxx/turns/turn_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>turn = client.beta.agents.sessions.turns.retrieve(
    &quot;turn_xxx&quot;, session_id=&quot;sess_xxx&quot;
)
print(turn.status)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-turn-get-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>公开 Turn ID</p><p><strong>object</strong> <code>string</code></p><p>对象类型，固定为 <code>agent.session.turn</code></p><p><strong>session_id</strong> <code>string</code></p><p>所属 Session</p><p><strong>agent_id</strong> <code>string</code></p><p>执行 Agent</p><p><strong>subagent_id</strong> <code>string / null</code></p><p>子 Agent ID。根 Turn 为 <code>null</code></p><p><strong>status</strong> <code>string</code></p><p>Turn 状态：<code>in_progress</code>、<code>waiting</code>、<code>completed</code>、<code>failed</code>、<code>cancelled</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>started_at<code>/</code>completed_at</strong> <code>integer / null</code></p><p>开始时间和完成时间，Unix 秒。未到边界时为 <code>null</code></p><p><strong>error</strong> <code>object / null</code></p><p>Turn 级错误；<code>null</code> 表示无错误</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>code</strong> <code>string</code></p><p>错误码</p><p><strong>message</strong> <code>string</code></p><p>错误说明</p></div></section><p><strong>usage</strong> <code>object / null</code></p><p>Token 用量；相关计数不齐时为 <code>null</code></p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数</p><a id="accordion-input-tokens-details"></a><section><p>input_tokens_details</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的输入 Token 数</p></div></section><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数</p><a id="accordion-output-tokens-details"></a><section><p>output_tokens_details</p><div><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>推理 Token 数</p></div></section><p><strong>total_tokens</strong> <code>integer</code></p><p>总 Token 数</p></div></section><p><code>usage</code> 包含 <code>input_tokens</code>、<code>input_tokens_details.cached_tokens</code>、<code>output_tokens</code>、<code>output_tokens_details.reasoning_tokens</code> 和 <code>total_tokens</code>。相关计数不齐时，整个 <code>usage</code> 为 <code>null</code>。</p><p><code>waiting</code> 不是成功终态。<code>completed</code>、<code>failed</code>、<code>cancelled</code> 才是终态。SSE 的 <code>turn.created</code> 事件中可能出现 <code>queued</code>，持久 Turn 从 <code>in_progress</code> 开始。</p></td><td><a id="h-oa-turn-get-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
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
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-turn-get-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `404` | `not_found_error` / `not_found_error` | 确认 Session、Turn 存在且属于同一工作空间，并使用匹配的路径层级 |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id` |
