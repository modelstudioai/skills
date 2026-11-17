# 列出 Artifact

分页列出 Session 已发布的不可变产物版本。

## 接口

**GET** `/agents/sessions/{session_id}/artifacts`

分页列出指定 Session 已发布的 Artifact。成功返回 `200` 和列表信封。

**说明**Artifact 需要目标工作空间已开通产物能力，并在 Turn 成功完成后才会产生。托管环境完成 Turn 后，如果工作空间未开通产物能力，列表返回空数组。本轮没有新增产物时，列表仍可能包含此前 Turn 的产物；可读取返回项的 `turn_id` 筛选本轮结果。

**说明**使用 `environment.type=none` 的 Session 没有关联环境，产物列表可能返回 `404`。需要托管环境完成 Turn 后再查询。

## 查询参数

**environment\_id** `string` **（可选）**

环境 ID，可选，按环境过滤

**limit** `integer` **（可选）**

每页数量，默认 20，范围 1–100

**order** `string` **（可选）**

排序方向，`asc` 或 `desc`，默认 `desc`

**after** `string` **（可选）**

上一页的 `last_id`

**before** `string` **（可选）**

反向分页游标，可选；与 `after` 不能同时使用

当前不提供按 `turn_id` 或 `path` 的服务端过滤。分页后由调用方自行筛选。

## 请求示例

curl

```
curl -sS --get "$BASE_URL/agents/sessions/sess_xxx/artifacts" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  --data-urlencode "environment_id=ccarenv_xxx" \
  --data-urlencode "limit=100" \
  --data-urlencode "order=desc"
```

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["BASE_URL"],
)

page = client.beta.agents.sessions.artifacts.list(
    "sess_xxx",
    environment_id="ccarenv_xxx",
    limit=100,
    order="desc",
)
for artifact in page.data:
    print(artifact.id, artifact.turn_id, artifact.path)
```

### 响应字段

**object** `string`

列表对象类型，固定为 `list`

**data** `array`

当前页的 Artifact 列表，可为空

**first\_id** `string / null`

当前页首项 ID。空页为 `null`

**last\_id** `string / null`

当前页末项 ID。空页为 `null`

**has\_more** `boolean`

当前方向是否还有下一页

`data` 项字段：

列表不返回底层存储标识、签名下载地址或凭据。

data 项

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

## 响应示例

```
{
  "object": "list",
  "data": [{
    "id": "artifact_xxx",
    "object": "agent.session.artifact",
    "session_id": "sess_xxx",
    "environment_id": "ccarenv_xxx",
    "turn_id": "turn_xxx",
    "path": "/workspace/outputs/report.txt",
    "size_bytes": 19,
    "created_at": 1793941200
  }],
  "first_id": "artifact_xxx",
  "last_id": "artifact_xxx",
  "has_more": false
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按查询参数说明修正 `limit`、`order`，并避免同时传冲突参数

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且可见的 Session ID

`404`

`not_found_error` / `not_found_error`

使用当前集合上一页返回的 `last_id` 作为游标

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。排查时保留 Session ID、Turn ID、环境 ID 和 `x-request-id`。
