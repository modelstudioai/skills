# 归档 Vault

归档 Vault 并级联归档其下 Credential。该接口是百炼扩展。

<a id="接口"></a>

<a id="h-oa-va-endpoint"></a>

## 接口

**POST** `/vaults/{vault_id}/archive`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

<table><tbody><tr><td><a id="h-oa-va-req"></a><h2>路径参数</h2><p><strong>vault_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Vault ID，按不透明 ID 使用</p><p>本接口没有请求体。</p></td><td><a id="h-oa-vault-archive-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/vaults/vlt_xxx/archive&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.post(
    f&quot;{os.environ['BASE_URL']}/vaults/vlt_xxx/archive&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
)
print(resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-va-resp"></a><h3>响应字段</h3><p><code>200</code>，返回归档后的 Vault：</p><p><strong>id</strong> <code>string</code></p><p>Vault ID</p><p><strong>object</strong> <code>string</code></p><p>Vault 对象类型，固定为 <code>vault</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>name</strong> <code>string / null</code></p><p>显示名称</p><p><strong>metadata</strong> <code>object</code></p><p>元数据，字符串键值对；未设置时为 <code>{}</code></p><p>响应仍是 Vault 结构，不返回 <code>archived_at</code> 或 <code>status</code>。归档 Vault 会级联归档其下 Credential。归档后资源仍可获取，默认列表同时包含 <code>active</code> 和 <code>archived</code>。没有恢复接口。</p></td><td><a id="h-oa-vault-archive-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;vlt_xxx&quot;,
  &quot;object&quot;: &quot;vault&quot;,
  &quot;created_at&quot;: 1793941200,
  &quot;name&quot;: &quot;production-secrets&quot;,
  &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;}
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-va-errors"></a>

## 错误码

错误响应结构见[错误码](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Vault ID |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
