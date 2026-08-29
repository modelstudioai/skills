# Unisound-云知声

本文档介绍如何在阿里云百炼平台调用云知声直供的 U2 系列模型推理服务。

**重要**本文档描述的功能仅在华北2（北京）地域可用，如需使用模型，需从华北2（北京）地域[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

## 快速开始

unisound/unisound-u2 是云知声直供的推理模型，默认开启思考模式。通过 `thinking` 参数控制是否开启思考模式：传入 `{"type": "enabled"}` 开启，传入 `{"type": "disabled"}` 关闭；通过 `reasoning_effort` 控制思考强度。运行以下代码快速调用思考模式的 unisound/unisound-u2 模型。

需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。如果通过SDK调用，需要[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

**说明**`thinking` 与 `reasoning_effort` 非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。

#### Python

### 示例代码

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
    model="unisound/unisound-u2",
    messages=messages,
    stream=True,
    stream_options={
        "include_usage": True
    },
    # unisound-u2 默认开启思考模式，如需关闭可将 thinking 改为 {"type": "disabled"}
    extra_body={
        "thinking": {"type": "enabled"},
        "reasoning_effort": "xhigh"
    }
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

### 返回结果

```
====================思考过程====================

用户想比较 9.9 和 9.11 的大小。
把两个数对齐小数位：9.9 = 9.90，9.11 = 9.11。
比较小数部分：0.90 > 0.11，所以 9.9 更大。
====================完整回复====================

9.9 更大。

将两个数对齐小数位后比较：9.9 = 9.90，9.11 = 9.11。小数部分 0.90 > 0.11，因此 9.9 > 9.11。
====================Token 消耗====================

CompletionUsage(completion_tokens=96, prompt_tokens=10, total_tokens=106, prompt_tokens_details={'cached_tokens': 0})
```

#### Node.js

### 示例代码

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
            model: 'unisound/unisound-u2',
            messages,
            stream: true,
            stream_options: {
                include_usage: true
            },
            // unisound-u2 默认开启思考模式，如需关闭可改为 thinking: { type: 'disabled' }
            thinking: { type: 'enabled' },
            reasoning_effort: 'xhigh'
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

### 返回结果

```
====================思考过程====================

用户想比较 9.9 和 9.11 的大小。
把两个数对齐小数位：9.9 = 9.90，9.11 = 9.11。
比较小数部分：0.90 > 0.11，所以 9.9 更大。
====================完整回复====================

9.9 更大。

将两个数对齐小数位后比较：9.9 = 9.90，9.11 = 9.11。小数部分 0.90 > 0.11，因此 9.9 > 9.11。
====================Token 消耗====================

{ prompt_tokens: 10, completion_tokens: 96, total_tokens: 106, prompt_tokens_details: { cached_tokens: 0 } }
```

#### HTTP

### 示例代码

#### curl

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "unisound/unisound-u2",
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
    "thinking": {
        "type": "enabled"
    },
    "reasoning_effort": "xhigh"
}'
```

## 其它功能

**功能**

**支持情况**

**备注**

[多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation)

支持

—

[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)

支持

不支持通过 `tool_stream` 以流式方式返回工具入参

[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)

支持

`response_format` 仅支持 `{"type": "text"}` 和 `{"type": "json_object"}`，不支持 json\_schema

[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)

不支持

—

多模态输入

不支持

仅支持文本输入

unisound/unisound-u2 不支持以下参数：`n`、`stop`、`preserve_thinking`、`thinking_budget`、`tool_stream`、`enable_code_interpreter`、`enable_search`、`search_options`、`skill`。

支持的参数中，部分参数取值范围与功能与百炼不一致：

**参数**

**百炼**

**U2**

`temperature`

取值范围 \[0, 2)

取值范围 \[0, 2)，默认 1.0

`top_k`

取值为大于或等于 0 的整数；设为 null 或大于 100 时禁用 top\_k 策略

取值必须为大于或等于 1 的整数，默认 40

`thinking`

通过 `enable_thinking` 控制是否开启思考模式

默认开启思考模式；通过 `thinking`（取值 `{"type": "enabled"}` 或 `{"type": "disabled"}`）控制是否开启思考模式，并通过 `reasoning_effort` 控制思考强度

## 模型列表与计费

U2 系列模型是云知声直供的推理模型，默认开启思考模式。

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
