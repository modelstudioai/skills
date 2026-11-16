# 触发 Deployment Run

手动触发一次 Deployment 执行。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/deployments/{deployment_id}/run`

## 路径参数

**deployment\_id** `string` **（必选）**

Deployment ID

## 请求示例

curl

```
curl -X POST "$AGENTSTUDIO_URL/deployments/depl_xxx/run" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**id** `string`

Deployment Run ID

**type** `string`

固定值 deployment\_run

**deployment\_id** `string`

—

**agent** `object`

—

**session\_id** `string | null`

异步 Session 创建完成前为 null

**trigger\_source** `string`

—

**status** `string`

—

**error** `object | null`

错误信息，仅运行失败时返回

**started\_at** `string`

ISO 8601 时间戳

**finished\_at** `string | null`

—

**request\_id** `string`

本次请求的唯一标识，排查问题时附带

## 响应

```
{
  "id": "drun_xxx",
  "type": "deployment_run",
  "deployment_id": "depl_xxx",
  "agent": {
    "id": "agent_xxx",
    "version": 13
  },
  "session_id": null,
  "trigger_source": "manual",
  "status": "running",
  "error": null,
  "started_at": "2026-07-28T02:00:00Z",
  "finished_at": null,
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

`DEPLOYMENT_TRIGGER_CONFLICT`

Concurrent trigger conflict.
