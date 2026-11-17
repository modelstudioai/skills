# 列出 Environment template

分页列出当前工作空间的环境模板。

## 接口

**GET** `/agents/environments/templates`

成功返回 `200` 和列表信封。

## 查询参数

**limit** `integer` **（可选）**

每页数量，默认 20；建议使用 `1..100`

**order** `string` **（可选）**

排序方向，`asc` 或 `desc`，默认 `desc`

**after** `string` **（可选）**

上一页的 `last_id`；不包含游标项

**before** `string` **（可选）**

上一页的 `first_id`，用于反向翻页，不能与 `after` 同时使用

同时传 `after` 和 `before` 返回 `400`。游标无效或模板不存在时返回 `404`。

## 请求示例

curl

```
curl -sS "$BASE_URL/agents/environments/templates?limit=20&order=desc" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
page = client.beta.agents.environments.templates.list(limit=20, order="desc")
for template in page.data:
    print(template.id, template.name)
```

### 响应字段

**object** `string`

列表对象类型，固定为 `list`

**data** `array`

当页环境模板；空时为 `[]`

**first\_id** `string / null`

当页首项 ID。空页为 `null`

**last\_id** `string / null`

当页末项 ID。空页为 `null`。后续 `after` 使用该值

**has\_more** `boolean`

当前检索方向是否还有下一页

`data[]` 中每个环境模板包含 `id`、`object`、`name`、`created_at`、`updated_at`、`packages`、`network`、`desktop`、`capability_directories`、`skills`、`plugins`、`files`，字段含义与获取环境模板一致。

## 响应示例

```
{
  "object": "list",
  "data": [
    {
      "id": "envtmpl_xxx",
      "name": "example-template",
      "object": "agent.environment.template",
      "created_at": 1794452344,
      "updated_at": 1794452344,
      "packages": {"python": [], "system": [], "npm": []},
      "network": {"access": "disabled", "allowed_domains": []},
      "desktop": {"enabled": false},
      "capability_directories": ["/workspace/skills"],
      "skills": [],
      "plugins": [],
      "files": []
    }
  ],
  "first_id": "envtmpl_xxx",
  "last_id": "envtmpl_xxx",
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

使用当前集合中有效的游标

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
