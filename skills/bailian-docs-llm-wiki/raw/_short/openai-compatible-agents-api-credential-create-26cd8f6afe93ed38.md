# 创建 Credential

在指定 Vault 中创建 Credential，仅支持 environment\_variable 类型。

## 接口

**POST** `/vaults/{vault_id}/credentials`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 路径参数

**vault\_id** `string` **（必选）**

父 Vault ID，按不透明 ID 使用

## 请求体

**name** `string` **（必选）**

显示名称，不是环境变量名。去除首尾空白后 1–256 字节

**metadata** `object` **（可选）**

元数据，字符串键值对，最多 16 项；key 1–64 字符，value 最多 512 字符。传 `null` 返回 `400`

**auth** `object` **（必选）**

认证信息。缺失或为 `null` 返回 `400`

属性

**type** `string` **（必选）**

认证类型，固定为 `environment_variable`

**secret\_name** `string` **（必选）**

注入到环境的环境变量名。必须以字母开头，只能包含字母、数字和下划线，不能以保留前缀开头

**secret\_value** `string` **（必选）**

密钥值，1–1048576 字符，不能包含换行或 NUL。只写不回传

**networking** `object` **（必选）**

目标域名配置。缺失或为 `null` 返回 `400`

属性

**type** `string` **（必选）**

网络访问类型，`limited` 或 `unrestricted`

**allowed\_hosts** `array` **（条件必填）**

允许使用该凭据的目标域名或 IPv4，1–16 个。除特殊值 `*` 外，每项为精确域名或 IPv4，不支持协议、端口、路径和 IPv6，也不支持 `*.example.com` 等通配符；数组中包含 `*` 时对全部目标主机生效。除特殊值 `*` 外，域名至少包含两个标签，每个标签最多 63 字符，总长度不超过 253 字符；转小写后不能重复

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/vaults/vlt_xxx/credentials" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "crm-token",
    "metadata": {"team": "support"},
    "auth": {
      "type": "environment_variable",
      "secret_name": "CRM_TOKEN",
      "secret_value": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "networking": {
        "type": "limited",
        "allowed_hosts": ["api.example.com"]
      }
    }
  }'
```

Python

```
import os
import requests

resp = requests.post(
    f"{os.environ['BASE_URL']}/vaults/vlt_xxx/credentials",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
    json={
        "name": "crm-token",
        "metadata": {"team": "support"},
        "auth": {
            "type": "environment_variable",
            "secret_name": "CRM_TOKEN",
            "secret_value": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "networking": {
                "type": "limited",
                "allowed_hosts": ["api.example.com"],
            },
        },
    },
)
print(resp.status_code, resp.json())
```

`auth.injection_location` 不是公开输入，传入会返回 `400`。

**说明**`unrestricted` 凭据不单独指定目标域名列表；挂载到 Agents API 环境时，环境必须配置 `network.access="restricted"`，并提供非空、合法的 `allowed_domains`。`limited` 且 `allowed_hosts` 包含 `*` 时，凭据对发往全部目标主机的出网请求生效；出于安全考虑，建议在[创建 Environment](raw/_short/openai-compatible-agents-api-environment-create-aa976bec02220caa.md)时，将 `network.access` 设为 `restricted`，并配置非空的 `allowed_domains`。

### 响应字段

`201`，返回 Credential： 响应不返回 `secret_value`、密钥标识或 `injection_location`。

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

`400`

`invalid_request_error` / `unknown_parameter`

请求包含未知字段，例如 `auth.injection_location`

`400`

`invalid_request_error` / `invalid_type`

按字段说明修正类型

`400`

`invalid_request_error` / `invalid_request_error`

`name`、`metadata`、`auth` 或主机配置不符合要求

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

父 Vault 不存在、已删除或不属于当前工作空间

`409`

`conflict_error` / `conflict_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
