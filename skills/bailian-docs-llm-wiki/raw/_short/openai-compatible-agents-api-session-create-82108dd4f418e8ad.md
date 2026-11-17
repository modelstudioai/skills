# 创建 Session

创建 Session，绑定 Agent 与运行环境，并可提交首轮输入。

## 接口

**POST** `/agents/sessions`

非流式请求返回 `201` JSON；`stream=true` 时返回 `201 text/event-stream`。创建返回 `201` 表示 Session 和首轮输入已受理，不表示 Turn 已执行完成。

## 请求体

**environment** `object` **（必选）**

运行环境，见下文

**agent\_id** `string / null` **（条件必填）**

已保存 Agent ID，最多 64 字符

**agent** `object` **（条件必填）**

内联 Agent 配置；与 `agent_id` 同时提供时作为会话级覆盖，未覆盖字段沿用已保存值

属性

**model** `string` **（条件必填）**

模型 ID；内联创建必填；引用已保存 Agent 时可继承。创建预检最多 256 字符，必须命中当前工作空间可用的模型。可选模型见[创建 Agent 的可选模型](https://help.aliyun.com/zh/model-studio/openai-compatible-agents-api-agent-create#h-oa-agent-create-models)。

**instructions** `string / null` **（可选）**

系统指令，最多 1,048,576 Unicode 字符；执行时合并到系统提示词

**name** `string / null` **（可选）**

展示名称，不参与执行配置

reasoning

**effort** `string / null` **（可选）**

推理强度，`none`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`、`ultra`；未指定时返回 `none`

**summary** `string / null` **（可选）**

推理摘要类型，`auto`、`concise`、`detailed`、`none`；未指定时返回 `auto`。字符串 `none` 与 JSON `null` 不同

text

**format** `object / null` **（可选）**

文本格式配置，只接受 `type: text`，未知字段拒绝，缺失或 `null` 为 `{"type":"text"}`

**verbosity** `string / null` **（可选）**

输出详细程度，只接受 `medium`，缺失或 `null` 为 `medium`

**tools** `array` **（可选）**

工具列表，缺失为空列表，显式 `null` 不接受。`function` 最多 32 个，MCP 最多 16 个

属性

function

**type** `string` **（必选）**

工具类型，固定为 `function`

**name** `string` **（必选）**

函数名称，1..64 字节，字符集 `A-Za-z0-9_.:-`；同一 Agent 内不能重复

**description** `string` **（必选）**

函数说明，去除空白后非空，不超过 1024 字节

**parameters** `object` **（必选）**

参数定义；必须是 `type: object` 的 JSON Schema

mcp

**type** `string` **（必选）**

工具类型，固定为 `mcp`

**server\_label** `string` **（必选）**

MCP 服务标识，1..64 字节，同一 Agent 内唯一

**transport** `object` **（必选）**

HTTP 或 stdio 传输配置

属性

**type** `string` **（必选）**

传输类型，`http` 或 `stdio`

**server\_url** `string` **（条件必填）**

MCP 服务地址；`service` 只接受百炼定位 URL（`/api/v1/mcps/{code}/mcp`）；`environment` 接受环境可达的普通 HTTP 地址

**headers** `object<string,string> / null` **（可选）**

附加 HTTP 请求头

**authorization** `string / null` **（可选）**

只用于 `connection_origin=environment` 的 HTTP 分支

**command** `string` **（条件必填）**

启动命令

**cwd** `string` **（条件必填）**

绝对路径；stdio 必须有环境

**args** `array<string>` **（可选）**

命令参数

**allowed\_tools** `array<string> / null` **（可选）**

允许调用的工具名列表；`null` 表示不过滤

**connection\_origin** `string` **（可选）**

连接来源，`service` 或 `environment`，默认 `service`

**required** `boolean` **（可选）**

是否要求 MCP 初始化成功

web\_search

**type** `string` **（必选）**

工具类型，固定为 `web_search`

**multi\_agent** `object / null` **（可选）**

多 Agent 配置，缺失或 `null` 为禁用；对象存在时 `enabled` 可省略，默认 `false`，显式 `null` 拒绝

属性

**max\_concurrent\_subagents** `integer` **（可选）**

最大并发 Subagent 数，显式值要求 `enabled=true` 且为 `1..32`，显式 `null` 拒绝；启用时缺失默认 6，禁用时返回 `null`

**input** `string 或 array / null` **（条件必填）**

首轮输入。字符串是单条 user 文本消息的简写；空字符串会被拒绝

属性

**role** `string` **（必选）**

消息角色，固定为 `user`

**type** `string` **（可选）**

消息类型，显式值只能是 `message`

**content** `array` **（必选）**

消息内容，不能为空

属性

**type** `string` **（必选）**

内容片段类型；`input_text` 或 `input_image`

**text** `string` **（条件必填）**

文本内容，最多 1,048,576 字符；同一项不能同时包含 `image_url`

**image\_url** `string` **（条件必填）**

图片 URL，最多 1,048,576 字符；同一项不能同时包含 `text`；不保证 URL 可访问

**metadata** `object / null` **（可选）**

元数据，字符串键值对，最多 16 项；key 最多 64 字符，value 最多 512 字符；value 不接受 `null`

**stream** `boolean` **（可选）**

是否返回 SSE 流，`true` 时创建响应直接返回 SSE 流，Session 进入 `idle` 或 `failed` 后结束，缺失为 `false`，`null` 不合法

**vault\_ids** `array<string> / null` **（可选）**

挂载的 Vault，最多 10 个，缺失或 `null` 为 `[]`

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/agents/sessions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": {
      "model": "qwen3.8-max",
      "instructions": "回答简洁。"
    },
    "environment": {"type": "none"},
    "input": "你好"
  }'
```

Python

```
session = client.beta.agents.sessions.create(
    agent={
        "model": "qwen3.8-max",
        "instructions": "回答简洁。",
    },
    environment={"type": "none"},
    input="你好",
)
print(session.id, session.status)
```

### Environment

写法

说明

`{"type":"none"}`

不创建沙箱，不提供 Shell、文件读写等内置工具

`{"type":"openai_hosted"}`

按请求内联配置创建托管环境

`{"type":"openai_hosted","environment_id":"..."}`

引用已创建的环境；不能同时追加 `files`、`skills` 等配置

`openai_hosted` 支持的字段、限制和异步准备行为见[环境](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-environment.md)。`self_hosted` 当前不支持。准备完成前引用该环境的 Session 可能创建失败；使用环境前先确认状态为 `ready`。

**说明**引用已有环境时，`vault_ids` 必须与环境创建时的 `vault_ids` 一致；不能在 Session 上追加新的 Vault。

### Agent 配置

`agent` 用于内联创建或覆盖已保存 Agent。同时提供 `agent_id` 时按顶层字段替换：省略的字段保持已保存值，显式 `null` 按字段规则处理；最终有效配置会再次执行与内联配置相同的预检。

同时提供的示例：`{"agent_id":"agent_xxx","agent":{"instructions":"只回复 OK"},"environment":{"type":"none"},"input":"只回复 OK"}`。

`agent.id` 由响应生成或来自已保存 Agent，不能在内联配置中指定。`agent.metadata`、`compaction`、`experimental` 等未知字段会被拒绝。不同类型的工具不得夹带其他分支字段；布尔字段的 `null` 不等价于缺失。

### Message 与 Content

`input` 为数组时，每项是一条 user 消息。`message` 和 `content` 的未知字段会被拒绝。

未知顶层字段会被拒绝。请求体上限 16 MiB；删除 `instructions` 后的 `agent` + `metadata` + `environment` 紧凑 JSON 上限 1,310,720 字节。

### 响应字段

字段不齐时为 `null`。 创建响应的 `status` 可以是 `in_progress`。HTTP `201` 表示 Session 和首轮输入已受理，不证明 Turn 成功；以 Turn 终态或 SSE 的 `agent.session.idle` 判断本轮结束。

**id** `string`

Session ID，继续对话时复用

**object** `string`

Session 对象类型，固定为 `agent.session`

**created\_at** `integer`

创建时间，Unix 秒

**last\_active\_at** `integer`

最近活动时间，Unix 秒；不是版本号或锁

**status** `string`

Session 状态：`idle`、`in_progress`、`requires_action`、`failed`

**agent** `object`

当前生效的 Agent 快照。

属性

**id** `string`

Agent ID；内联配置生成的是会话快照 ID，不是可复用的已保存 Agent，不能通过 Agent GET 查询

**model** `string`

模型 ID

**instructions** `string / null`

自定义指令

**name** `string / null`

展示名称

**reasoning** `object / null`

推理配置，包含 `effort`、`summary`

**text** `object / null`

文本输出配置；包含 `format` 和 `verbosity`

**tools** `array`

工具配置

**multi\_agent** `object / null`

子 Agent 配置；包含 `enabled`、`max_concurrent_subagents`

**environment** `object`

环境安全摘要；`type=none` 时只有 `type`。

属性

**type** `string`

环境类型；`none` 或 `openai_hosted`

**id** `string`

环境 ID，无权威来源时省略

**status** `string`

环境状态：无权威来源时省略

**environment\_template\_id** `string`

环境模板 ID；无权威来源时省略

**workspace\_directory** `string`

工作目录；无权威来源时省略

**error** `string / null`

环境错误说明；无权威来源时省略

**desktop** `object / null`

桌面配置；包含 `enabled`

**capability\_directories** `array<string> / null`

能力发现目录

**network** `object / null`

网络策略；包含 `access`、`allowed_domains`

**packages** `object / null`

包列表；包含 `npm`、`python`、`system`

**files** `array`

环境文件安全元数据

**skills** `array`

Skill 安全元数据

**plugins** `array`

插件信息，当前托管环境为 `[]`

**metadata** `object`

Session 元数据，空值为 `{}`

**vault\_ids** `array<string>`

创建时记录的 Vault ID

**required\_actions** `array`

需要客户端处理的 Function 调用；空时为 `[]`。

属性

**type** `string`

Item 类型，固定为 `function_call`

**turn\_id** `string`

公开 Turn ID

**call\_id** `string`

Function 调用 ID

**name** `string`

函数名

**arguments** `object`

已解析的调用参数

**error** `string / null`

Session 级错误说明，与 Turn 的结构化 error 不同

**usage** `object / null`

Token 用量。

属性

**input\_tokens** `integer`

输入 Token 数

**input\_tokens\_details** `object`

输入 Token 明细。

属性

**cached\_tokens** `integer`

命中缓存的输入 Token 数

**output\_tokens** `integer`

输出 Token 数

**output\_tokens\_details** `object`

输出 Token 明细。

属性

**reasoning\_tokens** `integer`

推理 Token 数

**total\_tokens** `integer`

总 Token 数

**spend\_control** `object`

费用控制，仅历史记录带值时返回；创建和更新接口不接受写入。

属性

**limit** `integer`

额度上限，单位为美分

**consumed** `integer / null`

已消耗额度，单位为美分

## 响应示例

```
{
  "id": "sess_xxx",
  "object": "agent.session",
  "created_at": 1794118835,
  "last_active_at": 1794118835,
  "status": "in_progress",
  "agent": {
    "id": "agent_xxx",
    "model": "qwen3.8-max",
    "instructions": "回答简洁。",
    "reasoning": {"effort": "none", "summary": "auto"},
    "text": {"format": {"type": "text"}, "verbosity": "medium"},
    "tools": [],
    "multi_agent": {"enabled": false, "max_concurrent_subagents": null},
    "name": null
  },
  "environment": {"type": "none"},
  "metadata": {},
  "required_actions": [],
  "vault_ids": [],
  "error": null,
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {"cached_tokens": 0},
    "output_tokens": 0,
    "output_tokens_details": {"reasoning_tokens": 0},
    "total_tokens": 0
  }
}
```

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `missing_required_parameter`

传入 `environment`，例如 `{"type":"none"}` 或 `{"type":"openai_hosted"}`

`400`

`invalid_request_error` / 具体 code 依字段而定

按条件补齐 `input`；没有 `agent_id` 时补齐 `agent.model`

`400`

`invalid_request_error` / `invalid_type`、`invalid_value`、`unknown_parameter`、`invalid_json`

删除未知字段，修正字段类型和枚举值，并发送合法 JSON

`400`

`invalid_request_error` / 具体 code 依字段而定

按字段说明缩短 `metadata`、`vault_ids` 或字符串字段

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在的资源 ID

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id`

`503`

`server_error` / 具体服务错误码

稍后重试；持续失败时提交工单并提供 `x-request-id`
