# 删除 Environment

硬删除：环境配置一并清除，不可恢复。若需保留配置请改用归档接口。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**DELETE** `/environments/{environment_id}`

## 请求示例

bash

```
curl -X DELETE "$AGENTSTUDIO_URL/environments/env_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

python

```
client.environments.delete("env_xxx")
```

java

```
client.environments().delete("env_xxx");
```

## 响应示例

```
{
  "id": "env_xxx",
  "type": "environment_deleted",
  "request_id": "xxx"
}
```

### 响应字段

字段

类型

说明

`id`

string

被删除的环境 ID

`type`

string

固定为 `environment_deleted`

`request_id`

string

本次请求的唯一标识
