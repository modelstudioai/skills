# 更新自定义 MCP

更新自定义 MCP 的名称、描述或配置。修改配置会重新部署服务。

<a id="接口"></a>

<a id="h-mcp-update-endpoint"></a>

## 接口

**POST** `/api/v1/mcp/servers/{mcpCode}`

仅支持自定义 MCP。只修改名称或描述时不会重新部署；同时修改 `mcp_type` 和 `mcp_config` 时会完整替换配置并重新部署。

<a id="请求参数"></a>

<a id="h-mcp-update-params"></a>

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| mcpCode | `string` | 是 | MCP 编码 |

请求体至少包含一个可修改字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| server\_name | `string` | 否 | 新名称，不能为空白 |
| description | `string` | 否 | 新描述，不能为空白 |
| mcp\_type | `string` | 否 | 新服务类型，必须与 `mcp_config` 同时提交 |
| mcp\_config | `object` | 否 | 新配置，必须与 `mcp_type` 同时提交；为完整替换，不是局部合并 |

修改配置前，需要先停用服务。服务处于运行中或部署中时，修改配置返回 `400`。

<a id="响应"></a>

<a id="h-mcp-update-response"></a>

## 响应

返回 `CreateResponse`，未赋值的字段不输出。只修改名称或描述时，不返回状态字段。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| mcp\_code | `string` | MCP 编码 |
| server\_name | `string` | 更新后的名称 |
| server\_status | `string` | 重新部署结果，仅修改配置时返回 |
| server\_status\_text | `string` | 状态文案，仅修改配置时返回 |
| activate\_fail\_reason | `string` | 部署失败原因，仅部署失败时返回 |

<a id="示例"></a>

<a id="h-mcp-update-example"></a>

## 示例

<a id="修改名称和描述"></a>

### 修改名称和描述

<a id="code-block"></a>

```bash
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/mcp-a1b2c3d4e5f6g7h8" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "server_name": "weather-mcp-v2",
    "description": "天气查询 MCP（新版）"
  }'
```

<a id="code-block-2"></a>

```json
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "mcp_code": "mcp-a1b2c3d4e5f6g7h8",
    "server_name": "weather-mcp-v2"
  },
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

<a id="修改配置"></a>

### 修改配置

<a id="code-block-3"></a>

```bash
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/mcp-a1b2c3d4e5f6g7h8" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mcp_type": "SSE",
    "mcp_config": {
      "url": "https://mcp.example.com/sse"
    }
  }'
```

<a id="code-block-4"></a>

```json
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "mcp_code": "mcp-a1b2c3d4e5f6g7h8",
    "server_name": "weather-mcp-v2",
    "server_status": "ACTIVATED",
    "server_status_text": "已启用"
  },
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

<a id="错误"></a>

<a id="h-mcp-update-errors"></a>

## 错误

| HTTP 状态码 | error\_code | 说明 |
| --- | --- | --- |
| 400 | InvalidParameter | 请求体为空，或 `mcp_type` 与 `mcp_config` 未同时提交 |
| 400 | OperationNotSupported | 官方 MCP，或服务正在运行、部署中 |
| 404 | McpServerNotFound | MCP 服务不存在，或不属于当前工作空间 |
| 409 | McpServerBusy | MCP 服务有操作执行中 |
