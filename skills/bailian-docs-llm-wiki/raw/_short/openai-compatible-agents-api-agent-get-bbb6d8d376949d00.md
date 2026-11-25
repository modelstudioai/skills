# 获取 Agent

根据 Agent ID 返回完整的 Agent 配置。

<a id="接口"></a>

<a id="h-oa-agent-get-endpoint"></a>

## 接口

**GET** `/agents/{agent_id}`

成功返回 `200` 和完整 Agent 对象。

<table><tbody><tr><td><a id="h-oa-agent-get-params"></a><h2>路径参数</h2><p><strong>agent_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Agent ID，按不透明字符串使用</p><p>本接口没有 Query 参数。<code>agent_id</code> 格式错误、不存在、已删除或属于其他工作空间时返回 <code>404</code>。</p></td><td><a id="h-oa-agent-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/agents/agent_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>agent = client.beta.agents.retrieve(&quot;agent_xxx&quot;)
print(agent.id, agent.model)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-agent-get-response"></a><h3>响应字段</h3><p>未设置的可选字段可能返回 <code>null</code>。</p><p><strong>id</strong> <code>string</code></p><p>Agent ID，按不透明字符串使用</p><p><strong>object</strong> <code>string</code></p><p>Agent 对象类型，固定为 <code>agent</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间的 Unix 秒时间戳</p><p><strong>updated_at</strong> <code>integer</code></p><p>最近修改时间的 Unix 秒时间戳，不是版本号</p><p><strong>name</strong> <code>string / null</code></p><p>展示名称</p><p><strong>metadata</strong> <code>object / null</code></p><p>元数据，保存的字符串键值对</p><p><strong>model</strong> <code>string</code></p><p>保存的模型 ID</p><p><strong>reasoning</strong> <code>object / null</code></p><p>推理配置。两项均可为 <code>null</code>。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>effort</strong> <code>string / null</code></p><p>推理强度：<code>none</code>、<code>minimal</code>、<code>low</code>、<code>medium</code>、<code>high</code>、<code>xhigh</code>、<code>max</code></p><p><strong>summary</strong> <code>string / null</code></p><p>推理摘要：<code>concise</code>、<code>detailed</code>、<code>auto</code></p></div></section><p><strong>text</strong> <code>object / null</code></p><p>文本输出配置。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>format</strong> <code>object</code></p><p>输出格式。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong> <code>string / null</code></p><p>输出格式类型，固定为 <code>text</code></p></div></section><p><strong>verbosity</strong> <code>string / null</code></p><p>输出详细程度，<code>low</code>、<code>medium</code>、<code>high</code></p></div></section><p><strong>instructions</strong> <code>string / null</code></p><p>保存的自定义指令</p><p><strong>tools</strong> <code>array / null</code></p><p>保存的工具配置；每个分支只返回本分支字段</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>function</strong> <code>object</code></p><p>Function 工具配置，返回 <code>name</code>、<code>description</code>、<code>parameters</code></p><p><strong>mcp</strong> <code>object</code></p><p>MCP 工具配置，返回 <code>server_label</code>、<code>transport</code>、<code>allowed_tools</code>、<code>required</code>、<code>connection_origin</code>；<code>transport</code> 为 <code>http</code> 或 <code>stdio</code></p><p><strong>web_search</strong> <code>object</code></p><p>Web Search 工具配置，返回 <code>type</code> 和已保存的配置</p></div></section><p><strong>multi_agent</strong> <code>object / null</code></p><p>子 Agent 配置。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>enabled</strong> <code>boolean</code></p><p>是否启用子 Agent 工具</p><p><strong>max_concurrent_subagents</strong> <code>integer / null</code></p><p>最大并发子 Agent 数；不补默认值</p></div></section></td><td><a id="h-oa-agent-get-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;agent_xxx&quot;,
  &quot;object&quot;: &quot;agent&quot;,
  &quot;created_at&quot;: 1794117521,
  &quot;updated_at&quot;: 1794117521,
  &quot;name&quot;: &quot;quickstart-agent&quot;,
  &quot;metadata&quot;: null,
  &quot;model&quot;: &quot;qwen3.8-max&quot;,
  &quot;reasoning&quot;: null,
  &quot;text&quot;: null,
  &quot;instructions&quot;: &quot;回答简洁，只输出必要信息。&quot;,
  &quot;tools&quot;: null,
  &quot;multi_agent&quot;: null
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-agent-get-errors"></a>

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Agent ID |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
