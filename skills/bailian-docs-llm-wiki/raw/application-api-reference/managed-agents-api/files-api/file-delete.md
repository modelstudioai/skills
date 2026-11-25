# 删除 File

硬删除文件元数据与原始内容，不可恢复。已挂载到会话沙箱的内部拷贝不受影响；新会话无法再挂载该 file\_id。

<a id="前提"></a>

<a id="h-fd-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-fd-endpoint"></a>

## 接口

**DELETE** `/files/{file_id}`

<a id="请求示例"></a>

<a id="h-fd-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X DELETE "$AGENTSTUDIO_URL/files/file_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
client.files.delete("file_xxx")
```

<a id="fig-code-group-python-sdk-tab"></a>

Python SDK

<a id="code-code-group-python-sdk"></a>

```python
import os
import dashscope

client = dashscope.Client(api_key=os.getenv('DASHSCOPE_API_KEY'))

# 删除文件
result = client.files.delete('file-xxx')
print(result.deleted)
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
client.files().delete("file_xxx");
```

<table><tbody><tr><td><a id="h-fd-dto"></a><h3>响应字段</h3><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-fd-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
