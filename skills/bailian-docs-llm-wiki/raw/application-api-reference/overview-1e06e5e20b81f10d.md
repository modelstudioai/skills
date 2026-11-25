# MCP API 概览

MCP API 用于管理百炼上的 MCP 服务，支持查询、创建、更新、开通、启停、删除、工具调用与推荐。

MCP API 用于管理阿里云百炼上的 MCP 服务，覆盖官方 MCP 与自定义 MCP 的查询、创建、更新、开通、启停和删除，并提供工具列表、工具调用与工具推荐能力。

> **说明**
>
> 调用前请先配置[认证](overview/authentication-58370587ddc046ee.md)；错误处理见[MCP API 错误码](overview/errors-972b4127b84f4429.md)。

<a id="前提条件"></a>

<a id="h-mcp-api-prereq"></a>

## 前提条件

1.  已开通阿里云百炼，并[创建 API Key](../model-api-reference/preparations/get-api-key.md)。
2.  已获取工作空间 ID。登录[百炼控制台](https://bailian.console.aliyun.com/)，在右上角工作空间菜单中复制工作空间 ID。

<a id="endpoint"></a>

<a id="h-mcp-api-endpoint"></a>

## Endpoint

<a id="code-block"></a>

```text
https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/mcp/servers
```

-   `workspace_id`：工作空间 ID。

<a id="响应结构"></a>

<a id="h-mcp-api-response"></a>

## 响应结构

成功和业务错误统一返回以下结构，响应头包含 `x-request-id`：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| success | `boolean` | 请求是否成功。工具是否执行成功还需查看 `data.isError` |
| error\_code | `string / null` | 错误码，成功时为 `null` |
| error\_msg | `string / null` | 错误信息，成功时为 `null` |
| data | `object / array / null` | 业务数据，失败时为 `null` |
| request\_id | `string` | 请求 ID |

<a id="code-block-2"></a>

```json
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {},
  "request_id": "6f1c2a8e-3b0d-4c55-9a0e-2f7d1c9b8a11"
}
```

<a id="枚举"></a>

<a id="h-mcp-api-enums"></a>

## 枚举

**type（归属类型）**

| 值 | 说明 |
| --- | --- |
| OFFICIAL | 官方 MCP |
| CUSTOMER | 自定义 MCP |

**server\_type（服务类型）**

| 值 | 说明 |
| --- | --- |
| STDIO | 通过 npx/uvx 启动，部署在函数计算 FC |
| HTTP | 远程 Streamable HTTP 服务 |
| SSE | 远程 SSE 服务 |
| OPENAPI | 将已有 HTTP API 转换为 MCP |

**server\_status（服务状态）**

| 值 | 自定义 MCP 文案 | 官方 MCP 文案 |
| --- | --- | --- |
| INACTIVE | 未启用 | 未开通 |
| ACTIVATING | 部署中 | 开通中 |
| ACTIVATED | 已启用 | 已启用 |
| ACTIVATE\_FAILED | 部署失败 | 开通失败 |
| DELETED | 已删除 | \- |

<a id="数据结构"></a>

<a id="h-mcp-api-structures"></a>

## 数据结构

<a id="detailresponse"></a>

### DetailResponse

详情、列表项、开通、停用、启用和删除接口返回的服务信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| mcp\_code | `string / null` | MCP 唯一编码 |
| server\_name | `string / null` | MCP 名称 |
| description | `string / null` | MCP 描述 |
| type | `string / null` | OFFICIAL / CUSTOMER |
| server\_type | `string / null` | STDIO / HTTP / SSE / OPENAPI |
| server\_status | `string / null` | 服务状态 |
| server\_status\_text | `string / null` | 状态文案 |
| dashscope\_endpoint | `string / null` | MCP 接入地址，仅已启用或开通中时返回 |
| meta\_info | `object / null` | 服务元信息 |
| mcp\_config | `object / null` | 自定义 MCP 的已保存配置；官方 MCP 为 `null` |

<a id="meta-info"></a>

### meta\_info

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| icon | `string / null` | 图标地址，仅官方 MCP |
| provider | `string / null` | 提供方，仅官方 MCP |
| is\_onekey | `boolean` | 是否为 One Key MCP，仅官方 MCP |
| console\_detail\_url | `string` | 控制台详情地址 |
| classification | `string / null` | 分类中文名称，未配置时为 `null` |
| activate\_user\_count | `long / null` | 累计开通账号数 |
| call\_total\_count | `long / null` | 累计调用次数 |
| average\_call\_time | `long / null` | 当日成功调用平均耗时，单位毫秒 |
| call\_success\_rate | `double / null` | 成功率，取值 0 到 1 |

自定义 MCP 的 `meta_info` 不包含 `icon`、`provider`、`is_onekey`。

<a id="createresponse"></a>

### CreateResponse

创建和更新接口返回的服务信息，未赋值的字段不输出。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| mcp\_code | `string` | MCP 编码 |
| server\_name | `string` | MCP 名称 |
| server\_status | `string` | 服务状态 |
| server\_status\_text | `string` | 状态文案 |
| activate\_fail\_reason | `string` | 部署失败原因，仅部署失败时返回 |

<a id="请求命名"></a>

<a id="h-mcp-api-naming"></a>

## 请求命名

分页参数使用 `pageNo`、`pageSize`，推荐条数使用 `topN`，路径参数使用 `mcpCode`。请求体和响应字段使用 snake\_case，工具调用结果除外：工具 schema 沿用 MCP 协议字段 `inputSchema`、`additionalProperties`，工具调用结果使用 `isError`。

<a id="接口列表"></a>

<a id="h-mcp-api-list"></a>

## 接口列表

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| [查询 MCP 列表](overview/overview/list-c680a6eef36ba755.md) | GET `/list` | 分页查询官方和自定义 MCP |
| [创建自定义 MCP](overview/overview/create-a29c49f8a08e5095.md) | POST `/` | 创建并部署自定义 MCP |
| [查询 MCP 详情](overview/overview/get-b57e1839b6840677.md) | GET `/{mcpCode}` | 查询 MCP 详情 |
| [更新自定义 MCP](overview/overview/update.md) | POST `/{mcpCode}` | 更新名称、描述或配置 |
| [删除自定义 MCP](overview/overview/delete-23f946e3aa963ba8.md) | DELETE `/{mcpCode}` | 删除自定义 MCP |
| [查询工具列表](overview/overview/list-64eddd50625ee03f.md) | GET `/{mcpCode}/tools` | 查询 MCP 提供的工具 |
| [调用工具](overview/overview/call.md) | POST `/{mcpCode}/tools/call` | 调用指定工具 |
| [推荐工具](overview/overview/recommend.md) | GET `/tools/recommend` | 按自然语言需求推荐工具 |
| [开通官方 MCP](overview/overview/activate.md) | POST `/{mcpCode}/activate` | 开通官方 MCP |
| [关闭官方 MCP](overview/overview/deactivate.md) | POST `/{mcpCode}/deactivate` | 关闭官方 MCP |
| [停用自定义 MCP](overview/overview/disable.md) | POST `/{mcpCode}/disable` | 停用自定义 MCP |
| [启用自定义 MCP](overview/overview/enable.md) | POST `/{mcpCode}/enable` | 启用自定义 MCP |

> **警告**
>
> `mcp_config` 中的 `headers` 等配置会按保存值返回，可能包含敏感信息。请仅在可信环境调用，并妥善保护响应内容。
