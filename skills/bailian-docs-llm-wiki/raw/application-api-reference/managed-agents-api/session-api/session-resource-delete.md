# 卸载会话资源

从会话中卸载指定资源，同时清除其内部副本。此操作不可恢复。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**DELETE** `/sessions/{session_id}/resources/{resource_id}`

## 路径参数

**参数**

**必填**

**类型**

**说明**

`session_id`

是

string

会话 ID，格式 sesn\_<ULID>

`resource_id`

是

string

资源 ID，格式 sesrsc\_<ULID>

## 请求示例

bash

```
curl -X DELETE "$AGENTSTUDIO_URL/sessions/sesn_xxx/resources/sesrsc_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 响应

```
{
  "id": "sesrsc_xxx",
  "type": "session_resource_deleted",
  "request_id": "xxx"
}
```

### 响应字段

**字段**

**类型**

**说明**

`id`

string

被卸载的资源 ID

`type`

string

固定为 session\_resource\_deleted，标识卸载成功

`request_id`

string

本次请求的唯一标识

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
