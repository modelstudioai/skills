# 查询 Webhook 详情

查询单个 Webhook 的详情。详情不返回 Signing Secret。

<a id="前提"></a>

<a id="h-get-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-get-endpoint"></a>

## 接口

**GET** `/webhook_endpoints/{id}`

<table><tbody><tr><td><a id="h-get-path"></a><h2>路径参数</h2><p><strong>id</strong> <code>string</code> <strong>（必选）</strong></p><p>Webhook ID，格式 wep_&lt;ULID&gt;</p></td><td><a id="h-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/webhook_endpoints/wep_01JXX7YQGPRPV1BZXA35QE7WDP&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-get-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Webhook ID，格式 wep_&lt;ULID&gt;</p><p><strong>description</strong> <code>string | null</code></p><p>描述</p><p><strong>url</strong> <code>string</code></p><p>回调 URL</p><p><strong>events</strong> <code>array&lt;string&gt;</code></p><p>订阅的命名事件类型</p><p><strong>status</strong> <code>string</code></p><p>Webhook 状态：<code>ACTIVE</code> 或 <code>DISABLED</code></p><p><strong>disabled_reason</strong> <code>string | null</code></p><p>禁用原因；未禁用时为 <code>null</code></p><p><strong>consecutive_fail</strong> <code>integer</code></p><p>当前连续失败次数</p><p><strong>last_success_at</strong> <code>string | null</code></p><p>最近成功投递时间</p><p><strong>last_failure_at</strong> <code>string | null</code></p><p>最近失败投递时间</p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识</p></td><td><a id="h-get-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;wep_01JXX7YQGPRPV1BZXA35QE7WDP&quot;,
  &quot;description&quot;: &quot;生产环境会话事件&quot;,
  &quot;url&quot;: &quot;https://example.com/managedagent/webhooks&quot;,
  &quot;events&quot;: [
    &quot;session.updated&quot;,
    &quot;session.status_idled&quot;,
    &quot;session.thread_terminated&quot;
  ],
  &quot;status&quot;: &quot;ACTIVE&quot;,
  &quot;disabled_reason&quot;: null,
  &quot;consecutive_fail&quot;: 2,
  &quot;last_success_at&quot;: &quot;2026-08-06T10:05:00Z&quot;,
  &quot;last_failure_at&quot;: &quot;2026-08-06T10:10:00Z&quot;,
  &quot;created_at&quot;: &quot;2026-08-06T10:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-08-06T10:00:00Z&quot;,
  &quot;request_id&quot;: &quot;8e1d16e4&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-get-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 404 | `11800001` | webhook not found |
