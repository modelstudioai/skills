# 列出 Memory Store

分页列出当前工作空间的记忆库，按创建时间倒序。

<a id="前提"></a>

<a id="h-list-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-list-endpoint"></a>

## 接口

**GET** `/memory_stores`

<table><tbody><tr><td><a id="h-list-query"></a><h2>Query 参数</h2><p><strong>include_archived</strong> <code>boolean</code> <strong>（可选）</strong></p><p>默认 false 只返回未归档；true 同时返回未归档与已归档</p><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>单页条数，1-100，默认 20</p><p><strong>page</strong> <code>string</code> <strong>（可选）</strong></p><p>分页游标。首次不传，后续传上一次响应的 next_page 翻下一页</p></td><td><a id="h-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/memory_stores&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-list-dto"></a><h3>响应字段</h3><p><strong>data</strong> <code>array&lt;object&gt;</code></p><p>记忆库数组</p><p><strong>id</strong> <code>string</code></p><p>记忆库 ID，格式 memstore_xxx</p><p><strong>type</strong> <code>string</code></p><p>固定为 memory_store</p><p><strong>name</strong> <code>string</code></p><p>记忆库名称，1-255 字符</p><p><strong>description</strong> <code>string</code></p><p>用途说明；未填写时为空字符串</p><p><strong>metadata</strong> <code>object</code></p><p>业务自定义键值对元数据</p><p><strong>archived_at</strong> <code>string | null</code></p><p>归档时间，未归档时省略或为 null</p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，ISO 8601 UTC</p><p><strong>updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601 UTC</p><p><strong>next_page</strong> <code>string | null</code></p><p>下一页游标；响应不含该字段或为 null 时表示末页</p></td><td><a id="h-list-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
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
  ],
  &quot;next_page&quot;: null
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-list-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `invalid_request_error` | 参数、路径、limit 或分页游标非法 |
| 401 | `InvalidApiKey` | API Key 缺失、错误或失效 |
| 403 | `permission_error` | 身份或资源访问权限不足 |
