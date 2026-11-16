# 查询会话资源详情

查询会话中单个已挂载资源的详情。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/sessions/{session_id}/resources/{resource_id}`

## 路径参数

**session\_id**`string`**（必选）**

会话 ID，格式 sesn\_<ULID>

**resource\_id**`string`**（必选）**

资源 ID，格式 sesrsc\_<ULID>

## 请求示例

curl

```
curl "$AGENTSTUDIO_URL/sessions/sesn_xxx/resources/sesrsc_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**id**`string`

资源 ID，格式 sesrsc\_<ULID>

**type**`string`

资源类型，固定为 file

**file\_id**`string`

内部副本的文件 ID

**mount\_path**`string`

加上 /mnt/session/uploads/ 前缀后的完整挂载路径

**created\_at**`string`

创建时间，ISO 8601

**updated\_at**`string`

最近更新时间，ISO 8601

**request\_id**`string`

本次请求的唯一标识

## 响应

```
{
  "id": "sesrsc_xxx",
  "type": "file",
  "file_id": "file_xxx",
  "mount_path": "/mnt/session/uploads/data.csv",
  "created_at": "2026-05-28T08:23:11Z",
  "updated_at": "2026-05-28T08:23:11Z",
  "request_id": "xxx"
}
```

## 错误码

**状态码**

**错误码**

**说明**
