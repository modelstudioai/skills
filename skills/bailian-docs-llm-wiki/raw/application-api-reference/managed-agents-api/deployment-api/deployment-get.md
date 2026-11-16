# 获取 Deployment

根据 ID 获取单个 Deployment 的详细信息。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/deployments/{deployment_id}`

## 路径参数

**deployment\_id** `string` **（必选）**

Deployment ID

## 请求示例

curl

```
curl "$AGENTSTUDIO_URL/deployments/depl_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**id** `string`

Deployment ID

**type** `string`

固定值 deployment

**name** `string`

Deployment 名称

**description** `string`

部署用途描述

**agent** `object`

—

**environment\_id** `string`

—

**schedule** `object`

—

**initial\_events** `array<object>`

—

**resources** `array<object>`

—

**vault\_ids** `array<string>`

—

**metadata** `object`

—

**status** `string`

—

**paused\_reason** `object | null`

暂停原因，仅暂停状态时返回

**archived\_at** `string | null`

—

**created\_at** `string`

—

**updated\_at** `string`

—

**request\_id** `string`

本次请求的唯一标识，排查问题时附带

## 响应

```
{
  "id": "depl_xxx",
  "type": "deployment",
  "name": "每日订单汇总",
  "status": "active",
  "agent": {
    "id": "agent_xxx",
    "version": 12
  },
  "environment_id": "env_xxx",
  "schedule": {
    "type": "cron",
    "expression": "0 9 * * 1-5",
    "timezone": "Asia/Shanghai",
    "last_run_at": null,
    "next_run_at": "2026-07-28T01:00:00Z"
  },
  "initial_events": [
    {
      "type": "message",
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "汇总昨日订单数据"
        }
      ]
    }
  ],
  "resources": [],
  "vault_ids": [],
  "metadata": {},
  "paused_reason": null,
  "archived_at": null,
  "created_at": "2026-07-28T01:00:00Z",
  "updated_at": "2026-07-28T01:00:00Z",
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

404

`DEPLOYMENT_NOT_FOUND`

Deployment not found.
