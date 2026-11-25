# 创建 Agent

创建一个可复用的 Agent 配置，保存模型、指令、工具与多 Agent 设置。

<a id="接口"></a>

<a id="h-oa-agent-create-endpoint"></a>

## 接口

**POST** `/agents`

成功返回 `201` 和完整 Agent 对象。创建只保存配置，不启动 Session、模型或 MCP 服务；相同请求体重复提交会创建新资源。

<table><tbody><tr><td><a id="h-oa-agent-create-body"></a><h2>请求体</h2><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型 ID，必须命中当前工作空间可用的模型，否则返回 <code>404 model_not_found</code>。可选模型见<a href="#h-oa-agent-create-models">可选模型</a>。</p><p><strong>name</strong> <code>string / null</code> <strong>（可选）</strong></p><p>展示名称，最多 128 字符。</p><p><strong>instructions</strong> <code>string / null</code> <strong>（可选）</strong></p><p>追加到 Agent 默认指令的自定义指令，最多 1,048,576 字符。</p><p><strong>metadata</strong> <code>object / null</code> <strong>（可选）</strong></p><p>元数据，字符串键值对；建议最多 16 项，key 建议最多 64 字符，value 建议最多 512 字符。全部值必须是字符串。</p><p><strong>reasoning</strong> <code>object / null</code> <strong>（可选）</strong></p><p>推理配置，包含以下字段。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>effort</strong> <code>string / null</code> <strong>（可选）</strong></p><p>推理强度：<code>none</code>、<code>minimal</code>、<code>low</code>、<code>medium</code>、<code>high</code>、<code>xhigh</code>、<code>max</code>。</p><p><strong>summary</strong> <code>string / null</code> <strong>（可选）</strong></p><p>推理摘要：<code>concise</code>、<code>detailed</code>、<code>auto</code>。</p></div></section><p><strong>text</strong> <code>object / null</code> <strong>（可选）</strong></p><p>文本输出配置，包含以下字段。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><a id="accordion-format"></a><section><p>format</p><div><p><strong>type</strong> <code>string</code> <strong>（条件必填）</strong></p><p>输出格式类型，固定为 <code>text</code>。</p></div></section><p><strong>verbosity</strong> <code>string / null</code> <strong>（可选）</strong></p><p>输出详细程度，<code>low</code>、<code>medium</code>、<code>high</code>；Session 执行侧当前只接受 <code>medium</code>。</p></div></section><p><strong>tools</strong> <code>array / null</code> <strong>（可选）</strong></p><p>工具配置。每个工具必须提供 <code>type</code>，当前支持 <code>function</code>、<code>mcp</code>、<code>web_search</code>。创建只保存配置，不代表工具可执行。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><a id="accordion-function"></a><section><p>function</p><div><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>函数名称</p><p><strong>description</strong> <code>string / null</code> <strong>（必选）</strong></p><p>函数说明，可以传 <code>null</code></p><p><strong>parameters</strong> <code>object</code> <strong>（必选）</strong></p><p>函数入参 JSON Schema，必须声明 <code>type: object</code></p></div></section><a id="accordion-mcp"></a><section><p>mcp</p><div><p><strong>server_label</strong> <code>string</code> <strong>（必选）</strong></p><p>MCP 服务标识</p><p><strong>transport</strong> <code>object</code> <strong>（必选）</strong></p><p>传输配置，见下方分支</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>传输类型，<code>http</code> 或 <code>stdio</code></p><p><strong>server_url</strong> <code>string / null</code> <strong>（条件必填）</strong></p><p>MCP 服务地址</p><p><strong>headers</strong> <code>object&lt;string,string&gt; / null</code> <strong>（可选）</strong></p><p>附加 HTTP 请求头，不要放密钥</p><p><strong>command</strong> <code>string</code> <strong>（条件必填）</strong></p><p>启动命令</p><p><strong>cwd</strong> <code>string</code> <strong>（条件必填）</strong></p><p>工作目录，必须是绝对路径，路径段不能是 <code>.</code> 或 <code>..</code></p><p><strong>args</strong> <code>array&lt;string&gt; / null</code> <strong>（可选）</strong></p><p>命令参数</p></div></section><p><strong>allowed_tools</strong> <code>array&lt;string&gt; / null</code> <strong>（可选）</strong></p><p>允许调用的工具名列表；<code>null</code> 表示不过滤</p><p><strong>required</strong> <code>boolean</code> <strong>（可选）</strong></p><p>是否要求 MCP 初始化成功</p><p><strong>connection_origin</strong> <code>string / null</code> <strong>（可选）</strong></p><p>连接来源，<code>service</code> 或 <code>environment</code>，默认 <code>service</code></p></div></section><a id="accordion-web-search"></a><section><p>web_search</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>工具类型，固定为 <code>web_search</code></p></div></section></div></section><p><strong>multi_agent</strong> <code>object / null</code> <strong>（可选）</strong></p><p>子 Agent 配置，包含以下字段。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>enabled</strong> <code>boolean</code> <strong>（必选）</strong></p><p>是否启用子 Agent 工具；父对象存在时必填。</p><p><strong>max_concurrent_subagents</strong> <code>integer / null</code> <strong>（可选）</strong></p><p>并发子 Agent 上限；执行侧当前支持 <code>1..32</code>，默认 6。</p></div></section><p>未知顶层字段不会报错，可能被过滤并记录，不能以请求未报错判断字段已经生效。</p></td><td><a id="h-oa-agent-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/agents&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;model&quot;: &quot;qwen3.8-max&quot;,
    &quot;name&quot;: &quot;support-agent&quot;,
    &quot;instructions&quot;: &quot;回答简洁，必要时给出操作步骤。&quot;,
    &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;}
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>agent = client.beta.agents.create(
    model=&quot;qwen3.8-max&quot;,
    name=&quot;support-agent&quot;,
    instructions=&quot;回答简洁，必要时给出操作步骤。&quot;,
    metadata={&quot;team&quot;: &quot;support&quot;},
)
print(agent.id)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-agent-create-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Agent ID，按不透明字符串使用。</p><p><strong>object</strong> <code>string</code></p><p>Agent 对象类型，固定为 <code>agent</code>。</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间的 Unix 秒时间戳。</p><p><strong>updated_at</strong> <code>integer</code></p><p>最近修改时间的 Unix 秒时间戳，不是版本号。</p><p><strong>name</strong> <code>string / null</code></p><p>展示名称。</p><p><strong>metadata</strong> <code>object / null</code></p><p>元数据，保存的字符串键值对。</p><p><strong>model</strong> <code>string</code></p><p>保存的模型 ID。</p><p><strong>reasoning</strong> <code>object / null</code></p><p>推理配置。两项均可为 <code>null</code>。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>effort</strong> <code>string / null</code></p><p>推理强度：<code>none</code>、<code>minimal</code>、<code>low</code>、<code>medium</code>、<code>high</code>、<code>xhigh</code>、<code>max</code></p><p><strong>summary</strong> <code>string / null</code></p><p>推理摘要：<code>concise</code>、<code>detailed</code>、<code>auto</code></p></div></section><p><strong>text</strong> <code>object / null</code></p><p>文本输出配置。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>format</strong> <code>object</code></p><p>输出格式。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>type</strong> <code>string / null</code></p><p>输出格式类型，固定为 <code>text</code></p></div></section><p><strong>verbosity</strong> <code>string / null</code></p><p>输出详细程度，<code>low</code>、<code>medium</code>、<code>high</code></p></div></section><p><strong>instructions</strong> <code>string / null</code></p><p>保存的自定义指令。</p><p><strong>tools</strong> <code>array / null</code></p><p>保存的工具配置；每个分支只返回本分支字段</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>function</strong> <code>object</code></p><p>Function 工具配置，返回 <code>name</code>、<code>description</code>、<code>parameters</code></p><p><strong>mcp</strong> <code>object</code></p><p>MCP 工具配置，返回 <code>server_label</code>、<code>transport</code>、<code>allowed_tools</code>、<code>required</code>、<code>connection_origin</code>；<code>transport</code> 为 <code>http</code> 或 <code>stdio</code></p><p><strong>web_search</strong> <code>object</code></p><p>Web Search 工具配置，返回 <code>type</code> 和已保存的配置</p></div></section><p><strong>multi_agent</strong> <code>object / null</code></p><p>子 Agent 配置。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>enabled</strong> <code>boolean</code></p><p>是否启用子 Agent 工具</p><p><strong>max_concurrent_subagents</strong> <code>integer / null</code></p><p>最大并发子 Agent 数；不补默认值</p></div></section></td><td><a id="h-oa-agent-create-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;agent_xxx&quot;,
  &quot;object&quot;: &quot;agent&quot;,
  &quot;created_at&quot;: 1794117521,
  &quot;updated_at&quot;: 1794117521,
  &quot;name&quot;: &quot;support-agent&quot;,
  &quot;metadata&quot;: {&quot;team&quot;: &quot;support&quot;},
  &quot;model&quot;: &quot;qwen3.8-max&quot;,
  &quot;reasoning&quot;: null,
  &quot;text&quot;: null,
  &quot;instructions&quot;: &quot;回答简洁，必要时给出操作步骤。&quot;,
  &quot;tools&quot;: null,
  &quot;multi_agent&quot;: null
}
</code></pre></td></tr></tbody></table>

<a id="可选模型"></a>

<a id="h-oa-agent-create-models"></a>

## 可选模型

`model` 支持以下模型：

| 品牌 | 模型 ID | 模型能力 |
| --- | --- | --- |
| 千问 | qwen4-max | 推理模型、视觉理解、文本生成 |
| 千问 | qwen3.8-max | 推理模型、视觉理解、文本生成 |
| 千问 | qwen3.7-max | 推理模型、文本生成 |
| 千问 | qwen3.7-plus | 推理模型、视觉理解、文本生成 |
| 千问 | qwen3.6-plus | 推理模型、视觉理解、文本生成 |
| DeepSeek | deepseek-v4-pro | 推理模型、文本生成 |
| 智谱 AI | glm-5.3 | 推理模型、文本生成 |
| 智谱 AI | glm-5.2 | 推理模型、文本生成 |
| 月之暗面 | kimi-k3 | 推理模型、视觉理解、文本生成 |

具备视觉理解能力的模型可处理创建会话时传入的图片，详见[创建会话](openai-compatible-agents-api-session-create-82108dd4f418e8ad.md)。

> **说明**
>
> 模型列表持续更新，以控制台创建 Agent 时的下拉列表为准。

<a id="错误码"></a>

<a id="h-oa-agent-create-errors"></a>

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按请求体说明补齐 `model`、修正字段类型和枚举、满足工具跨字段约束，并发送合法 JSON |
| `400` | `invalid_request_error` / `string_above_max_length` | 将 `instructions` 缩短到 1,048,576 字符以内 |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `invalid_request_error` / `model_not_found` | 改为当前工作空间可用的模型 ID |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |

鉴权、工作空间路由和限流错误可能由网关直接返回，结构可能与业务错误不同。
