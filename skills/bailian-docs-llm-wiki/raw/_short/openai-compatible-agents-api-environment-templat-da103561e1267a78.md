# 删除 Environment template

删除指定的环境模板。

<a id="接口"></a>

<a id="h-oa-env-template-delete-endpoint"></a>

## 接口

**DELETE** `/agents/environments/templates/{template_id}`

成功返回 `200` 和删除信封。删除后再次获取或删除返回 `404`。

<table><tbody><tr><td><a id="h-oa-env-template-delete-path"></a><h2>路径参数</h2><p><strong>template_id</strong> <code>string</code> <strong>（必选）</strong></p><p>环境模板 ID</p><p>本接口没有请求体和 Query 参数。</p></td><td><a id="h-oa-environment-template-delete-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X DELETE &quot;$BASE_URL/agents/environments/templates/envtmpl_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>client.beta.agents.environments.templates.delete(&quot;envtmpl_xxx&quot;)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-env-template-delete-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>被删除的环境模板 ID</p><p><strong>object</strong> <code>string</code></p><p>环境模板删除结果对象类型，固定为 <code>agent.environment.template.deleted</code></p><p><strong>deleted</strong> <code>boolean</code></p><p>是否删除成功，删除成功时为 <code>true</code></p></td><td><a id="h-oa-environment-template-delete-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;envtmpl_xxx&quot;,
  &quot;object&quot;: &quot;agent.environment.template.deleted&quot;,
  &quot;deleted&quot;: true
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-env-template-delete-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在的环境模板 ID |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
