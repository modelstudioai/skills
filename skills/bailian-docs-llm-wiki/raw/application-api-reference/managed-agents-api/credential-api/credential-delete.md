# 删除 Credential

永久删除指定 Credential，删除后不可恢复。

<a id="前提"></a>

<a id="h-delete-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-delete-endpoint"></a>

## 接口

**DELETE** `/vaults/{vault_id}/credentials/{credential_id}`

<table><tbody><tr><td><a id="h-delete-path"></a><h2>路径参数</h2><p><strong>vault_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Vault ID，格式 vlt_xxx</p><p><strong>credential_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Credential ID，格式 cred_xxx</p></td><td><a id="h-delete-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X DELETE &quot;$AGENTSTUDIO_URL/vaults/vlt_xxx/credentials/cred_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-delete-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>已删除的 Credential ID</p><p><strong>type</strong> <code>string</code></p><p>固定为 credential_deleted</p><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识</p></td><td><a id="h-delete-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;cred_xxx&quot;,
  &quot;type&quot;: &quot;credential_deleted&quot;,
  &quot;request_id&quot;: &quot;req_xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-delete-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
