# 上传 File

通过 multipart/form-data 上传 Agent API 源文件，取得 file\_id。

<a id="接口"></a>

<a id="h-oa-file-upload-api"></a>

## 接口

**POST** `/agents/file`

使用 `multipart/form-data` 上传当前工作空间的源文件。成功返回 `200` 和文件元数据。上传与写入环境是两步操作，拿到 `file_id` 后还需[写入环境文件](openai-compatible-agents-api-environment-file-cr-f8552f442d3bb910.md)。

<table><tbody><tr><td><a id="h-oa-file-upload-params"></a><h2>请求体</h2><p><strong>file</strong> <code>二进制文件</code> <strong>（必选）</strong></p><p>表单中的文件部分；文件名从表单解析，<code>mime_type</code> 由服务端检测</p><p>不需要 <code>purpose</code> 字段。服务端固定按 Agent API 来源保存文件。上传大小受网关和内容审核限制。</p></td><td><a id="h-oa-file-upload-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/agents/file&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  -F &quot;file=@input.txt;type=text/plain&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-file-upload-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>源文件 ID</p><p><strong>type</strong> <code>string</code></p><p>资源类型，固定为 <code>file</code></p><p><strong>filename</strong> <code>string</code></p><p>文件名</p><p><strong>mime_type</strong> <code>string</code></p><p>服务端检测的 MIME 类型</p><p><strong>size_bytes</strong> <code>integer</code></p><p>文件大小，单位字节</p><p><strong>downloadable</strong> <code>boolean</code></p><p>平台元数据标记，不能替代环境下发的审核判断</p><p><strong>status</strong> <code>string</code></p><p>文件状态：<code>checking</code>、<code>available</code>、<code>rejected</code>、<code>type_rejected</code> 等</p><p><strong>created_at</strong> <code>string</code></p><p>创建时间，RFC3339 时间字符串</p><p><strong>request_id</strong> <code>string</code></p><p>本次上传请求标识</p><p>上传成功不表示文件已通过检查或可以立即写入环境。文件处于检查中或检查未通过时，写入环境可能失败或等待。</p></td><td><a id="h-oa-file-upload-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;file_xxx&quot;,
  &quot;type&quot;: &quot;file&quot;,
  &quot;filename&quot;: &quot;input.txt&quot;,
  &quot;mime_type&quot;: &quot;text/plain&quot;,
  &quot;size_bytes&quot;: 18,
  &quot;downloadable&quot;: false,
  &quot;status&quot;: &quot;checking&quot;,
  &quot;created_at&quot;: &quot;2026-11-06T00:00:00Z&quot;,
  &quot;request_id&quot;: &quot;req_xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-file-upload-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error`，`param=file` | 选择非空文件后重试 |
| `413` | `invalid_request_error` / `invalid_request_error`，`param=file` | 减小文件大小后重试 |
| — | 可能返回 `No such File` 或 batch 用途限制 | 改用 `/agents/file` 上传源文件 |

网关拒绝可能使用不同状态和结构。排查时保留 HTTP 状态、`x-request-id` 和文件元数据。
