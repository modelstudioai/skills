# 上传 File

通过 multipart/form-data 上传 Agent API 源文件，取得 file\_id。

## 接口

**POST** `/agents/file`

使用 `multipart/form-data` 上传当前工作空间的源文件。成功返回 `200` 和文件元数据。上传与写入环境是两步操作，拿到 `file_id` 后还需[写入环境文件](raw/_short/openai-compatible-agents-api-environment-file-cr-f8552f442d3bb910.md)。

## 请求体

**file** `二进制文件` **（必选）**

表单中的文件部分；文件名从表单解析，`mime_type` 由服务端检测

不需要 `purpose` 字段。服务端固定按 Agent API 来源保存文件。上传大小受网关和内容审核限制。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/agents/file" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -F "file=@input.txt;type=text/plain"
```

### 响应字段

**id** `string`

源文件 ID

**type** `string`

资源类型，固定为 `file`

**filename** `string`

文件名

**mime\_type** `string`

服务端检测的 MIME 类型

**size\_bytes** `integer`

文件大小，单位字节

**downloadable** `boolean`

平台元数据标记，不能替代环境下发的审核判断

**status** `string`

文件状态：`checking`、`available`、`rejected`、`type_rejected` 等

**created\_at** `string`

创建时间，RFC3339 时间字符串

**request\_id** `string`

本次上传请求标识

上传成功不表示文件已通过检查或可以立即写入环境。文件处于检查中或检查未通过时，写入环境可能失败或等待。

## 响应示例

```
{
  "id": "file_xxx",
  "type": "file",
  "filename": "input.txt",
  "mime_type": "text/plain",
  "size_bytes": 18,
  "downloadable": false,
  "status": "checking",
  "created_at": "2026-11-06T00:00:00Z",
  "request_id": "req_xxx"
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`，`param=file`

选择非空文件后重试

`413`

`invalid_request_error` / `invalid_request_error`，`param=file`

减小文件大小后重试

—

可能返回 `No such File` 或 batch 用途限制

改用 `/agents/file` 上传源文件

网关拒绝可能使用不同状态和结构。排查时保留 HTTP 状态、`x-request-id` 和文件元数据。
