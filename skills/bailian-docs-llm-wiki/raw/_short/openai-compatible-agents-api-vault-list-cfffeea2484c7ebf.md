# 列出 Vault

分页列出工作空间中的 Vault，支持按元数据和归档状态筛选。

## 接口

**GET** `/vaults`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 查询参数

**limit** `integer` **（可选）**

每页数量，默认 20，范围 1–100。空字符串、0、负数、非数字或超出范围返回 `400`

**order** `string` **（可选）**

排序方向，`asc` 或 `desc`，默认 `desc`

**after** `string` **（可选）**

上一页的 `last_id`。从该项之后开始，不包含该项

**metadata\[key\]** `string` **（可选）**

元数据过滤条件，按 metadata 精确匹配，多个条件之间为 AND

**status** `string` **（可选）**

Vault 状态：`active` 或 `archived`，默认两者都包含。也支持重复传入 `status[]`，值会合并为筛选集合

`before` 不是支持参数。

## 请求示例

curl

```
curl -sS "$BASE_URL/vaults?limit=20&order=desc&status=active" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
import os
import requests

resp = requests.get(
    f"{os.environ['BASE_URL']}/vaults",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
    params={"limit": 20, "order": "desc", "status": "active"},
)
print(resp.json())
```

### 响应字段

`200`，返回列表信封：

**object** `string`

列表对象类型，固定为 `list`

**data** `array`

当前页的 Vault 数组

**first\_id** `string / null`

当前页首项 ID。空页为 `null`

**last\_id** `string / null`

当前页末项 ID，下一页的 `after` 使用该值。空页为 `null`

**has\_more** `boolean`

是否还有更多匹配资源

### Vault 字段

**id** `string`

Vault ID

**object** `string`

Vault 对象类型，固定为 `vault`

**created\_at** `integer`

创建时间，Unix 秒

**name** `string / null`

显示名称

**metadata** `object`

元数据，字符串键值对；未设置时为 `{}`

空页返回 `data: []`，`first_id` 和 `last_id` 为 `null`，`has_more` 为 `false`。

## 响应示例

```
{
  "object": "list",
  "data": [
    {
      "id": "vlt_xxx",
      "object": "vault",
      "created_at": 1793941200,
      "name": "production-secrets",
      "metadata": {"team": "support"}
    }
  ],
  "first_id": "vlt_xxx",
  "last_id": "vlt_xxx",
  "has_more": false
}
```

## 错误码

错误响应结构见[错误码](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按查询参数说明修正 `limit`、`order` 或 metadata 过滤条件

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前集合上一页返回的 `last_id` 作为 `after`

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
