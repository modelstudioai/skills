# 查询 MCP 列表

分页查询官方 MCP 和当前工作空间下的自定义 MCP，支持按类型、关键词和分类筛选。

## 接口

**GET** `/api/v1/mcp/servers/list`

不传 `type` 时返回官方 MCP 和当前工作空间下的自定义 MCP。

## 请求参数

参数

类型

必填

默认值

说明

type

`string`

否

\-

`OFFICIAL` 或 `CUSTOMER`，区分大小写

keywords

`string`

否

\-

对 MCP 名称、描述等文本进行全文匹配，空白时不筛选

classification

`string`

否

\-

分类 code，精确匹配；`ALL` 表示不筛选

pageNo

`int`

否

1

页码，从 1 开始

pageSize

`int`

否

20

每页条数，取值 1 到 100

`pageNo × pageSize` 不能超过 10000。

## 响应

`data` 字段：

字段

类型

说明

items

`array<DetailResponse>`

当前页 MCP 列表，每项包含完整的详情字段，`mcp_config` 为 `null`

total

`long`

总条数

page\_no

`int`

当前页码

page\_size

`int`

每页条数

## 示例

```
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers/list?type=CUSTOMER&keywords=weather&pageNo=1&pageSize=20" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "items": [
      {
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
        "mcp_config": null
      }
    ],
    "total": 1,
    "page_no": 1,
    "page_size": 20
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

分页参数超出范围，或携带了不支持的查询参数

500

InternalError

服务内部错误

502

McpUpstreamError

下游 MCP 操作失败
