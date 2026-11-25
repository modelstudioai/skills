# 创建 Webhook

创建一个 Webhook endpoint，订阅具名事件并投递到指定回调地址。Signing Secret 只在本次响应返回，后续查询不再返回。每个 Workspace 最多创建 20 个 Webhook。

<a id="前提"></a>

<a id="h-create-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-create-endpoint"></a>

## 接口

**POST** `/webhook_endpoints`

<table><tbody><tr><td><a id="h-create-req"></a><h2>请求体</h2><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>回调地址；允许 HTTP 或 HTTPS，端口不限，可用域名或公网 IP；私网、回环、链路本地和保留地址会被拒绝</p><p><strong>events</strong> <code>array&lt;string&gt;</code> <strong>（必选）</strong></p><p>可订阅的具名事件类型数组，不支持通配订阅</p><p><strong>description</strong> <code>string</code> <strong>（可选）</strong></p><p>描述，最长 256 个字符</p></td><td><a id="h-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/webhook_endpoints&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;description&quot;: &quot;生产环境会话事件&quot;,
    &quot;url&quot;: &quot;https://example.com/managedagent/webhooks&quot;,
    &quot;events&quot;: [
      &quot;session.updated&quot;,
      &quot;session.status_idled&quot;,
      &quot;session.thread_terminated&quot;
    ]
  }'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-create-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Webhook ID，格式 wep_&lt;ULID&gt;</p><p><strong>description</strong> <code>string | null</code></p><p>描述</p><p><strong>url</strong> <code>string</code></p><p>回调地址</p><p><strong>events</strong> <code>array&lt;string&gt;</code></p><p>订阅的具名事件类型</p><p><strong>status</strong> <code>string</code></p><p>Webhook 状态</p><p><strong>disabled_reason</strong> <code>string | null</code></p><p>禁用原因，未禁用时为 null</p><p><strong>consecutive_fail</strong> <code>integer</code></p><p>当前连续失败数，新建时为 0</p><p><strong>last_success_at</strong> <code>string | null</code></p><p>最近成功投递时间，新建时为 null</p><p><strong>last_failure_at</strong> <code>string | null</code></p><p>最近失败投递时间，新建时为 null</p><p><strong>signing_secret</strong> <code>string</code></p><p>验签密钥，格式 whsec_ 加标准 Base64 文本。仅在创建和重置成功响应返回</p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-create-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
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
  &quot;consecutive_fail&quot;: 0,
  &quot;last_success_at&quot;: null,
  &quot;last_failure_at&quot;: null,
  &quot;signing_secret&quot;: &quot;whsec_xxx&quot;,
  &quot;created_at&quot;: &quot;2026-08-06T10:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-08-06T10:00:00Z&quot;,
  &quot;request_id&quot;: &quot;8e1d16e4&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-create-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `11800016` | invalid webhook request |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
