# 启用 Webhook

启用被禁用的 Webhook。请求体为空。重新启用不会补发禁用期间产生的事件。

<a id="前提"></a>

<a id="h-enable-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-enable-endpoint"></a>

## 接口

**POST** `/webhook_endpoints/{id}/enable`

<table><tbody><tr><td><a id="h-enable-path"></a><h2>路径参数</h2><p><strong>id</strong> <code>string</code> <strong>（必选）</strong></p><p>Webhook ID，格式 wep_&lt;ULID&gt;</p></td><td><a id="h-enable-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/webhook_endpoints/wep_01JXX7YQGPRPV1BZXA35QE7WDP/enable&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-enable-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>—</p><p><strong>description</strong> <code>string | null</code></p><p>—</p><p><strong>url</strong> <code>string</code></p><p>—</p><p><strong>events</strong> <code>array&lt;string&gt;</code></p><p>—</p><p><strong>status</strong> <code>string</code></p><p>启用后为 ACTIVE</p><p><strong>disabled_reason</strong> <code>string | null</code></p><p>—</p><p><strong>consecutive_fail</strong> <code>integer</code></p><p>返回启用完成时的当前值</p><p><strong>last_success_at</strong> <code>string | null</code></p><p>返回启用完成时的当前值</p><p><strong>last_failure_at</strong> <code>string | null</code></p><p>返回启用完成时的当前值</p><p><strong>created_at</strong> <code>string</code></p><p>—</p><p><strong>updated_at</strong> <code>string</code></p><p>—</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-enable-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;wep_01JXX7YQGPRPV1BZXA35QE7WDP&quot;,
  &quot;description&quot;: &quot;生产环境会话事件&quot;,
  &quot;url&quot;: &quot;https://example.com/managedagent/webhooks&quot;,
  &quot;events&quot;: [
    &quot;session.status_idled&quot;
  ],
  &quot;status&quot;: &quot;ACTIVE&quot;,
  &quot;disabled_reason&quot;: null,
  &quot;consecutive_fail&quot;: 2,
  &quot;last_success_at&quot;: &quot;2026-08-06T10:05:00Z&quot;,
  &quot;last_failure_at&quot;: &quot;2026-08-06T10:10:00Z&quot;,
  &quot;created_at&quot;: &quot;2026-08-06T10:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-08-06T10:20:00Z&quot;,
  &quot;request_id&quot;: &quot;8e1d16e4&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-enable-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 404 | `11800001` | webhook not found |
