# MCP API 错误码

MCP API 的错误响应结构、常见错误码和工具调用错误处理。

MCP API 的成功响应和业务错误使用统一响应结构，响应头包含 `x-request-id`。

## 响应结构

字段

类型

说明

success

`boolean`

请求是否成功。工具是否执行成功还需查看 `data.isError`

error\_code

`string / null`

错误码，成功时为 `null`

error\_msg

`string / null`

错误信息，成功时为 `null`

data

`object / array / null`

业务数据，失败时为 `null`

request\_id

`string`

请求 ID

```
{
  "success": false,
  "error_code": "McpServerNotFound",
  "error_msg": "MCP 服务不存在",
  "data": null,
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

## 常见错误码

HTTP 状态码

error\_code

说明

400

InvalidParameter

请求参数缺失、格式错误或超出取值范围

400

OperationNotSupported

当前 MCP 服务不支持该操作

403

AccessDenied

无权限访问目标地址或资源

404

McpServerNotFound

MCP 服务不存在

404

McpServerUnavailable

MCP 服务已删除或已下架

409

McpServerBusy

MCP 服务有操作执行中

409

McpServerStateConflict

MCP 服务当前状态不允许该操作

409

McpServerNotActivated

MCP 服务尚未开通

500

InternalError

服务内部错误

502

McpUpstreamError

下游 MCP 操作失败

503

McpUpstreamThrottled

下游 MCP 请求被限流

504

McpUpstreamTimeout

下游 MCP 请求超时

## 工具调用错误

-   `tools/call` 调用失败时可能返回 `400`，并透传 MCP 服务的 `error_code` 和 `error_msg`。
-   工具自身执行出错时，可能返回 `200`、`success=true`、`data.isError=true`。请同时检查 HTTP 状态码和 `data.isError`。
-   `tools` 查询工具列表失败时可能返回 `400` 或 `500` `InternalError`。

## 排查建议

1.  使用 `request_id` 定位具体请求。
2.  检查 API Key、工作空间 ID 和 Endpoint 是否正确，详见[认证](raw/application-api-reference/overview/authentication.md)。
3.  确认 MCP 服务已开通且状态为已启用。
4.  确认请求体字段名和类型符合接口文档。
