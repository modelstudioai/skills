# 查询 File

返回文件元数据（不含内容），常用于确认上传后的安全审核 status 是否已转为 available。

<a id="前提"></a>

<a id="h-fg-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-fg-endpoint"></a>

## 接口

**GET** `/files/{file_id}`

返回文件元数据（`filename`、`size_bytes`、`mime_type`、`created_at`、`status`），不含内容。`scope` 字段仅在会话沙箱内部拷贝上返回。

<a id="状态说明"></a>

<a id="h-fg-status"></a>

## 状态说明

`status` 表示安全审核结果，取值：`available`（审核通过，可挂载到会话）、`checking`（审核中）、`rejected`（内容未通过审核）、`type_rejected`（文件类型不支持）。仅 `available` 状态的文件可被挂载到会话或作为消息内容引用。

<a id="请求示例"></a>

<a id="h-fg-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl "$AGENTSTUDIO_URL/files/file_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
file = client.files.retrieve("file_xxx")
print(file.filename, file.size_bytes, file.mime_type)
```

<a id="fig-code-group-python-sdk-tab"></a>

Python SDK

<a id="code-code-group-python-sdk"></a>

```python
import os
import dashscope

client = dashscope.Client(api_key=os.getenv('DASHSCOPE_API_KEY'))

# 查询文件信息（返回文件元数据，不含内容）
result = client.files.get('file-xxx')
print(result.file_id, result.name, result.size)
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
AgentStudioFile f = client.files().retrieve("file_xxx");
System.out.println(f.getFilename() + " " + f.getSizeBytes());
```

<table><tbody><tr><td><a id="h-fg-dto"></a><h3>响应字段</h3><p>响应为 File 对象。字段如下：</p><p><strong>id</strong> <code>string</code></p><p>文件 ID，格式如 <code>file_kyu8k8lut4d4x47ii7qf92yk</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>file</code></p><p><strong>filename</strong> <code>string</code></p><p>文件名</p><p><strong>mime_type</strong> <code>string</code></p><p>服务端检测的 MIME 类型</p><p><strong>size_bytes</strong> <code>int</code></p><p>文件大小，单位字节</p><p><strong>downloadable</strong> <code>bool</code></p><p>是否支持下载，当前接口直传与会话沙箱拷贝均为 <code>false</code></p><p><strong>status</strong> <code>string</code></p><p>安全审核状态：<code>available</code> / <code>checking</code> / <code>rejected</code> / <code>type_rejected</code></p><p><strong>scope</strong> <code>object</code></p><p>仅会话沙箱内部拷贝返回，结构 <code>{&quot;type&quot;: &quot;session&quot;, &quot;id&quot;: &quot;sesn_...&quot;}</code>；普通上传文件不返回该字段</p><p><strong>created_at</strong> <code>string</code></p><p>上传时间，ISO 8601</p><p><strong>requestId</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-fg-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;file_xxx&quot;,
  &quot;type&quot;: &quot;file&quot;,
  &quot;filename&quot;: &quot;sales_2025.csv&quot;,
  &quot;downloadable&quot;: false,
  &quot;mime_type&quot;: &quot;text/csv&quot;,
  &quot;size_bytes&quot;: 524288,
  &quot;status&quot;: &quot;available&quot;,
  &quot;created_at&quot;: &quot;2026-06-16T14:51:39+08:00&quot;,
  &quot;requestId&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
