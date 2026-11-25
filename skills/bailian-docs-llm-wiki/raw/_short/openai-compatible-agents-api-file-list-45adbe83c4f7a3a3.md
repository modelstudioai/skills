# 列出 Source file

分页列出当前工作空间的 Agent API 源文件。

<a id="接口"></a>

<a id="h-oa-file-list-endpoint"></a>

## 接口

**GET** `/agents/file`

成功返回 `200` 和列表信封。只返回当前工作空间内通过 Agent API 上传的源文件，不返回产物或环境内的实时文件。

<table><tbody><tr><td><a id="h-oa-file-list-query"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，默认 20；建议使用 <code>1..100</code></p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code>；不包含游标项</p><p><strong>before</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>first_id</code>，用于反向翻页，不能与 <code>after</code> 同时使用</p><p>同时传 <code>after</code> 和 <code>before</code> 返回 <code>400</code>。游标不存在、已删除或不属于当前工作空间时返回 <code>404</code>。</p></td><td><a id="h-oa-file-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/agents/file?limit=20&amp;order=desc&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.get(
    f&quot;{os.environ['BASE_URL']}/agents/file&quot;,
    params={&quot;limit&quot;: 20, &quot;order&quot;: &quot;desc&quot;},
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
)
print(resp.status_code, resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-file-list-response"></a><h3>响应字段</h3><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array</code></p><p>当页源文件；空时为 <code>[]</code></p><p><strong>first_id</strong> <code>string / null</code></p><p>当页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当页末项 ID。空页为 <code>null</code>。后续 <code>after</code> 使用该值</p><p><strong>has_more</strong> <code>boolean</code></p><p>当前检索方向是否还有下一页</p><p><code>data[]</code> 中的每个源文件与获取源文件的响应字段一致。</p><p>源文件列表项不包含 <code>request_id</code>；本次请求标识从响应头 <code>x-request-id</code> 获取。</p><a id="accordion-data-项"></a><section><p>data 项</p><div><p><strong>id</strong> <code>string</code></p><p>源文件 ID</p><p><strong>object</strong> <code>string</code></p><p>源文件对象类型，固定为 <code>file</code></p><p><strong>bytes</strong> <code>integer</code></p><p>文件大小，单位字节</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>filename</strong> <code>string</code></p><p>文件名</p><p><strong>status</strong> <code>string</code></p><p>文件状态：<code>uploaded</code>、<code>processed</code> 或 <code>error</code>。<code>processed</code> 表示文件可用；<code>uploaded</code> 表示已上传、正在内容审核；<code>error</code> 表示处理失败或未通过内容审核</p></div></section></td><td><a id="h-oa-file-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;file_xxx&quot;,
      &quot;object&quot;: &quot;file&quot;,
      &quot;bytes&quot;: 18,
      &quot;created_at&quot;: 1794321796,
      &quot;filename&quot;: &quot;input.txt&quot;,
      &quot;status&quot;: &quot;processed&quot;
    }
  ],
  &quot;first_id&quot;: &quot;file_xxx&quot;,
  &quot;last_id&quot;: &quot;file_xxx&quot;,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-file-list-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order`、`after`、`before` |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中有效的源文件游标 |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
