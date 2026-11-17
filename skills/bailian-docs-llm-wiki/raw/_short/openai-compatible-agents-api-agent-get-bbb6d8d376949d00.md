# 获取 Agent

根据 Agent ID 返回完整的 Agent 配置。

## 接口

**GET** `/agents/{agent_id}`

成功返回 `200` 和完整 Agent 对象。

## 路径参数

**agent\_id** `string` **（必选）**

Agent ID，按不透明字符串使用

本接口没有 Query 参数。`agent_id` 格式错误、不存在、已删除或属于其他工作空间时返回 `404`。

## 请求示例

curl

```
curl -sS "$BASE_URL/agents/agent_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
agent = client.beta.agents.retrieve("agent_xxx")
print(agent.id, agent.model)
```

### 响应字段

未设置的可选字段可能返回 `null`。

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

## 响应示例

```
{
  "id": "agent_xxx",
  "object": "agent",
  "created_at": 1794117521,
  "updated_at": 1794117521,
  "name": "quickstart-agent",
  "metadata": null,
  "model": "qwen3.8-max",
  "reasoning": null,
  "text": null,
  "instructions": "回答简洁，只输出必要信息。",
  "tools": null,
  "multi_agent": null
}
```

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

HTTP 状态码

错误类型 / 错误码

解决方案

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且未删除的 Agent ID

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
