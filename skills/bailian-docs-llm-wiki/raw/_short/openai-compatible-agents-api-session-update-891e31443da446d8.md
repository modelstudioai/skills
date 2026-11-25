# 更新 Session

更新 Session 的 metadata、模型、推理强度与服务档位，只影响后续 Turn。

<a id="接口"></a>

<a id="h-oa-session-update-endpoint"></a>

## 接口

**POST** `/agents/sessions/{session_id}`

成功返回 `200` 和更新后的完整 Session。更新只支持 `metadata`、`agent.model` 和 `agent.reasoning.effort`。

更新只影响后续 Turn，不改变正在执行的 Turn，也不回写已保存的 Agent。并发更新冲突时返回 `409 conflict_error`，重新读取后重试。

<table><tbody><tr><td><a id="h-oa-session-update-body"></a><h2>请求体</h2><p><strong>metadata</strong> <code>object / null</code> <strong>（可选）</strong></p><p>元数据，整体替换，缺失保持原值，<code>null</code> 或 <code>{}</code> 清空。最多 16 项，key 非空且不超过 64 字符，value 为字符串且不超过 512 字符</p><p><strong>agent</strong> <code>object</code> <strong>（可选）</strong></p><p>会话级设置，缺失保持原值，<code>null</code> 拒绝，<code>{}</code> 合法但不修改设置。未知字段拒绝</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>model</strong> <code>string</code> <strong>（可选）</strong></p><p>后续 Turn 使用的模型，缺失保持原值，<code>null</code> 或全空白拒绝。更新入口上限 1,048,576 字符，模型变更必须属于当前工作空间可用的模型</p><p><strong>reasoning</strong> <code>object</code> <strong>（可选）</strong></p><p>只能包含 <code>effort</code>，不能传 <code>summary</code>，缺失保持原值，<code>null</code> 拒绝</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>effort</strong> <code>string / null</code> <strong>（可选）</strong></p><p>推理强度，<code>none</code>、<code>minimal</code>、<code>low</code>、<code>medium</code>、<code>high</code>、<code>xhigh</code>、<code>max</code>、<code>ultra</code>；<code>null</code> 重置为模型默认值</p></div></section></div></section><p><code>metadata</code> 和 <code>agent</code> 至少出现一个。空请求体、JSON <code>null</code> 或整个请求体为 <code>{}</code> 时返回 <code>400</code>。</p><p><code>agent: {}</code> 本身合法，但不会修改任何设置。更新先校验设置，再读取和合并资源；非法设置与资源不存在同时发生时，可能先返回 <code>400</code>。</p></td><td><a id="h-oa-session-update-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/agents/sessions/sess_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;metadata&quot;: {&quot;source&quot;: &quot;updated&quot;},
    &quot;agent&quot;: {
      &quot;model&quot;: &quot;qwen3.8-max&quot;,
      &quot;reasoning&quot;: {&quot;effort&quot;: &quot;medium&quot;}
    }
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>session = client.beta.agents.sessions.update(
    &quot;sess_xxx&quot;,
    metadata={&quot;source&quot;: &quot;updated&quot;},
    agent={
        &quot;model&quot;: &quot;qwen3.8-max&quot;,
        &quot;reasoning&quot;: {&quot;effort&quot;: &quot;medium&quot;},
    },
)
print(session.status)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-session-update-response"></a><h3>响应字段</h3><p>返回更新后的完整 Session 对象。 字段不齐时为 <code>null</code>。</p><p><strong>id</strong> <code>string</code></p><p>Session ID，继续对话时复用</p><p><strong>object</strong> <code>string</code></p><p>Session 对象类型，固定为 <code>agent.session</code></p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>last_active_at</strong> <code>integer</code></p><p>最近活动时间，Unix 秒；不是版本号或锁</p><p><strong>status</strong> <code>string</code></p><p>Session 状态：<code>idle</code>、<code>in_progress</code>、<code>requires_action</code>、<code>failed</code></p><p><strong>agent</strong> <code>object</code></p><p>当前生效的 Agent 快照。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>id</strong> <code>string</code></p><p>Agent ID；内联配置生成的是会话快照 ID，不是可复用的已保存 Agent，不能通过 Agent GET 查询</p><p><strong>model</strong> <code>string</code></p><p>模型 ID</p><p><strong>instructions</strong> <code>string / null</code></p><p>自定义指令</p><p><strong>name</strong> <code>string / null</code></p><p>展示名称</p><p><strong>reasoning</strong> <code>object / null</code></p><p>推理配置，包含 <code>effort</code>、<code>summary</code></p><p><strong>text</strong> <code>object / null</code></p><p>文本输出配置；包含 <code>format</code> 和 <code>verbosity</code></p><p><strong>tools</strong> <code>array</code></p><p>工具配置</p><p><strong>multi_agent</strong> <code>object / null</code></p><p>子 Agent 配置；包含 <code>enabled</code>、<code>max_concurrent_subagents</code></p></div></section><p><strong>environment</strong> <code>object</code></p><p>环境安全摘要；<code>type=none</code> 时只有 <code>type</code>。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>环境类型；<code>none</code> 或 <code>openai_hosted</code></p><p><strong>id</strong> <code>string</code></p><p>环境 ID，无权威来源时省略</p><p><strong>status</strong> <code>string</code></p><p>环境状态：无权威来源时省略</p><p><strong>environment_template_id</strong> <code>string</code></p><p>环境模板 ID；无权威来源时省略</p><p><strong>workspace_directory</strong> <code>string</code></p><p>工作目录；无权威来源时省略</p><p><strong>error</strong> <code>string / null</code></p><p>环境错误说明；无权威来源时省略</p><p><strong>desktop</strong> <code>object / null</code></p><p>桌面配置；包含 <code>enabled</code></p><p><strong>capability_directories</strong> <code>array&lt;string&gt; / null</code></p><p>能力发现目录</p><p><strong>network</strong> <code>object / null</code></p><p>网络策略；包含 <code>access</code>、<code>allowed_domains</code></p><p><strong>packages</strong> <code>object / null</code></p><p>包列表；包含 <code>npm</code>、<code>python</code>、<code>system</code></p><p><strong>files</strong> <code>array</code></p><p>环境文件安全元数据</p><p><strong>skills</strong> <code>array</code></p><p>Skill 安全元数据</p><p><strong>plugins</strong> <code>array</code></p><p>插件信息，当前托管环境为 <code>[]</code></p></div></section><p><strong>metadata</strong> <code>object</code></p><p>Session 元数据，空值为 <code>{}</code></p><p><strong>vault_ids</strong> <code>array&lt;string&gt;</code></p><p>创建时记录的 Vault ID，不代表挂载已完成</p><p><strong>required_actions</strong> <code>array</code></p><p>需要客户端处理的 Function 调用；空时为 <code>[]</code>。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>Item 类型，固定为 <code>function_call</code></p><p><strong>turn_id</strong> <code>string</code></p><p>公开 Turn ID</p><p><strong>call_id</strong> <code>string</code></p><p>Function 调用 ID</p><p><strong>name</strong> <code>string</code></p><p>函数名</p><p><strong>arguments</strong> <code>object</code></p><p>已解析的调用参数</p></div></section><p><strong>error</strong> <code>string / null</code></p><p>Session 级错误说明，与 Turn 的结构化 error 不同</p><p><strong>usage</strong> <code>object / null</code></p><p>Token 用量。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数</p><p><strong>input_tokens_details</strong> <code>object</code></p><p>输入 Token 明细。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的输入 Token 数</p></div></section><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数</p><p><strong>output_tokens_details</strong> <code>object</code></p><p>输出 Token 明细。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>推理 Token 数</p></div></section><p><strong>total_tokens</strong> <code>integer</code></p><p>总 Token 数</p></div></section><p><strong>spend_control</strong> <code>object</code></p><p>费用控制，仅历史记录带值时返回；创建和更新接口不接受写入。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>limit</strong> <code>integer</code></p><p>额度上限，单位为美分</p><p><strong>consumed</strong> <code>integer / null</code></p><p>已消耗额度，单位为美分</p></div></section></td><td><a id="h-oa-session-update-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sess_xxx&quot;,
  &quot;object&quot;: &quot;agent.session&quot;,
  &quot;created_at&quot;: 1794118835,
  &quot;last_active_at&quot;: 1794119300,
  &quot;status&quot;: &quot;idle&quot;,
  &quot;agent&quot;: {
    &quot;id&quot;: &quot;agent_xxx&quot;,
    &quot;model&quot;: &quot;qwen3.8-max&quot;,
    &quot;instructions&quot;: &quot;回答简洁。&quot;,
    &quot;reasoning&quot;: {&quot;effort&quot;: &quot;medium&quot;, &quot;summary&quot;: &quot;auto&quot;},
    &quot;text&quot;: {&quot;format&quot;: {&quot;type&quot;: &quot;text&quot;}, &quot;verbosity&quot;: &quot;medium&quot;},
    &quot;tools&quot;: [],
    &quot;multi_agent&quot;: {&quot;enabled&quot;: false, &quot;max_concurrent_subagents&quot;: null},
    &quot;name&quot;: null
  },
  &quot;environment&quot;: {&quot;type&quot;: &quot;none&quot;},
  &quot;metadata&quot;: {&quot;source&quot;: &quot;updated&quot;},
  &quot;required_actions&quot;: [],
  &quot;vault_ids&quot;: [],
  &quot;error&quot;: null,
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 12,
    &quot;input_tokens_details&quot;: {&quot;cached_tokens&quot;: 0},
    &quot;output_tokens&quot;: 8,
    &quot;output_tokens_details&quot;: {&quot;reasoning_tokens&quot;: 0},
    &quot;total_tokens&quot;: 20
  }
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-session-update-errors"></a>

## 错误码

业务错误返回 `error` 对象，包含 `type`、`code`、`message` 和 `param`。常见错误如下：

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 至少传入 `metadata` 或 `agent` 之一，并发送合法 JSON 对象 |
| `400` | `invalid_request_error` / `unknown_parameter`、`invalid_type`、`invalid_value` | 删除未知字段，按字段说明修正类型和枚举值 |
| `400` | `invalid_request_error` / `object_above_max_properties`、`empty_property_name`、`property_name_above_max_length`、`string_above_max_length` | 按字段说明缩短 `metadata` 或字符串字段 |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中未归档且格式正确的 Session ID |
| `409` | `conflict_error` / `conflict_error` | 重新读取 Session 后重试 |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id` |
