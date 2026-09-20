# 发布 Agent

将 beta 草稿发布为新版本，版本号自增。

## 前提

已获取阿里云百炼 API Key 与业务空间 ID，鉴权方式见[API 认证](raw/application-api-reference/rag-api/rag-api-authentication.md)。发布 Agent 需要知识库-修改权限，由[业务空间成员管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)中的角色决定，详见[权限要求](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-overview.md)。

## 接口

**POST** `/api/v1/indices/rag/app/deploy`

将指定 Agent 的 `beta` 版本发布为正式版本。发布后 Agent 状态变为 `deployed`，版本号递增为数字（如 `1`、`2` 等）。

**说明**支持并发发布安全（底层通过 DB 唯一索引 + 冲突重试作为容错机制）。

## 请求体

字段

必填

类型

说明

`agent_id`

是

string

Agent ID。

`agent_version_desc`

否

string

本次发布的版本描述。

## 请求示例

```
curl -X POST "$BASE_URL/api/v1/indices/rag/app/deploy" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "aid-8f3a1b2c4d5e6f70",
    "agent_version_desc": "新增防泄漏功能，优化检索参数"
}'
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`（`{workspace_id}` 为业务空间 ID），`BAILIAN_API_KEY` 为阿里云百炼 API Key。

## 响应示例

操作成功返回 200。

```
{
  "request_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "status_code": 200,
  "code": "Success",
  "message": "",
  "status": "SUCCESS",
  "success": true,
  "data": {
    "agent_id": "aid-8f3a1b2c4d5e6f70",
    "agent_version": "2",
    "agent_status": "deployed"
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

`data.agent_version`

string

发布后的版本号，如 `1`、`2`。

`data.agent_status`

string

Agent 状态，发布后为 `deployed`。

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
