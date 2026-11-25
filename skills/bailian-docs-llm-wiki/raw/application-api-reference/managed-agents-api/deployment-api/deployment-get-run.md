# 获取 Deployment Run

获取单个 Deployment Run 的详细信息。

<a id="前提"></a>

<a id="h-get-run-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-get-run-endpoint"></a>

## 接口

**GET** `/deployment_runs/{deployment_run_id}`

<table><tbody><tr><td><a id="h-get-run-path"></a><h2>路径参数</h2><p><strong>deployment_run_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Deployment Run ID</p></td><td><a id="h-get-run-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/deployment_runs/drun_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-get-run-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Deployment Run ID</p><p><strong>type</strong> <code>string</code></p><p>固定值 deployment_run</p><p><strong>deployment_id</strong> <code>string</code></p><p>—</p><p><strong>agent</strong> <code>object</code></p><p>—</p><p><strong>session_id</strong> <code>string | null</code></p><p>—</p><p><strong>trigger_source</strong> <code>string</code></p><p>—</p><p><strong>status</strong> <code>string</code></p><p>—</p><p><strong>error</strong> <code>object | null</code></p><p>错误信息，仅运行失败时返回</p><p><strong>started_at</strong> <code>string</code></p><p>ISO 8601 时间戳</p><p><strong>finished_at</strong> <code>string | null</code></p><p>—</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-get-run-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;drun_xxx&quot;,
  &quot;type&quot;: &quot;deployment_run&quot;,
  &quot;deployment_id&quot;: &quot;depl_xxx&quot;,
  &quot;agent&quot;: {
    &quot;id&quot;: &quot;agent_xxx&quot;,
    &quot;version&quot;: 13
  },
  &quot;session_id&quot;: &quot;sesn_xxx&quot;,
  &quot;trigger_source&quot;: &quot;manual&quot;,
  &quot;status&quot;: &quot;succeeded&quot;,
  &quot;error&quot;: null,
  &quot;started_at&quot;: &quot;2026-07-28T02:00:00Z&quot;,
  &quot;finished_at&quot;: &quot;2026-07-28T02:03:00Z&quot;,
  &quot;request_id&quot;: &quot;req_xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-get-run-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | Required parameter missing or invalid. |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
| 404 | `DEPLOYMENT_RUN_NOT_FOUND` | Deployment run not found. |
