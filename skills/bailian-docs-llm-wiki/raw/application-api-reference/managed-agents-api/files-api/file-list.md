# 列出 File

分页列出工作空间下的文件，按 created\_at 倒序返回。可通过 scope\_id 仅列出某会话沙箱内的文件。

<a id="前提"></a>

<a id="h-fl-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-fl-endpoint"></a>

## 接口

**GET** `/files`

<table><tbody><tr><td><a id="h-fl-q"></a><h2>Query 参数</h2><p><strong>limit</strong> <code>int</code> 默认 20</p><p>每页数量，最大 100</p><p><strong>page</strong> <code>string</code> 默认 —</p><p>首次不传，后续传上一次响应的 <code>next_page</code></p><p><strong>scope_id</strong> <code>string</code> 默认 —</p><p>传入会话 ID，仅返回该会话沙箱内的文件</p></td><td><a id="h-fl-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/files?limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>for file in client.files.list(limit=20):
    print(file.id, file.filename, file.size_bytes)
</code></pre></div><a id="fig-code-group-python-sdk-tab"></a>Python SDK<div><a id="code-code-group-python-sdk"></a><pre class="language-python"><code>import os
import dashscope

client = dashscope.Client(api_key=os.getenv('DASHSCOPE_API_KEY'))

# 列出已上传的文件（page_no 为页码，page_size 为每页数量）
result = client.files.list(page_no=1, page_size=10)
print(result.files)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>CursorPage&lt;AgentStudioFile&gt; page = client.files().list(
    FileListParam.builder().limit(20).build());
for (AgentStudioFile f : page.getData()) {
    System.out.println(f.getId() + &quot; &quot; + f.getFilename() + &quot; &quot; + f.getSizeBytes());
}
</code></pre></div></div></td></tr></tbody></table>

<a id="响应示例"></a>

<a id="h-fl-resp"></a>

## 响应示例

<a id="code-block"></a>

```json
{
  "data": [
    {
      "id": "file_xxx",
      "type": "file",
      "filename": "sales_2025.csv",
      "downloadable": false,
      "mime_type": "text/csv",
      "size_bytes": 524288,
      "status": "available",
      "created_at": "2026-06-16T14:51:39+08:00"
    },
    {
      "id": "file_xxx",
      "type": "file",
      "filename": "demo.png",
      "downloadable": false,
      "mime_type": "image/png",
      "size_bytes": 102400,
      "status": "checking",
      "created_at": "2026-06-16T14:48:02+08:00"
    }
  ],
  "next_page": "xxx",
  "requestId": "xxx"
}
```

响应包含 `data`（File 对象数组）与 `next_page`。File 对象字段如下：

<a id="file-对象字段"></a>

<a id="h-fl-dto"></a>

### File 对象字段

**id** `string`

文件 ID，格式 `file_<24位字母数字>`

**type** `string`

固定为 `file`

**filename** `string`

文件名

**mime\_type** `string`

服务端检测的 MIME 类型

**size\_bytes** `int`

文件大小，单位字节

**downloadable** `bool`

是否支持下载，当前接口直传与会话沙箱拷贝均为 `false`

**status** `string`

安全审核状态：`available` / `checking` / `rejected` / `type_rejected`

**created\_at** `string`

上传时间，ISO 8601
