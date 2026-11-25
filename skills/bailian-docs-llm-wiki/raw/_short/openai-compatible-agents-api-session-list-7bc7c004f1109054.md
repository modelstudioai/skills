# 列出 Session

分页列出当前工作空间中的 Session，可按 Agent 过滤。

<a id="接口"></a>

<a id="h-oa-session-list-endpoint"></a>

## 接口

**GET** `/agents/sessions`

成功返回 `200` 和列表信封，`data` 为 Session 对象数组。

<table><tbody><tr><td><a id="h-oa-session-list-query"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，默认 20，范围 <code>1..100</code>；空串或不在此范围返回 <code>400</code></p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code>；非法值返回 <code>400</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>资源 ID 游标，最多 256 字节且不能为空白；不包含游标项</p><p><strong>agent_id</strong> <code>string</code> <strong>（可选）</strong></p><p>Agent ID 过滤条件，按已保存或内联 Agent ID 过滤，显式空值非法，重复传入返回 <code>400</code></p><p>翻页时首次不传 <code>after</code>，后续传上一页的 <code>last_id</code>。列表按 <code>(created_at, 资源 ID)</code> 排序。<code>before</code> 等其他未知 Query 参数会被忽略，反向翻页请使用 <code>order</code> 和 <code>after</code>。</p><p>列表可能有短暂延迟，可能暂时看不到刚创建的 Session；需要确认最新状态时使用<a href="openai-compatible-agents-api-session-get-87a5c7829bfca12d.md">获取 Session</a>。列表不提供全局快照或立即可见性保证。</p></td><td><a id="h-oa-session-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/agents/sessions?limit=20&amp;order=desc&amp;agent_id=agent_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>page = client.beta.agents.sessions.list(
    limit=20,
    order=&quot;desc&quot;,
    agent_id=&quot;agent_xxx&quot;,
)
for session in page.data:
    print(session.id, session.status)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-session-list-response"></a><h3>响应字段</h3><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array</code></p><p>当页 Session 对象，空时为 <code>[]</code></p><p><strong>first_id</strong> <code>string / null</code></p><p>当页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当页末项 ID。空页为 <code>null</code>，后续 <code>after</code> 使用该值</p><p><strong>has_more</strong> <code>boolean</code></p><p>当前检索方向是否还有下一页</p><a id="h-oa-session-list-fields"></a><h3>Session 字段</h3><p><strong>id</strong> <code>string</code></p><p>Session ID，继续对话时复用</p><p><strong>object</strong> <code>string</code></p><p>Session 对象类型，固定为 <code>agent.session</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>last_active_at</strong> <code>integer</code></p><p>最近活动时间，Unix 秒；不是版本号或锁</p><p><strong>status</strong> <code>string</code></p><p>Session 状态：<code>idle</code>、<code>in_progress</code>、<code>requires_action</code>、<code>failed</code></p><p><strong>agent</strong> <code>object</code></p><p>当前生效的 Agent 快照。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>id</strong> <code>string</code></p><p>Agent ID；内联配置生成的是会话快照 ID，不是可复用的已保存 Agent，不能通过 Agent GET 查询</p><p><strong>model</strong> <code>string</code></p><p>模型 ID</p><p><strong>instructions</strong> <code>string / null</code></p><p>自定义指令</p><p><strong>name</strong> <code>string / null</code></p><p>展示名称</p><p><strong>reasoning</strong> <code>object / null</code></p><p>推理配置，包含 <code>effort</code>、<code>summary</code></p><p><strong>text</strong> <code>object / null</code></p><p>文本输出配置；包含 <code>format</code> 和 <code>verbosity</code></p><p><strong>tools</strong> <code>array</code></p><p>工具配置</p><p><strong>multi_agent</strong> <code>object / null</code></p><p>子 Agent 配置；包含 <code>enabled</code>、<code>max_concurrent_subagents</code></p></div></section><p><strong>environment</strong> <code>object</code></p><p>环境安全摘要；<code>type=none</code> 时只有 <code>type</code>。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>环境类型；<code>none</code> 或 <code>openai_hosted</code></p><p><strong>id</strong> <code>string</code></p><p>环境 ID，无权威来源时省略</p><p><strong>status</strong> <code>string</code></p><p>环境状态：无权威来源时省略</p><p><strong>environment_template_id</strong> <code>string</code></p><p>环境模板 ID；无权威来源时省略</p><p><strong>workspace_directory</strong> <code>string</code></p><p>工作目录；无权威来源时省略</p><p><strong>error</strong> <code>string / null</code></p><p>环境错误说明；无权威来源时省略</p><p><strong>desktop</strong> <code>object / null</code></p><p>桌面配置；包含 <code>enabled</code></p><p><strong>capability_directories</strong> <code>array&lt;string&gt; / null</code></p><p>能力发现目录</p><p><strong>network</strong> <code>object / null</code></p><p>网络策略；包含 <code>access</code>、<code>allowed_domains</code></p><p><strong>packages</strong> <code>object / null</code></p><p>包列表；包含 <code>npm</code>、<code>python</code>、<code>system</code></p><p><strong>files</strong> <code>array</code></p><p>环境文件安全元数据</p><p><strong>skills</strong> <code>array</code></p><p>Skill 安全元数据</p><p><strong>plugins</strong> <code>array</code></p><p>插件信息，当前托管环境为 <code>[]</code></p></div></section><p><strong>metadata</strong> <code>object</code></p><p>Session 元数据，空值为 <code>{}</code></p><p><strong>vault_ids</strong> <code>array&lt;string&gt;</code></p><p>创建时记录的 Vault ID，不代表挂载已完成</p><p><strong>required_actions</strong> <code>array</code></p><p>需要客户端处理的 Function 调用；空时为 <code>[]</code>。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>Item 类型，固定为 <code>function_call</code></p><p><strong>turn_id</strong> <code>string</code></p><p>公开 Turn ID</p><p><strong>call_id</strong> <code>string</code></p><p>Function 调用 ID</p><p><strong>name</strong> <code>string</code></p><p>函数名</p><p><strong>arguments</strong> <code>object</code></p><p>已解析的调用参数</p></div></section><p><strong>error</strong> <code>string / null</code></p><p>Session 级错误说明，与 Turn 的结构化 error 不同</p><p><strong>usage</strong> <code>object / null</code></p><p>Token 用量。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数</p><p><strong>input_tokens_details</strong> <code>object</code></p><p>输入 Token 明细。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的输入 Token 数</p></div></section><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数</p><p><strong>output_tokens_details</strong> <code>object</code></p><p>输出 Token 明细。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>推理 Token 数</p></div></section><p><strong>total_tokens</strong> <code>integer</code></p><p>总 Token 数</p></div></section><p><strong>spend_control</strong> <code>object</code></p><p>费用控制，仅历史记录带值时返回；创建和更新接口不接受写入。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>limit</strong> <code>integer</code></p><p>额度上限，单位为美分</p><p><strong>consumed</strong> <code>integer / null</code></p><p>已消耗额度，单位为美分</p></div></section><p>字段不齐时为 <code>null</code>。</p></td><td><a id="h-oa-session-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [],
  &quot;first_id&quot;: null,
  &quot;last_id&quot;: null,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-session-list-errors"></a>

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order`、`agent_id`，并移除重复参数 |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 确认父资源存在且属于当前工作空间；使用本集合上一页返回的 `last_id` 作为 `after` |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id` |
