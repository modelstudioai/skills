# 创建 Credential

在指定 Vault 中创建一个 Credential。auth 当前仅支持 environment\_variable 类型。secret\_value 等敏感值仅写入时传入，响应中不返回。

<a id="前提"></a>

<a id="h-create-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-create-endpoint"></a>

## 接口

**POST** `/vaults/{vault_id}/credentials`

<table><tbody><tr><td><a id="h-create-req"></a><h2>请求体</h2><p><strong>auth</strong> <code>object</code> <strong>（必选）</strong></p><p>认证信息，固定为 environment_variable 类型。</p><p><strong>display_name</strong> <code>string</code> <strong>（可选）</strong></p><p>Credential 可读名称，最大 255 字符</p><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>业务自定义键值对元数据</p><a id="h-create-auth"></a><h3>auth 类型</h3><p><code>auth</code> 当前仅支持 <code>environment_variable</code> 一种类型，以环境变量形式注入会话。</p><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 environment_variable</p><p><strong>secret_name</strong> <code>string</code> <strong>（必选）</strong></p><p>环境变量名称，需满足 <code>^[a-zA-Z][a-zA-Z0-9_]*$</code>：以字母开头，仅支持字母、数字和下划线。创建后不可修改</p><p><strong>secret_value</strong> <code>string</code> <strong>（必选）</strong></p><p>环境变量值，仅写入时传入，响应中不返回</p><p><strong>networking</strong> <code>object</code> <strong>（必选）</strong></p><p>网络策略，限制只有发往指定域名的请求才会被替换为真实密钥</p><p><strong>networking.allowed_hosts</strong> <code>array</code> <strong>（必选）</strong></p><p>允许替换真实密钥的域名列表，支持 <code>*.example.com</code> 通配子域，最多 10 个。填 <code>*</code> 对全部域名生效</p><p><strong>injection_location</strong> <code>object</code> <strong>（必选）</strong></p><p>替换位置，标识密钥写入请求的位置。替换位置为请求头；请求体与查询参数中的占位符不会被替换</p><p><strong>injection_location.header</strong> <code>boolean</code> <strong>（可选）</strong></p><p>是否启用请求头替换，固定传 true</p><div><div><p><strong>说明</strong>同一 Vault 内 <code>secret_name</code> 不能重复，否则返回 409 <code>CREDENTIAL_SECRET_NAME_DUPLICATE</code>“该Vault下已存在相同变量名称的凭证”。</p></div></div></td><td><a id="h-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/vaults/vlt_xxx/credentials&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;display_name&quot;: &quot;第三方 API 密钥&quot;,
    &quot;auth&quot;: {
      &quot;type&quot;: &quot;environment_variable&quot;,
      &quot;secret_name&quot;: &quot;API_KEY&quot;,
      &quot;secret_value&quot;: &quot;sk-xxxx&quot;,
      &quot;networking&quot;: {
        &quot;allowed_hosts&quot;: [
          &quot;api.example.com&quot;,
          &quot;*.example.com&quot;
        ]
      },
      &quot;injection_location&quot;: {
        &quot;header&quot;: true
      }
    }
  }'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-create-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Credential ID，格式 cred_xxx</p><p><strong>type</strong> <code>string</code></p><p>固定为 credential</p><p><strong>vault_id</strong> <code>string</code></p><p>所属 Vault ID</p><p><strong>display_name</strong> <code>string</code></p><p>Credential 可读名称</p><p><strong>auth</strong> <code>object</code></p><p>认证信息，敏感值已脱敏（如 secret_value 不返回）</p><p><strong>auth.type</strong> <code>string</code></p><p>认证类型，当前仅支持 environment_variable</p><p><strong>auth.secret_name</strong> <code>string</code></p><p>环境变量名称</p><p><strong>auth.networking</strong> <code>object</code></p><p>网络策略</p><p><strong>auth.networking.allowed_hosts</strong> <code>array</code></p><p>允许替换真实密钥的域名列表</p><p><strong>auth.injection_location</strong> <code>object</code></p><p>替换位置。替换位置为请求头；请求体与查询参数中的占位符不会被替换</p><p><strong>auth.injection_location.header</strong> <code>boolean</code></p><p>是否启用请求头替换</p><p><strong>metadata</strong> <code>object</code></p><p>业务自定义键值对</p><p><strong>archived_at</strong> <code>string | null</code></p><p>归档时间，未归档时为 null</p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识</p></td><td><a id="h-create-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
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

<a id="h-create-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
| 409 | `CREDENTIAL_SECRET_NAME_DUPLICATE` | `secret_name` 在该 Vault 内已存在。 |
