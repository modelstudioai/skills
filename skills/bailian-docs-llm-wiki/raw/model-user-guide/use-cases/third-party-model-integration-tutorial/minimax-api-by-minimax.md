# MiniMax

本文档介绍如何在阿里云百炼平台调用稀宇科技（简称MiniMax）直供的模型推理服务。

**重要**本文档描述的功能仅在华北2（北京）地域可用，如需使用模型，需从华北2（北京）地域[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

## 服务开通

1.  前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 MiniMax，找到 MiniMax 模型卡片，单击立即开通；
2.  在弹窗内确认开通及授权。

完成以上步骤即可调用MiniMax提供的 MiniMax 模型服务。

## 快速开始

API 使用前提：已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，需要[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

#### OpenAI兼容

#### Python

### 示例代码

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
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

### 返回结果

```
====================思考过程====================

用户问我是谁。根据系统提示，我应该以"MiniMax-M2.7"的身份回应，并且提到我是由MiniMax公司开发的。

这是一个简单的自我介绍问题，我应该简洁明了地回答。

====================完整回复====================

你好！我是 **MiniMax-M2.7**，由 **MiniMax** 公司开发的AI助手。

我可以帮助你回答问题、提供信息、进行对话等各种任务。有什么我可以帮助你的吗？
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

### 返回结果

```
====================思考过程====================

用户问我是谁。根据系统提示，我应该以"MiniMax-M2.7"的身份回应，并且提到我是由MiniMax公司开发的。

这是一个简单的自我介绍问题，我应该简洁明了地回答。

====================完整回复====================

你好！我是 **MiniMax-M2.7**，由 **MiniMax** 公司开发的AI助手。

我可以帮助你回答问题、提供信息、进行对话等各种任务。有什么我可以帮助你的吗？
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
    "model": "MiniMax/MiniMax-M2.7",
    "messages": [
        {
            "role": "user",
            "content": "你是谁"
        }
    ]
}'
```

### 返回结果

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

## MiniMax-M3.1-Flash 与 MiniMax-M3 的差异

能力

MiniMax/MiniMax-M3.1-Flash

MiniMax/MiniMax-M3

思考模式

始终开启，不可关闭

默认自适应思考，可关闭

思考深度

支持 `low`、`medium`、`high`、`xhigh`、`max`，默认 `max`

不支持 `reasoning_effort`

思考内容

始终通过 `reasoning_content` 字段单独返回，不支持将 `reasoning_split` 设为 `false`

`reasoning_split` 为 `true` 时通过 `reasoning_content` 单独返回，为 `false` 时在 `content` 中以 `<think>` 标签返回

上下文窗口

1M Token

1M Token

图片和视频输入

支持

支持

Prompt 缓存

支持

支持

默认限流

200 RPM、10,000,000 TPM

500 RPM、20,000,000 TPM

实际服务可能同时按 RPS（RPM/60）与 TPS（TPM/60）执行每秒限流，具体规则请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

使用以下示例调用 MiniMax/MiniMax-M3.1-Flash，并通过 `reasoning_effort` 设置思考深度：

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

response = client.chat.completions.create(
    model="MiniMax/MiniMax-M3.1-Flash",
    reasoning_effort="max",
    messages=[{"role": "user", "content": "分析采用微服务架构的主要权衡。"}],
)

print(response.choices[0].message.reasoning_content)
print(response.choices[0].message.content)
```

### 从 MiniMax-M3 迁移

仅将模型 ID 更换为 `MiniMax/MiniMax-M3.1-Flash` 时，请同步检查以下差异：

-   删除 `thinking: {"type":"disabled"}` 或 `reasoning_effort: "none"`。MiniMax-M3.1-Flash 不支持关闭思考，传入上述参数会返回 400 错误。
-   不要将 `reasoning_split` 设为 `false`。共用 MiniMax-M3 和 MiniMax-M3.1-Flash 调用代码时，可将其设为 `true`，并统一从 `reasoning_content` 读取思考内容。使用 OpenAI Python SDK 时，通过 `extra_body={"reasoning_split": True}` 传入；通过 HTTP 调用时，将其放在请求体顶层。`thinking` 参数的位置与之相同。
-   从 `reasoning_content` 字段读取思考内容，不要读取 `reasoning_details`。兼容 MiniMax-M3 时，应先判断 `reasoning_content` 是否存在；MiniMax-M3.1-Flash 无需解析 `content` 中的 `<think>` 标签。
-   为输出预留足够长度。思考内容计入 `max_tokens` 或 `max_completion_tokens`，上限过小可能导致 `finish_reason` 为 `length` 且回答为空。
-   多轮 Function Calling 时，将包含 `reasoning_content` 和 `tool_calls` 的完整 assistant 消息加入对话历史，以保持思考过程连续。

## 多模态调用示例

MiniMax/MiniMax-M3.1-Flash 和 MiniMax/MiniMax-M3 均支持文本、图片和视频输入，并输出文本。

**重要**

-   MiniMax/MiniMax-M3.1-Flash 始终开启思考，可通过 `reasoning_effort` 调整思考深度。
-   MiniMax/MiniMax-M3 通过 `thinking` 参数控制思考模式，默认值为 `adaptive`；设置为 `disabled` 可关闭思考。

### 图像理解

图像理解功能让 MiniMax/MiniMax-M3.1-Flash 和 MiniMax/MiniMax-M3 能够识别和分析单张或多张图像。以下示例使用 MiniMax/MiniMax-M3；如需使用 MiniMax/MiniMax-M3.1-Flash，请更换模型 ID，并可通过 `reasoning_effort` 调整思考深度。

#### OpenAI兼容

**说明**`thinking`非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body`传入，Node.js SDK中作为顶层参数传入。

#### Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 单图传入示例（自适应思考模式）
completion = client.chat.completions.create(
    model="MiniMax/MiniMax-M3",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "图中描绘的是什么景象?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    }
                }
            ]
        }
    ],
    extra_body={"thinking": {"type": "adaptive"}}  # 自适应思考模式
)

# 输出思考过程
if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    print(completion.choices[0].message.reasoning_content)

# 输出回复内容
print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
print(completion.choices[0].message.content)

# 多图传入示例（开启思考模式，取消注释使用）
# completion = client.chat.completions.create(
#     model="MiniMax/MiniMax-M3",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "这些图描绘了什么内容？"},
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"}
#                 }
#             ]
#         }
#     ],
#     extra_body={"thinking": {"type": "adaptive"}}
# )
#
# # 输出思考过程和回复
# if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
#     print("\n思考过程：\n" + completion.choices[0].message.reasoning_content)
# print("\n完整回复：\n" + completion.choices[0].message.content)
```

#### Node.js

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

// 单图传入示例（自适应思考模式）
const completion = await openai.chat.completions.create({
    model: 'MiniMax/MiniMax-M3',
    messages: [
        {
            role: 'user',
            content: [
                { type: 'text', text: '图中描绘的是什么景象?' },
                {
                    type: 'image_url',
                    image_url: {
                        url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg'
                    }
                }
            ]
        }
    ],
    thinking: {"type": "adaptive"}  // 自适应思考模式
});

// 输出思考过程
if (completion.choices[0].message.reasoning_content) {
    console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');
    console.log(completion.choices[0].message.reasoning_content);
}

// 输出回复内容
console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
console.log(completion.choices[0].message.content);

// 多图传入示例（开启思考模式，取消注释使用）
// const multiCompletion = await openai.chat.completions.create({
//     model: 'MiniMax/MiniMax-M3',
//     messages: [
//         {
//             role: 'user',
//             content: [
//                 { type: 'text', text: '这些图描绘了什么内容？' },
//                 {
//                     type: 'image_url',
//                     image_url: { url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg' }
//                 },
//                 {
//                     type: 'image_url',
//                     image_url: { url: 'https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png' }
//                 }
//             ]
//         }
//     ],
//     thinking: {"type": "adaptive"}
// });
//
// // 输出思考过程和回复
// if (multiCompletion.choices[0].message.reasoning_content) {
//     console.log('\n思考过程：\n' + multiCompletion.choices[0].message.reasoning_content);
// }
// console.log('\n完整回复：\n' + multiCompletion.choices[0].message.content);
```

#### HTTP

#### curl

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "MiniMax/MiniMax-M3",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "图中描绘的是什么景象?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    }
                }
            ]
        }
    ],
    "thinking": {"type": "adaptive"}
}'

# 多图输入示例（取消注释使用）
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
# -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
# -H "Content-Type: application/json" \
# -d '{
#     "model": "MiniMax/MiniMax-M3",
#     "messages": [
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "这些图描绘了什么内容？"
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
#                     }
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"
#                     }
#                 }
#             ]
#         }
#     ],
#     "thinking": {"type": "adaptive"}
# }'
```

### 视频理解

#### OpenAI兼容

#### Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="MiniMax/MiniMax-M3",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "video_url",
                    "video_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                    "fps": 2
                },
                {
                    "type": "text",
                    "text": "这段视频的内容是什么?"
                }
            ]
        }
    ]
)

print(completion.choices[0].message.content)
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "MiniMax/MiniMax-M3",
        messages: [
            {
                role: "user",
                content: [
                    {
                        type: "video_url",
                        video_url: {
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                        },
                        fps: 2
                    },
                    {
                        type: "text",
                        text: "这段视频的内容是什么?"
                    }
                ]
            }
        ]
    });

    console.log(response.choices[0].message.content);
}

main();
```

#### HTTP

#### curl

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "MiniMax/MiniMax-M3",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
            },
            "fps": 2
          },
          {
            "type": "text",
            "text": "这段视频的内容是什么?"
          }
        ]
      }
    ]
  }'
```

### 文件限制

#### 图像文件

-   **传入方式：**支持通过公网URL或Base64编码传入。
-   **支持的图像格式：**PNG、JPEG、WEBP、GIF
-   **图像大小：**单张图片不超过10MB。

#### 视频文件

-   **视频大小与时长：**视频文件不超过50MB，时长不超过30分钟。
-   **视频格式：**MP4、AVI、MOV、MKV。
-   **音频理解：**不支持对视频文件的音频进行理解。

## 其它功能

MiniMax/MiniMax-M3.1-Flash 支持多轮对话、深度思考、Function Calling 和上下文缓存。

模型

[多轮对话](raw/model-user-guide/model-experience/text-generation-model/multi-round-conversation.md)

[深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)

[Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)

[结构化输出](raw/model-user-guide/model-experience/text-generation-model/qwen-structured-output.md)

[联网搜索](raw/model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md)

[前缀续写](raw/model-user-guide/model-experience/text-generation-model/partial-mode.md)

[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)

MiniMax/MiniMax-M3.1-Flash

支持

支持

支持

不支持

不支持

不支持

支持

MiniMax/MiniMax-M3

支持

支持

支持

不支持

不支持

不支持

支持

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

上下文缓存类型为隐式缓存，自动开启，与阿里云百炼的[隐式缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)服务有以下不同：

-   MiniMax/MiniMax-M3.1-Flash、MiniMax/MiniMax-M2.5 命中缓存的输入 Token 折扣为 10%，MiniMax/MiniMax-M3、MiniMax/MiniMax-M2.7 折扣为 20%。MiniMax/MiniMax-M3、MiniMax/MiniMax-M2.7 和 MiniMax/MiniMax-M2.5 的缓存最少 Token 数为 512（百炼为 1024）。
-   MiniMax/MiniMax-M3.1-Flash 和 MiniMax/MiniMax-M3 的 `n` 参数仅支持 `1`，即每次请求只能生成一条回复。
-   MiniMax/MiniMax-M3.1-Flash 不支持 `stop`。传入后不会按指定停止词截断输出；请求可能仍成功且返回 `finish_reason: "stop"`，但这不表示指定停止词已生效。
-   MiniMax/MiniMax-M3.1-Flash 不支持通过 `parallel_tool_calls` 控制工具调用的并行性。设置为 `false` 也不能保证串行调用，模型仍可能在一轮中返回多个 `tool_calls`。
-   MiniMax/MiniMax-M3.1-Flash 的 `tool_choice` 仅支持 `auto`。其他取值可能报错或不生效，例如指定函数名称不能保证模型调用该函数。MiniMax/MiniMax-M3 的 `tool_choice` 仅支持 `none` 和 `auto`。

## 参数默认值

> 当前不支持修改以下参数

模型

`temperature`

`top_p`

MiniMax/MiniMax-M3.1-Flash

1.0

0.95

MiniMax/MiniMax-M3

1.0

0.95

MiniMax/MiniMax-M2.7

1.0

0.9

MiniMax/MiniMax-M2.5

1.0

0.9

## 模型列表与计费

MiniMax-M3.1-Flash 是最新多模态推理模型，支持 100 万 Token 上下文、图像和视频理解以及五档思考深度，推荐用于复杂 Agentic 任务、软件开发和网络安全等场景。MiniMax-M3 支持关闭思考模式，适用于需要在思考和非思考模式间切换的场景；MiniMax-M2.7 擅长编程、文本摘要等任务。

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。

按照模型的输入与输出 Token 数量计费。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
