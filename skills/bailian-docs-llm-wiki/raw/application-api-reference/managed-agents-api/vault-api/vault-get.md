# 获取 Vault

根据 ID 获取单个 Vault 的详细信息。

<a id="前提"></a>

<a id="h-get-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-get-endpoint"></a>

## 接口

**GET** `/vaults/{vault_id}`

<table><tbody><tr><td><a id="h-get-path"></a><h2>路径参数</h2><p><strong>vault_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Vault ID，格式 vlt_xxx</p></td><td><a id="h-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/vaults/vlt_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-get-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Vault ID，格式 vlt_xxx</p><p><strong>type</strong> <code>string</code></p><p>固定为 vault</p><p><strong>display_name</strong> <code>string</code></p><p>Vault 可读名称</p><p><strong>metadata</strong> <code>object</code></p><p>业务自定义键值对</p><p><strong>archived_at</strong> <code>string | null</code></p><p>归档时间，未归档时为 null</p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p></td><td><a id="h-get-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;vlt_xxx&quot;,
  &quot;type&quot;: &quot;vault&quot;,
  &quot;display_name&quot;: &quot;生产环境密钥箱&quot;,
  &quot;metadata&quot;: {
    &quot;environment&quot;: &quot;production&quot;
  },
  &quot;archived_at&quot;: null,
  &quot;created_at&quot;: &quot;2026-06-20T10:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-06-20T10:00:00Z&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-get-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
