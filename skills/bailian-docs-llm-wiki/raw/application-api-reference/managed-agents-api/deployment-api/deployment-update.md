# 更新 Deployment

更新指定 Deployment 的配置信息。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/deployments/{deployment_id}`

## 路径参数

**deployment\_id** `string` **（必选）**

Deployment ID

## 请求体

**name** `string` **（可选）**

Deployment 名称，最长 256 字符

**description** `string` **（可选）**

部署用途描述

**agent** `object` **（可选）**

关联的 Agent

**environment\_id** `string | null` **（可选）**

关联的 Environment ID

**schedule** `object | null` **（可选）**

定时触发配置；传 null 则清除定时触发

**initial\_events** `array<object>` **（可选）**

触发时发送给 Agent 的初始事件列表，1-50 项

**resources** `array<object>` **（可选）**

挂载文件资源列表

**vault\_ids** `array<string>` **（可选）**

关联的 Vault ID 列表

**metadata** `object` **（可选）**

业务自定义键值对

## 请求示例

curl

```
curl -X POST "$AGENTSTUDIO_URL/deployments/depl_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "每日订单汇总-v2",
    "schedule": null
  }'
```

### 响应字段

**id** `string`

—

**type** `string`

—

**name** `string`

—

**description** `string`

—

**agent** `object`

—

**environment\_id** `string`

—

**schedule** `object | null`

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
  "name": "每日订单汇总-v2",
  "status": "active",
  "agent": {
    "id": "agent_xxx",
    "version": 12
  },
  "environment_id": "env_xxx",
  "schedule": null,
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

409

`DEPLOYMENT_STATE_CONFLICT`

Cannot update an archived deployment.
