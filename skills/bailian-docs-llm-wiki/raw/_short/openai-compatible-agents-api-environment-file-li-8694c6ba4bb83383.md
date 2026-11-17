# 列出 Environment file

查询指定环境中已落盘的文件和目录分页。

## 接口

**GET** `/agents/environments/{environment_id}/files`

查询指定环境中的实时文件。成功返回 `200` 和目录分页。该接口用于核对文件是否已经落盘，不返回文件正文。

## 查询参数

**path** `string` **（可选）**

目录路径，可选，限定 `/workspace/` 内已存在的绝对目录

**limit** `integer` **（可选）**

每页数量

**page** `string` **（可选）**

分页游标；首次不传，后续传上一页返回的 `next`

分页请求参数名是 `page`，响应游标字段是 `next`；不是源文件或 Artifact 的 `after`。

## 请求示例

curl

```
curl -sS --get "$BASE_URL/agents/environments/ccarenv_xxx/files" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  --data-urlencode "path=/workspace/input/" \
  --data-urlencode "limit=20"
```

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["BASE_URL"],
)

page = client.beta.agents.environments.files.list(
    "ccarenv_xxx",
    path="/workspace/input/",
    limit=20,
)
for environment_file in page.data:
    print(environment_file.path, environment_file.size_bytes)
```

### 响应字段

**object** `string`

分页对象类型，固定为 `page`

**data** `array`

当前页的环境文件

**next** `string / null`

下一页游标；没有下一页时为 `null`

**has\_more** `boolean`

是否还有下一页

`data[]` 中每一项包含：

响应包含当前页的 `data` 数组和下一页游标。目录为空时 `data` 为空数组。

data 项

**environment\_id** `string`

环境 ID

**object** `string`

环境文件对象类型，固定为 `agent.environment.file`

**path** `string`

环境内文件路径

**size\_bytes** `integer`

文件大小，单位字节

## 响应示例

```
{
  "object": "page",
  "data": [
    {
      "environment_id": "ccarenv_xxx",
      "object": "agent.environment.file",
      "path": "/workspace/input/input.txt",
      "size_bytes": 18
    }
  ],
  "next": null,
  "has_more": false
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

传入 `/workspace/` 内已存在的绝对目录

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且可见的环境 ID

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。
