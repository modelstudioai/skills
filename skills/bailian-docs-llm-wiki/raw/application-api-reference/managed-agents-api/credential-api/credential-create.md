# 创建 Credential

在指定 Vault 中创建一个 Credential。auth 当前仅支持 environment\_variable 类型。secret\_value 等敏感值仅写入时传入，响应中不返回。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/vaults/{vault_id}/credentials`

## 请求体

**字段**

**必填**

**类型**

**说明**

`auth`

是

object

认证信息，固定为 environment\_variable 类型。

`display_name`

否

string

Credential 可读名称，最大 255 字符

`metadata`

否

object

业务自定义键值对元数据

### auth 类型

`auth` 当前仅支持 `environment_variable` 一种类型，以环境变量形式注入会话。

**字段**

**必填**

**类型**

**说明**

`type`

是

string

固定为 environment\_variable

`secret_name`

是

string

环境变量名称，创建后不可修改

`secret_value`

是

string

环境变量值，仅写入时传入，响应中不返回

`networking`

是

object

网络策略，限制只有发往指定域名的请求才会被替换为真实密钥

`networking.allowed_hosts`

是

array

允许替换真实密钥的域名列表，支持 `*.example.com` 通配子域，最多 10 个。填 `*` 对全部域名生效

`injection_location`

是

object

替换位置，标识密钥写入请求的位置。当前仅支持 Authorization 请求头，写入请求体暂不支持

`injection_location.header`

否

boolean

是否写入 Authorization 请求头（Bearer 格式）

## 请求示例

bash

```
curl -X POST "$AGENTSTUDIO_URL/vaults/vlt_xxx/credentials" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "第三方 API 密钥",
    "auth": {
      "type": "environment_variable",
      "secret_name": "API_KEY",
      "secret_value": "sk-xxxx",
      "networking": {
        "allowed_hosts": [
          "api.example.com",
          "*.example.com"
        ]
      },
      "injection_location": {
        "header": true
      }
    }
  }'
```

## 响应

```
{
  "id": "cred_xxx",
  "type": "credential",
  "vault_id": "vlt_xxx",
  "display_name": "第三方 API 密钥",
  "auth": {
    "type": "environment_variable",
    "secret_name": "API_KEY",
    "networking": {
      "allowed_hosts": [
        "api.example.com",
        "*.example.com"
      ]
    },
    "injection_location": {
      "header": true
    }
  },
  "metadata": {},
  "archived_at": null,
  "created_at": "2026-07-10T08:00:00Z",
  "updated_at": "2026-07-10T08:00:00Z",
  "request_id": "req_xxx"
}
```

### 响应字段

**字段**

**类型**

**说明**

`id`

string

Credential ID，格式 cred\_xxx

`type`

string

固定为 credential

`vault_id`

string

所属 Vault ID

`display_name`

string

Credential 可读名称

`auth`

object

认证信息，敏感值已脱敏（如 secret\_value 不返回）

`auth.type`

string

认证类型，当前仅支持 environment\_variable

`auth.secret_name`

string

环境变量名称

`auth.networking`

object

网络策略

`auth.networking.allowed_hosts`

array

允许替换真实密钥的域名列表

`auth.injection_location`

object

替换位置。当前仅支持 Authorization 请求头，写入请求体暂不支持

`auth.injection_location.header`

boolean

是否写入 Authorization 请求头

`metadata`

object

业务自定义键值对

`archived_at`

string | null

归档时间，未归档时为 null

`created_at`

string

创建时间，ISO 8601

`updated_at`

string

最近更新时间，ISO 8601

`request_id`

string

请求唯一标识

## 错误码

**状态码**

**错误码**

**说明**

400

`InvalidParameter`

Required parameter missing or invalid.

401

`InvalidApiKey`

Invalid API-key provided.
