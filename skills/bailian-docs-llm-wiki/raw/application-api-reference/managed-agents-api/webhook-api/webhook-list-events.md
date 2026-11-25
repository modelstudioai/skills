# 查询指定 Webhook 的事件

按 event\_id 倒序返回指定 Webhook 最近 7 天的投递事件，每个事件包含当前 Webhook 的 delivery 信息。没有匹配记录时返回空数组；Webhook 删除后，已有投递事件在 7 天保留期内仍可查询。

<a id="前提"></a>

<a id="h-list-events-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-list-events-endpoint"></a>

## 接口

**GET** `/webhook_endpoints/{id}/events`

<a id="路径参数"></a>

<a id="h-list-events-path"></a>

## 路径参数

**id** `string` **（必选）**

Webhook ID，格式 wep\_<ULID>

<table><tbody><tr><td><a id="h-list-events-query"></a><h2>Query 参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，默认 20，范围 1～100</p><p><strong>page</strong> <code>string</code> <strong>（可选）</strong></p><p>不透明分页游标；首页不传，后续传上一页返回的 next_page</p></td><td><a id="h-list-events-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/webhook_endpoints/wep_01JXX7YQGPRPV1BZXA35QE7WDP/events?limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-list-events-dto"></a><h3>响应字段</h3><p><strong>data</strong> <code>array&lt;object&gt;</code></p><p>事件对象数组</p><p><strong>data[].type</strong> <code>string</code></p><p>固定为 <code>event</code></p><p><strong>data[].id</strong> <code>string</code></p><p>事件 ID，格式 whe_&lt;ULID&gt;；同一事件的所有投递尝试使用相同外层 id</p><p><strong>data[].created_at</strong> <code>string</code></p><p>事件创建时间，ISO 8601</p><p><strong>data[].data</strong> <code>object</code></p><p>事件载荷</p><p><strong>data[].data.id</strong> <code>string</code></p><p>资源标识；Thread 事件中为 Session 标识</p><p><strong>data[].data.type</strong> <code>string</code></p><p>事件类型</p><p><strong>data[].data.workspace_id</strong> <code>string</code></p><p>工作空间 ID</p><p><strong>data[].data.session_thread_id</strong> <code>string</code></p><p>Thread 事件中为具体 Thread 标识</p><p><strong>data[].delivery</strong> <code>object</code></p><p>当前 Webhook 的投递信息</p><p><strong>data[].delivery.webhook_id</strong> <code>string</code></p><p>Webhook ID</p><p><strong>data[].delivery.status</strong> <code>string</code></p><p>投递状态，如 <code>SUCCEEDED</code></p><p><strong>data[].delivery.attempt_count</strong> <code>integer</code></p><p>投递尝试次数</p><p><strong>data[].delivery.delivery_at</strong> <code>string</code></p><p>投递开始时间，ISO 8601</p><p><strong>data[].delivery.finish_at</strong> <code>string</code></p><p>投递完成时间，ISO 8601</p><p><strong>data[].delivery.failure_reason</strong> <code>string | null</code></p><p>失败原因；成功时为 <code>null</code></p><p><strong>next_page</strong> <code>string | null</code></p><p>下一页游标，末页为 null</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-list-events-resp"></a><h2>响应</h2><p>响应包含 <code>data</code>（Webhook对象数组）与 <code>next_page</code>（下一页游标，无更多数据时为 <code>null</code>）。</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
      &quot;type&quot;: &quot;event&quot;,
      &quot;id&quot;: &quot;whe_01JXX8JY9BBM4BK4C2P7K3M3ZR&quot;,
      &quot;created_at&quot;: &quot;2026-08-06T10:30:21.123Z&quot;,
      &quot;data&quot;: {
        &quot;id&quot;: &quot;sesn_xxx&quot;,
        &quot;type&quot;: &quot;session.thread_idled&quot;,
        &quot;workspace_id&quot;: &quot;ws_xxx&quot;,
        &quot;session_thread_id&quot;: &quot;sthread_xxx&quot;
      },
      &quot;delivery&quot;: {
        &quot;webhook_id&quot;: &quot;wep_01JXX7YQGPRPV1BZXA35QE7WDP&quot;,
        &quot;status&quot;: &quot;SUCCEEDED&quot;,
        &quot;attempt_count&quot;: 1,
        &quot;delivery_at&quot;: &quot;2026-08-06T10:30:21.450Z&quot;,
        &quot;finish_at&quot;: &quot;2026-08-06T10:30:21.780Z&quot;,
        &quot;failure_reason&quot;: null
      }
    }
  ],
  &quot;next_page&quot;: null,
  &quot;request_id&quot;: &quot;8e1d16e4&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-list-events-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `11800016` | invalid webhook event query |
