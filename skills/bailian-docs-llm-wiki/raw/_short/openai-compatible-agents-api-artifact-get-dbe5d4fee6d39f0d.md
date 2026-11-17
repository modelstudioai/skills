# 获取 Artifact

查询单个不可变产物版本的元数据。

## 接口

**GET** `/agents/sessions/{session_id}/artifacts/{artifact_id}`

返回指定 Artifact 的元数据。成功返回 `200`，不返回文件正文。

## 路径参数

**session\_id** `string` **（必选）**

Artifact 所属 Session

**artifact\_id** `string` **（必选）**

列表返回的 Artifact 版本 ID，不是 `file_id` 或快照 ID

无请求体。

## 请求示例

curl

```
curl -sS "$BASE_URL/agents/sessions/sess_xxx/artifacts/artifact_xxx" \
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

artifact = client.beta.agents.sessions.artifacts.retrieve(
    "artifact_xxx",
    session_id="sess_xxx",
)
print(artifact.id, artifact.path, artifact.size_bytes)
```

### 响应字段

**id** `string`

Artifact 版本 ID，不是 `file_id`

**object** `string`

Artifact 对象类型，固定为 `agent.session.artifact`

**session\_id** `string`

所属 Session

**environment\_id** `string`

发布来源环境

**turn\_id** `string`

发布来源 Turn

**path** `string`

产物生成时的沙箱完整路径

**size\_bytes** `integer`

文件大小，单位字节

**created\_at** `integer`

创建时间，Unix 秒

详情不返回底层存储标识、签名下载地址或凭据。

## 响应示例

```
{
  "id": "artifact_xxx",
  "object": "agent.session.artifact",
  "session_id": "sess_xxx",
  "environment_id": "ccarenv_xxx",
  "turn_id": "turn_xxx",
  "path": "/workspace/outputs/report.txt",
  "size_bytes": 19,
  "created_at": 1793941200
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
