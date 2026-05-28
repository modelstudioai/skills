# Kimi-月之暗面

本文档介绍如何在阿里云百炼平台调用月之暗面（Moonshot AI）直供的模型推理服务。

**重要**

本文档仅适用于“中国内地（北京）”地域。如需使用模型，需使用“中国内地（北京）”地域的[API Key](https://bailian.console.alibabacloud.com/?tab=model#/api-key)。

## **服务开通**

1.  前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 Kimi，找到 Kimi 模型卡片，单击立即开通；
    
2.  在弹窗内确认开通及授权。
    

完成以上步骤即可调用月之暗面提供的 Kimi 模型服务。

## **快速开始**

**前提条件**

-   需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
    
-   如果通过SDK调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk#8833b9274f4v8)
    

kimi-k2.6 、kimi-k2.5 支持输入文本、图像或视频，可通过 `enable_thinking` 参数控制思考模式，默认开启思考模式：

-   **思考模式**（`enable_thinking: true`）：模型会输出详细的推理过程（`reasoning_content`）
    
-   **非思考模式**（`enable_thinking: false` 或不设置）：直接输出结果，不包含推理过程
    

kimi-k2.6 支持通过 `preserve_thinking` 参数在多轮对话中传递思考过程，详情请参见[传递思考过程](https://help.aliyun.com/zh/model-studio/deep-thinking#jln7docdq5et5)。

以下示例演示如何调用思考模式的 kimi-k2.6 模型进行文本生成。

## OpenAI兼容

**说明**

`enable_thinking`非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body`传入，Node.js SDK 作为顶层参数传入。

## Python

```
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="kimi/kimi-k2.6",
    messages=[{"role": "user", "content": "1+1等于多少？"}],
    # 通过 extra_body 设置 enable_thinking 开启思考模式
    extra_body={"enable_thinking": True}
)

msg = completion.choices[0].message

if getattr(msg, "reasoning_content", None):
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    print(msg.reasoning_content or "")
print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
print(msg.content)
```

### **返回结果**

```
====================思考过程====================

用户问了一个简单的数学问题："1+1等于多少？"

这是一个非常基础的算术问题，答案是2。

我应该直接、清晰地回答这个问题。虽然用户用中文提问，但答案是一个通用的数学事实。

回答结构：
1. 直接给出答案：2
2. 可以简要说明这是基本的算术运算

不需要过度复杂化，保持简洁明了。

====================完整回复====================

1+1等于**2**。

这是最基本的算术运算，两个单位相加得到两个单位。
```

## Node.js

```
import OpenAI from "openai";
import process from 'process';

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const messages = [
  { role: "system", content: "You are a helpful assistant." },
  { role: "user", content: "1+1等于多少？" },
];

const response = await client.chat.completions.create({
  model: "kimi/kimi-k2.6",
  messages,
  extra_body: { enable_thinking: true },
});

const msg = response.choices[0].message;
if (msg.reasoning_content) {
  console.log("\n" + "=".repeat(20) + "思考过程" + "=".repeat(20) + "\n");
  console.log(msg.reasoning_content || "");
}
console.log("\n" + "=".repeat(20) + "完整回复" + "=".repeat(20) + "\n");
console.log(msg.content);
```

### **返回结果**

```
====================思考过程====================

用户问了一个简单的数学问题："1+1等于多少？"

这是一个非常基础的算术问题，答案是2。

我应该直接、清晰地回答这个问题。虽然用户用中文提问，但答案是一个通用的数学事实。

回答结构：
1. 直接给出答案：2
2. 可以简要说明这是基本的算术运算

不需要过度复杂化，保持简洁明了。

====================完整回复====================

1+1等于**2**。

这是最基本的算术运算，两个单位相加得到两个单位。
```

## HTTP

## curl

```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "kimi/kimi-k2.6",
    "messages":[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "1+1等于多少？"
        }
    ],
    "enable_thinking": true
}'
```

## **多模态调用示例**

kimi-k2.5 、kimi-k2.6不仅支持纯文本对话，还具备强大的多模态理解能力。本章节将介绍如何让模型理解图像和视频内容。

**重要**

图像/视频文件仅支持通过公网URL传入，不支持 Base64 编码。

### **图像理解**

图像理解功能让 Kimi 模型能够识别和分析图像内容。您可以传入单张或多张图像。图像文件的限制请参见[图像限制](#ac28219766ibq)。

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 单图传入示例（开启思考模式）
completion = client.chat.completions.create(
    model="kimi/kimi-k2.6",
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
    extra_body={"enable_thinking":True}  # 开启思考模式
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
#     model="kimi/kimi-k2.6",
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
#     extra_body={"enable_thinking":True}
# )
#
# # 输出思考过程和回复
# if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
#     print("\n思考过程：\n" + completion.choices[0].message.reasoning_content)
# print("\n完整回复：\n" + completion.choices[0].message.content)
```

## Node.js

```
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
});

// 单图传入示例（开启思考模式）
const completion = await openai.chat.completions.create({
    model: 'kimi/kimi-k2.6',
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
    enable_thinking: true  // 开启思考模式
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
//     model: 'kimi-k2.5',
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
//     enable_thinking: true
// });
//
// // 输出思考过程和回复
// if (multiCompletion.choices[0].message.reasoning_content) {
//     console.log('\n思考过程：\n' + multiCompletion.choices[0].message.reasoning_content);
// }
// console.log('\n完整回复：\n' + multiCompletion.choices[0].message.content);
```

## HTTP

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "kimi/kimi-k2.6",
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
    "enable_thinking": true
}'

# 多图输入示例（取消注释使用）
# curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
# -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
# -H "Content-Type: application/json" \
# -d '{
#     "model": "kimi/kimi-k2.6",
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
#     "enable_thinking": true
# }'
```

### **视频理解**

视频文件的限制请参见[视频限制](#3a523e6bb19wp)。

## OpenAI兼容

## Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="kimi/kimi-k2.6",
    messages=[
        {
            "role": "user",
            "content": [
                # 直接传入视频文件时，请将type的值设置为video_url
                {
                    "type": "video_url",
                    "video_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    }
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

## Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "kimi/kimi-k2.6",
        messages: [
            {
                role: "user",
                content: [
                    // 直接传入视频文件时，请将type的值设置为video_url
                    {
                        type: "video_url",
                        video_url: {
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                        }
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

### **返回结果**

```
====================思考过程====================

用户问了一个简单的数学问题："1+1等于多少？"

这是一个非常基础的算术问题，答案是2。

我应该直接、清晰地回答这个问题。虽然用户用中文提问，但答案是一个通用的数学事实。

回答结构：
1. 直接给出答案：2
2. 可以简要说明这是基本的算术运算

不需要过度复杂化，保持简洁明了。

====================完整回复====================

1+1等于**2**。

这是最基本的算术运算，两个单位相加得到两个单位。
```

## HTTP

## curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "kimi/kimi-k2.6",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
            },
            "fps":2
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

### **文件限制**

## 图像文件

-   **图像分辨率：**建议图像分辨率不超过4k (4096\*2160)
    
-   **支持的图像格式：**PNG、JPEG、WEBP、GIF
    
-   **图像大小与图像数量：**无限制，但需确保请求的文本和图像的大小不超过 100M。
    

## 视频文件

-   **视频大小与视频时长：**无限制，但需确保请求的文本和视频的大小不超过 100M。
    
-   **视频格式：** MP4、MPEG、MOV、AVI、X-FLV、MPG、WEBM、WMV、3GPP。
    
-   **视频尺寸：**无特定限制，建议不超过2K，再高的分辨率只会增加处理时间，也不会对模型理解的效果有提升。
    
-   **音频理解：**不支持对视频文件的音频进行理解。
    

## **其它功能**

**模型**

[多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation)

[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)

[前缀续写](https://help.aliyun.com/zh/model-studio/partial-mode)

[联网搜索](https://help.aliyun.com/zh/model-studio/web-search)

[上下文缓存](https://help.aliyun.com/zh/model-studio/context-cache)

[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)

kimi/kimi-k2.6

支持

支持

支持

不支持

支持

支持

kimi/kimi-k2.5

-   kimi/kimi-k2.6、kimi/kimi-k2.5支持上下文缓存（隐式缓存，自动开启），kimi/kimi-k2.6命中缓存的输入Token按输入价格的16.9%计费，kimi/kimi-k2.5命中缓存的输入Token按输入价格的17.5%计费。
    
-   在思考模式下，使用 kimi/kimi-k2.6、kimi/kimi-k2.5 进行工具调用时：必须在每轮 assistant 消息中保留 `reasoning_content` 字段，`tool_choice` 也仅支持 `"auto"`（默认）和 `"none"`），否则会报错。
    

## **参数默认值**

**模型**

**stream\_options**

**temperature**

**top\_p**

**repetition\_penalty**

**presence\_penalty**

**tool\_choice**

**top\_k**

kimi/kimi-k2.6

仅支持设置为`true`

思考模式：1.0  
非思考模式：0.6

思考模式/非思考模式：0.95

思考模式/非思考模式：0.0

思考模式/非思考模式：0.0

思考模式/非思考模式：auto

\-

kimi/kimi-k2.5

-   `stream_options`仅支持设置为`true`，`temperature`、`top_p`、`repetition_penalty`、`presence_penalty`不支持设置为其他值；
    
-   在思考模式下，不支持强制调用某个工具，`tool_choice`仅支持设置为`auto`（默认值）和`none`。
    
-   “-”表示没有默认值，也不支持设置。
    

## **模型列表与计费**

kimi/kimi-k2.6、kimi/kimi-k2.5属于混合思考模型，通过`enable_thinking`参数控制是否开启思考模式（注意：无法通过`thinking_budget`限制思考长度）。

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## **错误码**

如果执行报错，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
