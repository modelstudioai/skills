# Kimi-月之暗面

本文档介绍如何在阿里云百炼平台调用月之暗面（Moonshot AI）直供的模型推理服务。

> **重要**
>
> 本文档描述的功能仅在华北2（北京）地域可用，如需使用模型，需从华北2（北京）地域[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)。

<a id="服务开通"></a>

<a id="305311640441x"></a>

## 服务开通

1.  前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 Kimi，找到 Kimi 模型卡片，单击立即开通；
2.  在弹窗内确认开通及授权。

完成以上步骤即可调用月之暗面提供的 Kimi 模型服务。

<a id="快速开始"></a>

<a id="61623d75547kl"></a>

## 快速开始

**前提条件**

-   需要已[获取与配置 API Key](../../../model-api-reference/preparations/get-api-key.md)并完成[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
-   如果通过SDK调用，需要[安装SDK](../../../model-api-reference/preparations/install-sdk.md)

kimi 系列模型均支持输入文本、图像或视频：

1.  kimi/kimi-k2.7-code-highspeed 与 kimi/kimi-k2.7-code 功能完全一致，速度提升5~6倍。
    
2.  kimi/kimi-k3、kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code 为仅思考模型。
    
3.  kimi/kimi-k2.6 可通过 `enable_thinking` 参数控制思考模式，默认开启思考模式：
    
    -   **思考模式**（`reasoning_effort: "max"`）：模型会输出详细的推理过程（`reasoning_content`）
    -   **非思考模式**（`enable_thinking: false` 或不设置）：直接输出结果，不包含推理过程

以上模型均支持通过 `preserve_thinking` 参数在多轮对话中传递思考过程，详情请参见[传递思考过程](../../model-experience/text-generation-model/deep-thinking.md#jln7docdq5et5)。

以下示例演示如何调用思考模式的 kimi/kimi-k3 模型进行文本生成。

<a id="sec-tabs"></a>

<a id="openai兼容"></a>

<a id="openai兼容-h4"></a>

#### OpenAI兼容

<a id="sec-tabs-2"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

<a id="code-block"></a>

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="kimi/kimi-k3",
    messages=[{"role": "user", "content": "1+1等于多少？"}],
    # 通过 reasoning_effort 设置思考强度
    reasoning_effort="max"
)

msg = completion.choices[0].message

if getattr(msg, "reasoning_content", None):
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    print(msg.reasoning_content or "")
print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
print(msg.content)
```

<a id="f2828e7338ck1"></a>

### 返回结果

<a id="code-block-2"></a>

```text
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

<a id="node-js"></a>

<a id="node-js-h4"></a>

#### Node.js

<a id="code-block-3"></a>

```javascript
import OpenAI from "openai";
import process from 'process';

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

const messages = [
  { role: "system", content: "You are a helpful assistant." },
  { role: "user", content: "1+1等于多少？" },
];

const response = await client.chat.completions.create({
  model: "kimi/kimi-k3",
  messages,
  reasoning_effort: "max",
});

const msg = response.choices[0].message;
if (msg.reasoning_content) {
  console.log("\n" + "=".repeat(20) + "思考过程" + "=".repeat(20) + "\n");
  console.log(msg.reasoning_content || "");
}
console.log("\n" + "=".repeat(20) + "完整回复" + "=".repeat(20) + "\n");
console.log(msg.content);
```

<a id="1f1fdf8de1624"></a>

### 返回结果

<a id="code-block-4"></a>

```text
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

<a id="http"></a>

<a id="http-h4"></a>

#### HTTP

<a id="sec-tabs-3"></a>

<a id="curl"></a>

<a id="curl-h4"></a>

#### curl

<a id="code-block-5"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "kimi/kimi-k3",
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
    "reasoning_effort": "max"
}'
```

<a id="多模态调用示例"></a>

<a id="01016f0bac41v"></a>

## 多模态调用示例

Kimi 系列模型不仅支持纯文本对话，还具备强大的多模态理解能力。本章节将介绍如何让模型理解图像和视频内容。

> **重要**
>
> 图像/视频文件仅支持通过公网URL传入，不支持 Base64 编码。

<a id="图像理解"></a>

<a id="0f01025abdjum"></a>

### 图像理解

图像理解功能让 Kimi 模型能够识别和分析图像内容。您可以传入单张或多张图像。图像文件的限制请参见[图像限制](kimi-api-by-moonshot-ai.md)。

<a id="sec-tabs-4"></a>

<a id="openai兼容-2"></a>

<a id="openai兼容-2-h4"></a>

#### OpenAI兼容

<a id="sec-tabs-5"></a>

<a id="python-2"></a>

<a id="python-2-h4"></a>

#### Python

<a id="code-block-6"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 单图传入示例（开启思考模式）
completion = client.chat.completions.create(
    model="kimi/kimi-k3",
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
    reasoning_effort="max"  # 开启思考模式
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
#     model="kimi/kimi-k3",
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
#     reasoning_effort="max"
# )
#
# # 输出思考过程和回复
# if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
#     print("\n思考过程：\n" + completion.choices[0].message.reasoning_content)
# print("\n完整回复：\n" + completion.choices[0].message.content)
```

<a id="node-js-2"></a>

<a id="node-js-2-h4"></a>

#### Node.js

<a id="code-block-7"></a>

```javascript
import OpenAI from "openai";
import process from 'process';

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

// 单图传入示例（开启思考模式）
const completion = await openai.chat.completions.create({
    model: 'kimi/kimi-k3',
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
    reasoning_effort: "max"  // 开启思考模式
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
//     model: 'kimi/kimi-k3',
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
//     reasoning_effort: "max"
// });
//
// // 输出思考过程和回复
// if (multiCompletion.choices[0].message.reasoning_content) {
//     console.log('\n思考过程：\n' + multiCompletion.choices[0].message.reasoning_content);
// }
// console.log('\n完整回复：\n' + multiCompletion.choices[0].message.content);
```

<a id="http-2"></a>

<a id="http-2-h4"></a>

#### HTTP

<a id="sec-tabs-6"></a>

<a id="curl-2"></a>

<a id="curl-2-h4"></a>

#### curl

<a id="code-block-8"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "kimi/kimi-k3",
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
    "reasoning_effort": "max"
}'

# 多图输入示例（取消注释使用）
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
# -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
# -H "Content-Type: application/json" \
# -d '{
#     "model": "kimi/kimi-k3",
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
#     "reasoning_effort": "max"
# }'
```

<a id="视频理解"></a>

<a id="6b81857353589"></a>

### 视频理解

视频文件的限制请参见[视频限制](kimi-api-by-moonshot-ai.md)。

<a id="sec-tabs-7"></a>

<a id="openai兼容-3"></a>

<a id="openai兼容-3-h4"></a>

#### OpenAI兼容

<a id="sec-tabs-8"></a>

<a id="python-3"></a>

<a id="python-3-h4"></a>

#### Python

<a id="code-block-9"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="kimi/kimi-k3",
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

<a id="node-js-3"></a>

<a id="node-js-3-h4"></a>

#### Node.js

<a id="code-block-10"></a>

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.chat.completions.create({
        model: "kimi/kimi-k3",
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

<a id="05b2102035onc"></a>

### 返回结果

<a id="code-block-11"></a>

```text
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

<a id="http-3"></a>

<a id="http-3-h4"></a>

#### HTTP

<a id="sec-tabs-9"></a>

<a id="curl-3"></a>

<a id="curl-3-h4"></a>

#### curl

<a id="code-block-12"></a>

```bash
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "kimi/kimi-k3",
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

<a id="文件限制"></a>

<a id="844ab9bc5dkkk"></a>

### 文件限制

<a id="sec-tabs-10"></a>

<a id="图像文件"></a>

<a id="图像文件-h4"></a>

#### 图像文件

-   **图像分辨率：**建议图像分辨率不超过4k (4096\*2160)
-   **支持的图像格式：**PNG、JPEG、WEBP、GIF
-   **图像大小与图像数量：**无限制，但需确保请求的文本和图像的大小不超过 100M。

<a id="视频文件"></a>

<a id="视频文件-h4"></a>

#### 视频文件

-   **视频大小与视频时长：**无限制，但需确保请求的文本和视频的大小不超过 100M。
-   **视频格式：** MP4、MPEG、MOV、AVI、X-FLV、MPG、WEBM、WMV、3GPP。
-   **视频尺寸：**无特定限制，建议不超过2K，再高的分辨率只会增加处理时间，也不会对模型理解的效果有提升。
-   **音频理解：**不支持对视频文件的音频进行理解。

<a id="其它功能"></a>

<a id="d062ed0e4d5fe"></a>

## 其它功能

<table><thead><tr><th>模型</th><th><a href="../../model-experience/text-generation-model/multi-round-conversation.md">多轮对话</a></th><th><a href="../../model-experience/text-generation-model/tool-calls/qwen-function-calling.md">Function Calling</a></th><th><a href="../../model-experience/text-generation-model/partial-mode.md">前缀续写</a></th><th><a href="../../model-experience/text-generation-model/tool-calls/web-search.md">联网搜索</a></th><th><a href="../../model-experience/text-generation-model/context-cache.md">上下文缓存</a></th><th><a href="../../model-experience/text-generation-model/qwen-structured-output.md">结构化输出</a></th></tr></thead><tbody><tr><td><p>kimi/kimi-k3</p></td><td rowspan="6"><p>支持</p></td><td rowspan="6"><p>支持</p></td><td rowspan="6"><p>支持</p></td><td rowspan="6"><p>不支持</p></td><td rowspan="6"><p>支持</p></td><td rowspan="6"><p>支持</p></td></tr><tr><td><p>kimi/kimi-k3.1-pro</p></td></tr><tr><td><p>kimi/kimi-k3.1-pro-highspeed</p></td></tr><tr><td><p>kimi/kimi-k2.7-code-highspeed</p></td></tr><tr><td><p>kimi/kimi-k2.7-code</p></td></tr><tr><td><p>kimi/kimi-k2.6</p></td></tr></tbody></table>

以上模型支持上下文缓存（隐式缓存，自动开启）：

-   kimi/kimi-k3、kimi/kimi-k3.1-pro命中缓存的输入Token按输入价格的10%计费
-   kimi/kimi-k3.1-pro-highspeed命中缓存的输入Token按输入价格的5%计费
-   kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code 命中缓存的输入Token按输入价格的20.0%计费，
-   kimi/kimi-k2.6命中缓存的输入Token按输入价格的16.9%计费

<a id="参数默认值"></a>

<a id="5c21b5ebd7so8"></a>

## 参数默认值

| 参数 | kimi/kimi-k3、kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed | kimi/kimi-k2.7-code-highspeed | kimi/kimi-k2.7-code | kimi/kimi-k2.6 |
| --- | --- | --- | --- | --- |
| `tool_choice` | auto | auto | auto | 思考模式/非思考模式：auto |
| `preserve_thinking` | 默认关闭 | 默认开启 | 默认开启 | 默认关闭 |
| `reasoning_effort` | max | \- | \- | \- |
| `temperature` | 1 | 1.0 | 1.0 | 思考模式：1.0<br><br>非思考模式：0.6 |
| `top_p` | 0.95 | 0.95 | 0.95 | 思考模式/非思考模式：0.95 |
| `repetition_penalty` | 0.0 | 0.0 | 0.0 | 思考模式/非思考模式：0.0 |
| `presence_penalty` | \- | 0.0 | 0.0 | 思考模式/非思考模式：0.0 |
| `stream_options` | 仅支持设置为`true` | 仅支持设置为`true` | 仅支持设置为`true` | 仅支持设置为`true` |

-   `stream_options`仅支持设置为`true`，`temperature`、`top_p`、`repetition_penalty`、`presence_penalty`不支持设置为其他值；
-   kimi/kimi-k3、kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed 支持 `reasoning_effort` 参数，唯一支持值 `max`。
-   kimi/kimi-k3.1-pro、kimi/kimi-k3.1-pro-highspeed 不支持 `parallel_tool_calls` 和 `n` 参数。
-   在思考模式下，使用 Kimi 模型进行工具调用时：必须在每轮 assistant 消息中保留 `reasoning_content` 字段；对于`tool_choice`参数，`kimi-k3`、`kimi-k3.1-pro`、`kimi-k3.1-pro-highspeed` 支持 `auto` / `none` / `required` 三档；其他模型不支持 `required`，传入会报错。以上三个模型支持动态加载工具，详细用法请参见[动态加载工具](https://platform.kimi.com/docs/guide/use-dynamic-tool-loading)。
-   ”-”表示没有默认值，也不支持设置。

<a id="模型列表与计费"></a>

<a id="a1208aad3d0k8"></a>

## 模型列表与计费

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

<a id="错误码"></a>

<a id="2048aa1f92x46"></a>

## 错误码

如果执行报错，请参见[错误码](../../../model-api-reference/preparations/error-code.md)进行解决。
