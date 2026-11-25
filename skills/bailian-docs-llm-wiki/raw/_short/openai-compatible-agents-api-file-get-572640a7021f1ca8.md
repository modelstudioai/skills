# 获取 Source file

根据源文件 ID 返回文件元数据。

<a id="接口"></a>

<a id="h-oa-file-get-endpoint"></a>

## 接口

**GET** `/agents/file/{file_id}`

成功返回 `200` 和源文件元数据。该接口返回的字段与源文件列表、上传响应不同：使用 `bytes`、Unix 秒时间戳和 `object` 字段。

<table><tbody><tr><td><a id="h-oa-file-get-path"></a><h2>路径参数</h2><p><strong>file_id</strong> <code>string</code> <strong>（必选）</strong></p><p>源文件 ID</p><p>不提供源文件内容下载接口。</p></td><td><a id="h-oa-file-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/agents/file/file_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.get(
    f&quot;{os.environ['BASE_URL']}/agents/file/file_xxx&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
)
print(resp.status_code, resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-file-get-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>源文件 ID</p><p><strong>object</strong> <code>string</code></p><p>源文件对象类型，固定为 <code>file</code></p><p><strong>bytes</strong> <code>integer</code></p><p>文件大小，单位字节</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>filename</strong> <code>string</code></p><p>文件名</p><p><strong>status</strong> <code>string</code></p><p>文件状态：<code>uploaded</code>、<code>processed</code> 或 <code>error</code>。<code>processed</code> 表示文件可用；<code>uploaded</code> 表示已上传、正在内容审核；<code>error</code> 表示处理失败或未通过内容审核</p></td><td><a id="h-oa-file-get-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;file_xxx&quot;,
  &quot;object&quot;: &quot;file&quot;,
  &quot;bytes&quot;: 18,
  &quot;created_at&quot;: 1794321796,
  &quot;filename&quot;: &quot;input.txt&quot;,
  &quot;status&quot;: &quot;uploaded&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-file-get-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在的源文件 ID |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
