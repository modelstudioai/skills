# 测试 Webhook

向当前 Webhook 发送一次 webhook.test POST 请求，回调地址返回 2xx 后才返回成功。请求体为空。测试不重试，不保存投递记录，不影响连续失败计数。3xx 或安全校验失败仍会按安全规则禁用当前 Webhook。

<a id="前提"></a>

<a id="h-test-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-test-endpoint"></a>

## 接口

**POST** `/webhook_endpoints/{id}/test`

<table><tbody><tr><td><a id="h-test-path"></a><h2>路径参数</h2><p><strong>id</strong> <code>string</code> <strong>（必选）</strong></p><p>Webhook ID，格式 wep_&lt;ULID&gt;</p></td><td><a id="h-test-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/webhook_endpoints/wep_01JXX7YQGPRPV1BZXA35QE7WDP/test&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-test-dto"></a><h3>响应字段</h3><p><strong>type</strong> <code>string</code></p><p>固定为 event</p><p><strong>id</strong> <code>string</code></p><p>事件 ID，格式 whe_&lt;ULID&gt;</p><p><strong>created_at</strong> <code>string</code></p><p>事件创建时间，ISO 8601</p><p><strong>data</strong> <code>object</code></p><p>事件载荷</p><p><strong>data.id</strong> <code>string</code></p><p>Webhook ID</p><p><strong>data.type</strong> <code>string</code></p><p>固定为 webhook.test</p><p><strong>data.workspace_id</strong> <code>string</code></p><p>工作空间 ID</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-test-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;type&quot;: &quot;event&quot;,
  &quot;id&quot;: &quot;whe_01JXX8JY9BBM4BK4C2P7K3M3ZR&quot;,
  &quot;created_at&quot;: &quot;2026-08-06T10:30:21.123Z&quot;,
  &quot;data&quot;: {
    &quot;id&quot;: &quot;wep_01JXX7YQGPRPV1BZXA35QE7WDP&quot;,
    &quot;type&quot;: &quot;webhook.test&quot;,
    &quot;workspace_id&quot;: &quot;ws_xxx&quot;
  },
  &quot;request_id&quot;: &quot;8e1d16e4&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-test-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 404 | `11800001` | webhook not found |
| 409 | — | Webhook 未启用 |
| 502 | `11800015` | Webhook endpoint returned HTTP 408, response body: request timeout |
