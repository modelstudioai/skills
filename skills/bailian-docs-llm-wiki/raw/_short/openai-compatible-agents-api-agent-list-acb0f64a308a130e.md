# 列出 Agent

分页列出当前工作空间中的 Agent。

## 接口

**GET** `/agents`

成功返回 `200` 和列表信封，`data` 为 Agent 对象数组。

## 查询参数

**limit** `integer` **（可选）**

每页数量，默认 20；建议使用 `1..100`

**order** `string` **（可选）**

排序方向，`asc` 或 `desc`，默认 `desc`

**after** `string` **（可选）**

上一页的 `last_id`；不包含游标项

**before** `string` **（可选）**

上一页的 `first_id`，用于反向翻页，不能与 `after` 同时使用；游标必须是当前工作空间中有效的 Agent

同时传 `after` 和 `before` 返回 `400`。翻页时首次不传 `after`，后续传上一页的 `last_id`；反向翻页使用 `first_id` 作为 `before`。`has_more` 表示当前扫描方向还有结果。列表按 Agent ID 字典序排序，不保证按 `created_at` 稳定排序，也不提供并发写入下的快照隔离。

## 请求示例

curl

```
curl -sS "$BASE_URL/agents?limit=20&order=desc" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
page = client.beta.agents.list(limit=20, order="desc")
for agent in page.data:
    print(agent.id, agent.name)
```

### 响应字段

**object** `string`

列表对象类型，固定为 `list`

**data** `array`

当页 Agent 对象，空时为 `[]`

**first\_id** `string / null`

当页首项 ID。空页为 `null`

**last\_id** `string / null`

当页末项 ID。空页为 `null`

**has\_more** `boolean`

当前扫描方向是否还有下一页

### Agent 字段

**id** `string`

Agent ID，按不透明字符串使用

**object** `string`

Agent 对象类型，固定为 `agent`

**created\_at** `integer`

创建时间的 Unix 秒时间戳

**updated\_at** `integer`

最近修改时间的 Unix 秒时间戳，不是版本号

**name** `string / null`

展示名称

**metadata** `object / null`

元数据，保存的字符串键值对

**model** `string`

保存的模型 ID

**reasoning** `object / null`

推理配置。两项均可为 `null`。

属性

**effort** `string / null`

推理强度：`none`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`

**summary** `string / null`

推理摘要：`concise`、`detailed`、`auto`

**text** `object / null`

文本输出配置。

属性

**format** `object`

输出格式。

属性

**type** `string / null`

输出格式类型，固定为 `text`

**verbosity** `string / null`

输出详细程度，`low`、`medium`、`high`

**instructions** `string / null`

保存的自定义指令

**tools** `array / null`

保存的工具配置；每个分支只返回本分支字段

属性

**function** `object`

Function 工具配置，返回 `name`、`description`、`parameters`

**mcp** `object`

MCP 工具配置，返回 `server_label`、`transport`、`allowed_tools`、`required`、`connection_origin`；`transport` 为 `http` 或 `stdio`

**web\_search** `object`

Web Search 工具配置，返回 `type` 和已保存的配置

**multi\_agent** `object / null`

子 Agent 配置。

属性

**enabled** `boolean`

是否启用子 Agent 工具

**max\_concurrent\_subagents** `integer / null`

最大并发子 Agent 数；不补默认值

未设置的可选字段可能返回 `null`。

## 响应示例

```
{
  "object": "list",
  "data": [],
  "first_id": null,
  "last_id": null,
  "has_more": false
}
```

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按查询参数说明修正 `limit`、`order`

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用本集合上一页返回的 `last_id` 作为 `after`

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
