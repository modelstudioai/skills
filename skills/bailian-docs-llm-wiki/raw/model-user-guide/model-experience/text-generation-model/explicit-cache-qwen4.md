# 显式缓存（Qwen4）

仅适用于 Qwen4 系列模型的显式缓存。通过自动缓存或缓存断点指定需要复用的输入前缀，并按 5 分钟或 1 小时设置缓存有效期，减少重复计算，降低延迟和输入成本。

在多轮对话、长文档问答、Agent 等场景中，连续请求往往包含大量相同的开头内容，例如系统提示词、工具说明或参考文档。使用显式缓存（Qwen4）后，有效期内的后续请求可以直接读取这部分内容的缓存，无需重复计算，从而降低响应延迟和输入成本。

显式缓存通过缓存断点指定需要复用的内容前缀，命中是确定的：只要前缀完全相同且在有效期内，后续请求就能读取缓存。系统自动识别公共前缀的[隐式缓存](context-cache.md#2317ea09cfxok)不保证命中。

Qwen4 在基础用法之上提供自动缓存和缓存有效期（TTL）两项进阶用法，详见[进阶用法](#advanced)。

> **说明**
>
> 本文介绍原有显式缓存在 Qwen4 上的版本：内容块断点的用法保持不变，并新增自动缓存与缓存有效期（TTL）。与[上下文缓存](context-cache.md)中两种缓存方式的关系：
>
> -   **显式缓存**：通过缓存断点指定输入前缀，命中确定，即本文介绍的内容。
> -   **隐式缓存**：不设置任何缓存参数时自动识别公共前缀，不保证命中，详见[隐式缓存](context-cache.md#2317ea09cfxok)。
> -   OpenAI 兼容 Chat Completions 接口原有的 `cache_control` 内容块标记继续兼容，用法与 `prompt_cache_breakpoint` 相同，详见[基础用法](#basic-usage)。

<a id="工作原理"></a>

<a id="how-it-works"></a>

## 工作原理

缓存以断点为单位创建和读取。自动缓存的断点由系统设置在输入末尾，缓存断点由您在内容块上标记。每个断点对应的缓存前缀是从请求开头到断点所在内容块末尾的全部输入。

收到请求后，系统以每个断点为终点，向前查找最多 20 个内容块，选取已缓存的最长相同前缀：

-   **命中缓存**：读取已缓存的前缀，并按本次请求的 TTL 续期。
-   **未命中缓存**：从请求开头到断点处的内容创建为新的缓存。若前缀中有部分内容已命中缓存，仅对新增部分创建缓存。

缓存前缀需完全相同才能命中，且仅在同一用户的请求之间复用。将固定不变的内容放在前面、每次变化的内容放在断点之后，可以提高命中率。

未设置任何缓存参数时，系统使用[隐式缓存](context-cache.md#2317ea09cfxok)自动识别请求的公共前缀，但不保证命中。需要稳定复用指定内容时，请开启自动缓存或设置缓存断点。

<a id="基础用法"></a>

<a id="basic-usage"></a>

## 基础用法

在请求中需要复用的内容块上设置缓存断点。系统以该内容块的末尾作为断点，把从请求开头到该处的全部输入作为缓存前缀：第一次请求创建缓存，有效期内前缀相同的后续请求读取缓存。缓存前缀至少为 1,024 Token。

<a id="sec-tabs"></a>

<a id="openai-兼容-chat-completions"></a>

<a id="openai-兼容-chat-completions-h4"></a>

#### OpenAI 兼容 Chat Completions

在 `messages` 中需要缓存的内容块上添加 `prompt_cache_breakpoint`，值为 `{"mode": "explicit"}`。添加断点的消息，其 `content` 需使用数组形式：

<a id="code-block"></a>

```python
messages=[
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": long_text,
        "prompt_cache_breakpoint": {"mode": "explicit"},  # <-- 缓存断点
      },
      {"type": "text", "text": "请概括这份文档。"},  # 断点之后的内容不参与该缓存
    ],
  }
],
```

原有的 `"cache_control": {"type": "ephemeral"}` 内容块标记继续兼容，用法与 `prompt_cache_breakpoint` 相同。同一用户的相同前缀可以在两种标记之间复用缓存。新接入推荐使用 `prompt_cache_breakpoint`。

> **警告**
>
> 同一请求中请只使用 `prompt_cache_breakpoint` 和 `cache_control` 中的一种。

以下示例连续发送两次请求：第一次请求创建缓存，第二次请求保持前缀不变、只修改问题，从而读取缓存。

<a id="code-block-2"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
  # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  # 以下为华北2（北京）地域的 URL，调用时请将 WorkspaceId 替换为真实的业务空间 ID，各地域的 URL 不同。
  base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 需要复用的长文档，缓存前缀最少为 1024 Token
long_text = "<固定的长文档>" * 400

def ask(question):
  completion = client.chat.completions.create(
    model="qwen4-max",
    messages=[
      {
        "role": "user",
        "content": [
          {"type": "text", "text": long_text, "prompt_cache_breakpoint": {"mode": "explicit"}},  # <-- 缓存断点
          {"type": "text", "text": question},  # 断点之后的内容每次可以不同
        ],
      }
    ],
    extra_body={
      "enable_thinking": False,
    },
  )
  return completion.usage.prompt_tokens_details

ask("请概括这份文档。")  # 第一次请求：创建缓存
details = ask("请列出文档的三个要点。")  # 第二次请求：读取缓存
print(f"读取缓存 {details.cached_tokens} Token，创建缓存 {details.cache_write_tokens} Token")
```

第二次请求的 `cached_tokens` 为读取的缓存量，`cache_write_tokens` 为本次创建的缓存量。前缀不变时，`cache_write_tokens` 为 0。数字为示意，实际取决于文档长度。

<a id="openai-兼容-responses"></a>

<a id="openai-兼容-responses-h4"></a>

#### OpenAI 兼容 Responses

<a id="responses-api"></a>

通过 OpenAI 兼容的 `/compatible-mode/v1/responses` 接口使用缓存。在请求顶层设置 `prompt_cache_options`；在 `input` 的消息内容块上设置 `prompt_cache_breakpoint`。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `prompt_cache_options` | `object` | 可选对象，配置缓存模式和有效期。 |
| `prompt_cache_options.mode` | `string` | 可选，支持 `implicit` 和 `explicit`，默认 `implicit`。`implicit` 开启显式缓存，在最后一条输入消息末尾自动设置断点；手动断点与自动断点同时生效。`explicit` 需结合手动断点才会创建缓存，没有断点时不生效。 |
| `prompt_cache_options.ttl` | `string` | 可选，支持 `5m` 和 `1h`，默认 `5m`。 |
| `input[].content[].prompt_cache_breakpoint` | `object` | 内容块上的可选对象，优先级高于顶层缓存模式。支持添加到 `input_text`、`input_image`、`input_file` 类型的内容块。 |
| `prompt_cache_breakpoint.mode` | `string` | 设置断点时必填，仅支持 `explicit`。请显式传入 `{"mode": "explicit"}`。 |

以下示例串行发送两次请求，保持断点前的长文档相同，仅改变断点后的问题。第一次创建缓存，第二次在有效期内读取缓存。示例使用 `qwen4-max`。运行前安装 `openai` 并设置 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_BASE_URL`；北京的 Base URL 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，将 `{WorkspaceId}` 替换为业务空间 ID。

<a id="code-block-3"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["DASHSCOPE_BASE_URL"],
)
long_text = "Cache reference: Paris is the capital of France. " * 400

for question in ["Summarize this document.", "What is the capital of France?"]:
    response = client.responses.create(
        model="qwen4-max",
        input=[{
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": long_text,
                    "prompt_cache_breakpoint": {"mode": "explicit"},
                },
                {"type": "input_text", "text": question},
            ],
        }],
        reasoning={"effort": "none"},
        max_output_tokens=128,
        extra_body={"prompt_cache_options": {"mode": "explicit", "ttl": "5m"}},
    )
    print(response.output_text)
    print(response.usage.model_dump())
```

curl 请求中的 `DASHSCOPE_RESPONSES_URL` 为上述 Base URL 加 `/responses`。将占位文档替换为至少 1,024 Token 的真实文档。

<a id="code-block-4"></a>

```bash
curl "$DASHSCOPE_RESPONSES_URL" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen4-max",
    "input": [{
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "<DOCUMENT_WITH_AT_LEAST_1024_TOKENS>",
          "prompt_cache_breakpoint": {"mode": "explicit"}
        },
        {"type": "input_text", "text": "Summarize this document."}
      ]
    }],
    "reasoning": {"effort": "none"},
    "max_output_tokens": 128,
    "prompt_cache_options": {"mode": "explicit", "ttl": "5m"}
  }'
```

<a id="anthropic兼容"></a>

<a id="anthropic兼容-h4"></a>

#### Anthropic兼容

在 `system` 或 `messages` 中需要缓存的内容块上添加 `cache_control`，值为 `{"type": "ephemeral"}`：

<a id="code-block-5"></a>

```python
system=[
  {
    "type": "text",
    "text": long_text,
    "cache_control": {"type": "ephemeral"},  # <-- 缓存断点
  }
],
```

<a id="使用多个断点"></a>

<a id="multiple-breakpoints"></a>

### 使用多个断点

当提示词由变化频率不同的几部分组成时，可以为每一部分分别设置断点。例如智能客服的提示词通常包括系统人设（几乎不变）、知识库检索结果（随咨询主题变化）和对话历史（持续增长）。在每部分末尾设置断点后，即使知识库内容发生变化，系统人设部分仍可命中缓存。

每个请求最多保留最后 4 个有效断点，超出的断点不生效。开启[自动缓存](#auto)时，自动断点占用其中 1 个。

<a id="断点位置变化时的续期"></a>

<a id="breakpoint-renewal"></a>

### 断点位置变化时的续期

系统只创建或续期本次请求中的断点。断点位置改变后，即使读取了旧断点的缓存，旧断点的有效期也不会延长。

例如，在 TTL 不变的情况下，上次请求的断点位于第 2,048 Token 处，本次请求将断点移到第 3,072 Token 处且未保留旧断点。若旧断点在查找范围内且未过期，本次请求读取前 2,048 Token 的缓存，并为后续 1,024 Token 创建缓存；系统只创建或续期第 3,072 Token 处的断点，第 2,048 Token 处的缓存不续期。

<a id="进阶用法"></a>

<a id="advanced"></a>

## 进阶用法

Qwen4 在基础用法之上提供以下两项能力，可以组合使用：

-   **自动缓存**：由系统自动在输入末尾设置断点，适合多轮对话。
-   **缓存有效期（TTL）**：可选 5 分钟或 1 小时。

<a id="自动缓存"></a>

<a id="auto"></a>

### 自动缓存

开启自动缓存后，系统自动在每次请求的输入末尾设置断点，无需随对话增长逐轮移动断点。自动断点不包含用于开始生成回复的模板后缀。自动缓存可以与基础用法中的[缓存断点](#basic-usage)同时使用；若输入末尾已有手动断点，不会重复设置。

<a id="sec-tabs-2"></a>

<a id="openai-兼容-chat-completions-2"></a>

<a id="openai-兼容-chat-completions-2-h4"></a>

#### OpenAI 兼容 Chat Completions

在请求顶层设置 `prompt_cache_options`，并将 `mode` 设置为 `implicit`。使用 OpenAI Python SDK 时通过 `extra_body` 传入：

<a id="code-block-6"></a>

```python
completion = client.chat.completions.create(
  model="qwen4-max",
  messages=[{"role": "user", "content": "请概括这份文档：" + long_text}],
  extra_body={
    "enable_thinking": False,
    "prompt_cache_options": {"mode": "implicit"},  # <-- 开启自动缓存
  },
)
```

`prompt_cache_options.mode` 的取值与对应行为如下：

| 设置 | 自动断点 | 缓存行为 |
| --- | --- | --- |
| `mode` 为 `implicit` | 设置 | 输入末尾的自动断点和手动断点同时生效 |
| `mode` 为 `explicit`，有手动断点 | 不设置 | 按手动断点创建或读取缓存 |
| `mode` 为 `explicit`，无手动断点 | 不设置 | 使用隐式缓存 |
| 不传 `prompt_cache_options`、传 `null` 或 `{}`，或只设置 `ttl` | 不设置 | 有手动断点时按手动断点缓存，否则使用隐式缓存 |

> **说明**
>
> `mode` 为 `implicit` 时使用的是自动断点缓存，按本文的 TTL 与计费规则处理，与不传缓存参数时的[隐式缓存](context-cache.md#2317ea09cfxok)不同。`mode` 为 `explicit` 只表示不自动设置断点，不会关闭隐式缓存。`mode` 仅对当前请求生效。

<a id="openai-兼容-responses-2"></a>

<a id="openai-兼容-responses-2-h4"></a>

#### OpenAI 兼容 Responses

设置 `prompt_cache_options` 开启显式缓存，`mode` 默认为 `implicit`。系统在最后一条输入消息末尾自动设置断点，与手动断点同时生效。

<a id="code-block-7"></a>

```python
response = client.responses.create(
    model="qwen4-max",
    input=[{"role": "user", "content": [{"type": "input_text", "text": long_text}]}],
    reasoning={"effort": "none"},
    max_output_tokens=128,
    extra_body={"prompt_cache_options": {"mode": "implicit", "ttl": "1h"}},
)
print(response.usage.model_dump())
```

<a id="anthropic兼容-2"></a>

<a id="anthropic兼容-2-h4"></a>

#### Anthropic兼容

在请求顶层设置 `cache_control`，值为 `{"type": "ephemeral"}`。顶层 `cache_control` 用于开启自动缓存，与内容块上的 `cache_control` 可以同时使用。使用 Anthropic Python SDK 时通过 `extra_body` 传入：

<a id="code-block-8"></a>

```python
message = client.messages.create(
  model="qwen4-max",
  max_tokens=1024,
  messages=[{"role": "user", "content": "请概括这份文档：" + long_text}],
  extra_body={"cache_control": {"type": "ephemeral"}},  # <-- 在请求顶层开启自动缓存
)
```

以下完整示例开启自动缓存，并连续发送两次相同的长文档请求：第一次请求创建缓存，第二次请求读取缓存。

<a id="sec-tabs-3"></a>

<a id="openai-兼容-chat-completions-3"></a>

<a id="openai-兼容-chat-completions-3-h4"></a>

#### OpenAI 兼容 Chat Completions

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
  # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  # 以下为华北2（北京）地域的 URL，调用时请将 WorkspaceId 替换为真实的业务空间 ID，各地域的 URL 不同。
  base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 需要复用的长文档，缓存前缀最少为 1024 Token
long_text = "<固定的长文档>" * 400

def ask():
  completion = client.chat.completions.create(
    model="qwen4-max",
    messages=[{"role": "user", "content": "请概括这份文档：" + long_text}],
    extra_body={
      "enable_thinking": False,
      "prompt_cache_options": {"mode": "implicit"},  # <-- 开启自动缓存
    },
  )
  return completion.usage.prompt_tokens_details

for i in range(1, 3):
  details = ask()
  print(f"第 {i} 次请求：读取缓存 {details.cached_tokens} Token，创建缓存 {details.cache_write_tokens} Token")
```

<a id="fig-code-group-node-js-tab"></a>

Node.js

<a id="code-code-group-node-js"></a>

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  // 若没有配置环境变量，请将下行替换为：apiKey: "sk-xxx"
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为华北2（北京）地域的 URL，调用时请将 WorkspaceId 替换为真实的业务空间 ID，各地域的 URL 不同。
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

// 需要复用的长文档，缓存前缀最少为 1024 Token
const longText = "<固定的长文档>".repeat(400);

async function ask() {
  const completion = await client.chat.completions.create({
    model: "qwen4-max",
    messages: [{ role: "user", content: "请概括这份文档：" + longText }],
    enable_thinking: false,
    prompt_cache_options: { mode: "implicit" }, // <-- 开启自动缓存
  });
  return completion.usage.prompt_tokens_details;
}

async function main() {
  for (let i = 1; i <= 2; i++) {
    const details = await ask();
    console.log(`第 ${i} 次请求：读取缓存 ${details.cached_tokens} Token，创建缓存 ${details.cache_write_tokens} Token`);
  }
}

main().catch(console.error);
```

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
# 以下为华北2（北京）地域的 URL，调用时请将 WorkspaceId 替换为真实的业务空间 ID，各地域的 URL 不同。
# 将 <固定的长文档> 替换为不少于 1024 Token 的长文档，并在有效期内发送两次。
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen4-max",
    "messages": [
      {"role": "user", "content": "请概括这份文档：<固定的长文档>"}
    ],
    "enable_thinking": false,
    "prompt_cache_options": {"mode": "implicit"}
  }'
```

<a id="openai-兼容-responses-3"></a>

<a id="openai-兼容-responses-3-h4"></a>

#### OpenAI 兼容 Responses

<a id="code-block-9"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["DASHSCOPE_BASE_URL"],
)
long_text = "Cache reference: Paris is the capital of France. " * 400

for question in ["Summarize this document.", "Summarize this document."]:
    response = client.responses.create(
        model="qwen4-max",
        input=[{
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": long_text,
                },
                {"type": "input_text", "text": question},
            ],
        }],
        reasoning={"effort": "none"},
        max_output_tokens=128,
        extra_body={"prompt_cache_options": {"mode": "implicit", "ttl": "5m"}},
    )
    print(response.output_text)
    print(response.usage.model_dump())
```

<a id="anthropic兼容-3"></a>

<a id="anthropic兼容-3-h4"></a>

#### Anthropic兼容

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-python-tab"></a>

Python

<a id="code-code-group-2-python"></a>

```python
import os
import anthropic

client = anthropic.Anthropic(
  # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  # 以下为华北2（北京）地域的 URL，调用时请将 WorkspaceId 替换为真实的业务空间 ID，各地域的 URL 不同。
  base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
)

# 需要复用的长文档，缓存前缀最少为 1024 Token
long_text = "<固定的长文档>" * 400

def ask():
  message = client.messages.create(
    model="qwen4-max",
    max_tokens=1024,
    messages=[{"role": "user", "content": "请概括这份文档：" + long_text}],
    extra_body={"cache_control": {"type": "ephemeral"}},  # <-- 在请求顶层开启自动缓存
  )
  return message.usage

for i in range(1, 3):
  usage = ask()
  print(f"第 {i} 次请求：读取缓存 {usage.cache_read_input_tokens} Token，创建缓存 {usage.cache_creation_input_tokens} Token")
```

<a id="fig-code-group-2-node-js-tab"></a>

Node.js

<a id="code-code-group-2-node-js"></a>

```javascript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  // 若没有配置环境变量，请将下行替换为：apiKey: "sk-xxx"
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为华北2（北京）地域的 URL，调用时请将 WorkspaceId 替换为真实的业务空间 ID，各地域的 URL 不同。
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
});

// 需要复用的长文档，缓存前缀最少为 1024 Token
const longText = "<固定的长文档>".repeat(400);

async function ask() {
  const message = await client.messages.create({
    model: "qwen4-max",
    max_tokens: 1024,
    messages: [{ role: "user", content: "请概括这份文档：" + longText }],
    cache_control: { type: "ephemeral" }, // <-- 在请求顶层开启自动缓存
  });
  return message.usage;
}

async function main() {
  for (let i = 1; i <= 2; i++) {
    const usage = await ask();
    console.log(`第 ${i} 次请求：读取缓存 ${usage.cache_read_input_tokens} Token，创建缓存 ${usage.cache_creation_input_tokens} Token`);
  }
}

main().catch(console.error);
```

<a id="fig-code-group-2-curl-tab"></a>

curl

<a id="code-code-group-2-curl"></a>

```bash
# 以下为华北2（北京）地域的 URL，调用时请将 WorkspaceId 替换为真实的业务空间 ID，各地域的 URL 不同。
# 将 <固定的长文档> 替换为不少于 1024 Token 的长文档，并在有效期内发送两次。
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $DASHSCOPE_API_KEY" \
  -d '{
    "model": "qwen4-max",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral"},
    "messages": [
      {"role": "user", "content": "请概括这份文档：<固定的长文档>"}
    ]
  }'
```

预期输出类似如下，具体 Token 数取决于文档长度：

<a id="code-block-10"></a>

```text
第 1 次请求：读取缓存 0 Token，创建缓存 2048 Token
第 2 次请求：读取缓存 2048 Token，创建缓存 0 Token
```

第二次请求的输入与第一次相同，因此读取了第一次创建的缓存。

<a id="设置缓存有效期"></a>

<a id="ttl"></a>

### 设置缓存有效期

缓存有效期（TTL）可选 `5m`（5 分钟）或 `1h`（1 小时），默认为 `5m`。缓存在有效期内被命中时会自动续期，续期方式见[续期规则](#ttl-rules)。

<a id="sec-tabs-4"></a>

<a id="openai-兼容-chat-completions-4"></a>

<a id="openai-兼容-chat-completions-4-h4"></a>

#### OpenAI 兼容 Chat Completions

在请求顶层的 `prompt_cache_options.ttl` 中设置，对本次请求的全部断点生效：

<a id="code-block-11"></a>

```python
extra_body={
  "prompt_cache_options": {
    "mode": "implicit",
    "ttl": "1h",  # <-- 缓存有效期为 1 小时
  },
},
```

未设置 `prompt_cache_options.ttl` 时，使用请求中最后一个 `cache_control` 标记的 `ttl`；该标记未设置 `ttl`，或请求中没有 `cache_control` 标记时，TTL 为 `5m`。

TTL 只对显式缓存生效，设置 `ttl` 时需同时设置缓存断点或开启自动缓存。

<a id="openai-兼容-responses-4"></a>

<a id="openai-兼容-responses-4-h4"></a>

#### OpenAI 兼容 Responses

在请求顶层的 `prompt_cache_options.ttl` 中设置缓存有效期，支持 `5m` 和 `1h`，默认为 `5m`。

<a id="code-block-12"></a>

```python
extra_body={"prompt_cache_options": {"mode": "implicit", "ttl": "1h"}}
```

<a id="anthropic兼容-4"></a>

<a id="anthropic兼容-4-h4"></a>

#### Anthropic兼容

开启自动缓存时，在顶层 `cache_control` 中设置 `ttl`，未设置时为 `5m`：

<a id="code-block-13"></a>

```python
extra_body={"cache_control": {"type": "ephemeral", "ttl": "1h"}},  # <-- 缓存有效期为 1 小时
```

使用缓存断点时，在内容块的 `cache_control` 中设置 `ttl`：

<a id="code-block-14"></a>

```python
system=[
  {
    "type": "text",
    "text": long_text,
    "cache_control": {"type": "ephemeral", "ttl": "1h"},  # <-- 缓存有效期为 1 小时
  }
],
```

<a id="续期规则"></a>

<a id="ttl-rules"></a>

#### 续期规则

首次请求或缓存已过期时，按本次请求的 TTL 创建缓存。命中有效缓存时，按以下规则续期和计费：

-   **到期时间取较晚值，并保留较高的档位。** 新的到期时间约为“原到期时间”与“本次缓存处理开始时间 + 本次 TTL”中较晚的一个。例如，12:03 命中 12:05 到期的 5m 缓存，新的到期时间约为 12:08。又如，5m 请求命中有效的 1h 缓存时，按 5m 计算续期，但缓存仍保留 1h 档位，后续 1h 请求在有效期内仍按读取缓存计费。
-   **从 5m 升级为 1h 时，升级部分按 1h 创建缓存计费。** 1h 请求命中有效的 5m 缓存时，命中部分按 1h 重新创建，不再计为读取。若部分前缀已有有效的 1h 缓存，这部分仍按读取计费，仅剩余部分和新增前缀按创建计费。其他情况（5m 请求命中 5m 缓存、5m 请求命中 1h 缓存、1h 请求命中 1h 缓存）的命中部分均按读取计费。

有效期从本次缓存处理开始时计算，不在原到期时间上累加，也不从回复结束时重新计时。生成回复的耗时计入有效期，实际到期时间会预留少量处理时间。

以下示例为对同一份缓存的连续请求，该缓存于 12:00 按 1h 创建，原到期时间为 13:00：

| 请求 | 本次 TTL | 请求前的到期时间 | 请求后的到期时间（约） | 计费与档位 |
| --- | --- | --- | --- | --- |
| 12:20 发起 | 5m | 13:00 | 13:00 | 读取缓存。12:25 早于原到期时间，到期时间不变，既不缩短，也不续到 13:20 |
| 12:58 发起 | 5m | 13:00 | 13:03 | 读取缓存。到期时间延长至本次开始后 5 分钟，仍保留 1h 档位 |
| 13:01 发起 | 1h | 13:03 | 14:01 | 读取缓存。缓存已是 1h 档位，不产生升级创建 |

以上示例基于相同前缀的串行请求。多个请求并发写入同一缓存时可能相互覆盖，不保证保留最晚的到期时间。

<a id="查看缓存用量"></a>

<a id="usage"></a>

## 查看缓存用量

响应的 `usage` 中返回读取缓存和创建缓存的 Token 数。流式输出时，OpenAI 兼容 Chat Completions 接口需设置 `stream_options` 为 `{"include_usage": true}`，从最后一个包含 `usage` 的数据块中读取。

<a id="sec-tabs-5"></a>

<a id="openai-兼容-chat-completions-5"></a>

<a id="openai-兼容-chat-completions-5-h4"></a>

#### OpenAI 兼容 Chat Completions

以下为首次创建缓存时的 `usage`（纯文本输入、非思考模式）：

<a id="code-block-15"></a>

```json
{
  "usage": {
    "prompt_tokens": 2304,
    "completion_tokens": 128,
    "total_tokens": 2432,
    "prompt_tokens_details": {
      "text_tokens": 2304,
      "cached_tokens": 0,
      "cache_write_tokens": 2048,
      "cache_creation_input_tokens": 2048,
      "cache_type": "ephemeral",
      "cache_creation": {
        "ephemeral_5m_input_tokens": 2048,
        "ephemeral_1h_input_tokens": 0
      }
    },
    "completion_tokens_details": {}
  }
}
```

| 字段 | 说明 |
| --- | --- |
| `prompt_tokens` | 全部输入 Token 数，包含读取缓存、创建缓存和未使用缓存的部分，命中缓存后不扣减 |
| `total_tokens` | `prompt_tokens` 与 `completion_tokens` 之和 |
| `prompt_tokens_details.cached_tokens` | 读取缓存的 Token 数 |
| `prompt_tokens_details.cache_write_tokens` | 创建缓存的 Token 数 |
| `prompt_tokens_details.cache_creation_input_tokens` | 创建缓存的 Token 数，与 `cache_write_tokens` 相等，统计时不要重复相加 |
| `prompt_tokens_details.cache_type` | 显式缓存的类型，固定为 `ephemeral` |
| `prompt_tokens_details.cache_creation` | 按 TTL 统计的创建缓存 Token 数，`ephemeral_5m_input_tokens` 与 `ephemeral_1h_input_tokens` 之和等于创建缓存的 Token 数 |

上例中未使用缓存的输入为 2304 − 0 − 2048 = 256 Token。各缓存字段均为原始 Token 数，不含计费倍率。有效期内以相同前缀再次请求时，`cached_tokens` 为 2048，`cache_write_tokens`、`cache_creation_input_tokens` 及 `cache_creation` 中的两项均为 0，`prompt_tokens` 仍为 2304。

图像、音频、视频等输入明细按实际输入返回，思考等输出明细按模型与配置返回；不适用的字段不会返回，而不是返回 0。

<a id="openai-兼容-responses-5"></a>

<a id="openai-兼容-responses-5-h4"></a>

#### OpenAI 兼容 Responses

响应顶层的 `prompt_cache_options` 返回缓存 `mode`（`implicit` 或 `explicit`）与 `ttl`（`5m` 或 `1h`）。缓存用量位于 `usage.input_tokens_details`。流式请求从 `response.completed` 事件中的 `response.usage` 读取用量，不使用 Chat Completions 的 `stream_options.include_usage`。

| 字段 | 说明 |
| --- | --- |
| `input_tokens` | 全部输入 Token 数，包括读取缓存、创建缓存和未使用缓存的部分。 |
| `input_tokens_details.cached_tokens` | 读取缓存的 Token 数。 |
| `input_tokens_details.cache_write_tokens` | 创建缓存的 Token 数。 |
| `input_tokens_details.cache_write_tokens_details.ttl_5m_tokens / ttl_1h_tokens` | 按 TTL 统计的创建 Token 数，两项之和等于 `cache_write_tokens`。 |

以下为北京测试端点上首次创建 5m 缓存时返回的字段示例。相同前缀的第二次请求中，`cached_tokens` 为 4488，`cache_write_tokens` 及两个 TTL 创建字段均为 0。

<a id="code-block-16"></a>

```json
{
  "prompt_cache_options": {
    "mode": "explicit",
    "ttl": "5m"
  },
  "usage": {
    "input_tokens": 4498,
    "input_tokens_details": {
      "cached_tokens": 0,
      "cache_write_tokens": 4488,
      "cache_write_tokens_details": {
        "ttl_5m_tokens": 4488,
        "ttl_1h_tokens": 0
      }
    },
    "output_tokens": 32,
    "output_tokens_details": {
      "reasoning_tokens": 32
    },
    "total_tokens": 4530
  }
}
```

不要将 Responses 的 `input_tokens_details` 字段与 Chat Completions 的 `prompt_tokens_details` 或 Anthropic 的 `cache_creation` 字段混用。

<a id="anthropic兼容-5"></a>

<a id="anthropic兼容-5-h4"></a>

#### Anthropic兼容

以下为开启自动缓存并将 TTL 设置为 `1h` 时，首次创建缓存的 `usage`：

<a id="code-block-17"></a>

```json
{
  "usage": {
    "input_tokens": 8,
    "output_tokens": 128,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 2048,
    "cache_creation": {
      "ephemeral_5m_input_tokens": 0,
      "ephemeral_1h_input_tokens": 2048
    },
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  }
}
```

| 字段 | 说明 |
| --- | --- |
| `input_tokens` | 未读取缓存、也未创建缓存的输入 Token 数 |
| `cache_read_input_tokens` | 读取缓存的 Token 数 |
| `cache_creation_input_tokens` | 创建缓存的 Token 数 |
| `cache_creation` | 按 TTL 统计的创建缓存 Token 数 |
| `prompt_tokens_details.cached_tokens` | 读取缓存的 Token 数，与 `cache_read_input_tokens` 相同，统计时不要重复相加 |

全部输入 Token 数为 `input_tokens`、`cache_read_input_tokens` 与 `cache_creation_input_tokens` 之和，上例中为 8 + 0 + 2048 = 2056。

<a id="最佳实践"></a>

<a id="best-practices"></a>

## 最佳实践

-   **多轮对话优先使用自动缓存。** 自动断点随对话增长后移，无需逐轮调整断点位置。
-   **将固定内容放在前面。** 系统提示词、工具定义、参考文档等不变的内容放在输入开头，时间戳、用户问题等每次变化的内容放在最后。
-   **将断点设置在每次请求都相同的最后一个内容块上。** 不要将断点设置在每次都会变化的内容块上，否则每次请求都会创建新缓存，无法读取。
-   **追加历史消息，不改写已有内容。** 修改、删减或重新排序前面的消息或工具定义，会使之后的缓存无法命中。
-   **按变化频率使用多个断点。** 例如工具定义很少变化、参考文档每天更新时，分别在两者末尾设置断点。
-   **单轮新增内容块较多时补充断点。** 每个断点最多向前查找 20 个内容块，单轮新增内容超过该范围时，在中间位置增加断点。
-   **按复用间隔选择 TTL。** 复用间隔在 5 分钟以内时使用 `5m`，命中即可续期；复用间隔在 5 分钟到 1 小时之间时使用 `1h`。
-   **通过用量字段观察命中情况。** 缓存命中率可按读取缓存的 Token 数除以全部输入 Token 数计算，命中率偏低时，检查前缀和断点位置是否稳定。

<a id="计费说明"></a>

<a id="billing"></a>

## 计费说明

缓存断点仅影响输入 Token 的计费，输出 Token 按原价计费。

| 输入 Token 类型 | 计费方式 |
| --- | --- |
| 创建缓存，TTL 为 5m | 输入 Token 单价的约 125% |
| 创建缓存，TTL 为 1h | 输入 Token 单价的约 200% |
| 读取缓存 | [Qwen4-Max](../../test-1/model-pricing.md) |
| 未读取也未创建缓存 | 输入 Token 单价 |

若本次缓存前缀包含已有的有效缓存，已有部分按读取缓存计费，仅新增部分按创建缓存计费。TTL 从 5m 升级为 1h 时的计费见[续期规则](#ttl-rules)。

<a id="使用限制"></a>

<a id="limits"></a>

## 使用限制

-   仅 Qwen4 系列模型支持。
-   缓存前缀最少为 1,024 Token。不足 1,024 Token 时不创建缓存，请求正常返回，按 TTL 统计的创建明细不返回。
-   每个请求最多保留最后 4 个有效断点，开启自动缓存时自动断点占用其中 1 个。
-   系统以每个断点为终点，最多向前查找 20 个内容块。待命中的缓存与断点之间间隔超过 20 个内容块时，无法命中。
-   TTL 仅可设置为 `5m` 或 `1h`。

<a id="常见问题"></a>

<a id="faq"></a>

## 常见问题

<a id="q-不设置任何缓存参数-还能命中缓存吗"></a>

<a id="faq-no-params"></a>

### Q：不设置任何缓存参数，还能命中缓存吗？

可以。未设置缓存参数时使用[隐式缓存](context-cache.md#2317ea09cfxok)，系统自动识别请求的公共前缀，但不保证命中。需要稳定命中时，请设置缓存断点或开启自动缓存。

<a id="q-只设置了-ttl-为什么缓存有效期没有变化"></a>

<a id="faq-ttl-only"></a>

### Q：只设置了 TTL，为什么缓存有效期没有变化？

TTL 只对显式缓存生效。在 OpenAI 兼容 Chat Completions 接口中只设置 `prompt_cache_options.ttl` 时，请求使用隐式缓存。请同时添加手动断点，或将 `prompt_cache_options.mode` 设置为 `implicit`。

<a id="q-使用-5m-请求命中-1h-缓存-会缩短缓存有效期吗"></a>

<a id="faq-5m-hit-1h"></a>

### Q：使用 5m 请求命中 1h 缓存，会缩短缓存有效期吗？

不会。新的到期时间取原到期时间与本次续期时间中较晚的一个，且缓存保留 1h 档位。详见[续期规则](#ttl-rules)。
