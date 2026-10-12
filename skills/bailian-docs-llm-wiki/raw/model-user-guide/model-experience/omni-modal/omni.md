# 全模态概述

选择适合多模态理解、音视频分析、语音对话、内容审核、语音翻译等全模态场景的模型。

## 从闭源模型迁移到百炼?

如果你正在使用 GPT 或 Gemini 的全模态/实时能力，可参考下表选择百炼对位模型。

**闭源模型代表**

**百炼推荐**

音视频理解与文本生成

[Gemini 3.8 Flash](https://ai.google.dev/gemini-api/docs/audio)

[qwen3.8-omni-flash](raw/model-user-guide/support/model-studio-model-list/model-list-omni/qwen3-8-omni-flash.md)

实时翻译

[Gemini 3.5 Live Translate（Preview）](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-live-translate-preview)

`qwen3.8-livetranslate-flash-realtime`

## 使用场景

全模态模型支持文本、音频、图片和视频理解。Qwen3.8-Omni-Flash 适用于音视频内容分析、会议纪要和字幕生成，支持思考模式、工具调用和联网搜索。根据您的场景选择合适的模型：

**场景**

**推荐模型**

**用户指南**

**音视频理解与文本生成**：分析音视频内容，生成会议纪要、字幕和文本答复

Qwen3.8-Omni-Flash

[Qwen3.8-Omni-Flash 调用指南](https://help.aliyun.com/zh/model-studio/qwen-omni#qwen38-offline)

**实时语音/视频对话**：通过麦克风和摄像头与AI实时交互（语音助手、智能客服、视觉问答、直播分析）

Qwen3.8-Omni-Flash-Realtime

[实时（Qwen-Omni-Realtime）](raw/model-user-guide/model-experience/omni-modal/realtime.md)

**实时语音对话（语义 VAD）**：端到端语音交互，支持语义轮次检测（smart\_turn），无意义附和声不会打断，支持 Function Calling（语音助手、智能客服）

Qwen-Audio

[实时语音对话（Qwen-Audio-Realtime）](https://help.aliyun.com/zh/model-studio/qwen-audio-realtime-user-guides)

**离线音频输出**：上传音频或视频文件，生成语音回复

Qwen3.5-Omni

[非实时（Qwen-Omni）](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)

**实时语音翻译**：语音同传，时延低至2.3秒，支持60种语言（同声传译、多语言会议）

Qwen3.8-LiveTranslate-Flash-Realtime

[实时语音/音视频翻译-千问](raw/model-user-guide/model-experience/speech-to-speech/qwen3-5-livetranslate-flash-realtime.md)

**音视频文件翻译**：上传音频/视频文件翻译为目标语言（视频配音、播客翻译）

Qwen3-Livetranslate

[音视频文件翻译-千问](raw/model-user-guide/model-experience/speech-to-speech/qwen3-livetranslate-flash.md)

**声音复刻**：提供参考音频，AI用该音色生成语音回复

Qwen3.8-Omni-Flash-Realtime；Qwen3.5-Omni Plus / Flash

[声音复刻](raw/_short/qwen-omni-voice-cloning-717550bc449e9e29.md)

-   使用 Qwen3.8-Omni-Flash 进行内容分析时，支持音频最长3小时、视频最长2小时。
-   支持工具调用（Function Calling）：Qwen3.8-Omni-Flash-Realtime、Qwen3.8-Omni-Flash、Qwen3.5-Omni Plus / Flash（文本输出）、Qwen3.5-Omni-Realtime、Qwen3-Omni-Flash、Qwen-Audio Realtime。
-   支持联网搜索：Qwen3.8-Omni-Flash-Realtime、Qwen3.8-Omni-Flash、Qwen3.5-Omni、Qwen-Audio Realtime。

## 翻译

音视频翻译为文本或字幕时，推荐使用 [Qwen3.8-Omni-Flash](https://help.aliyun.com/zh/model-studio/qwen-omni#qwen38-offline)。需要输出翻译后的语音时，可按下方说明选择适合时延和语音输出需求的模型。

**说明**快速搭建翻译应用推荐 `qwen3.8-livetranslate-flash-realtime`（60种语言，同传时延低至2.3秒，开箱即用）；需要语音输出、联网搜索和术语注入时，实时对话可选择 Qwen3.8-Omni-Flash-Realtime，文件调用可选择 Qwen3.5-Omni。Qwen3.8-Omni-Flash-Realtime 的语音生成语种与 Qwen3.5-Omni-Realtime 一致，各音色支持范围见[音色列表](https://help.aliyun.com/zh/model-studio/omni-voice-list#qwen38-voices)。

支持的语言

**语言**

[Qwen3.8 / 3.5-Livetranslate](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#4ffd192226f0s)

**Qwen3-Livetranslate**

[Qwen3.8-Omni-Flash-Realtime](https://help.aliyun.com/zh/model-studio/omni-voice-list#qwen38-voices)（语音）

**Qwen3.5-Omni（语音）**

**Qwen3-Omni-Flash（语音）**

英语

支持

支持

支持

支持

支持

中文（普通话）

支持

支持

支持

支持

支持

粤语

仅文本

支持

支持

支持

支持

四川话

支持

支持

支持

支持

支持

上海话

支持

支持

不支持

不支持

支持

北京话

支持

支持

支持

支持

支持

天津话

支持

支持

支持

支持

支持

南京话

不支持

不支持

支持

支持

支持

陕西话

不支持

不支持

支持

支持

支持

闽南语

不支持

不支持

支持

支持

支持

法语

支持

支持

支持

支持

支持

德语

支持

支持

支持

支持

支持

俄语

支持

支持

支持

支持

支持

意大利语

支持

支持

支持

支持

支持

西班牙语

支持

支持

支持

支持

支持

葡萄牙语

支持

支持

支持

支持

支持

日语

支持

支持

支持

支持

支持

韩语

支持

支持

支持

支持

支持

泰语

支持

支持 仅文本

支持

支持

支持

印尼语

支持

支持 仅文本

支持

支持

不支持

越南语

支持

支持 仅文本

支持

支持

不支持

阿拉伯语

支持

支持 仅文本

支持

支持

不支持

印地语

支持

支持 仅文本

支持

支持

不支持

土耳其语

支持

支持 仅文本

支持

支持

不支持

芬兰语

支持

不支持

支持

支持

不支持

波兰语

支持

不支持

支持

支持

不支持

荷兰语

支持

不支持

支持

支持

不支持

捷克语

支持

不支持

支持

支持

不支持

乌尔都语

支持

不支持

支持

支持

不支持

他加禄语

支持

不支持

支持

支持

不支持

瑞典语

支持

不支持

支持

支持

不支持

丹麦语

支持

不支持

支持

支持

不支持

希伯来语

支持

不支持

支持

支持

不支持

冰岛语

支持

不支持

支持

支持

不支持

马来语

支持

不支持

支持

支持

不支持

挪威语

支持

不支持

支持

支持

不支持

波斯语

支持

不支持

支持

支持

不支持

希腊语

仅文本

支持 仅文本

不支持

不支持

不支持

南非荷兰语

仅文本

不支持

不支持

不支持

不支持

阿斯图里亚斯语

仅文本

不支持

不支持

不支持

不支持

白俄罗斯语

仅文本

不支持

不支持

不支持

不支持

保加利亚语

仅文本

不支持

不支持

不支持

不支持

孟加拉语

仅文本

不支持

不支持

不支持

不支持

波斯尼亚语

仅文本

不支持

不支持

不支持

不支持

加泰罗尼亚语

仅文本

不支持

不支持

不支持

不支持

宿务语

仅文本

不支持

不支持

不支持

不支持

爱沙尼亚语

仅文本

不支持

不支持

不支持

不支持

加利西亚语

仅文本

不支持

不支持

不支持

不支持

古吉拉特语

仅文本

不支持

不支持

不支持

不支持

克罗地亚语

仅文本

不支持

不支持

不支持

不支持

匈牙利语

仅文本

不支持

不支持

不支持

不支持

爪哇语

仅文本

不支持

不支持

不支持

不支持

哈萨克语

仅文本

不支持

不支持

不支持

不支持

卡纳达语

仅文本

不支持

不支持

不支持

不支持

柯尔克孜语

仅文本

不支持

不支持

不支持

不支持

拉脱维亚语

仅文本

不支持

不支持

不支持

不支持

马其顿语

仅文本

不支持

不支持

不支持

不支持

马拉雅拉姆语

仅文本

不支持

不支持

不支持

不支持

马拉地语

仅文本

不支持

不支持

不支持

不支持

旁遮普语

仅文本

不支持

不支持

不支持

不支持

罗马尼亚语

仅文本

不支持

不支持

不支持

不支持

斯洛伐克语

仅文本

不支持

不支持

不支持

不支持

斯洛文尼亚语

仅文本

不支持

不支持

不支持

不支持

斯瓦希里语

仅文本

不支持

不支持

不支持

不支持

塔吉克语

仅文本

不支持

不支持

不支持

不支持

阿塞拜疆语

仅文本

不支持

不支持

不支持

不支持

乌克兰语

仅文本

不支持

不支持

不支持

不支持

“支持”表示同时输出语音和文本。“仅文本”表示该语言不输出语音。Qwen3.8-LiveTranslate-Flash-Realtime 列中的“—”表示语种代码清单未单列该方言。

Qwen3.8-Omni-Flash、Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni 均支持113种输入语言/方言，完整输入语种列表见[模型选型](https://help.aliyun.com/zh/model-studio/qwen-omni#d54e85c641oux)。

Qwen3.8 / 3.5-Livetranslate 支持60种语言（29种音频+文本，31种仅文本）。

## 推荐模型

模型

API

适用场景

qwen3.8-omni-flash

Chat Completions / Responses

音视频理解、文本生成、思考、Function Calling、联网搜索

qwen3.8-omni-flash-realtime

Realtime API（WebSocket / WebRTC / AOQ）

实时音视频对话、Function Calling、MCP、声音复刻

qwen3.5-omni-plus / qwen3.5-omni-flash

Chat Completions

离线语音输出、声音复刻

qwen3.8-livetranslate-flash-realtime

Realtime API（WebSocket）

实时翻译

qwen3-livetranslate-flash

Chat Completions

音视频文件翻译

qwen-audio-3.1-realtime-plus / qwen-audio-3.0-realtime-plus / qwen-audio-3.0-realtime-flash

Realtime API（WebSocket）

实时语音对话

## 所有模型

### Qwen3.8-Omni

`qwen3.8-omni-flash` 适用于音视频理解和内容分析，思考模式默认开启；`qwen3.8-omni-flash-realtime` 适用于实时音视频对话。

模型ID

API

输入

输出

Function Calling

联网搜索

[qwen3.8-omni-flash](raw/model-user-guide/support/model-studio-model-list/model-list-omni/qwen3-8-omni-flash.md)

Chat Completions / Responses

文本、音频、图片、视频

仅文本

支持

支持

[qwen3.8-omni-flash-realtime](raw/model-user-guide/support/model-studio-model-list/model-list-omni/qwen3-8-omni-flash-realtime.md)

Realtime API

文本、音频、图片、视频

文本、音频

支持

支持

离线模型支持 1M Token 上下文、多通道空间音频、隐式缓存和 Responses Session 缓存，参见[调用说明](https://help.aliyun.com/zh/model-studio/qwen-omni#qwen38-offline)。实时模型还支持 MCP、多通道音频和声音复刻，参见[实时调用指南](raw/model-user-guide/model-experience/omni-modal/realtime.md)。

### Qwen3.5-Omni

非实时 Qwen3.5-Omni 支持音频最长3小时、视频最长1小时。

**模型ID**

**API**

**输入**

**Function Calling**

**联网搜索**

**思考模式**

`qwen3.5-omni-plus-realtime`

Realtime API（WebSocket）

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-plus-realtime-2026-03-15`

Realtime API（WebSocket）

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-plus`

Chat Completions

文本、音频、图片、视频

支持（北京，文本输出）

支持

不支持

`qwen3.5-omni-plus-2026-03-15`

Chat Completions

文本、音频、图片、视频

支持（北京，文本输出）

支持

不支持

`qwen3.5-omni-flash-realtime`

Realtime API（WebSocket）

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-flash-realtime-2026-03-15`

Realtime API（WebSocket）

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-flash`

Chat Completions

文本、音频、图片、视频

支持（北京，文本输出）

支持

不支持

`qwen3.5-omni-flash-2026-03-15`

Chat Completions

文本、音频、图片、视频

支持（北京，文本输出）

支持

不支持

### Qwen3-Omni

**模型ID**

**API**

**输入**

**Function Calling**

**联网搜索**

**思考模式**

`qwen3-omni-flash-realtime-2025-09-15`

Realtime API（WebSocket）

文本、音频、图片、视频

不支持

不支持

不支持

`qwen3-omni-flash`

Chat Completions

文本、音频、图片、视频

支持

不支持

支持

### Qwen3.8-Livetranslate

模型ID

API

输入

语言数

[qwen3.8-livetranslate-flash-realtime](raw/model-user-guide/support/model-studio-model-list/model-list-speech-to-speech/qwen3-8-livetranslate-flash-realtime.md)

[Realtime API](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)

音频、图片

60

### Qwen3.5-Livetranslate

**模型ID**

**API**

**输入**

**语言数**

`qwen3.5-livetranslate-flash-realtime`

Realtime API（WebSocket）

音频、图片

60

`qwen3.5-livetranslate-flash-realtime-2026-05-19`

Realtime API（WebSocket）

音频、图片

60

`qwen3.5-livetranslate-flash`

Chat Completions

音频、视频

60

### Qwen3-Livetranslate

**模型ID**

**API**

**输入**

**语言数**

`qwen3-livetranslate-flash`

Chat Completions

音频、视频

18

`qwen3-livetranslate-flash-2025-12-01`

Chat Completions

音频、视频

18

### Qwen-Audio

**模型ID**

**API**

**输入**

**Function Calling**

**联网搜索**

**思考模式**

`qwen-audio-3.1-realtime-plus`

Realtime API（WebSocket）

音频、文本

支持

支持

不支持

`qwen-audio-3.0-realtime-plus`

Realtime API（WebSocket）

音频、文本

支持

支持

不支持

`qwen-audio-3.0-realtime-flash`

Realtime API（WebSocket）

音频、文本

支持

支持

不支持
