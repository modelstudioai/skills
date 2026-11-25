# 更新 Deployment

更新指定 Deployment 的配置信息。

<a id="前提"></a>

<a id="h-update-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-update-endpoint"></a>

## 接口

**POST** `/deployments/{deployment_id}`

<a id="路径参数"></a>

<a id="h-update-path"></a>

## 路径参数

**deployment\_id** `string` **（必选）**

Deployment ID

<table><tbody><tr><td><a id="h-update-req"></a><h2>请求体</h2><p><strong>name</strong> <code>string</code> <strong>（可选）</strong></p><p>Deployment 名称，最长 256 字符</p><p><strong>description</strong> <code>string</code> <strong>（可选）</strong></p><p>部署用途描述</p><p><strong>agent</strong> <code>object</code> <strong>（可选）</strong></p><p>关联的 Agent</p><p><strong>environment_id</strong> <code>string | null</code> <strong>（可选）</strong></p><p>关联的 Environment ID</p><p><strong>schedule</strong> <code>object | null</code> <strong>（可选）</strong></p><p>定时触发配置；传 null 则清除定时触发</p><p><strong>initial_events</strong> <code>array&lt;object&gt;</code> <strong>（可选）</strong></p><p>触发时发送给 Agent 的初始事件列表，1-50 项</p><p><strong>resources</strong> <code>array&lt;object&gt;</code> <strong>（可选）</strong></p><p>挂载文件资源列表</p><p><strong>vault_ids</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>关联的 Vault ID 列表</p><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>业务自定义键值对</p></td><td><a id="h-update-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/deployments/depl_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;name&quot;: &quot;每日订单汇总-v2&quot;,
    &quot;schedule&quot;: null
  }'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-update-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>—</p><p><strong>type</strong> <code>string</code></p><p>—</p><p><strong>name</strong> <code>string</code></p><p>—</p><p><strong>description</strong> <code>string</code></p><p>—</p><p><strong>agent</strong> <code>object</code></p><p>—</p><p><strong>environment_id</strong> <code>string</code></p><p>—</p><p><strong>schedule</strong> <code>object | null</code></p><p>—</p><p><strong>initial_events</strong> <code>array&lt;object&gt;</code></p><p>—</p><p><strong>resources</strong> <code>array&lt;object&gt;</code></p><p>—</p><p><strong>vault_ids</strong> <code>array&lt;string&gt;</code></p><p>—</p><p><strong>metadata</strong> <code>object</code></p><p>—</p><p><strong>status</strong> <code>string</code></p><p>—</p><p><strong>paused_reason</strong> <code>object | null</code></p><p>暂停原因，仅暂停状态时返回</p><p><strong>archived_at</strong> <code>string | null</code></p><p>—</p><p><strong>created_at</strong> <code>string</code></p><p>—</p><p><strong>updated_at</strong> <code>string</code></p><p>—</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-update-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;depl_xxx&quot;,
  &quot;type&quot;: &quot;deployment&quot;,
  &quot;name&quot;: &quot;每日订单汇总-v2&quot;,
  &quot;status&quot;: &quot;active&quot;,
  &quot;agent&quot;: {
    &quot;id&quot;: &quot;agent_xxx&quot;,
    &quot;version&quot;: 12
  },
  &quot;environment_id&quot;: &quot;env_xxx&quot;,
  &quot;schedule&quot;: null,
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

<a id="h-update-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
| 409 | `DEPLOYMENT_STATE_CONFLICT` | Cannot update an archived deployment. |
