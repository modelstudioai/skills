# 更新 Session

修改会话的 title、metadata 与 environment\_variables。会话更新是唯一会触发 session.updated 事件的操作。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/sessions/{session_id}`

支持修改 `title`、`metadata` 与 `environment_variables`。**会话更新是唯一会触发**`session.updated`**事件的操作**。

## 请求体

字段

必填

类型

说明

`title`

否

string

会话标题

`metadata`

否

object

业务自定义键值

`environment_variables`

否

object

会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取

## 请求示例

bash

```
curl -X POST "$AGENTSTUDIO_URL/sessions/sesn_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q3 销售复盘（已归档）",
    "metadata": {"biz_ticket_id": "1234", "status": "done"},
    "environment_variables": {"API_BASE_URL": "https://api.example.com", "LOG_LEVEL": "info"}
  }'
```

python

```
session = client.sessions.update(
    "sesn_xxx",
    title="Q3 销售复盘（已归档）",
    metadata={"biz_ticket_id": "1234", "status": "done"},
    environment_variables={"API_BASE_URL": "https://api.example.com", "LOG_LEVEL": "info"},
)
```

java

```
Map<String, String> metadata = new HashMap<>();
metadata.put("biz_ticket_id", "1234");
metadata.put("status", "done");

Map<String, String> environmentVariables = new HashMap<>();
environmentVariables.put("API_BASE_URL", "https://api.example.com");
environmentVariables.put("LOG_LEVEL", "info");

Session updated = client.sessions().update("sesn_xxx",
    SessionUpdateParam.builder()
        .title("Q3 销售复盘（已归档）")
        .metadata(metadata)
        .environmentVariables(environmentVariables)
        .build());
```

## 响应示例

仅返回更新后的字段、`updated_at` 与 `request_id`。

```
{
  "id": "sesn_xxx",
  "type": "session",
  "status": "idle",
  "title": "Q3 销售复盘（已归档）",
  "metadata": {"biz_ticket_id": "1234", "status": "done"},
  "updated_at": "2026-05-28T09:30:00Z",
  "request_id": "xxx",
  "environment_variables": {"API_BASE_URL": "https://api.example.com", "LOG_LEVEL": "info"}
}
```

### 响应字段

字段

类型

说明

`id`

string

会话 ID

`type`

string

固定为 `session`

`status`

string

当前会话状态（更新不改变状态）

`title` / `metadata`

string / object

请求体覆盖后的新值

`updated_at`

string

最近更新时间，ISO 8601

`request_id`

string

本次请求的唯一标识

`environment_variables`

object

会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取
