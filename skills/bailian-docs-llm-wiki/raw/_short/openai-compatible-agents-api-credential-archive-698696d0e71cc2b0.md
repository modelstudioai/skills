# 归档 Credential

归档指定 Credential。该接口是百炼扩展，没有恢复接口。

<a id="接口"></a>

<a id="h-oa-ca-endpoint"></a>

## 接口

**POST** `/vaults/{vault_id}/credentials/{credential_id}/archive`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

<table><tbody><tr><td><a id="h-oa-ca-req"></a><h2>路径参数</h2><p><strong>vault_id</strong> <code>string</code> <strong>（必选）</strong></p><p>父 Vault ID，按不透明 ID 使用</p><p><strong>credential_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Credential ID，按不透明 ID 使用</p><p>本接口没有请求体。</p></td><td><a id="h-oa-credential-archive-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/vaults/vlt_xxx/credentials/vcrd_xxx/archive&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.post(
    f&quot;{os.environ['BASE_URL']}/vaults/vlt_xxx/credentials/vcrd_xxx/archive&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
)
print(resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-ca-resp"></a><h3>响应字段</h3><p><code>200</code>，返回归档后的 Credential：</p><p><strong>id</strong> <code>string</code></p><p>Credential ID</p><p><strong>object</strong> <code>string</code></p><p>Credential 对象类型，固定为 <code>vault.credential</code></p><p><strong>vault_id</strong> <code>string</code></p><p>所属 Vault ID</p><p><strong>name</strong> <code>string</code></p><p>显示名称</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>updated_at</strong> <code>integer</code></p><p>最近更新时间，Unix 秒</p><p><strong>metadata</strong> <code>object</code></p><p>元数据，字符串键值对；未设置时为 <code>{}</code></p><a id="accordion-auth"></a><section><p>auth</p><div><p><strong>type</strong> <code>string</code></p><p>认证类型，固定为 <code>environment_variable</code></p><p><strong>secret_name</strong> <code>string</code></p><p>环境变量名</p><a id="accordion-networking"></a><section><p>networking</p><div><p><strong>type</strong> <code>string</code></p><p>网络访问类型，<code>limited</code> 或 <code>unrestricted</code></p><p><strong>allowed_hosts</strong> <code>array</code></p><p>允许的目标域名或 IPv4，仅 <code>limited</code> 时返回</p></div></section></div></section><p>响应不返回 <code>archived_at</code>、<code>status</code>、<code>secret_value</code>、密钥标识或 <code>injection_location</code>。归档后 Credential 仍可获取，默认列表同时包含 <code>active</code> 和 <code>archived</code>。没有恢复接口。归档 Vault 会级联归档其下 Credential。</p></td><td><a id="h-oa-credential-archive-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;vcrd_xxx&quot;,
  &quot;object&quot;: &quot;vault.credential&quot;,
  &quot;vault_id&quot;: &quot;vlt_xxx&quot;,
  &quot;name&quot;: &quot;crm-token&quot;,
  &quot;created_at&quot;: 1793941200,
  &quot;updated_at&quot;: 1793944800,
  &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;},
  &quot;auth&quot;: {
    &quot;type&quot;: &quot;environment_variable&quot;,
    &quot;secret_name&quot;: &quot;CRM_TOKEN&quot;,
    &quot;networking&quot;: {
      &quot;type&quot;: &quot;limited&quot;,
      &quot;allowed_hosts&quot;: [&quot;api.example.com&quot;]
    }
  }
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-ca-errors"></a>

## 错误码

错误响应结构见[错误码](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | Credential 不存在、已删除、父归属不符或不属于当前工作空间 |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
