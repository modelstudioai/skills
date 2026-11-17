# 更新 Credential

轮换 Credential 的密钥或更新元数据，不支持修改名称和网络配置。

## 接口

**POST** `/vaults/{vault_id}/credentials/{credential_id}`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 路径参数

**vault\_id** `string` **（必选）**

父 Vault ID，按不透明 ID 使用

**credential\_id** `string` **（必选）**

Credential ID，按不透明 ID 使用

## 请求体

**metadata** `object` **（可选）**

元数据，省略时保持原值；`null` 返回 `400`；`{}` 清空。最多 16 项；key 1–64 字符，value 最多 512 字符

**auth** `object` **（可选）**

认证信息；省略时只更新 metadata；`null` 返回 `400`

属性

**type** `string` **（条件必填）**

认证类型，固定为 `environment_variable`

**secret\_value** `string` **（条件必填）**

新密钥值，不能为空或纯空白；长度和控制字符限制同创建

`metadata` 和 `auth` 至少传一项。同时省略两者或传入 `{}`，返回 `400`。更新只支持修改 `metadata` 和轮换 `secret_value`；不支持修改 `name`、`secret_name` 或 `networking`，传入这些字段会返回 `400 unknown_parameter`。

`metadata` 整体替换，不合并。轮换保留原环境变量名和网络配置；响应不返回 `secret_value`、密钥标识或 `injection_location`。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/vaults/vlt_xxx/credentials/vcrd_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {"rotation": "2026-11"},
    "auth": {
      "type": "environment_variable",
      "secret_value": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }'
```

Python

```
import os
import requests

resp = requests.post(
    f"{os.environ['BASE_URL']}/vaults/vlt_xxx/credentials/vcrd_xxx",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
    json={
        "metadata": {"rotation": "2026-11"},
        "auth": {
            "type": "environment_variable",
            "secret_value": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        },
    },
)
print(resp.status_code, resp.json())
```

### 响应字段

`200`，返回更新后的 Credential：

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
  "updated_at": 1793944800,
  "metadata": {"rotation": "2026-11"},
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

`400`

`invalid_request_error` / `unknown_parameter`

请求包含未知字段，例如 `name`、`secret_name` 或 `networking`

`400`

`invalid_request_error` / `invalid_type`

按字段说明修正类型

`400`

`invalid_request_error` / `invalid_request_error`

请求体为空、`auth.type` 不合法、`secret_value` 为空白，或 `metadata` 为 `null`

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

Credential 不存在、已删除、父归属不符或不属于当前工作空间

`409`

`conflict_error` / `conflict_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
