# 删除 Source file

删除当前工作空间的 Agent API 源文件。

## 接口

**DELETE** `/agents/file/{file_id}`

成功返回 `200` 和删除信封。删除后再次删除返回 `404`，使用该源文件写入环境会失败。

## 路径参数

**file\_id** `string` **（必选）**

源文件 ID

本接口没有请求体和 Query 参数。

删除源文件不会删除已经写入环境的副本，也不会删除已发布的 Artifact。

如果环境模板引用了该源文件，删除后从该模板创建环境会失败并返回 `404 File not found`。

## 请求示例

curl

```
curl -sS -X DELETE "$BASE_URL/agents/file/file_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
import os
import requests

resp = requests.delete(
    f"{os.environ['BASE_URL']}/agents/file/file_xxx",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
)
print(resp.status_code, resp.json())
```

### 响应字段

**id** `string`

被删除的源文件 ID

**object** `string`

源文件删除结果对象类型，固定为 `file.deleted`

**deleted** `boolean`

是否删除成功，删除成功时为 `true`

## 响应示例

```
{
  "id": "file_xxx",
  "object": "file.deleted",
  "deleted": true
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
