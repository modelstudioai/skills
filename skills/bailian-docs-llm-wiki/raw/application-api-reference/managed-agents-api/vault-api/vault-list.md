# 列出 Vault

分页列出工作空间下的 Vault，默认不包含已归档项。

<a id="前提"></a>

<a id="h-list-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-list-endpoint"></a>

## 接口

**GET** `/vaults`

<table><tbody><tr><td><a id="h-list-query"></a><h2>Query 参数</h2><p><strong>include_archived</strong> <code>boolean</code> <strong>（可选）</strong></p><p>是否包含已归档 Vault，默认 false</p><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页返回数量，默认 20，最大 100</p><p><strong>page</strong> <code>string</code> <strong>（可选）</strong></p><p>分页游标，取自上一页响应的 next_page 值</p></td><td><a id="h-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/vaults?include_archived=true&amp;limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-list-dto"></a><h3>响应字段</h3><p><strong>data</strong> <code>array&lt;object&gt;</code></p><p>Vault 对象数组</p><p><strong>data[].id</strong> <code>string</code></p><p>Vault ID，格式 <code>vlt_xxx</code></p><p><strong>data[].type</strong> <code>string</code></p><p>固定为 <code>vault</code></p><p><strong>data[].display_name</strong> <code>string</code></p><p>Vault 可读名称</p><p><strong>data[].metadata</strong> <code>object</code></p><p>业务自定义键值对</p><p><strong>data[].archived_at</strong> <code>string | null</code></p><p>归档时间，未归档时为 null</p><p><strong>data[].created_at</strong> <code>string</code></p><p>创建时间，ISO 8601</p><p><strong>data[].updated_at</strong> <code>string</code></p><p>最近更新时间，ISO 8601</p><p><strong>next_page</strong> <code>string | null</code></p><p>下一页游标；无更多数据时为 null</p></td><td><a id="h-list-resp"></a><h2>响应</h2><p>响应包含 <code>data</code>（密钥库对象数组）与 <code>next_page</code>（下一页游标，无更多数据时为 <code>null</code>）。</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;vlt_xxx&quot;,
      &quot;type&quot;: &quot;vault&quot;,
      &quot;display_name&quot;: &quot;生产环境密钥箱&quot;,
      &quot;metadata&quot;: {
        &quot;environment&quot;: &quot;production&quot;
      },
      &quot;archived_at&quot;: null,
      &quot;created_at&quot;: &quot;2026-06-20T10:00:00Z&quot;,
      &quot;updated_at&quot;: &quot;2026-06-20T10:00:00Z&quot;
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
