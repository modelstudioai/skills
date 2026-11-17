# 删除 Artifact

删除单个不可变产物版本，不影响其他版本和环境原文件。

## 接口

**DELETE** `/agents/sessions/{session_id}/artifacts/{artifact_id}`

删除指定的 Artifact 版本。成功返回 `200` 和删除信封。

## 路径参数

**session\_id** `string` **（必选）**

Artifact 所属 Session

**artifact\_id** `string` **（必选）**

要删除的 Artifact 版本 ID

无请求体。

## 请求示例

curl

```
curl -sS -X DELETE \
  "$BASE_URL/agents/sessions/sess_xxx/artifacts/artifact_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["BASE_URL"],
)

deleted = client.beta.agents.sessions.artifacts.delete(
    "artifact_xxx",
    session_id="sess_xxx",
)
print(deleted.deleted)
```

### 响应字段

**id** `string`

被删除的 Artifact 版本 ID

**object** `string`

Artifact 删除结果对象类型，固定为 `agent.session.artifact.deleted`

**deleted** `boolean`

是否删除成功，成功为 `true`

删除只移除指定的 Artifact 版本。删除后详情、下载和重复删除返回 `404`，列表不再出现该版本。删除 Artifact 不等于删除沙箱中的原文件，也不等于删除上传的源文件。

## 响应示例

```
{
  "id": "artifact_xxx",
  "object": "agent.session.artifact.deleted",
  "deleted": true
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且未删除的 Artifact ID

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。
