# 提交 Event

向 Session 提交 user 消息、取消当前 Turn 或回填 Function 调用结果。

## 接口

`POST /agents/sessions/{session_id}/events`

成功返回 `202 Accepted`，Body 为空，响应头可能带 `x-request-id`。

`202` 表示持久接纳和投递已受理，不表示模型已经消费输入或 Turn 已完成。执行结果通过 SSE、Turn 终态和 Item 历史确认。

## 路径参数

**session\_id** `string` **（必选）**

Session ID，例如 `sess_xxx`

## 请求体

**events** `array<object>` **（必选）**

事件数组。空数组 `[]` 表示空批受理，不产生输入

根据 `type` 选择以下一种事件结构。

事件类型

agent.session.input.message

**type** `string` **（必选）**

固定为 `agent.session.input.message`。

**input** `array<object>` **（必选）**

user 消息数组，不能为空。

input 项

**role** `string` **（必选）**

消息角色，固定为 `user`。

**content** `array` **（必选）**

内容片段数组，不能为空。

content 项

**type** `string` **（必选）**

内容片段类型；`input_text` 或 `input_image`。

**text** `string` **（条件必填）**

文本内容。

**image\_url** `string` **（条件必填）**

图片地址。

```
{
  "type": "agent.session.input.message",
  "input": [{
    "role": "user",
    "content": [{"type": "input_text", "text": "继续补充说明。"}]
  }]
}
```

agent.session.input.cancel

**type** `string` **（必选）**

固定为 `agent.session.input.cancel`。只接受 `type`，不接受 `turn_id` 等其他字段。

```
{"type": "agent.session.input.cancel"}
```

agent.session.input.tool\_result

**type** `string` **（必选）**

固定为 `agent.session.input.tool_result`。

**turn\_id** `string` **（必选）**

来自 `required_actions` 的公开 Turn ID。

**call\_id** `string` **（必选）**

对应的 Function 调用 ID。

**success** `boolean` **（必选）**

调用是否成功。

**output** `string 或 array / null` **（条件必填）**

Function 输出；字符串，或 `input_text` / `input_image` 数组。

**error** `string / null` **（条件必填）**

失败信息。

```
{
  "type": "agent.session.input.tool_result",
  "turn_id": "turn_xxx",
  "call_id": "call_xxx",
  "success": true,
  "output": "已发货"
}
```

`message` 的 `input` 是数组，不是创建 Session 时的字符串简写。`cancel` 只取消当前正在执行的 Turn。不同分支携带其他分支字段或未知字段会被拒绝。

## 请求示例

curl

```
curl -X POST "$BASE_URL/agents/sessions/sess_xxx/events" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "OpenAI-Beta: agents=v1" \
  -d '{
    "events": [{
      "type": "agent.session.input.message",
      "input": [{
        "role": "user",
        "content": [{"type": "input_text", "text": "继续补充说明。"}]
      }]
    }]
  }'
```

Python

```
client.beta.agents.sessions.events.create(
    "sess_xxx",
    events=[{
        "type": "agent.session.input.message",
        "input": [{
            "role": "user",
            "content": [{"type": "input_text", "text": "继续补充说明。"}],
        }],
    }],
)
```

### Function Calling

模型发起 Function 调用后，Session 的 `required_actions` 会出现待处理项：

```
{
  "type": "function_call",
  "turn_id": "turn_xxx",
  "call_id": "call_xxx",
  "name": "lookup_order",
  "arguments": {"order_id": "A123"}
}
```

应用执行函数后，回填结果：

```
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

### 幂等

可以携带 `Idempotency-Key` Header：

-   Key 长度为 1–256 字符；空串或超长返回 `400`。
-   同一 Session、同一 Key、同一内容重试时复用受理结果，不重复触发已交付的输入。
-   同一 Key、不同内容返回 `409 conflict_error`。
-   仅包含 `cancel` 的批次是当前取消例外：同 Key 再次请求仍作用于当时的当前 Turn。
-   不携带 Key 时不提供请求级自动去重。
-   全部为 message 的批次按数组顺序合并为一次输入；混合批次逐项处理，后项语义失败不回滚前项已受理的效果。

## 响应示例

```
HTTP/1.1 202 Accepted
x-request-id: <request-id>
```

`202 Accepted`，无响应体。受理成功不代表工具结果已被模型消费，也不代表 Turn 已完成。

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `invalid_request_error`

修正请求体结构和事件内容；为 `Idempotency-Key` 传入 1–256 字符的非空值

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且未删除的 Session ID

`409`

`conflict_error` / `conflict_error`

确认资源当前状态；同一 `Idempotency-Key` 使用相同请求内容重试

`503`

`server_error` / `agents_api_upstream_unavailable`

稍后重试；持续失败时提交工单并提供 `x-request-id`
