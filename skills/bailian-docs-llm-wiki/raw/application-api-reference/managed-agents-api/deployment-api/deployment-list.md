# 列出 Deployment

分页查询 Deployment 列表，支持按 Agent、状态、关键词等条件筛选。

<a id="前提"></a>

<a id="h-list-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-list-endpoint"></a>

## 接口

**GET** `/deployments`

<table><tbody><tr><td><a id="h-list-query"></a><h2>Query 参数</h2><p><strong>agent_id</strong> <code>string</code> <strong>（可选）</strong></p><p>按 Agent ID 筛选</p><p><strong>keyword</strong> <code>string</code> <strong>（可选）</strong></p><p>按 ID 或名称模糊搜索</p><p><strong>status</strong> <code>string</code> <strong>（可选）</strong></p><p>按状态筛选：<code>active</code> 或 <code>paused</code></p><p><strong>include_archived</strong> <code>boolean</code> <strong>（可选）</strong></p><p>是否包含已归档的 Deployment，默认 <code>false</code></p><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页返回数量，最大 100，默认 <code>20</code></p><p><strong>page</strong> <code>string</code> <strong>（可选）</strong></p><p>分页游标</p><p><strong>created_at[gte]</strong> <code>string</code> <strong>（可选）</strong></p><p>创建时间下界，RFC 3339</p><p><strong>created_at[lte]</strong> <code>string</code> <strong>（可选）</strong></p><p>创建时间上界，RFC 3339</p></td><td><a id="h-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/deployments?agent_id=agent_xxx&amp;keyword=data&amp;status=active&amp;include_archived=true&amp;limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-list-dto"></a><h3>响应字段</h3><p><strong>data</strong> <code>array&lt;object&gt;</code></p><p>部署对象数组</p><p><strong>data[].id</strong> <code>string</code></p><p>Deployment ID</p><p><strong>data[].type</strong> <code>string</code></p><p>固定为 <code>deployment</code></p><p><strong>data[].name</strong> <code>string</code></p><p>Deployment 名称</p><p><strong>data[].description</strong> <code>string</code></p><p>Deployment 用途说明</p><p><strong>data[].agent</strong> <code>object</code></p><p>关联 Agent 在锁定版本的快照</p><p><strong>data[].environment_id</strong> <code>string</code></p><p>关联 Environment ID</p><p><strong>data[].schedule</strong> <code>object</code></p><p>定时触发配置</p><p><strong>data[].initial_events</strong> <code>array&lt;object&gt;</code></p><p>触发时发送给 Agent 的初始事件</p><p><strong>data[].resources</strong> <code>array&lt;object&gt;</code></p><p>挂载的文件资源</p><p><strong>data[].vault_ids</strong> <code>array&lt;string&gt;</code></p><p>关联 Vault ID 列表</p><p><strong>data[].metadata</strong> <code>object</code></p><p>业务自定义键值对</p><p><strong>data[].status</strong> <code>string</code></p><p>Deployment 状态：<code>active</code> 或 <code>paused</code></p><p><strong>data[].paused_reason</strong> <code>object | null</code></p><p>暂停原因；仅状态为 <code>paused</code> 时返回</p><p><strong>data[].archived_at</strong> <code>string | null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>data[].created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>data[].updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p><p><strong>data[].request_id</strong> <code>string</code></p><p>请求唯一标识</p><p><strong>next_page</strong> <code>string | null</code></p><p>下一页游标；无更多数据时为 <code>null</code></p></td><td><a id="h-list-resp"></a><h2>响应</h2><p>响应包含 <code>data</code>（部署对象数组）与 <code>next_page</code>（下一页游标，无更多数据时为 <code>null</code>）。</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
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
      &quot;initial_events&quot;: [],
      &quot;resources&quot;: [],
      &quot;vault_ids&quot;: [],
      &quot;metadata&quot;: {},
      &quot;paused_reason&quot;: null,
      &quot;archived_at&quot;: null,
      &quot;created_at&quot;: &quot;2026-07-28T01:00:00Z&quot;,
      &quot;updated_at&quot;: &quot;2026-07-28T01:00:00Z&quot;,
      &quot;request_id&quot;: &quot;req_xxx&quot;
    }
  ],
  &quot;next_page&quot;: null
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-list-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
