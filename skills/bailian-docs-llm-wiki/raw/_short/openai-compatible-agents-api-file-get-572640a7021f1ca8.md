# 获取 Source file

根据源文件 ID 返回文件元数据。

## 接口

**GET** `/agents/file/{file_id}`

成功返回 `200` 和源文件元数据。该接口返回的字段与源文件列表、上传响应不同：使用 `bytes`、Unix 秒时间戳和 `object` 字段。

## 路径参数

**file\_id** `string` **（必选）**

源文件 ID

不提供源文件内容下载接口。

## 请求示例

curl

```
curl -sS "$BASE_URL/agents/file/file_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
import os
import requests

resp = requests.get(
    f"{os.environ['BASE_URL']}/agents/file/file_xxx",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
)
print(resp.status_code, resp.json())
```

### 响应字段

**id** `string`

源文件 ID

**object** `string`

源文件对象类型，固定为 `file`

**bytes** `integer`

文件大小，单位字节

**created\_at** `integer`

创建时间，Unix 秒

**filename** `string`

文件名

**status** `string`

文件状态：`uploaded`、`processed` 或 `error`。`processed` 表示文件可用；`uploaded` 表示已上传、正在内容审核；`error` 表示处理失败或未通过内容审核

## 响应示例

```
{
  "id": "file_xxx",
  "object": "file",
  "bytes": 18,
  "created_at": 1794321796,
  "filename": "input.txt",
  "status": "uploaded"
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在的源文件 ID

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
