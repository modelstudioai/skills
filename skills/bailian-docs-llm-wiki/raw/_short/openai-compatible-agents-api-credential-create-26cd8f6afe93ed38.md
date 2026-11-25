# 创建 Credential

在指定 Vault 中创建 Credential，仅支持 environment\_variable 类型。

<a id="接口"></a>

<a id="h-oa-cc-endpoint"></a>

## 接口

**POST** `/vaults/{vault_id}/credentials`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

<table><tbody><tr><td><a id="h-oa-cc-path"></a><h2>路径参数</h2><p><strong>vault_id</strong> <code>string</code> <strong>（必选）</strong></p><p>父 Vault ID，按不透明 ID 使用</p><a id="h-oa-cc-req"></a><h2>请求体</h2><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>显示名称，不是环境变量名。去除首尾空白后 1–256 字节</p><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>元数据，字符串键值对，最多 16 项；key 1–64 字符，value 最多 512 字符。传 <code>null</code> 返回 <code>400</code></p><p><strong>auth</strong> <code>object</code> <strong>（必选）</strong></p><p>认证信息。缺失或为 <code>null</code> 返回 <code>400</code></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>认证类型，固定为 <code>environment_variable</code></p><p><strong>secret_name</strong> <code>string</code> <strong>（必选）</strong></p><p>注入到环境的环境变量名。必须以字母开头，只能包含字母、数字和下划线，不能以保留前缀开头</p><p><strong>secret_value</strong> <code>string</code> <strong>（必选）</strong></p><p>密钥值，1–1048576 字符，不能包含换行或 NUL。只写不回传</p><p><strong>networking</strong> <code>object</code> <strong>（必选）</strong></p><p>目标域名配置。缺失或为 <code>null</code> 返回 <code>400</code></p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>网络访问类型，<code>limited</code> 或 <code>unrestricted</code></p><p><strong>allowed_hosts</strong> <code>array</code> <strong>（条件必填）</strong></p><p>允许使用该凭据的目标域名或 IPv4，1–16 个。除特殊值 <code>*</code> 外，每项为精确域名或 IPv4，不支持协议、端口、路径和 IPv6，也不支持 <code>*.example.com</code> 等通配符；数组中包含 <code>*</code> 时对全部目标主机生效。除特殊值 <code>*</code> 外，域名至少包含两个标签，每个标签最多 63 字符，总长度不超过 253 字符；转小写后不能重复</p></div></section></div></section></td><td><a id="h-oa-credential-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/vaults/vlt_xxx/credentials&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;name&quot;: &quot;crm-token&quot;,
    &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;},
    &quot;auth&quot;: {
      &quot;type&quot;: &quot;environment_variable&quot;,
      &quot;secret_name&quot;: &quot;CRM_TOKEN&quot;,
      &quot;secret_value&quot;: &quot;sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&quot;,
      &quot;networking&quot;: {
        &quot;type&quot;: &quot;limited&quot;,
        &quot;allowed_hosts&quot;: [&quot;api.example.com&quot;]
      }
    }
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.post(
    f&quot;{os.environ['BASE_URL']}/vaults/vlt_xxx/credentials&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
    json={
        &quot;name&quot;: &quot;crm-token&quot;,
        &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;},
        &quot;auth&quot;: {
            &quot;type&quot;: &quot;environment_variable&quot;,
            &quot;secret_name&quot;: &quot;CRM_TOKEN&quot;,
            &quot;secret_value&quot;: &quot;sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&quot;,
            &quot;networking&quot;: {
                &quot;type&quot;: &quot;limited&quot;,
                &quot;allowed_hosts&quot;: [&quot;api.example.com&quot;],
            },
        },
    },
)
print(resp.status_code, resp.json())
</code></pre></div></div><p><code>auth.injection_location</code> 不是公开输入，传入会返回 <code>400</code>。</p><div><div><p><strong>说明</strong><code>unrestricted</code> 凭据不单独指定目标域名列表；挂载到 Agents API 环境时，环境必须配置 <code>network.access=&quot;restricted&quot;</code>，并提供非空、合法的 <code>allowed_domains</code>。<code>limited</code> 且 <code>allowed_hosts</code> 包含 <code>*</code> 时，凭据对发往全部目标主机的出网请求生效；出于安全考虑，建议在<a href="openai-compatible-agents-api-environment-create-aa976bec02220caa.md">创建 Environment</a>时，将 <code>network.access</code> 设为 <code>restricted</code>，并配置非空的 <code>allowed_domains</code>。</p></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-cc-resp"></a><h3>响应字段</h3><p><code>201</code>，返回 Credential： 响应不返回 <code>secret_value</code>、密钥标识或 <code>injection_location</code>。</p><p><strong>id</strong> <code>string</code></p><p>Credential ID</p><p><strong>object</strong> <code>string</code></p><p>Credential 对象类型，固定为 <code>vault.credential</code></p><p><strong>vault_id</strong> <code>string</code></p><p>所属 Vault ID</p><p><strong>name</strong> <code>string</code></p><p>显示名称</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>updated_at</strong> <code>integer</code></p><p>最近更新时间，Unix 秒</p><p><strong>metadata</strong> <code>object</code></p><p>元数据，字符串键值对；未设置时为 <code>{}</code></p><p><strong>auth</strong> <code>object</code></p><p>认证配置。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>认证类型，固定为 <code>environment_variable</code></p><p><strong>secret_name</strong> <code>string</code></p><p>环境变量名</p><p><strong>networking</strong> <code>object</code></p><p>目标域名配置。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>网络访问类型，<code>limited</code> 或 <code>unrestricted</code></p><p><strong>allowed_hosts</strong> <code>array</code></p><p>允许的目标域名或 IPv4，仅 <code>limited</code> 时返回</p></div></section></div></section></td><td><a id="h-oa-credential-create-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;vcrd_xxx&quot;,
  &quot;object&quot;: &quot;vault.credential&quot;,
  &quot;vault_id&quot;: &quot;vlt_xxx&quot;,
  &quot;name&quot;: &quot;crm-token&quot;,
  &quot;created_at&quot;: 1793941200,
  &quot;updated_at&quot;: 1793941200,
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

<a id="h-oa-cc-errors"></a>

## 错误码

错误响应结构见[错误码](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `unknown_parameter` | 请求包含未知字段，例如 `auth.injection_location` |
| `400` | `invalid_request_error` / `invalid_type` | 按字段说明修正类型 |
| `400` | `invalid_request_error` / `invalid_request_error` | `name`、`metadata`、`auth` 或主机配置不符合要求 |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 父 Vault 不存在、已删除或不属于当前工作空间 |
| `409` | `conflict_error` / `conflict_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
