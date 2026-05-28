# 音视频翻译-通义千问 API 参考

本文介绍通过 OpenAI 兼容接口调用 qwen3-livetranslate-flash 模型的输入与输出参数。

> 相关文档：[音视频翻译-通义千问](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash)

> 不支持通过 DashScope 接口调用。

## OpenAI 兼容

## 北京地域

SDK 调用配置的`base_url`为：`https://dashscope.aliyuncs.com/compatible-mode/v1`

HTTP 调用配置的`endpoint`：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

## 新加坡地域

SDK 调用配置的`base_url`为：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

HTTP 调用配置的`endpoint`：`POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`

> 您需要已[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过OpenAI SDK进行调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

### 请求体

Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ----------------音频输入 ----------------
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "input_audio",
                "input_audio": {
                    "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                    "format": "wav",
                },
            }
        ],
    }
]

# ----------------视频输入(需取消注释)----------------
# messages = [
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "video_url",
#                 "video_url": {
#                     "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
#                 },
#             }
#         ],
#     },
# ]

completion = client.chat.completions.create(
    model="qwen3-livetranslate-flash",
    messages=messages,
    modalities=["text", "audio"],
    audio={"voice": "Cherry", "format": "wav"},
    stream=True,
    stream_options={"include_usage": True},
    extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}},
)

for chunk in completion:
    print(chunk)
```

Node.js

```
import OpenAI from "openai";

const client = new OpenAI({
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

// ---------------- 音频输入 ----------------
const messages = [
    {
        role: "user",
        content: [
            {
                type: "input_audio",
                input_audio: {
                    data: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                    format: "wav",
                },
            },
        ],
    },
];

// ---------------- 视频输入(需取消注释) ----------------
// const messages = [
//     {
//         role: "user",
//         content: [
//             {
//                 type: "video_url",
//                 video_url: {
//                     url: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4",
//                 },
//             },
//         ],
//     },
// ];

async function main() {
    const completion = await client.chat.completions.create({
        model: "qwen3-livetranslate-flash",
        messages: messages,
        modalities: ["text", "audio"],
        audio: { voice: "Cherry", format: "wav" },
        stream: true,
        stream_options: { include_usage: true },
        translation_options: { source_lang: "zh", target_lang: "en" },
    });

    for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
    }
}

main();
```

curl

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域示例，如果使用新加坡地域的模型，需要将请求地址替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-livetranslate-flash",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                        "format": "wav"
                    }
                }
            ]
        }
    ],
    "modalities": ["text", "audio"],
    "audio": {
        "voice": "Cherry",
        "format": "wav"
    },
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "translation_options": {
        "source_lang": "zh",
        "target_lang": "en"
    }
}'
```

**model** `_string_` **（必选）**

模型名称。支持的模型：qwen3-livetranslate-flash、qwen3-livetranslate-flash-2025-12-01。

**messages** `_array_` **（必选）**

消息数组，用于向大模型传递上下文。仅支持传入一个 User Message。

**消息类型**

User Message `_object_` **（必选）**

用户消息。

**属性**

**content** `_array_` **（必选）**

消息内容。

**属性**

**type** `_string_` **（必选）**

可选值：

-   `input_audio`
    
    输入音频时需设为`input_audio`。
    
-   `video_url`
    
    输入视频文件时需设为`video_url`。
    

**input\_audio** `_object_`

输入的音频信息。当`type`为`input_audio`时是必选参数。

**属性**

**data** `_string_`**（必选）**

音频的 URL 或Base64 Data URL。传入本地文件请参见：[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。

**format** `_string_`**（必选）**

输入音频的格式，如`mp3`、`wav`等。

**video\_url** `_object_`

输入的视频文件信息。当`type`为`video_url`时是必选参数。

**属性**

**url** `_string_`**（必选）**

视频文件的公网 URL 或 Base64 Data URL。输入本地视频文件请参见[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。

**role** `_string_` **（必选）**

用户消息的角色，固定为`user`。

**stream** `_boolean_` **（必选）** 默认值为 `false`

是否以流式方式输出回复。模型仅支持流式输出方式调用，仅可设为`true`。

**stream\_options** `_object_` （可选）

流式输出的配置项，仅在 `stream` 为 `true` 时生效。

**属性**

**include\_usage** `_boolean_` （可选）默认值为 `false`

是否在**最后一个数据块**包含Token消耗信息。

可选值：

-   `true`：包含；
    
-   `false`：不包含。
    

**modalities** `array` （可选）默认值为`["text"]`

输出数据的模态。可选值：

-   `["text","audio"]`：输出文本与音频；
    
-   `["text"]`：仅输出文本。
    

**audio** `_object_` （可选）

输出音频的音色与格式。`modalities`参数需为`["text","audio"]`。

**属性**

**voice** `_string_` **（必选）**

输出音频的音色。请参见[支持的音色](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash#0a5bde7593gdk)。

**format** `_string_` **（必选）**

输出音频的格式，仅支持设定为`wav`。

**max\_tokens** `_integer_` （可选）

用于限制模型输出的最大 Token 数。若生成内容超过此值，响应将被截断。

默认值与最大值均为模型的最大输出长度，请参见[模型选型](https://help.aliyun.com/zh/model-studio/machine-translation#efd59c2b9eosx)。

**seed** `_integer_` （可选）

随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 `seed` 且其他参数不变，模型将尽可能返回相同结果。

取值范围：`[0,231−1]`。

**temperature** `_float_` （可选） 默认值为0.000001

采样温度，控制模型生成内容的多样性。temperature越高，生成的内容更多样，反之更确定。

取值范围： \[0, 2)

为了翻译的准确性，不建议修改该值。

**top\_p** `_float_` （可选）默认值为0.8

核采样的概率阈值，控制模型生成内容的多样性。

top\_p越高，生成的内容更多样。反之更确定。

取值范围：（0,1.0\]

为了翻译的准确性，不建议修改该值。

**presence\_penalty** `_float_` （可选）默认值为0

控制模型生成文本时的内容重复度。

取值范围：\[-2.0, 2.0\]。正值降低重复度，负值增加重复度。为了翻译的准确性，不建议修改该值。

**top\_k** `_integer_` （可选）默认值为1

生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top\_k大于100时，表示不启用top\_k策略，此时仅有top\_p策略生效。

取值需要大于或等于0。为了翻译的准确性，不建议修改该值。

该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra\_body** 对象中，配置方式为：`extra_body={"top_k": xxx}`；通过 Node.js SDK 或 HTTP 方式调用时，请作为顶层参数传递。

**repetition\_penalty** `_float_` （可选）默认值为1.05

模型生成时连续序列中的重复度。提高repetition\_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。取值大于0即可。为了翻译的准确性，不建议修改该值。

该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra\_body** 对象中，配置方式为：`extra_body={"repetition_penalty": xxx}`；通过 Node.js SDK 或 HTTP 方式调用时，请作为顶层参数传递。

**translation\_options** `_object_` **（必选）**

需配置的翻译参数。

**属性**

**source\_lang** `_string_` （可选）

源语言的英文全称，请参见[支持的语种](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash#4ffd192226f0s)。若不设置，模型会自动识别输入的语种。

**target\_lang** `_string_` **（必选）**

目标语言的英文全称，请参见[支持的语种](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash#4ffd192226f0s)。

该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 **extra\_body** 对象中，配置方式为：`extra_body={"translation_options": xxx}`；通过 Node.js SDK 或 HTTP 方式调用时，请作为顶层参数传递。

### chat响应chunk对象（流式输出）

## 文本输出chunk

```
{
  "id": "chatcmpl-c22a54b8-40cc-4a1d-988b-f84cdf86868f",
  "choices": [
    {
      "delta": {
        "content": " of",
        "function_call": null,
        "refusal": null,
        "role": null,
        "tool_calls": null
      },
      "finish_reason": null,
      "index": 0,
      "logprobs": null
    }
  ],
  "created": 1764755440,
  "model": "qwen3-livetranslate-flash",
  "object": "chat.completion.chunk",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": null
}
```

## 音频输出chunk

```
{
  "id": "chatcmpl-c22a54b8-40cc-4a1d-988b-f84cdf86868f",
  "choices": [
    {
      "delta": {
        "content": null,
        "function_call": null,
        "refusal": null,
        "role": null,
        "tool_calls": null,
        "audio": {
          "data": "///+//7////+////////////AAAAAAAAAAABA......",
          "expires_at": 1764755440,
          "id": "audio_c22a54b8-40cc-4a1d-988b-f84cdf86868f"
        }
      },
      "finish_reason": null,
      "index": 0,
      "logprobs": null
    }
  ],
  "created": 1764755440,
  "model": "qwen3-livetranslate-flash",
  "object": "chat.completion.chunk",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": null
}
```

## Token 消耗chunk

```
{
  "id": "chatcmpl-c22a54b8-40cc-4a1d-988b-f84cdf86868f",
  "choices": [],
  "created": 1764755440,
  "model": "qwen3-livetranslate-flash",
  "object": "chat.completion.chunk",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 242,
    "prompt_tokens": 415,
    "total_tokens": 657,
    "completion_tokens_details": {
      "accepted_prediction_tokens": null,
      "audio_tokens": 191,
      "reasoning_tokens": null,
      "rejected_prediction_tokens": null,
      "text_tokens": 51
    },
    "prompt_tokens_details": {
      "audio_tokens": 415,
      "cached_tokens": null,
      "text_tokens": 0
    }
  }
}
```

**id** `_string_`

本次调用的唯一标识符。每个chunk对象有相同的 id。

**choices** `_array_`

模型生成内容的数组。若设置`include_usage`参数为`true`，则`choices`在最后一个chunk中为空数组。

**属性**

**delta** `_object_`

请求的增量对象。

**属性**

**content** `_string_`

增量消息内容。

**reasoning\_content** `_string_`

该值固定为`null`。

**function\_call** `_object_`

该值固定为`null`。

**audio** `_object_`

输出的音频信息。

**属性**

**data** `_string_`

增量的 Base64 音频编码数据。

**expires\_at** `_integer_`

创建请求时的时间戳。

**id** `_string_`

输出音频的唯一标识符。

**refusal** `_object_`

该参数当前固定为`null`。

**role** `_string_`

增量消息对象的角色，只在第一个chunk中有值。

**tool\_calls** `_array_`

该值固定为`null`。

**finish\_reason** `_string_`

模型停止生成的原因。有以下情况：

-   自然停止输出时为`stop`；
    
-   生成未结束时为`null`；
    
-   生成长度过长而结束为`length`。
    

**index** `_integer_`

当前响应在`choices`数组中的索引，固定为0。

**logprobs** `_object_`

该值固定为`null`。

**created** `_integer_`

本次请求被创建时的时间戳。每个chunk有相同的时间戳。

**model** `_string_`

本次请求使用的模型。

**object** `_string_`

始终为`chat.completion.chunk`。

**service\_tier** `_string_`

该值固定为`null`。

**system\_fingerprint**`_string_`

该值固定为`null`。

**usage** `_object_`

本次请求消耗的Token。只在`include_usage`为`true`时，在最后一个chunk显示。

**属性**

**completion\_tokens** `_integer_`

模型输出的 Token 数。

**prompt\_tokens** `_integer_`

输入 Token 数。

**total\_tokens** `_integer_`

总 Token 数，为`prompt_tokens`与`completion_tokens`的总和。

**completion\_tokens\_details** `_object_`

输出 Token 的详细信息。

**属性**

**audio\_tokens** `_integer_`

输出的音频 Token 数。

**reasoning\_tokens** `_integer_`

该值固定为`null`。

**text\_tokens** `_integer_`

输出文本 Token 数。

**prompt\_tokens\_details** `_object_`

输入 Token的细粒度分类。

**属性**

**audio\_tokens** `_integer_`

输入音频的 Token 数。

> 视频文件中的音频 Token 数通过本参数返回。

**text\_tokens** `_integer_`

输入文本的 Token 数。该值固定为0。

**video\_tokens** `_integer_`

输入视频的 Token 数。
