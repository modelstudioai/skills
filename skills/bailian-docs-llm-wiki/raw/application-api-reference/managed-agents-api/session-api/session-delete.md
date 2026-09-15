# 删除 Session

硬删除：会话元数据、事件历史、内部拷贝的资源一并清除，不可恢复。若需保留事件历史请改用归档接口。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**DELETE** `/sessions/{session_id}`

## 请求示例

bash

```
curl -X DELETE "$AGENTSTUDIO_URL/sessions/sesn_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

python

```
client.sessions.delete("sesn_xxx")
```

java

```
client.sessions().delete("sesn_xxx");
```

## 响应示例

```
{
  "id": "sesn_xxx",
  "type": "session_deleted",
  "request_id": "xxx"
}
```

### 响应字段

字段

类型

说明

`id`

string

被删除的会话 ID

`type`

string

固定为 `session_deleted`，标识删除成功

`request_id`

string

本次请求的唯一标识
