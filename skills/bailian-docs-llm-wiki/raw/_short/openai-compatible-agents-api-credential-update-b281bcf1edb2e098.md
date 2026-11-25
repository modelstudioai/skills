# 更新 Credential

轮换 Credential 的密钥或更新元数据，不支持修改名称和网络配置。

<a id="接口"></a>

<a id="h-oa-cu-endpoint"></a>

## 接口

**POST** `/vaults/{vault_id}/credentials/{credential_id}`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

<table><tbody><tr><td><a id="h-oa-cu-path"></a><h2>路径参数</h2><p><strong>vault_id</strong> <code>string</code> <strong>（必选）</strong></p><p>父 Vault ID，按不透明 ID 使用</p><p><strong>credential_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Credential ID，按不透明 ID 使用</p><a id="h-oa-cu-req"></a><h2>请求体</h2><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>元数据，省略时保持原值；<code>null</code> 返回 <code>400</code>；<code>{}</code> 清空。最多 16 项；key 1–64 字符，value 最多 512 字符</p><p><strong>auth</strong> <code>object</code> <strong>（可选）</strong></p><p>认证信息；省略时只更新 metadata；<code>null</code> 返回 <code>400</code></p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（条件必填）</strong></p><p>认证类型，固定为 <code>environment_variable</code></p><p><strong>secret_value</strong> <code>string</code> <strong>（条件必填）</strong></p><p>新密钥值，不能为空或纯空白；长度和控制字符限制同创建</p></div></section><p><code>metadata</code> 和 <code>auth</code> 至少传一项。同时省略两者或传入 <code>{}</code>，返回 <code>400</code>。更新只支持修改 <code>metadata</code> 和轮换 <code>secret_value</code>；不支持修改 <code>name</code>、<code>secret_name</code> 或 <code>networking</code>，传入这些字段会返回 <code>400 unknown_parameter</code>。</p><p><code>metadata</code> 整体替换，不合并。轮换保留原环境变量名和网络配置；响应不返回 <code>secret_value</code>、密钥标识或 <code>injection_location</code>。</p></td><td><a id="h-oa-credential-update-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/vaults/vlt_xxx/credentials/vcrd_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;metadata&quot;: {&quot;rotation&quot;: &quot;2026-11&quot;},
    &quot;auth&quot;: {
      &quot;type&quot;: &quot;environment_variable&quot;,
      &quot;secret_value&quot;: &quot;sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&quot;
    }
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.post(
    f&quot;{os.environ['BASE_URL']}/vaults/vlt_xxx/credentials/vcrd_xxx&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
    json={
        &quot;metadata&quot;: {&quot;rotation&quot;: &quot;2026-11&quot;},
        &quot;auth&quot;: {
            &quot;type&quot;: &quot;environment_variable&quot;,
            &quot;secret_value&quot;: &quot;sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&quot;,
        },
    },
)
print(resp.status_code, resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-cu-resp"></a><h3>响应字段</h3><p><code>200</code>，返回更新后的 Credential：</p><p><strong>id</strong> <code>string</code></p><p>Credential ID</p><p><strong>object</strong> <code>string</code></p><p>Credential 对象类型，固定为 <code>vault.credential</code></p><p><strong>vault_id</strong> <code>string</code></p><p>所属 Vault ID</p><p><strong>name</strong> <code>string</code></p><p>显示名称</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>updated_at</strong> <code>integer</code></p><p>最近更新时间，Unix 秒</p><p><strong>metadata</strong> <code>object</code></p><p>元数据，字符串键值对；未设置时为 <code>{}</code></p><p><strong>auth</strong> <code>object</code></p><p>认证配置。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>认证类型，固定为 <code>environment_variable</code></p><p><strong>secret_name</strong> <code>string</code></p><p>环境变量名</p><p><strong>networking</strong> <code>object</code></p><p>目标域名配置。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>网络访问类型，<code>limited</code> 或 <code>unrestricted</code></p><p><strong>allowed_hosts</strong> <code>array</code></p><p>允许的目标域名或 IPv4，仅 <code>limited</code> 时返回</p></div></section></div></section></td><td><a id="h-oa-credential-update-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;vcrd_xxx&quot;,
  &quot;object&quot;: &quot;vault.credential&quot;,
  &quot;vault_id&quot;: &quot;vlt_xxx&quot;,
  &quot;name&quot;: &quot;crm-token&quot;,
  &quot;created_at&quot;: 1793941200,
  &quot;updated_at&quot;: 1793944800,
  &quot;metadata&quot;: {&quot;rotation&quot;: &quot;2026-11&quot;},
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

<a id="h-oa-cu-errors"></a>

## 错误码

错误响应结构见[错误码](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `unknown_parameter` | 请求包含未知字段，例如 `name`、`secret_name` 或 `networking` |
| `400` | `invalid_request_error` / `invalid_type` | 按字段说明修正类型 |
| `400` | `invalid_request_error` / `invalid_request_error` | 请求体为空、`auth.type` 不合法、`secret_value` 为空白，或 `metadata` 为 `null` |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | Credential 不存在、已删除、父归属不符或不属于当前工作空间 |
| `409` | `conflict_error` / `conflict_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
