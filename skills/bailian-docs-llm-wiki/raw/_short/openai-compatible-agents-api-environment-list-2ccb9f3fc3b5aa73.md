# 列出 Environment

分页列出当前工作空间的托管环境，按指定顺序返回。

## 接口

**GET** `/agents/environments`

分页列出当前工作空间的托管环境。成功返回 `200` 和列表信封。

## 查询参数

**limit** `integer` **（可选）**

每页数量，默认 20，范围 1–100

**order** `string` **（可选）**

排序方向，`asc` 或 `desc`，默认 `desc`

**after** `string` **（可选）**

上一页的 `last_id`；结果不包含游标项

**type** `string` **（可选）**

环境类型；`openai_hosted` 或 `bailian_hosted`，当前只校验取值，不按类型过滤，不要依赖它区分托管环境

`before` 当前返回 `400`。

## 请求示例

curl

```
curl -sS --get "$BASE_URL/agents/environments" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  --data-urlencode "limit=20" \
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

page = client.beta.agents.environments.list(limit=20, order="desc")
while True:
    for environment in page.data:
        print(environment.id, environment.status)
    if not page.has_more:
        break
    page = page.get_next_page()
```

### 响应字段

**object** `string`

列表对象类型，固定为 `list`

**data** `array`

当前页的环境列表，可为空

**first\_id** `string / null`

当前页首项 ID。空页为 `null`

**last\_id** `string / null`

当前页末项 ID。空页为 `null`

**has\_more** `boolean`

当前方向是否还有下一页

空列表返回：

## 响应示例

```
{
  "object": "list",
  "data": [{
    "id": "ccarenv_xxx",
    "object": "agent.environment",
    "type": "openai_hosted",
    "status": "ready",
    "files": [],
    "skills": [],
    "plugins": []
  }],
  "first_id": "ccarenv_xxx",
  "last_id": "ccarenv_xxx",
  "has_more": false
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按查询参数说明修正 `limit`、`order`，并移除 `before`

`401`

`invalid_request_error` / `workspace_required` 或 `user_required`

使用当前工作空间的 API Key

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。
