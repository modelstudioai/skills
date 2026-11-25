# 暂停 Deployment

暂停指定 Deployment，停止定时触发。

<a id="前提"></a>

<a id="h-pause-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-pause-endpoint"></a>

## 接口

**POST** `/deployments/{deployment_id}/pause`

<table><tbody><tr><td><a id="h-pause-path"></a><h2>路径参数</h2><p><strong>deployment_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Deployment ID</p></td><td><a id="h-pause-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/deployments/depl_xxx/pause&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-pause-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Deployment ID</p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>deployment</code></p><p><strong>name</strong> <code>string</code></p><p>Deployment 名称</p><p><strong>description</strong> <code>string</code></p><p>Deployment 用途说明</p><p><strong>agent</strong> <code>object</code></p><p>关联 Agent 在锁定版本的快照</p><p><strong>environment_id</strong> <code>string</code></p><p>关联 Environment ID</p><p><strong>schedule</strong> <code>object</code></p><p>定时触发配置。暂停后 <code>next_run_at</code> 为 <code>null</code></p><p><strong>initial_events</strong> <code>array&lt;object&gt;</code></p><p>触发时发送给 Agent 的初始事件</p><p><strong>resources</strong> <code>array&lt;object&gt;</code></p><p>挂载的文件资源</p><p><strong>vault_ids</strong> <code>array&lt;string&gt;</code></p><p>关联 Vault ID 列表</p><p><strong>metadata</strong> <code>object</code></p><p>业务自定义键值对</p><p><strong>status</strong> <code>string</code></p><p>此操作后固定为 <code>paused</code></p><p><strong>paused_reason</strong> <code>object</code></p><p>暂停原因</p><p><strong>archived_at</strong> <code>string | null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识</p></td><td><a id="h-pause-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;depl_xxx&quot;,
  &quot;type&quot;: &quot;deployment&quot;,
  &quot;name&quot;: &quot;每日订单汇总&quot;,
  &quot;status&quot;: &quot;paused&quot;,
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
    &quot;next_run_at&quot;: null
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
  &quot;paused_reason&quot;: {
    &quot;type&quot;: &quot;manual&quot;
  },
  &quot;archived_at&quot;: null,
  &quot;created_at&quot;: &quot;2026-07-28T01:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-07-28T01:00:00Z&quot;,
  &quot;request_id&quot;: &quot;req_xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-pause-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
| 409 | `DEPLOYMENT_STATE_CONFLICT` | Cannot pause an archived deployment. |
