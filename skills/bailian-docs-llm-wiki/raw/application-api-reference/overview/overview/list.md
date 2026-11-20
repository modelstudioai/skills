# 查询工具列表

查询指定 MCP 服务提供的工具名称、描述和入参 schema。

## 接口

**GET** `/api/v1/mcp/servers/{mcpCode}/tools`

返回指定 MCP 服务当前可用的工具列表。

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

`data` 为工具数组，每个工具包含以下字段：

字段

类型

说明

name

`string / null`

工具名称

description

`string / null`

工具描述

inputSchema

`object / null`

工具入参 schema

inputSchema.type

`string / null`

通常为 `object`

inputSchema.properties

`map<string,object> / null`

参数定义

inputSchema.required

`array<string> / null`

必填参数名

inputSchema.additionalProperties

`boolean / null`

是否允许额外参数

## 示例

```
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/mcp-a1b2c3d4e5f6g7h8/tools" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": [
    {
      "name": "get_weather",
      "description": "查询指定城市的天气",
      "inputSchema": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "城市名称"
          }
        },
        "required": ["city"],
        "additionalProperties": false
      }
    }
  ],
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

## 错误

HTTP 状态码

error\_code

说明

400

\-

服务未开通、实例异常或工具列表为空，错误码由 MCP 服务返回

500

InternalError

服务内部错误

**说明**One Key MCP 服务无需提前开通。首次查询工具或调用工具时，服务可能自动完成开通。
