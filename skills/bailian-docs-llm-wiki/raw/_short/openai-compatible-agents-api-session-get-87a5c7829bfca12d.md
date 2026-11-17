# 获取 Session

根据 Session ID 返回会话状态、Agent 快照、环境摘要与 Token 用量。

## 接口

**GET** `/agents/sessions/{session_id}`

成功返回 `200` 和完整 Session 对象。

## 路径参数

**session\_id** `string` **（必选）**

Session ID，按不透明字符串使用

本接口没有 Query 参数。`session_id` 格式错误、不存在、已归档或属于其他工作空间时返回 `404`。

## 请求示例

curl

```
curl -sS "$BASE_URL/agents/sessions/sess_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
session = client.beta.agents.sessions.retrieve("sess_xxx")
print(session.id, session.status)
```

### 响应字段

字段不齐时为 `null`。 `status=idle` 或 HTTP `200` 不充分证明上一轮 Turn 成功；需要结合 Turn 终态判断。`usage` 要求相关计数齐全，否则整个字段为 `null`。

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

创建时记录的 Vault ID，不代表挂载已完成

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
  "last_active_at": 1794118900,
  "status": "idle",
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
    "input_tokens": 12,
    "input_tokens_details": {"cached_tokens": 0},
    "output_tokens": 8,
    "output_tokens_details": {"reasoning_tokens": 0},
    "total_tokens": 20
  }
}
```

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

按路径参数格式传入有效值

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中未归档且格式正确的 Session ID

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id`
