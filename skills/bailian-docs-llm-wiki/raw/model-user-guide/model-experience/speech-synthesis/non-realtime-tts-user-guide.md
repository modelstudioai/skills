# 非实时语音合成

非实时语音合成通过HTTP API将文本转换为语音，适用于有声书制作、在线教育配音、内容制作等对延迟要求不高的场景，支持丰富音色、多语言、声音复刻与声音设计。

## 概述

通过HTTP API将完整文本转换为语音文件，支持非流式和流式两种输出模式。

-   **非流式**返回音频文件 URL，有效期 24 小时；**流式**逐段返回音频数据。
-   支持多种语言，含中文方言。
-   支持[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)与[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)进行定制音色创建。
-   支持[指令控制](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#nrt_instruct_h3)，通过自然语言指令控制语音表现力。
-   支持[情感与富语言标签](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#nrt_emtag_h3)，可在文本中嵌入标签控制情感表达或插入拟声效果

**说明**各模型系列的调用端点不同：Qwen-Audio-TTS 与 CosyVoice 使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer`；Qwen-TTS 使用 `https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`；MiniMax 使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。端点不可混用，请以各模型系列示例中的端点为准。

低延迟流式场景请参见[实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)。各模型选型建议请参见[语音合成](raw/model-user-guide/model-experience/speech-synthesis/tts-model.md)。

**说明**百炼控制台**音色设计**页面合成的语音仅支持在线试听，无法下载音频文件。如需下载音频，请通过 API 或 SDK 调用。

## 前提条件

开始前，请确认已完成以下准备工作：

-   [配置API Key](raw/model-api-reference/preparations/get-api-key.md)，并[设置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
-   （可选）如果通过 DashScope SDK调用，[安装最新版SDK](raw/model-api-reference/preparations/install-sdk.md)

## 快速开始

以下各 Tab 分别演示不同模型系列的语音合成。更多语言示例和详细参数说明，请参见[API 参考](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#bb4dbbdb74em4)。

#### Qwen-Audio-TTS

以下示例演示如何使用 Qwen-Audio-TTS 模型合成语音。

**重要**Qwen-Audio-TTS 非实时语音合成仅在北京地域可用。

#### 非流式输出

非流式模式下，响应中包含合成音频的 URL，有效期为 24 小时。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-audio-3.0-tts-flash",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "longanhuan_v3.6",
      "format": "wav",
      "sample_rate": 24000
    }
}'
```

#### 流式输出

添加 `X-DashScope-SSE: enable` Header 开启流式输出，服务端以 Server-Sent Events（SSE）方式逐段返回音频数据。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-audio-3.0-tts-flash",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "longanhuan_v3.6",
      "format": "wav",
      "sample_rate": 24000
    }
}'
```

#### CosyVoice

以下示例演示如何使用 CosyVoice 模型合成语音。

**重要**CosyVoice 非实时语音合成仅在北京地域可用。

#### 非流式输出

非流式模式下，响应中包含合成音频的 URL，有效期为 24 小时。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "cosyvoice-v3-flash",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "longanyang",
      "format": "wav",
      "sample_rate": 24000
    }
}'
```

#### 流式输出

添加 `X-DashScope-SSE: enable` Header 开启流式输出，服务端以 Server-Sent Events（SSE）方式逐段返回音频数据。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "cosyvoice-v3-flash",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "longanyang",
      "format": "wav",
      "sample_rate": 24000
    }
}'
```

#### MiniMax

MiniMax 支持情感控制、语速调节和音调调整。

**重要**MiniMax 非实时语音合成仅在北京地域可用。

#### 非流式输出

非流式模式下，响应中包含完整的合成音频。

```
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "MiniMax/speech-2.8-hd",
  "input": {
    "text": "今天天气真不错，适合出去走走。",
    "voice_setting": {
      "voice_id": "male-qn-qingse",
      "speed": 1,
      "vol": 1,
      "pitch": 0,
      "emotion": "happy"
    },
    "audio_setting": {
      "sample_rate": 32000,
      "bitrate": 128000,
      "format": "mp3",
      "channel": 1
    }
  }
}'
```

#### 流式输出

添加 `X-DashScope-SSE: enable` Header 开启流式输出。

```
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key

curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
  "model": "MiniMax/speech-2.8-hd",
  "input": {
    "text": "今天天气真不错，适合出去走走。",
    "voice_setting": {
      "voice_id": "male-qn-qingse",
      "speed": 1,
      "vol": 1,
      "pitch": 0,
      "emotion": "happy"
    },
    "audio_setting": {
      "sample_rate": 32000,
      "bitrate": 128000,
      "format": "mp3",
      "channel": 1
    }
  }
}'
```

## 进阶功能

### 指令控制

指令控制通过自然语言描述控制语音的音调、语速、情感和音色特点，无需调整复杂的音频参数。

**各模型指令规格**：

**说明**指令参数名因模型系列而异：CosyVoice 使用 `instruction`，Qwen-TTS 使用 `instructions`。跨模型迁移时请注意修改参数名。

#### Qwen-Audio-TTS

**支持的模型**：`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`

系统音色和声音复刻音色：均可输入任意指令。

#### CosyVoice

**支持的模型**：`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`

不同模型对指令的格式要求不同：

-   `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`：
    
    -   声音复刻/设计音色：可输入任意指令。
    -   系统音色：v3.5不支持系统音色。
-   `cosyvoice-v3-plus`：
    
    -   声音复刻/设计音色：不支持指令控制。
    -   系统音色：指令必须使用固定格式和内容，参见[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。
-   `cosyvoice-v3-flash`：
    
    -   声音复刻/设计音色：可输入任意指令。
    -   系统音色：指令必须使用固定格式和内容，参见[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。

**使用方式**：通过 `instruction` 参数指定指令内容。

**指令文本支持的语言**：

-   `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`：
    
    -   声音复刻/设计音色：中文、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语。
    -   系统音色：v3.5不支持系统音色。
-   `cosyvoice-v3-plus`：
    
    -   声音复刻/设计音色：中文、英文、法语、德语、日语、韩语、俄语。
    -   系统音色：指令必须使用固定格式和内容，参见[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。
-   `cosyvoice-v3-flash`：
    
    -   声音复刻/设计音色：中文、英文、法语、德语、日语、韩语、俄语。
    -   系统音色：中文。

**指令文本长度限制**：不超过 100 字符。汉字（包括简体/繁体汉字、日文汉字和韩文汉字）按 2 个字符计算，其他字符（如标点符号、字母、数字、日韩文假名/谚文等）按 1 个字符计算。

#### Qwen-TTS

**支持的模型**：仅支持Qwen3-TTS-Instruct-Flash 系列模型。

**使用方式**：通过 `instructions` 参数传入指令内容。

**指令文本支持的语言**：仅支持中文和英文。

**指令文本长度限制**：不超过 1,600 Token。

**适用场景**：

-   有声书和广播剧配音
-   广告和宣传片配音
-   游戏角色和动画配音
-   情感化的智能语音助手
-   纪录片和新闻播报

**如何编写高质量的声音描述**：

-   **核心原则**：
    
    1.  **具体而非模糊**：使用描绘声音特质的词语，如“低沉”、“清脆”、“语速偏快”，避免“好听”、“普通”等主观或模糊的表述。
    2.  **多维而非单一**：好的描述通常涵盖多个维度（如性别、年龄、情感等）。仅写“女声”过于宽泛，难以生成有特色的音色。
    3.  **客观而非主观**：聚焦声音的物理和感知特征。例如，用”音调偏高，带有活力“代替”我最喜欢的声音”。
    4.  **原创而非模仿**：描述声音的特质，而非要求模仿特定人物（如名人、演员）。模型不支持模仿，且可能涉及版权风险。
    5.  **简洁而非冗余**：确保每个词都有明确作用，避免重复的同义词或无意义的修饰。
-   **描述维度参考**：
    
    建议组合以下维度描述声音，维度越丰富，生成效果越精准。
    

**维度**

**描述示例**

性别

男性、女性、中性

年龄

儿童（5-12 岁）、青少年（13-18 岁）、青年（19-35 岁）、中年（36-55 岁）、老年（55 岁以上）

音调

高音、中音、低音、偏高、偏低

语速

快速、中速、缓慢、偏快、偏慢

情感

开朗、沉稳、温柔、严肃、活泼、冷静、治愈

特点

有磁性、清脆、沙哑、圆润、甜美、浑厚、有力

用途

新闻播报、广告配音、有声书、动画角色、语音助手、纪录片解说

-   **示例**：
    
    -   标准播音风格：吐字清晰精准，字正腔圆
    -   年轻活泼的女性声音，语速较快，带有明显的上扬语调，适合介绍时尚产品
    -   沉稳的中年男性，语速缓慢，音色低沉有磁性，适合朗读新闻或纪录片解说
    -   温柔知性的女性，30 岁左右，语调平和，适合有声书朗读
    -   可爱的儿童声音，大约 8 岁女孩，说话略带稚气，适合动画角色配音

### 方言

本节介绍如何让模型用**中文方言**（如河南话、四川话等）输出语音。不同模型和音色类型的设置方式不同。

#### Qwen-Audio-TTS

-   **系统音色**：在[Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)中选择以下任一种音色：
    
    -   支持方言的系统音色，无需额外设置即可输出对应方言。
    -   支持[指令控制](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#nrt_instruct_h3)且可指定方言的音色，通过指令文本指定方言。
-   **声音复刻音色**：通过[指令控制](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#nrt_instruct_h3)功能设置，例如指令文本写 `请用河南话表达`。
    
-   **声音设计音色**：暂不支持方言。
    

**具体支持哪些方言**：参见[Qwen-Audio-TTS](https://help.aliyun.com/zh/model-studio/tts-model#qat_all01)中各模型“支持的语言”。

#### CosyVoice

-   **系统音色**：在[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)中选择以下任一种音色：
    
    -   支持方言的系统音色（例如 `longshange_v3`），无需额外设置即可输出对应方言。
    -   支持[指令控制](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#nrt_instruct_h3)且可指定方言的音色（例如 `longanhuan_v3`），通过指令文本指定方言。
-   **声音复刻音色**：通过[指令控制](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#nrt_instruct_h3)功能设置，例如指令文本写 `请用河南话表达`。
    
-   **声音设计音色**：暂不支持方言。
    

**具体支持哪些方言**：参见[CosyVoice](https://help.aliyun.com/zh/model-studio/tts-model#tts08_cosy02)中各模型“支持的语言”。

**示例**：以 `cosyvoice-v3-flash` + `longanhuan_v3` 音色，通过指令文本 `"请用河南话表达。"` 输出河南话语音。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "cosyvoice-v3-flash",
    "input": {
      "text": "叫你去买盐，你买回来一袋面，这不是弄啥嘞吗！",
      "voice": "longanhuan_v3",
      "format": "wav",
      "sample_rate": 24000,
      "instruction": "请用河南话表达。"
    }
}'
```

**说明**此处指令参数名 `instruction` 为 CosyVoice 专用；Qwen-TTS 的指令参数名为 `instructions`，请勿混用。

#### Qwen-TTS

-   **系统音色**：使用支持方言的系统音色，参见[Qwen-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-tts-voice-list.md)。
-   **声音复刻音色**：不支持方言。
-   **声音设计音色**：不支持方言。

**具体支持哪些方言**：参见[Qwen3-TTS](https://help.aliyun.com/zh/model-studio/tts-model#tts08_q3tts02)中各模型“支持的语言”。

### 情感与富语言标签

Qwen-Audio-TTS 系列模型支持在待合成文本（`text` 参数）中直接嵌入情感与富语言标签，用于控制语音的情感表达或在指定位置插入拟声效果（如笑声、叹息等），无需调整复杂的音频参数即可生成更具表现力的语音。

**重要****支持的模型**：仅 `qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus` 和 `qwen-audio-3.0-tts-flash`。

**控制类标签**

控制类标签用于设定语音的情感或风格。将标签写在文本中，标签会作用于其后的所有文本，直到遇到下一个控制类标签，或因句子较长被自动切分为止。

**标签**

**说明**

`[sad]`

悲伤

`[amazed]`

惊叹

`[deep and loud shouting]`

深沉大声呐喊

`[trembling]`

颤抖

`[angry]`

愤怒

`[excited]`

兴奋

`[sarcastic]`

讽刺

`[curious]`

好奇

`[like dracula]`

德古拉风格（低沉、阴森）

`[bored]`

无聊

`[tired]`

疲惫

`[scornful]`

轻蔑

`[shouting]`

大喊

`[asmr]`

ASMR 轻柔耳语

`[panicked]`

恐慌

`[mischievously]`

调皮

`[empathetic]`

共情

`[whispers]`

耳语

`[reluctantly]`

不情愿

`[crying]`

哭泣

`[serious]`

严肃

`[very slowly]`

非常缓慢地说话

`[very fast]`

非常快速地说话

**富语言类标签**

富语言类标签用于在文本的当前位置插入一段拟声效果，不影响前后文本的情感风格。

**标签**

**说明**

`[gasp]`

倒吸一口气

`[sighing]`

叹息

`[clears throat]`

清嗓

`[giggles]`

咯咯笑

`[laughing]`

大笑

`[cough]`

咳嗽

`[snorts]`

哼声、嗤笑

**使用示例**

以下示例展示如何在 `text` 参数中组合使用控制类标签和富语言类标签：

`[excited]今天的天气真不错！[laughing]我们一起出去玩吧！`

上述文本中，`[excited]` 是控制类标签，作用于其后的所有文本，使语音带有兴奋的情感；`[laughing]` 是富语言类标签，在该位置插入一段笑声效果后继续合成后续文本。

您也可以在同一段文本中切换不同情感：

`[serious]请注意安全事项。[excited]好了，现在让我们开始吧！`

其中 `[serious]` 控制第一句为严肃语气，`[excited]` 从第二句起切换为兴奋语气。

## 支持的模型与地域

#### 华北2（北京）

调用以下模型时，请选择北京地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-Audio-TTS**：qwen-audio-3.0-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-flash
    
-   **CosyVoice**：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash、cosyvoice-v2
    
-   **Qwen-TTS**：
    
    -   **Qwen3-TTS-Instruct-Flash**：qwen3-tts-instruct-flash（稳定版，当前等同 qwen3-tts-instruct-flash-2026-01-26）、qwen3-tts-instruct-flash-2026-01-26（最新快照版）
    -   **Qwen3-TTS-VD：**qwen3-tts-vd-2026-01-26（最新快照版）
    -   **Qwen3-TTS-VC：**qwen3-tts-vc-2026-01-22（最新快照版）
    -   **Qwen3-TTS-Flash**：qwen3-tts-flash（稳定版，当前等同 qwen3-tts-flash-2025-11-27）、qwen3-tts-flash-2025-11-27、qwen3-tts-flash-2025-09-18
    -   **Qwen-TTS**：qwen-tts（稳定版，当前等同 qwen-tts-2025-04-10）、qwen-tts-latest（最新版，当前等同 qwen-tts-2025-05-22）、qwen-tts-2025-05-22（快照版）、qwen-tts-2025-04-10（快照版）
-   **MiniMax**：MiniMax/speech-2.8-hd、MiniMax/speech-02-hd、MiniMax/speech-2.8-turbo、MiniMax/speech-02-turbo
    

#### 新加坡

调用以下模型时，请选择新加坡地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-TTS**：
    
    -   **Qwen3-TTS-Instruct-Flash**：qwen3-tts-instruct-flash（稳定版，当前等同 qwen3-tts-instruct-flash-2026-01-26）、qwen3-tts-instruct-flash-2026-01-26（最新快照版）
    -   **Qwen3-TTS-VD：**qwen3-tts-vd-2026-01-26（最新快照版）
    -   **Qwen3-TTS-VC：**qwen3-tts-vc-2026-01-22（最新快照版）
    -   **Qwen3-TTS-Flash**：qwen3-tts-flash（稳定版，当前等同 qwen3-tts-flash-2025-11-27）、qwen3-tts-flash-2025-11-27、qwen3-tts-flash-2025-09-18

## 支持的系统音色

不同模型支持的音色不同。将请求参数 `voice` 设为下表中 **voice 参数**列的值即可。

-   [Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)
-   [CosyVoice音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)
-   [Qwen-TTS音色列表](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-list#261bc7f209ri2)

## API 参考

-   [非实时语音合成-Qwen-Audio-TTS API参考](raw/_short/non-realtime-qwen-audio-tts-api-0b292236e8ca1637.md) / [非实时语音合成-CosyVoice API参考](raw/_short/non-realtime-cosyvoice-api-685311b646d9ca3f.md)
-   [非实时语音合成-千问API参考](raw/_short/qwen-tts-api-88cc336b17a3a583.md)
-   [非实时语音合成-MiniMax API参考](raw/_short/minimax-speech-synthesis-36f3b02a593324ef.md)

## 常见问题

### Q：音频文件链接的有效期是多久？

A：音频文件链接在生成后 24 小时内有效。链接过期后，重新调用接口即可获取新链接。
