# 创建 Session

创建 Session，绑定 Agent 与运行环境，并可提交首轮输入。

<a id="接口"></a>

<a id="h-oa-session-create-endpoint"></a>

## 接口

**POST** `/agents/sessions`

非流式请求返回 `201` JSON；`stream=true` 时返回 `201 text/event-stream`。创建返回 `201` 表示 Session 和首轮输入已受理，不表示 Turn 已执行完成。

<table><tbody><tr><td><a id="h-oa-session-create-body"></a><h2>请求体</h2><p><strong>environment</strong> <code>object</code> <strong>（必选）</strong></p><p>运行环境，见下文</p><p><strong>agent_id</strong> <code>string / null</code> <strong>（条件必填）</strong></p><p>已保存 Agent ID，最多 64 字符</p><p><strong>agent</strong> <code>object</code> <strong>（条件必填）</strong></p><p>内联 Agent 配置；与 <code>agent_id</code> 同时提供时作为会话级覆盖，未覆盖字段沿用已保存值</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>model</strong> <code>string</code> <strong>（条件必填）</strong></p><p>模型 ID；内联创建必填；引用已保存 Agent 时可继承。创建预检最多 256 字符，必须命中当前工作空间可用的模型。可选模型见<a href="openai-compatible-agents-api-agent-create-49e111e036159fc7.md#h-oa-agent-create-models">创建 Agent 的可选模型</a>。</p><p><strong>instructions</strong> <code>string / null</code> <strong>（可选）</strong></p><p>系统指令，最多 1,048,576 Unicode 字符；执行时合并到系统提示词</p><p><strong>name</strong> <code>string / null</code> <strong>（可选）</strong></p><p>展示名称，不参与执行配置</p><a id="accordion-reasoning"></a><section><p>reasoning</p><div><p><strong>effort</strong> <code>string / null</code> <strong>（可选）</strong></p><p>推理强度，<code>none</code>、<code>minimal</code>、<code>low</code>、<code>medium</code>、<code>high</code>、<code>xhigh</code>、<code>max</code>、<code>ultra</code>；未指定时返回 <code>none</code></p><p><strong>summary</strong> <code>string / null</code> <strong>（可选）</strong></p><p>推理摘要类型，<code>auto</code>、<code>concise</code>、<code>detailed</code>、<code>none</code>；未指定时返回 <code>auto</code>。字符串 <code>none</code> 与 JSON <code>null</code> 不同</p></div></section><a id="accordion-text"></a><section><p>text</p><div><p><strong>format</strong> <code>object / null</code> <strong>（可选）</strong></p><p>文本格式配置，只接受 <code>type: text</code>，未知字段拒绝，缺失或 <code>null</code> 为 <code>{&quot;type&quot;:&quot;text&quot;}</code></p><p><strong>verbosity</strong> <code>string / null</code> <strong>（可选）</strong></p><p>输出详细程度，只接受 <code>medium</code>，缺失或 <code>null</code> 为 <code>medium</code></p></div></section><p><strong>tools</strong> <code>array</code> <strong>（可选）</strong></p><p>工具列表，缺失为空列表，显式 <code>null</code> 不接受。<code>function</code> 最多 32 个，MCP 最多 16 个</p><a id="accordion-属性-2"></a><section><p>属性</p><div><a id="accordion-function"></a><section><p>function</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>工具类型，固定为 <code>function</code></p><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>函数名称，1..64 字节，字符集 <code>A-Za-z0-9_.:-</code>；同一 Agent 内不能重复</p><p><strong>description</strong> <code>string</code> <strong>（必选）</strong></p><p>函数说明，去除空白后非空，不超过 1024 字节</p><p><strong>parameters</strong> <code>object</code> <strong>（必选）</strong></p><p>参数定义；必须是 <code>type: object</code> 的 JSON Schema</p></div></section><a id="accordion-mcp"></a><section><p>mcp</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>工具类型，固定为 <code>mcp</code></p><p><strong>server_label</strong> <code>string</code> <strong>（必选）</strong></p><p>MCP 服务标识，1..64 字节，同一 Agent 内唯一</p><p><strong>transport</strong> <code>object</code> <strong>（必选）</strong></p><p>HTTP 或 stdio 传输配置</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>传输类型，<code>http</code> 或 <code>stdio</code></p><p><strong>server_url</strong> <code>string</code> <strong>（条件必填）</strong></p><p>MCP 服务地址；<code>service</code> 只接受百炼定位 URL（<code>/api/v1/mcps/{code}/mcp</code>）；<code>environment</code> 接受环境可达的普通 HTTP 地址</p><p><strong>headers</strong> <code>object&lt;string,string&gt; / null</code> <strong>（可选）</strong></p><p>附加 HTTP 请求头</p><p><strong>authorization</strong> <code>string / null</code> <strong>（可选）</strong></p><p>只用于 <code>connection_origin=environment</code> 的 HTTP 分支</p><p><strong>command</strong> <code>string</code> <strong>（条件必填）</strong></p><p>启动命令</p><p><strong>cwd</strong> <code>string</code> <strong>（条件必填）</strong></p><p>绝对路径；stdio 必须有环境</p><p><strong>args</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>命令参数</p></div></section><p><strong>allowed_tools</strong> <code>array&lt;string&gt; / null</code> <strong>（可选）</strong></p><p>允许调用的工具名列表；<code>null</code> 表示不过滤</p><p><strong>connection_origin</strong> <code>string</code> <strong>（可选）</strong></p><p>连接来源，<code>service</code> 或 <code>environment</code>，默认 <code>service</code></p><p><strong>required</strong> <code>boolean</code> <strong>（可选）</strong></p><p>是否要求 MCP 初始化成功</p></div></section><a id="accordion-web-search"></a><section><p>web_search</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>工具类型，固定为 <code>web_search</code></p></div></section></div></section><p><strong>multi_agent</strong> <code>object / null</code> <strong>（可选）</strong></p><p>多 Agent 配置，缺失或 <code>null</code> 为禁用；对象存在时 <code>enabled</code> 可省略，默认 <code>false</code>，显式 <code>null</code> 拒绝</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>max_concurrent_subagents</strong> <code>integer</code> <strong>（可选）</strong></p><p>最大并发 Subagent 数，显式值要求 <code>enabled=true</code> 且为 <code>1..32</code>，显式 <code>null</code> 拒绝；启用时缺失默认 6，禁用时返回 <code>null</code></p></div></section></div></section><p><strong>input</strong> <code>string 或 array / null</code> <strong>（条件必填）</strong></p><p>首轮输入。字符串是单条 user 文本消息的简写；空字符串会被拒绝</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>role</strong> <code>string</code> <strong>（必选）</strong></p><p>消息角色，固定为 <code>user</code></p><p><strong>type</strong> <code>string</code> <strong>（可选）</strong></p><p>消息类型，显式值只能是 <code>message</code></p><p><strong>content</strong> <code>array</code> <strong>（必选）</strong></p><p>消息内容，不能为空</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>内容片段类型；<code>input_text</code> 或 <code>input_image</code></p><p><strong>text</strong> <code>string</code> <strong>（条件必填）</strong></p><p>文本内容，最多 1,048,576 字符；同一项不能同时包含 <code>image_url</code></p><p><strong>image_url</strong> <code>string</code> <strong>（条件必填）</strong></p><p>图片 URL，最多 1,048,576 字符；同一项不能同时包含 <code>text</code>；不保证 URL 可访问</p></div></section></div></section><p><strong>metadata</strong> <code>object / null</code> <strong>（可选）</strong></p><p>元数据，字符串键值对，最多 16 项；key 最多 64 字符，value 最多 512 字符；value 不接受 <code>null</code></p><p><strong>stream</strong> <code>boolean</code> <strong>（可选）</strong></p><p>是否返回 SSE 流，<code>true</code> 时创建响应直接返回 SSE 流，Session 进入 <code>idle</code> 或 <code>failed</code> 后结束，缺失为 <code>false</code>，<code>null</code> 不合法</p><p><strong>vault_ids</strong> <code>array&lt;string&gt; / null</code> <strong>（可选）</strong></p><p>挂载的 Vault，最多 10 个，缺失或 <code>null</code> 为 <code>[]</code></p></td><td><a id="h-oa-session-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/agents/sessions&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;agent&quot;: {
      &quot;model&quot;: &quot;qwen3.8-max&quot;,
      &quot;instructions&quot;: &quot;回答简洁。&quot;
    },
    &quot;environment&quot;: {&quot;type&quot;: &quot;none&quot;},
    &quot;input&quot;: &quot;你好&quot;
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>session = client.beta.agents.sessions.create(
    agent={
        &quot;model&quot;: &quot;qwen3.8-max&quot;,
        &quot;instructions&quot;: &quot;回答简洁。&quot;,
    },
    environment={&quot;type&quot;: &quot;none&quot;},
    input=&quot;你好&quot;,
)
print(session.id, session.status)
</code></pre></div></div></td></tr></tbody></table>

<a id="environment"></a>

<a id="h-oa-session-create-environment"></a>

### Environment

| 写法 | 说明 |
| --- | --- |
| `{"type":"none"}` | 不创建沙箱，不提供 Shell、文件读写等内置工具 |
| `{"type":"openai_hosted"}` | 按请求内联配置创建托管环境 |
| `{"type":"openai_hosted","environment_id":"..."}` | 引用已创建的环境；不能同时追加 `files`、`skills` 等配置 |

`openai_hosted` 支持的字段、限制和异步准备行为见[环境](../application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-environment.md)。`self_hosted` 当前不支持。准备完成前引用该环境的 Session 可能创建失败；使用环境前先确认状态为 `ready`。

> **说明**
>
> 引用已有环境时，`vault_ids` 必须与环境创建时的 `vault_ids` 一致；不能在 Session 上追加新的 Vault。

<a id="agent-配置"></a>

<a id="h-oa-session-create-agent"></a>

### Agent 配置

`agent` 用于内联创建或覆盖已保存 Agent。同时提供 `agent_id` 时按顶层字段替换：省略的字段保持已保存值，显式 `null` 按字段规则处理；最终有效配置会再次执行与内联配置相同的预检。

同时提供的示例：`{"agent_id":"agent_xxx","agent":{"instructions":"只回复 OK"},"environment":{"type":"none"},"input":"只回复 OK"}`。

`agent.id` 由响应生成或来自已保存 Agent，不能在内联配置中指定。`agent.metadata`、`compaction`、`experimental` 等未知字段会被拒绝。不同类型的工具不得夹带其他分支字段；布尔字段的 `null` 不等价于缺失。

<a id="message-与-content"></a>

<a id="h-oa-session-create-message"></a>

### Message 与 Content

`input` 为数组时，每项是一条 user 消息。`message` 和 `content` 的未知字段会被拒绝。

未知顶层字段会被拒绝。请求体上限 16 MiB；删除 `instructions` 后的 `agent` + `metadata` + `environment` 紧凑 JSON 上限 1,310,720 字节。

<table><tbody><tr><td><a id="h-oa-session-create-response"></a><h3>响应字段</h3><p>字段不齐时为 <code>null</code>。 创建响应的 <code>status</code> 可以是 <code>in_progress</code>。HTTP <code>201</code> 表示 Session 和首轮输入已受理，不证明 Turn 成功；以 Turn 终态或 SSE 的 <code>agent.session.idle</code> 判断本轮结束。</p><p><strong>id</strong> <code>string</code></p><p>Session ID，继续对话时复用</p><p><strong>object</strong> <code>string</code></p><p>Session 对象类型，固定为 <code>agent.session</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>last_active_at</strong> <code>integer</code></p><p>最近活动时间，Unix 秒；不是版本号或锁</p><p><strong>status</strong> <code>string</code></p><p>Session 状态：<code>idle</code>、<code>in_progress</code>、<code>requires_action</code>、<code>failed</code></p><p><strong>agent</strong> <code>object</code></p><p>当前生效的 Agent 快照。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>id</strong> <code>string</code></p><p>Agent ID；内联配置生成的是会话快照 ID，不是可复用的已保存 Agent，不能通过 Agent GET 查询</p><p><strong>model</strong> <code>string</code></p><p>模型 ID</p><p><strong>instructions</strong> <code>string / null</code></p><p>自定义指令</p><p><strong>name</strong> <code>string / null</code></p><p>展示名称</p><p><strong>reasoning</strong> <code>object / null</code></p><p>推理配置，包含 <code>effort</code>、<code>summary</code></p><p><strong>text</strong> <code>object / null</code></p><p>文本输出配置；包含 <code>format</code> 和 <code>verbosity</code></p><p><strong>tools</strong> <code>array</code></p><p>工具配置</p><p><strong>multi_agent</strong> <code>object / null</code></p><p>子 Agent 配置；包含 <code>enabled</code>、<code>max_concurrent_subagents</code></p></div></section><p><strong>environment</strong> <code>object</code></p><p>环境安全摘要；<code>type=none</code> 时只有 <code>type</code>。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>环境类型；<code>none</code> 或 <code>openai_hosted</code></p><p><strong>id</strong> <code>string</code></p><p>环境 ID，无权威来源时省略</p><p><strong>status</strong> <code>string</code></p><p>环境状态：无权威来源时省略</p><p><strong>environment_template_id</strong> <code>string</code></p><p>环境模板 ID；无权威来源时省略</p><p><strong>workspace_directory</strong> <code>string</code></p><p>工作目录；无权威来源时省略</p><p><strong>error</strong> <code>string / null</code></p><p>环境错误说明；无权威来源时省略</p><p><strong>desktop</strong> <code>object / null</code></p><p>桌面配置；包含 <code>enabled</code></p><p><strong>capability_directories</strong> <code>array&lt;string&gt; / null</code></p><p>能力发现目录</p><p><strong>network</strong> <code>object / null</code></p><p>网络策略；包含 <code>access</code>、<code>allowed_domains</code></p><p><strong>packages</strong> <code>object / null</code></p><p>包列表；包含 <code>npm</code>、<code>python</code>、<code>system</code></p><p><strong>files</strong> <code>array</code></p><p>环境文件安全元数据</p><p><strong>skills</strong> <code>array</code></p><p>Skill 安全元数据</p><p><strong>plugins</strong> <code>array</code></p><p>插件信息，当前托管环境为 <code>[]</code></p></div></section><p><strong>metadata</strong> <code>object</code></p><p>Session 元数据，空值为 <code>{}</code></p><p><strong>vault_ids</strong> <code>array&lt;string&gt;</code></p><p>创建时记录的 Vault ID</p><p><strong>required_actions</strong> <code>array</code></p><p>需要客户端处理的 Function 调用；空时为 <code>[]</code>。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>Item 类型，固定为 <code>function_call</code></p><p><strong>turn_id</strong> <code>string</code></p><p>公开 Turn ID</p><p><strong>call_id</strong> <code>string</code></p><p>Function 调用 ID</p><p><strong>name</strong> <code>string</code></p><p>函数名</p><p><strong>arguments</strong> <code>object</code></p><p>已解析的调用参数</p></div></section><p><strong>error</strong> <code>string / null</code></p><p>Session 级错误说明，与 Turn 的结构化 error 不同</p><p><strong>usage</strong> <code>object / null</code></p><p>Token 用量。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数</p><p><strong>input_tokens_details</strong> <code>object</code></p><p>输入 Token 明细。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的输入 Token 数</p></div></section><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数</p><p><strong>output_tokens_details</strong> <code>object</code></p><p>输出 Token 明细。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>推理 Token 数</p></div></section><p><strong>total_tokens</strong> <code>integer</code></p><p>总 Token 数</p></div></section><p><strong>spend_control</strong> <code>object</code></p><p>费用控制，仅历史记录带值时返回；创建和更新接口不接受写入。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>limit</strong> <code>integer</code></p><p>额度上限，单位为美分</p><p><strong>consumed</strong> <code>integer / null</code></p><p>已消耗额度，单位为美分</p></div></section></td><td><a id="h-oa-session-create-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sess_xxx&quot;,
  &quot;object&quot;: &quot;agent.session&quot;,
  &quot;created_at&quot;: 1794118835,
  &quot;last_active_at&quot;: 1794118835,
  &quot;status&quot;: &quot;in_progress&quot;,
  &quot;agent&quot;: {
    &quot;id&quot;: &quot;agent_xxx&quot;,
    &quot;model&quot;: &quot;qwen3.8-max&quot;,
    &quot;instructions&quot;: &quot;回答简洁。&quot;,
    &quot;reasoning&quot;: {&quot;effort&quot;: &quot;none&quot;, &quot;summary&quot;: &quot;auto&quot;},
    &quot;text&quot;: {&quot;format&quot;: {&quot;type&quot;: &quot;text&quot;}, &quot;verbosity&quot;: &quot;medium&quot;},
    &quot;tools&quot;: [],
    &quot;multi_agent&quot;: {&quot;enabled&quot;: false, &quot;max_concurrent_subagents&quot;: null},
    &quot;name&quot;: null
  },
  &quot;environment&quot;: {&quot;type&quot;: &quot;none&quot;},
  &quot;metadata&quot;: {},
  &quot;required_actions&quot;: [],
  &quot;vault_ids&quot;: [],
  &quot;error&quot;: null,
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 0,
    &quot;input_tokens_details&quot;: {&quot;cached_tokens&quot;: 0},
    &quot;output_tokens&quot;: 0,
    &quot;output_tokens_details&quot;: {&quot;reasoning_tokens&quot;: 0},
    &quot;total_tokens&quot;: 0
  }
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-session-create-errors"></a>

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `missing_required_parameter` | 传入 `environment`，例如 `{"type":"none"}` 或 `{"type":"openai_hosted"}` |
| `400` | `invalid_request_error` / 具体 code 依字段而定 | 按条件补齐 `input`；没有 `agent_id` 时补齐 `agent.model` |
| `400` | `invalid_request_error` / `invalid_type`、`invalid_value`、`unknown_parameter`、`invalid_json` | 删除未知字段，修正字段类型和枚举值，并发送合法 JSON |
| `400` | `invalid_request_error` / 具体 code 依字段而定 | 按字段说明缩短 `metadata`、`vault_ids` 或字符串字段 |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在的资源 ID |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id` |
| `503` | `server_error` / 具体服务错误码 | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
