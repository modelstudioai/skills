# 删除 Agent

删除 Agent 配置；已有 Session 使用创建时的快照，不受影响。

<a id="接口"></a>

<a id="h-oa-agent-delete-endpoint"></a>

## 接口

**DELETE** `/agents/{agent_id}`

成功返回 `200` 和删除信封。删除为软归档：Agent 标记为已删除并记录删除时间，之后获取或再次删除返回 `404`。

删除只归档 Agent，不停止已有 Session，也不清理环境。已有 Session 使用创建时的 Agent 快照，不受后续删除影响。

<table><tbody><tr><td><a id="h-oa-agent-delete-params"></a><h2>路径参数</h2><p><strong>agent_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Agent ID，按不透明字符串使用</p><p>本接口没有请求体和 Query 参数。</p></td><td><a id="h-oa-agent-delete-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X DELETE &quot;$BASE_URL/agents/agent_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>client.beta.agents.delete(&quot;agent_xxx&quot;)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-agent-delete-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>被删除的 Agent ID</p><p><strong>object</strong> <code>string</code></p><p>Agent 删除结果对象类型，固定为 <code>agent.deleted</code></p><p><strong>deleted</strong> <code>boolean</code></p><p>是否删除成功，删除成功时为 <code>true</code></p></td><td><a id="h-oa-agent-delete-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;agent_xxx&quot;,
  &quot;object&quot;: &quot;agent.deleted&quot;,
  &quot;deleted&quot;: true
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-agent-delete-errors"></a>

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Agent ID |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
