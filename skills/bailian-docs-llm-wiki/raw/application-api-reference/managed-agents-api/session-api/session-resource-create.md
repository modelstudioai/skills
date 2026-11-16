# 运行时挂载资源

在会话运行期间动态挂载一个文件。服务端会将文件复制一份内部副本，并把挂载路径加上 /mnt/session/uploads/ 前缀。此操作不产生会话事件。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/sessions/{session_id}/resources`

## 路径参数

**session\_id** `string` **（必选）**

会话 ID，格式 sesn\_<ULID>

## 请求体

**type**`string`**（必选）**

资源类型，固定为 file

**file\_id**`string`**（必选）**

已上传的文件 ID

**mount\_path**`string`**（必选）**

挂载路径，以 /uploads 开头

## 请求示例

curl

```
curl -X POST "$AGENTSTUDIO_URL/sessions/sesn_xxx/resources" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "file",
    "file_id": "file_xxx",
    "mount_path": "/uploads/workspace/late.csv"
  }'
```

### 响应字段

**id**`string`

资源 ID，格式 sesrsc\_<ULID>

**type**`string`

资源类型，固定为 file

**file\_id**`string`

内部副本的文件 ID，与请求中的 file\_id 不同

**mount\_path**`string`

会话内的完整挂载路径

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
  "mount_path": "/mnt/session/uploads/workspace/late.csv",
  "created_at": "2026-05-28T08:25:00Z",
  "updated_at": "2026-05-28T08:25:00Z",
  "request_id": "xxx"
}
```

## 错误码

**状态码**

**错误码**

**说明**
