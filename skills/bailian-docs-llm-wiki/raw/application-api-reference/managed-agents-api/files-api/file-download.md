# 下载 File

下载文件内容，直接返回文件的原始二进制流（不返回 JSON，也不返回预签名 URL）。响应带 Content-Type（随文件实际类型返回）与 Content-Length 头。 仅 downloadable 为 true 的文件可下载；当前接口直传与会话沙箱拷贝的文件 downloadable 均为 false，调用会返回 400。

<a id="前提"></a>

<a id="h-download-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-download-endpoint"></a>

## 接口

**GET** `/files/{file_id}/content`

<table><tbody><tr><td><a id="h-download-path"></a><h2>路径参数</h2><p><strong>file_id</strong> <code>string</code> <strong>（必选）</strong></p><p>文件 ID</p></td><td><a id="h-download-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/files/file_xxx/content&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<a id="响应"></a>

<a id="h-download-resp"></a>

## 响应

成功，返回文件原始二进制流。

<a id="错误码"></a>

<a id="h-download-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `invalid_request_error` | File '...' is not downloadable |
| 401 | `InvalidApiKey` | Invalid API-key provided. |
| 404 | `not_found_error` | File not found. |
