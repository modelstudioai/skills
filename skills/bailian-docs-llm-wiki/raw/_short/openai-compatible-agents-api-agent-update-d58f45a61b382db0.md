# 更新 Agent

更新 Agent 配置；省略的顶层字段保持原值，传入的对象或数组整体替换。

## 接口

**POST** `/agents/{agent_id}`

成功返回 `200` 和更新后的完整 Agent 对象。更新采用顶层字段替换语义：省略的字段保持原值，显式传入的对象或数组整体替换，`null` 清除可空字段。更新不是递归 JSON Merge Patch；`metadata:{"a":"new"}` 会删除未出现在新对象中的旧 key。

`model` 可以省略，但显式 `null` 返回 `400`。更新冲突时服务端会重新读取并合并，最多尝试 3 次；耗尽返回 `500`；不提供公开的 `version` 或 ETag 条件更新字段。`{}` 不修改业务字段，也不保证 `updated_at` 一定变化。

## 请求体

**model** `string` **（可选）**

模型 ID；省略保持原值，显式 `null` 返回 `400`；修改后必须属于当前工作空间可用的模型，否则返回 `404 model_not_found`。可选模型见[创建 Agent 的可选模型](https://help.aliyun.com/zh/model-studio/openai-compatible-agents-api-agent-create#h-oa-agent-create-models)。

**name** `string / null` **（可选）**

展示名称，最多 128 字符；`null` 清空

**instructions** `string / null` **（可选）**

自定义指令，最多 1,048,576 字符；`null` 清空

**metadata** `object / null` **（可选）**

元数据，字符串键值对，整体替换，`null` 清空，`{}` 替换为空对象

**reasoning** `object / null` **（可选）**

推理配置，整体替换；`null` 清空。

属性

**effort** `string / null` **（可选）**

推理强度：`none`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`

**summary** `string / null` **（可选）**

推理摘要：`concise`、`detailed`、`auto`

**text** `object / null` **（可选）**

文本配置，整体替换；`null` 清空。只支持固定 `text` 输出

**tools** `array / null` **（可选）**

工具列表，整体替换；`null` 清空，`[]` 替换为空列表。

属性

function

**name** `string` **（必选）**

函数名称，同一 Agent 内不能重复

**description** `string / null` **（必选）**

函数说明，可以传 `null`

**parameters** `object` **（必选）**

函数入参 JSON Schema，必须声明 `type: object`

mcp

**server\_label** `string` **（必选）**

MCP 服务标识，同一 Agent 内不能重复

**transport** `object` **（必选）**

传输配置，见下方分支

属性

**type** `string` **（必选）**

传输类型，`http` 或 `stdio`

**server\_url** `string / null` **（条件必填）**

MCP 服务地址

**headers** `object<string,string> / null` **（可选）**

附加 HTTP 请求头，不要放密钥

**command** `string` **（条件必填）**

启动命令

**cwd** `string` **（条件必填）**

工作目录，必须是绝对路径，路径段不能是 `.` 或 `..`

**args** `array<string> / null` **（可选）**

命令参数

**allowed\_tools** `array<string> / null` **（可选）**

允许调用的工具名列表；`null` 表示不过滤

**required** `boolean` **（可选）**

是否要求 MCP 初始化成功

**connection\_origin** `string / null` **（可选）**

连接来源，`service` 或 `environment`，默认 `service`

web\_search

**type** `string` **（必选）**

工具类型，固定为 `web_search`

**multi\_agent** `object / null` **（可选）**

多 Agent 配置，整体替换；`null` 清空，不补默认并发值

工具字段：每个工具必须提供 `type`，当前支持 `function`、`mcp`、`web_search`。更新只保存配置，不代表工具可执行。

未知顶层字段不会报错，可能被过滤并记录，不能以请求未报错判断字段已经生效。

更新先校验 patch，再查询资源；非法 patch 与资源不存在同时发生时，可能先返回 `400`。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/agents/agent_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "example-agent",
    "metadata": {"purpose": "qa"},
    "reasoning": {"effort": "medium", "summary": "auto"},
    "tools": [{"type": "web_search"}]
  }'
```

Python

```
agent = client.beta.agents.update(
    "agent_xxx",
    name="example-agent",
    metadata={"purpose": "qa"},
    reasoning={"effort": "medium", "summary": "auto"},
    tools=[{"type": "web_search"}],
)
print(agent.updated_at)
```

### 响应字段

返回更新后的完整 Agent 对象。 未设置的可选字段可能返回 `null`。

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
  "updated_at": 1794117600,
  "name": "example-agent",
  "metadata": {"purpose": "qa"},
  "model": "qwen3.8-max",
  "reasoning": {"effort": "medium", "summary": "auto"},
  "text": null,
  "instructions": "回答简洁，必要时给出操作步骤。",
  "tools": [
    {
      "type": "web_search"
    }
  ],
  "multi_agent": null
}
```

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按请求体字段说明修正类型、枚举、长度和跨字段约束；省略 `model`，不要传 `null`

`400`

`invalid_request_error` / `string_above_max_length`

将 `instructions` 缩短到 1,048,576 字符以内

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`invalid_request_error` / `model_not_found`

改为当前工作空间可用的模型 ID

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且未删除的 Agent ID

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
