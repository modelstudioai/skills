# 列出 Vault

分页列出工作空间中的 Vault，支持按元数据和归档状态筛选。

<a id="接口"></a>

<a id="h-oa-vl-endpoint"></a>

## 接口

**GET** `/vaults`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

<table><tbody><tr><td><a id="h-oa-vl-req"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，默认 20，范围 1–100。空字符串、0、负数、非数字或超出范围返回 <code>400</code></p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code>。从该项之后开始，不包含该项</p><p><strong>metadata[key]</strong> <code>string</code> <strong>（可选）</strong></p><p>元数据过滤条件，按 metadata 精确匹配，多个条件之间为 AND</p><p><strong>status</strong> <code>string</code> <strong>（可选）</strong></p><p>Vault 状态：<code>active</code> 或 <code>archived</code>，默认两者都包含。也支持重复传入 <code>status[]</code>，值会合并为筛选集合</p><p><code>before</code> 不是支持参数。</p></td><td><a id="h-oa-vault-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/vaults?limit=20&amp;order=desc&amp;status=active&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.get(
    f&quot;{os.environ['BASE_URL']}/vaults&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
    params={&quot;limit&quot;: 20, &quot;order&quot;: &quot;desc&quot;, &quot;status&quot;: &quot;active&quot;},
)
print(resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-vl-resp"></a><h3>响应字段</h3><p><code>200</code>，返回列表信封：</p><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array</code></p><p>当前页的 Vault 数组</p><p><strong>first_id</strong> <code>string / null</code></p><p>当前页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当前页末项 ID，下一页的 <code>after</code> 使用该值。空页为 <code>null</code></p><p><strong>has_more</strong> <code>boolean</code></p><p>是否还有更多匹配资源</p><a id="h-oa-vault-list-fields"></a><h3>Vault 字段</h3><p><strong>id</strong> <code>string</code></p><p>Vault ID</p><p><strong>object</strong> <code>string</code></p><p>Vault 对象类型，固定为 <code>vault</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>name</strong> <code>string / null</code></p><p>显示名称</p><p><strong>metadata</strong> <code>object</code></p><p>元数据，字符串键值对；未设置时为 <code>{}</code></p><p>空页返回 <code>data: []</code>，<code>first_id</code> 和 <code>last_id</code> 为 <code>null</code>，<code>has_more</code> 为 <code>false</code>。</p></td><td><a id="h-oa-vault-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;vlt_xxx&quot;,
      &quot;object&quot;: &quot;vault&quot;,
      &quot;created_at&quot;: 1793941200,
      &quot;name&quot;: &quot;production-secrets&quot;,
      &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;}
    }
  ],
  &quot;first_id&quot;: &quot;vlt_xxx&quot;,
  &quot;last_id&quot;: &quot;vlt_xxx&quot;,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-vl-errors"></a>

## 错误码

错误响应结构见[错误码](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order` 或 metadata 过滤条件 |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前集合上一页返回的 `last_id` 作为 `after` |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
