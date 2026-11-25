# 删除 Session

删除 Session，停止执行并清理公开历史；清理未完成时返回 409。

<a id="接口"></a>

<a id="h-oa-session-delete-endpoint"></a>

## 接口

**DELETE** `/agents/sessions/{session_id}`

成功返回 `200` 和删除信封。删除会停止该 Session 的执行，关闭输入接纳并清理公开历史；

清理尚未完成时返回 `409 conflict_error`，使用同一请求重试。删除成功后再次 DELETE 仍返回 `200` 删除信封；再次 GET 返回 `404`。未知 Session ID 或跨工作空间的 DELETE 返回 `404`。

<table><tbody><tr><td><a id="h-oa-session-delete-params"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Session ID，按不透明字符串使用</p><p>本接口没有请求体和 Query 参数。</p></td><td><a id="h-oa-session-delete-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X DELETE &quot;$BASE_URL/agents/sessions/sess_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>client.beta.agents.sessions.delete(&quot;sess_xxx&quot;)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-session-delete-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>被删除的 Session ID</p><p><strong>object</strong> <code>string</code></p><p>Session 删除结果对象类型，固定为 <code>agent.session.deleted</code></p><p><strong>deleted</strong> <code>boolean</code></p><p>是否删除成功，删除成功时为 <code>true</code></p></td><td><a id="h-oa-session-delete-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sess_xxx&quot;,
  &quot;object&quot;: &quot;agent.session.deleted&quot;,
  &quot;deleted&quot;: true
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-session-delete-errors"></a>

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按 Session ID 格式传入有效值 |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中未归档的 Session ID |
| `409` | `conflict_error` / `conflict_error` | 使用同一请求重试 |
| `503` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
