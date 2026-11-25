# 运行时挂载资源

在会话运行期间动态挂载一个文件。服务端会将文件复制一份内部副本，并把挂载路径加上 /mnt/session/uploads/ 前缀。此操作不产生会话事件。

<a id="前提"></a>

<a id="h-create-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-create-endpoint"></a>

## 接口

**POST** `/sessions/{session_id}/resources`

<a id="路径参数"></a>

<a id="h-create-path"></a>

## 路径参数

**session\_id** `string` **（必选）**

会话 ID，格式 sesn\_<ULID>

<table><tbody><tr><td><a id="h-create-req"></a><h2>请求体</h2><strong>type</strong><code>string</code><strong>（必选）</strong><p>资源类型，固定为 file</p><strong>file_id</strong><code>string</code><strong>（必选）</strong><p>已上传的文件 ID</p><strong>mount_path</strong><code>string</code><strong>（必选）</strong><p>挂载路径，以 /uploads 开头</p></td><td><a id="h-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/sessions/sesn_xxx/resources&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;type&quot;: &quot;file&quot;,
    &quot;file_id&quot;: &quot;file_xxx&quot;,
    &quot;mount_path&quot;: &quot;/uploads/workspace/late.csv&quot;
  }'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-create-dto"></a><h3>响应字段</h3><strong>id</strong><code>string</code><p>资源 ID，格式 sesrsc_&lt;ULID&gt;</p><strong>type</strong><code>string</code><p>资源类型，固定为 file</p><strong>file_id</strong><code>string</code><p>内部副本的文件 ID，与请求中的 file_id 不同</p><strong>mount_path</strong><code>string</code><p>会话内的完整挂载路径</p><strong>created_at</strong><code>string</code><p>创建时间，ISO 8601</p><strong>updated_at</strong><code>string</code><p>最近更新时间，ISO 8601</p><strong>request_id</strong><code>string</code><p>本次请求的唯一标识</p></td><td><a id="h-create-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sesrsc_xxx&quot;,
  &quot;type&quot;: &quot;file&quot;,
  &quot;file_id&quot;: &quot;file_xxx&quot;,
  &quot;mount_path&quot;: &quot;/mnt/session/uploads/workspace/late.csv&quot;,
  &quot;created_at&quot;: &quot;2026-05-28T08:25:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-05-28T08:25:00Z&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-create-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
