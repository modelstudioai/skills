# 获取 Deployment Run

获取单个 Deployment Run 的详细信息。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/deployment_runs/{deployment_run_id}`

## 路径参数

**deployment\_run\_id** `string` **（必选）**

Deployment Run ID

## 请求示例

curl

```
curl "$AGENTSTUDIO_URL/deployment_runs/drun_xxx" \
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

—

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
  "session_id": "sesn_xxx",
  "trigger_source": "manual",
  "status": "succeeded",
  "error": null,
  "started_at": "2026-07-28T02:00:00Z",
  "finished_at": "2026-07-28T02:03:00Z",
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

`DEPLOYMENT_RUN_NOT_FOUND`

Deployment run not found.
