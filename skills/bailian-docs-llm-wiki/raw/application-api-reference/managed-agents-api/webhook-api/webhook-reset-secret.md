# 重置 Signing Secret

重置 Webhook 的 Signing Secret。请求体为空。新的 Signing Secret 只在本次响应返回，后续投递使用重置后的 Secret 重新计算签名。

<a id="前提"></a>

<a id="h-reset-secret-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-reset-secret-endpoint"></a>

## 接口

**POST** `/webhook_endpoints/{id}/reset_secret`

<table><tbody><tr><td><a id="h-reset-secret-path"></a><h2>路径参数</h2><p><strong>id</strong> <code>string</code> <strong>（必选）</strong></p><p>Webhook ID，格式 wep_&lt;ULID&gt;</p></td><td><a id="h-reset-secret-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/webhook_endpoints/wep_01JXX7YQGPRPV1BZXA35QE7WDP/reset_secret&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-reset-secret-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>—</p><p><strong>signing_secret</strong> <code>string</code></p><p>新的验签密钥，格式 whsec_ 加标准 Base64 文本。仅在本次响应返回</p><p><strong>updated_at</strong> <code>string</code></p><p>—</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-reset-secret-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;wep_01JXX7YQGPRPV1BZXA35QE7WDP&quot;,
  &quot;signing_secret&quot;: &quot;whsec_new_xxx&quot;,
  &quot;updated_at&quot;: &quot;2026-08-06T10:35:00Z&quot;,
  &quot;request_id&quot;: &quot;8e1d16e4&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-reset-secret-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 404 | `11800005` | failed to reset webhook signing secret |
