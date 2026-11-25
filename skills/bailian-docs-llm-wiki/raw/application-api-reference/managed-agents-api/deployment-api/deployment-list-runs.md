# 列出 Deployment Runs

分页列出指定 Deployment 的执行记录。

<a id="前提"></a>

<a id="h-list-runs-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-list-runs-endpoint"></a>

## 接口

**GET** `/deployments/{deployment_id}/runs`

<a id="路径参数"></a>

<a id="h-list-runs-path"></a>

## 路径参数

**deployment\_id** `string` **（必选）**

Deployment ID

<table><tbody><tr><td><a id="h-list-runs-query"></a><h2>Query 参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>分页大小，最大 100，默认 <code>20</code></p><p><strong>page</strong> <code>string</code> <strong>（可选）</strong></p><p>分页游标</p></td><td><a id="h-list-runs-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/deployments/depl_xxx/runs?limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-list-runs-dto"></a><h3>响应字段</h3><p><strong>data</strong> <code>array&lt;object&gt;</code></p><p>部署执行对象数组</p><p><strong>data[].id</strong> <code>string</code></p><p>Deployment Run ID</p><p><strong>data[].type</strong> <code>string</code></p><p>固定为 <code>deployment_run</code></p><p><strong>data[].deployment_id</strong> <code>string</code></p><p>关联 Deployment ID</p><p><strong>data[].agent</strong> <code>object</code></p><p>关联 Agent；包含 <code>id</code> 和 <code>version</code></p><p><strong>data[].session_id</strong> <code>string | null</code></p><p>Session ID；异步会话创建完成前为 <code>null</code></p><p><strong>data[].trigger_source</strong> <code>string</code></p><p>触发来源：<code>manual</code> 或 <code>schedule</code></p><p><strong>data[].status</strong> <code>string</code></p><p>运行状态：<code>running</code>、<code>succeeded</code> 或 <code>failed</code></p><p><strong>data[].error</strong> <code>object | null</code></p><p>错误信息；仅运行失败时返回</p><p><strong>data[].started_at</strong> <code>string</code></p><p>运行开始时间，ISO 8601</p><p><strong>data[].finished_at</strong> <code>string | null</code></p><p>运行结束时间，ISO 8601；运行中为 <code>null</code></p><p><strong>data[].request_id</strong> <code>string</code></p><p>请求唯一标识</p><p><strong>next_page</strong> <code>string | null</code></p><p>下一页游标；无更多数据时为 <code>null</code></p></td><td><a id="h-list-runs-resp"></a><h2>响应</h2><p>响应包含 <code>data</code>（部署执行对象数组）与 <code>next_page</code>（下一页游标，无更多数据时为 <code>null</code>）。</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;drun_xxx&quot;,
      &quot;type&quot;: &quot;deployment_run&quot;,
      &quot;deployment_id&quot;: &quot;depl_xxx&quot;,
      &quot;agent&quot;: {
        &quot;id&quot;: &quot;agent_xxx&quot;,
        &quot;version&quot;: 13
      },
      &quot;session_id&quot;: &quot;sesn_xxx&quot;,
      &quot;trigger_source&quot;: &quot;schedule&quot;,
      &quot;status&quot;: &quot;succeeded&quot;,
      &quot;error&quot;: null,
      &quot;started_at&quot;: &quot;2026-07-28T01:00:00Z&quot;,
      &quot;finished_at&quot;: &quot;2026-07-28T01:05:00Z&quot;,
      &quot;request_id&quot;: &quot;req_xxx&quot;
    }
  ],
  &quot;next_page&quot;: null
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-list-runs-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
