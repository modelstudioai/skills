# 查询 Webhook 列表

返回当前 Workspace 下全部未删除的 Webhook。接口不分页。列表不返回 Signing Secret。

<a id="前提"></a>

<a id="h-list-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-list-endpoint"></a>

## 接口

**GET** `/webhook_endpoints`

<a id="请求示例"></a>

<a id="h-list-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl "$AGENTSTUDIO_URL/webhook_endpoints" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<table><tbody><tr><td><a id="h-list-dto"></a><h3>响应字段</h3><p><strong>data</strong> <code>array&lt;object&gt;</code></p><p>Webhook 对象数组</p><p><strong>data[].id</strong> <code>string</code></p><p>Webhook ID</p><p><strong>data[].description</strong> <code>string | null</code></p><p>描述</p><p><strong>data[].url</strong> <code>string</code></p><p>回调 URL</p><p><strong>data[].events</strong> <code>array&lt;string&gt;</code></p><p>订阅的命名事件类型</p><p><strong>data[].status</strong> <code>string</code></p><p>Webhook 状态：<code>ACTIVE</code> 或 <code>DISABLED</code></p><p><strong>data[].disabled_reason</strong> <code>string | null</code></p><p>禁用原因；未禁用时为 <code>null</code></p><p><strong>data[].consecutive_fail</strong> <code>integer</code></p><p>当前连续失败次数</p><p><strong>data[].last_success_at</strong> <code>string | null</code></p><p>最近成功投递时间</p><p><strong>data[].last_failure_at</strong> <code>string | null</code></p><p>最近失败投递时间</p><p><strong>data[].created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>data[].updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识</p></td><td><a id="h-list-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
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
      &quot;updated_at&quot;: &quot;2026-08-06T10:00:00Z&quot;
    }
  ],
  &quot;request_id&quot;: &quot;8e1d16e4&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-list-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
