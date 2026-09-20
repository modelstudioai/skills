# 删除 Agent

软删除 Agent，标记状态为 deleted，接口幂等。

## 前提

已获取阿里云百炼 API Key 与业务空间 ID，鉴权方式见[API 认证](raw/application-api-reference/rag-api/rag-api-authentication.md)。删除 Agent 需要知识库-删除权限，由[业务空间成员管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)中的角色决定，详见[权限要求](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

## 接口

**POST** `/api/v1/indices/rag/app/delete`

删除指定的 Agent。删除后 Agent 状态变为 `deleted`，无法再用于问答或检索。接口幂等：重复删除不会返回错误。

**警告**删除操作不可逆，删除后 Agent 无法恢复，关联的 `agent_id` 将无法用于 [`knowledge/search`](raw/application-api-reference/rag-api/knowledge/knowledgesearch.md) 和 [`knowledge/chat`](raw/application-api-reference/rag-api/knowledge/knowledgechat.md) 调用。

## 请求体

字段

必填

类型

说明

`agent_id`

是

string

Agent ID。

## 请求示例

```
curl -X POST "$BASE_URL/api/v1/indices/rag/app/delete" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "aid-8f3a1b2c4d5e6f70"
}'
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`（`{workspace_id}` 为业务空间 ID），`BAILIAN_API_KEY` 为阿里云百炼 API Key。

## 响应示例

操作成功返回 200。

```
{
  "request_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "status_code": 200,
  "code": "Success",
  "message": "",
  "status": "SUCCESS",
  "success": true,
  "data": {
    "agent_id": "aid-8f3a1b2c4d5e6f70",
    "agent_status": "deleted"
  }
}
```

## 响应字段

字段

类型

说明

`request_id`

string

请求唯一标识，排查问题时请提供此 ID。

`status_code`

integer

HTTP 状态码。

`code`

string

响应码，成功时为 `Success`。

`message`

string

提示信息。

`status`

string

请求状态：`SUCCESS` 或 `FAILED`。

`success`

boolean

请求是否成功。

`data.agent_id`

string

Agent ID。

`data.agent_status`

string

Agent 状态，删除后为 `deleted`。

## 错误码

HTTP 状态码

错误码

说明

400

`Index.InvalidParameter`

请求参数不合法，请检查参数是否完整且类型正确。

失败响应示例：

```
{
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "status_code": 400,
  "code": "Index.InvalidParameter",
  "message": "请求参数不合法，请检查参数是否完整且类型正确。",
  "status": "FAILED",
  "success": false
}
```
