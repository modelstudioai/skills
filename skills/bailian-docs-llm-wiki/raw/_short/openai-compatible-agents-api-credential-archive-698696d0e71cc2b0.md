# 归档 Credential

归档指定 Credential。该接口是百炼扩展，没有恢复接口。

## 接口

**POST** `/vaults/{vault_id}/credentials/{credential_id}/archive`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 路径参数

**vault\_id** `string` **（必选）**

父 Vault ID，按不透明 ID 使用

**credential\_id** `string` **（必选）**

Credential ID，按不透明 ID 使用

本接口没有请求体。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/vaults/vlt_xxx/credentials/vcrd_xxx/archive" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
import os
import requests

resp = requests.post(
    f"{os.environ['BASE_URL']}/vaults/vlt_xxx/credentials/vcrd_xxx/archive",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
)
print(resp.json())
```

### 响应字段

`200`，返回归档后的 Credential：

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

auth

**type** `string`

认证类型，固定为 `environment_variable`

**secret\_name** `string`

环境变量名

networking

**type** `string`

网络访问类型，`limited` 或 `unrestricted`

**allowed\_hosts** `array`

允许的目标域名或 IPv4，仅 `limited` 时返回

响应不返回 `archived_at`、`status`、`secret_value`、密钥标识或 `injection_location`。归档后 Credential 仍可获取，默认列表同时包含 `active` 和 `archived`。没有恢复接口。归档 Vault 会级联归档其下 Credential。

## 响应示例

```
{
  "id": "vcrd_xxx",
  "object": "vault.credential",
  "vault_id": "vlt_xxx",
  "name": "crm-token",
  "created_at": 1793941200,
  "updated_at": 1793944800,
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
