# 归档 Deployment

归档指定 Deployment，操作幂等。

<a id="前提"></a>

<a id="h-archive-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-archive-endpoint"></a>

## 接口

**POST** `/deployments/{deployment_id}/archive`

<table><tbody><tr><td><a id="h-archive-path"></a><h2>路径参数</h2><p><strong>deployment_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Deployment ID</p></td><td><a id="h-archive-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/deployments/depl_xxx/archive&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-archive-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Deployment ID</p><p><strong>type</strong> <code>string</code></p><p>固定值 deployment</p><p><strong>name</strong> <code>string</code></p><p>Deployment 名称</p><p><strong>description</strong> <code>string</code></p><p>Deployment 描述</p><p><strong>agent</strong> <code>object</code></p><p>—</p><p><strong>environment_id</strong> <code>string</code></p><p>—</p><p><strong>schedule</strong> <code>object</code></p><p>定时触发配置</p><p><strong>initial_events</strong> <code>array&lt;object&gt;</code></p><p>—</p><p><strong>resources</strong> <code>array&lt;object&gt;</code></p><p>—</p><p><strong>vault_ids</strong> <code>array&lt;string&gt;</code></p><p>—</p><p><strong>metadata</strong> <code>object</code></p><p>—</p><p><strong>status</strong> <code>string</code></p><p>—</p><p><strong>paused_reason</strong> <code>string | null</code></p><p>—</p><p><strong>archived_at</strong> <code>string | null</code></p><p>—</p><p><strong>created_at</strong> <code>string</code></p><p>—</p><p><strong>updated_at</strong> <code>string</code></p><p>—</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-archive-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;depl_xxx&quot;,
  &quot;type&quot;: &quot;deployment&quot;,
  &quot;name&quot;: &quot;Daily Report Generator&quot;,
  &quot;description&quot;: &quot;Generates daily sales reports&quot;,
  &quot;agent&quot;: {
    &quot;id&quot;: &quot;agent_xxx&quot;,
    &quot;version&quot;: 13
  },
  &quot;environment_id&quot;: &quot;env_xxx&quot;,
  &quot;schedule&quot;: {
    &quot;cron&quot;: &quot;0 9 * * *&quot;
  },
  &quot;initial_events&quot;: [],
  &quot;resources&quot;: [],
  &quot;vault_ids&quot;: [],
  &quot;metadata&quot;: {},
  &quot;status&quot;: &quot;active&quot;,
  &quot;paused_reason&quot;: null,
  &quot;archived_at&quot;: &quot;2026-07-28T03:00:00Z&quot;,
  &quot;created_at&quot;: &quot;2026-07-20T10:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-07-28T03:00:00Z&quot;,
  &quot;request_id&quot;: &quot;req_xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-archive-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
