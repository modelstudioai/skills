# 列出会话资源

分页列出会话当前已挂载的资源。

<a id="前提"></a>

<a id="h-list-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-list-endpoint"></a>

## 接口

**GET** `/sessions/{session_id}/resources`

<a id="路径参数"></a>

<a id="h-list-path"></a>

## 路径参数

**session\_id** `string` **（必选）**

会话 ID，格式 sesn\_<ULID>

<table><tbody><tr><td><a id="h-list-query"></a><h2>Query 参数</h2><strong>limit</strong><code>integer</code><strong>（可选）</strong><p>每页数量，最大 100，默认 <code>20</code></p><strong>page</strong><code>string</code><strong>（可选）</strong><p>分页游标（opaque token）。首次不传，后续传上一次响应返回的游标</p></td><td><a id="h-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/sessions/sesn_xxx/resources?limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-list-dto"></a><h3>响应字段</h3><strong>data</strong><code>array&lt;object&gt;</code><p>资源对象数组</p><strong>data[].id</strong><code>string</code><p>资源 ID，格式 sesrsc_&lt;ULID&gt;</p><strong>data[].type</strong><code>string</code><p>资源类型，固定为 <code>file</code></p><strong>data[].file_id</strong><code>string</code><p>内部副本的文件 ID</p><strong>data[].mount_path</strong><code>string</code><p>加上 <code>/mnt/session/uploads/</code> 前缀后的完整挂载路径</p><strong>data[].created_at</strong><code>string</code><p>创建时间，ISO 8601</p><strong>data[].updated_at</strong><code>string</code><p>最近更新时间，ISO 8601</p><strong>next_page</strong><code>string</code><p>下一页游标，原样传入 page 参数续翻；无更多数据时为 null</p><strong>request_id</strong><code>string</code><p>本次请求的唯一标识</p></td><td><a id="h-list-resp"></a><h2>响应</h2><p>响应包含 <code>data</code>（会话资源对象数组）与 <code>next_page</code>（下一页游标，无更多数据时为 <code>null</code>）。</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;sesrsc_xxx&quot;,
      &quot;type&quot;: &quot;file&quot;,
      &quot;file_id&quot;: &quot;file_xxx&quot;,
      &quot;mount_path&quot;: &quot;/mnt/session/uploads/data.csv&quot;,
      &quot;created_at&quot;: &quot;2026-05-28T08:23:11.456000Z&quot;,
      &quot;updated_at&quot;: &quot;2026-05-28T08:23:11.456000Z&quot;
    },
    {
      &quot;id&quot;: &quot;sesrsc_yyy&quot;,
      &quot;type&quot;: &quot;file&quot;,
      &quot;file_id&quot;: &quot;file_yyy&quot;,
      &quot;mount_path&quot;: &quot;/mnt/session/uploads/late.csv&quot;,
      &quot;created_at&quot;: &quot;2026-05-28T08:25:00.000000Z&quot;,
      &quot;updated_at&quot;: &quot;2026-05-28T08:25:00.000000Z&quot;
    }
  ],
  &quot;next_page&quot;: &quot;page_xxxxxxxxxxxxx&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-list-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
