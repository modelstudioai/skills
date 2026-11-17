# 创建 Agent

创建一个可复用的 Agent 配置，保存模型、指令、工具与多 Agent 设置。

## 接口

**POST** `/agents`

成功返回 `201` 和完整 Agent 对象。创建只保存配置，不启动 Session、模型或 MCP 服务；相同请求体重复提交会创建新资源。

## 请求体

**model** `string` **（必选）**

模型 ID，必须命中当前工作空间可用的模型，否则返回 `404 model_not_found`。可选模型见[可选模型](#h-oa-agent-create-models)。

**name** `string / null` **（可选）**

展示名称，最多 128 字符。

**instructions** `string / null` **（可选）**

追加到 Agent 默认指令的自定义指令，最多 1,048,576 字符。

**metadata** `object / null` **（可选）**

元数据，字符串键值对；建议最多 16 项，key 建议最多 64 字符，value 建议最多 512 字符。全部值必须是字符串。

**reasoning** `object / null` **（可选）**

推理配置，包含以下字段。

属性

**effort** `string / null` **（可选）**

推理强度：`none`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`。

**summary** `string / null` **（可选）**

推理摘要：`concise`、`detailed`、`auto`。

**text** `object / null` **（可选）**

文本输出配置，包含以下字段。

属性

format

**type** `string` **（条件必填）**

输出格式类型，固定为 `text`。

**verbosity** `string / null` **（可选）**

输出详细程度，`low`、`medium`、`high`；Session 执行侧当前只接受 `medium`。

**tools** `array / null` **（可选）**

工具配置。每个工具必须提供 `type`，当前支持 `function`、`mcp`、`web_search`。创建只保存配置，不代表工具可执行。

属性

function

**name** `string` **（必选）**

函数名称

**description** `string / null` **（必选）**

函数说明，可以传 `null`

**parameters** `object` **（必选）**

函数入参 JSON Schema，必须声明 `type: object`

mcp

**server\_label** `string` **（必选）**

MCP 服务标识

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

子 Agent 配置，包含以下字段。

属性

**enabled** `boolean` **（必选）**

是否启用子 Agent 工具；父对象存在时必填。

**max\_concurrent\_subagents** `integer / null` **（可选）**

并发子 Agent 上限；执行侧当前支持 `1..32`，默认 6。

未知顶层字段不会报错，可能被过滤并记录，不能以请求未报错判断字段已经生效。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/agents" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-max",
    "name": "support-agent",
    "instructions": "回答简洁，必要时给出操作步骤。",
    "metadata": {"team": "support"}
  }'
```

Python

```
agent = client.beta.agents.create(
    model="qwen3.8-max",
    name="support-agent",
    instructions="回答简洁，必要时给出操作步骤。",
    metadata={"team": "support"},
)
print(agent.id)
```

### 响应字段

**id** `string`

Agent ID，按不透明字符串使用。

**object** `string`

Agent 对象类型，固定为 `agent`。

**created\_at** `integer`

创建时间的 Unix 秒时间戳。

**updated\_at** `integer`

最近修改时间的 Unix 秒时间戳，不是版本号。

**name** `string / null`

展示名称。

**metadata** `object / null`

元数据，保存的字符串键值对。

**model** `string`

保存的模型 ID。

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

保存的自定义指令。

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
  "name": "support-agent",
  "metadata": {"team": "support"},
  "model": "qwen3.8-max",
  "reasoning": null,
  "text": null,
  "instructions": "回答简洁，必要时给出操作步骤。",
  "tools": null,
  "multi_agent": null
}
```

## 可选模型

`model` 支持以下模型：

**品牌**

**模型 ID**

**模型能力**

千问

qwen4-max

推理模型、视觉理解、文本生成

千问

qwen3.8-max

推理模型、视觉理解、文本生成

千问

qwen3.7-max

推理模型、文本生成

千问

qwen3.7-plus

推理模型、视觉理解、文本生成

千问

qwen3.6-plus

推理模型、视觉理解、文本生成

DeepSeek

deepseek-v4-pro

推理模型、文本生成

智谱 AI

glm-5.3

推理模型、文本生成

智谱 AI

glm-5.2

推理模型、文本生成

月之暗面

kimi-k3

推理模型、视觉理解、文本生成

具备视觉理解能力的模型可处理创建会话时传入的图片，详见[创建会话](raw/_short/openai-compatible-agents-api-session-create-82108dd4f418e8ad.md)。

**说明**模型列表持续更新，以控制台创建 Agent 时的下拉列表为准。

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按请求体说明补齐 `model`、修正字段类型和枚举、满足工具跨字段约束，并发送合法 JSON

`400`

`invalid_request_error` / `string_above_max_length`

将 `instructions` 缩短到 1,048,576 字符以内

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`invalid_request_error` / `model_not_found`

改为当前工作空间可用的模型 ID

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`

鉴权、工作空间路由和限流错误可能由网关直接返回，结构可能与业务错误不同。
