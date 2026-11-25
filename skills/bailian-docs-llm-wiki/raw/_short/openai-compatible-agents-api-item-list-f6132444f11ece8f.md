# 列出 Item

分页查询根 Agent 跨 Turn 的 Item 历史，用于结果核对和断线恢复。

<a id="接口"></a>

<a id="h-oa-item-list-endpoint"></a>

## 接口

`GET /agents/sessions/{session_id}/items`

返回根 Agent 跨 Turn 的 Item，不混入子 Agent 自己的历史。成功返回 `200`。查询不启动模型、不恢复执行，也不创建资源。

<table><tbody><tr><td><a id="h-oa-item-list-path"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Session ID，例如 <code>sess_xxx</code></p><a id="h-oa-item-list-query"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，默认 20，范围 1–100</p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code>；不包含游标项</p></td><td><a id="h-oa-item-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl --get &quot;$BASE_URL/agents/sessions/sess_xxx/items&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  --data-urlencode &quot;limit=20&quot; \
  --data-urlencode &quot;order=asc&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>items = client.beta.agents.sessions.items.list(
    &quot;sess_xxx&quot;, limit=20, order=&quot;asc&quot;
)
for item in items.data:
    print(item.type, item.id)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-item-list-response"></a><h3>响应字段</h3><p>列表信封：</p><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array&lt;Item&gt;</code></p><p>当页 Item；空时为 <code>[]</code></p><p><strong>first_id</strong> <code>string / null</code></p><p>当页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当页末项 ID。空页为 <code>null</code>。后续 <code>after</code> 使用该值</p><p><strong>has_more</strong> <code>boolean</code></p><p>当前检索方向是否还有下一页</p></td><td><a id="h-oa-item-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;msg_xxx&quot;,
      &quot;turn_id&quot;: &quot;turn_xxx&quot;,
      &quot;type&quot;: &quot;message&quot;,
      &quot;status&quot;: &quot;completed&quot;,
      &quot;role&quot;: &quot;assistant&quot;,
      &quot;phase&quot;: &quot;final_answer&quot;,
      &quot;content&quot;: [{&quot;type&quot;: &quot;output_text&quot;, &quot;text&quot;: &quot;完成&quot;}]
    }
  ],
  &quot;first_id&quot;: &quot;msg_xxx&quot;,
  &quot;last_id&quot;: &quot;msg_xxx&quot;,
  &quot;has_more&quot;: false
}
</code></pre><a id="code-block-2"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [],
  &quot;first_id&quot;: null,
  &quot;last_id&quot;: null,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="item-类型"></a>

<a id="h-oa-item-list-types"></a>

## Item 类型

每个 Item 都有 `id`、`turn_id` 和 `type`，业务字段平铺在对象顶层。

| `type` | 字段 |
| --- | --- |
| `message` | `status`（output 状态）、`role`（`user` / `assistant`）、`phase`（`commentary` / `final_answer` / `null`）、`content`（内容片段数组） |
| `reasoning` | `status`、`summary`（`type=summary_text` 的片段数组） |
| `function_call` | `status`、`call_id`、`name`、`arguments`（任意 JSON，可省略） |
| `function_call_output` | `status`、`call_id`、`output`（内容数组或 `null`；以字符串提交工具结果时，读取时会归一化为数组）、`error`（`string / null`） |
| `command_execution` | `status`、`command`、`cwd`、`duration_ms`、`exit_code`、`output` |
| `mcp_call` | `status`、`server_label`、`name`、`arguments`、`output`、`error` |
| `web_search_call` | `status`、`action`（`search`、`open_page`、`find_in_page` 或 `other`） |
| `agent_message` | `sender_agent_id`、`recipient_agent_id`、`content` |
| `create_subagent_call` | `status`、`agent_id`、`content`、`model`、`reasoning_effort` |
| `send_subagent_input_call` | `status`、`sender_agent_id`、`recipient_agent_id`、`content` |
| `resume_subagent_call` | `status`、`sender_agent_id`、`recipient_agent_id` |
| `wait_for_subagents_call` | `status`、`sender_agent_id`、`recipient_agent_ids` |
| `interrupt_subagent_call` | `status`、`sender_agent_id`、`recipient_agent_id` |
| `close_subagent_call` | `status`、`sender_agent_id`、`recipient_agent_id` |

内容片段按 `type` 区分：`input_text`、`output_text` 包含 `text`；`input_image` 包含 `image_url`；`encrypted_content` 不是可展示文本。

持久 Item 采用终结内容。SSE 的 `item.added` 可展示进行中状态，实时未完成 Item 不保证可在列表查询到。列表可能有短暂延迟，刚创建的数据可能暂时不可见。

<a id="错误码"></a>

<a id="h-oa-item-list-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order`；使用本集合上一页返回的 `last_id` 作为 `after` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Session ID |
| `502` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供响应头中的 `x-request-id` |
