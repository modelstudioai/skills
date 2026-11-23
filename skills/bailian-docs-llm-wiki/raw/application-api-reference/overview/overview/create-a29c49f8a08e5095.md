# 创建自定义 MCP

创建自定义 MCP 服务并立即部署，支持 STDIO、HTTP、SSE 和 OPENAPI 四种类型。

## 接口

**POST** `/api/v1/mcp/servers`

创建成功后立即触发部署，返回 `201` 和 `Location` 响应头。部署失败仍返回 `201`，服务状态为 `ACTIVATE_FAILED`，失败原因放在 `activate_fail_reason`。

## 请求体

字段

类型

必填

说明

server\_name

`string`

是

MCP 名称，不能为空白

description

`string`

是

MCP 描述，不能为空白

mcp\_type

`string`

是

`STDIO`、`HTTP`、`SSE` 或 `OPENAPI`

mcp\_config

`object`

是

按 `mcp_type` 传入对应配置

### STDIO

字段

类型

必填

说明

command

`string`

是

`npx` 或 `uvx`

args

`array<string>`

是

启动参数，不能为空；每项匹配 `[A-Za-z0-9_@./:=,+-]+`

env

`map<string,string>`

否

环境变量，名称匹配 `[A-Za-z_][A-Za-z0-9_]*`，值必须为字符串

fc\_deploy\_region

`string`

否

函数计算部署地域，需使用控制台支持的地域

使用 STDIO 前，需要为账号授权函数计算 FC。

### HTTP / SSE

字段

类型

必填

说明

url

`string`

是

公网 HTTP(S) 地址，不能包含凭据、`#` 片段或反斜杠

headers

`map<string,string>`

否

下游请求头，名称需为合法 HTTP Header，值不能包含 CR/LF

不包含路径时，HTTP 默认使用 `/mcp`，SSE 默认使用 `/sse`。

### OPENAPI

字段

类型

必填

说明

api\_host

`string`

是

公网 HTTP(S) 地址，不能包含查询串、片段、凭据或反斜杠

headers

`map<string,string>`

否

下游请求头，名称需为合法 HTTP Header，值不能为空白或包含 CR/LF

api\_list

`array<Api>`

是

API 列表，不能为空

**Api**

字段

类型

必填

说明

name

`string`

是

工具名，不能为空白，同一 `api_list` 内不能重复

description

`string`

是

工具描述，不能为空白

path

`string`

是

以 `/` 开头的相对路径，支持 `{param}` 占位符

method

`string`

是

`GET` 或 `POST`

content\_type

`string`

否

`application/json`（默认）或 `application/x-www-form-urlencoded`

input\_params

`array<InputParam>`

否

入参定义，省略时按空数组处理

**InputParam**

字段

类型

必填

说明

name

`string`

是

参数名，不能为空白，同级不能重复

description

`string`

是

参数描述，不能为空白

location

`string`

顶层必填

`Query`、`Path`、`Header` 或 `Body`；子属性可省略

type

`string`

是

`String`、`Number`、`Integer`、`Boolean`、`Object`、`Array<String>`、`Array<Number>`、`Array<Integer>`、`Array<Boolean>` 或 `Array<Object>`

required

`boolean`

否

是否必填，默认 `false`

properties

`array<InputParam>`

视类型

`Object` 或 `Array<Object>` 必须提供非空子属性

`GET` 不能定义顶层 `Body` 参数；顶层对象和数组参数只能放在 `Body`。全部枚举值区分大小写。

## 响应

返回 `CreateResponse`，未赋值的字段不输出。

字段

类型

说明

mcp\_code

`string`

MCP 编码

server\_name

`string`

MCP 名称

server\_status

`string`

部署结果状态

server\_status\_text

`string`

状态文案

activate\_fail\_reason

`string`

部署失败原因，仅部署失败时返回

## 示例

### 创建 HTTP 类型

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "server_name": "weather-mcp",
    "description": "天气查询 MCP",
    "mcp_type": "HTTP",
    "mcp_config": {
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }'
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "mcp_code": "mcp-a1b2c3d4e5f6g7h8",
    "server_name": "weather-mcp",
    "server_status": "ACTIVATED",
    "server_status_text": "已启用"
  },
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

响应头：

```
Location: /api/v1/mcp/servers/mcp-a1b2c3d4e5f6g7h8
X-Request-Id: 6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11
```

### 创建 STDIO 类型

```
{
  "server_name": "amap-maps",
  "description": "高德地图 MCP",
  "mcp_type": "STDIO",
  "mcp_config": {
    "command": "npx",
    "args": ["-y", "@amap/amap-maps-mcp-server"],
    "env": {
      "AMAP_MAPS_API_KEY": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    },
    "fc_deploy_region": "cn-hangzhou"
  }
}
```

### 创建 OPENAPI 类型

```
{
  "server_name": "order-api",
  "description": "订单查询 API",
  "mcp_type": "OPENAPI",
  "mcp_config": {
    "api_host": "https://api.example.com",
    "headers": {
      "X-Api-Key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    },
    "api_list": [
      {
        "name": "getOrder",
        "description": "根据订单号查询订单",
        "path": "/orders/{orderId}",
        "method": "GET",
        "input_params": [
          {
            "name": "orderId",
            "description": "订单号",
            "location": "Path",
            "type": "String",
            "required": true
          }
        ]
      }
    ]
  }
}
```

## 错误

HTTP 状态码

error\_code

说明

400

InvalidParameter

请求体缺失、字段类型错误或字段取值不合法

403

AccessDenied

函数计算未授权，或目标地址不允许访问

500

InternalError

服务内部错误

目标地址为内网地址时返回 `403`，地址格式错误或无法解析时返回 `400`。
