# 查询会话资源详情

查询会话中单个已挂载资源的详情。

<a id="前提"></a>

<a id="h-get-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-get-endpoint"></a>

## 接口

**GET** `/sessions/{session_id}/resources/{resource_id}`

<table><tbody><tr><td><a id="h-get-path"></a><h2>路径参数</h2><strong>session_id</strong><code>string</code><strong>（必选）</strong><p>会话 ID，格式 sesn_&lt;ULID&gt;</p><strong>resource_id</strong><code>string</code><strong>（必选）</strong><p>资源 ID，格式 sesrsc_&lt;ULID&gt;</p></td><td><a id="h-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/sessions/sesn_xxx/resources/sesrsc_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-get-dto"></a><h3>响应字段</h3><strong>id</strong><code>string</code><p>资源 ID，格式 sesrsc_&lt;ULID&gt;</p><strong>type</strong><code>string</code><p>资源类型，固定为 file</p><strong>file_id</strong><code>string</code><p>内部副本的文件 ID</p><strong>mount_path</strong><code>string</code><p>加上 /mnt/session/uploads/ 前缀后的完整挂载路径</p><strong>created_at</strong><code>string</code><p>创建时间，ISO 8601</p><strong>updated_at</strong><code>string</code><p>最近更新时间，ISO 8601</p><strong>request_id</strong><code>string</code><p>本次请求的唯一标识</p></td><td><a id="h-get-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sesrsc_xxx&quot;,
  &quot;type&quot;: &quot;file&quot;,
  &quot;file_id&quot;: &quot;file_xxx&quot;,
  &quot;mount_path&quot;: &quot;/mnt/session/uploads/data.csv&quot;,
  &quot;created_at&quot;: &quot;2026-05-28T08:23:11Z&quot;,
  &quot;updated_at&quot;: &quot;2026-05-28T08:23:11Z&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-get-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
