# 更新 Vault

更新 Vault 的名称或元数据。更新使用 POST，元数据整体替换。

<a id="接口"></a>

<a id="h-oa-vu-endpoint"></a>

## 接口

**POST** `/vaults/{vault_id}`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

<table><tbody><tr><td><a id="h-oa-vu-path"></a><h2>路径参数</h2><p><strong>vault_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Vault ID，按不透明 ID 使用</p><a id="h-oa-vu-req"></a><h2>请求体</h2><p><strong>name</strong> <code>string / null</code> <strong>（可选）</strong></p><p>Vault 名称，省略时保持原值；<code>null</code> 清除名称；提供时去除首尾空白后 1–256 字节</p><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>元数据，省略时保持原值；<code>null</code> 返回 <code>400</code>；<code>{}</code> 清空。最多 16 项；key 1–64 字符，value 最多 512 字符</p><p><code>metadata</code> 整体替换，不合并；未出现在新对象中的旧 key 会被删除。更新空对象 <code>{}</code> 不会修改可空字段。未知字段返回 <code>400 unknown_parameter</code>。</p></td><td><a id="h-oa-vault-update-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/vaults/vlt_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;name&quot;: &quot;production-secrets-v2&quot;,
    &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;, &quot;stage&quot;: &quot;prod&quot;}
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.post(
    f&quot;{os.environ['BASE_URL']}/vaults/vlt_xxx&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
    json={
        &quot;name&quot;: &quot;production-secrets-v2&quot;,
        &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;, &quot;stage&quot;: &quot;prod&quot;},
    },
)
print(resp.status_code, resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-vu-resp"></a><h3>响应字段</h3><p><code>200</code>，返回更新后的 Vault：</p><p><strong>id</strong> <code>string</code></p><p>Vault ID</p><p><strong>object</strong> <code>string</code></p><p>Vault 对象类型，固定为 <code>vault</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>name</strong> <code>string / null</code></p><p>显示名称</p><p><strong>metadata</strong> <code>object</code></p><p>元数据，字符串键值对；未设置时为 <code>{}</code></p></td><td><a id="h-oa-vault-update-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;vlt_xxx&quot;,
  &quot;object&quot;: &quot;vault&quot;,
  &quot;created_at&quot;: 1793941200,
  &quot;name&quot;: &quot;production-secrets-v2&quot;,
  &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;, &quot;stage&quot;: &quot;prod&quot;}
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-vu-errors"></a>

## 错误码

错误响应结构见[错误码](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `unknown_parameter` | 移除 `status` 等未知字段 |
| `400` | `invalid_request_error` / `invalid_type` | 按字段说明修正类型 |
| `400` | `invalid_request_error` / `invalid_request_error` | 按字段说明修正 `name`，并避免传 `null` 的 `metadata` |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Vault ID |
| `409` | `conflict_error` / `conflict_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
