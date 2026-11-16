# 删除 Credential

永久删除指定 Credential，删除后不可恢复。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**DELETE** `/vaults/{vault_id}/credentials/{credential_id}`

## 路径参数

**vault\_id** `string` **（必选）**

Vault ID，格式 vlt\_xxx

**credential\_id** `string` **（必选）**

Credential ID，格式 cred\_xxx

## 请求示例

curl

```
curl -X DELETE "$AGENTSTUDIO_URL/vaults/vlt_xxx/credentials/cred_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**id** `string`

已删除的 Credential ID

**type** `string`

固定为 credential\_deleted

**request\_id** `string`

请求唯一标识

## 响应

```
{
  "id": "cred_xxx",
  "type": "credential_deleted",
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
