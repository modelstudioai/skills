# 获取 Memory Store

获取指定记忆库的元数据。

<a id="前提"></a>

<a id="h-get-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-get-endpoint"></a>

## 接口

**GET** `/memory_stores/{memory_store_id}`

<table><tbody><tr><td><a id="h-get-path"></a><h2>路径参数</h2><p><strong>memory_store_id</strong> <code>string</code> <strong>（必选）</strong></p><p>记忆库 ID</p></td><td><a id="h-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/memory_stores/memstore_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-get-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>记忆库 ID，格式 memstore_xxx</p><p><strong>type</strong> <code>string</code></p><p>固定为 memory_store</p><p><strong>name</strong> <code>string</code></p><p>记忆库名称，1-255 字符</p><p><strong>description</strong> <code>string</code></p><p>用途说明；未填写时为空字符串</p><p><strong>metadata</strong> <code>object</code></p><p>业务自定义键值对元数据</p><p><strong>archived_at</strong> <code>string | null</code></p><p>归档时间，未归档时省略或为 null</p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，ISO 8601 UTC</p><p><strong>updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601 UTC</p></td><td><a id="h-get-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;memstore_xxx&quot;,
  &quot;type&quot;: &quot;memory_store&quot;,
  &quot;name&quot;: &quot;项目知识库&quot;,
  &quot;description&quot;: &quot;项目约定、决策记录与排查笔记&quot;,
  &quot;metadata&quot;: {
    &quot;team&quot;: &quot;data&quot;
  },
  &quot;created_at&quot;: &quot;2026-09-17T08:00:00Z&quot;,
  &quot;updated_at&quot;: &quot;2026-09-17T08:00:00Z&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-get-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 401 | `InvalidApiKey` | API Key 缺失、错误或失效 |
| 403 | `permission_error` | 身份或资源访问权限不足 |
| 404 | `not_found_error` | 资源不存在或不属于当前工作空间 |
