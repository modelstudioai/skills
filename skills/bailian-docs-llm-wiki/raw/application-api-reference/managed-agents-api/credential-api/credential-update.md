# 更新 Credential

更新指定 Credential 的属性。auth 中的 type 和 secret\_name 不可修改。

<a id="前提"></a>

<a id="h-update-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-update-endpoint"></a>

## 接口

**POST** `/vaults/{vault_id}/credentials/{credential_id}`

<a id="路径参数"></a>

<a id="h-update-path"></a>

## 路径参数

**vault\_id** `string` **（必选）**

Vault ID，格式 vlt\_xxx

**credential\_id** `string` **（必选）**

Credential ID，格式 cred\_xxx

<table><tbody><tr><td><a id="h-update-req"></a><h2>请求体</h2><p><strong>auth</strong> <code>object</code> <strong>（可选）</strong></p><p>认证信息，固定为 environment_variable 类型。更新时 type 与 secret_name 不可修改，secret_value 留空表示不修改。</p><p><strong>display_name</strong> <code>string</code> <strong>（可选）</strong></p><p>Credential 可读名称，最大 255 字符</p><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>业务自定义键值对元数据</p><div><div><p><strong>说明</strong><code>auth.secret_name</code> 需满足 <code>^[a-zA-Z][a-zA-Z0-9_]*$</code>：以字母开头，仅支持字母、数字和下划线。更新时不可修改。</p></div></div></td><td><a id="h-update-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/vaults/vlt_xxx/credentials/cred_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;display_name&quot;: &quot;生产环境 API 密钥&quot;,
    &quot;auth&quot;: {
      &quot;type&quot;: &quot;environment_variable&quot;,
      &quot;secret_name&quot;: &quot;API_KEY&quot;,
      &quot;secret_value&quot;: &quot;sk-new-value&quot;,
      &quot;networking&quot;: {
        &quot;allowed_hosts&quot;: [
          &quot;api.example.com&quot;
        ]
      },
      &quot;injection_location&quot;: {
        &quot;header&quot;: true
      }
    }
  }'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-update-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Credential ID，格式 cred_xxx</p><p><strong>type</strong> <code>string</code></p><p>固定为 credential</p><p><strong>vault_id</strong> <code>string</code></p><p>所属 Vault ID</p><p><strong>display_name</strong> <code>string</code></p><p>Credential 可读名称</p><p><strong>auth</strong> <code>object</code></p><p>认证信息，敏感值已脱敏</p><p><strong>metadata</strong> <code>object</code></p><p>业务自定义键值对</p><p><strong>archived_at</strong> <code>string | null</code></p><p>归档时间，未归档时为 null</p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识</p></td><td><a id="h-update-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;cred_xxx&quot;,
  &quot;type&quot;: &quot;credential&quot;,
  &quot;vault_id&quot;: &quot;vlt_xxx&quot;,
  &quot;display_name&quot;: &quot;生产环境 API 密钥&quot;,
  &quot;auth&quot;: {
    &quot;type&quot;: &quot;environment_variable&quot;,
    &quot;secret_name&quot;: &quot;API_KEY&quot;,
    &quot;networking&quot;: {
      &quot;allowed_hosts&quot;: [
        &quot;api.example.com&quot;
      ]
    },
    &quot;injection_location&quot;: {
      &quot;header&quot;: true
    }
  },
  &quot;metadata&quot;: {},
  &quot;archived_at&quot;: null,
  &quot;created_at&quot;: &quot;2026-07-10T08:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-07-15T03:00:00Z&quot;,
  &quot;request_id&quot;: &quot;req_xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-update-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
