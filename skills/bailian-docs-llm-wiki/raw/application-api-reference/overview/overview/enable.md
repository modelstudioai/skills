# 启用自定义 MCP

使用已保存的配置重新部署并启用自定义 MCP 服务。

<a id="接口"></a>

<a id="h-mcp-enable-endpoint"></a>

## 接口

**POST** `/api/v1/mcp/servers/{mcpCode}/enable`

仅支持自定义 MCP。服务会使用已保存的配置重新部署，不能通过此接口提交新配置或环境变量。无需请求体。

<a id="请求参数"></a>

<a id="h-mcp-enable-params"></a>

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| mcpCode | `string` | 是 | 自定义 MCP 编码 |

<a id="响应"></a>

<a id="h-mcp-enable-response"></a>

## 响应

返回 `DetailResponse`，仅填充 `mcp_code`、`server_status` 和 `server_status_text`，其余字段为 `null`。

<a id="code-block"></a>

```bash
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/mcp-a1b2c3d4e5f6g7h8/enable" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="code-block-2"></a>

```json
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
    "server_status": "ACTIVATED",
    "server_status_text": "已启用",
    "dashscope_endpoint": null,
    "meta_info": null,
    "mcp_config": null
  },
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

<a id="错误"></a>

<a id="h-mcp-enable-errors"></a>

## 错误

| HTTP 状态码 | error\_code | 说明 |
| --- | --- | --- |
| 400 | OperationNotSupported | 官方 MCP |
| 400 | EnableFailed | 启用失败 |
| 404 | McpServerNotFound | MCP 服务不存在 |
| 409 | McpServerBusy | MCP 服务有操作执行中 |
