# 删除 Vault

软删除指定 Vault，操作不可恢复。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**DELETE** `/vaults/{vault_id}`

## 路径参数

**参数**

**必填**

**类型**

**说明**

`vault_id`

是

string

Vault ID，格式 vlt\_xxx

## 请求示例

bash

```
curl -X DELETE "$AGENTSTUDIO_URL/vaults/vlt_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 响应

```
{
  "id": "vlt_xxx",
  "type": "vault_deleted"
}
```

### 响应字段

**字段**

**类型**

**说明**

`id`

string

已删除的 Vault ID

`type`

string

固定为 vault\_deleted

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
