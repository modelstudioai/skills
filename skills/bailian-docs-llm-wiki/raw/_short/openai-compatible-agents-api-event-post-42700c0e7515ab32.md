# 提交 Event

向 Session 提交 user 消息、取消当前 Turn 或回填 Function 调用结果。

<a id="接口"></a>

<a id="h-oa-event-post-endpoint"></a>

## 接口

`POST /agents/sessions/{session_id}/events`

成功返回 `202 Accepted`，Body 为空，响应头可能带 `x-request-id`。

`202` 表示持久接纳和投递已受理，不表示模型已经消费输入或 Turn 已完成。执行结果通过 SSE、Turn 终态和 Item 历史确认。

<table><tbody><tr><td><a id="h-oa-event-post-params"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Session ID，例如 <code>sess_xxx</code></p><a id="h-oa-event-post-body"></a><h2>请求体</h2><p><strong>events</strong> <code>array&lt;object&gt;</code> <strong>（必选）</strong></p><p>事件数组。空数组 <code>[]</code> 表示空批受理，不产生输入</p><p>根据 <code>type</code> 选择以下一种事件结构。</p><a id="accordion-事件类型"></a><section><p>事件类型</p><div><a id="accordion-agent-session-input-message"></a><section><p>agent.session.input.message</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>agent.session.input.message</code>。</p><p><strong>input</strong> <code>array&lt;object&gt;</code> <strong>（必选）</strong></p><p>user 消息数组，不能为空。</p><a id="accordion-input-项"></a><section><p>input 项</p><div><p><strong>role</strong> <code>string</code> <strong>（必选）</strong></p><p>消息角色，固定为 <code>user</code>。</p><p><strong>content</strong> <code>array</code> <strong>（必选）</strong></p><p>内容片段数组，不能为空。</p><a id="accordion-content-项"></a><section><p>content 项</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>内容片段类型；<code>input_text</code> 或 <code>input_image</code>。</p><p><strong>text</strong> <code>string</code> <strong>（条件必填）</strong></p><p>文本内容。</p><p><strong>image_url</strong> <code>string</code> <strong>（条件必填）</strong></p><p>图片地址。</p></div></section></div></section><a id="code-block"></a><pre class="language-json"><code>{
  &quot;type&quot;: &quot;agent.session.input.message&quot;,
  &quot;input&quot;: [{
    &quot;role&quot;: &quot;user&quot;,
    &quot;content&quot;: [{&quot;type&quot;: &quot;input_text&quot;, &quot;text&quot;: &quot;继续补充说明。&quot;}]
  }]
}
</code></pre></div></section><a id="accordion-agent-session-input-cancel"></a><section><p>agent.session.input.cancel</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>agent.session.input.cancel</code>。只接受 <code>type</code>，不接受 <code>turn_id</code> 等其他字段。</p><a id="code-block-2"></a><pre class="language-json"><code>{&quot;type&quot;: &quot;agent.session.input.cancel&quot;}
</code></pre></div></section><a id="accordion-agent-session-input-tool-result"></a><section><p>agent.session.input.tool_result</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>agent.session.input.tool_result</code>。</p><p><strong>turn_id</strong> <code>string</code> <strong>（必选）</strong></p><p>来自 <code>required_actions</code> 的公开 Turn ID。</p><p><strong>call_id</strong> <code>string</code> <strong>（必选）</strong></p><p>对应的 Function 调用 ID。</p><p><strong>success</strong> <code>boolean</code> <strong>（必选）</strong></p><p>调用是否成功。</p><p><strong>output</strong> <code>string 或 array / null</code> <strong>（条件必填）</strong></p><p>Function 输出；字符串，或 <code>input_text</code> / <code>input_image</code> 数组。</p><p><strong>error</strong> <code>string / null</code> <strong>（条件必填）</strong></p><p>失败信息。</p><a id="code-block-3"></a><pre class="language-json"><code>{
  &quot;type&quot;: &quot;agent.session.input.tool_result&quot;,
  &quot;turn_id&quot;: &quot;turn_xxx&quot;,
  &quot;call_id&quot;: &quot;call_xxx&quot;,
  &quot;success&quot;: true,
  &quot;output&quot;: &quot;已发货&quot;
}
</code></pre></div></section></div></section><p><code>message</code> 的 <code>input</code> 是数组，不是创建 Session 时的字符串简写。<code>cancel</code> 只取消当前正在执行的 Turn。不同分支携带其他分支字段或未知字段会被拒绝。</p></td><td><a id="h-oa-event-post-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$BASE_URL/agents/sessions/sess_xxx/events&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  -d '{
    &quot;events&quot;: [{
      &quot;type&quot;: &quot;agent.session.input.message&quot;,
      &quot;input&quot;: [{
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [{&quot;type&quot;: &quot;input_text&quot;, &quot;text&quot;: &quot;继续补充说明。&quot;}]
      }]
    }]
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>client.beta.agents.sessions.events.create(
    &quot;sess_xxx&quot;,
    events=[{
        &quot;type&quot;: &quot;agent.session.input.message&quot;,
        &quot;input&quot;: [{
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{&quot;type&quot;: &quot;input_text&quot;, &quot;text&quot;: &quot;继续补充说明。&quot;}],
        }],
    }],
)
</code></pre></div></div></td></tr></tbody></table>

<a id="function-calling"></a>

<a id="h-oa-event-post-function"></a>

### Function Calling

模型发起 Function 调用后，Session 的 `required_actions` 会出现待处理项：

<a id="code-block-4"></a>

```json
{
  "type": "function_call",
  "turn_id": "turn_xxx",
  "call_id": "call_xxx",
  "name": "lookup_order",
  "arguments": {"order_id": "A123"}
}
```

应用执行函数后，回填结果：

<a id="code-block-5"></a>

```json
{
  "events": [{
    "type": "agent.session.input.tool_result",
    "turn_id": "turn_xxx",
    "call_id": "call_xxx",
    "success": true,
    "output": "已发货"
  }]
}
```

`arguments` 已经解析为对象，不需要再次按 JSON 字符串解析。客户端重启后先获取 Session，读取 `required_actions` 再继续。

<a id="幂等"></a>

<a id="h-oa-event-post-idempotency"></a>

### 幂等

可以携带 `Idempotency-Key` Header：

-   Key 长度为 1–256 字符；空串或超长返回 `400`。
-   同一 Session、同一 Key、同一内容重试时复用受理结果，不重复触发已交付的输入。
-   同一 Key、不同内容返回 `409 conflict_error`。
-   仅包含 `cancel` 的批次是当前取消例外：同 Key 再次请求仍作用于当时的当前 Turn。
-   不携带 Key 时不提供请求级自动去重。
-   全部为 message 的批次按数组顺序合并为一次输入；混合批次逐项处理，后项语义失败不回滚前项已受理的效果。

<a id="响应示例"></a>

<a id="h-oa-event-post-resp"></a>

## 响应示例

<a id="code-block-6"></a>

```text
HTTP/1.1 202 Accepted
x-request-id: <request-id>
```

`202 Accepted`，无响应体。受理成功不代表工具结果已被模型消费，也不代表 Turn 已完成。

<a id="错误码"></a>

<a id="h-oa-event-post-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 修正请求体结构和事件内容；为 `Idempotency-Key` 传入 1–256 字符的非空值 |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Session ID |
| `409` | `conflict_error` / `conflict_error` | 确认资源当前状态；同一 `Idempotency-Key` 使用相同请求内容重试 |
| `503` | `server_error` / `agents_api_upstream_unavailable` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
