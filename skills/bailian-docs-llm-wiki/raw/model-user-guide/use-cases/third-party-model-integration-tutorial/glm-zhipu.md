# GLM-智谱

本文档介绍如何在阿里云百炼平台调用智谱直供的模型推理服务。

> 阿里云百炼提供两个推理服务供应商的GLM模型服务，智谱供应商支持更长回复长度；[阿里云百炼](bailian.aliyun.com)供应商提供免费额度，且采取阶梯计费策略。

**重要**

本文档仅适用于“中国内地（北京）”地域。如需使用模型，需使用“中国内地（北京）”地域的[API Key](https://bailian.console.alibabacloud.com/?tab=model#/api-key)。

## **服务开通**

1.  前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 ZHIPU/GLM-5，找到智谱GLM系列文本模型卡片，单击立即开通；
    
2.  在弹窗内确认开通及授权。
    

完成以上步骤即可调用智谱提供的 GLM 模型服务。

## **快速开始**

glm-5.1 是 GLM 系列最新模型，支持通过`enable_thinking`参数设置思考与非思考模式。运行以下代码快速调用思考模式的 glm-5.1 模型。

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

messages = [{"role": "user", "content": "你是谁"}]
completion = client.chat.completions.create(
    model="ZHIPU/GLM-5.1",
    messages=messages,
    # 通过 extra_body 设置 enable_thinking 开启思考模式
    extra_body={"enable_thinking": True},
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

让我仔细思考用户提出的这个看似简单但实际上很有深度的问题。

从语言特点来看，用户使用的是中文，这意味着我应该用中文来回应。这是一个最基础的自我介绍问题，但背后可能包含着多层次的含义。

首先需要明确的是，作为一个语言模型，我应该诚实地说明自己的身份和本质。我既不是人类，也不具备真正的情感意识，而是一个由深度学习技术训练的AI助手。这是最基本的事实。

其次，考虑到用户可能的需求场景，他们或许想了解：
1. 我能提供什么样的服务
2. 我的专业领域是什么
3. 我的局限性在哪里
4. 如何与我更好地互动

在回答中，我应该既表达友好和开放的态度，又保持专业和准确。要说明自己擅长的主要领域，比如知识问答、写作辅助、创意支持等，但同时也要坦诚地指出自己的局限性，比如缺乏真实的情感体验。

此外，为了让回答更加完整，我还应该表达出愿意帮助用户解决问题的积极态度。可以适当引导用户提出更具体的问题，这样可以更好地展现自己的能力。

考虑到这是一个开放式的开场白，回答时既要简洁明了，又要包含足够的信息量，让用户对我的基本情况有一个清晰的认识，同时为后续的对话奠定良好的基础。

最后，语气应该保持谦逊和专业，既不过于技术化，也不显得过分随意，让用户感到舒适和自然。
====================完整回复====================

我是智谱AI训练的GLM大语言模型，旨在为用户提供信息和帮助解决问题。我被设计用来理解和生成人类语言，可以回答问题、提供解释或参与各类话题讨论。

我不会存储您的个人数据，我们的对话是匿名的。有什么我能帮您了解或探讨的话题吗？
====================Token 消耗====================

CompletionUsage(completion_tokens=344, prompt_tokens=7, total_tokens=351, completion_tokens_details=None, prompt_tokens_details=None)
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
        const messages = [{ role: 'user', content: '你是谁' }];
        
        const stream = await openai.chat.completions.create({
            model: 'ZHIPU/GLM-5.1',
            messages,
            // 注意：在 Node.js SDK，enable_thinking 这样的非标准参数作为顶层属性传递，无需放在 extra_body 中
            enable_thinking: true,
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

让我仔细思考用户的问题"你是谁"。这需要从多个角度来分析和回应。

首先，这是一个基础的身份认知问题。作为GLM大语言模型，需要准确表达自己的身份定位。应该清晰地说明自己是由智谱AI开发的AI助手。

其次，思考用户提出这个问题的可能意图。他们可能是初次接触，想了解基本功能；也可能想确认是否能提供特定帮助；或者只是想测试回应方式。因此需要给出一个开放且友好的回答。

还要考虑回答的完整性。除了身份介绍，也应该简要说明主要功能，如问答、创作、分析等，让用户了解可以如何使用这个助手。

最后，要确保语气友好亲和，表达出乐于帮助的态度。可以用"很高兴为您服务"这样的表达，让用户感受到交流的温暖。

基于这些思考，可以组织一个简洁明了的回答，既能回答用户问题，又能引导后续交流。
====================完整回复====================

我是GLM，由智谱AI训练的大语言模型。我通过大规模文本数据训练，能够理解和生成人类语言，帮助用户回答问题、提供信息和进行对话交流。

我会持续学习和改进，以提供更好的服务。很高兴能为您解答问题或提供帮助！有什么我能为您做的吗？
====================Token 消耗====================

{ prompt_tokens: 7, completion_tokens: 248, total_tokens: 255 }
```

## HTTP

### **示例代码**

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "ZHIPU/GLM-5.1",
    "messages": [
        {
            "role": "user", 
            "content": "你是谁"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true
}'
```

## **流式工具调用**

glm-5.1、glm-5支持`tool_stream`参数（boolean，默认`false`），仅在`stream`为`true`时生效。开启后，Function Calling 返回的 tool\_call 参数（arguments）会以流式增量方式逐步返回。

`stream`与`tool_stream`的组合行为如下：

**stream**

**tool\_stream**

**tool\_call 返回方式**

true

true

arguments 以增量方式分多个 chunk 返回

true

false（默认）

arguments 在一个 chunk 中完整返回

false

true/false

tool\_stream 不生效，arguments 在完整响应中一次性返回

## OpenAI兼容

## Python

### **示例代码**

```
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    }
]

messages = [{"role": "user", "content": "北京天气怎么样"}]

completion = client.chat.completions.create(
    model="ZHIPU/GLM-5.1",
    tools=tools,
    messages=messages,
    extra_body={
        "tool_stream": True,
    },
    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        delta = chunk.choices[0].delta
        if hasattr(delta, 'content') and delta.content:
            print(f"[content] {delta.content}")
        if hasattr(delta, 'tool_calls') and delta.tool_calls:
            for tc in delta.tool_calls:
                print(f"[tool_call] id={tc.id}, name={tc.function.name}, args={tc.function.arguments}")
        if chunk.choices[0].finish_reason:
            print(f"[finish_reason] {chunk.choices[0].finish_reason}")
    if not chunk.choices and chunk.usage:
        print(f"[usage] {chunk.usage}")
```

## Node.js

### **示例代码**

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

const tools = [
    {
        type: "function",
        function: {
            name: "get_weather",
            description: "获取指定城市的天气信息",
            parameters: {
                type: "object",
                properties: {
                    city: { type: "string", description: "城市名称" }
                },
                required: ["city"]
            }
        }
    }
];

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'ZHIPU/GLM-5.1',
            messages: [{ role: 'user', content: '北京天气怎么样' }],
            tools: tools,
            tool_stream: true,
            stream: true,
            stream_options: {
                include_usage: true
            },
        });

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                if (chunk.usage) {
                    console.log(`[usage] ${JSON.stringify(chunk.usage)}`);
                }
                continue;
            }

            const delta = chunk.choices[0].delta;

            if (delta.content) {
                console.log(`[content] ${delta.content}`);
            }

            if (delta.tool_calls) {
                for (const tc of delta.tool_calls) {
                    console.log(`[tool_call] id=${tc.id}, name=${tc.function.name}, args=${tc.function.arguments}`);
                }
            }

            if (chunk.choices[0].finish_reason) {
                console.log(`[finish_reason] ${chunk.choices[0].finish_reason}`);
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "ZHIPU/GLM-5.1",
    "messages": [
        {
            "role": "user",
            "content": "北京天气怎么样"
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取指定城市的天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "城市名称"}
                    },
                    "required": ["city"]
                }
            }
        }
    ],
    "stream": true,
    "stream_options": {"include_usage": true},
    "tool_stream": true
}'
```

## **其它功能**

**模型**

[多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation)

[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling#dd5a3dca390k9)

[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)

[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)

[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)

[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)

ZHIPU/GLM-5.1

支持

支持

支持

> 仅非思考模式

不支持

不支持

支持

ZHIPU/GLM-5

支持

支持

支持

> 仅非思考模式

不支持

不支持

支持

上下文缓存类型为隐式缓存，自动开启，与阿里云百炼的[隐式缓存](https://help.aliyun.com/zh/model-studio/context-cache)服务有以下不同：

-   命中缓存的输入 Token 折扣为 25%（百炼为 20%）；
    
-   缓存最少 Token 数为 512（百炼为 256）。
    

## **参数默认值**

**模型**

**enable\_thinking**

**temperature**

**top\_p**

**top\_k**

**repetition\_penalty**

ZHIPU/GLM-5.1

true

1.0

0.95

\-

\-

ZHIPU/GLM-5

true

1.0

0.95

\-

\-

\-表示没有默认值，也不支持设置。

## **模型列表与计费**

GLM 系列模型是智谱AI专为智能体设计的混合推理模型，提供思考与非思考两种模式。

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## **错误码**

如果执行报错，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

以下为智谱独有的业务错误码。HTTP 错误码与百炼通用错误码一致，请参见上述链接。

**错误分类**

**错误码**

**错误信息**

基础错误

500

内部错误

身份验证错误

1000

身份验证失败

1001

Header 中未收到 Authentication 参数，无法进行身份验证

1002

Authentication Token 非法，请确认 Authentication Token 正确传递

1003

Authentication Token 已过期，请重新生成/获取

1004

通过 Authentication Token 的验证失败

1100

账户读写

账户错误

1110

您的账户当前处于非活动状态。请检查账户信息

1111

您的账户不存在

1112

您的账户已被锁定，请联系客服解锁

1113

您的账户已欠费，请充值后重试

1120

无法成功访问您的账户，请稍后重试

1121

账户存违规行为，账号已被锁定

API 调用错误

1200

API 调用错误

1210

API 调用参数有误，请检查文档

1211

模型不存在，请检查模型代码

1212

当前模型不支持 `${method}` 调用方式

1213

未正常接收到 `${field}` 参数

1214

`${field}` 参数非法。请检查文档

1215

`${field1}` 与 `${field2}` 不能同时设置，请检查文档

1220

您无权访问 `${API_name}`

1221

API `${API_name}` 已下线

1222

API `${API_name}` 不存在

1230

API 调用流程出错

1231

您已有请求：`${request_id}`

1234

网络错误，错误id：`${error_id}`，请联系客服

1261

Prompt 超长

API 策略阻止错误

1300

API 调用被策略阻止

1301

系统检测到输入或生成内容可能包含不安全或敏感内容，请您避免输入易产生敏感内容的提示语，感谢您的配合

1302

您当前使用该 API 的并发数过高，请降低并发，或联系客服增加限额

1303

您当前使用该 API 的频率过高，请降低频率，或联系客服增加限额

1304

该 API 已达今日调用次数限额，如有更多需求，请联系客服购买

1305

该 API 已触发流量限制

1308

已达到 `${number}` `${unit}` 的使用上限。您的限额将在 `${next_flush_time}` 重置

1309

您的 GLM Coding Plan 套餐已到期，暂无法使用，前往官方续订后即可恢复 [**https://bigmodel.cn/claude-code**](https://bigmodel.cn/claude-code)

1310

您已达到每周/每月使用上限，您的限额将在 `${next_flush_time}` 重置

1311

当前订阅套餐暂未开放`${model_name}`权限

1312

该模型当前访问量过大，请您稍后再试，或切换其他模型如 `${model_name}` 等

1313

您的账户当前使用模式不符合公平使用策略，请求频率已受到限制。详情请参阅《条款与协议-订阅及自动续费协议》，如需恢复请前往个人中心-编程套餐总览-顶部申请解除限制
