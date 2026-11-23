# 查询 MCP 详情

查询官方 MCP 或当前工作空间下自定义 MCP 的详情、状态和配置。

## 接口

**GET** `/api/v1/mcp/servers/{mcpCode}`

## 请求参数

参数

类型

必填

说明

mcpCode

`string`

是

MCP 编码

## 响应

返回完整的 `DetailResponse`。自定义 MCP 的 `mcp_config` 按保存值返回；配置无法恢复时为 `null`。官方 MCP 的 `mcp_config` 始终为 `null`。

字段

类型

说明

mcp\_code

`string`

MCP 编码

server\_name

`string`

MCP 名称

description

`string`

MCP 描述

type

`string`

`OFFICIAL` 或 `CUSTOMER`

server\_type

`string`

`STDIO`、`HTTP`、`SSE` 或 `OPENAPI`

server\_status

`string`

服务状态

server\_status\_text

`string`

状态文案

dashscope\_endpoint

`string / null`

MCP 接入地址，仅已启用或开通中时返回

meta\_info

`object / null`

服务元信息

mcp\_config

`object / null`

自定义 MCP 的已保存配置

`meta_info` 字段见 [MCP API 概览](https://help.aliyun.com/zh/model-studio/mcp-api/overview#h-mcp-api-structures)。

## 示例

```
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/mcp-a1b2c3d4e5f6g7h8" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "mcp_code": "mcp-a1b2c3d4e5f6g7h8",
    "server_name": "weather-mcp",
    "description": "天气查询 MCP",
    "type": "CUSTOMER",
    "server_type": "HTTP",
    "server_status": "ACTIVATED",
    "server_status_text": "已启用",
    "dashscope_endpoint": "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/mcp-a1b2c3d4e5f6g7h8/mcp",
    "meta_info": {
      "console_detail_url": "https://bailian.console.aliyun.com/flow-agent/mcp-manage/detail/mcp-a1b2c3d4e5f6g7h8/custom",
      "classification": "生活服务",
      "activate_user_count": 10,
      "call_total_count": 1200,
      "average_call_time": 125,
      "call_success_rate": 0.99
    },
    "mcp_config": {
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
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

404

McpServerNotFound

MCP 服务不存在，或不属于当前工作空间

404

McpServerUnavailable

MCP 服务已删除或已下架

**警告**`mcp_config.headers` 会按保存值返回，可能包含 API Key 等敏感信息。请妥善保护响应内容。
