# 列出 Environment template

分页列出当前工作空间的环境模板。

<a id="接口"></a>

<a id="h-oa-env-template-list-endpoint"></a>

## 接口

**GET** `/agents/environments/templates`

成功返回 `200` 和列表信封。

<table><tbody><tr><td><a id="h-oa-env-template-list-query"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，默认 20；建议使用 <code>1..100</code></p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code>；不包含游标项</p><p><strong>before</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>first_id</code>，用于反向翻页，不能与 <code>after</code> 同时使用</p><p>同时传 <code>after</code> 和 <code>before</code> 返回 <code>400</code>。游标无效或模板不存在时返回 <code>404</code>。</p></td><td><a id="h-oa-environment-template-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/agents/environments/templates?limit=20&amp;order=desc&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>page = client.beta.agents.environments.templates.list(limit=20, order=&quot;desc&quot;)
for template in page.data:
    print(template.id, template.name)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-env-template-list-response"></a><h3>响应字段</h3><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array</code></p><p>当页环境模板；空时为 <code>[]</code></p><p><strong>first_id</strong> <code>string / null</code></p><p>当页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当页末项 ID。空页为 <code>null</code>。后续 <code>after</code> 使用该值</p><p><strong>has_more</strong> <code>boolean</code></p><p>当前检索方向是否还有下一页</p><p><code>data[]</code> 中每个环境模板包含 <code>id</code>、<code>object</code>、<code>name</code>、<code>created_at</code>、<code>updated_at</code>、<code>packages</code>、<code>network</code>、<code>desktop</code>、<code>capability_directories</code>、<code>skills</code>、<code>plugins</code>、<code>files</code>，字段含义与获取环境模板一致。</p></td><td><a id="h-oa-environment-template-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;envtmpl_xxx&quot;,
      &quot;name&quot;: &quot;example-template&quot;,
      &quot;object&quot;: &quot;agent.environment.template&quot;,
      &quot;created_at&quot;: 1794452344,
      &quot;updated_at&quot;: 1794452344,
      &quot;packages&quot;: {&quot;python&quot;: [], &quot;system&quot;: [], &quot;npm&quot;: []},
      &quot;network&quot;: {&quot;access&quot;: &quot;disabled&quot;, &quot;allowed_domains&quot;: []},
      &quot;desktop&quot;: {&quot;enabled&quot;: false},
      &quot;capability_directories&quot;: [&quot;/workspace/skills&quot;],
      &quot;skills&quot;: [],
      &quot;plugins&quot;: [],
      &quot;files&quot;: []
    }
  ],
  &quot;first_id&quot;: &quot;envtmpl_xxx&quot;,
  &quot;last_id&quot;: &quot;envtmpl_xxx&quot;,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-env-template-list-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order`、`after`、`before` |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前集合中有效的游标 |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
