# 列出 Subagent

分页查询 Session 的子 Agent 列表，查看名称、状态和生命周期时间。

<a id="接口"></a>

<a id="h-oa-subagent-list-endpoint"></a>

## 接口

`GET /agents/sessions/{session_id}/subagents`

返回 Session 的子 Agent 列表。根 Agent 不作为子 Agent 返回。成功返回 `200`。查询不启动或恢复子 Agent，也不创建资源。

<table><tbody><tr><td><a id="h-oa-subagent-list-path"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Session ID，例如 <code>sess_xxx</code></p><a id="h-oa-subagent-list-query"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，范围 1–100，默认 20</p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code>；结果不包含游标项</p><p><code>before</code> 会被忽略，不用于反向分页。使用 <code>order</code> 和 <code>after</code> 翻页。</p></td><td><a id="h-oa-subagent-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl --get &quot;$BASE_URL/agents/sessions/sess_xxx/subagents&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  --data-urlencode &quot;limit=20&quot; \
  --data-urlencode &quot;order=asc&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>subagents = client.beta.agents.sessions.subagents.list(
    &quot;sess_xxx&quot;, limit=20, order=&quot;asc&quot;
)
for subagent in subagents.data:
    print(subagent.id, subagent.status)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-subagent-list-response"></a><h3>响应字段</h3><p>列表信封：</p><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array&lt;Subagent&gt;</code></p><p>当页子 Agent；空时为 <code>[]</code></p><p><strong>first_id</strong> <code>string / null</code></p><p>当页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当页末项 ID。空页为 <code>null</code>。后续 <code>after</code> 使用该值</p><p><strong>has_more</strong> <code>boolean</code></p><p>当前检索方向是否还有下一页</p><p>Subagent 字段：</p><p><code>active</code> 可以空闲等待，不表示持续运行。历史查询不自行启动或恢复子 Agent。</p><a id="accordion-data-项"></a><section><p>data 项</p><div><p><strong>id</strong> <code>string</code></p><p>稳定的子 Agent ID</p><p><strong>object</strong> <code>string</code></p><p>Subagent 对象类型，固定为 <code>agent.session.subagent</code></p><p><strong>session_id</strong> <code>string</code></p><p>所属 Session</p><p><strong>parent_agent_id</strong> <code>string</code></p><p>父 Agent</p><p><strong>name</strong> <code>string / null</code></p><p>展示名</p><p><strong>instructions</strong> <code>array / null</code></p><p>公开指令内容</p><p><strong>status</strong> <code>string</code></p><p>Subagent 状态：<code>active</code> 或 <code>closed</code></p><p><strong>opened_at</strong> <code>integer</code></p><p>打开时间，Unix 秒</p><p><strong>closed_at</strong> <code>integer / null</code></p><p>关闭时间，Unix 秒；未关闭时为 <code>null</code></p></div></section></td><td><a id="h-oa-subagent-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [
    {
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
  ],
  &quot;first_id&quot;: &quot;subagent_xxx&quot;,
  &quot;last_id&quot;: &quot;subagent_xxx&quot;,
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

<a id="h-oa-subagent-list-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order`；使用本集合上一页返回的 `last_id` 作为 `after` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Session ID |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id` |
