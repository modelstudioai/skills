# 列出 Agent

分页列出当前工作空间中的 Agent。

<a id="接口"></a>

<a id="h-oa-agent-list-endpoint"></a>

## 接口

**GET** `/agents`

成功返回 `200` 和列表信封，`data` 为 Agent 对象数组。

<table><tbody><tr><td><a id="h-oa-agent-list-query"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，默认 20；建议使用 <code>1..100</code></p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code>；不包含游标项</p><p><strong>before</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>first_id</code>，用于反向翻页，不能与 <code>after</code> 同时使用；游标必须是当前工作空间中有效的 Agent</p><p>同时传 <code>after</code> 和 <code>before</code> 返回 <code>400</code>。翻页时首次不传 <code>after</code>，后续传上一页的 <code>last_id</code>；反向翻页使用 <code>first_id</code> 作为 <code>before</code>。<code>has_more</code> 表示当前扫描方向还有结果。列表按 Agent ID 字典序排序，不保证按 <code>created_at</code> 稳定排序，也不提供并发写入下的快照隔离。</p></td><td><a id="h-oa-agent-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/agents?limit=20&amp;order=desc&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>page = client.beta.agents.list(limit=20, order=&quot;desc&quot;)
for agent in page.data:
    print(agent.id, agent.name)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-agent-list-response"></a><h3>响应字段</h3><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array</code></p><p>当页 Agent 对象，空时为 <code>[]</code></p><p><strong>first_id</strong> <code>string / null</code></p><p>当页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当页末项 ID。空页为 <code>null</code></p><p><strong>has_more</strong> <code>boolean</code></p><p>当前扫描方向是否还有下一页</p><a id="h-oa-agent-list-fields"></a><h3>Agent 字段</h3><p><strong>id</strong> <code>string</code></p><p>Agent ID，按不透明字符串使用</p><p><strong>object</strong> <code>string</code></p><p>Agent 对象类型，固定为 <code>agent</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间的 Unix 秒时间戳</p><p><strong>updated_at</strong> <code>integer</code></p><p>最近修改时间的 Unix 秒时间戳，不是版本号</p><p><strong>name</strong> <code>string / null</code></p><p>展示名称</p><p><strong>metadata</strong> <code>object / null</code></p><p>元数据，保存的字符串键值对</p><p><strong>model</strong> <code>string</code></p><p>保存的模型 ID</p><p><strong>reasoning</strong> <code>object / null</code></p><p>推理配置。两项均可为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>effort</strong> <code>string / null</code></p><p>推理强度：<code>none</code>、<code>minimal</code>、<code>low</code>、<code>medium</code>、<code>high</code>、<code>xhigh</code>、<code>max</code></p><p><strong>summary</strong> <code>string / null</code></p><p>推理摘要：<code>concise</code>、<code>detailed</code>、<code>auto</code></p></div></section><p><strong>text</strong> <code>object / null</code></p><p>文本输出配置。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>format</strong> <code>object</code></p><p>输出格式。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong> <code>string / null</code></p><p>输出格式类型，固定为 <code>text</code></p></div></section><p><strong>verbosity</strong> <code>string / null</code></p><p>输出详细程度，<code>low</code>、<code>medium</code>、<code>high</code></p></div></section><p><strong>instructions</strong> <code>string / null</code></p><p>保存的自定义指令</p><p><strong>tools</strong> <code>array / null</code></p><p>保存的工具配置；每个分支只返回本分支字段</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>function</strong> <code>object</code></p><p>Function 工具配置，返回 <code>name</code>、<code>description</code>、<code>parameters</code></p><p><strong>mcp</strong> <code>object</code></p><p>MCP 工具配置，返回 <code>server_label</code>、<code>transport</code>、<code>allowed_tools</code>、<code>required</code>、<code>connection_origin</code>；<code>transport</code> 为 <code>http</code> 或 <code>stdio</code></p><p><strong>web_search</strong> <code>object</code></p><p>Web Search 工具配置，返回 <code>type</code> 和已保存的配置</p></div></section><p><strong>multi_agent</strong> <code>object / null</code></p><p>子 Agent 配置。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>enabled</strong> <code>boolean</code></p><p>是否启用子 Agent 工具</p><p><strong>max_concurrent_subagents</strong> <code>integer / null</code></p><p>最大并发子 Agent 数；不补默认值</p></div></section><p>未设置的可选字段可能返回 <code>null</code>。</p></td><td><a id="h-oa-agent-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [],
  &quot;first_id&quot;: null,
  &quot;last_id&quot;: null,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-agent-list-errors"></a>

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order` |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用本集合上一页返回的 `last_id` 作为 `after` |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
