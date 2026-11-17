# 下载 Artifact

下载不可变产物版本的原始二进制内容。

## 接口

**GET** `/agents/sessions/{session_id}/artifacts/{artifact_id}/content`

下载指定 Artifact 的原始内容。成功返回 `200` 和二进制流。

## 路径参数

**session\_id** `string` **（必选）**

Artifact 所属 Session

**artifact\_id** `string` **（必选）**

列表返回的 Artifact 版本 ID

无请求体。可以发送 `Accept: application/octet-stream`。

## 请求示例

curl

```
curl --fail-with-body -sS -D headers.txt -o artifact.part \
  "$BASE_URL/agents/sessions/sess_xxx/artifacts/artifact_xxx/content" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Accept: application/octet-stream"

if [ $? -eq 0 ]; then
  mv artifact.part artifact.bin
  wc -c artifact.bin
else
  echo "download failed"
  rm -f artifact.part
  exit 1
fi
```

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["BASE_URL"],
)

content = client.beta.agents.sessions.artifacts.content(
    "artifact_xxx",
    session_id="sess_xxx",
)
with open("artifact.bin", "wb") as output:
    output.write(content.content)
print(len(content.content))
```

## 响应示例

```
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Length: 19
Content-Disposition: attachment; filename="report.txt"
```

成功响应的 `Content-Type` 为 `application/octet-stream`，并带有附件文件名。常见响应头：

响应头

说明

`Content-Type`

`application/octet-stream`

`Content-Length`

文件字节数

`Content-Disposition`

`attachment` 和文件名

`Cache-Control`

`private, no-store`

错误仍返回 JSON，不要把错误 Body 当作产物内容。建议先下载到临时文件，确认 HTTP 状态后再重命名。

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且未删除的 Artifact ID

错误正文形如 `{"error":{"type","code","message","param"}}`，网关或路由错误可能使用不同结构。排查时保留 HTTP 状态、响应头、`x-request-id` 和 Artifact ID。
