# Qwen-Omni

Qwen-Omni 接受文本、图片、音频、视频的多模态输入，输出文本或语音回复。支持数十种语言和方言，适用于内容审核、文本创作、视觉识别、音视频交互等场景。

**支持的地域：**北京、新加坡，需使用各地域的[API Key](raw/model-api-reference/preparations/get-api-key.md)。

## 快速开始

**前提条件**

-   已[配置API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   Qwen-Omni 模型仅支持 OpenAI 兼容方式调用，需要[安装最新版SDK](raw/model-api-reference/preparations/install-sdk.md)。OpenAI Python SDK最低版本为 1.52.0，Node.js SDK最低版本为 4.68.0。

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

-   **Qwen3.5-Omni 系列：**适用于长视频分析、会议纪要、字幕生成、内容审核、音视频交互等场景。
    
    -   输入限制：3 小时音频或 1 小时视频
    -   音频控制：支持通过指令调节音量、语速、情绪
    -   视觉能力：与 Qwen3.5 同等水平，可理解画面、语音、音效等多模态信息
    -   多模态组合输入：支持文本与图片、音频、视频的任意组合同时输入，不限于单一模态
    -   声音复刻：支持自定义音色（仅qwen3.5-omni-plus、qwen3.5-omni-flash支持，快照版本暂不支持），详情请参见[声音复刻](raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)
-   **Qwen3-Omni-Flash 系列：**适用于短视频分析、成本敏感场景。
    
    -   输入限制：150 秒以内音视频
    -   思考模式：Qwen-Omni 系列中唯一支持思考模式的系列
    -   输入模态：仅支持文本与单一其他模态（图片、音频或视频）的组合输入
-   **Qwen-Omni-Turbo 系列**
    
    已停止更新，功能受限。建议迁移至 Qwen3.5-Omni 系列或 Qwen3-Omni-Flash 系列。
    

**模型系列**

**音视频描述能力**

**深度思考**

**联网搜索**

**输入音频语种**

**输出音频语种**

**音色数量**

Qwen3.5-Omni

最新一代全模态模型

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

#### 流式输出

Qwen-Omni 的所有请求必须设置 `stream=True`。

#### 模型配置

根据使用场景配置参数、提示词和音视频长度，在成本、速度与效果之间取得平衡。

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

## 多模态组合输入

**说明**多模态组合输入仅 Qwen3.5-Omni 系列支持，可在同一请求中同时传入多种模态数据（如图片+音频+文本、视频+图片+文本等任意组合）。

以下示例展示如何在一个请求中同时传入图片和音频，由模型综合分析多模态内容。

#### OpenAI 兼容

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
    model="qwen3.5-omni-plus",
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
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
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
    model: "qwen3.5-omni-plus",
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
    "modalities": ["text", "audio"],
    "audio": {"voice": "Tina", "format": "wav"}
}'
```

## 单一模态输入

以下场景中，每次请求仅传入文本与一种其他模态（视频、音频或图片）的组合，所有 Qwen-Omni 模型均支持。

#### 视频+文本输入

视频的传入方式可以为[视频文件形式](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)或[图片列表形式](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)。

#### 视频文件形式（可理解视频中的音频）

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
    

#### OpenAI 兼容

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
    model="qwen3.5-omni-plus", # 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    model: "qwen3.5-omni-plus", // 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.5-omni-plus",
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
    "modalities":["text","audio"],
    "audio":{"voice":"Tina","format":"wav"}
}'
```

#### 图片列表形式

**图片数量**

-   Qwen3.5-Omni系列：最少传入 2 张图片，最多可传入 2048 张图片
-   Qwen3-Omni-Flash：最少传入 2 张图片，最多可传入 128 张图片
-   Qwen-Omni-Turbo：最少传入 4 张图片，最多可传入 80 张图片

#### OpenAI 兼容

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
    model="qwen3.5-omni-plus", # 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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

const openai = new OpenAI({
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",  // 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.5-omni-plus",
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
    "modalities": ["text", "audio"],
    "audio": {
        "voice": "Tina",
        "format": "wav"
    }
}'
```

#### 音频+文本输入

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
    

以下示例代码以传入音频公网URL为例，传入本地音频请参见：[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。当前只支持以流式输出的方式进行调用。

#### OpenAI 兼容

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
    model="qwen3.5-omni-plus", # 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    # 设置输出数据的模态，当前支持两种：["text","audio"]、["text"]
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    # stream 必须设置为 True，否则会报错
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
    model: "qwen3.5-omni-plus",  // 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.5-omni-plus",
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
    "modalities":["text","audio"],
    "audio":{"voice":"Tina","format":"wav"}
}'
```

#### 图片+文本输入

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
    

以下示例代码以传入图片公网URL为例，传入本地图片请参见：[输入 Base64 编码的本地文件](https://help.aliyun.com/zh/model-studio/qwen-omni#c516d1e824x03)。当前只支持以流式输出的方式进行调用。

#### OpenAI 兼容

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
    model="qwen3.5-omni-plus", # 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    # 设置输出数据的模态，当前支持两种：["text","audio"]、["text"]
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    # stream 必须设置为 True，否则会报错
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
    // 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
    model: "qwen3.5-omni-plus",
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
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.5-omni-plus",
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
    "modalities":["text","audio"],
    "audio":{"voice":"Tina","format":"wav"}
}'
```

## 联网搜索

Qwen3.5-Omni 系列支持联网搜索，获取实时信息后进行推理分析。

-   联网搜索功能仅在 **Qwen3.5-Omni 系列**模型中支持，仅支持 `agent` 搜索策略。
-   计费请参考[计费说明](https://help.aliyun.com/zh/model-studio/web-search#92ce83df3a599)中的`agent`策略。

通过 `enable_search` 参数开启联网搜索。以下示例查询实时信息：

#### OpenAI 兼容

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
        model="qwen3.5-omni-plus",
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
    model: "qwen3.5-omni-plus",
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
    "model": "qwen3.5-omni-plus",
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

Qwen-Omni 系列中，仅 Qwen3-Omni-Flash 属于混合思考模型，通过 `enable_thinking` 参数控制思考模式：

-   `true`：开启思考模式
-   `false`（默认）：关闭思考模式

> 在思考模式下，**不支持输出音频。**

#### OpenAI 兼容

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

使用 Qwen-Omni 多轮对话时，注意以下限制：

-   Assistant Message
    
    messages 数组中的 Assistant Message 只能包含文本数据。
    
-   User Message
    
    每条 User Message 只能包含文本和一种模态数据，多轮对话中可在不同轮次传入不同模态。
    

#### OpenAI 兼容

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
    model="qwen3.5-omni-plus", # 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    # 设置输出数据的模态，当前支持两种：["text","audio"]、["text"]
    modalities=["text"],
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
     // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",  // 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
  "model": "qwen3.5-omni-plus",
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

Qwen-Omni 以流式输出 Base64 编码的音频数据，有两种处理方式：

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

> 使用 Base64 编码方式传入文件时，编码后的 Base64 字符串大小必须小于 10MB。

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
    model="qwen3.5-omni-plus",# 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    model: "qwen3.5-omni-plus",  // 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    model="qwen3.5-omni-plus", # 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    model: "qwen3.5-omni-plus",  // 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    model="qwen3.5-omni-plus", # 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    model: "qwen3.5-omni-plus",  // 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    model="qwen3.5-omni-plus",  # 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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
    model: "qwen3.5-omni-plus",  // 模型为Qwen3-Omni-Flash时，请在非思考模式下运行
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

## API参考

Qwen-Omni 模型的输入输出参数详情，请参见[OpenAI兼容-Chat](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

## 计费与限流

**计费规则**

Qwen-Omni 根据不同模态（音频、图像、视频）的 Token 数计费。详情请参见百炼控制台。

音频、图片与视频转换为Token数的规则

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

Qwen3.5-Omni 系列每张图最少 24 个 Token，其他模型最少 4 个 Token；默认上限 1280 个 Token。Qwen3.5-Omni 系列可通过 `vl_high_resolution_images` 参数将上限提升至 16384 个 Token（Qwen-Omni-Turbo 和 Qwen3-Omni-Flash 不支持）。以下代码可估算单张图片消耗的 Token 数：

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

-   **方法1（推荐）：**Qwen3-Omni-Flash 已支持 System Message，建议切换至该系列。
    
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

Qwen-Omni 支持的音色列表请参见[音色列表](raw/model-user-guide/model-experience/omni-modal/omni-voice-list.md)。
