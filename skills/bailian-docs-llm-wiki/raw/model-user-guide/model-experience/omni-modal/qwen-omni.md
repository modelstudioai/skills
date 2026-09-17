# Qwen-Omni

通过 HTTP API 使用 Qwen-Omni 理解文本、图片、音频和视频。文本分析使用 Qwen3.8-Omni-Flash，语音输出使用 Qwen3.5-Omni。

## 快速开始

根据输出需求选择示例：文本分析使用 Qwen3.8-Omni-Flash，生成语音使用 Qwen3.5-Omni。

#### 文本输出（Qwen3.8-Omni-Flash）

先[配置 API Key](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)并[安装 OpenAI SDK](raw/model-api-reference/preparations/install-sdk.md)。将 `DASHSCOPE_BASE_URL` 环境变量设为业务空间对应的 [Chat Completions 服务地址](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)中的 `base_url`，并将 `AUDIO_URL` 设为可访问的 WAV 音频 URL。需使用对应地域的 [API Key](raw/model-api-reference/preparations/get-api-key.md)。

在 macOS 或 Linux 终端中安装依赖并设置以下环境变量。将服务地址和音频 URL 替换为实际值；`DASHSCOPE_API_KEY` 按上方链接配置。

```
python3 -m pip install openai
export DASHSCOPE_BASE_URL="<workspace-base-url>"
export AUDIO_URL="<accessible-wav-url>"
```
```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["DASHSCOPE_BASE_URL"],
)
completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "总结这段录音的主要内容。"},
            {"type": "input_audio", "input_audio": {
                "data": os.environ["AUDIO_URL"],
                "format": "wav",
            }},
        ],
    }],
    stream=True,
    stream_options={"include_usage": True},
)
output_section = None
for chunk in completion:
    if not chunk.choices:
        if chunk.usage:
            print("\nUsage:", chunk.usage)
        continue
    delta = chunk.choices[0].delta
    if getattr(delta, "reasoning_content", None):
        if output_section != "thinking":
            print("\n思考过程:")
            output_section = "thinking"
        print(delta.reasoning_content, end="", flush=True)
    if delta.content:
        if output_section != "answer":
            print("\n模型回复:")
            output_section = "answer"
        print(delta.content, end="", flush=True)
```

#### 语音输出（Qwen3.5-Omni）

**前提条件**

-   已[配置API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   以下语音输出示例使用 OpenAI 兼容方式调用，需要[安装最新版SDK](raw/model-api-reference/preparations/install-sdk.md)。OpenAI Python SDK最低版本为 1.52.0，Node.js SDK最低版本为 4.68.0。

**说明**运行前安装依赖：`pip install numpy soundfile openai`（Python）或 `npm install openai wav`（Node.js）。

以下示例向 Qwen-Omni 发送一条文本消息，流式接收文本和音频回复，流结束后将音频解码并保存为 WAV 文件。

python

```
# 运行前的准备工作:
# 运行下列命令安装第三方依赖
# pip install numpy soundfile openai

import os
import base64
import soundfile as sf
import numpy as np
from openai import OpenAI

# 1. 初始化客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 确认已配置环境变量
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 2. 发起请求
try:
    completion = client.chat.completions.create(
        model="qwen3.5-omni-plus",
        messages=[{"role": "user", "content": "你是谁"}],
        modalities=["text", "audio"],  # 指定输出文本和音频
        audio={"voice": "Tina", "format": "wav"},
        stream=True,  # 必须设置为 True
        stream_options={"include_usage": True},
    )

    # 3. 处理流式响应并解码音频
    print("模型回复：")
    audio_base64_string = ""
    for chunk in completion:
        # 处理文本部分
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")

        # 收集音频部分
        if chunk.choices and hasattr(chunk.choices[0].delta, "audio") and chunk.choices[0].delta.audio:
            audio_base64_string += chunk.choices[0].delta.audio.get("data", "")

    # 4. 保存音频文件
    if audio_base64_string:
        wav_bytes = base64.b64decode(audio_base64_string)
        audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
        sf.write("audio_assistant.wav", audio_np, samplerate=24000)
        print("\n音频文件已保存至：audio_assistant.wav")

except Exception as e:
    print(f"请求失败: {e}")
```

javascript

```
// 运行前的准备工作:
// Windows/Mac/Linux 通用:
// 1. 确保已安装 Node.js (建议版本 >= 14)
// 2. 运行以下命令安装必要的依赖:
//    npm install openai wav

import OpenAI from "openai";
import { createWriteStream } from 'node:fs';
import { Writer } from 'wav';

// 定义音频转换函数：将Base64字符串转换并保存为标准的 WAV 音频文件
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

        console.log(`\n音频文件已成功保存为 ${audioPath}`);
    } catch (error) {
        console.error('处理过程中发生错误:', error);
    }
}

//  1. 初始化客户端
const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);
// 2. 发起请求
const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [
        {
            "role": "user",
            "content": "你是谁？"
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text", "audio"],
    audio: { voice: "Tina", format: "wav" }
});

let audioString = "";
console.log("大模型的回复：")

// 3. 处理流式响应并解码音频
for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        // 处理文本内容
        if (chunk.choices[0].delta.content) {
            process.stdout.write(chunk.choices[0].delta.content);
        }
        // 处理音频内容
        if (chunk.choices[0].delta.audio) {
            if (chunk.choices[0].delta.audio["data"]) {
                audioString += chunk.choices[0].delta.audio["data"];
            }
        }
    }
}
// 4. 保存音频文件
convertAudio(audioString, "audio_assistant.wav");
```

bash

```
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.5-omni-plus",
    "messages": [
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    "stream":true,
    "stream_options":{
        "include_usage":true
    },
    "modalities":["text","audio"],
    "audio":{"voice":"Tina","format":"wav"}
}'
```

返回结果

运行`Python`或`Node.js`代码后，控制台输出模型的文本回复，同目录下生成`audio_assistant.wav`音频文件。

```
大模型的回复：
我是阿里云研发的大规模语言模型，我叫千问。有什么我可以帮助你的吗？
```

运行`HTTP`代码直接返回文本和`Base64`编码的音频数据（`audio`字段）。

```
data: {"choices":[{"delta":{"content":"我"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1757647879,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-a68eca3b-c67e-4666-a72f-73c0b4919860"}
data: {"choices":[{"delta":{"content":"是"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1757647879,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-a68eca3b-c67e-4666-a72f-73c0b4919860"}
......
data: {"choices":[{"delta":{"audio":{"data":"/v8AAAAAAAAAAAAAAA...","expires_at":1757647879,"id":"audio_a68eca3b-c67e-4666-a72f-73c0b4919860"}},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1757647879,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-a68eca3b-c67e-4666-a72f-73c0b4919860"}
data: {"choices":[{"finish_reason":"stop","delta":{"content":""},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1764763585,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-e8c82e9e-073e-4289-a786-a20eb444ac9c"}
data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":207,"completion_tokens":103,"total_tokens":310,"completion_tokens_details":{"audio_tokens":83,"text_tokens":20},"prompt_tokens_details":{"text_tokens":207}},"created":1757940330,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-9cdd5a26-f9e9-4eff-9dcc-93a878165afc"}
```

## 模型选型

音视频理解、会议纪要、字幕生成和文本问答优先使用 **Qwen3.8-Omni-Flash**，支持深度思考、工具调用和联网搜索，详见[调用示例](#qwen38-offline)。需要直接生成语音回复时，可选择下方 Qwen3.5-Omni。

### Qwen3.8-Omni-Flash

支持地域：华北2（北京）、新加坡、中国香港、日本（东京）、德国（法兰克福）、美国（弗吉尼亚）。需使用对应地域的 [API Key](raw/model-api-reference/preparations/get-api-key.md)。

`qwen3.8-omni-flash` 适用于音视频理解、会议纪要和内容分析。

模型

输入

输出

调用方式

`qwen3.8-omni-flash`

文本、图片、音频、视频

文本

Chat Completions、Responses

-   上下文长度为 1M Token。
-   音频输入支持 113 种语言和方言，与 Qwen3.5-Omni 一致。完整列表见[模型选型](#d54e85c641oux)中 Qwen3.5-Omni 的“输入音频语种”。
-   支持 Function Calling 和联网搜索。Responses 内置工具当前仅支持 `web_search`。

### Qwen3.5-Omni：音频输出与多模态交互

支持地域：北京、新加坡，需使用对应地域的 [API Key](raw/model-api-reference/preparations/get-api-key.md)。

-   **Qwen3.5-Omni 系列：**支持音视频理解、语音回复及音频控制。
    
    -   输入限制：3 小时音频或 1 小时视频
    -   音频控制：支持通过指令调节音量、语速、情绪
    -   视觉能力：与 Qwen3.5 同等水平，可理解画面、语音、音效等多模态信息
    -   多模态组合输入：支持文本与图片、音频、视频的任意组合同时输入，不限于单一模态
    -   声音复刻：支持自定义音色（仅qwen3.5-omni-plus、qwen3.5-omni-flash支持，快照版本暂不支持），详情请参见[声音复刻](raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)

### 其他模型与规格

-   **Qwen3-Omni-Flash 系列：**
    -   输入限制：150 秒以内音视频
    -   思考模式：支持通过 `enable_thinking` 开启或关闭思考
    -   输入模态：仅支持文本与单一其他模态（图片、音频或视频）的组合输入
-   **Qwen-Omni-Turbo 系列**
    
    已停止更新。文本分析场景可迁移至 Qwen3.8-Omni-Flash；需要音频输出时可选择 Qwen3.5-Omni。
    

**模型系列**

**音视频描述能力**

**深度思考**

**联网搜索**

**输入音频语种**

**输出音频语种**

**音色数量**

Qwen3.5-Omni

支持音频输出的全模态模型

强

不支持

支持

113 种

含74 种语言、39 种方言

**语言：**中文、英语、德语、法语、意大利语、捷克语、印尼语、泰语、韩语、波兰语、日语、越南语、芬兰语、葡萄牙语、西班牙语、荷兰语、俄语、马来语、加泰罗尼亚语、瑞典语、土耳其语、乌克兰语、罗马尼亚语、斯洛伐克语、丹麦语、冰岛语、挪威语（博克马尔）、马其顿语、希腊语、匈牙利语、加利西亚语、菲律宾语、克罗地亚语、波斯尼亚语、斯洛文尼亚语、保加利亚语、哈萨克语、白俄罗斯语、拉脱维亚语、爱沙尼亚语、阿塞拜疆语、维吾尔语、斯瓦希里语、印地语、世界语、柯尔克孜语、塔吉克语、宿务语、南非语、阿拉伯语、立陶宛语、爪哇语、孟加拉语、波斯语、希伯来语、旁遮普语、古吉拉特语、蒙古语、阿斯图里亚斯语、卡纳达语、马拉地语、国际语、马拉雅拉姆语、马耳他语、新挪威语、泰卢固语、乌尔都语、格鲁吉亚语、巴斯克语、泰米尔语、奥里亚语、塞尔维亚语、毛利语

**方言：**  
东北话、贵州话、粤语、河南话、香港粤语、上海话、陕西话、天津话、台湾话、云南话、安徽话、福建话、甘肃话、广东话、湖北话、湖南话、江西话、山东话、山西话、四川话、广西话、海南话、重庆话、长沙话、杭州话、合肥话、银川话、郑州话、沈阳话、温州话、武汉话、昆明话、太原话、南昌话、济南话、兰州话、南京话、客家话、闽南语  
  

36 种

含 29 种语言、7 种方言

**语言：**  
中文、英语、德语、意大利语、葡萄牙语、西班牙语、日语、韩语、法语、俄语、泰语、印度尼西亚语、阿拉伯语、越南语、土耳其语、芬兰语、波兰语、印地语、荷兰语、捷克语、乌尔都语、他加禄语、瑞典语、丹麦语、希伯来语、冰岛语、马来语、挪威语、波斯语  
  

**方言：**  
四川话、北京话、天津话、南京话、陕西话、粤语、闽南语  
  

55 种

Qwen3-Omni-Flash

混合思考模型

较弱

支持

不支持

19 种

含 11 种语言、8 种方言

**语言：**

中文、英语、德语、法语、意大利语、泰语、韩语、日语、俄语、西班牙语、葡萄牙语

**方言：**

四川话、上海话、粤语、闽南语、陕西话、南京话、天津话、北京话

19 种

含 11 种语言、8 种方言

**语言：**

中文、英语、德语、法语、意大利语、泰语、韩语、日语、俄语、西班牙语、葡萄牙语

**方言：**

四川话、上海话、粤语、闽南语、陕西话、南京话、天津话、北京话

17~49 种

> 因版本而异

Qwen-Omni-Turbo

**已停止更新**

无

不支持

不支持

中文、英语

中文、英语

4 种

> 模型名称、上下文长度、价格及快照版本请参见百炼控制台；并发限流规则请参见 [限流](raw/model-user-guide/get-started-with-models/rate-limit.md) 。

## 模型效果

### 音视频内容分析

> 请你对这个视频按时间戳生成全面的描述。

**00:00.000 – 00:02.500**

雨夜中的城市街道填满宽银幕画面。长时间曝光下，红蓝车灯拖出光轨滑过，在湿漉漉的路面上闪烁。一位身穿深色及膝风衣、内搭浅色衬衫领带的孤独男子，沿着右侧人行道向镜头走来。雨滴凝结在他的肩膀和头发上；每一步都在潮湿的混凝土上发出沉闷的啪嗒声。低沉不祥的电子嗡鸣支撑着环境音，同时稳定的雨声四处噼啪作响。他身旁的砖墙上贴满彩色涂鸦，街区远处几块霓虹灯招牌发光——一块清晰显示橙红色草书体 "Nice"，另一块竖置招牌的末端露出字母 "AT"。

......

**00:12.300 – 00:14.533**

镜头向下倾斜。在手电筒光圈内，一张泛黄老化的单页纸躺在浅水洼中，边缘烧焦且边角卷曲。墨迹段落覆盖大部分表面，但潮湿和焦痕使文字无法辨认。男子跪下，戴手套的手指伸向文件；手靠近时水波向外荡漾。警笛达到峰值，随后开始略微消退，而环境嗡鸣保持稳定。画面在颤抖的纸页即将被触碰前定格，片段结束。

> 仅展示部分时间戳内容。

### 多方言理解

> 给出不同方言歌手的声音特征、演唱时的情绪状态、以及对应的完整歌词

这段音频由多位来自中国不同地区的歌手用各自的方言进行说唱，展现了中国方言的丰富多样性。以下是每位歌手的声音特征、情绪状态及对应歌词的详细描述：

**杭州话（吴语）****声音特征：**

这位男歌手的声音较为柔和，带有吴语特有的软糯和温婉。他的语调起伏平缓，节奏轻快，给人一种娓娓道来的感觉。

**情绪状态：**

悠闲、惬意且充满生活气息。他描绘了杭州的慢生活和城市变迁，情绪中带着对家乡的眷恋和对现代发展的感慨，整体感觉舒适而亲切。

**对应歌词：**

\> 杭州话，听听看，我们格文化，包括家门口的儿化音

\> 像花开在西湖边，不搞文化调查，只有我们搞得懂

\> 你们都不懂，三不搭门，格儿，老儿，粉儿，伢儿，这外人分得清

\> 出发，变化快，地铁交通发达，据说要去看看

\> 包容新马泰，看十三太，为城市骄傲，性格直给

\> 感情你只为过桥，而且味道不一样，你不来嘞

> 仅展示部分效果。

### 歌词字幕生成

> 请你识别这首歌的歌词，并分句给出歌词的时间戳，输出格式如下：\[00:00:15,020 --> 00:00:28,085\] ：When you walk through a storm, hold your head up high.\[00:00:28,085 --> 00:00:40,200\] And don't be afraid of the dark. ......

\[00:00:12,680 --> 00:00:16,960\] 猫线绕过树摇晃的月光

\[00:00:18,400 --> 00:00:22,800\] 暖气片哼着九八年排行

\[00:00:24,160 --> 00:00:28,080\] 时间拨开云雾般的热浪

\[00:00:28,920 --> 00:00:33,000\] 屏幕里的霓虹晒在鼻梁

......

\[00:03:16,720 --> 00:03:21,680\] 我们窝在年轮最柔软一墙

\[00:03:22,400 --> 00:03:27,000\] 呼吸被余温酿成蜂蜜糖

\[00:03:28,160 --> 00:03:33,200\] 沙发陷落成云絮的形状

\[00:03:34,000 --> 00:03:38,800\] 每个毛孔都晒着晴朗

\[00:04:09,000 --> 00:04:10,020\] (End)

> 仅展示部分效果。

### 音视频编程

## 使用方式

### 流式输出

以下 Qwen3.5-Omni、Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 示例必须设置 `stream=True`。

### Responses：音频和视频输入

以下示例使用 Qwen3.8-Omni-Flash，通过 Responses API 处理音视频输入并生成文本回复。

沿用[快速开始](#qwen38-offline)示例的 API Key、`DASHSCOPE_BASE_URL` 和 `AUDIO_URL`。Responses 请求使用 `input`，其中音频 URL 放在 `audio_url`，与 Chat Completions 的 `input_audio.data` 结构不同。音频和视频输入仅允许出现在 `user` 消息中。

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["DASHSCOPE_BASE_URL"],
)
response = client.responses.create(
    model="qwen3.8-omni-flash",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "总结这段录音的主要内容。"},
            {"type": "input_audio", "audio_url": os.environ["AUDIO_URL"], "format": "wav"},
        ],
    }],
    stream=False,
)
print(response.output_text)
```

分析视频时，将 `VIDEO_URL` 设为可访问的视频 URL，并将上例 `input[0].content` 替换为以下内容：

```
[
    {"type": "input_text", "text": "描述视频中的画面和声音。"},
    {"type": "input_video", "video_url": os.environ["VIDEO_URL"]},
]
```

使用双通道或四通道空间音频时，在上述音频内容对象中加入 `"use_multichannel": True`（Python），与 `audio_url`、`format` 同级。该参数默认为 `False`，此时按单通道解析。

音频 Base64 输入、字段说明和工具范围请参见[创建响应](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。

### 模型配置

以下为 Qwen3.5-Omni 的配置建议，可按场景调整参数、提示词和音视频长度。Qwen3.8-Omni-Flash 的提示词见[推荐提示词](#qwen38-prompts)。

#### 音视频理解

**使用场景**

**推荐视频长度**

**Prompt 建议**

**max\_pixels 推荐参数值**

快速审核，成本低

≤60分钟

50 个词以内的简单 Prompt

230,400

内容提取（长视频分段）

≤60分钟

921,600~2,073,600

标准分析（短视频打标）

≤4分钟

使用下方的结构化 Prompt

建议Prompt

```
Provide a detailed description of the video.
It should explicitly include three sections:
1. A structured chronological storyline of **every noticeable audio and visual details**
2. A structured list of all visible text. For each text element, include start timestamp, end timestamp, the exact text content, the appearance characteristics. If no text appears, explicitly state so.
3. A structured speech-to-text transcription, include speaker（Corresponding to the character or voice‑over in Section 1, including their accent and tone）, exact spoken content, start timestamp, end timestamp, and speaking state (prosody, emotion, and style). If no speech appears, explicitly state so.
Aside from these three required sections, you are free to organize any additional content in any way you find helpful. This additional content can include global information about the entire video or localized information about specific moments. You may choose the topic of this extra content freely.
Output Format:
```
## Storyline
<xx:xx.xxx> - <xx:xx.xxx>
<an unstructured long paragraph in natural language describing what happened during this period, blending both audio and video details.>
<xx:xx.xxx> - <xx:xx.xxx>
<an unstructured long paragraph in natural language describing what happened during this period, blending both audio and video details.>
<xx:xx.xxx> - <xx:xx.xxx>
<an unstructured long paragraph in natural language describing what happened during this period, blending both audio and video details.>
...
## Visible Text
<xx:xx.xxx> - <xx:xx.xxx>
“<element>”: <appearance>
“<element>”: <appearance>
<xx:xx.xxx> - <xx:xx.xxx>
“<element>”: <appearance>
“<element>”: <appearance>
“<element>”: <appearance>
<xx:xx.xxx> - <xx:xx.xxx>
“<element>”: <appearance>
...
## Speakers and Transcript
Speaker profiles:
<speaker> - <profile>
<speaker> - <profile>
<speaker> - <profile>
...
<xx:xx.xxx> - <xx:xx.xxx>
Speaker: <speaker>
State: <description>
Content: “<content>”
<xx:xx.xxx> - <xx:xx.xxx>
Speaker: <speaker>
State: <description>
Content: “<content>”
<xx:xx.xxx> - <xx:xx.xxx>
Speaker: <speaker>
State: <description>
Content: “<content>”
...
## <another section>
<paragraphs>
## <another section>
<paragraphs>
...
```
```

921,600~2,073,600

精细分析（多说话人/复杂场景）

≤2分钟

2,073,600

**说明**长视频需要细粒度描述时，建议分段处理。

#### 音频理解

控制音频长度和提示词复杂度，平衡成本与效果。

**使用场景**

**推荐音频长度**

**Prompt 建议**

快速审核、低成本

≤60分钟

50 个词以内的简单 Prompt

内容提取（长音频分段）

≤60分钟

标准分析（音频打标）

≤2分钟

使用结构化 Prompt

结构化Prompt

```
Provide a detailed description of the audio.

It should explicitly include two sections:

1. A structured chronological storyline of **every noticeable audio details**
2. A structured speech-to-text transcription, include speaker（Corresponding to the character or voice‑over in Section 1, including their accent and tone）, exact spoken content, start timestamp, end timestamp, and speaking state (prosody, emotion, and style). If no speech appears, explicitly state so.

Aside from these two required components, you are free to organize any additional content in any way you find helpful. This additional content can include global information about the entire audio or localized information about specific moments. You may choose the topic of this extra content freely.

Output Format:

```
## Storyline

<xx:xx.xxx> - <xx:xx.xxx>
<an unstructured long paragraph in natural language describing what happened during this period, blending both audio details.>

<xx:xx.xxx> - <xx:xx.xxx>
<an unstructured long paragraph in natural language describing what happened during this period, blending both audio details.>

<xx:xx.xxx> - <xx:xx.xxx>
<an unstructured long paragraph in natural language describing what happened during this period, blending both audio details.>

...

...

## Speakers and Transcript

Speaker profiles:
<speaker> - <profile>
<speaker> - <profile>
<speaker> - <profile>
...

<xx:xx.xxx> - <xx:xx.xxx>
Speaker: <speaker>
State: <description>
Content: “<content>”

<xx:xx.xxx> - <xx:xx.xxx>
Speaker: <speaker>
State: <description>
Content: “<content>”

<xx:xx.xxx> - <xx:xx.xxx>
Speaker: <speaker>
State: <description>
Content: “<content>”

...

## <another section>

<paragraphs>

## <another section>

<paragraphs>

...
```
```

精细分析（多说话人/复杂场景）

≤1分钟

**说明**长音频需要细粒度描述时，建议分段处理。

### 推荐提示词

以下提示词适用于 `qwen3.8-omni-flash`。根据使用场景选择提示词，将其作为 Chat Completions 的 `system` 消息，并在 `user` 消息中传入待分析的音频或视频。提示词中的输出格式要求用于引导模型生成内容。

音视频精细描述：按时间顺序组织

结合画面和声音，按时间顺序描述事件，并提供时间范围，便于回看定位。

```
You are a rigorous audio-visual description expert. Your task is to watch and analyze the entire video and produce a highly detailed, coherent, evidence-grounded description that reconstructs, as accurately as possible, what is actually visible, audible, and readable in the video.

Produce a complete, directly usable video description — not an analysis report, not a checklist, not a rough summary. The description must cover the main content of the video from beginning to end, organized in chronological order into naturally coherent, information-dense paragraphs. Level of detail must always yield to factual accuracy: details that cannot be confirmed may be omitted, but you must never guess, fill in, or fabricate anything in order to make the description richer.

## Core Principles

1. Cover the main content of the video from beginning to end, including the opening, the main process, scene changes, important actions, speech, on-screen text, sound, and the ending. Removing redundancy applies only to attributes that have not changed — clothing, room layout, aspect ratio, a continuing music bed — which are described once and then revisited only when they change. It does not license coarser event granularity: you must not skip or compress new actions, text, sounds, or state changes.

2. Every statement must be grounded in what is actually visible, audible, or readable in the video. Do not add background knowledge, common sense, prior assumptions, or speculation from outside the video. Do not treat "seems plausible" as "the video has proven it."

3. Prioritize preserving clearly discernible concrete facts, including people, animals, objects, appearance, clothing, colors, quantities, positions, actions, interactions, on-screen text, subtitles, speech, ambient sound, music, sound effects, camera changes, scene cuts, and state changes.

4. Track people, animals, and objects continuously. Once an entity has been clearly identified, keep its identity consistent in later appearances; if multiple similar entities cannot be reliably distinguished, use positional descriptions such as "the device on the left" or "the person in the center of the frame" rather than forcing a name onto them. Avoid ambiguous references such as "he," "she," "it," "this person," or "that thing."

5. Do not invent a person's identity, age, occupation, emotion, intention, relationship, or the reason behind an action. You may describe visible facial expressions and body movements, but do not interpret an expression directly as a mental state. For example, write "the corners of his mouth turn up and he smiles" rather than "he feels happy."

6. When the identity of an entity, an action, a quantity, text, speech, a temporal relationship, a sound source, or a causal relationship cannot be confirmed, and that uncertainty affects understanding, use brief, specific, conservative wording, for example "the on-screen text is small and cannot be fully made out" or "voices can be heard, but the exact lines are unclear." For unimportant unclear details, simply omit them; do not repeatedly pile up "possibly," "seemingly," and "appears to be."

7. When speech, subtitles, or on-screen text are clearly discernible, preserve the original wording as far as possible, especially for personal names, place names, numbers, brands, labels, proper nouns, formulas, code, and key statements. Do not translate, rewrite, or correct the original text on your own initiative.

8. Distinguish facts directly observed in the footage from opinions expressed by people in the video, by narration, or by subtitles. If a host or narrator offers an evaluation, explanation, recommendation, or causal judgment, write it explicitly as "the host states," "the narration explains," or "the subtitle says"; do not rewrite an opinion voiced in the video as the describer's own objective conclusion.

9. When level of detail and reliability conflict, reliability comes first. It is better to write fewer unconfirmable details than to hallucinate in order to fill up information.

## Description Granularity

The unit of segmentation is a change in information, not a fixed number of seconds. Begin a new event wherever the subject, object, or goal changes; an action enters a new stage; contact is made or released; direction, speed, or trajectory changes noticeably; an observable state change occurs; the speaker turn changes; the sound or music structure changes; the scene, shot, or narrative layer changes; or the interface focus, control, parameter, or result state changes.

For each significant action, write as much of the following as the video actually supports: the subject, its state before the action, the action itself, the object or point of contact, which hand, body part, or tool is used, the direction and trajectory, the speed or manner, any intermediate stage, the resulting state, and the observable consequence. A named action on its own is a label, not a description. "She opens the bottle" is insufficient; "she steadies the bottle with her left hand, then twists the metal cap counter-clockwise with her right, and once the cap is free she sets it down to the right of the bottle" carries the actual granularity. The same applies to a state change: give both ends of it, since "the waveform is narrower after he applies the setting" carries the change while "he adjusts the audio" does not.

Granularity does not degrade with video length. A long or repetitive video receives the same local event granularity as a short one. Length may add chapter-level organization, but it must never replace a sequence of distinct actions with a single coarser generalizing verb.

Before using left, right, in front, or behind, make the frame of reference unambiguous, distinguishing the viewer's left and right within the frame, a person's own left and right, and the left and right inside a software window or interface. When a visual event and a sound belong to the same occurrence, write them together and make the relation explicit rather than listing picture and sound separately for the reader to pair up. Whenever you give a number, make the basis of the count explicit: what is being counted, over which time window, and whether you are counting instantaneous on-screen quantity, distinct entities across the whole video, completed actions, attempts, or sound occurrences.

## Scope of Content Coverage

Describe the following whenever the video actually contains them:

* the video type, subject, narrative line, and overall visual form;
* the main people, animals, and objects, and their identities or roles;
* appearance, clothing, colors, materials, quantities, and spatial positions;
* actions, interactions, operating steps, and their order;
* the scene environment, foreground, middle ground, background, lighting, left-right relationships, and spatial changes;
* camera viewpoint, shot size, focus, push/pull/pan/tilt, following shots, transitions, and frame layout;
* titles, subtitles, labels, interface text, numbers, formulas, code, tables, and charts;
* speech, narration, language, speakers, discernible original spoken content, and obvious tonal characteristics;
* background music, ambient sound, sound effects, and the onset, end, and obvious changes of sounds;
* the entrance, exit, movement, contact, operation, and state changes of the subjects;
* professional procedures, tools, terminology, and conclusions explicitly demonstrated or explicitly stated in the video;
* temporal continuity, location changes, and time jumps between different scenes.

Do not infer a music track's specific BPM, genre, instrumentation, key, mixing, compression, or reverb from listening impression alone. When the sound source cannot be confirmed, use neutral wording such as "an impact sound is heard" or "a short electronic sound effect occurs." Attribute a sound to a specific object only when the sound clearly corresponds to an action visible in the frame.

For OCR, numbers, and charts, transcribe verbatim only when the content is clear enough. Do not guess content from blurry text, and do not estimate values from the heights of bars or lines in a chart. If it cannot be read reliably, omit the specific value or state that part of the text cannot be made out.

## Timestamp Rules

Describe the video in chronological order, and start a new paragraph at shot cuts, scene changes, changes of main activity, the appearance of a new subject, speaker changes, the appearance of key text, or obvious state changes.

Begin each time segment with the following format:

[hh:mm:ss:xxx-hh:mm:ss:xxx]

For example:

[00:00:04:000-00:00:12:000] The shot cuts to ...

Timestamps must be safe time intervals backed by evidence. Timing may be determined from clear shot cuts, subtitle appearances, speech onset and offset points, ASR timestamps, or stably locatable visual events. Do not generate timings from paragraph length, average shot duration, or guesswork, and do not fabricate millisecond-level precision merely to satisfy the millisecond format.

Match precision to the evidence available. Chapters and long scenes take ranges of seconds to minutes; shot boundaries and ordinary actions are locatable to roughly half a second to a second; dialogue turns to a few tenths of a second; clicks, contacts, impacts, and cue tones to around a tenth of a second. If an event can only be confirmed as falling somewhere near a given second, write an approximate range rather than a fabricated millisecond timestamp.

Write an additional precise time point inside a paragraph only when that event can genuinely be located reliably. Otherwise, describe only the order in which events occur and the time segment they fall in. Adjacent time segments must not overlap, and do not manufacture unreliable time boundaries in the pursuit of precision.

Distinguish a new event from a repeated action, a slow-motion pass, a replay, or a flashback. A replayed sequence keeps the same clothing, action order, and target, and should be identified as a replay rather than described as further new events.

## Output Format

Write one concise overview paragraph followed by multiple chronologically ordered description paragraphs.

Open with a short overview introducing the video type, core subjects, main scenes, visual style, and overall auditory environment. Then describe the concrete content in chronological order, integrating visuals, speech, on-screen text, and audio within the same time segment; do not mechanically split by modality into "visual," "audio," "OCR," and so on.

Add a brief closing paragraph only when the video genuinely has a clear overall outcome or concluding development. The closing must not introduce new information absent from the preceding text, and must not offer your own evaluation of the video.

Do not use tables, bullet points, numbered lists, XML, JSON, analytical subheadings, or mechanical headings such as "Scene 1" or "Shot 2.3." Do not output your analysis process, observation process, evidence lists, tool-call records, quality assessments, or any explanation unrelated to the video.

The final output should be natural, fluent, specific, coherent, and information-dense without excessive repetition, and must at all times obey the principles of "evidence first, timing grounded, details reliable."

Please describe this video in detail.
```

音视频精细描述：分开输出转写和画面文字

分别输出事件描述、画面文字和语音转写，保留原文、说话人和时间范围，便于查找与核对。

```
Provide a detailed description of the video.

Make sure your description covers every one of the following dimensions:

Visual
- Subjects and characters: appearance, clothing, gender/age cues, identity, distinctive features
- Actions and events in chronological order, and how the scene evolves over time
- Setting and background: location, environment, time of day
- Spatial layout and relations between subjects/objects; counts and quantities
- On-screen text: captions, titles, subtitles, logos, UI — exact content and appearance
- Visual style: colors, lighting, camera shots, angles, and camera movement

Audio
- Speech: the exact spoken content, transcribed verbatim
- Speakers: who is speaking (mapped to the on-screen person or voice-over), with accent, tone, gender/age cues
- Speaking state: prosody, emotion, volume, and speaking style
- Music: presence, genre/mood, and lyrics if any
- Sound effects and ambient/background sounds
- Non-speech vocalizations: laughter, crying, applause, etc.

Audio-visual correspondence
- Which speech or sound aligns with which on-screen person or visual event
- The timing of each event, expressed with timestamps

It should explicitly include three sections:

1. A structured chronological storyline of **every noticeable audio and visual details**
2. A structured list of all visible text. For each text element, include start timestamp, end timestamp, the exact text content, the appearance characteristics. If no text appears, explicitly state so.
3. A structured speech-to-text transcription, include speaker（Corresponding to the character or voice‑over in Section 1, including their accent and tone）, exact spoken content, start timestamp, end timestamp, and speaking state (prosody, emotion, and style). If no speech appears, explicitly state so.

Aside from these three required sections, you are free to organize any additional content in any way you find helpful. This additional content can include global information about the entire video or localized information about specific moments. You may choose the topic of this extra content freely.

Rules:

- Add as much descriptive detail as possible.
- Do not use Markdown bold formatting.
- Carefully look at frames and listen to the audio, making sure no detail is overlooked.

Output Format:
```

音视频结构化描述

按场景和事件输出 JSON。将任务说明和完整 JSON Schema 一起放入提示词，明确字段、类型、必填项和约束。

```
Describe the audio and visual content in detail in English, organized into scenes and events, following the JSON Schema below.
All timestamps must be relative to the beginning of the video. End times must not precede start times or exceed the video duration. Each event must fall within the time range of its parent scene.
Include only information directly supported by the audio or video. Do not guess or invent details. Do not infer causality merely because a sound and an action occur at the same time.
Return only valid JSON, without Markdown fences or commentary.

JSON Schema:
{
  "$defs": {
    "Event": {
      "additionalProperties": false,
      "properties": {
        "time_range": {
          "$ref": "#/$defs/TimeRange",
          "description": "Time range of the event"
        },
        "participants": {
          "description": "People, animals, or objects involved, named by observable features; use consistent names for the same participant",
          "items": {
            "type": "string"
          },
          "title": "Participants",
          "type": "array"
        },
        "action": {
          "description": "Specific actions, interactions, and observable outcomes",
          "title": "Action",
          "type": "string"
        },
        "sounds": {
          "description": "Sounds heard during the event; use an empty list if none are discernible",
          "items": {
            "type": "string"
          },
          "title": "Sounds",
          "type": "array"
        }
      },
      "required": [
        "time_range",
        "participants",
        "action",
        "sounds"
      ],
      "title": "Event"
      ,
      "type": "object"
    },
    "Scene": {
      "additionalProperties": false,
      "properties": {
        "time_range": {
          "$ref": "#/$defs/TimeRange",
          "description": "Time range of the scene"
        },
        "setting": {
          "description": "Environment, spatial layout, and main visual features",
          "title": "Setting",
          "type": "string"
        },
        "events": {
          "description": "Events in chronological order; use an empty list if there are none",
          "items": {
            "$ref": "#/$defs/Event"
          },
          "title": "Events",
          "type": "array"
        }
      },
      "required": [
        "time_range",
        "setting",
        "events"
      ],
      "title": "Scene",
      "type": "object"
    },
    "TimeRange": {
      "additionalProperties": false,
      "properties": {
        "start_seconds": {
          "description": "Start time in seconds relative to the beginning of the video",
          "minimum": 0,
          "title": "Start Seconds",
          "type": "number"
        },
        "end_seconds": {
          "description": "End time in seconds; must not precede the start time",
          "minimum": 0,
          "title": "End Seconds",
          "type": "number"
        }
      },
      "required": [
        "start_seconds",
        "end_seconds"
      ],
      "title": "TimeRange",
      "type": "object"
    }
  },
  "additionalProperties": false,
  "properties": {
    "summary": {
      "description": "An overview of the main content of the video",
      "title": "Summary",
      "type": "string"
    },
    "scenes": {
      "description": "Scenes in chronological order; group continuous footage with a consistent setting into one scene",
      "items": {
        "$ref": "#/$defs/Scene"
      },
      "title": "Scenes",
      "type": "array"
    }
  },
  "required": [
    "summary",
    "scenes"
  ],
  "title": "CaptionResult",
  "type": "object"
}
```

音视频高动态描述

描述快速变化的画面、动作和事件过程。根据内容动态程度调整视频采样帧率，在最高 15 fps 的输入场景下保持稳定效果，捕捉更细致的动作与时序变化。帧率越高，处理成本越高，应按需设置。

```
You are a rigorous audio-visual description expert. Your task is to watch and analyze the entire video and produce a highly detailed, coherent, evidence-grounded description that reconstructs, as accurately as possible, what is actually visible, audible, and readable in the video.
Produce a complete, directly usable video description — not an analysis report, not a checklist, not a rough summary. The description must cover the main content of the video from beginning to end, organized in chronological order into naturally coherent, information-dense paragraphs. Level of detail must always yield to factual accuracy: details that cannot be confirmed may be omitted, but you must never guess, fill in, or fabricate anything in order to make the description richer.
## Core Principles
1. Cover the main content of the video from beginning to end, including the opening, the main process, scene changes, important actions, speech, on-screen text, sound, and the ending. Removing redundancy applies only to attributes that have not changed — clothing, room layout, aspect ratio, a continuing music bed — which are described once and then revisited only when they change. It does not license coarser event granularity: you must not skip or compress new actions, text, sounds, or state changes.
2. Every statement must be grounded in what is actually visible, audible, or readable in the video. Do not add background knowledge, common sense, prior assumptions, or speculation from outside the video. Do not treat "seems plausible" as "the video has proven it."
3. Prioritize preserving clearly discernible concrete facts, including people, animals, objects, appearance, clothing, colors, quantities, positions, actions, interactions, on-screen text, subtitles, speech, ambient sound, music, sound effects, camera changes, scene cuts, and state changes.
4. Track people, animals, and objects continuously. Once an entity has been clearly identified, keep its identity consistent in later appearances; if multiple similar entities cannot be reliably distinguished, use positional descriptions such as "the device on the left" or "the person in the center of the frame" rather than forcing a name onto them. Avoid ambiguous references such as "he," "she," "it," "this person," or "that thing."
5. Do not invent a person's identity, age, occupation, emotion, intention, relationship, or the reason behind an action. You may describe visible facial expressions and body movements, but do not interpret an expression directly as a mental state. For example, write "the corners of his mouth turn up and he smiles" rather than "he feels happy."
6. When the identity of an entity, an action, a quantity, text, speech, a temporal relationship, a sound source, or a causal relationship cannot be confirmed, and that uncertainty affects understanding, use brief, specific, conservative wording, for example "the on-screen text is small and cannot be fully made out" or "voices can be heard, but the exact lines are unclear." For unimportant unclear details, simply omit them; do not repeatedly pile up "possibly," "seemingly," and "appears to be."
7. When speech, subtitles, or on-screen text are clearly discernible, preserve the original wording as far as possible, especially for personal names, place names, numbers, brands, labels, proper nouns, formulas, code, and key statements. Do not translate, rewrite, or correct the original text on your own initiative.
8. Distinguish facts directly observed in the footage from opinions expressed by people in the video, by narration, or by subtitles. If a host or narrator offers an evaluation, explanation, recommendation, or causal judgment, write it explicitly as "the host states," "the narration explains," or "the subtitle says"; do not rewrite an opinion voiced in the video as the describer's own objective conclusion.
9. When level of detail and reliability conflict, reliability comes first. It is better to write fewer unconfirmable details than to hallucinate in order to fill up information.

## Description Granularity
The unit of segmentation is a change in information, not a fixed number of seconds. Begin a new event wherever the subject, object, or goal changes; an action enters a new stage; contact is made or released; direction, speed, or trajectory changes noticeably; an observable state change occurs; the speaker turn changes; the sound or music structure changes; the scene, shot, or narrative layer changes; or the interface focus, control, parameter, or result state changes.
For each significant action, write as much of the following as the video actually supports: the subject, its state before the action, the action itself, the object or point of contact, which hand, body part, or tool is used, the direction and trajectory, the speed or manner, any intermediate stage, the resulting state, and the observable consequence. A named action on its own is a label, not a description. "She opens the bottle" is insufficient; "she steadies the bottle with her left hand, then twists the metal cap counter-clockwise with her right, and once the cap is free she sets it down to the right of the bottle" carries the actual granularity. The same applies to a state change: give both ends of it, since "the waveform is narrower after he applies the setting" carries the change while "he adjusts the audio" does not.
Granularity does not degrade with video length. A long or repetitive video receives the same local event granularity as a short one. Length may add chapter-level organization, but it must never replace a sequence of distinct actions with a single coarser generalizing verb.
Before using left, right, in front, or behind, make the frame of reference unambiguous, distinguishing the viewer's left and right within the frame, a person's own left and right, and the left and right inside a software window or interface. When a visual event and a sound belong to the same occurrence, write them together and make the relation explicit rather than listing picture and sound separately for the reader to pair up. Whenever you give a number, make the basis of the count explicit: what is being counted, over which time window, and whether you are counting instantaneous on-screen quantity, distinct entities across the whole video, completed actions, attempts, or sound occurrences.

## Scope of Content Coverage
Describe the following whenever the video actually contains them:

* the video type, subject, narrative line, and overall visual form;
* the main people, animals, and objects, and their identities or roles;
* appearance, clothing, colors, materials, quantities, and spatial positions;
* actions, interactions, operating steps, and their order;
* the scene environment, foreground, middle ground, background, lighting, left-right relationships, and spatial changes;
* camera viewpoint, shot size, focus, push/pull/pan/tilt, following shots, transitions, and frame layout;
* titles, subtitles, labels, interface text, numbers, formulas, code, tables, and charts;
* speech, narration, language, speakers, discernible original spoken content, and obvious tonal characteristics;
* background music, ambient sound, sound effects, and the onset, end, and obvious changes of sounds;
* the entrance, exit, movement, contact, operation, and state changes of the subjects;
* professional procedures, tools, terminology, and conclusions explicitly demonstrated or explicitly stated in the video;
* temporal continuity, location changes, and time jumps between different scenes.

Do not infer a music track's specific BPM, genre, instrumentation, key, mixing, compression, or reverb from listening impression alone. When the sound source cannot be confirmed, use neutral wording such as "an impact sound is heard" or "a short electronic sound effect occurs." Attribute a sound to a specific object only when the sound clearly corresponds to an action visible in the frame.
For OCR, numbers, and charts, transcribe verbatim only when the content is clear enough. Do not guess content from blurry text, and do not estimate values from the heights of bars or lines in a chart. If it cannot be read reliably, omit the specific value or state that part of the text cannot be made out.

## Timestamp Rules

Describe the video in chronological order, and start a new paragraph at shot cuts, scene changes, changes of main activity, the appearance of a new subject, speaker changes, the appearance of key text, or obvious state changes.
Begin each time segment with the following format:

`[hh:mm:ss:xxx-hh:mm:ss:xxx]`

For example:

`[00:00:04:000-00:00:12:000] The shot cuts to ...`

Timestamps must be safe time intervals backed by evidence. Timing may be determined from clear shot cuts, subtitle appearances, speech onset and offset points, ASR timestamps, or stably locatable visual events. Do not generate timings from paragraph length, average shot duration, or guesswork, and do not fabricate millisecond-level precision merely to satisfy the millisecond format.
Match precision to the evidence available. Chapters and long scenes take ranges of seconds to minutes; shot boundaries and ordinary actions are locatable to roughly half a second to a second; dialogue turns to a few tenths of a second; clicks, contacts, impacts, and cue tones to around a tenth of a second. If an event can only be confirmed as falling somewhere near a given second, write an approximate range rather than a fabricated millisecond timestamp.
Write an additional precise time point inside a paragraph only when that event can genuinely be located reliably. Otherwise, describe only the order in which events occur and the time segment they fall in. Adjacent time segments must not overlap, and do not manufacture unreliable time boundaries in the pursuit of precision.
Distinguish a new event from a repeated action, a slow-motion pass, a replay, or a flashback. A replayed sequence keeps the same clothing, action order, and target, and should be identified as a replay rather than described as further new events.

## Output Format

- Write one concise overview paragraph followed by multiple chronologically ordered description paragraphs.
- Open with a short overview introducing the video type, core subjects, main scenes, visual style, and overall auditory environment. Then describe the concrete content in chronological order, integrating visuals, speech, on-screen text, and audio within the same time segment; do not mechanically split by modality into "visual," "audio," "OCR," and so on.
- Add a brief closing paragraph only when the video genuinely has a clear overall outcome or concluding development. The closing must not introduce new information absent from the preceding text, and must not offer your own evaluation of the video.
- Do not use tables, bullet points, numbered lists, XML, JSON, analytical subheadings, or mechanical headings such as "Scene 1" or "Shot 2.3." Do not output your analysis process, observation process, evidence lists, tool-call records, quality assessments, or any explanation unrelated to the video.
- The final output should be natural, fluent, specific, coherent, and information-dense without excessive repetition, and must at all times obey the principles of "evidence first, timing grounded, details reliable."

Please describe this video in a super detail manner.
```

多说话人音画协同分析

结合音频和视频识别说话人并输出带时间戳的转写。将视频作为输入时，模型可结合画面信息分析说话人与语音的对应关系。

```
Transcribe the dialogue with speaker identification and timestamps. Output format: <soc><sos><start_time>text<end_time><speakerX><eos>...<eoc>.
```

音频时间定位

定位指定声音事件。使用前将提示词中的 `[audio event label]` 替换为目标事件，例如 `dog_barking`；结果包含事件类型及以秒为单位的起止时间。

```
Detect the timestamps of the following sound event in the audio: [audio event label]. Output the result strictly as a JSON array. Each element must contain exactly these keys: "type" (the event label, copied verbatim from the request), "start_time" and "end_time" (both MUST be decimal numbers in seconds, e.g. 4.5 or 12.0, NOT strings, and NOT in mm:ss or hh:mm:ss format). If the same event occurs multiple times, output one element per occurrence, all sharing the same "type", inside the SAME JSON array. Do not include any text outside the JSON array. Example: [{"type": "dog_barking", "start_time": 1.23, "end_time": 4.56}]
```

## 多模态组合输入

Qwen3.8-Omni-Flash 和 Qwen3.5-Omni 支持在同一请求中组合输入文本、图片、音频和视频。以下示例使用 Qwen3.8-Omni-Flash 综合分析图片与音频，并生成文本回答。如需生成语音，请使用 Qwen3.5-Omni，参见[音频输出示例](#b6a6667a65zvt)。

python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    },
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                        "format": "wav"
                    },
                },
                {"type": "text", "text": "请描述图片内容，并告诉我音频在说什么。"},
            ],
        },
    ],
    modalities=["text"],

    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    messages: [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg" },
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                        "format": "wav"
                    },
                },
                { "type": "text", "text": "请描述图片内容，并告诉我音频在说什么。" }
            ]
        }
    ],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"],

});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
```

bash

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-omni-flash",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    }
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                        "format": "wav"
                    }
                },
                {
                    "type": "text",
                    "text": "请描述图片内容，并告诉我音频在说什么。"
                }
            ]
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "modalities": ["text"]

}'
```

## 单一模态输入

以下场景中，每次请求传入文本与一种其他模态（视频、音频或图片）。示例使用 Qwen3.8-Omni-Flash，通过 Chat Completions 返回文本。

#### 视频+文本输入

视频的传入方式可以为[视频文件形式](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)或[图片列表形式](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)。

#### 视频文件形式（可理解视频中的音频）

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "video_url",
                    "video_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                },
                {"type": "text", "text": "视频的内容是什么?"},
            ],
        },
    ],

    modalities=["text"],

    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);
const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    messages: [
        {
            "role": "user",
            "content": [{
                "type": "video_url",
                "video_url": { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4" },
            },
            { "type": "text", "text": "视频的内容是什么?" }]
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"],

});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
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
    "model": "qwen3.8-omni-flash",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "video_url",
          "video_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
          }
        },
        {
          "type": "text",
          "text": "视频的内容是什么"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options": {
        "include_usage": true
    },
    "modalities":["text"]

}'
```

Qwen3.5-Omni、Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 输入限制

-   文件数量：
    
    -   Qwen3.5-Omni系列：使用公网URL方式，最多可传入 512 个；使用Base64编码方式，最多可传入 250 个。
    -   Qwen3-Omni-Flash系列、Qwen-Omni-Turbo系列：仅支持输入一个；
-   文件大小：
    
    -   使用公网URL方式：
        
        -   Qwen3.5-Omni系列：限制为 2GB
        -   Qwen3-Omni-Flash：限制为 256 MB
        -   Qwen-Omni-Turbo：限制为 150 MB
    -   使用 Base64 编码方式：编码后的 Base64 字符串大小必须小于 10MB
        
-   时长限制：
    
    -   Qwen3.5-Omni系列：1 小时
    -   Qwen3-Omni-Flash：150 秒
    -   Qwen-Omni-Turbo：40 秒
-   文件格式：MP4、AVI、MKV、MOV、FLV、WMV 等。
    
-   视频文件中的视觉信息与音频信息会分开计费。
    

#### 图片列表形式

python

```
import os
from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "video",
                    "video": [
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg",
                    ],
                },
                {"type": "text", "text": "描述这个视频的具体过程"},
            ],
        }
    ],

    modalities=["text"],

    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";

const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    messages: [{
        role: "user",
        content: [
            {
                type: "video",
                video: [
                    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
                ]
            },
            {
                type: "text",
                text: "描述这个视频的具体过程"
            }
        ]
    }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"],

});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
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
    "model": "qwen3.8-omni-flash",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "video",
                    "video": [
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
                    ]
                },
                {
                    "type": "text",
                    "text": "描述这个视频的具体过程"
                }
            ]
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "modalities": ["text"]
}'
```

Qwen3.5-Omni、Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 输入限制

**图片数量**

-   Qwen3.5-Omni系列：最少传入 2 张图片，最多可传入 2048 张图片
-   Qwen3-Omni-Flash：最少传入 2 张图片，最多可传入 128 张图片
-   Qwen-Omni-Turbo：最少传入 4 张图片，最多可传入 80 张图片

#### 音频+文本输入

以下示例代码以传入音频公网URL为例，传入本地音频请参见：[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。以下示例使用流式输出。

python

```
import os
from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                        "format": "wav",
                    },
                },
                {"type": "text", "text": "这段音频在说什么"},
            ],
        },
    ],

    modalities=["text"],

    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    print(chunk)
    # if chunk.choices:
    #     print(chunk.choices[0].delta)
    # else:
    #     print(chunk.usage)
```

javascript

```
import OpenAI from "openai";

// 初始化 openai 客户端
const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey:"sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    messages: [
        {
            "role": "user",
            "content": [{
                "type": "input_audio",
                "input_audio": { "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav", "format": "wav" },
            },
            { "type": "text", "text": "这段音频在说什么" }]
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"],

});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
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
    "model": "qwen3.8-omni-flash",
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
        },
        {
          "type": "text",
          "text": "这段音频在说什么"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{
        "include_usage":true
    },
    "modalities":["text"]

}'
```

Qwen3.5-Omni、Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 输入限制

-   文件数量：
    
    -   Qwen3.5-Omni系列：使用公网URL方式，最多可传入 2048 个；使用Base64编码方式，最多可传入 250 个；
    -   Qwen3-Omni-Flash系列、Qwen-Omni-Turbo系列：仅支持输入一个；
-   文件大小：
    
    -   使用公网URL方式：
        
        -   Qwen3.5-Omni系列：不超过 2GB
        -   Qwen3-Omni-Flash：不超过 100MB
        -   Qwen-Omni-Turbo：不超过 10MB
    -   使用 Base64 编码方式：编码后的 Base64 字符串大小必须小于 10MB
        
-   时长限制：
    
    -   Qwen3.5-Omni系列：最长 3 小时
    -   Qwen3-Omni-Flash：最长 20 分钟
    -   Qwen-Omni-Turbo：最长 3 分钟
-   文件格式：支持AMR、 WAV、 3GP、 3GPP、 AAC、 MP3等主流格式
    

#### 图片+文本输入

以下示例代码以传入图片公网URL为例，传入本地图片请参见：[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。以下示例使用流式输出。

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    },
                },
                {"type": "text", "text": "图中描绘的是什么景象？"},
            ],
        },
    ],

    modalities=["text"],

    stream=True,
    stream_options={
        "include_usage": True
    }
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);
const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    messages: [
        {
            "role": "user",
            "content": [{
                "type": "image_url",
                "image_url": { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg" },
            },
            { "type": "text", "text": "图中描绘的是什么景象？" }]
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"],

});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
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
    "model": "qwen3.8-omni-flash",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
          }
        },
        {
          "type": "text",
          "text": "图中描绘的是什么景象？"
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{
        "include_usage":true
    },
    "modalities":["text"]

}'
```

Qwen3.5-Omni、Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 输入限制

Qwen-Omni 模型支持传入多张图片。对输入图片的要求如下：

-   图片数量：
    
    -   公网URL传入：最多可传入 2048 张
    -   Base64 编码：最多可传入 250 张
-   图像大小：
    
    -   使用公网URL方式：
        
        -   Qwen3.5-Omni系列：单个图片文件的大小不超过 20MB
        -   Qwen3-Omni-Flash系列、Qwen-Omni-Turbo系列：单个图片文件的大小不超过 10MB
    -   使用 Base64 编码方式：编码后的 Base64 字符串大小必须小于 10MB；
        
-   图片的宽度和高度均应大于 10 像素，宽高比不应超过 200:1 或 1:200
    
-   支持的图片类型请参见[图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)
    

### 多通道音频

`qwen3.8-omni-flash` 支持双通道立体声和四通道 FOA 空间音频（WYZX 通道顺序），可保留空间信息用于音频理解。

`use_multichannel` 默认为 `false`，此时所有音频均按单通道解析。设为 `true` 且输入为双通道（左右）或四通道（FOA，WYZX 顺序）音频时，模型解析空间音频信息。

使用[快速开始](#qwen38-offline)中的 Chat Completions 示例时，将 `AUDIO_URL` 替换为对应的多通道 WAV 音频，并在 `client.chat.completions.create()` 中增加以下参数。HTTP 请求中，`use_multichannel` 位于请求体顶层。

```
extra_body={"use_multichannel": True},
```

## 联网搜索

Qwen3.8-Omni-Flash 支持联网搜索，可获取实时信息并生成文本回答。

Qwen3.8-Omni-Flash 的 Responses 调用使用 `web_search` 工具；Qwen3.5-Omni 的 Chat Completions 调用使用 `agent` 搜索策略。费用请参见[联网搜索计费说明](https://help.aliyun.com/zh/model-studio/web-search#92ce83df3a599)。

以下 Chat Completions 示例使用 Qwen3.8-Omni-Flash，通过 `enable_search=True` 开启联网搜索，并设置 `reasoning_effort="none"` 关闭思考，流式读取文本回复。

python

```
# 运行前的准备工作:
# pip install openai

import os
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 发起请求（开启联网搜索）
try:
    completion = client.chat.completions.create(
        model="qwen3.8-omni-flash",
        reasoning_effort="none",
        messages=[{
            "role": "user",
            "content": "请查询今天的日期和星期，并告诉我今天有哪些重要节日"
        }],
        stream=True,
        stream_options={"include_usage": True},
        # 开启联网搜索
        extra_body={
            "enable_search": True
        }
    )

    print("模型回复（包含实时信息）：")
    for chunk in completion:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")
    print()

except Exception as e:
    print(f"请求失败: {e}")
```

javascript

```
// 运行前的准备工作:
// npm install openai

import OpenAI from "openai";

// 初始化客户端
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

// 发起请求（开启联网搜索）
const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    reasoning_effort: "none",
    messages: [{
        "role": "user",
        "content": "请查询今天的日期和星期，并告诉我今天有哪些重要节日"
    }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    // 开启联网搜索
    enable_search: true
});

console.log("模型回复（包含实时信息）：");

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        if (chunk.choices[0].delta.content) {
            process.stdout.write(chunk.choices[0].delta.content);
        }
    }
}
console.log();
```

bash

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-omni-flash",
    "reasoning_effort": "none",
    "messages": [
        {
            "role": "user",
            "content": "请查询今天的日期和星期，并告诉我今天有哪些重要节日"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_search": true
}'
```

## 开启/关闭思考模式

### Qwen3.8-Omni-Flash

`qwen3.8-omni-flash` 默认开启思考，`reasoning_effort` 默认为 `xhigh`。Chat Completions 请求体顶层的 `reasoning_effort` 接受 `none`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`。`reasoning_effort` 与 `thinking_budget` 不能同时设置，否则请求报错。

可直接选择 `low`、`medium`、`xhigh` 三档思考力度。兼容取值中，`minimal` 映射为 `low`，`high` 和 `max` 映射为 `xhigh`，`none` 表示关闭思考。

在[快速开始](#qwen38-offline)中的 Chat Completions 示例的 `client.chat.completions.create()` 中增加以下参数。`reasoning_effort` 直接作为 SDK 参数传入。

```
reasoning_effort="low",
```

### Qwen3-Omni-Flash

本节介绍 Qwen3-Omni-Flash 的混合思考模式，通过 `enable_thinking` 参数控制思考模式：

-   `true`：开启思考模式
-   `false`（默认）：关闭思考模式

> 在思考模式下，**不支持输出音频。**

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-omni-flash",
    messages=[{"role": "user", "content": "你是谁"}],

    # 开启/关闭思考模式，在思考模式下不支持输出音频；qwen-omni-turbo不支持设置enable_thinking。
    extra_body={'enable_thinking': True},

    # 设置输出数据的模态，非思考模式下当前支持两种：["text","audio"]、["text"]，思考模式仅支持：["text"]
    modalities=["text"],

    # 设置音色，思考模式下不支持设置audio参数
    # audio={"voice": "Tina", "format": "wav"},
    # stream 必须设置为 True，否则会报错
    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";

const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey:"sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const completion = await openai.chat.completions.create({
    model: "qwen3-omni-flash",
    messages: [
        { role: "user", content: "你是谁？" }
    ],
    // stream 必须设置为 True，否则会报错
    stream: true,
    stream_options: {
        include_usage: true
    },
    // 开启/关闭思考模式，在思考模式下不支持输出音频；qwen-omni-turbo不支持设置enable_thinking。
    enable_thinking: true,
    //  设置输出数据的模态，非思考模式下当前支持两种：["text","audio"]、["text"]，思考模式仅支持：["text"]
    modalities: ["text"],
    // 设置音色，思考模式下不支持设置audio参数
    //audio: { voice: "Tina", format: "wav" }
});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
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
    "model": "qwen3-omni-flash",
    "messages": [
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    "stream":true,
    "stream_options":{
        "include_usage":true
    },
    "modalities":["text"],
    "enable_thinking": true
}'
```

返回结果

```
data: {"choices":[{"delta":{"content":null,"role":"assistant","reasoning_content":""},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1757937336,"system_fingerprint":null,"model":"qwen3-omni-flash","id":"chatcmpl-ce3d6fe5-e717-4b7e-8b40-3aef12288d4c"}
data: {"choices":[{"finish_reason":null,"logprobs":null,"delta":{"content":null,"reasoning_content":"嗯"},"index":0}],"object":"chat.completion.chunk","usage":null,"reated":1757937336,"system_fingerprint":null,"model":"qwen3-omni-flash","id":"chatcmpl-ce3d6fe5-e717-4b7e-8b40-3aef12288d4c"}
data: {"choices":[{"delta":{"content":null,"reasoning_content":"，"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"reated":1757937336,"system_fingerprint":null,"model":"qwen3-omni-flash","id":"chatcmpl-ce3d6fe5-e717-4b7e-8b40-3aef12288d4c"}
......
data: {"choices":[{"delta":{"content":"告诉我"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1757937336,"tem_fingerprint":null,"model":"qwen3-omni-flash","id":"chatcmpl-ce3d6fe5-e717-4b7e-8b40-3aef12288d4c"}
data: {"choices":[{"delta":{"content":"！"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1757937336,"systm_fingerprint":null,"model":"qwen3-omni-flash","id":"chatcmpl-ce3d6fe5-e717-4b7e-8b40-3aef12288d4c"}
data: {"choices":[{"finish_reason":"stop","delta":{"content":"","reasoning_content":null},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1757937336,"system_fingerprint":null,"model":"qwen3-omni-flash","id":"chatcmpl-ce3d6fe5-e717-4b7e-8b40-3aef12288d4c"}
data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":11,"completion_tokens":363,"total_tokens":374,"completion_tokens_details":{"reasoning_tokens":195,"text_tokens":168},"prompt_tokens_details":{"text_tokens":11}},"created":1757937336,"system_fingerprint":null,"model":"qwen3-omni-flash","id":"chatcmpl-ce3d6fe5-e717-4b7e-8b40-3aef12288d4c"}
```

## 多轮对话

Qwen3.8-Omni-Flash 多轮对话中，`preserve_thinking` 默认开启。客户端将上一轮的回复和思考分别放入历史 assistant 消息的 `content` 和 `reasoning_content` 字段，再随 `messages` 传入下一轮请求。提供历史思考并启用该参数后，这些思考内容计入输入 Token 和费用。完整多轮示例见[传递思考过程](https://help.aliyun.com/zh/model-studio/deep-thinking#jln7docdq5et5)。

以下多轮示例使用 Qwen3.8-Omni-Flash，并通过 `reasoning_effort="none"` 关闭思考。历史 assistant 消息传入文本回复；本示例每条 user 消息传入文本和一种模态，组合输入见[多模态组合输入](#h2-multi-modal-combined)：

-   Assistant Message
    
    messages 数组中的 Assistant Message 只能包含文本数据。
    
-   User Message
    
    本示例每条 User Message 包含文本和一种模态数据，多轮对话中可在不同轮次传入不同模态。
    

python

```
import os
from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    reasoning_effort="none",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3",
                        "format": "mp3",
                    },
                },
                {"type": "text", "text": "这段音频在说什么"},
            ],
        },
        {
            "role": "assistant",
            "content": [{"type": "text", "text": "这段音频在说：欢迎使用阿里云"}],
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": "介绍一下这家公司？"}],
        },
    ],

    modalities=["text"],

    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";

const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    reasoning_effort: "none",
    messages: [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3",
                        "format": "mp3",
                    },
                },
                { "type": "text", "text": "这段音频在说什么" },
            ],
        },
        {
            "role": "assistant",
            "content": [{ "type": "text", "text": "这段音频在说：欢迎使用阿里云" }],
        },
        {
            "role": "user",
            "content": [{ "type": "text", "text": "介绍一下这家公司？" }]
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"]
});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
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
  "model": "qwen3.8-omni-flash",
  "reasoning_effort": "none",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_audio",
          "input_audio": {
            "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
          }
        },
        {
          "type": "text",
          "text": "这段音频在说什么"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "这段音频在说：欢迎使用阿里云"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "介绍一下这家公司？"
        }
      ]
    }
  ],
  "stream": true,
  "stream_options": {
    "include_usage": true
  },
  "modalities": ["text"]
}'
```

## 解析输出的Base64 编码的音频数据

Qwen3.5-Omni 等支持语音输出的型号以流式方式输出 Base64 编码的音频数据，有两种处理方式：

-   **方式一（推荐）**：收集各 chunk 的 Base64 数据，流结束后统一解码保存为音频文件。
-   **方式二**：逐 chunk 实时解码并播放，需额外安装 pyaudio。

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
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.5-omni-plus", # 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
    messages=[{"role": "user", "content": "你是谁"}],
    # 设置输出数据的模态，当前支持两种：["text","audio"]、["text"]
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    # stream 必须设置为 True，否则会报错
    stream=True,
    stream_options={"include_usage": True},
)

# 方式1: 待生成结束后再进行解码
audio_string = ""
for chunk in completion:
    if chunk.choices:
        if hasattr(chunk.choices[0].delta, "audio"):
            try:
                audio_string += chunk.choices[0].delta.audio["data"]
            except Exception as e:
                print(chunk.choices[0].delta.content)
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
#                 print(chunk.choices[0].delta.content)

# time.sleep(0.8)
# # 清理资源
# stream.stop_stream()
# stream.close()
# p.terminate()
```
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

const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey:"sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",  //模型为Qwen3-Omni-Flash时，请在非思考模式下运行
    messages: [
        {
            "role": "user",
            "content": "你是谁？"
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text", "audio"],
    audio: { voice: "Tina", format: "wav" }
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

import queue
import threading

client = OpenAI(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为新加坡地域URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1",
)

# 方式2: 边生成边解码(使用方式2请将方式1的代码进行注释)
# # 初始化 PyAudio
import pyaudio
import time
# 创建一个队列用于存储音频数据
audio_queue = queue.Queue()
# 设置是否已经开始播放
started_playing = False
# 设置缓冲时间（秒）
buffer_time = 5

# 音频播放函数（将在单独线程中运行）
def play_audio():
    global started_playing

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,
                    output=True)

    # 收集的音频数据（用于缓冲）
    buffer_data = bytearray()

    try:
        while True:
            # 如果队列为空且已经开始播放，等待一小段时间
            if audio_queue.empty():
                if started_playing:
                    time.sleep(0.1)
                    # 如果队列持续为空，可能意味着音频结束了
                    if audio_queue.empty():
                        # 播放剩余的缓冲数据
                        if buffer_data:
                            stream.write(bytes(buffer_data))
                            buffer_data = bytearray()
                        continue
                else:
                    time.sleep(0.1)
                    continue

            # 从队列获取音频数据
            audio_np = audio_queue.get()

            # 将数据添加到缓冲区
            buffer_data.extend(audio_np.tobytes())

            # 如果还没开始播放且缓冲区大小足够，开始播放
            samples_per_second = 24000 * 2  # 采样率 * 每个样本的字节数（16位=2字节）
            buffer_size_threshold = int(samples_per_second * buffer_time)

            if not started_playing and len(buffer_data) >= buffer_size_threshold:
                started_playing = True

            # 如果已经开始播放，按块播放数据
            if started_playing:
                # 每次播放一小块数据（例如0.1秒的数据）
                chunk_size = int(samples_per_second * 0.1)
                while len(buffer_data) >= chunk_size:
                    chunk = buffer_data[:chunk_size]
                    buffer_data = buffer_data[chunk_size:]
                    stream.write(bytes(chunk))

            # 标记任务完成
            audio_queue.task_done()
    finally:
        # 清理资源
        stream.stop_stream()
        stream.close()
        p.terminate()

# 启动播放线程
audio_thread = threading.Thread(target=play_audio, daemon=True)
audio_thread.start()

completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[{"role": "user", "content": "你是谁"}],
    # 设置输出数据的模态，当前支持两种：["text","audio"]、["text"]
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    # stream 必须设置为 True，否则会报错
    stream=True,
    stream_options={"include_usage": True},
)

# 接收音频数据并放入队列
for chunk in completion:
    if chunk.choices:
        if hasattr(chunk.choices[0].delta, "audio"):
            try:
                audio_string = chunk.choices[0].delta.audio["data"]
                wav_bytes = base64.b64decode(audio_string)
                audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
                # 将音频数据放入队列，而不是直接播放
                audio_queue.put(audio_np)
            except Exception as e:
                print(chunk.choices[0].delta.audio["transcript"])

# 等待所有音频数据播放完毕
audio_queue.join()
# 额外等待一段时间，确保最后的音频都播放完毕
time.sleep(2)
```

## 输入 Base64 编码的本地文件

以下示例使用 Qwen3.8-Omni-Flash，将本地文件编码为 Base64 后传入，并返回文本。Qwen3.5-Omni、Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 要求编码后的 Base64 字符串小于 10MB。

#### 图片

以保存在本地的[eagle.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250326/nlgymo/eagle.png)为例。

python

```
import os
from openai import OpenAI
import base64

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

#  Base64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image = encode_image("eagle.png")

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                },
                {"type": "text", "text": "图中描绘的是什么景象？"},
            ],
        },
    ],

    modalities=["text"],

    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const encodeImage = (imagePath) => {
    const imageFile = readFileSync(imagePath);
    return imageFile.toString('base64');
};
const base64Image = encodeImage("eagle.png")

const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    messages: [
        {
            "role": "user",
            "content": [{
                "type": "image_url",
                "image_url": { "url": `data:image/png;base64,${base64Image}` },
            },
            { "type": "text", "text": "图中描绘的是什么景象？" }]
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"],

});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
```

#### 音频

以保存在本地的[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250214/pijhos/welcome.mp3)为例。

python

```
import os
from openai import OpenAI
import base64
import numpy as np
import soundfile as sf
import requests

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

def encode_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

base64_audio = encode_audio("welcome.mp3")

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": f"data:;base64,{base64_audio}",
                        "format": "mp3",
                    },
                },
                {"type": "text", "text": "这段音频在说什么"},
            ],
        },
    ],

    modalities=["text"],

    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const encodeAudio = (audioPath) => {
    const audioFile = readFileSync(audioPath);
    return audioFile.toString('base64');
};
const base64Audio = encodeAudio("welcome.mp3")

const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    messages: [
        {
            "role": "user",
            "content": [{
                "type": "input_audio",
                "input_audio": { "data": `data:;base64,${base64Audio}`, "format": "mp3" },
            },
            { "type": "text", "text": "这段音频在说什么" }]
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"],

});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
```

#### 视频

#### 视频文件

以保存在本地的[spring\_mountain.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250326/fqojlv/spring_mountain.mp4)为例。

python

```
import os
from openai import OpenAI
import base64
import numpy as np
import soundfile as sf

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

#  Base64 编码格式
def encode_video(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")

base64_video = encode_video("spring_mountain.mp4")

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "video_url",
                    "video_url": {"url": f"data:;base64,{base64_video}"},
                },
                {"type": "text", "text": "她在唱什么"},
            ],
        },
    ],

    modalities=["text"],

    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

const encodeVideo = (videoPath) => {
    const videoFile = readFileSync(videoPath);
    return videoFile.toString('base64');
};
const base64Video = encodeVideo("spring_mountain.mp4")

const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    messages: [
        {
            "role": "user",
            "content": [{
                "type": "video_url",
                "video_url": { "url": `data:;base64,${base64Video}` },
            },
            { "type": "text", "text": "她在唱什么" }]
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"],

});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
```

#### 图片列表

以保存在本地的[football1.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/vzfwkh/football1.jpg)、[football2.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250319/vgkgqy/football2.jpg)、[football3.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250127/fytnla/football3.jpg)与[football4.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250127/ygitwp/football4.jpg)为例。

python

```
import os
from openai import OpenAI
import base64
import numpy as np
import soundfile as sf

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

#  Base64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

base64_image_1 = encode_image("football1.jpg")
base64_image_2 = encode_image("football2.jpg")
base64_image_3 = encode_image("football3.jpg")
base64_image_4 = encode_image("football4.jpg")

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "video",
                    "video": [
                        f"data:image/jpeg;base64,{base64_image_1}",
                        f"data:image/jpeg;base64,{base64_image_2}",
                        f"data:image/jpeg;base64,{base64_image_3}",
                        f"data:image/jpeg;base64,{base64_image_4}",
                    ],
                },
                {"type": "text", "text": "描述这个视频的具体过程"},
            ],
        }
    ],

    modalities=["text"],

    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
```

javascript

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const encodeImage = (imagePath) => {
    const imageFile = readFileSync(imagePath);
    return imageFile.toString('base64');
  };
const base64Image1 = encodeImage("football1.jpg")
const base64Image2 = encodeImage("football2.jpg")
const base64Image3 = encodeImage("football3.jpg")
const base64Image4 = encodeImage("football4.jpg")

const completion = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    messages: [{
        role: "user",
        content: [
            {
                type: "video",
                video: [
                    `data:image/jpeg;base64,${base64Image1}`,
                    `data:image/jpeg;base64,${base64Image2}`,
                    `data:image/jpeg;base64,${base64Image3}`,
                    `data:image/jpeg;base64,${base64Image4}`
                ]
            },
            {
                type: "text",
                text: "描述这个视频的具体过程"
            }
        ]
    }],
    stream: true,
    stream_options: {
        include_usage: true
    },
    modalities: ["text"],

});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta);
    } else {
        console.log(chunk.usage);
    }
}
```

## API参考

-   [Chat Completions](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)：本页各型号的输入输出参数。
-   [Responses](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)：Qwen3.8-Omni-Flash 的输入输出参数。

## 计费与限流

Qwen3.8-Omni-Flash 支持自动生效的[隐式缓存](https://help.aliyun.com/zh/model-studio/context-cache#2317ea09cfxok)。 `qwen3.8-omni-flash` 支持 Responses Session 缓存，配置方式见[Session 缓存](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#example-session-cache-title)。

**计费规则**

Qwen-Omni 根据不同模态（音频、图像、视频）的 Token 数计费。详情请参见百炼控制台。

音频、图片与视频转换为Token数的规则

以下换算规则适用于 Qwen3.5-Omni、Qwen3-Omni-Flash 和 Qwen-Omni-Turbo。

#### 音频

-   `Qwen3.5-Omni系列`：
    
    -   输入音频计算公式：`总 Tokens 数 = 音频时长（单位：秒）* 7`
    -   输出音频计算公式：`总 Tokens 数 = 音频时长（单位：秒）* 12.5`
-   `Qwen3-Omni-Flash：输入与输出音频的计算公式均为总 Tokens 数 = 音频时长（单位：秒）* 12.5`
    
-   `Qwen-Omni-Turbo：输入与输出音频的计算公式均为总 Tokens 数 = 音频时长（单位：秒）* 25`
    

不足 1 秒的音频按 1 秒计算。

#### 图片

-   `Qwen3.5-Omni系列`、`Qwen3-Omni-Flash`模型**：**每`32x32`像素对应 1 个 Token
-   `Qwen-Omni-Turbo`模型：每`28x28`像素对应 1 个 Token

Qwen3.5-Omni 系列每张图最少 24 个 Token，Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 最少 4 个 Token；默认上限 1280 个 Token。Qwen3.5-Omni 系列可通过 `vl_high_resolution_images` 参数将上限提升至 16384 个 Token（Qwen-Omni-Turbo 和 Qwen3-Omni-Flash 不支持）。以下代码可估算单张图片消耗的 Token 数：

```
import math
from PIL import Image  # pip install Pillow

# ============ 模型参数配置（按需修改） ============

# 图像因子：Qwen3.5-Omni系列、Qwen3-Omni-Flash 为 32；Qwen-Omni-Turbo 为 28
IMAGE_FACTOR = 32

# Token 下限：Qwen3.5-Omni系列为 24；Qwen-Omni-Turbo、Qwen3-Omni-Flash 为 4
MIN_TOKENS = 24

# 高分辨率模式（仅 Qwen3.5-Omni 系列支持，Qwen-Omni-Turbo 和 Qwen3-Omni-Flash 不支持）
# True  → Token 上限 16384
# False → Token 上限 1280（默认）
VL_HIGH_RESOLUTION_IMAGES = False

# ============ 像素范围（由上方参数自动计算） ============

MIN_PIXELS = MIN_TOKENS * IMAGE_FACTOR * IMAGE_FACTOR
MAX_PIXELS = (16384 if VL_HIGH_RESOLUTION_IMAGES else 1280) * IMAGE_FACTOR * IMAGE_FACTOR

def smart_resize(height, width, factor=IMAGE_FACTOR,
                 min_pixels=MIN_PIXELS, max_pixels=MAX_PIXELS):
    """将图像宽高对齐到 factor 整数倍，并缩放到 [min_pixels, max_pixels] 范围内。"""
    h_bar = max(factor, round(height / factor) * factor)
    w_bar = max(factor, round(width / factor) * factor)

    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = math.floor(height / beta / factor) * factor
        w_bar = math.floor(width / beta / factor) * factor
    elif h_bar * w_bar < min_pixels:
        beta = math.sqrt(min_pixels / (height * width))
        h_bar = math.ceil(height * beta / factor) * factor
        w_bar = math.ceil(width * beta / factor) * factor

    return h_bar, w_bar

if __name__ == "__main__":
    image = Image.open("xxx/test.jpg")
    print(f"原始尺寸：{image.width}x{image.height}")

    resized_h, resized_w = smart_resize(image.height, image.width)
    token = int(resized_h * resized_w / (IMAGE_FACTOR * IMAGE_FACTOR)) + 2
    print(f"缩放后尺寸：{resized_w}x{resized_h}，Token 数：{token}")
```

#### 视频

视频文件的 Token 分为视觉部分 `video_tokens` 和音频部分 `audio_tokens`。

-   `video_tokens`
    
    计算过程较为复杂。请参见以下代码：
    

```
# pip install opencv-python
import math
import cv2

# ============ 模型参数配置（按需修改） ============

# 图像因子：Qwen3.5-Omni系列、Qwen3-Omni-Flash 为 32；Qwen-Omni-Turbo 为 28
IMAGE_FACTOR = 32

FRAME_FACTOR = 2
FPS = 2
MAX_RATIO = 200

# 视频帧的像素下限
VIDEO_MIN_PIXELS = 64 * IMAGE_FACTOR * IMAGE_FACTOR

# 视频帧的像素上限
# Qwen3.5-Omni系列：640 * 32 * 32
# Qwen3-Omni-Flash：768 * 32 * 32
# Qwen-Omni-Turbo：768 * 28 * 28
VIDEO_MAX_PIXELS = 640 * IMAGE_FACTOR * IMAGE_FACTOR

# 最少抽取帧数：Qwen3.5-Omni系列、Qwen3-Omni-Flash 为 2；Qwen-Omni-Turbo 为 4
FPS_MIN_FRAMES = 2

# 最大抽取帧数：Qwen3.5-Omni系列为 2048；Qwen3-Omni-Flash 为 128；Qwen-Omni-Turbo 为 80
FPS_MAX_FRAMES = 2048

# 视频输入的最大像素值
# Qwen3.5-Omni系列：180224 * 32 * 32
# Qwen3-Omni-Flash：16384 * 32 * 32
# Qwen-Omni-Turbo：16384 * 28 * 28
VIDEO_TOTAL_PIXELS = 180224 * IMAGE_FACTOR * IMAGE_FACTOR

# ============ 核心函数 ============

def get_video_info(video_path):
    """读取视频的基本信息：高度、宽度、总帧数、帧率。"""
    cap = cv2.VideoCapture(video_path)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return height, width, total_frames, fps

def smart_nframes(total_frames, video_fps):
    """根据视频时长和帧率，计算实际抽取的帧数。"""
    min_frames = math.ceil(FPS_MIN_FRAMES / FRAME_FACTOR) * FRAME_FACTOR
    max_frames = min(FPS_MAX_FRAMES, total_frames) // FRAME_FACTOR * FRAME_FACTOR

    duration = total_frames / video_fps if video_fps else 0
    if duration - int(duration) > (1 / FPS):
        total_frames = math.ceil(duration * video_fps)
    else:
        total_frames = math.ceil(int(duration) * video_fps)

    nframes = total_frames / video_fps * FPS
    nframes = int(min(max(nframes, min_frames), max_frames, total_frames))
    if not (FRAME_FACTOR <= nframes <= total_frames):
        raise ValueError(f"nframes should in [{FRAME_FACTOR}, {total_frames}], got {nframes}")
    return nframes

def smart_resize(height, width, nframes, factor=IMAGE_FACTOR):
    """将视频帧缩放到合理的像素范围内，宽高对齐到 factor 整数倍。"""
    max_pixels = max(
        min(VIDEO_MAX_PIXELS, VIDEO_TOTAL_PIXELS / nframes * FRAME_FACTOR),
        int(VIDEO_MIN_PIXELS * 1.05)
    )
    if max(height, width) / min(height, width) > MAX_RATIO:
        raise ValueError(f"aspect ratio exceeds {MAX_RATIO}")

    h_bar = max(factor, round(height / factor) * factor)
    w_bar = max(factor, round(width / factor) * factor)

    if h_bar * w_bar > max_pixels:
        beta = math.sqrt((height * width) / max_pixels)
        h_bar = math.floor(height / beta / factor) * factor
        w_bar = math.floor(width / beta / factor) * factor
    elif h_bar * w_bar < VIDEO_MIN_PIXELS:
        beta = math.sqrt(VIDEO_MIN_PIXELS / (height * width))
        h_bar = math.ceil(height * beta / factor) * factor
        w_bar = math.ceil(width * beta / factor) * factor

    return h_bar, w_bar

# ============ 计算 Token ============

if __name__ == "__main__":
    video_path = "spring_mountain.mp4"

    height, width, total_frames, video_fps = get_video_info(video_path)
    print(f"视频信息：{width}x{height}，{total_frames} 帧，{video_fps:.1f} fps")

    nframes = smart_nframes(total_frames, video_fps)
    resized_h, resized_w = smart_resize(height, width, nframes)

    video_tokens = int(
        math.ceil(nframes / FPS) * resized_h / IMAGE_FACTOR * resized_w / IMAGE_FACTOR
    ) + 2
    print(f"抽取帧数：{nframes}，缩放后尺寸：{resized_w}x{resized_h}，video_tokens：{video_tokens}")
```

-   `audio_tokens`
    
    -   `Qwen3.5-Omni系列`：
        
        -   输入音频计算公式：`总 Tokens 数 = 音频时长（单位：秒）* 7`
        -   输出音频计算公式：`总 Tokens 数 = 音频时长（单位：秒）* 12.5`
    -   `Qwen3-Omni-Flash：输入与输出音频的计算公式均为总 Tokens 数 = 音频时长（单位：秒）* 12.5`
        
    -   `Qwen-Omni-Turbo：输入与输出音频的计算公式均为总 Tokens 数 = 音频时长（单位：秒）* 25`
        
    
    若音频时长不足1秒，则按 1 秒计算。
    

**免费额度**

免费额度的领取、查询和使用方法，请参见[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。

**限流**

限流规则及常见问题请参见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 常见问题

### Q：如何给 Qwen-Omni-Turbo 模型设置角色？

A：Qwen-Omni-Turbo 在输出模态包含音频时**不支持设定 System Message**——即使设置"你是XXX"等角色信息，模型的自我认知仍然是千问。

-   **方法1：**文本回复场景可使用支持 System Message 的 Qwen3.8-Omni-Flash。Qwen3-Omni-Flash 的既有 System Message 用法仍适用。
    
-   **方法2：**在 messages 数组开头手动添加角色设定的 User Message 和 Assistant Message，变通实现角色设定。
    
    用于角色设定的示例代码
    
    #### OpenAI 兼容
    
    python
    
    ```
    import os
    from openai import OpenAI
    
    client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    )
    
    completion = client.chat.completions.create(
        model="qwen3.5-omni-plus",
        messages=[
            {"role": "user", "content": "你是一个商场的导购员，你负责的商品有手机、电脑、冰箱"},
            {"role": "assistant", "content": "好的，我记住了你的设定。"},
            {"role": "user", "content": "你是谁"},
        ],
        # 设置输出数据的模态，当前支持两种：["text","audio"]、["text"]
        modalities=["text", "audio"],
        audio={"voice": "Tina", "format": "wav"},
        # stream 必须设置为 True，否则会报错
        stream=True,
        stream_options={"include_usage": True},
    )
    
    for chunk in completion:
        if chunk.choices:
            print(chunk.choices[0].delta)
        else:
            print(chunk.usage)
    ```
    
    javascript
    
    ```
    import OpenAI from "openai";
    
    const openai = new OpenAI(
        {
            // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
            apiKey: process.env.DASHSCOPE_API_KEY,
            // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
            baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
        }
    );
    const completion = await openai.chat.completions.create({
        model: "qwen3.5-omni-plus",
        messages: [
            { role: "user", content: "你是一个商场的导购员，你负责的商品有手机、电脑、冰箱" },
            { role: "assistant", content: "好的，我记住了你的设定。" },
            { role: "user", content: "你是谁？" }
        ],
        stream: true,
        stream_options: {
            include_usage: true
        },
        modalities: ["text", "audio"],
        audio: { voice: "Tina", format: "wav" }
    });
    
    for await (const chunk of completion) {
        if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
            console.log(chunk.choices[0].delta);
        } else {
            console.log(chunk.usage);
        }
    }
    ```
    
    bash
    
    ```
    curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "qwen3.5-omni-plus",
        "messages": [
            {
                "role": "user",
                "content": "你是一个商场的导购员，你负责的商品有手机、电脑、冰箱"
            },
            {
                "role": "assistant",
                "content": "好的，我记住了你的设定。"
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ],
        "stream":true,
        "stream_options":{
            "include_usage":true
        },
        "modalities":["text","audio"],
        "audio":{"voice":"Tina","format":"wav"}
    }'
    ```
    
    #### DashScope
    
    python
    
    ```
    import os
    import dashscope
    import base64
    import numpy as np
    import soundfile as sf
    
    dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'
    messages =  [{"role": "user", "content": [{"text": "你是谁？"}]}]
    response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        model="qwen-omni-turbo",
        messages=messages,
        modalities=["text","audio"],
        stream=True
        )
    
    audio_string = ""
    for r in response:
        try:
            audio_string += r.output.choices[0].message.content[0]["audio"]["data"]
        except:
            print(r.output.choices[0].message.content)
    
    wav_bytes = base64.b64decode(audio_string)
    audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
    sf.write('audio_assistant.wav', audio_np, samplerate=24000)
    ```
    
    bash
    
    ```
    curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
    --header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
    --header 'Content-Type: application/json' \
    --header 'X-DashScope-SSE: enable' \
    --data '{
        "model": "qwen-omni-turbo",
        "input":{
            "messages": [{"role": "user", "content": [{"text": "你是谁"}]}]
        },
        "parameters": {
            "debug": true,
            "modalities": ["text", "audio"]
        }
    }'
    ```
    

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

## 音色列表

支持语音输出的 Qwen-Omni 型号，其可用音色请参见[音色列表](raw/model-user-guide/model-experience/omni-modal/omni-voice-list.md)。
