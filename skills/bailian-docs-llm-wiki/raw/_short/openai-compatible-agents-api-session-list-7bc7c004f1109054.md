# 列出 Session

分页列出当前工作空间中的 Session，可按 Agent 过滤。

## 接口

**GET** `/agents/sessions`

成功返回 `200` 和列表信封，`data` 为 Session 对象数组。

## 查询参数

**limit** `integer` **（可选）**

每页数量，默认 20，范围 `1..100`；空串或不在此范围返回 `400`

**order** `string` **（可选）**

排序方向，`asc` 或 `desc`，默认 `desc`；非法值返回 `400`

**after** `string` **（可选）**

资源 ID 游标，最多 256 字节且不能为空白；不包含游标项

**agent\_id** `string` **（可选）**

Agent ID 过滤条件，按已保存或内联 Agent ID 过滤，显式空值非法，重复传入返回 `400`

翻页时首次不传 `after`，后续传上一页的 `last_id`。列表按 `(created_at, 资源 ID)` 排序。`before` 等其他未知 Query 参数会被忽略，反向翻页请使用 `order` 和 `after`。

列表可能有短暂延迟，可能暂时看不到刚创建的 Session；需要确认最新状态时使用[获取 Session](raw/_short/openai-compatible-agents-api-session-get-87a5c7829bfca12d.md)。列表不提供全局快照或立即可见性保证。

## 请求示例

curl

```
curl -sS "$BASE_URL/agents/sessions?limit=20&order=desc&agent_id=agent_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
page = client.beta.agents.sessions.list(
    limit=20,
    order="desc",
    agent_id="agent_xxx",
)
for session in page.data:
    print(session.id, session.status)
```

### 响应字段

**object** `string`

列表对象类型，固定为 `list`

**data** `array`

当页 Session 对象，空时为 `[]`

**first\_id** `string / null`

当页首项 ID。空页为 `null`

**last\_id** `string / null`

当页末项 ID。空页为 `null`，后续 `after` 使用该值

**has\_more** `boolean`

当前检索方向是否还有下一页

### Session 字段

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

字段不齐时为 `null`。

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

按查询参数说明修正 `limit`、`order`、`agent_id`，并移除重复参数

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

确认父资源存在且属于当前工作空间；使用本集合上一页返回的 `last_id` 作为 `after`

`502`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id`
