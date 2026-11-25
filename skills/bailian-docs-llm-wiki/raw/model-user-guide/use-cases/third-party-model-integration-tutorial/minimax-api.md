# MiniMax

本文档介绍如何调用阿里云百炼部署的 MiniMax 模型推理服务。

> **重要**
>
> 本文档描述的功能仅在华北2（北京）地域可用，如需使用模型，需从华北2（北京）地域[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)。

<a id="快速开始"></a>

<a id="9d84551784a6l"></a>

## 快速开始

API 使用前提：已[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装SDK](../../../model-api-reference/preparations/install-sdk.md)。

<a id="sec-tabs"></a>

<a id="openai兼容"></a>

<a id="openai兼容-h4"></a>

#### OpenAI兼容

<a id="sec-tabs-2"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

<a id="bd292015a22sc"></a>

### 示例代码

<a id="code-block"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[{"role": "user", "content": "你是谁"}],
    stream=True,
)

reasoning_content = ""  # 完整思考过程
answer_content = ""     # 完整回复
is_answering = False    # 是否进入回复阶段

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if chunk.choices:
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

<a id="7a142728d5hah"></a>

### 返回结果

<a id="code-block-2"></a>

```text
====================思考过程====================

用户用中文问"你是谁"，意思是"你是谁？"或"Who are you?"

我应该用中文回复，介绍自己是一个AI助手。
====================完整回复====================

你好！我是 MiniMax-M2.5，一个AI助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？
```

<a id="node-js"></a>

<a id="node-js-h4"></a>

#### Node.js

<a id="9f294ed715hm6"></a>

### 示例代码

<a id="code-block-3"></a>

```javascript
import OpenAI from "openai";
import process from 'process';

// 初始化OpenAI客户端
const openai = new OpenAI({
    // 如果没有配置环境变量，请用阿里云百炼API Key替换：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = ''; // 完整思考过程
let answerContent = ''; // 完整回复
let isAnswering = false; // 是否进入回复阶段

async function main() {
    const messages = [{ role: 'user', content: '你是谁' }];

    const stream = await openai.chat.completions.create({
        model: 'MiniMax-M2.5',
        messages,
        stream: true,
    });

    console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

    for await (const chunk of stream) {
        if (chunk.choices?.length) {
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
    }
}

main();
```

<a id="d221c3c1d3k93"></a>

### 返回结果

<a id="code-block-4"></a>

```text
====================思考过程====================

用户用中文问"你是谁"，意思是"你是谁？"或"Who are you?"

我应该用中文回复，介绍自己是一个AI助手。
====================完整回复====================

你好！我是 MiniMax-M2.5，一个AI助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？
```

<a id="http"></a>

<a id="http-h4"></a>

#### HTTP

<a id="d8d5ba8f252i6"></a>

### 示例代码

<a id="sec-tabs-3"></a>

<a id="curl"></a>

<a id="curl-h4"></a>

#### curl

<a id="code-block-5"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "MiniMax-M2.5",
    "messages": [
        {
            "role": "user",
            "content": "你是谁"
        }
    ]
}'
```

<a id="03cd04fa04kxk"></a>

### 返回结果

<a id="code-block-6"></a>

```json
{
    "choices": [
        {
            "message": {
                "content": "你好！我是 MiniMax-M2.5，一个由 MiniMax 公司开发的 AI 助手。我可以帮助你回答问题、提供信息、进行对话，以及完成各种文字相关的任务。有什么我可以帮助你的吗？",
                "reasoning_content": "用户用中文问\"你是谁\"，意思是\"你是谁？\"或\"Who are you?\"\n\n我应该用中文回复，介绍自己。",
                "role": "assistant"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 40,
        "completion_tokens": 72,
        "total_tokens": 112,
        "completion_tokens_details": {
            "reasoning_tokens": 26
        },
        "prompt_tokens_details": {
            "cached_tokens": 0
        }
    },
    "created": 1771944590,
    "system_fingerprint": null,
    "model": "MiniMax-M2.5",
    "id": "chatcmpl-b1277a9c-52da-9de7-988a-d5c063d83xxx"
}
```

<a id="dashscope"></a>

<a id="dashscope-h4"></a>

#### DashScope

<a id="sec-tabs-4"></a>

<a id="python-2"></a>

<a id="python-2-h4"></a>

#### Python

<a id="1e7877cdadkn2"></a>

### 示例代码

<a id="code-block-7"></a>

```python
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 初始化请求参数
messages = [{"role": "user", "content": "你是谁？"}]

completion = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=messages,
    stream=True,              # 开启流式输出
)

reasoning_content = ""  # 完整思考过程
answer_content = ""     # 完整回复
is_answering = False    # 是否进入回复阶段

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    message = chunk.choices[0].delta

    # 只收集思考内容
    if message.reasoning_content:
        if not is_answering:
            print(message.reasoning_content, end="", flush=True)
        reasoning_content += message.reasoning_content

    # 收到 content，开始进行回复
    if message.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
        print(message.content, end="", flush=True)
        answer_content += message.content

# 循环结束后，reasoning_content 和 answer_content 变量中包含了完整的内容
# 您可以在这里根据需要进行后续处理
# print(f"\n\n完整思考过程:\n{reasoning_content}")
# print(f"\n完整回复:\n{answer_content}")
```

<a id="dab4d2a159ddg"></a>

### 返回结果

<a id="code-block-8"></a>

```text
====================思考过程====================

用户用中文问"你是谁"，意思是"你是谁？"或"Who are you?"

我应该用中文回复，介绍自己是一个AI助手。
====================完整回复====================

你好！我是 MiniMax-M2.5，一个AI助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？
```

<a id="java"></a>

<a id="java-h4"></a>

#### Java

<a id="a14509b864v6m"></a>

### 示例代码

<a id="code-block-9"></a>

```java
// dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    static {
        // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;

    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();

        if (reasoning!= null&&!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
            }
            System.out.print(reasoning);
        }

        if (content!= null&&!content.isEmpty()) {
            finalContent.append(content);
            if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
            }
            System.out.print(content);
        }
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("MiniMax-M2.5")
                .incrementalOutput(true)
                .resultFormat("message")
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }

    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("你是谁？").build();
            streamCallWithMessage(gen, userMsg);
            // 打印最终结果
            // if (reasoningContent.length() > 0) {
            //     System.out.println("\n====================完整回复====================");
            //     System.out.println(finalContent.toString());
            // }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="0a2fd0c94cpt2"></a>

### 返回结果

<a id="code-block-10"></a>

```text
====================思考过程====================

用户用中文问"你是谁"，意思是"你是谁？"或"Who are you?"

我应该用中文回复，介绍自己是一个AI助手。
====================完整回复====================

你好！我是 MiniMax-M2.5，一个AI助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？
```

<a id="http-2"></a>

<a id="http-2-h4"></a>

#### HTTP

<a id="67b33216b2wow"></a>

### 示例代码

<a id="sec-tabs-5"></a>

<a id="curl-2"></a>

<a id="curl-2-h4"></a>

#### curl

<a id="code-block-11"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "MiniMax-M2.5",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

<a id="1f41c33807oma"></a>

### 返回结果

<a id="code-block-12"></a>

```json
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "content": "你好！我是 MiniMax-M2.5，由 MiniMax 公司开发的 AI 助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？",
                    "reasoning_content": "用户用中文问\"你是谁？\"，意思是\"Who are you?\"\n\n我应该用中文回答，介绍自己。我应该说明我是MiniMax-M2.5，由MiniMax公司开发的AI助手。",
                    "role": "assistant"
                }
            }
        ]
    },
    "usage": {
        "input_tokens": 41,
        "output_tokens": 79,
        "output_tokens_details": {
            "reasoning_tokens": 39
        },
        "prompt_tokens_details": {
            "cached_tokens": 0
        },
        "total_tokens": 120
    },
    "request_id": "1bbd770e-564a-4601-83fc-3bf639423xxx"
}
```

<a id="anthropic兼容"></a>

<a id="anthropic兼容-h4"></a>

#### Anthropic兼容

<a id="sec-tabs-6"></a>

<a id="python-3"></a>

<a id="python-3-h4"></a>

#### Python

<a id="mm_anthropic_py_code_h3"></a>

### 示例代码

<a id="code-block-13"></a>

```python
import anthropic
import os

client = anthropic.Anthropic(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
)

message = client.messages.create(
    model="MiniMax-M2.5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "你是谁"}
    ],
    stream=True,
)

for event in message:
    if event.type == "content_block_delta":
        if hasattr(event.delta, "thinking"):
            print(event.delta.thinking, end="", flush=True)
        if hasattr(event.delta, "text"):
            print(event.delta.text, end="", flush=True)
```

<a id="http-3"></a>

<a id="http-3-h4"></a>

#### HTTP

<a id="mm_anthropic_curl_code_h3"></a>

### 示例代码

<a id="sec-tabs-7"></a>

<a id="curl-3"></a>

<a id="curl-3-h4"></a>

#### curl

<a id="code-block-14"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "anthropic-version: 2023-06-01" \
-d '{
    "model": "MiniMax-M2.5",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": "你是谁"
        }
    ]
}'
```

<a id="其它功能"></a>

<a id="d062ed0e4d5fe"></a>

## 其它功能

<table><thead><tr><th><strong>模型</strong></th><th><p><a href="../../model-experience/text-generation-model/multi-round-conversation.md">多轮对话</a></p></th><th><p><a href="../../model-experience/text-generation-model/deep-thinking.md">深度思考</a></p></th><th><p><a href="../../model-experience/text-generation-model/tool-calls/qwen-function-calling.md">Function Calling</a></p></th><th><p><a href="../../model-experience/text-generation-model/qwen-structured-output.md">结构化输出</a></p></th><th><p><a href="../../model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a></p></th><th><p><a href="../../model-experience/text-generation-model/partial-mode.md">前缀续写</a></p></th><th><p><a href="../../model-experience/text-generation-model/context-cache.md">上下文缓存</a></p></th></tr></thead><tbody><tr><td><p>MiniMax-M2.5</p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>支持</p></td><td><p>不支持</p></td><td><p>支持</p></td><td><p>不支持</p></td><td><p>支持</p><blockquote><p>仅支持隐式缓存</p></blockquote></td></tr></tbody></table>

<a id="参数默认值"></a>

<a id="20f0ad5093srb"></a>

## 参数默认值

| 模型 | temperature | top\_p | presence\_penalty |
| --- | --- | --- | --- |
| MiniMax-M2.5 | 1.0 | 0.95 | 0.0 |

<a id="模型列表与计费"></a>

<a id="m7n8o9p0q1r2s6"></a>

## 模型列表与计费

MiniMax-M2.5 模型擅长编程、办公、文本摘要等任务，且输出速度快，推荐使用。

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。

按照模型的输入与输出 Token 数量计费。

<a id="错误码"></a>

<a id="e592dd2ca4qfl"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../../model-api-reference/preparations/error-code.md)进行解决。
