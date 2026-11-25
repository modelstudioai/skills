# 更新 Webhook

更新 Webhook 的描述、回调地址或订阅事件。字段缺省表示保持不变。

<a id="前提"></a>

<a id="h-update-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-update-endpoint"></a>

## 接口

**PUT** `/webhook_endpoints/{id}`

<a id="路径参数"></a>

<a id="h-update-path"></a>

## 路径参数

**id** `string` **（必选）**

Webhook ID，格式 wep\_<ULID>

<table><tbody><tr><td><a id="h-update-req"></a><h2>请求体</h2><p><strong>description</strong> <code>string | null</code> <strong>（可选）</strong></p><p>最长 256 个字符；null 或空字符串表示清空，字段缺省表示保持不变</p><p><strong>url</strong> <code>string</code> <strong>（可选）</strong></p><p>新回调地址；传入时重新校验，私网、回环、链路本地和保留地址会被拒绝</p><p><strong>events</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>使用具名事件类型替换整个订阅列表；字段缺省表示保持不变</p></td><td><a id="h-update-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X PUT &quot;$AGENTSTUDIO_URL/webhook_endpoints/wep_01JXX7YQGPRPV1BZXA35QE7WDP&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;description&quot;: &quot;生产环境 Agent 与 Session 事件&quot;,
    &quot;url&quot;: &quot;https://example.com/managedagent/webhooks-v2&quot;,
    &quot;events&quot;: [
      &quot;agent.updated&quot;,
      &quot;session.status_idled&quot;
    ]
  }'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-update-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>—</p><p><strong>description</strong> <code>string | null</code></p><p>—</p><p><strong>url</strong> <code>string</code></p><p>—</p><p><strong>events</strong> <code>array&lt;string&gt;</code></p><p>—</p><p><strong>status</strong> <code>string</code></p><p>—</p><p><strong>disabled_reason</strong> <code>string | null</code></p><p>—</p><p><strong>consecutive_fail</strong> <code>integer</code></p><p>返回更新完成时的当前值</p><p><strong>last_success_at</strong> <code>string | null</code></p><p>返回更新完成时的当前值</p><p><strong>last_failure_at</strong> <code>string | null</code></p><p>返回更新完成时的当前值</p><p><strong>created_at</strong> <code>string</code></p><p>—</p><p><strong>updated_at</strong> <code>string</code></p><p>—</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-update-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;wep_01JXX7YQGPRPV1BZXA35QE7WDP&quot;,
  &quot;description&quot;: &quot;生产环境 Agent 与 Session 事件&quot;,
  &quot;url&quot;: &quot;https://example.com/managedagent/webhooks-v2&quot;,
  &quot;events&quot;: [
    &quot;agent.updated&quot;,
    &quot;session.status_idled&quot;
  ],
  &quot;status&quot;: &quot;ACTIVE&quot;,
  &quot;disabled_reason&quot;: null,
  &quot;consecutive_fail&quot;: 2,
  &quot;last_success_at&quot;: &quot;2026-08-06T10:05:00Z&quot;,
  &quot;last_failure_at&quot;: &quot;2026-08-06T10:10:00Z&quot;,
  &quot;created_at&quot;: &quot;2026-08-06T10:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-08-06T10:15:00Z&quot;,
  &quot;request_id&quot;: &quot;8e1d16e4&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-update-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `11800016` | invalid webhook request |
| 404 | `11800001` | webhook not found |
