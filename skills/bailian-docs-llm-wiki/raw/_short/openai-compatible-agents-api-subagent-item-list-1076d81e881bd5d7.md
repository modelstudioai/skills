# 列出 Subagent 的 Item

分页查询指定子 Agent 跨 Turn 的 Item 历史，工具执行记录不混入根 Agent。

<a id="接口"></a>

<a id="h-oa-subagent-item-list-endpoint"></a>

## 接口

`GET /agents/sessions/{session_id}/subagents/{subagent_id}/items`

返回指定子 Agent 跨 Turn 的 Item。子 Agent 的工具执行记录保存在自己的路径下，不混入根 Agent 的 Item。成功返回 `200`。查询不启动或恢复子 Agent，也不创建资源。

<table><tbody><tr><td><a id="h-oa-subagent-item-list-path"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Session ID，例如 <code>sess_xxx</code></p><p><strong>subagent_id</strong> <code>string</code> <strong>（必选）</strong></p><p>稳定的子 Agent ID，例如 <code>subagent_xxx</code></p><p>路径上下级必须匹配。子 Agent 不属于该 Session 时不返回数据。</p><a id="h-oa-subagent-item-list-query"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，范围 1–100，默认 20</p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code>；结果不包含游标项</p><p><code>before</code> 会被忽略，不用于反向分页。使用 <code>order</code> 和 <code>after</code> 翻页。</p></td><td><a id="h-oa-subagent-item-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl --get &quot;$BASE_URL/agents/sessions/sess_xxx/subagents/subagent_xxx/items&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  --data-urlencode &quot;limit=20&quot; \
  --data-urlencode &quot;order=asc&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>items = client.beta.agents.sessions.subagents.items.list(
    &quot;subagent_xxx&quot;,
    session_id=&quot;sess_xxx&quot;,
    limit=20,
    order=&quot;asc&quot;,
)
for item in items.data:
    print(item.type, item.id)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-subagent-item-list-response"></a><h3>响应字段</h3><p>列表信封：</p><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array&lt;Item&gt;</code></p><p>当页 Item；空时为 <code>[]</code></p><p><strong>first_id</strong> <code>string / null</code></p><p>当页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当页末项 ID。空页为 <code>null</code>。后续 <code>after</code> 使用该值</p><p><strong>has_more</strong> <code>boolean</code></p><p>当前检索方向是否还有下一页</p><p>每个 Item 都有 <code>id</code>、<code>turn_id</code> 和 <code>type</code>，业务字段平铺在对象顶层。Item 类型和内容片段说明见<a href="openai-compatible-agents-api-item-list-f6132444f11ece8f.md">列出 Item</a>。</p><p>持久 Item 采用终结内容。SSE 的 <code>item.added</code> 可展示进行中状态，实时未完成 Item 不保证可在列表查询到。</p></td><td><a id="h-oa-subagent-item-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;msg_xxx&quot;,
      &quot;turn_id&quot;: &quot;turn_xxx&quot;,
      &quot;type&quot;: &quot;message&quot;,
      &quot;status&quot;: &quot;completed&quot;,
      &quot;role&quot;: &quot;assistant&quot;,
      &quot;phase&quot;: &quot;final_answer&quot;,
      &quot;content&quot;: [{&quot;type&quot;: &quot;output_text&quot;, &quot;text&quot;: &quot;完成&quot;}]
    }
  ],
  &quot;first_id&quot;: &quot;msg_xxx&quot;,
  &quot;last_id&quot;: &quot;msg_xxx&quot;,
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

<a id="h-oa-subagent-item-list-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order`；使用本集合上一页返回的 `last_id` 作为 `after` |
| `404` | `not_found_error` / `not_found_error` | 确认 Session、Subagent 存在且属于同一工作空间，并使用匹配的路径层级 |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id` |
