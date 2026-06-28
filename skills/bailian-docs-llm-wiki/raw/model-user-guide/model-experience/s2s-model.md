# 语音转语音

为“语音输入 → 语音输出”场景（语音对话、语音翻译、同声传译等）选择模型。

**说明**

本文档面向“语音 → 语音”场景。如需视觉理解、音视频分析、内容审核等更广泛的多模态能力，请参考[全模态](https://help.aliyun.com/zh/model-studio/omni/)。

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

-   **ASR（语音识别）**：[语音识别](https://help.aliyun.com/zh/model-studio/asr-model/)
    
-   **LLM（大语言模型）**：[文本生成](https://help.aliyun.com/zh/model-studio/text-generation-model/)
    
-   **TTS（语音合成）**：[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)
    

## 实时还是文件模式？

-   **实时（WebSocket）**：适用于语音助手、呼叫中心、同声传译等实时语音交互场景。音频流式输入，语音流式输出。模型名称中包含`-realtime`。
    
-   **文件模式（HTTP）**：可以用延迟换取更好的效果，适用于视频配音、播客翻译、离线内容处理等场景。文件模式下还支持 Function Calling、联网搜索、思考模式、视频上下文等附带能力（详见下方“S2S 单模型的附带能力”）。
    

## 按场景选模型（S2S 单模型路线）

以下场景均针对 S2S 单模型路线。Pipeline 路线请按上述链接分别在 ASR / LLM / TTS 文档中选型。

**场景**

**推荐模型**

**API**

语音助手 / 客服对话

`qwen3.5-omni-plus-realtime`

WebSocket

成本敏感的对话

`qwen3.5-omni-flash-realtime`

WebSocket

同声传译 / 直播翻译

`qwen3.5-livetranslate-flash-realtime`

WebSocket

视频配音 / 播客翻译

`qwen3-livetranslate-flash`

HTTP

视频分析 / 批量打标（需要思考模式）

`qwen3-omni-flash`

HTTP

## S2S 单模型的附带能力

以下能力由 Qwen3.5-Omni / Qwen3-Omni 模型在 S2S 单模型路线下直接提供。Pipeline 路线中，对应能力需要由其中的 LLM 等组件分别支持。

### Function Calling

让模型根据听到和看到的内容执行操作 -- 查询知识库、查询日程、触发工作流。使用Qwen3.5 Omni（WebSocket与HTTP模式） 或 Qwen3 Omni（HTTP模式）。

**说明**

实时模型和Livetranslate模型不支持此功能。

### 联网搜索

让模型检索实时信息，回答关于时事、股价、天气等问题。使用Qwen3.5 Omni（HTTP和WebSocket），包括Plus和Flash系列。模型自主决定是否搜索。

**说明**

Qwen3-Omni-Flash和Livetranslate模型不支持此功能。

### 思考模式

当回答质量比延迟更重要时，使用Qwen3 Omni（HTTP模式）。模型在回复前会逐步推理，适用于视频分析、批量打标等场景。

**说明**

思考模式下不支持生成语音。

## 翻译

以下模型系列均支持语音翻译：

-   **Qwen3.5-Livetranslate**：支持 60 种语言互译，其中 29 种支持音频+文本输出、31 种仅支持文本输出，覆盖中文、英语、法语、德语、俄语、日语、韩语、西班牙语、葡萄牙语、阿拉伯语等主流语种。。
    
-   **Qwen3-Livetranslate**：支持18种语言 + 5种中文方言，约3秒延迟，开箱即用。文件模式支持输入视频以获得上下文感知的翻译精度。其中7种语言仅输出文本（不输出语音）。
    
-   **Qwen3.5-Omni**：支持29种输出语言 + 7种中文方言。优秀的音视频理解能力和联网搜索。可通过系统提示词注入术语和领域上下文。支持实时和文件模式。
    
-   **Qwen3-Omni-Flash**：支持11种输出语言 + 8种中文方言。可通过系统提示词注入术语和领域上下文。支持实时和文件模式。成本更低。
    

**说明**

快速搭建翻译应用推荐Livetranslate；最高质量和最广语言覆盖推荐Qwen3.5-Omni；成本敏感场景推荐Qwen3-Omni-Flash。

**支持的语言**

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

Qwen3.5-Omni支持113种输入语言/方言。

Qwen3.5-Livetranslate支持60种语言（29种音频+文本，31种仅文本）。

旧版`qwen-omni-turbo`仅支持中文和英文。

## 推荐模型

下表列出每个系列的常用入口模型。如需锁定特定日期版本（用于版本回归或稳定性需求），请见下方“所有模型”。

**模型**

**API**

**输入**

**Function Calling**

**联网搜索**

**思考模式**

**翻译**

`qwen3.5-omni-plus-realtime`

WebSocket

文本、音频、图片

支持

支持

\--

29种

`qwen3.5-omni-plus`

HTTP

文本、音频、图片、视频

支持

支持

\--

29种

`qwen3.5-omni-flash-realtime`

WebSocket

文本、音频、图片

支持

支持

\--

29种

`qwen3.5-omni-flash`

HTTP

文本、音频、图片、视频

支持

支持

\--

29种

`qwen3-omni-flash-realtime`

WebSocket

文本、音频、图片、视频

\--

\--

\--

11种

`qwen3-omni-flash`

HTTP

文本、音频、图片、视频

支持

\--

支持

11种

`qwen3.5-livetranslate-flash-realtime`

WebSocket

音频、图片

\--

\--

\--

60种

`qwen3-livetranslate-flash`

HTTP

音频、视频

\--

\--

\--

18种

## 所有模型

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

HTTP

文本、音频、图片、视频

支持

支持

\--

`qwen3.5-omni-plus-2026-03-15`

HTTP

文本、音频、图片、视频

支持

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

HTTP

文本、音频、图片、视频

支持

支持

\--

`qwen3.5-omni-flash-2026-03-15`

HTTP

文本、音频、图片、视频

支持

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

HTTP

文本、音频、图片、视频

支持

\--

支持

`qwen3-omni-flash-2025-12-01`

HTTP

文本、音频、图片、视频

支持

\--

支持

`qwen3-omni-flash-2025-09-15`

HTTP

文本、音频、图片、视频

支持

\--

支持

### Qwen3.5-Livetranslate

**模型**

**API**

**输入**

**语言数**

`qwen3.5-livetranslate-flash-realtime`

WebSocket

音频

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

HTTP

音频、视频

18

`qwen3-livetranslate-flash-2025-12-01`

HTTP

音频、视频

18

### 旧版模型

以下模型不再更新，新项目建议使用Qwen3.5-Omni。

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

-   Qwen3.5-Omni / Qwen3-Omni（WebSocket，实时）→ 实时Qwen-Omni-Realtime
    
-   Qwen3.5-Omni / Qwen3-Omni（HTTP，文件）→ 非实时Qwen-Omni
    
-   Qwen3.5-Livetranslate（WebSocket，实时）→ 实时语音音视频翻译-千问
    
-   Qwen3-Livetranslate（HTTP，文件）→ 音视频文件翻译-千问
