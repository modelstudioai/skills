# 删除 Vault

删除 Vault 及其下全部 Credential。删除后无法恢复。

<a id="接口"></a>

<a id="h-oa-vd-endpoint"></a>

## 接口

**DELETE** `/vaults/{vault_id}`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

<table><tbody><tr><td><a id="h-oa-vd-req"></a><h2>路径参数</h2><p><strong>vault_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Vault ID，按不透明 ID 使用</p></td><td><a id="h-oa-vault-delete-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X DELETE &quot;$BASE_URL/vaults/vlt_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.delete(
    f&quot;{os.environ['BASE_URL']}/vaults/vlt_xxx&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
)
print(resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-vd-resp"></a><h3>响应字段</h3><p><code>200</code>，返回删除信封：</p><p><strong>id</strong> <code>string</code></p><p>被删除的 Vault ID</p><p><strong>object</strong> <code>string</code></p><p>Vault 删除结果对象类型，固定为 <code>vault.deleted</code></p><p><strong>deleted</strong> <code>boolean</code></p><p>是否删除成功，成功时为 <code>true</code></p><p>删除 Vault 会删除其下全部 Credential。删除后再次获取或删除返回 <code>404</code>。</p></td><td><a id="h-oa-vault-delete-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;vlt_xxx&quot;,
  &quot;object&quot;: &quot;vault.deleted&quot;,
  &quot;deleted&quot;: true
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-vd-errors"></a>

## 错误码

错误响应结构见[错误码](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Vault ID |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
