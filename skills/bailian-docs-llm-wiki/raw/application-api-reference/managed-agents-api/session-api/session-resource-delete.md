# 卸载会话资源

从会话中卸载指定资源，同时清除其内部副本。此操作不可恢复。

<a id="前提"></a>

<a id="h-delete-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-delete-endpoint"></a>

## 接口

**DELETE** `/sessions/{session_id}/resources/{resource_id}`

<table><tbody><tr><td><a id="h-delete-path"></a><h2>路径参数</h2><strong>session_id</strong><code>string</code><strong>（必选）</strong><p>会话 ID，格式 sesn_&lt;ULID&gt;</p><strong>resource_id</strong><code>string</code><strong>（必选）</strong><p>资源 ID，格式 sesrsc_&lt;ULID&gt;</p></td><td><a id="h-delete-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X DELETE &quot;$AGENTSTUDIO_URL/sessions/sesn_xxx/resources/sesrsc_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-delete-dto"></a><h3>响应字段</h3><strong>id</strong><code>string</code><p>被卸载的资源 ID</p><strong>type</strong><code>string</code><p>固定为 session_resource_deleted，标识卸载成功</p><strong>request_id</strong><code>string</code><p>本次请求的唯一标识</p></td><td><a id="h-delete-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sesrsc_xxx&quot;,
  &quot;type&quot;: &quot;session_resource_deleted&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-delete-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
