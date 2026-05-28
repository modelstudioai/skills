# MiMo-小米

本文档介绍如何在阿里云百炼平台调用小米直供的 MiMo 系列模型推理服务。

**重要**

本文档仅适用于“中国内地（北京）”地域。如需使用模型，需使用“中国内地（北京）”地域的[API Key](https://bailian.console.alibabacloud.com/?tab=model#/api-key)。

## **快速开始**

mimo-v2.5-pro 是小米直供的混合推理模型，默认开启思考模式（`enable_thinking`默认为`true`），如需直接输出结果可显式传入`enable_thinking: false`。运行以下代码快速调用思考模式的 mimo-v2.5-pro 模型。

需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk#8833b9274f4v8)。

## OpenAI兼容

**说明**

`enable_thinking`非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body`传入，Node.js SDK 作为顶层参数传入。

## Python

### **示例代码**

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [{"role": "user", "content": "1+1 等于多少？"}]
completion = client.chat.completions.create(
    model="xiaomi/mimo-v2.5-pro",
    messages=messages,
    # mimo-v2.5-pro 默认开启思考模式，如需关闭可改为 {"enable_thinking": False}
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

### **返回结果**

```
====================思考过程====================

用户问了一个简单的算术问题：1+1等于多少。
这是最基础的加法运算，答案是 2。我直接给出答案并简要说明即可。
====================完整回复====================

1+1 等于 2。这是最基本的加法运算。
====================Token 消耗====================

CompletionUsage(completion_tokens=42, prompt_tokens=9, total_tokens=51, prompt_tokens_details={'cached_tokens': 0})
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
    try {
        const messages = [{ role: 'user', content: '1+1 等于多少？' }];

        const stream = await openai.chat.completions.create({
            model: 'xiaomi/mimo-v2.5-pro',
            messages,
            // mimo-v2.5-pro 默认开启思考模式，如需关闭可改为 enable_thinking: false
            stream: true,
            stream_options: {
                include_usage: true
            },
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

### **返回结果**

```
====================思考过程====================

用户问了一个简单的算术问题：1+1等于多少。
这是最基础的加法运算，答案是 2。我直接给出答案并简要说明即可。
====================完整回复====================

1+1 等于 2。这是最基本的加法运算。
====================Token 消耗====================

{ prompt_tokens: 9, completion_tokens: 42, total_tokens: 51, prompt_tokens_details: { cached_tokens: 0 } }
```

## HTTP

### **示例代码**

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "xiaomi/mimo-v2.5-pro",
    "messages": [
        {
            "role": "user",
            "content": "1+1 等于多少？"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    }
}'
```

## **其它功能**

**功能**

**支持情况**

**备注**

[多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation)

支持

思考模式下需在每轮 assistant 消息中保留 `reasoning_content` 字段，否则会报错

[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling#dd5a3dca390k9)

支持

`tool_choice` 仅支持 `auto`；工具函数名只能包含 a-z、A-Z、0-9、下划线、连字符，最大长度 64

[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)

支持

隐式缓存，自动开启

[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)

支持

`response_format`不支持 json\_schema

[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)

不支持

—

[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)

不支持

—

多模态输入

不支持

—

mimo-v2.5-pro 不支持以下参数：`top_k`、`reasoning_effort`、`thinking_budget`、`modalities`、`repetition_penalty`、`vl_high_resolution_images`、`preserve_thinking`、`tool_stream`、`enable_code_interpreter`、`parallel_tool_calls`、`seed`、`logprobs`、`top_logprobs`、`n`、`audio`、`enable_search`、`search_options`、`X-DashScope-DataInspection`、`skill`。

支持的参数中，部分参数取值范围与功能与百炼不一致：

**参数**

**百炼**

**MiMo**

`temperature`

范围为 \[0, 2)

范围 \[0, 1.5\]，默认 1.0

`top_p`

范围为 (0, 1.0\]

范围 \[0.01, 1.0\]，默认 0.95

`presence_penalty`

—

范围为 \[-2, 2\]，默认值为 0

`stop`

—

最多 4 个序列

`max_tokens`

不限制模型思维链长度，仅限制输出长度

限制模型的输出和思维链长度

## **模型列表与计费**

MiMo 系列模型是小米直供的混合推理模型，提供思考与非思考两种模式。

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## **错误码**

MiMo 系列模型由小米直供，其错误码与百炼平台标准错误码存在差异。调用 MiMo 模型时，请以下表为准。

**错误码**

**错误原因**

**解决方法**

400 - 格式错误

请求体格式错误

-   检查 JSON 格式是否正确
    
-   检查是否包含所有必需参数
    
-   检查参数值是否在有效范围内
    
-   检查消息格式是否符合接口要求
    
-   检查字段是否输入正确
    
-   多轮对话思考模式下，需完整回传 `reasoning_content` 字段给接口
    

401 - 认证失败

缺少或无效的 API Key，或 Authorization 请求头格式错误

检查 API Key 及请求头格式是否正确

402 - 余额不足

账户余额不足

检查账户余额，及时进行充值

403 - 拒绝访问

服务暂不支持当前地区，或 API Key 被风控

新建 API Key，并注意输入内容安全

404 - 资源未找到

接口或模型不支持图像输入能力

确认使用的模型或接口是否支持多模态图像输入

421 - 内容拦截

内容审核拦截

避免输入不安全或敏感内容

429 - 请求超限

请求过于频繁

实现指数退避和重试逻辑，或降低请求频率

500 - 服务器失败

服务器内部故障

请稍后重试，或联系我们解决

503 - 服务器故障

服务器负载过高

请稍后重试
