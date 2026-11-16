# 查询 Webhook 列表

返回当前 Workspace 下全部未删除的 Webhook。接口不分页。列表不返回 Signing Secret。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/webhook_endpoints`

## 请求示例

curl

```
curl "$AGENTSTUDIO_URL/webhook_endpoints" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**data** `array<object>`

Webhook 对象数组

**data\[\].id** `string`

Webhook ID

**data\[\].description** `string | null`

描述

**data\[\].url** `string`

回调 URL

**data\[\].events** `array<string>`

订阅的命名事件类型

**data\[\].status** `string`

Webhook 状态：`ACTIVE` 或 `DISABLED`

**data\[\].disabled\_reason** `string | null`

禁用原因；未禁用时为 `null`

**data\[\].consecutive\_fail** `integer`

当前连续失败次数

**data\[\].last\_success\_at** `string | null`

最近成功投递时间

**data\[\].last\_failure\_at** `string | null`

最近失败投递时间

**data\[\].created\_at** `string`

创建时间，ISO 8601

**data\[\].updated\_at** `string`

最近更新时间，ISO 8601

**request\_id** `string`

请求唯一标识

## 响应

```
{
  "data": [
    {
      "id": "wep_01JXX7YQGPRPV1BZXA35QE7WDP",
      "description": "生产环境会话事件",
      "url": "https://example.com/managedagent/webhooks",
      "events": [
        "session.updated",
        "session.status_idled",
        "session.thread_terminated"
      ],
      "status": "ACTIVE",
      "disabled_reason": null,
      "consecutive_fail": 2,
      "last_success_at": "2026-08-06T10:05:00Z",
      "last_failure_at": "2026-08-06T10:10:00Z",
      "created_at": "2026-08-06T10:00:00Z",
      "updated_at": "2026-08-06T10:00:00Z"
    }
  ],
  "request_id": "8e1d16e4"
}
```

## 错误码

**状态码**

**错误码**

**说明**

401

`InvalidApiKey`

Invalid API-key provided.
