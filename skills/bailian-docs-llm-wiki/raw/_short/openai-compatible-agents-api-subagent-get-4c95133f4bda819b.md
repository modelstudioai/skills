# 获取 Subagent

获取单个子 Agent 的详情，查看父 Agent、公开指令和生命周期状态。

<a id="接口"></a>

<a id="h-oa-subagent-get-endpoint"></a>

## 接口

`GET /agents/sessions/{session_id}/subagents/{subagent_id}`

成功返回 `200`，响应体是单个 Subagent。查询不启动或恢复子 Agent，也不创建资源。

<table><tbody><tr><td><a id="h-oa-subagent-get-path"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Session ID，例如 <code>sess_xxx</code></p><p><strong>subagent_id</strong> <code>string</code> <strong>（必选）</strong></p><p>稳定的子 Agent ID，例如 <code>subagent_xxx</code></p><p>路径上下级必须匹配。子 Agent 不属于该 Session，或跨工作空间时不会返回数据。</p></td><td><a id="h-oa-subagent-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$BASE_URL/agents/sessions/sess_xxx/subagents/subagent_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>subagent = client.beta.agents.sessions.subagents.retrieve(
    &quot;subagent_xxx&quot;, session_id=&quot;sess_xxx&quot;
)
print(subagent.status)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-subagent-get-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>稳定的子 Agent ID</p><p><strong>object</strong> <code>string</code></p><p>Subagent 对象类型，固定为 <code>agent.session.subagent</code></p><p><strong>session_id</strong> <code>string</code></p><p>所属 Session</p><p><strong>parent_agent_id</strong> <code>string</code></p><p>父 Agent</p><p><strong>name</strong> <code>string / null</code></p><p>展示名</p><p><strong>instructions</strong> <code>array / null</code></p><p>公开指令内容</p><p><strong>status</strong> <code>string</code></p><p>Subagent 状态：<code>active</code> 或 <code>closed</code></p><p><strong>opened_at</strong> <code>integer</code></p><p>打开时间，Unix 秒</p><p><strong>closed_at</strong> <code>integer / null</code></p><p>关闭时间，Unix 秒；未关闭时为 <code>null</code></p><p><code>active</code> 可以空闲等待，不表示持续运行。<code>closed_at</code> 在未关闭时为 <code>null</code>。</p></td><td><a id="h-oa-subagent-get-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;subagent_xxx&quot;,
  &quot;object&quot;: &quot;agent.session.subagent&quot;,
  &quot;session_id&quot;: &quot;sess_xxx&quot;,
  &quot;parent_agent_id&quot;: &quot;agent_xxx&quot;,
  &quot;name&quot;: &quot;researcher&quot;,
  &quot;instructions&quot;: null,
  &quot;status&quot;: &quot;active&quot;,
  &quot;opened_at&quot;: 1794118835,
  &quot;closed_at&quot;: null
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-subagent-get-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `404` | `not_found_error` / `not_found_error` | 确认 Session、Subagent 存在且属于同一工作空间，并使用匹配的路径层级 |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id` |
