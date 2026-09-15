# 列出 Vault

分页列出工作空间下的 Vault，默认不包含已归档项。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/vaults`

## Query 参数

**参数**

**必填**

**类型**

**说明**

`include_archived`

否

boolean

是否包含已归档 Vault，默认 false

`limit`

否

integer

每页返回数量，默认 20，最大 100

`page`

否

string

分页游标，取自上一页响应的 next\_page 值

## 请求示例

bash

```
curl "$AGENTSTUDIO_URL/vaults?include_archived=true&limit=20" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 响应

响应包含 `data`（密钥库对象数组）与 `next_page`（下一页游标，无更多数据时为 `null`）。

```
{
  "data": [
    {
      "id": "vlt_xxx",
      "type": "vault",
      "display_name": "生产环境密钥箱",
      "metadata": {
        "environment": "production"
      },
      "archived_at": null,
      "created_at": "2026-06-20T10:00:00Z",
      "updated_at": "2026-06-20T10:00:00Z"
    }
  ],
  "next_page": null
}
```

### 响应字段

**字段**

**类型**

**说明**

`data`

array<object>

Vault 对象数组

`data[].id`

string

Vault ID，格式 `vlt_xxx`

`data[].type`

string

固定为 `vault`

`data[].display_name`

string

Vault 可读名称

`data[].metadata`

object

业务自定义键值对

`data[].archived_at`

string | null

归档时间，未归档时为 null

`data[].created_at`

string

创建时间，ISO 8601

`data[].updated_at`

string

最近更新时间，ISO 8601

`next_page`

string | null

下一页游标；无更多数据时为 null

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
