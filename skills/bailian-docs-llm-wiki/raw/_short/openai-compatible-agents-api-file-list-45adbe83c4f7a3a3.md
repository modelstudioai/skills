# 列出 Source file

分页列出当前工作空间的 Agent API 源文件。

## 接口

**GET** `/agents/file`

成功返回 `200` 和列表信封。只返回当前工作空间内通过 Agent API 上传的源文件，不返回产物或环境内的实时文件。

## 查询参数

**limit** `integer` **（可选）**

每页数量，默认 20；建议使用 `1..100`

**order** `string` **（可选）**

排序方向，`asc` 或 `desc`，默认 `desc`

**after** `string` **（可选）**

上一页的 `last_id`；不包含游标项

**before** `string` **（可选）**

上一页的 `first_id`，用于反向翻页，不能与 `after` 同时使用

同时传 `after` 和 `before` 返回 `400`。游标不存在、已删除或不属于当前工作空间时返回 `404`。

## 请求示例

curl

```
curl -sS "$BASE_URL/agents/file?limit=20&order=desc" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
import os
import requests

resp = requests.get(
    f"{os.environ['BASE_URL']}/agents/file",
    params={"limit": 20, "order": "desc"},
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
)
print(resp.status_code, resp.json())
```

### 响应字段

**object** `string`

列表对象类型，固定为 `list`

**data** `array`

当页源文件；空时为 `[]`

**first\_id** `string / null`

当页首项 ID。空页为 `null`

**last\_id** `string / null`

当页末项 ID。空页为 `null`。后续 `after` 使用该值

**has\_more** `boolean`

当前检索方向是否还有下一页

`data[]` 中的每个源文件与获取源文件的响应字段一致。

源文件列表项不包含 `request_id`；本次请求标识从响应头 `x-request-id` 获取。

data 项

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
  "object": "list",
  "data": [
    {
      "id": "file_xxx",
      "object": "file",
      "bytes": 18,
      "created_at": 1794321796,
      "filename": "input.txt",
      "status": "processed"
    }
  ],
  "first_id": "file_xxx",
  "last_id": "file_xxx",
  "has_more": false
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按查询参数说明修正 `limit`、`order`、`after`、`before`

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中有效的源文件游标

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
