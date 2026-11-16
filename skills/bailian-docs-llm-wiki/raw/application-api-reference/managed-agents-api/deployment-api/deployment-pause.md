# 暂停 Deployment

暂停指定 Deployment，停止定时触发。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/deployments/{deployment_id}/pause`

## 路径参数

**deployment\_id** `string` **（必选）**

Deployment ID

## 请求示例

curl

```
curl -X POST "$AGENTSTUDIO_URL/deployments/depl_xxx/pause" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**id** `string`

Deployment ID

**type** `string`

固定为 `deployment`

**name** `string`

Deployment 名称

**description** `string`

Deployment 用途说明

**agent** `object`

关联 Agent 在锁定版本的快照

**environment\_id** `string`

关联 Environment ID

**schedule** `object`

定时触发配置。暂停后 `next_run_at` 为 `null`

**initial\_events** `array<object>`

触发时发送给 Agent 的初始事件

**resources** `array<object>`

挂载的文件资源

**vault\_ids** `array<string>`

关联 Vault ID 列表

**metadata** `object`

业务自定义键值对

**status** `string`

此操作后固定为 `paused`

**paused\_reason** `object`

暂停原因

**archived\_at** `string | null`

归档时间，未归档时为 `null`

**created\_at** `string`

创建时间，ISO 8601

**updated\_at** `string`

最近更新时间，ISO 8601

**request\_id** `string`

请求唯一标识

## 响应

```
{
  "id": "depl_xxx",
  "type": "deployment",
  "name": "每日订单汇总",
  "status": "paused",
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
    "next_run_at": null
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
  "paused_reason": {
    "type": "manual"
  },
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

Cannot pause an archived deployment.
