# 禁用 Webhook

手动禁用 Webhook。请求体为空。禁用后不再投递新的事件，已产生但尚未投递的事件会被取消。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/webhook_endpoints/{id}/disable`

## 路径参数

**id** `string` **（必选）**

Webhook ID，格式 wep\_<ULID>

## 请求示例

curl

```
curl -X POST "$AGENTSTUDIO_URL/webhook_endpoints/wep_01JXX7YQGPRPV1BZXA35QE7WDP/disable" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**id** `string`

—

**description** `string | null`

—

**url** `string`

—

**events** `array<string>`

—

**status** `string`

禁用后为 DISABLED

**disabled\_reason** `string | null`

手动禁用为 MANUAL

**consecutive\_fail** `integer`

返回禁用完成时的当前值

**last\_success\_at** `string | null`

返回禁用完成时的当前值

**last\_failure\_at** `string | null`

返回禁用完成时的当前值

**created\_at** `string`

—

**updated\_at** `string`

—

**request\_id** `string`

本次请求的唯一标识，排查问题时附带

## 响应

```
{
  "id": "wep_01JXX7YQGPRPV1BZXA35QE7WDP",
  "description": "生产环境会话事件",
  "url": "https://example.com/managedagent/webhooks",
  "events": [
    "session.status_idled"
  ],
  "status": "DISABLED",
  "disabled_reason": "MANUAL",
  "consecutive_fail": 2,
  "last_success_at": "2026-08-06T10:05:00Z",
  "last_failure_at": "2026-08-06T10:10:00Z",
  "created_at": "2026-08-06T10:00:00Z",
  "updated_at": "2026-08-06T10:25:00Z",
  "request_id": "8e1d16e4"
}
```

## 错误码

**状态码**

**错误码**

**说明**

404

`11800001`

webhook not found
