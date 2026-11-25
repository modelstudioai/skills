# 创建 Vault

创建一个 Vault，作为 Credential 的容器。创建空对象可生成匿名 Vault。

<a id="接口"></a>

<a id="h-oa-vc-endpoint"></a>

## 接口

**POST** `/vaults`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

<table><tbody><tr><td><a id="h-oa-vc-req"></a><h2>请求体</h2><p><strong>name</strong> <code>string</code> <strong>（可选）</strong></p><p>显示名称。去除首尾空白后 1–256 字节。省略时响应返回 <code>null</code>，显式传入 <code>null</code> 返回 <code>400</code></p><p><strong>metadata</strong> <code>object / null</code> <strong>（可选）</strong></p><p>元数据，字符串键值对，最多 16 项；key 1–64 字符，value 最多 512 字符。省略或传 <code>null</code> 时响应为 <code>{}</code></p><p>创建空对象 <code>{}</code> 会生成匿名 Vault，响应中的 <code>name</code> 为 <code>null</code>，不会自动生成名称。</p></td><td><a id="h-oa-vault-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/vaults&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;name&quot;: &quot;production-secrets&quot;,
    &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;}
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.post(
    f&quot;{os.environ['BASE_URL']}/vaults&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
    json={&quot;name&quot;: &quot;production-secrets&quot;, &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;}},
)
print(resp.status_code, resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-vc-resp"></a><h3>响应字段</h3><p><code>201</code>，返回 Vault：</p><p><strong>id</strong> <code>string</code></p><p>Vault ID</p><p><strong>object</strong> <code>string</code></p><p>Vault 对象类型，固定为 <code>vault</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>name</strong> <code>string / null</code></p><p>显示名称</p><p><strong>metadata</strong> <code>object</code></p><p>元数据，字符串键值对；未设置时为 <code>{}</code></p></td><td><a id="h-oa-vault-create-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;vlt_xxx&quot;,
  &quot;object&quot;: &quot;vault&quot;,
  &quot;created_at&quot;: 1793941200,
  &quot;name&quot;: &quot;production-secrets&quot;,
  &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;}
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-vc-errors"></a>

## 错误码

错误响应结构见[错误码](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `unknown_parameter` | 移除未知字段 |
| `400` | `invalid_request_error` / `invalid_type` | 按字段说明修正类型 |
| `400` | `invalid_request_error` / `invalid_request_error` | 按字段说明修正 `name` 或 `metadata` |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `409` | `conflict_error` / `conflict_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
