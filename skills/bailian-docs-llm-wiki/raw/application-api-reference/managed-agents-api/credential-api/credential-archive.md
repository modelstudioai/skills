# 归档 Credential

归档指定 Credential，归档后 Credential 不再注入会话，但仍可查询和恢复。响应中 archived\_at 字段已设置归档时间。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/vaults/{vault_id}/credentials/{credential_id}/archive`

## 路径参数

**vault\_id** `string` **（必选）**

Vault ID，格式 vlt\_xxx

**credential\_id** `string` **（必选）**

Credential ID，格式 cred\_xxx

## 请求示例

curl

```
curl -X POST "$AGENTSTUDIO_URL/vaults/vlt_xxx/credentials/cred_xxx/archive" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**id** `string`

Credential ID，格式 cred\_xxx

**type** `string`

固定为 credential

**vault\_id** `string`

所属 Vault ID

**display\_name** `string`

Credential 可读名称

**auth** `object`

认证信息，敏感值已脱敏

**metadata** `object`

业务自定义键值对

**archived\_at** `string`

归档时间，ISO 8601

**created\_at** `string`

创建时间，ISO 8601

**updated\_at** `string`

最近更新时间，ISO 8601

**request\_id** `string`

请求唯一标识

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
  "archived_at": "2026-07-15T06:00:00Z",
  "created_at": "2026-07-10T08:00:00Z",
  "updated_at": "2026-07-15T06:00:00Z",
  "request_id": "req_xxx"
}
```

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
