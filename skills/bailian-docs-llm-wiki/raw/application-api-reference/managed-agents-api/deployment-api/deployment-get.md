# 获取 Deployment

根据 ID 获取单个 Deployment 的详细信息。

<a id="前提"></a>

<a id="h-get-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-get-endpoint"></a>

## 接口

**GET** `/deployments/{deployment_id}`

<table><tbody><tr><td><a id="h-get-path"></a><h2>路径参数</h2><p><strong>deployment_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Deployment ID</p></td><td><a id="h-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/deployments/depl_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-get-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Deployment ID</p><p><strong>type</strong> <code>string</code></p><p>固定值 deployment</p><p><strong>name</strong> <code>string</code></p><p>Deployment 名称</p><p><strong>description</strong> <code>string</code></p><p>部署用途描述</p><p><strong>agent</strong> <code>object</code></p><p>—</p><p><strong>environment_id</strong> <code>string</code></p><p>—</p><p><strong>schedule</strong> <code>object</code></p><p>—</p><p><strong>initial_events</strong> <code>array&lt;object&gt;</code></p><p>—</p><p><strong>resources</strong> <code>array&lt;object&gt;</code></p><p>—</p><p><strong>vault_ids</strong> <code>array&lt;string&gt;</code></p><p>—</p><p><strong>metadata</strong> <code>object</code></p><p>—</p><p><strong>status</strong> <code>string</code></p><p>—</p><p><strong>paused_reason</strong> <code>object | null</code></p><p>暂停原因，仅暂停状态时返回</p><p><strong>archived_at</strong> <code>string | null</code></p><p>—</p><p><strong>created_at</strong> <code>string</code></p><p>—</p><p><strong>updated_at</strong> <code>string</code></p><p>—</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-get-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;depl_xxx&quot;,
  &quot;type&quot;: &quot;deployment&quot;,
  &quot;name&quot;: &quot;每日订单汇总&quot;,
  &quot;status&quot;: &quot;active&quot;,
  &quot;agent&quot;: {
    &quot;id&quot;: &quot;agent_xxx&quot;,
    &quot;version&quot;: 12
  },
  &quot;environment_id&quot;: &quot;env_xxx&quot;,
  &quot;schedule&quot;: {
    &quot;type&quot;: &quot;cron&quot;,
    &quot;expression&quot;: &quot;0 9 * * 1-5&quot;,
    &quot;timezone&quot;: &quot;Asia/Shanghai&quot;,
    &quot;last_run_at&quot;: null,
    &quot;next_run_at&quot;: &quot;2026-07-28T01:00:00Z&quot;
  },
  &quot;initial_events&quot;: [
    {
      &quot;type&quot;: &quot;message&quot;,
      &quot;role&quot;: &quot;user&quot;,
      &quot;content&quot;: [
        {
          &quot;type&quot;: &quot;text&quot;,
          &quot;text&quot;: &quot;汇总昨日订单数据&quot;
        }
      ]
    }
  ],
  &quot;resources&quot;: [],
  &quot;vault_ids&quot;: [],
  &quot;metadata&quot;: {},
  &quot;paused_reason&quot;: null,
  &quot;archived_at&quot;: null,
  &quot;created_at&quot;: &quot;2026-07-28T01:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-07-28T01:00:00Z&quot;,
  &quot;request_id&quot;: &quot;req_xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-get-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
| 404 | `DEPLOYMENT_NOT_FOUND` | Deployment not found. |
