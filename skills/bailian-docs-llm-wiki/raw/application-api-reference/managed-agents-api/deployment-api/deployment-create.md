# 创建 Deployment

创建一个新的部署，绑定 Agent 并配置触发方式。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/deployments`

## 请求体

**name** `string` **（必选）**

Deployment 名称，最长 256 字符

**description** `string` **（可选）**

部署用途描述

**agent** `object` **（必选）**

关联的 Agent

**environment\_id** `string` **（可选）**

关联的 Environment ID

**schedule** `object` **（可选）**

定时触发配置；不传则为手动触发

**initial\_events** `array<object>` **（必选）**

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
curl -X POST "$AGENTSTUDIO_URL/deployments" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "每日订单汇总",
    "agent": {
      "id": "agent_xxx",
      "version": 12
    },
    "environment_id": "env_xxx",
    "schedule": {
      "type": "cron",
      "expression": "0 9 * * 1-5",
      "timezone": "Asia/Shanghai"
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
    ]
  }'
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
