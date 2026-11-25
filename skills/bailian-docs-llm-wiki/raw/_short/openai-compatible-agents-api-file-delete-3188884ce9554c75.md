# 删除 Source file

删除当前工作空间的 Agent API 源文件。

<a id="接口"></a>

<a id="h-oa-file-delete-endpoint"></a>

## 接口

**DELETE** `/agents/file/{file_id}`

成功返回 `200` 和删除信封。删除后再次删除返回 `404`，使用该源文件写入环境会失败。

<table><tbody><tr><td><a id="h-oa-file-delete-path"></a><h2>路径参数</h2><p><strong>file_id</strong> <code>string</code> <strong>（必选）</strong></p><p>源文件 ID</p><p>本接口没有请求体和 Query 参数。</p><p>删除源文件不会删除已经写入环境的副本，也不会删除已发布的 Artifact。</p><p>如果环境模板引用了该源文件，删除后从该模板创建环境会失败并返回 <code>404 File not found</code>。</p></td><td><a id="h-oa-file-delete-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X DELETE &quot;$BASE_URL/agents/file/file_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import requests

resp = requests.delete(
    f&quot;{os.environ['BASE_URL']}/agents/file/file_xxx&quot;,
    headers={&quot;Authorization&quot;: f&quot;Bearer {os.environ['DASHSCOPE_API_KEY']}&quot;},
)
print(resp.status_code, resp.json())
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-file-delete-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>被删除的源文件 ID</p><p><strong>object</strong> <code>string</code></p><p>源文件删除结果对象类型，固定为 <code>file.deleted</code></p><p><strong>deleted</strong> <code>boolean</code></p><p>是否删除成功，删除成功时为 <code>true</code></p></td><td><a id="h-oa-file-delete-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;file_xxx&quot;,
  &quot;object&quot;: &quot;file.deleted&quot;,
  &quot;deleted&quot;: true
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-file-delete-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在的源文件 ID |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
