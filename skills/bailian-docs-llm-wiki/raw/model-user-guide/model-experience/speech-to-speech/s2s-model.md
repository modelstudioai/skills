# 语音转语音概述

为“语音输入 → 语音输出”场景（语音对话、语音翻译、同声传译等）选择模型。

## 从闭源模型迁移到百炼?

如果你正在使用 OpenAI Realtime 或 Gemini Live，可参考下表选择百炼对位模型。

**闭源模型代表**

**百炼推荐**

高能力实时对话

OpenAI GPT Realtime、Gemini 3.1 Live

`qwen-audio-3.1-realtime-plus`

成本敏感对话

OpenAI gpt-4o-mini Realtime

`qwen-audio-3.0-realtime-flash`

实时翻译 / 同传

Gemini 3.1 Live

`qwen3.8-livetranslate-flash-realtime`

**说明**本文档面向“语音 → 语音”场景。视觉理解、音视频分析和内容审核等能力见[全模态](raw/model-user-guide/model-experience/omni-modal/omni.md)；其中视频分析、内容标注等需要推理并输出文本的场景，可参考 [Qwen3.8-Omni-Flash](https://help.aliyun.com/zh/model-studio/qwen-omni#qwen38-offline)。

## S2S（Speech-to-Speech）与Pipeline对比

构建语音应用有两种方式：

**S2S**

**Pipeline（ASR + LLM + TTS）**

延迟

低 -- 单模型流式处理

较高 -- 3个阶段串行处理

音频理解

端到端 -- 能感知语调、情绪并做出相应回应

先转文本再处理 -- 音频中的细微信息丢失

音色定制

通过系统提示词选择预设音色

声音克隆、声音设计（CosyVoice）

-   **使用S2S**：当交互式对话、低延迟和音频感知的回复是关键需求时。
-   **使用Pipeline**：当需要自定义音色，或者需要为每个阶段分别选择最优的ASR、LLM和TTS模型时。

本文档继续介绍 S2S 单模型路线（Omni、Livetranslate）。如选择 Pipeline 路线，分别在以下文档中挑选三个组件：

-   **ASR（语音识别）**：[语音识别](raw/model-user-guide/model-experience/speech-recognition/asr-model.md)
-   **LLM（大语言模型）**：[文本生成](raw/model-user-guide/model-experience/text-generation-model.md)
-   **TTS（语音合成）**：[语音合成](raw/model-user-guide/model-experience/speech-synthesis/tts-model.md)

## 实时还是文件模式？

-   **实时（WebSocket）**：适用于语音助手、呼叫中心、同声传译等实时语音交互场景。音频流式输入，语音流式输出。
-   **文件模式（HTTP）**：可以用延迟换取更好的效果，适用于视频配音、播客翻译、离线内容处理等场景。文件模式下还支持 Function Calling、联网搜索、思考模式、视频上下文等附带能力（详见下方“S2S 单模型的附带能力”）。

## 按场景选模型（S2S 单模型路线）

以下场景均针对 S2S 单模型路线。Pipeline 路线请按上述链接分别在 ASR / LLM / TTS 文档中选型。

**场景**

**推荐模型**

**API**

实时音视频对话

[qwen3.8-omni-flash-realtime](raw/model-user-guide/support/model-studio-model-list/model-list-omni/qwen3-8-omni-flash-realtime.md)

WebSocket / WebRTC / AOQ

语音助手 / 客服对话

`qwen-audio-3.1-realtime-plus`

WebSocket

成本敏感的对话

`qwen-audio-3.0-realtime-flash`

WebSocket

同声传译 / 直播翻译

`qwen3.8-livetranslate-flash-realtime`

WebSocket

视频配音 / 播客翻译

`qwen3-livetranslate-flash`

Chat Completions

语义 VAD 语音助手 / 智能客服（支持 Function Calling）

`qwen-audio-3.1-realtime-plus`

WebSocket

## S2S 单模型的附带能力

以下介绍语音交互中的工具调用、联网搜索及文本推理能力。

### Function Calling

根据音视频内容查询知识库、查询日程或触发工作流，可使用 Qwen3.8-Omni-Flash-Realtime（WebSocket / WebRTC / AOQ）、Qwen-Audio Realtime（WebSocket）。

### 联网搜索

需要检索实时信息并生成语音回复时，实时对话可使用 Qwen3.8-Omni-Flash-Realtime 或 Qwen3.5-Omni-Realtime；文件调用可使用 Qwen3.5-Omni（Chat Completions，Plus 和 Flash 系列）。模型自主决定是否搜索。Qwen-Audio Realtime 3.0 Plus/Flash 和 3.1 Plus 也支持联网搜索，通过 `enable_search` 开启，不能与 Function Calling 同时启用。

**说明**Qwen3-Omni-Flash 和 Livetranslate 模型不支持此功能。

### 思考模式

**说明**Qwen3-Omni-Flash 在思考模式下不支持生成语音。

## 翻译

以下模型系列均支持语音翻译：

-   **Qwen3.8-Livetranslate**：支持 60 种源语言和 29 种语言的语音输出，支持音频与图像输入。详见[模型信息](raw/model-user-guide/support/model-studio-model-list/model-list-speech-to-speech/qwen3-8-livetranslate-flash-realtime.md)。
-   **Qwen3.5-Livetranslate**：支持 60 种语言互译，其中 29 种支持音频+文本输出、31 种仅支持文本输出，覆盖中文、英语、法语、德语、俄语、日语、韩语、西班牙语、葡萄牙语、阿拉伯语等主流语种。
-   **Qwen3-Livetranslate**：支持18种语言 + 5种中文方言，约3秒延迟，开箱即用。文件模式支持输入视频以获得上下文感知的翻译精度。其中7种语言仅输出文本（不输出语音）。
-   **Qwen3.8-Omni-Flash-Realtime**：支持实时语音翻译，语音生成语种与 Qwen3.5-Omni-Realtime 一致，支持36种语种和方言，各音色支持范围见[音色列表](https://help.aliyun.com/zh/model-studio/omni-voice-list#qwen38-voices)。
-   **Qwen3.5-Omni**：支持29种输出语言 + 7种中文方言。优秀的音视频理解能力和联网搜索。可通过系统提示词注入术语和领域上下文。支持实时和文件模式。
-   **Qwen3-Omni-Flash**：支持11种输出语言 + 8种中文方言。可通过系统提示词注入术语和领域上下文。支持实时和文件模式。

**说明**快速搭建翻译应用可选择 Livetranslate；需要离线语音输出、联网搜索和术语注入时，可选择 Qwen3.5-Omni。

支持的语言

**语言**

**Qwen3.5-Livetranslate**

**Qwen3-Livetranslate**

**Qwen3.5-Omni**

**Qwen3-Omni-Flash**

英语

支持

支持

支持

支持

中文（普通话）

支持

支持

支持

支持

粤语

仅文本

支持

支持

支持

四川话

支持

支持

支持

支持

上海话

支持

支持

支持

支持

北京话

支持

支持

支持

支持

天津话

支持

支持

支持

支持

南京话

\--

\--

支持

支持

陕西话

\--

\--

支持

支持

闽南语

\--

\--

支持

支持

法语

支持

支持

支持

支持

德语

支持

支持

支持

支持

俄语

支持

支持

支持

支持

意大利语

支持

支持

支持

支持

西班牙语

支持

支持

支持

支持

葡萄牙语

支持

支持

支持

支持

日语

支持

支持

支持

支持

韩语

支持

支持

支持

支持

泰语

支持

仅文本

支持

支持

印尼语

支持

仅文本

支持

\--

越南语

支持

仅文本

支持

\--

阿拉伯语

支持

仅文本

支持

\--

印地语

支持

仅文本

支持

\--

土耳其语

支持

仅文本

支持

\--

芬兰语

支持

\--

支持

\--

波兰语

支持

\--

支持

\--

荷兰语

支持

\--

支持

\--

捷克语

支持

\--

支持

\--

乌尔都语

支持

\--

支持

\--

他加禄语

支持

\--

支持

\--

瑞典语

支持

\--

支持

\--

丹麦语

支持

\--

支持

\--

希伯来语

支持

\--

支持

\--

冰岛语

支持

\--

支持

\--

马来语

支持

\--

支持

\--

挪威语

支持

\--

支持

\--

波斯语

支持

\--

支持

\--

希腊语

仅文本

仅文本

\--

\--

南非荷兰语

仅文本

\--

\--

\--

阿斯图里亚斯语

仅文本

\--

\--

\--

白俄罗斯语

仅文本

\--

\--

\--

保加利亚语

仅文本

\--

\--

\--

孟加拉语

仅文本

\--

\--

\--

波斯尼亚语

仅文本

\--

\--

\--

加泰罗尼亚语

仅文本

\--

\--

\--

宿务语

仅文本

\--

\--

\--

爱沙尼亚语

仅文本

\--

\--

\--

加利西亚语

仅文本

\--

\--

\--

古吉拉特语

仅文本

\--

\--

\--

克罗地亚语

仅文本

\--

\--

\--

匈牙利语

仅文本

\--

\--

\--

爪哇语

仅文本

\--

\--

\--

哈萨克语

仅文本

\--

\--

\--

卡纳达语

仅文本

\--

\--

\--

柯尔克孜语

仅文本

\--

\--

\--

拉脱维亚语

仅文本

\--

\--

\--

马其顿语

仅文本

\--

\--

\--

马拉雅拉姆语

仅文本

\--

\--

\--

马拉地语

仅文本

\--

\--

\--

旁遮普语

仅文本

\--

\--

\--

罗马尼亚语

仅文本

\--

\--

\--

斯洛伐克语

仅文本

\--

\--

\--

斯洛文尼亚语

仅文本

\--

\--

\--

斯瓦希里语

仅文本

\--

\--

\--

塔吉克语

仅文本

\--

\--

\--

阿塞拜疆语

仅文本

\--

\--

\--

乌克兰语

仅文本

\--

\--

\--

"支持"表示同时输出语音和文本。"仅文本"表示该语言不输出语音。

Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni 均支持113种输入语言/方言。

Qwen3.5-Livetranslate支持60种语言（29种音频+文本，31种仅文本）。

旧版`qwen-omni-turbo`仅支持中文和英文。

## 推荐模型

下表列出每个系列的常用入口模型。如需锁定特定日期版本（用于版本回归或稳定性需求），请见下方“所有模型”。

模型

API

适用场景

qwen3.8-omni-flash-realtime

WebSocket / WebRTC / AOQ

实时音视频对话

qwen-audio-3.1-realtime-plus / qwen-audio-3.0-realtime-flash

WebSocket

实时语音对话

qwen3.5-omni-plus / qwen3.5-omni-flash

Chat Completions

离线语音输出

qwen3.8-livetranslate-flash-realtime

WebSocket

实时翻译

qwen3-livetranslate-flash

Chat Completions

音视频文件翻译

## 所有模型

### Qwen-Audio

**模型**

**API**

**输入**

**Function Calling**

**联网搜索**

**思考模式**

**翻译**

`qwen-audio-3.1-realtime-plus`

WebSocket

音频、文本

支持

支持

\--

\--

`qwen-audio-3.0-realtime-plus`

WebSocket

音频、文本

支持

支持

\--

\--

`qwen-audio-3.0-realtime-flash`

WebSocket

音频、文本

支持

支持

\--

\--

### Qwen3.8-Omni

**模型**

**API**

**输入**

**Function Calling**

**联网搜索**

**思考模式**

`qwen3.8-omni-flash-realtime`

WebSocket / WebRTC / AOQ

文本、音频、图片、视频

支持

支持

\--

多通道音频、文本与音频输出及 MCP 用法见[实时调用指南](raw/model-user-guide/model-experience/omni-modal/realtime.md)。

### Qwen3.5-Omni

**模型**

**API**

**输入**

**Function Calling**

**联网搜索**

**思考模式**

`qwen3.5-omni-plus-realtime`

WebSocket

文本、音频、图片、视频

支持

支持

\--

`qwen3.5-omni-plus-realtime-2026-03-15`

WebSocket

文本、音频、图片、视频

支持

支持

\--

`qwen3.5-omni-plus`

Chat Completions

文本、音频、图片、视频

支持（北京，文本输出）

支持

\--

`qwen3.5-omni-plus-2026-03-15`

Chat Completions

文本、音频、图片、视频

支持（北京，文本输出）

支持

\--

`qwen3.5-omni-flash-realtime`

WebSocket

文本、音频、图片、视频

支持

支持

\--

`qwen3.5-omni-flash-realtime-2026-03-15`

WebSocket

文本、音频、图片、视频

支持

支持

\--

`qwen3.5-omni-flash`

Chat Completions

文本、音频、图片、视频

支持（北京，文本输出）

支持

\--

`qwen3.5-omni-flash-2026-03-15`

Chat Completions

文本、音频、图片、视频

支持（北京，文本输出）

支持

\--

### Qwen3-Omni

**模型**

**API**

**输入**

**Function Calling**

**联网搜索**

**思考模式**

`qwen3-omni-flash-realtime`

WebSocket

文本、音频、图片、视频

\--

\--

\--

`qwen3-omni-flash-realtime-2025-12-01`

WebSocket

文本、音频、图片、视频

\--

\--

\--

`qwen3-omni-flash-realtime-2025-09-15`

WebSocket

文本、音频、图片、视频

\--

\--

\--

`qwen3-omni-flash`

Chat Completions

文本、音频、图片、视频

支持

\--

支持

`qwen3-omni-flash-2025-12-01`

Chat Completions

文本、音频、图片、视频

支持

\--

支持

`qwen3-omni-flash-2025-09-15`

Chat Completions

文本、音频、图片、视频

支持

\--

支持

### Qwen3.8-Livetranslate

**模型**

**API**

**输入**

**语言数**

[qwen3.8-livetranslate-flash-realtime](raw/model-user-guide/support/model-studio-model-list/model-list-speech-to-speech/qwen3-8-livetranslate-flash-realtime.md)

WebSocket

音频、图片

60

### Qwen3.5-Livetranslate

**模型**

**API**

**输入**

**语言数**

`qwen3.5-livetranslate-flash-realtime`

WebSocket

音频、图片

60

`qwen3.5-livetranslate-flash-realtime-2026-05-19`

WebSocket

音频

60

### Qwen3-Livetranslate

**模型**

**API**

**输入**

**语言数**

`qwen3-livetranslate-flash-realtime`

WebSocket

音频

18

`qwen3-livetranslate-flash-realtime-2025-09-22`

WebSocket

音频

18

`qwen3-livetranslate-flash`

Chat Completions

音频、视频

18

`qwen3-livetranslate-flash-2025-12-01`

Chat Completions

音频、视频

18

### 旧版模型

以下模型不再更新，新项目的实时音视频对话推荐 Qwen3.8-Omni-Flash-Realtime；离线语音输出可选择 Qwen3.5-Omni。

**模型**

**输入**

**API**

`qwen2.5-omni-7b`

文本、音频、图片、视频

HTTP

`qwen-omni-turbo`

文本、音频、图片、视频

HTTP

`qwen-omni-turbo-latest`

文本、音频、图片、视频

HTTP

`qwen-omni-turbo-2025-03-26`

文本、音频、图片、视频

HTTP

`qwen-omni-turbo-realtime`

文本、音频

WebSocket

`qwen-omni-turbo-realtime-latest`

文本、音频

WebSocket

`qwen-omni-turbo-realtime-2025-05-08`

文本、音频

WebSocket

## 下一步

选定模型后，参考对应的调用文档：

-   Qwen-Audio Realtime（WebSocket，实时语音对话）→ [实时语音对话（Qwen-Audio-Realtime）](https://help.aliyun.com/zh/model-studio/qwen-audio-realtime-user-guides)
-   Qwen3.8-Omni-Flash-Realtime（WebSocket / WebRTC / AOQ，实时）→ [实时（Qwen-Omni-Realtime）](raw/model-user-guide/model-experience/omni-modal/realtime.md)
-   Qwen3.5-Omni（HTTP，离线语音输出）→ [非实时（Qwen-Omni）](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)
-   Qwen3.8-Livetranslate / Qwen3.5-Livetranslate（实时）→ [实时语音/音视频翻译-千问](raw/model-user-guide/model-experience/speech-to-speech/qwen3-5-livetranslate-flash-realtime.md)
-   Qwen3-Livetranslate（HTTP，文件）→ [音视频文件翻译-千问](raw/model-user-guide/model-experience/speech-to-speech/qwen3-livetranslate-flash.md)
