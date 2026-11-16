# 恢复 Deployment

将已暂停的 Deployment 恢复为活跃状态。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/deployments/{deployment_id}/unpause`

## 路径参数

**deployment\_id** `string` **（必选）**

Deployment ID

## 请求示例

curl

```
curl -X POST "$AGENTSTUDIO_URL/deployments/depl_xxx/unpause" \
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

Deployment 描述

**agent** `object`

—

**environment\_id** `string`

—

**schedule** `object`

定时触发配置

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

**paused\_reason** `string | null`

—

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
  "name": "Daily Report Generator",
  "description": "Generates daily sales reports",
  "agent": {
    "id": "agent_xxx",
    "version": 13
  },
  "environment_id": "env_xxx",
  "schedule": {
    "cron": "0 9 * * *"
  },
  "initial_events": [],
  "resources": [],
  "vault_ids": [],
  "metadata": {},
  "status": "active",
  "paused_reason": null,
  "archived_at": null,
  "created_at": "2026-07-20T10:00:00Z",
  "updated_at": "2026-07-28T02:00:00Z",
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

409

`DEPLOYMENT_STATE_CONFLICT`

Cannot unpause an archived deployment.
