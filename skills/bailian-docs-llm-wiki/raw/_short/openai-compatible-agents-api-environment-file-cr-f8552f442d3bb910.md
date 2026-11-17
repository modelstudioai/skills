# 写入 Environment file

将当前工作空间的源文件写入指定环境路径。

## 接口

**POST** `/agents/environments/{environment_id}/files`

将源文件写入指定环境的 `/workspace/` 路径。成功返回 `201` 和环境文件信息。写入成功只表示文件已经落盘，不表示模型已经读取。

## 路径参数

**environment\_id** `string` **（必选）**

环境 ID，当前工作空间中的环境

## 请求体

**type** `string` **（必选）**

文件引用类型，固定为 `file_id`

**file\_id** `string` **（必选）**

源文件 ID，来自当前工作空间的 Agent API 上传

**path** `string` **（必选）**

文件路径；`/workspace/` 内的规范绝对文件路径，不能包含目录穿越

请求体不接受额外字段。源文件必须来自当前工作空间的 Agent API 上传。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/agents/environments/ccarenv_xxx/files" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "file_id",
    "file_id": "file_xxx",
    "path": "/workspace/input/input.txt"
  }'
```

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["BASE_URL"],
)

environment_file = client.beta.agents.environments.files.create(
    "ccarenv_xxx",
    type="file_id",
    file_id="file_xxx",
    path="/workspace/input/input.txt",
)
print(environment_file.path, environment_file.size_bytes)
```

### 响应字段

**environment\_id** `string`

环境 ID

**object** `string`

环境文件对象类型，固定为 `agent.environment.file`

**path** `string`

环境内文件路径

**size\_bytes** `integer`

本次写入的字节数

响应没有新的源文件 ID，也不是 Artifact 发布回执。

## 响应示例

```
{
  "environment_id": "ccarenv_xxx",
  "object": "agent.environment.file",
  "path": "/workspace/input/input.txt",
  "size_bytes": 18
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按字段说明补齐必填字段，并修正 `type`、`path`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且可见的源文件 ID

`400`

`invalid_request_error` / `invalid_request_error`，`param=file_id`

使用通过 `POST /agents/file` 上传的源文件

`409`

`invalid_request_error` / `file_not_available`，`param=file_id`

更换为审核通过且可用的源文件

`504`

`server_error` / `environment_file_timeout`

稍后重试；持续失败时提交工单并提供 `x-request-id`

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。
