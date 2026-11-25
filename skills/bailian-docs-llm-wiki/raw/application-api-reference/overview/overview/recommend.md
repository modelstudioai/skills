# 推荐工具

根据自然语言需求推荐 MCP 工具，返回工具名称、描述和入参 schema。

<a id="接口"></a>

<a id="h-mcp-recommend-endpoint"></a>

## 接口

**GET** `/api/v1/mcp/servers/tools/recommend`

<a id="请求参数"></a>

<a id="h-mcp-recommend-params"></a>

## 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| query | `string` | 是 | \- | 自然语言检索需求，不能为空白 |
| topN | `int` | 否 | 10 | 建议返回数量；小于等于 0 时使用默认值 10 |

`topN` 是目标条数，不保证返回数量严格等于该值。

<a id="响应"></a>

<a id="h-mcp-recommend-response"></a>

## 响应

`data` 为工具数组，每项包含四个字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| mcp\_code | `string` | MCP 编码，可用于路径参数 `mcpCode` |
| tool\_name | `string` | 工具名称，可用于调用工具的 `tool_name` |
| tool\_description | `string / null` | 工具描述 |
| tool\_input\_schema | `object / null` | 工具入参 schema，结构与[查询工具列表](list-64eddd50625ee03f.md)的 `inputSchema` 相同 |

<a id="示例"></a>

<a id="h-mcp-recommend-example"></a>

## 示例

<a id="code-block"></a>

```bash
curl -G "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/tools/recommend" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --data-urlencode "query=根据订单号查询订单" \
  --data-urlencode "topN=5"
```

<a id="code-block-2"></a>

```json
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": [
    {
      "mcp_code": "mcp-a1b2c3d4e5f6g7h8",
      "tool_name": "getOrder",
      "tool_description": "根据订单号查询订单",
      "tool_input_schema": {
        "type": "object",
        "properties": {
          "orderId": {
            "type": "string",
            "description": "订单号"
          }
        },
        "required": ["orderId"],
        "additionalProperties": false
      }
    }
  ],
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

<a id="错误"></a>

<a id="h-mcp-recommend-errors"></a>

## 错误

| HTTP 状态码 | error\_code | 说明 |
| --- | --- | --- |
| 400 | InvalidParameter | `query` 缺失或空白，或携带了不支持的查询参数 |
| 502 | McpUpstreamError | 下游 MCP 操作失败 |

> **说明**
>
> 推荐结果不代表服务已经开通。调用 One Key MCP 工具时，服务可能自动完成开通并产生费用。
