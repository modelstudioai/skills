# 代码解释器

调用模型时启用内置的 Python 代码解释器，可使模型在沙箱环境里编写与运行 Python 代码，以解决数学计算、数据分析等复杂问题。

## 使用方式

代码解释器功能支持三种调用方式，启用参数有所不同：

#### OpenAI 兼容-Responses API

通过 `tools` 参数启用代码解释器功能，需添加 `code_interpreter` 工具。

> 为了获得最佳回复效果，建议同时开启 `code_interpreter`、`web_search` 和 `web_extractor` 工具。

```
# 导入依赖与创建客户端...
response = client.responses.create(
    model="qwen3.8-max",
    input="123的21次方是多少？",
    tools=[
        {"type": "code_interpreter"},
        {"type": "web_search"},
        {"type": "web_extractor"},
    ],
    extra_body={
        "enable_thinking": True
    }
)

print(response.output_text)
```

#### OpenAI 兼容-Chat Completions API

在 API 请求中传入 `enable_code_interpreter: true` 即可启用代码解释器。

```
# 导入依赖与创建客户端...
completion = client.chat.completions.create(
    # 需使用支持代码解释器的模型
    model="qwen3.5-plus",
    messages=[{"role": "user", "content": "123的21次方是多少？"}],
    # 由于 enable_code_interpreter 非 OpenAI 标准参数，使用 Python SDK 需要通过 extra_body 传入（使用Node.js SDK 需作为顶层参数传入）
    extra_body={
        "enable_code_interpreter": True,
        # 代码解释器功能仅支持思考模式调用
        "enable_thinking": True,
    },
    # 仅支持流式输出调用
    stream=True
)
```

> Chat Completions API 无法获取代码解释器运行的代码信息，如需获取请使用 Responses API 或 DashScope 协议。

#### DashScope

在 API 请求中设置 `enable_code_interpreter` 为`true`即可启用代码解释器。

```
# 导入依赖...
response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.5-plus",
    messages=[{"role": "user", "content": "123的21次方是多少？"}],
    # 通过 enable_code_interpreter 参数开启代码解释器
    enable_code_interpreter=True,
    # 代码解释器功能仅支持思考模式
    enable_thinking=True,
    result_format="message",
    # 仅支持流式输出调用
    stream=True
)
```

代码解释器运行的代码将通过`tool_info`字段返回。

启用后，模型将分阶段处理请求：

1.  **思考**：模型分析用户请求，并生成解决问题的思路和步骤。
2.  **代码执行**：模型生成并执行 Python 代码。
3.  **结果整合**：模型接收代码执行结果，并规划后续步骤。
4.  **回复**：模型生成自然语言回复。

> 第二步和第三步可能循环执行多次。

不同 API 返回的字段有所差异：

-   Responses API：思考内容通过 output 中 type="reasoning" 的对象返回，代码执行通过 type="code\_interpreter\_call" 返回，回复通过 type="message" 返回。
-   Chat Completions API / DashScope：思考内容通过 reasoning\_content 字段返回，回复通过 content 字段返回。DashScope 额外支持 tool\_info 字段返回代码内容。

## 适用范围

### 推荐模型

#### Responses API

千问Max：Qwen3.8-Max系列、Qwen3.7-Max系列

千问Plus：Qwen3.7-Plus系列、Qwen3.6-Plus系列、Qwen3.5-Plus系列

DeepSeek：deepseek-v4-flash、deepseek-v4-flash-0731

Qwen3.8开源系列

#### Chat Completions API / DashScope

-   千问Max（思考模式）：Qwen3-Max系列
-   千问Plus：Qwen3.5-Plus系列

### 其他模型

以下模型也支持此工具调用，但效果不如推荐模型。仅支持通过Responses API调用。

-   千问Flash：Qwen3.8-Flash系列、Qwen3.7-Flash系列、Qwen3.6-Flash系列、Qwen3.5-Flash系列
-   Qwen3.6开源系列（qwen3.6-27b除外）
-   Qwen3.5开源系列

## 快速开始

以下示例演示代码解释器如何高效解决数学计算问题。

#### OpenAI 兼容-Responses API

> 为获得最佳回复效果，建议同时开启 `code_interpreter`、`web_search` 和 `web_extractor` 工具。

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

response = client.responses.create(
    model="qwen3.8-max",
    input="12的3次方",
    tools=[
        {
            "type": "code_interpreter"
        },
        {
            "type": "web_search"
        },
        {
            "type": "web_extractor"
        }
    ],
    extra_body = {
        "enable_thinking": True
    }
)
# 取消以下注释查看中间过程输出
# print(response.output)
print("="*20+"回复内容"+"="*20)
print(response.output_text)
print("="*20+"Token 消耗与工具调用"+"="*20)
print(response.usage)
```

javascript

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.responses.create({
        model: "qwen3.8-max",
        input: "请计算12的三次方",
        tools: [
            { type: "code_interpreter" },
            { type: "web_search" },
            { type: "web_extractor" }
        ],
        enable_thinking: true
    });

    console.log("====================回复内容====================");
    console.log(response.output_text);

    // 打印工具调用次数
    console.log("====================Token 消耗与工具调用====================");
    if (response.usage && response.usage.x_tools) {
        console.log(`代码解释器运行次数: ${response.usage.x_tools.code_interpreter?.count || 0}`);
    }
    // 取消以下注释查看中间过程的输出
    // console.log(JSON.stringify(response.output[0], null, 2));
}

main();
```

bash

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "请计算12的三次方",
    "tools": [
        {"type": "code_interpreter"},
        {"type": "web_search"},
        {"type": "web_extractor"}
    ],
    "enable_thinking": true
}'
```

###### 响应示例

```
====================回复内容====================
12的3次方等于 **1728**。

计算过程：
12³ = 12 × 12 × 12 = 144 × 12 = 1728
====================Token 消耗与工具调用====================
ResponseUsage(input_tokens=1160, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=195, output_tokens_details=OutputTokensDetails(reasoning_tokens=105), total_tokens=1355, x_tools={'code_interpreter': {'count': 1}})
```

#### OpenAI 兼容-Chat Completions API

#### Python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "123的21次方是多少？"}]

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    extra_body={"enable_thinking": True, "enable_code_interpreter": True},
    stream=True,
    stream_options={
        "include_usage": True
    },
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
        continue

    delta = chunk.choices[0].delta

    # 只收集思考内容
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content

    # 收到content，开始进行回复
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
```

###### 响应示例

```
====================思考过程====================

用户问的是123的21次方是多少。这是一个数学计算问题，我需要计算123^21。

我可以使用代码计算器来计算这个值。我需要调用code_interpreter函数，传入计算123**21的Python代码。

让我构造这个函数调用。
用户询问123的21次方是多少，我使用Python代码计算了这个结果。计算结果显示123的21次方等于77269364466549865653073473388030061522211723。这是一个非常大的数字，我应该直接给出这个
====================完整回复====================

123的21次方是：77269364466549865653073473388030061522211723
Usage:
CompletionUsage(completion_tokens=245, prompt_tokens=719, total_tokens=964, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=153, rejected_prediction_tokens=None), prompt_tokens_details=None)
```

#### Node.js

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

async function main() {
    try {
        const messages = [{ role: 'user', content: '123的21次方是多少？' }];
        const stream = await openai.chat.completions.create({
            model: 'qwen3-max',
            messages,
            stream: true,
            enable_thinking: true,
            enable_code_interpreter: true
        });
        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\nUsage:');
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0].delta;

            // 只收集思考内容
            if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
                if (!isAnswering) {
                    process.stdout.write(delta.reasoning_content);
                }
                reasoningContent += delta.reasoning_content;
            }

            // 收到content，开始进行回复
            if (delta.content !== undefined && delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

###### 响应示例

```
====================思考过程====================

  The user is asking for the value of 123 raised to the power of 21. This is a mathematical calculation that I can perform using Python's code interpreter. I'll use the exponentiation operator ** to calculate this.

  Let me write the code to compute 123**21.The calculation has been completed successfully. The result of 123 raised to the power of 21 is a very large number: 77269364466549865653073473388030061522211723.

  I should present this result clearly to the user.

  ====================完整回复====================

  123的21次方是：77269364466549865653073473388030061522211723
```

#### curl

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-max",
    "messages": [
        {
            "role": "user",
            "content": "123的21次方是多少？"
        }
    ],
    "enable_code_interpreter": true,
    "enable_thinking": true,
    "stream": true
}'
```

#### 响应示例

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1761899724,"system_fingerprint":null,"model":"qwen3-max","id":"chatcmpl-2f96ef0b-5924-4dfc-b768-4d53ec538b4e"}

data: {"choices":[{"finish_reason":null,"logprobs":null,"delta":{"content":null,"reasoning_content":"用户"},"index":0}],"object":"chat.completion.chunk","usage":null,"created":1761899724,"system_fingerprint":null,"model":"qwen3-max","id":"chatcmpl-2f96ef0b-5924-4dfc-b768-4d53ec538b4e"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"问"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1761899724,"system_fingerprint":null,"model":"qwen3-max","id":"chatcmpl-2f96ef0b-5924-4dfc-b768-4d53ec538b4e"}

data: {"choices":[{"delta":{"content":null,"reasoning_content":"的是"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1761899724,"system_fingerprint":null,"model":"qwen3-max","id":"chatcmpl-2f96ef0b-5924-4dfc-b768-4d53ec538b4e"}

...

data: {"choices":[{"delta":{"content":"非常大的数字，总","reasoning_content":null},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1761899724,"system_fingerprint":null,"model":"qwen3-max","id":"chatcmpl-2f96ef0b-5924-4dfc-b768-4d53ec538b4e"}

data: {"choices":[{"delta":{"content":"共有43位","reasoning_content":null},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1761899724,"system_fingerprint":null,"model":"qwen3-max","id":"chatcmpl-2f96ef0b-5924-4dfc-b768-4d53ec538b4e"}

data: {"choices":[{"delta":{"content":"。","reasoning_content":null},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1761899724,"system_fingerprint":null,"model":"qwen3-max","id":"chatcmpl-2f96ef0b-5924-4dfc-b768-4d53ec538b4e"}

data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1761899724,"system_fingerprint":null,"model":"qwen3-max","id":"chatcmpl-2f96ef0b-5924-4dfc-b768-4d53ec538b4e"}

data: [DONE]
```

#### DashScope

> 不支持 Java SDK。

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

messages = [
    {"role": "user", "content": "123的21次方是多少？"},
]

response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.5-plus",
    messages=messages,
    enable_code_interpreter=True,
    enable_thinking=True,
    result_format="message",
    # 仅支持流式输出
    stream=True
)

for chunk in response:
    output = chunk["output"]
    print(output)
```

###### 响应示例

```
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": "The"}}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": " user is asking"}}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": " me"}}]}
...
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": " I'll write a"}}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": " simple Python program to calculate"}}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": ""}}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": ""}}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": ""}}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": ""}}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": ""}}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": "The"}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": " user"}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": " asked"}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
...
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": " I should present this result"}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": " to the user in"}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "", "reasoning_content": " a clear format."}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "123的", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "21次方是：\n\n", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "772693", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "644665", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "498656", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "530734", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "733880", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "300615", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "222117", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": "23", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
{"text": null, "finish_reason": null, "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": "", "reasoning_content": ""}}], "tool_info": [{"code_interpreter": {"code": "123**21"}, "type": "code_interpreter"}]}
```

#### curl

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen3.5-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "123的21次方是多少？"
            }
        ]
    },
    "parameters": {
        "enable_code_interpreter": true,
        "enable_thinking": true,
        "result_format": "message"
    }
}'
```

#### 响应示例

> <...文字内容...>为说明性注释，非实际 API 响应，用于标识处理阶段。

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"The","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":290,"output_tokens":3,"input_tokens":287,"output_tokens_details":{"reasoning_tokens":1}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":" user is asking","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":293,"output_tokens":6,"input_tokens":287,"output_tokens_details":{"reasoning_tokens":4}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}

...思考阶段...

id:21
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"null"}]},"usage":{"total_tokens":388,"output_tokens":101,"input_tokens":287,"output_tokens_details":{"reasoning_tokens":68}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}

...思考结束开始运行代码解释器...

id:22
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"null"}],"tool_info":[{"code_interpreter":{"code":"123**21"},"type":"code_interpreter"}]},"usage":{"total_tokens":388,"output_tokens":101,"input_tokens":287,"output_tokens_details":{"reasoning_tokens":68},"plugins":{"code_interpreter":{"count":1}}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}

...运行代码解释器后开始思考...

id:23
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"The","role":"assistant"},"finish_reason":"null"}],"tool_info":[{"code_interpreter":{"code":"123**21"},"type":"code_interpreter"}]},"usage":{"total_tokens":838,"output_tokens":104,"input_tokens":734,"output_tokens_details":{"reasoning_tokens":69},"plugins":{"code_interpreter":{"count":1}}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}

id:24
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":" user","role":"assistant"},"finish_reason":"null"}],"tool_info":[{"code_interpreter":{"code":"123**21"},"type":"code_interpreter"}]},"usage":{"total_tokens":839,"output_tokens":105,"input_tokens":734,"output_tokens_details":{"reasoning_tokens":70},"plugins":{"code_interpreter":{"count":1}}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}

...思考阶段...

id:43
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":" a clear format.","role":"assistant"},"finish_reason":"null"}],"tool_info":[{"code_interpreter":{"code":"123**21"},"type":"code_interpreter"}]},"usage":{"total_tokens":942,"output_tokens":208,"input_tokens":734,"output_tokens_details":{"reasoning_tokens":171},"plugins":{"code_interpreter":{"count":1}}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}

...思考结束，开始回复...

id:44
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"123的","reasoning_content":"","role":"assistant"},"finish_reason":"null"}],"tool_info":[{"code_interpreter":{"code":"123**21"},"type":"code_interpreter"}]},"usage":{"total_tokens":947,"output_tokens":213,"input_tokens":734,"output_tokens_details":{"reasoning_tokens":171},"plugins":{"code_interpreter":{"count":1}}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}

...

id:53
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"23","reasoning_content":"","role":"assistant"},"finish_reason":"null"}],"tool_info":[{"code_interpreter":{"code":"123**21"},"type":"code_interpreter"}]},"usage":{"total_tokens":997,"output_tokens":263,"input_tokens":734,"output_tokens_details":{"reasoning_tokens":171},"plugins":{"code_interpreter":{"count":1}}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}

id:54
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","reasoning_content":"","role":"assistant"},"finish_reason":"stop"}],"tool_info":[{"code_interpreter":{"code":"123**21"},"type":"code_interpreter"}]},"usage":{"total_tokens":997,"output_tokens":263,"input_tokens":734,"output_tokens_details":{"reasoning_tokens":171},"plugins":{"code_interpreter":{"count":1}}},"request_id":"a1959ad1-2637-4672-a21f-4d351371d254"}
```

## 响应解析

#### OpenAI 兼容-Responses API

以下示例使用 OpenAI Python SDK，演示如何在流式响应中解析 API 返回的数据。

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

response = client.responses.create(
    model="qwen3.8-max",
    input="12的3次方",
    tools=[
        {"type": "code_interpreter"}
    ],
    extra_body={
        "enable_thinking": True
    },
    stream=True
)

def print_section(title):
    print(f"\n{'=' * 20}{title}{'=' * 20}")

current_section = None
final_response = None

for event in response:
    # 思考过程增量输出
    if event.type == "response.reasoning_text.delta":
        if current_section != "reasoning":
            print_section("思考过程")
            current_section = "reasoning"
        print(event.delta, end="", flush=True)

    # 代码解释器调用完成
    elif event.type == "response.output_item.done" and hasattr(event.item, "code"):
        print_section("代码执行")
        print(f"代码:\n{event.item.code}")
        if event.item.outputs:
            print(f"结果: {event.item.outputs[0].logs}")
        current_section = "code"

    # 最终回复增量输出
    elif event.type == "response.output_text.delta":
        if current_section != "answer":
            print_section("完整回复")
            current_section = "answer"
        print(event.delta, end="", flush=True)

    # 响应完成，保存最终结果用于获取 usage
    elif event.type == "response.completed":
        final_response = event.response

# 输出 Token 消耗和工具调用次数
if final_response and final_response.usage:
    print_section("Token 消耗与工具调用")
    usage = final_response.usage
    print(f"输入 Token: {usage.input_tokens}")
    print(f"输出 Token: {usage.output_tokens}")
    print(f"思考 Token: {usage.output_tokens_details.reasoning_tokens}")
    # 若模型未实际调用代码解释器（如简单问题直接给出结果），响应不含 x_tools 字段
    if hasattr(usage, 'x_tools'):
        print(f"代码解释器调用次数: {usage.x_tools.get('code_interpreter', {}).get('count', 0)}")
    else:
        print("代码解释器调用次数: 0")
```

#### DashScope

以下 DashScope Python SDK 示例演示：在单次请求中执行两次计算，并返回代码及总调用次数。

> 由于 OpenAI Chat Completions API 在**代码执行**阶段不返回数据，**思考**与**结果整合**阶段之间会出现响应空窗。又因两个阶段均通过 `reasoning_content`返回内容，可统一视为**思考**阶段处理。响应解析示例请参见[快速开始](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-code-interpreter.md)代码。

```
import os
import dashscope
from dashscope import MultiModalConversation
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'

messages = [{"role": "user", "content": "运行两次代码解释器：第一次运行请计算123的23次方的值，第二次运行请将前者的结果除以5"}]

response = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.5-plus",
    messages=messages,
    result_format="message",
    enable_thinking=True,
    enable_code_interpreter=True,
    stream=True,
    incremental_output=True,
)

# 状态标志：跟踪是否已打印工具信息、是否进入回答阶段、是否在推理段
is_answering = False
in_reasoning_section = False
cur_tools = []

# 打印带标题的分隔区域
def print_section(title):
    print(f"\n{'=' * 20}{title}{'=' * 20}")

# 初始打印“思考过程”标题
print_section("思考过程")
in_reasoning_section = True

# 流式处理模型返回的每个数据块
for chunk in response:
    try:
        # 提取响应中的关键字段：内容、推理文本、工具调用信息
        choice = chunk.output.choices[0]
        msg = choice.message
        content = msg.get("content", "")            # 最终回答内容
        reasoning = msg.get("reasoning_content", "") # 推理过程文本
        tools = chunk.output.get("tool_info", None)  # 工具调用信息
    except (IndexError, AttributeError, KeyError):
        # 跳过结构异常的数据块
        continue
    # 若无有效内容，跳过当前块
    if not content and not reasoning and tools is None:
        continue
    # 输出推理过程
    if reasoning and not is_answering:
        if not in_reasoning_section:
            print_section("思考过程")
            in_reasoning_section = True
        print(reasoning, end="", flush=True)
    if tools is not None and tools != cur_tools:
        print_section("工具信息")
        print(tools)
        in_reasoning_section = False
        cur_tools = tools
    # 输出最终回答内容
    if content:
        if not is_answering:
            print_section("完整回复")
            is_answering = True
            in_reasoning_section = False
        print(content, end="", flush=True)
# 打印代码解释器调用次数
print_section("代码解释器运行次数")
print(chunk.usage.plugins)
```

### 响应示例

```
====================思考过程====================
用户要求运行两次代码解释器：
1. 第一次运行：计算123的23次方的值
2. 第二次运行：将前者的结果除以5

我需要先调用代码解释器计算123**23，然后用这个结果再调用一次代码解释器除以5。

让我先做第一次计算。

====================工具信息====================
[{'code_interpreter': {'code': '123**23'}, 'type': 'code_interpreter'}]

====================思考过程====================
第一次计算得到了123的23次方的值：1169008215014432917465348578887506800769541157267

现在需要第二次运行，将这个结果除以5。我需要使用这个确切的数值进行除法运算
====================工具信息====================
[{'code_interpreter': {'code': '123**23'}, 'type': 'code_interpreter'}, {'code_interpreter': {'code': ''}, 'type': 'code_interpreter'}]

====================工具信息====================
[{'code_interpreter': {'code': '123**23'}, 'type': 'code_interpreter'}, {'code_interpreter': {'code': '1169008215014432917465348578887506800769541157267 / 5'}, 'type': 'code_interpreter'}]

====================思考过程====================
用户要求运行两次代码解释器：
1. 第一次计算123的23次方，结果是：1169008215014432917465348578887506800769541157267
2. 第二次将这个结果除以5，得到：2.338016430028866e+47

现在我需要向用户报告这两个
====================完整回复====================
第一次运行结果：123的23次方 = 1169008215014432917465348578887506800769541157267

第二次运行结果：将上述结果除以5 = 2.338016430028866e+47
====================代码解释器运行次数====================
{'code_interpreter': {'count': 2}}
```

## 注意事项

-   代码解释器与 [Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md) 互斥，不可同时启用。
    
    > 同时启用会报错。
    
-   启用代码解释器后，单次请求会触发多次模型推理，`usage` 字段汇总所有调用的 Token 消耗。
    
-   大模型在进行精确数值计算（如时间戳转换、日期格式化、复杂数学运算等）时可能产生偏差。建议在涉及精确计算的场景下启用代码解释器，由 Python 代码完成计算，以确保结果准确。
    

## 计费说明

启用代码解释器工具**限时免费**，但会增加 Token 消耗。
