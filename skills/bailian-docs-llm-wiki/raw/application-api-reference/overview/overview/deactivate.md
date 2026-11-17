# 关闭官方 MCP

关闭当前工作空间下已开通的官方 MCP 服务。One Key MCP 不支持关闭。

## 接口

**POST** `/api/v1/mcp/servers/{mcpCode}/deactivate`

仅支持官方 MCP，且不支持 One Key MCP。关闭后服务状态变为 `INACTIVE`，状态文案为“未开通”。

## 请求参数

参数

类型

必填

说明

mcpCode

`string`

是

官方 MCP 编码

## 响应

返回 `DetailResponse`，仅填充 `mcp_code`、`server_status` 和 `server_status_text`，其余字段为 `null`。

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/amap-maps/deactivate" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "mcp_code": "amap-maps",
    "server_name": null,
    "description": null,
    "type": null,
    "server_type": null,
    "server_status": "INACTIVE",
    "server_status_text": "未开通",
    "dashscope_endpoint": null,
    "meta_info": null,
    "mcp_config": null
  },
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

## 错误

HTTP 状态码

error\_code

说明

400

InvalidParameter

携带了查询参数或请求体

400

OperationNotSupported

自定义 MCP

400

DeActivateFailed

One Key MCP，或服务正在部署中

404

McpServerNotFound

MCP 服务不存在

404

McpServerUnavailable

MCP 服务已下架
