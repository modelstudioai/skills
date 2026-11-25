# 思维链摘要与加密

Qwen4-Max 返回可展示的思维链摘要和完整思维链的密文，用于多轮对话中恢复历史思考。

适用模型：`qwen4-max`。

<a id="工作原理"></a>

<a id="how-it-works"></a>

## 工作原理

默认返回完整思维链。开启本功能后，原始思维链不再以明文返回，改为返回摘要与完整密文。摘要用于展示，密文用于恢复历史思考。

摘要与加密同时开启。未产生思考或加密失败时，密文可能缺失；摘要可能缺失或不完整，接口仍不返回原始思维链。

每轮请求都需开启本功能，并原样回传历史密文，以恢复对应的历史思考。

文本和多模态输入使用相同参数；密文只保存思维链，图片、视频等历史输入仍需保留。多段思考或工具调用时，每段密文随所属 assistant 消息分别保存。

Chat Completions 和 DashScope 需开启 `enable_thinking=true`；回传密文续推时设置 `preserve_thinking=true`。Responses 和 Anthropic Messages 使用各自的思考参数。

<a id="开启方式"></a>

<a id="enable"></a>

## 开启方式

以下示例使用北京地域。将 `WorkspaceId` 替换为真实业务空间 ID，并配置 `DASHSCOPE_API_KEY`。

| 接口 | 开启参数 | 摘要字段 | 密文字段 |
| --- | --- | --- | --- |
| Chat Completions | `thinking_display="summarized"` | `choices[i].message.reasoning_content` | `choices[i].message.encrypted_content` |
| Responses | `reasoning.summary="auto"` | `summary[].text` | `encrypted_content` |
| Anthropic Messages | `thinking.display="summarized"` | `thinking` | `signature` |
| DashScope | `parameters.thinking_display="summarized"` | `output.choices[i].message.reasoning_content` | `output.choices[i].message.encrypted_content` |

<a id="sec-tabs"></a>

<a id="chat-completions"></a>

<a id="chat-completions-h4"></a>

#### Chat Completions

<a id="chat"></a>

<a id="code-block"></a>

```bash
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen4-max",
  "messages": [
    {
      "role": "user",
      "content": "请计算 17×23。"
    }
  ],
  "enable_thinking": true,
  "thinking_display": "summarized",
  "preserve_thinking": true
}'
```

<a id="responses"></a>

<a id="responses-h4"></a>

#### Responses

<a id="responses-2"></a>

<a id="code-block-2"></a>

```bash
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen4-max",
  "input": "请计算 17×23。",
  "reasoning": {
    "summary": "auto"
  }
}'
```

<a id="anthropic-messages"></a>

<a id="anthropic-messages-h4"></a>

#### Anthropic Messages

<a id="anthropic"></a>

<a id="code-block-3"></a>

```bash
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages" \
  -H "x-api-key: $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen4-max",
  "max_tokens": 2048,
  "thinking": {
    "type": "enabled",
    "budget_tokens": 1024,
    "display": "summarized"
  },
  "messages": [
    {
      "role": "user",
      "content": "请计算 17×23。"
    }
  ]
}'
```

<a id="dashscope"></a>

<a id="dashscope-h4"></a>

#### DashScope

<a id="dashscope-2"></a>

<a id="code-block-4"></a>

```bash
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen4-max",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "text": "请计算 17×23。"
          }
        ]
      }
    ]
  },
  "parameters": {
    "result_format": "message",
    "incremental_output": false,
    "enable_thinking": true,
    "thinking_display": "summarized",
    "preserve_thinking": true
  }
}'
```

<a id="返回与流式处理"></a>

<a id="streaming"></a>

## 返回与流式处理

Chat Completions 流式顺序：`choices[i].delta.reasoning_content` 摘要增量 → 独立 `encrypted_content` 密文帧 → 正文或工具调用 → 结束。非流式字段位于 `choices[i].message`。密文一次返回，不要因文本为空而过滤密文帧，也不要为密文单独创建 assistant 消息。

Responses 的 reasoning item 包含 `summary`（`summary_text` 元素）和 `encrypted_content`。摘要按文本增量返回，密文在 reasoning item 完成事件及最终 response 中返回；可从完成快照补齐密文，不要重复追加摘要。

Anthropic Messages 的 thinking block 包含 `thinking` 摘要和 `signature` 密文。流式先返回 `thinking_delta`，再返回完整 `signature_delta`，关闭 thinking block 后返回正文或工具调用；未产生思考或加密失败时 signature 可能为空字符串。

DashScope 字段位于 `output.choices[i].message`，流式顺序与 Chat Completions 一致。密文放在 `encrypted_content`，不能放进 `content[].text`。中间帧的 `finish_reason` 为字符串 `"null"`，最终为 `"stop"`；usage 为累计值，不要重复累加。

<a id="多轮对话"></a>

<a id="multi-turn"></a>

## 多轮对话

回传历史时保留完整密文；摘要可省略，Responses 的 `summary` 可设为空数组。

<a id="sec-tabs-2"></a>

<a id="chat-completions-2"></a>

<a id="chat-completions-2-h4"></a>

#### Chat Completions

OpenAI Python SDK 的非标准参数 `enable_thinking`、`thinking_display`、`preserve_thinking` 通过 `extra_body` 传入。

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
questions = [
    "请计算 17×23。",
    "再加 9。"
]
history = []

for turn, question in enumerate(questions, start=1):
    history.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model="qwen4-max",
        messages=history,
        max_tokens=8192,
        stream=False,
        extra_body={
            "enable_thinking": True,
            "thinking_display": "summarized",
            "preserve_thinking": True,
        },
    )
    assistant_message = response.choices[0].message.model_dump(exclude_none=True)
    history.append(assistant_message)
    print(f"Turn {turn}")
    print("Summary:", assistant_message.get("reasoning_content", ""))
    print("Answer:", assistant_message["content"])
```

<a id="fig-code-group-node-js-tab"></a>

Node.js

<a id="code-code-group-node-js"></a>

```javascript
const questions = [
    "请计算 17×23。",
    "再加 9。"
];
const history = [];
const endpoint = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions";

for (const [index, question] of questions.entries()) {
  history.push({ role: "user", content: question });
  const httpResponse = await fetch(endpoint, {
    method: "POST",
    headers: { "Authorization": `Bearer ${process.env.DASHSCOPE_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: "qwen4-max", messages: history, max_tokens: 8192, stream: false, enable_thinking: true, thinking_display: "summarized", preserve_thinking: true }),
  });
  if (!httpResponse.ok) throw new Error(await httpResponse.text());
  const response = await httpResponse.json();
  const assistantMessage = response.choices[0].message;
  history.push(assistantMessage);
  console.log(`Turn ${index + 1}`);
  console.log("Summary:", assistantMessage.reasoning_content ?? "");
  console.log("Answer:", assistantMessage.content);
}
```

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
set -euo pipefail

history='[]'
questions=(
  '请计算 17×23。'
  '再加 9。'
)

for question in "${questions[@]}"; do
  history=$(jq --arg question "$question" '. + [{role: "user", content: $question}]' <<< "$history")
  request=$(jq -n --argjson history "$history" '{model: "qwen4-max", messages: $history, max_tokens: 8192, stream: false, enable_thinking: true, thinking_display: "summarized", preserve_thinking: true}')
  response=$(curl --fail-with-body -sS "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    --data "$request")
  history=$(jq -n --argjson history "$history" --argjson response "$response" \
    '$history + [$response.choices[0].message]')
  printf '%s\n' "$response" | jq '.choices[0].message | {summary: .reasoning_content, answer: .content}'
done
```

<a id="responses-3"></a>

<a id="responses-3-h4"></a>

#### Responses

设置 `reasoning.summary="auto"` 开启摘要与加密。下例使用 `store=false`，由客户端保存历史。

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-python-tab"></a>

Python

<a id="code-code-group-2-python"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
questions = [
    "请计算 17×23。",
    "再加 9。"
]
history = []

for turn, question in enumerate(questions, start=1):
    history.append({"role": "user", "content": question})
    response = client.responses.create(
        model="qwen4-max",
        input=history,
        reasoning={"effort": "medium", "summary": "auto"},
        max_output_tokens=8192,
        store=False,
        stream=False,
    )
    output_items = [item.model_dump(exclude_none=True) for item in response.output]
    history.extend(output_items)
    print(f"Turn {turn}")
    for item in output_items:
        if item["type"] == "reasoning":
            print("Summary:", "".join(part["text"] for part in (item.get("summary") or [])))
    print("Answer:", response.output_text)
```

<a id="fig-code-group-2-node-js-tab"></a>

Node.js

<a id="code-code-group-2-node-js"></a>

```javascript
const questions = [
    "请计算 17×23。",
    "再加 9。"
];
const history = [];
const endpoint = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses";

for (const [index, question] of questions.entries()) {
  history.push({ role: "user", content: question });
  const httpResponse = await fetch(endpoint, {
    method: "POST",
    headers: { "Authorization": `Bearer ${process.env.DASHSCOPE_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: "qwen4-max", input: history, reasoning: { effort: "medium", summary: "auto" }, max_output_tokens: 8192, store: false, stream: false }),
  });
  if (!httpResponse.ok) throw new Error(await httpResponse.text());
  const response = await httpResponse.json();
  history.push(...response.output);
  console.log(`Turn ${index + 1}`);
  for (const item of response.output) {
    if (item.type === "reasoning") console.log("Summary:", (item.summary ?? []).map(part => part.text).join(""));
    if (item.type === "message") console.log("Answer:", item.content.filter(part => part.type === "output_text").map(part => part.text).join(""));
  }
}
```

<a id="fig-code-group-2-curl-tab"></a>

curl

<a id="code-code-group-2-curl"></a>

```bash
set -euo pipefail

history='[]'
questions=(
  '请计算 17×23。'
  '再加 9。'
)

for question in "${questions[@]}"; do
  history=$(jq --arg question "$question" '. + [{role: "user", content: $question}]' <<< "$history")
  request=$(jq -n --argjson history "$history" '{model: "qwen4-max", input: $history, reasoning: {effort: "medium", summary: "auto"}, max_output_tokens: 8192, store: false, stream: false}')
  response=$(curl --fail-with-body -sS "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    --data "$request")
  history=$(jq -n --argjson history "$history" --argjson response "$response" \
    '$history + $response.output')
  printf '%s\n' "$response" | jq '{summary: [.output[] | select(.type == "reasoning") | .summary[].text], answer: [.output[] | select(.type == "message") | .content[] | select(.type == "output_text") | .text]}'
done
```

<a id="anthropic-messages-2"></a>

<a id="anthropic-messages-2-h4"></a>

#### Anthropic Messages

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-python-tab"></a>

Python

<a id="code-code-group-3-python"></a>

```python
import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
)
questions = [
    "请计算 17×23。",
    "再加 9。"
]
history = []

for turn, question in enumerate(questions, start=1):
    history.append({"role": "user", "content": question})
    response = client.messages.create(
        model="qwen4-max",
        messages=history,
        max_tokens=8192,
        thinking={"type": "enabled", "budget_tokens": 4096, "display": "summarized"},
        stream=False,
    )
    content_blocks = [block.model_dump(exclude_none=True) for block in response.content]
    history.append({"role": "assistant", "content": content_blocks})
    print(f"Turn {turn}")
    for block in content_blocks:
        if block["type"] == "thinking":
            print("Summary:", block["thinking"])
        elif block["type"] == "text":
            print("Answer:", block["text"])
```

<a id="fig-code-group-3-node-js-tab"></a>

Node.js

<a id="code-code-group-3-node-js"></a>

```javascript
const questions = [
    "请计算 17×23。",
    "再加 9。"
];
const history = [];
const endpoint = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages";

for (const [index, question] of questions.entries()) {
  history.push({ role: "user", content: question });
  const httpResponse = await fetch(endpoint, {
    method: "POST",
    headers: { "x-api-key": process.env.DASHSCOPE_API_KEY, "anthropic-version": "2023-06-01", "Content-Type": "application/json" },
    body: JSON.stringify({ model: "qwen4-max", messages: history, max_tokens: 8192, thinking: { type: "enabled", budget_tokens: 4096, display: "summarized" }, stream: false }),
  });
  if (!httpResponse.ok) throw new Error(await httpResponse.text());
  const response = await httpResponse.json();
  history.push({ role: "assistant", content: response.content });
  console.log(`Turn ${index + 1}`);
  for (const block of response.content) {
    if (block.type === "thinking") console.log("Summary:", block.thinking);
    if (block.type === "text") console.log("Answer:", block.text);
  }
}
```

<a id="fig-code-group-3-curl-tab"></a>

curl

<a id="code-code-group-3-curl"></a>

```bash
set -euo pipefail

history='[]'
questions=(
  '请计算 17×23。'
  '再加 9。'
)

for question in "${questions[@]}"; do
  history=$(jq --arg question "$question" '. + [{role: "user", content: $question}]' <<< "$history")
  request=$(jq -n --argjson history "$history" '{model: "qwen4-max", messages: $history, max_tokens: 8192, thinking: {type: "enabled", budget_tokens: 4096, display: "summarized"}, stream: false}')
  response=$(curl --fail-with-body -sS "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages" \
    -H "x-api-key: $DASHSCOPE_API_KEY" -H "anthropic-version: 2023-06-01" \
    -H "Content-Type: application/json" \
    --data "$request")
  history=$(jq -n --argjson history "$history" --argjson response "$response" \
    '$history + [{role: "assistant", content: $response.content}]')
  printf '%s\n' "$response" | jq '{summary: [.content[] | select(.type == "thinking") | .thinking], answer: [.content[] | select(.type == "text") | .text]}'
done
```

<a id="dashscope-3"></a>

<a id="dashscope-3-h4"></a>

#### DashScope

<a id="fig-code-group-4"></a>

<a id="fig-code-group-4-python-tab"></a>

Python

<a id="code-code-group-4-python"></a>

```python
import json
import os
from urllib.request import Request, urlopen

questions = [
    "请计算 17×23。",
    "再加 9。"
]
history = []

for turn, question in enumerate(questions, start=1):
    history.append({"role": "user", "content": [{"text": question}]})
    body = {
        "model": "qwen4-max",
        "input": {"messages": history},
        "parameters": {
            "result_format": "message",
            "incremental_output": False,
            "enable_thinking": True,
            "thinking_display": "summarized",
            "preserve_thinking": True,
            "max_tokens": 8192,
        },
    }
    request = Request(
        "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + os.environ["DASHSCOPE_API_KEY"],
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=120) as http_response:
        response = json.load(http_response)
    assistant_message = response["output"]["choices"][0]["message"]
    history.append(assistant_message)
    print(f"Turn {turn}")
    print("Summary:", assistant_message.get("reasoning_content", ""))
    print("Answer:", "".join(part.get("text", "") for part in assistant_message["content"]))
```

<a id="fig-code-group-4-node-js-tab"></a>

Node.js

<a id="code-code-group-4-node-js"></a>

```javascript
const questions = [
    "请计算 17×23。",
    "再加 9。"
];
const history = [];
const endpoint = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation";

for (const [index, question] of questions.entries()) {
  history.push({ role: "user", content: [{ text: question }] });
  const httpResponse = await fetch(endpoint, {
    method: "POST",
    headers: { "Authorization": `Bearer ${process.env.DASHSCOPE_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: "qwen4-max", input: { messages: history }, parameters: { result_format: "message", incremental_output: false, enable_thinking: true, thinking_display: "summarized", preserve_thinking: true, max_tokens: 8192 } }),
  });
  if (!httpResponse.ok) throw new Error(await httpResponse.text());
  const response = await httpResponse.json();
  const assistantMessage = response.output.choices[0].message;
  history.push(assistantMessage);
  console.log(`Turn ${index + 1}`);
  console.log("Summary:", assistantMessage.reasoning_content ?? "");
  console.log("Answer:", assistantMessage.content.map(part => part.text ?? "").join(""));
}
```

<a id="fig-code-group-4-curl-tab"></a>

curl

<a id="code-code-group-4-curl"></a>

```bash
set -euo pipefail

history='[]'
questions=(
  '请计算 17×23。'
  '再加 9。'
)

for question in "${questions[@]}"; do
  history=$(jq --arg question "$question" '. + [{role: "user", content: [{text: $question}]}]' <<< "$history")
  request=$(jq -n --argjson history "$history" '{model: "qwen4-max", input: {messages: $history}, parameters: {result_format: "message", incremental_output: false, enable_thinking: true, thinking_display: "summarized", preserve_thinking: true, max_tokens: 8192}}')
  response=$(curl --fail-with-body -sS "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    --data "$request")
  history=$(jq -n --argjson history "$history" --argjson response "$response" \
    '$history + [$response.output.choices[0].message]')
  printf '%s\n' "$response" | jq '.output.choices[0].message | {summary: .reasoning_content, answer: [.content[].text]}'
done
```

<a id="计费说明"></a>

<a id="billing"></a>

## 计费说明

本功能不额外收费，按模型原有输入、输出 Token 计费规则计费。
