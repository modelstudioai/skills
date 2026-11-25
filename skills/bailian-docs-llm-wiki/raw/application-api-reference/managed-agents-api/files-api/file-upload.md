# 上传 File

使用 multipart/form-data 上传单个文件，最大 50 MB。上传后进入安全审核，available 状态才可挂载或作为消息内容。

<a id="前提"></a>

<a id="h-fu-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="配额与限制"></a>

<a id="h-fu-quota"></a>

## 配额与限制

-   单个工作空间下文件总容量上限为 **100 GB**。
-   文件保存时效为 **30 天**，超过 30 天的文件不保证可用，可能被自动清理。需要长期保留请定期重新上传。
-   通过该接口直传的单个文件最大 **50 MB**。

<a id="接口"></a>

<a id="h-fu-endpoint"></a>

## 接口

**POST** `/files`

使用 `multipart/form-data` 编码。`filename` 自动从表单部分获取，`mime_type` 由服务端检测。

<a id="请求示例"></a>

<a id="h-fu-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X POST "$AGENTSTUDIO_URL/files" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -F "file=@./sales_2025.csv"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
file = client.files.upload("sales_2025.csv")
print(file.id)
```

<a id="fig-code-group-python-sdk-tab"></a>

Python SDK

<a id="code-code-group-python-sdk"></a>

```python
import os
import dashscope

client = dashscope.Client(api_key=os.getenv('DASHSCOPE_API_KEY'))

# 上传文件（purpose='fine-tune' 用于微调训练文件，purpose='inference' 用于推理临时文件）
result = client.files.upload(
    file_path='sales_2025.csv',
    purpose='fine-tune',
)
print(result.file_id, result.name)
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
AgentStudioFile file = client.files().upload(Paths.get("sales_2025.csv"), "text/csv");
System.out.println(file.getId());
```

<table><tbody><tr><td><a id="h-fu-dto"></a><h3>响应字段</h3><p>响应为 File 对象。字段如下：</p><p><strong>id</strong> <code>string</code></p><p>文件 ID，格式 <code>file_&lt;24位字母数字&gt;</code>（如 <code>file_maznwes8t9rsysg5r5enkvpr</code>）</p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>file</code></p><p><strong>filename</strong> <code>string</code></p><p>文件名（自上传时表单部分解析得到）</p><p><strong>mime_type</strong> <code>string</code></p><p>服务端检测的 MIME 类型</p><p><strong>size_bytes</strong> <code>int</code></p><p>文件大小，单位字节</p><p><strong>downloadable</strong> <code>bool</code></p><p>是否支持下载。当前接口直传与会话沙箱拷贝均为 <code>false</code></p><p><strong>status</strong> <code>string</code></p><p>安全审核状态：<code>available</code>（通过，可挂载） / <code>checking</code>（审核中） / <code>rejected</code>（内容未通过） / <code>type_rejected</code>（类型不支持）。新上传文件默认 <code>checking</code></p><p><strong>created_at</strong> <code>string</code></p><p>上传时间，ISO 8601</p><p><strong>requestId</strong> <code>string</code></p><p>本次请求的唯一标识。Python SDK 中对应属性为 <code>request_id</code></p></td><td><a id="h-fu-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;file_xxx&quot;,
  &quot;type&quot;: &quot;file&quot;,
  &quot;filename&quot;: &quot;sales_2025.csv&quot;,
  &quot;downloadable&quot;: false,
  &quot;mime_type&quot;: &quot;text/csv&quot;,
  &quot;size_bytes&quot;: 524288,
  &quot;status&quot;: &quot;checking&quot;,
  &quot;created_at&quot;: &quot;2026-06-16T14:51:39+08:00&quot;,
  &quot;requestId&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="作用域"></a>

<a id="h-fu-scope"></a>

## 作用域

普通上传返回的文件无 `scope` 字段（默认工作空间共享）；当文件被挂载到会话沙箱时，服务端会做内部拷贝并生成新的 `file_id`，该副本的元数据中带 `scope: {"type": "session", "id": "sesn_..."}`，仅对应会话可见。
