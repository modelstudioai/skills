# 音视频文件翻译-千问

千问3-LiveTranslate-Flash 是音视频翻译模型，支持 18 种语言（包括中文、英文、俄文、法文等）互译，可结合视觉上下文提升翻译准确性，并输出文本与语音。

## 工作方式

1.  **设置语种**：参考[支持的语种](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash#4ffd192226f0s)，在 `translation_options` 参数中设置源语种 (`source_lang`) 和目标语种 (`target_lang`)。
    
    > 省略 `source_lang`将启用自动检测，但指定语种能提升翻译准确率。
    
2.  **输入待翻译文件**：`messages` 数组中有且仅有一条 `role` 为 `user` 的消息，`content`字段需传入待翻译音频/视频的 URL 或 Base64 数据。
    
3.  **控制输出模态：**通过 `modalities` 参数控制输出模态：
    
    -   `["text"]`：仅输出文本；
        
    -   `["text","audio"]`：输出文本和 Base64 编码的音频。
        
        > 若输出音频，需在`audio`参数中设置音色（`voice`）。参考[支持的音色](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash#0a5bde7593gdk)。
        

以下为使用 OpenAI Python SDK 的核心代码：

```
# 导入依赖与创建客户端...
completion = client.chat.completions.create(
    model="qwen3-livetranslate-flash",    # 选择模型
    # messages 仅包含一条 user 消息，content 为待翻译文件
    messages = [
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
    # translation_options 非 OpenAI 标准参数，需通过 extra_body 传入
    extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}},
    # 示例：输出文本和音频
    modalities = ["text","audio"],
    audio={"voice": "Cherry", "format": "wav"},
    stream=True
)
```
**使用限制**

-   **单轮翻译**：模型专为翻译任务设计，不支持多轮对话。
-   **无 System Message**：不支持通过 `system` 角色设定全局行为。
-   **调用方式：**仅支持兼容 OpenAI 协议的流式输出。

**响应解析**

﻿`chunk`为流式响应对象：

-   **文本**：读取 `chunk.choices[0].delta.content`。
-   **音频**：读取 `chunk.choices[0].delta.audio["data"]`，模型输出音频的采样率是 24kHz。

## 支持的模型

**模型名称**

**版本**

**上下文长度**

**最大输入**

**最大输出**

**（Token数）**

**qwen3-livetranslate-flash**

> 当前能力等同于qwen3-livetranslate-flash-2025-12-01

稳定版

53,248

49,152

4,096

qwen3-livetranslate-flash-2025-12-01

快照版

## 如何使用

qwen3-livetranslate-flash 模型支持音频或视频输入，并输出文本与音频。

请确保已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过OpenAI SDK调用，需[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

以下示例使用音频输入。如需输入视频，请取消对应代码的注释。

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
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

javascript

```
import OpenAI from "openai";

const client = new OpenAI({
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
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

bash

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
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

此示例使用公网文件 URL。若使用本地文件，请参见[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)中的音频与视频部分。

## 解析 Base64 音频数据

模型以流式 Base64 编码格式输出音频。可采用以下两种方式处理数据：

-   **拼接解码：**拼接所有返回的 Base64 片段，待生成结束后统一解码，保存为音频文件。
-   **实时播放：**实时解码每个 Base64 片段并直接播放。

python

```
# Installation instructions for pyaudio:
# APPLE Mac OS X
#   brew install portaudio
#   pip install pyaudio
# Debian/Ubuntu
#   sudo apt-get install python-pyaudio python3-pyaudio
#   or
#   pip install pyaudio
# CentOS
#   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
# Microsoft Windows
#   python -m pip install pyaudio

import os
from openai import OpenAI
import base64
import numpy as np
import soundfile as sf

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
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
completion = client.chat.completions.create(
    model="qwen3-livetranslate-flash",
    messages=messages,
    modalities=["text", "audio"],
    audio={"voice": "Cherry", "format": "wav"},
    stream=True,
    stream_options={"include_usage": True},
    extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}},
)

# 方式1: 待生成结束后再进行解码
audio_string = ""
for chunk in completion:
    if chunk.choices:
        if hasattr(chunk.choices[0].delta, "audio"):
            try:
                audio_string += chunk.choices[0].delta.audio["data"]
            except Exception as e:
                print(chunk.choices[0].delta.audio["transcript"])
    else:
        print(chunk.usage)

wav_bytes = base64.b64decode(audio_string)
audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
sf.write("audio_assistant_py.wav", audio_np, samplerate=24000)

# 方式2: 边生成边解码(使用方式2请将方式1的代码进行注释)
# # 初始化 PyAudio
# import pyaudio
# import time
# p = pyaudio.PyAudio()
# # 创建音频流
# stream = p.open(format=pyaudio.paInt16,
#                 channels=1,
#                 rate=24000,
#                 output=True)

# for chunk in completion:
#     if chunk.choices:
#         if hasattr(chunk.choices[0].delta, "audio"):
#             try:
#                 audio_string = chunk.choices[0].delta.audio["data"]
#                 wav_bytes = base64.b64decode(audio_string)
#                 audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
#                 # 直接播放音频数据
#                 stream.write(audio_np.tobytes())
#             except Exception as e:
#                 print(chunk.choices[0].delta.audio["transcript"])

# time.sleep(0.8)
# # 清理资源
# stream.stop_stream()
# stream.close()
# p.terminate()
```

javascript

```
// 运行前的准备工作:
// Windows/Mac/Linux 通用:
// 1. 确保已安装 Node.js (建议版本 >= 14)
// 2. 运行以下命令安装必要的依赖:
//    npm install openai wav
//
// 如果要使用实时播放功能 (方式2), 还需要:
// Windows:
//    npm install speaker
// Mac:
//    brew install portaudio
//    npm install speaker
// Linux (Ubuntu/Debian):
//    sudo apt-get install libasound2-dev
//    npm install speaker

import OpenAI from "openai";

const client = new OpenAI({
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
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

const completion = await client.chat.completions.create({
    model: "qwen3-livetranslate-flash",
    messages: messages,
    modalities: ["text", "audio"],
    audio: { voice: "Cherry", format: "wav" },
    stream: true,
    stream_options: { include_usage: true },
    translation_options: { source_lang: "zh", target_lang: "en" },
});

// 方式1: 待生成结束后再进行解码
// 需要安装: npm install wav
import { createWriteStream } from 'node:fs';  // node:fs 是 Node.js 内置模块，无需安装
import { Writer } from 'wav';

async function convertAudio(audioString, audioPath) {
    try {
        // 解码Base64字符串为Buffer
        const wavBuffer = Buffer.from(audioString, 'base64');
        // 创建WAV文件写入流
        const writer = new Writer({
            sampleRate: 24000,  // 采样率
            channels: 1,        // 单声道
            bitDepth: 16        // 16位深度
        });
        // 创建输出文件流并建立管道连接
        const outputStream = createWriteStream(audioPath);
        writer.pipe(outputStream);

        // 写入PCM数据并结束写入
        writer.write(wavBuffer);
        writer.end();

        // 使用Promise等待文件写入完成
        await new Promise((resolve, reject) => {
            outputStream.on('finish', resolve);
            outputStream.on('error', reject);
        });

        // 添加额外等待时间确保音频完整
        await new Promise(resolve => setTimeout(resolve, 800));

        console.log(`音频文件已成功保存为 ${audioPath}`);
    } catch (error) {
        console.error('处理过程中发生错误:', error);
    }
}

let audioString = "";
for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        if (chunk.choices[0].delta.audio) {
            if (chunk.choices[0].delta.audio["data"]) {
                audioString += chunk.choices[0].delta.audio["data"];
            }
        }
    } else {
        console.log(chunk.usage);
    }
}
// 执行转换
convertAudio(audioString, "audio_assistant_mjs.wav");

// 方式2: 边生成边实时播放
// 需要先按照上方系统对应的说明安装必要组件
// import Speaker from 'speaker'; // 引入音频播放库

// // 创建扬声器实例（配置与 WAV 文件参数一致）
// const speaker = new Speaker({
//     sampleRate: 24000,  // 采样率
//     channels: 1,        // 声道数
//     bitDepth: 16,       // 位深
//     signed: true        // 有符号 PCM
// });
// for await (const chunk of completion) {
//     if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
//         if (chunk.choices[0].delta.audio) {
//             if (chunk.choices[0].delta.audio["data"]) {
//                 const pcmBuffer = Buffer.from(chunk.choices[0].delta.audio.data, 'base64');
//                 // 直接写入扬声器播放
//                 speaker.write(pcmBuffer);
//             }
//         }
//     } else {
//         console.log(chunk.usage);
//     }
// }
// speaker.on('finish', () => console.log('播放完成'));
// speaker.end(); // 根据实际 API 流结束情况调用
```

## 计费说明

#### 音频

输入或输出每秒音频均消耗 12.5 Token。

#### 视频

视频文件的 Token 分为 `video_tokens`（视觉）与 `audio_tokens`（音频）。

-   `video_tokens`
    
    本脚本用于计算 `video_tokens`。计算流程如下：
    
    1.  **帧数采样**：以 2 FPS 速率采样。将帧数限制在 \[4, 128\] 之间。
    2.  **尺寸调整**：将高与宽调整为 32 的倍数。根据帧数动态缩放，适配总像素限制。
    3.  **Token 计算**：⌈帧数/2⌉ × (高/32) × (宽/32) + 2。

```
# 使用前安装：pip install opencv-python
import math
import os
import cv2

# 固定参数
FRAME_FACTOR = 2

IMAGE_FACTOR = 32

# 视频帧的长宽比
MAX_RATIO = 200

# 视频帧的像素下限
VIDEO_MIN_PIXELS = 128 * 32 * 32

# 视频帧的像素上限
VIDEO_MAX_PIXELS = 768 * 32 * 32

FPS = 2
# 最少抽取帧数
FPS_MIN_FRAMES = 4

# 最大抽取帧数
FPS_MAX_FRAMES = 128

# 视频输入的最大像素值，
VIDEO_TOTAL_PIXELS = 16384 * 32 * 32

def round_by_factor(number, factor):
    return round(number / factor) * factor

def ceil_by_factor(number, factor):
    return math.ceil(number / factor) * factor

def floor_by_factor(number, factor):
    return math.floor(number / factor) * factor

def get_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return frame_height, frame_width, total_frames, video_fps

def smart_nframes(total_frames, video_fps):
    min_frames = ceil_by_factor(FPS_MIN_FRAMES, FRAME_FACTOR)
    max_frames = floor_by_factor(min(FPS_MAX_FRAMES, total_frames), FRAME_FACTOR)
    duration = total_frames / video_fps if video_fps != 0 else 0
    if duration - int(duration) > (1 / FPS):
        total_frames = math.ceil(duration * video_fps)
    else:
        total_frames = math.ceil(int(duration) * video_fps)
    nframes = total_frames / video_fps * FPS
    nframes = int(min(min(max(nframes, min_frames), max_frames), total_frames))
    if not (FRAME_FACTOR <= nframes <= total_frames):
        raise ValueError(f"nframes should in interval [{FRAME_FACTOR}, {total_frames}], but got {nframes}.")
    return nframes

def smart_resize(height, width, nframes, factor=IMAGE_FACTOR):
    min_pixels = VIDEO_MIN_PIXELS
    total_pixels = VIDEO_TOTAL_PIXELS
    max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR), int(min_pixels * 1.05))
    if max(height, width) / min(height, width) > MAX_RATIO:
        raise ValueError(f"absolute aspect ratio must be smaller than {MAX_RATIO}, got {max(height, width) / min(height, width)}")
    h_bar = max(factor, round_by_factor(height, factor))
    w_bar = max(factor, round_by_factor(width, factor))
    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = floor_by_factor(height / beta, factor)
        w_bar = floor_by_factor(width / beta, factor)
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = ceil_by_factor(height * beta, factor)
        w_bar = ceil_by_factor(width * beta, factor)
    return h_bar, w_bar

def video_token_calculate(video_path):
    height, width, total_frames, video_fps = get_video(video_path)
    nframes = smart_nframes(total_frames, video_fps)
    resized_height, resized_width = smart_resize(height, width, nframes)
    video_token = int(math.ceil(nframes / FPS) * resized_height / 32 * resized_width / 32)
    video_token += 2  # 视觉标记
    return video_token

if __name__ == "__main__":
    video_path = "spring_mountain.mp4"  # 你的视频路径
    video_token = video_token_calculate(video_path)
    print("video_tokens:", video_token)
```

-   `audio_tokens`
    
    每秒音频消耗 12.5 Token。若音频时长不足1秒，按 1 秒计算。
    

Token 费用请参见[选择模型](raw/model-user-guide/get-started-with-models/models.md)。

## API 参考

qwen3-livetranslate-flash 模型的输入输出参数请参见[音视频翻译-通义千问](raw/_short/qwen3-livetranslate-flash-api-75fa76c959634163.md)。

## 支持的语种

下表中的语种代码可用于指定源语种与目标语种。

> 部分目标语种仅支持输出文本，不支持输出音频。

**语种代码**

**语种**

**支持的输出模态**

en

英语

音频、文本

zh

中文

音频、文本

ru

俄语

音频、文本

fr

法语

音频、文本

de

德语

音频、文本

pt

葡萄牙语

音频、文本

es

西班牙语

音频、文本

it

意大利语

音频、文本

id

印尼语

文本

ko

韩语

音频、文本

ja

日语

音频、文本

vi

越南语

文本

th

泰语

文本

ar

阿拉伯语

文本

yue

粤语

音频、文本

hi

印地语

文本

el

希腊语

文本

tr

土耳其语

文本

## 支持的音色

**音色名**

`voice`**参数**

**音色效果**

**描述**

**支持的语种**

芊悦

Cherry

阳光积极、亲切自然小姐姐。

中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语

不吃鱼

Nofish

不会翘舌音的设计师。

中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语

上海-阿珍

Jada

风风火火的沪上阿姐。

中文

北京-晓东

Dylan

北京胡同里长大的少年。

中文

四川-晴儿

Sunny

甜到你心里的川妹子。

中文

天津-李彼得

Peter

天津相声，专业捧人。

中文

粤语-阿清

Kiki

甜美的港妹闺蜜。

粤语

四川-程川

Eric

一个跳脱市井的四川成都男子。

中文

## 常见问题

### Q：传入视频文件时，翻译的是什么内容？

A：翻译视频中的音频内容，视觉信息用于辅助上下文理解，以提升准确率。

**示例**：

当音频内容为`This is a mask`时：

-   若画面显示口罩，会翻译为“这是一个口罩”；
-   若画面显示面具，会翻译为“这是一个面具”。
