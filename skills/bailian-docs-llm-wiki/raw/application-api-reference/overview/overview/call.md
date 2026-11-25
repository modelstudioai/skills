# 调用工具

调用 MCP 服务中的指定工具，并传入工具参数。

<a id="接口"></a>

<a id="h-mcp-call-endpoint"></a>

## 接口

**POST** `/api/v1/mcp/servers/{mcpCode}/tools/call`

<a id="请求参数"></a>

<a id="h-mcp-call-params"></a>

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| mcpCode | `string` | 是 | MCP 编码 |

请求体：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| tool\_name | `string` | 是 | 工具名称，使用[查询工具列表](list-64eddd50625ee03f.md)返回的名称 |
| tool\_params | `object` | 否 | 工具参数，键和值按工具 schema 传入；省略时按空对象处理 |

无参数工具也需要传 `{"tool_name":"工具名称"}`，不能省略请求体。

<a id="响应"></a>

<a id="h-mcp-call-response"></a>

## 响应

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| isError | `boolean / null` | 工具是否执行出错 |
| content | `array<Content> / null` | 工具返回内容 |
| content\[\].type | `string / null` | 内容类型，例如 `text` |
| content\[\].text | `string / null` | 文本内容 |

<a id="示例"></a>

<a id="h-mcp-call-example"></a>

## 示例

<a id="code-block"></a>

```bash
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/mcp-a1b2c3d4e5f6g7h8/tools/call" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_weather",
    "tool_params": {
      "city": "杭州"
    }
  }'
```

<a id="code-block-2"></a>

```json
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "isError": false,
    "content": [
      {
        "type": "text",
        "text": "杭州今天晴，气温 18~26℃"
      }
    ]
  },
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

<a id="错误"></a>

<a id="h-mcp-call-errors"></a>

## 错误

| HTTP 状态码 | error\_code | 说明 |
| --- | --- | --- |
| 400 | InvalidParameter | `tool_name` 缺失，或 `tool_params` 不是 JSON 对象 |
| 400 | \- | MCP 服务调用失败，错误码由服务返回 |

> **说明**
>
> 工具自身执行出错时，接口可能返回 `200`、`success=true`、`data.isError=true`。请同时检查 HTTP 状态码和 `data.isError`。
