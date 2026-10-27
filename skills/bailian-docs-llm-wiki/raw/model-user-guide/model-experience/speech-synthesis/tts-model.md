# 语音合成概述

百炼语音合成可将文本转换为语音，支持系统音色，也可通过声音复刻、声音设计创建自定义音色，并可控制语速、情感、发音等合成效果。

## 模型选型

实时交互、内容制作和精细朗读控制对模型能力的要求不同，可根据以下需求选择模型。

**使用需求**

**推荐模型**

**选择说明**

语音助手、实时对话、智能客服

[`qwen-audio-3.1-tts-flash`](raw/model-user-guide/support/model-studio-model-list/model-list-speech-synthesis/qwen-audio-3-1-tts-flash.md)

面向低延迟交互场景，支持系统音色、声音复刻、声音设计、自然语言指令及情感与富语言标签。

有声书、影视配音、品牌声音与内容制作

[`qwen-audio-3.1-tts-plus`](raw/model-user-guide/support/model-studio-model-list/model-list-speech-synthesis/qwen-audio-3-1-tts-plus.md)

侧重音质、自然度和细节表现，支持系统音色、声音复刻、声音设计及丰富的表达控制。

各系列的模型 ID 参见[支持模型](#tts_supported_models)。

## 音色选择

前往[音色试听广场](https://creative.cosyvoice.net.cn/voice-plaza)试听音色。各模型可用的系统音色、`voice` 参数和试听音频参见下表中的音色列表。

**音色来源**

**需要准备**

**适用场景**

**使用入口**

系统音色

无需音频样本或音色描述，选择已有音色即可。

智能客服、有声阅读、内容播报等已有音色能够满足的场景。

-   [Qwen-Audio-TTS 音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)
-   [CosyVoice 音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)
-   [Qwen-TTS 音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-tts-voice-list.md)

复刻音色

提供目标说话人的音频样本。

复用品牌代言人、主播等已有声音，创建个性化语音助手或虚拟主播。

[声音复刻](raw/model-user-guide/model-experience/speech-synthesis/voice-cloning-user-guide.md)

设计音色

用文字描述期望的声音，例如“温暖的低音女声”。

没有录音素材，需要为品牌、游戏或动画角色创建新音色。

[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)

声音设计用于创建可重复使用的音色。如果只需在单次合成中调整语速、情感或说话方式，可使用[指令控制](#tts_synthesis_controls)。

## 合成方式

合成方式的区别在于一次输入完整文本还是分段持续输入，以及一次获取完整音频还是边合成边获取音频。流式输出音频与流式输入文本是两种不同的能力。

**合成方式**

**文本输入**

**音频输出**

**适用场景**

非流式

一次发送完整文本。

合成完成后获取完整音频。

无需边合成边播放的内容制作。

单向流式

一次发送完整文本。

边合成边分段返回音频。

文本已准备好，希望尽早开始播放。

双向流式

持续发送文本片段。

边合成边分段返回音频。

对接大模型等文本持续产生的实时交互。

-   **非实时合成**：一次提交完整文本，可选择非流式或流式获取音频，参见[非实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/non-realtime-tts-user-guide.md)。
    
-   **实时合成**：分段或持续提交文本，也可一次提交完整文本，参见[实时语音合成](raw/model-user-guide/model-experience/speech-synthesis/realtime-tts-user-guide.md)。对于移动端等实时交互应用，可按 [Realtime API 概述](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)选择可用的接入协议。其中，AOQ（AI over QUIC）针对低延迟和弱网传输进行优化，并内置回声消除和降噪能力。
    

## 合成效果控制

除了选择音色，还可以通过参数、指令或标签调整合成效果。

**希望调整的效果**

**控制方式**

语速、音调、音量

设置模型提供的对应合成参数。

情感、风格、说话方式

使用自然语言指令，例如“用温柔的语气，语速稍慢”。

局部情感及笑声、呼吸等表达

在待合成文本中加入情感与富语言标签。

发音、停顿、数字读法等

使用 [SSML](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide#sl01_tagref_h3) 标签精细控制朗读。

数学公式朗读

使用 [LaTeX](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide#sl02_symbols_h3) 表达公式。

按合成方式查看参数、支持条件和示例：

-   [非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#12884a10929p9)
-   [实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#rt_advanced_h2)

## 支持模型

选择调用地域，查看各系列的模型 ID。

#### 北京

-   **Qwen-Audio-TTS**：`qwen-audio-3.1-tts-plus`、`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`
-   **CosyVoice**：`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`、`cosyvoice-v2`
-   **Qwen3-TTS**：`qwen3-tts-flash-realtime`、`qwen3-tts-flash`
-   **MiniMax**：`MiniMax/speech-2.8-hd`、`MiniMax/speech-2.8-turbo`、`MiniMax/speech-02-hd`、`MiniMax/speech-02-turbo`

#### 新加坡

-   **Qwen-Audio-TTS**：`qwen-audio-3.1-tts-plus`、`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`
-   **CosyVoice**：`cosyvoice-v3-plus`、`cosyvoice-v3-flash`
-   **Qwen3-TTS**：`qwen3-tts-flash-realtime`、`qwen3-tts-flash`

## 语言与方言支持

按需要合成的语言或方言选择音色。下表按模型系列和音色类型列出支持范围。

#### Qwen-Audio-TTS

**音色类型**

**合成输出语言与方言**

系统音色

支持中文、英语等语言，具体范围因模型和音色而异，参见[Qwen-Audio-TTS 音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)。

复刻音色

中文（普通话、广东话、重庆话、东北话、甘肃话、贵州话、浙江话、河北话、河南话、湖北话、湖南话、江西话、宁波话、宁夏话、青岛话、陕西话、山西话、山东话、上海话、四川话、云南话）、英语、日语、韩语、俄语、法语、德语、葡萄牙语、泰语、印尼语、越南语、西班牙语、意大利语、马来西亚语、菲律宾语、阿拉伯语 （方言通过指令控制功能进行设置）

设计音色

中文（普通话）、英文

#### CosyVoice

**音色类型**

**合成输出语言与方言**

系统音色

-   `cosyvoice-v3.5-plus` / `cosyvoice-v3.5-flash`: 不支持
-   `cosyvoice-v3-plus`（因音色而异）: 中文（普通话）、英文
-   `cosyvoice-v3-flash`（因音色而异，部分方言由系统音色直接支持，部分通过指令控制功能设置）: 中文（普通话、广东话、东北话、河南话、湖南话、陕西话、山东话、四川话、安徽话、闽南话）、英文、日语、韩语、印尼语
-   `cosyvoice-v2`（因音色而异）: 中文（普通话、粤语、东北话、闽南话、陕西话）、英文、日语、韩语

**说明**系统音色的具体语言、方言和试听参见[CosyVoice 音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。

复刻音色

-   `cosyvoice-v3.5-plus` / `cosyvoice-v3.5-flash`（方言通过指令控制功能进行设置）: 中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语
-   `cosyvoice-v3-plus`: 中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语
-   `cosyvoice-v3-flash`（方言通过指令控制功能进行设置）: 中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语
-   `cosyvoice-v2`: 中文（普通话）、英文

设计音色

-   `cosyvoice-v3.5-plus` / `cosyvoice-v3.5-flash`: 中文（普通话）、英文
-   `cosyvoice-v3-plus`: 中文（普通话）、英文
-   `cosyvoice-v3-flash`: 中文（普通话）、英文
-   `cosyvoice-v2`: 不支持

#### Qwen3-TTS

**音色类型**

**合成输出语言与方言**

系统音色

中文（普通话、北京话、上海话、四川话、南京话、陕西话、闽南话、天津话、粤语，因音色而异）、英文、德语、意大利语、葡萄牙语、西班牙语、日语、韩语、法语、俄语

**说明**系统音色的具体语言、方言和试听参见[Qwen-TTS 音色列表](raw/model-user-guide/model-experience/speech-synthesis/tts-voice-list/qwen-tts-voice-list.md)。

复刻音色

不支持

设计音色

不支持
