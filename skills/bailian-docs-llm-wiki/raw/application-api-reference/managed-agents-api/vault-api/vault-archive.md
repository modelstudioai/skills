# 归档 Vault

软归档指定 Vault。归档后默认不出现在列表中，已绑定会话仍可使用其 Credential。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/vaults/{vault_id}/archive`

## 路径参数

**vault\_id** `string` **（必选）**

Vault ID，格式 vlt\_xxx

## 请求示例

curl

```
curl -X POST "$AGENTSTUDIO_URL/vaults/vlt_xxx/archive" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**id** `string`

Vault ID，格式 vlt\_xxx

**type** `string`

固定为 vault

**display\_name** `string`

Vault 可读名称

**metadata** `object`

业务自定义键值对

**archived\_at** `string | null`

归档时间，已填入归档时间，ISO 8601

**created\_at** `string`

创建时间，ISO 8601

**updated\_at** `string`

最近更新时间，ISO 8601

## 响应

```
{
  "id": "vlt_xxx",
  "type": "vault",
  "display_name": "生产环境密钥箱",
  "metadata": {
    "environment": "production"
  },
  "archived_at": "2026-07-10T08:00:00Z",
  "created_at": "2026-06-20T10:00:00Z",
  "updated_at": "2026-07-10T08:00:00Z"
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
