# MiniMax

本文档介绍如何在阿里云百炼平台调用稀宇科技（简称MiniMax）直供的模型推理服务。

**重要**

本文档仅适用于中国内地地域。如需使用模型，需从中国内地地域[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## **服务开通**

1.  前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 MiniMax，找到 MiniMax 模型卡片，单击立即开通；
    
2.  在弹窗内确认开通及授权。
    

完成以上步骤即可调用MiniMax提供的 MiniMax 模型服务。

## **快速开始**

API 使用前提：已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk#8833b9274f4v8)。

## OpenAI兼容

## Python

### **示例代码**

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="MiniMax/MiniMax-M2.7",
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

### **返回结果**

```
====================思考过程====================

用户问我是谁。根据系统提示，我应该以"MiniMax-M2.7"的身份回应，并且提到我是由MiniMax公司开发的。

这是一个简单的自我介绍问题，我应该简洁明了地回答。

====================完整回复====================

你好！我是 **MiniMax-M2.7**，由 **MiniMax** 公司开发的AI助手。

我可以帮助你回答问题、提供信息、进行对话等各种任务。有什么我可以帮助你的吗？
```

## Node.js

### **示例代码**

```
import OpenAI from "openai";
import process from 'process';

// 初始化OpenAI客户端
const openai = new OpenAI({
    // 如果没有配置环境变量，请用阿里云百炼API Key替换：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = ''; // 完整思考过程
let answerContent = ''; // 完整回复
let isAnswering = false; // 是否进入回复阶段

async function main() {
    const messages = [{ role: 'user', content: '你是谁' }];

    const stream = await openai.chat.completions.create({
        model: 'MiniMax/MiniMax-M2.7',
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

### **返回结果**

```
====================思考过程====================

用户问我是谁。根据系统提示，我应该以"MiniMax-M2.7"的身份回应，并且提到我是由MiniMax公司开发的。

这是一个简单的自我介绍问题，我应该简洁明了地回答。

====================完整回复====================

你好！我是 **MiniMax-M2.7**，由 **MiniMax** 公司开发的AI助手。

我可以帮助你回答问题、提供信息、进行对话等各种任务。有什么我可以帮助你的吗？
```

## HTTP

### **示例代码**

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "MiniMax/MiniMax-M2.7",
    "messages": [
        {
            "role": "user", 
            "content": "你是谁"
        }
    ]
}'
```

### **返回结果**

```
{
    "choices": [
        {
            "message": {
                "content": "\n\n你好！我是一个AI助手，由MiniMax公司开发。我的名字是MiniMax-M2.7。\n\n我可以帮助你回答问题、提供信息、进行对话、协助写作、分析问题等各种任务。有什么我可以帮助你的吗？",
                "reasoning_content": "用户用中文问\"你是谁\"，意思是\"你是谁？\"或\"Who are you?\"\n\n我应该用中文回复，介绍我自己是一个AI助手。\n\n让我写一个简洁的自我介绍。",
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
        "completion_tokens": 84,
        "total_tokens": 124,
        "completion_tokens_details": {
            "reasoning_tokens": 36
        }
    },
    "created": 1769161313,
    "system_fingerprint": null,
    "model": "MiniMax/MiniMax-M2.7",
    "id": "chatcmpl-30d4de0f-92fe-93d2-a1bf-e8153ae937df"
}
```

## **其它功能**

**模型**

[多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation)

[深度思考](https://help.aliyun.com/zh/model-studio/deep-thinking)

[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)

[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)

[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)

[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)

[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)

MiniMax/MiniMax-M2.7

支持

支持

支持

不支持

不支持

不支持

支持

MiniMax/MiniMax-M2.5

支持

支持

支持

不支持

不支持

不支持

支持

MiniMax/MiniMax-M2.1

支持

支持

支持

不支持

不支持

不支持

支持

上下文缓存类型为隐式缓存，自动开启，与阿里云百炼的[隐式缓存](https://help.aliyun.com/zh/model-studio/context-cache)服务有以下不同：

-   MiniMax/MiniMax-M2.7 命中缓存的输入 Token 折扣为 20%，MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1 折扣为 10%；
    
-   缓存最少 Token 数为 512（百炼为 256）。
    

## **参数默认值**

> 当前不支持修改以下参数

**模型**

**temperature**

**top\_p**

MiniMax/MiniMax-M2.7

1.0

0.9

MiniMax/MiniMax-M2.5

1.0

0.9

MiniMax/MiniMax-M2.1

1.0

0.9

## **模型列表与计费**

MiniMax-M2.7 模型，擅长编程、文本摘要等任务，推荐使用。

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。

按照模型的输入与输出 Token 数量计费。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
