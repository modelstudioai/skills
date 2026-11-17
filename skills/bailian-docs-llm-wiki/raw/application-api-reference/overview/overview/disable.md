# 停用自定义 MCP

停用自定义 MCP 服务，保留服务定义和已保存配置。

## 接口

**POST** `/api/v1/mcp/servers/{mcpCode}/disable`

仅支持自定义 MCP。停用会关闭服务实例，但保留服务定义和已保存配置，之后可以通过[启用自定义 MCP](raw/application-api-reference/overview/overview/enable.md)重新启用。

## 请求参数

参数

类型

必填

说明

mcpCode

`string`

是

自定义 MCP 编码

## 响应

返回 `DetailResponse`，仅填充 `mcp_code`、`server_status` 和 `server_status_text`，其余字段为 `null`。

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/mcp-a1b2c3d4e5f6g7h8/disable" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "mcp_code": "mcp-a1b2c3d4e5f6g7h8",
    "server_name": null,
    "description": null,
    "type": null,
    "server_type": null,
    "server_status": "INACTIVE",
    "server_status_text": "未启用",
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

官方 MCP

400

DisableFailed

停用失败，例如服务正在部署中

404

McpServerNotFound

MCP 服务不存在

409

McpServerBusy

MCP 服务有操作执行中
