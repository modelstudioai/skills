# 全模态

选择适合多模态理解、音视频分析、语音对话、内容审核、语音翻译等全模态场景的模型。

## 使用场景

全模态模型能同时理解文本、音频、图片和视频，并输出文本和语音。当前提供三个模型系列：**Qwen3.5-Omni**（旗舰，能力最全）、**Qwen3-Omni-Flash**（轻量，成本更低，支持深度推理）、**Qwen3.5-Livetranslate**（专业翻译，开箱即用）。根据您的场景选择合适的模型：

**场景**

**推荐模型**

**用户指南**

**实时语音/视频对话**：通过麦克风和摄像头与AI实时交互（语音助手、智能客服、视觉问答、直播分析）

Qwen3.5-Omni Realtime（WebSocket）

[实时（Qwen-Omni-Realtime）](https://help.aliyun.com/zh/model-studio/realtime)

**音视频内容分析**：上传音频或视频文件，AI分析内容并生成文本或语音回复（视频审核、会议纪要、字幕生成）

Qwen3.5-Omni（HTTP）

[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)

**轻量音视频分析**：上传音频或视频文件进行分析，成本更低（单次输入限150秒）。支持深度推理（思考模式），仅输出文本

Qwen3-Omni-Flash（HTTP）

[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)

**实时语音翻译**：语音同传，约3秒延迟，支持60种语言（同声传译、多语言会议）

Qwen3.5-Livetranslate（WebSocket）

[实时语音/音视频翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime)

**音视频文件翻译**：上传音频/视频文件翻译为目标语言（视频配音、播客翻译）

Qwen3-Livetranslate（HTTP）

[音视频文件翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-livetranslate-flash)

**声音复刻**：提供参考音频，AI用该音色生成语音回复

Qwen3.5-Omni Plus / Flash（HTTP / WebSocket）

[非实时（Qwen-Omni）](https://help.aliyun.com/zh/model-studio/qwen-omni)

-   内容分析场景中，Qwen3.5-Omni支持音频最长3小时、视频最长1小时。
    
-   支持工具调用（Function Calling）：Qwen3.5-Omni（WebSocket + HTTP）、Qwen3-Omni-Flash（仅HTTP）。
    
-   支持联网搜索：仅Qwen3.5-Omni（HTTP / WebSocket）。联网搜索与Function Calling不可同时开启。
    

## 翻译

全模态模型支持语音翻译，不同模型适用于不同翻译场景。

**说明**

快速搭建翻译应用推荐Qwen3.5-Livetranslate（60种语言，约3秒延迟，开箱即用）；最高质量和最广语言覆盖推荐Qwen3.5-Omni（29种输出语言，支持联网搜索和术语注入）；成本敏感场景推荐Qwen3-Omni-Flash（11种输出语言，成本更低）。

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

支持 仅文本

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

不支持

不支持

支持

支持

陕西话

不支持

不支持

支持

支持

闽南语

不支持

不支持

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

支持 仅文本

支持

支持

印尼语

支持

支持 仅文本

支持

不支持

越南语

支持

支持 仅文本

支持

不支持

阿拉伯语

支持

支持 仅文本

支持

不支持

印地语

支持

支持 仅文本

支持

不支持

土耳其语

支持

支持 仅文本

支持

不支持

芬兰语

支持

不支持

支持

不支持

波兰语

支持

不支持

支持

不支持

荷兰语

支持

不支持

支持

不支持

捷克语

支持

不支持

支持

不支持

乌尔都语

支持

不支持

支持

不支持

他加禄语

支持

不支持

支持

不支持

瑞典语

支持

不支持

支持

不支持

丹麦语

支持

不支持

支持

不支持

希伯来语

支持

不支持

支持

不支持

冰岛语

支持

不支持

支持

不支持

马来语

支持

不支持

支持

不支持

挪威语

支持

不支持

支持

不支持

波斯语

支持

不支持

支持

不支持

希腊语

支持 仅文本

支持 仅文本

不支持

不支持

南非荷兰语

支持 仅文本

不支持

不支持

不支持

阿斯图里亚斯语

支持 仅文本

不支持

不支持

不支持

白俄罗斯语

支持 仅文本

不支持

不支持

不支持

保加利亚语

支持 仅文本

不支持

不支持

不支持

孟加拉语

支持 仅文本

不支持

不支持

不支持

波斯尼亚语

支持 仅文本

不支持

不支持

不支持

加泰罗尼亚语

支持 仅文本

不支持

不支持

不支持

宿务语

支持 仅文本

不支持

不支持

不支持

爱沙尼亚语

支持 仅文本

不支持

不支持

不支持

加利西亚语

支持 仅文本

不支持

不支持

不支持

古吉拉特语

支持 仅文本

不支持

不支持

不支持

克罗地亚语

支持 仅文本

不支持

不支持

不支持

匈牙利语

支持 仅文本

不支持

不支持

不支持

爪哇语

支持 仅文本

不支持

不支持

不支持

哈萨克语

支持 仅文本

不支持

不支持

不支持

卡纳达语

支持 仅文本

不支持

不支持

不支持

柯尔克孜语

支持 仅文本

不支持

不支持

不支持

拉脱维亚语

支持 仅文本

不支持

不支持

不支持

马其顿语

支持 仅文本

不支持

不支持

不支持

马拉雅拉姆语

支持 仅文本

不支持

不支持

不支持

马拉地语

支持 仅文本

不支持

不支持

不支持

旁遮普语

支持 仅文本

不支持

不支持

不支持

罗马尼亚语

支持 仅文本

不支持

不支持

不支持

斯洛伐克语

支持 仅文本

不支持

不支持

不支持

斯洛文尼亚语

支持 仅文本

不支持

不支持

不支持

斯瓦希里语

支持 仅文本

不支持

不支持

不支持

塔吉克语

支持 仅文本

不支持

不支持

不支持

阿塞拜疆语

支持 仅文本

不支持

不支持

不支持

乌克兰语

支持 仅文本

不支持

不支持

不支持

“支持”表示同时输出语音和文本。“仅文本”表示该语言不输出语音。

Qwen3.5-Omni支持113种输入语言/方言。

Qwen3.5-Livetranslate支持60种语言（29种音频+文本，31种仅文本）。

旧版`qwen-omni-turbo`仅支持中文和英文。

## 推荐模型

**模型**

**API**

**输入**

**Function Calling**

**联网搜索**

**思考模式**

`qwen3.5-omni-plus-realtime`

WebSocket

文本、音频、图片

支持

支持

不支持

`qwen3.5-omni-plus`

HTTP

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-flash-realtime`

WebSocket

文本、音频、图片

支持

支持

不支持

`qwen3.5-omni-flash`

HTTP

文本、音频、图片、视频

支持

支持

不支持

`qwen3-omni-flash-realtime`

WebSocket

文本、音频、图片、视频

不支持

不支持

不支持

`qwen3-omni-flash`

HTTP

文本、音频、图片、视频

支持

不支持

支持

`qwen3.5-livetranslate-flash-realtime`

WebSocket

音频、图片

不支持

不支持

不支持

`qwen3.5-livetranslate-flash`

HTTP

音频、视频

不支持

不支持

不支持

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

不支持

`qwen3.5-omni-plus-realtime-2026-03-15`

WebSocket

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-plus`

HTTP

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-plus-2026-03-15`

HTTP

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-flash-realtime`

WebSocket

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-flash-realtime-2026-03-15`

WebSocket

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-flash`

HTTP

文本、音频、图片、视频

支持

支持

不支持

`qwen3.5-omni-flash-2026-03-15`

HTTP

文本、音频、图片、视频

支持

支持

不支持

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

不支持

不支持

不支持

`qwen3-omni-flash-realtime-2025-12-01`

WebSocket

文本、音频、图片、视频

不支持

不支持

不支持

`qwen3-omni-flash-realtime-2025-09-15`

WebSocket

文本、音频、图片、视频

不支持

不支持

不支持

`qwen3-omni-flash`

HTTP

文本、音频、图片、视频

支持

不支持

支持

`qwen3-omni-flash-2025-12-01`

HTTP

文本、音频、图片、视频

支持

不支持

支持

`qwen3-omni-flash-2025-09-15`

HTTP

文本、音频、图片、视频

支持

不支持

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
