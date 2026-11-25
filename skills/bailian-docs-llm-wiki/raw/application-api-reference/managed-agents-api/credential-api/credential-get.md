# 获取 Credential

获取指定 Credential 的详情。响应为 Credential 对象，auth 中的敏感值已脱敏。

<a id="前提"></a>

<a id="h-get-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-get-endpoint"></a>

## 接口

**GET** `/vaults/{vault_id}/credentials/{credential_id}`

<table><tbody><tr><td><a id="h-get-path"></a><h2>路径参数</h2><p><strong>vault_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Vault ID，格式 vlt_xxx</p><p><strong>credential_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Credential ID，格式 cred_xxx</p></td><td><a id="h-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/vaults/vlt_xxx/credentials/cred_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-get-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Credential ID，格式 cred_xxx</p><p><strong>type</strong> <code>string</code></p><p>固定为 credential</p><p><strong>vault_id</strong> <code>string</code></p><p>所属 Vault ID</p><p><strong>display_name</strong> <code>string</code></p><p>Credential 可读名称</p><p><strong>auth</strong> <code>object</code></p><p>认证信息，敏感值已脱敏（如 secret_value 不返回）</p><p><strong>auth.type</strong> <code>string</code></p><p>认证类型，当前仅支持 environment_variable</p><p><strong>auth.secret_name</strong> <code>string</code></p><p>环境变量名称</p><p><strong>auth.networking</strong> <code>object</code></p><p>网络策略</p><p><strong>auth.networking.allowed_hosts</strong> <code>array</code></p><p>允许替换真实密钥的域名列表</p><p><strong>auth.injection_location</strong> <code>object</code></p><p>替换位置。替换位置为请求头；请求体与查询参数中的占位符不会被替换</p><p><strong>auth.injection_location.header</strong> <code>boolean</code></p><p>是否启用请求头替换</p><p><strong>metadata</strong> <code>object</code></p><p>业务自定义键值对</p><p><strong>archived_at</strong> <code>string | null</code></p><p>归档时间，未归档时为 null</p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识</p></td><td><a id="h-get-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;cred_xxx&quot;,
  &quot;type&quot;: &quot;credential&quot;,
  &quot;vault_id&quot;: &quot;vlt_xxx&quot;,
  &quot;display_name&quot;: &quot;第三方 API 密钥&quot;,
  &quot;auth&quot;: {
    &quot;type&quot;: &quot;environment_variable&quot;,
    &quot;secret_name&quot;: &quot;API_KEY&quot;,
    &quot;networking&quot;: {
      &quot;allowed_hosts&quot;: [
        &quot;api.example.com&quot;,
        &quot;*.example.com&quot;
      ]
    },
    &quot;injection_location&quot;: {
      &quot;header&quot;: true
    }
  },
  &quot;metadata&quot;: {},
  &quot;archived_at&quot;: null,
  &quot;created_at&quot;: &quot;2026-07-10T08:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-07-10T08:00:00Z&quot;,
  &quot;request_id&quot;: &quot;req_xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-get-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
