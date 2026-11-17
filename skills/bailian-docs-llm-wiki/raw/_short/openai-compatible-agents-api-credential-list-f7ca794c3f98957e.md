# 列出 Credential

分页列出指定 Vault 下的 Credential，支持元数据和归档状态筛选。

## 接口

**GET** `/vaults/{vault_id}/credentials`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 路径参数

**vault\_id** `string` **（必选）**

父 Vault ID，按不透明 ID 使用

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

Credential 状态：`active` 或 `archived`，默认两者都包含。也支持重复传入 `status[]`，值会合并为筛选集合

`before` 不是支持参数。Credential 只会列出路径 Vault 下的资源，`after` 游标必须属于同一个 Vault。

## 请求示例

curl

```
curl -sS "$BASE_URL/vaults/vlt_xxx/credentials?limit=20&order=desc&status=active" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
import os
import requests

resp = requests.get(
    f"{os.environ['BASE_URL']}/vaults/vlt_xxx/credentials",
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

当前页的 Credential 数组

**first\_id** `string / null`

当前页首项 ID。空页为 `null`

**last\_id** `string / null`

当前页末项 ID，下一页的 `after` 使用该值。空页为 `null`

**has\_more** `boolean`

是否还有更多匹配资源

### Credential 字段

**id** `string`

Credential ID

**object** `string`

Credential 对象类型，固定为 `vault.credential`

**vault\_id** `string`

所属 Vault ID

**name** `string`

显示名称

**created\_at** `integer`

创建时间，Unix 秒

**updated\_at** `integer`

最近更新时间，Unix 秒

**metadata** `object`

元数据，字符串键值对；未设置时为 `{}`

**auth** `object`

认证配置。

属性

**type** `string`

认证类型，固定为 `environment_variable`

**secret\_name** `string`

环境变量名

**networking** `object`

目标域名配置。

属性

**type** `string`

网络访问类型，`limited` 或 `unrestricted`

**allowed\_hosts** `array`

允许的目标域名或 IPv4，仅 `limited` 时返回

响应不返回 `secret_value`、密钥标识或 `injection_location`。空页返回 `data: []`，`first_id` 和 `last_id` 为 `null`，`has_more` 为 `false`。

## 响应示例

```
{
  "object": "list",
  "data": [
    {
      "id": "vcrd_xxx",
      "object": "vault.credential",
      "vault_id": "vlt_xxx",
      "name": "crm-token",
      "created_at": 1793941200,
      "updated_at": 1793941200,
      "metadata": {"team": "support"},
      "auth": {
        "type": "environment_variable",
        "secret_name": "CRM_TOKEN",
        "networking": {
          "type": "limited",
          "allowed_hosts": ["api.example.com"]
        }
      }
    }
  ],
  "first_id": "vcrd_xxx",
  "last_id": "vcrd_xxx",
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

父 Vault 不存在，或 `after` 游标不存在、已删除、跨父 Vault

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
