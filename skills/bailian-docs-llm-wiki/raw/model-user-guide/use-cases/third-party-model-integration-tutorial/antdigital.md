# Ling-蚂蚁数科

本文档介绍如何在阿里云百炼平台调用蚂蚁数科直供的 Ling 系列模型推理服务。

**重要**本文档描述的功能仅在华北2（北京）地域可用，如需使用模型，需从华北2（北京）地域[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

## 服务开通

1.  前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 Ling，找到 antdigital/Ling-3.1-flash 模型卡片，单击立即开通；
2.  在弹窗内确认开通及授权。

完成以上步骤即可调用蚂蚁数科提供的 Ling 模型服务。

## 快速开始

**前提条件**

-   需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
-   如果通过SDK调用，需要[安装SDK](raw/model-api-reference/preparations/install-sdk.md)

antdigital/Ling-3.1-flash 是蚂蚁数科直供的混合思考模型，仅支持文本输入，默认开启思考模式：

-   **思考模式**（默认，或 `enable_thinking: true`）：模型会输出推理过程（`reasoning_content`）
-   **非思考模式**（`enable_thinking: false`）：直接输出结果，不包含推理过程

支持通过 `preserve_thinking` 参数在多轮对话中传递思考过程，详情请参见[传递思考过程](https://help.aliyun.com/zh/model-studio/deep-thinking#jln7docdq5et5)。

以下示例演示如何以流式输出调用思考模式的 antdigital/Ling-3.1-flash 模型。

**说明**

-   `enable_thinking` 非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。
-   流式输出时，`stream_options` 中的 `include_usage` 仅支持 `true`，传入 `false` 会报错。

#### Python

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "9.9和9.11哪个大？"}]
completion = client.chat.completions.create(
    model="antdigital/Ling-3.1-flash",
    messages=messages,
    stream=True,
    stream_options={
        "include_usage": True
    },
    # 默认开启思考模式，如需关闭可将 enable_thinking 设为 False
    extra_body={"enable_thinking": True}
)

reasoning_content = ""  # 完整思考过程
answer_content = ""  # 完整回复
is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    if not chunk.choices:
        print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
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

#### Node.js

```
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
    try {
        const messages = [{ role: 'user', content: '9.9和9.11哪个大？' }];

        const stream = await openai.chat.completions.create({
            model: 'antdigital/Ling-3.1-flash',
            messages,
            stream: true,
            stream_options: {
                include_usage: true
            },
            // 默认开启思考模式，如需关闭可将 enable_thinking 设为 false
            enable_thinking: true
        });

        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\n' + '='.repeat(20) + 'Token 消耗' + '='.repeat(20) + '\n');
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

#### curl

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "antdigital/Ling-3.1-flash",
    "messages": [
        {
            "role": "user",
            "content": "9.9和9.11哪个大？"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true
}'
```

## 其它功能

功能

支持情况

备注

[多轮对话](raw/model-user-guide/model-experience/text-generation-model/multi-round-conversation.md)

支持

—

[Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)

支持

支持通过 `tool_stream` 以流式方式返回工具入参；不支持 `parallel_tool_calls`

[前缀续写](raw/model-user-guide/model-experience/text-generation-model/partial-mode.md)

支持

—

[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)

支持

隐式缓存，命中缓存的输入 Token 按输入价格的 20% 计费

[结构化输出](raw/model-user-guide/model-experience/text-generation-model/qwen-structured-output.md)

支持

`response_format` 仅支持 `{"type": "json_object"}`，不支持 `json_schema`

[联网搜索](raw/model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md)

不支持

—

多模态输入

不支持

仅支持文本输入

antdigital/Ling-3.1-flash 不支持以下参数：`thinking_budget`、`reasoning_effort`、`parallel_tool_calls`、`seed`、`logprobs`、`top_logprobs`、`enable_code_interpreter`、`enable_search`、`search_options`、`skill`。

## 模型列表与计费

模型

说明

[antdigital/Ling-3.1-flash](raw/model-user-guide/support/model-studio-model-list/model-list-text-generation/ling-3-1-flash-by-antdigital.md)

混合思考模型，默认开启思考模式，上下文长度为 1048576 Token

模型价格与限流请参见[模型价格](raw/model-user-guide/test-1/model-pricing.md)和[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
