# 获取 Credential

获取 Credential 的认证配置和元数据，不返回 secret\_value。

## 接口

**GET** `/vaults/{vault_id}/credentials/{credential_id}`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 路径参数

**vault\_id** `string` **（必选）**

父 Vault ID，按不透明 ID 使用

**credential\_id** `string` **（必选）**

Credential ID，按不透明 ID 使用

## 请求示例

curl

```
curl -sS "$BASE_URL/vaults/vlt_xxx/credentials/vcrd_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
import os
import requests

resp = requests.get(
    f"{os.environ['BASE_URL']}/vaults/vlt_xxx/credentials/vcrd_xxx",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
)
print(resp.json())
```

### 响应字段

`200`，返回 Credential： 响应不返回 `secret_value`、密钥标识或 `injection_location`。已归档的 Credential 仍可获取。

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

## 响应示例

```
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
```

## 错误码

错误响应结构见[错误码](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

HTTP 状态码

错误类型 / 错误码

解决方案

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

Credential 不存在、已删除、父归属不符或不属于当前工作空间

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
