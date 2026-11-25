# 开通官方 MCP

开通官方 MCP 服务。提交后服务进入开通中状态，可通过详情接口查询结果。

<a id="接口"></a>

<a id="h-mcp-activate-endpoint"></a>

## 接口

**POST** `/api/v1/mcp/servers/{mcpCode}/activate`

用于开通官方 MCP 服务。One Key MCP 服务会按商品类型完成开通或下单。

<a id="请求参数"></a>

<a id="h-mcp-activate-params"></a>

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| mcpCode | `string` | 是 | 官方 MCP 编码 |

请求体可以省略。提供时支持以下字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| env | `map<string,string>` | 视服务 | 环境变量；服务声明的必填变量必须全部传入且不能为空白 |
| fc\_deploy\_region | `string` | 否 | 函数计算部署地域，需与控制台当前地域一致 |

需要选择 KMS 凭据或 RAM 角色的 MCP 服务，请前往控制台手动开通。

<a id="响应"></a>

<a id="h-mcp-activate-response"></a>

## 响应

返回完整的 `DetailResponse`。新发起开通时，部分基础字段可能为 `null`，可通过状态字段判断开通进度。

| 状态 | 说明 |
| --- | --- |
| ACTIVATING | 开通中 |
| ACTIVATED | 已启用 |
| ACTIVATE\_FAILED | 开通失败 |

<a id="示例"></a>

<a id="h-mcp-activate-example"></a>

## 示例

<a id="code-block"></a>

```bash
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/amap-maps/activate" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "env": {
      "AMAP_MAPS_API_KEY": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
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
    "mcp_code": "amap-maps",
    "server_name": null,
    "description": null,
    "type": null,
    "server_type": null,
    "server_status": "ACTIVATING",
    "server_status_text": "开通中",
    "dashscope_endpoint": "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcps/amap-maps/mcp",
    "meta_info": {
      "icon": null,
      "provider": null,
      "is_onekey": false,
      "console_detail_url": "https://bailian.console.aliyun.com/store/mcp/detail/amap-maps",
      "classification": "交通物流",
      "activate_user_count": 3000,
      "call_total_count": 120000,
      "average_call_time": 80,
      "call_success_rate": 0.995
    },
    "mcp_config": null
  },
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

<a id="错误"></a>

<a id="h-mcp-activate-errors"></a>

## 错误

| HTTP 状态码 | error\_code | 说明 |
| --- | --- | --- |
| 400 | InvalidParameter | 缺少必填环境变量，或部署地域与控制台不一致 |
| 400 | OperationNotSupported | 云市场 MCP，或需要 KMS 凭据或 RAM 角色的 MCP |
| 404 | McpServerNotFound | MCP 服务不存在 |
| 409 | McpServerBusy | MCP 服务有操作执行中 |

> **说明**
>
> 已开通的服务可能直接返回当前详情。
