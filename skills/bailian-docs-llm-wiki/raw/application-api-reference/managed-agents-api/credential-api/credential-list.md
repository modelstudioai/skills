# 列出 Credential

分页列出指定 Vault 下的所有 Credential。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/vaults/{vault_id}/credentials`

## 路径参数

**vault\_id** `string` **（必选）**

Vault ID，格式 vlt\_xxx

## Query 参数

**include\_archived** `boolean` **（可选）**

是否包含已归档的 Credential，默认 false

**limit** `integer` **（可选）**

每页返回数量，默认 20，最大 100

**page** `string` **（可选）**

分页游标，从上一次响应的 next\_page 获取

## 请求示例

curl

```
curl "$AGENTSTUDIO_URL/vaults/vlt_xxx/credentials?include_archived=true&limit=20" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**data** `array<object>`

Credential 对象数组

**data\[\].id** `string`

Credential ID，格式 cred\_xxx

**data\[\].type** `string`

固定为 credential

**data\[\].vault\_id** `string`

所属 Vault ID

**data\[\].display\_name** `string`

Credential 可读名称

**data\[\].auth** `object`

认证信息，敏感值已脱敏

**data\[\].metadata** `object`

业务自定义键值对

**data\[\].archived\_at** `string | null`

归档时间，未归档时为 null

**data\[\].created\_at** `string`

创建时间，ISO 8601

**data\[\].updated\_at** `string`

最近更新时间，ISO 8601

**data\[\].request\_id** `string`

请求唯一标识

**next\_page** `string | null`

下一页游标，无更多数据时为 null

## 响应

响应包含 `data`（密钥对象数组）与 `next_page`（下一页游标，无更多数据时为 `null`）。

```
{
  "data": [
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
  ],
  "next_page": null
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
