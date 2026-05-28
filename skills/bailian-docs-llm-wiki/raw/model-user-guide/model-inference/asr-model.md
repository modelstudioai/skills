# 语音识别

选择适合实时语音识别、录音文件识别等场景的模型。

本文按“先选维度、再看模型”的顺序帮助您完成选型：先从“[选型决策维度](#asr-decide02)”（实时/非实时、专业术语、说话人分离、情感识别）确认场景；再到“[推荐模型](#asr-rec02)”查看针对各场景的首选；如需更多版本可在“[所有模型](#asr-all02)”按系列展开；最后到“[音频规格](#asr-audio-spec02)”核对输入文件约束。各模型支持的语言（含方言）随附在“[所有模型](#asr-all02)”的各系列子节内。

## 选型决策维度

从以下 4 个维度逐项确认，每个维度都会推荐适配的模型。

### 实时还是非实时？

实时是指在用户说话的同时输出识别结果，非实时是指录音结束后再进行转写。

-   **实时（实时语音识别）**：基于WebSocket协议，音频流式输入，文本流式输出。适用于实时字幕、语音助手和会议转写。推荐使用 `fun-asr-realtime`（热词、方言支持）或 `qwen3.5-omni-plus-realtime`（Prompt上下文、多语种）。
    
-   **非实时（录音文件识别）**：基于HTTP协议，提交音频文件获取识别结果。适用于呼叫中心录音、播客和访谈等场景。推荐使用 `fun-asr`（热词、说话人分离）或 `qwen3.5-omni-plus`（Prompt上下文、多语种）。
    

Fun-ASR 和 Qwen-ASR 的实时模型支持通过 DashScope SDK（Java、Python）接入。Fun-ASR 模型还支持 Android、iOS SDK 接入。其他模型需根据对应的 WebSocket 或 HTTP 协议直接调用。

选择实时接入请参考[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)，选择非实时接入请参考[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)。

### 处理专业术语

两种方式，按灵活性排序：

1.  **Prompt上下文注入**：在系统提示词中描述您的领域背景，无需预配置。模型在每次请求时自适应。代价是每次请求的延迟高于专用ASR模型。使用 `qwen3.5-omni-plus-realtime`（实时）或 `qwen3.5-omni-plus`（非实时）。
    
2.  **热词**：提供带权重的词汇表。适合稳定且变化不频繁的术语列表。使用 `fun-asr-realtime`（实时）或 `fun-asr`（非实时）。
    

**说明**

Qwen3.5-Omni不是传统ASR，而是一个能理解音频的大语言模型。您通过Prompt注入上下文，模型无需热词列表即可自适应。

### 说话人分离

仅Fun-ASR系列的非实时模型（`fun-asr`、`fun-asr-mtl`）支持说话人分离。如果您需要区分“谁说了什么”，请使用这些模型。

### 情感识别

Qwen-ASR 和 Qwen3.5-Omni 系列模型在转写的同时支持情感识别。推荐使用 `qwen3-asr-flash-realtime`（实时）或 `qwen3-asr-flash-filetrans`（非实时）。

## 推荐模型

以下为各场景下最推荐的模型，可前往模型广场查看详情。

**模型**

**模式**

**API**

**精度增强**

**情感识别**

**说话人分离**

**支持语言**

**音频最大时长/大小**

`fun-asr-realtime`

实时

WebSocket

热词

不支持

不支持

中、英、日及方言

无限制

`fun-asr`

非实时

HTTP

热词

不支持

支持

多语种及方言

12小时 / 2GB

`qwen3.5-omni-plus-realtime`

实时

WebSocket

Prompt上下文

支持

不支持

多语种

2小时

`qwen3.5-omni-plus`

非实时

HTTP（OpenAI兼容）

Prompt上下文

支持

不支持

多语种

3小时 / 2GB

## 所有模型

### Fun-ASR

**模型**

**模式**

**API**

**精度增强**

**情感识别**

**说话人分离**

[**支持语言**](#488f624638yao)

**音频最大时长/大小**

`fun-asr-realtime`

实时

WebSocket

热词

不支持

不支持

中、英、日及方言

无限制

`fun-asr-realtime-2026-02-28`

实时

WebSocket

热词

不支持

不支持

中、英、日及方言

无限制

`fun-asr-realtime-2025-11-07`

实时

WebSocket

热词

不支持

不支持

中、英、日及方言

无限制

`fun-asr-realtime-2025-09-15`

实时

WebSocket

热词

不支持

不支持

中、英

无限制

`fun-asr-flash-8k-realtime`

实时

WebSocket

热词

不支持

不支持

中文

无限制

`fun-asr-flash-8k-realtime-2026-01-28`

实时

WebSocket

热词

不支持

不支持

中文

无限制

`fun-asr`

非实时

HTTP

热词

不支持

支持

多语种及方言

12小时 / 2GB

`fun-asr-2025-11-07`

非实时

HTTP

热词

不支持

支持

多语种及方言

12小时 / 2GB

`fun-asr-2025-08-25`

非实时

HTTP

热词

不支持

支持

中、英

12小时 / 2GB

`fun-asr-mtl`

非实时

HTTP

热词

不支持

支持

多语种及方言

12小时 / 2GB

`fun-asr-mtl-2025-08-25`

非实时

HTTP

热词

不支持

支持

多语种及方言

12小时 / 2GB

**支持的语言（按版本）**：

-   **Fun-ASR-Realtime 主版本**（`fun-asr-realtime`、`fun-asr-realtime-2026-02-28`、`fun-asr-realtime-2025-11-07`）：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英文、日语
    
-   `fun-asr-realtime-2025-09-15`：中文（普通话）、英文
    
-   **Fun-ASR-Flash-8K-Realtime**（`fun-asr-flash-8k-realtime`、`fun-asr-flash-8k-realtime-2026-01-28`）：中文
    
-   **Fun-ASR / Fun-ASR-MTL 主版本**（`fun-asr`、`fun-asr-2025-11-07`）：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
    
-   `fun-asr-2025-08-25`：中文（普通话）、英文
    
-   **Fun-ASR-MTL**（`fun-asr-mtl`、`fun-asr-mtl-2025-08-25`）：中文（普通话、粤语）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
    

### Qwen-ASR

**模型**

**模式**

**API**

**精度增强**

**情感识别**

**说话人分离**

[**支持语言**](#400aa3042azu7)

**音频最大时长/大小**

`qwen3-asr-flash-realtime`

实时

WebSocket

不支持

支持

不支持

多语种及方言

无限制

`qwen3-asr-flash-realtime-2026-02-10`

实时

WebSocket

不支持

支持

不支持

多语种及方言

无限制

`qwen3-asr-flash-realtime-2025-10-27`

实时

WebSocket

不支持

支持

不支持

多语种及方言

无限制

`qwen3-asr-flash-filetrans`

非实时

HTTP

不支持

支持

不支持

多语种及方言

12小时 / 2GB

`qwen3-asr-flash-filetrans-2025-11-17`

非实时

HTTP

不支持

支持

不支持

多语种及方言

12小时 / 2GB

`qwen3-asr-flash`

非实时

HTTP（OpenAI兼容）

不支持

支持

不支持

多语种及方言

5分钟 / 10MB

`qwen3-asr-flash-2026-02-10`

非实时

HTTP（OpenAI兼容）

不支持

支持

不支持

多语种及方言

5分钟 / 10MB

`qwen3-asr-flash-2025-09-08`

非实时

HTTP（OpenAI兼容）

不支持

支持

不支持

多语种及方言

5分钟 / 10MB

**支持的语言**：所有 Qwen-ASR 系列模型（`qwen3-asr-flash-realtime`、`qwen3-asr-flash-filetrans`、`qwen3-asr-flash` 及其快照版）均支持相同的语言列表：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语。

### Qwen3.5-Omni / Qwen3-Omni

**模型**

**模式**

**API**

**精度增强**

**情感识别**

**说话人分离**

**支持语言**

**音频最大时长/大小**

`qwen3.5-omni-plus-realtime`

实时

WebSocket

Prompt上下文

支持

不支持

多语种

2小时

`qwen3.5-omni-plus`

非实时

HTTP（OpenAI兼容）

Prompt上下文

支持

不支持

多语种

3小时 / 2GB

`qwen3.5-omni-flash-realtime`

实时

WebSocket

Prompt上下文

支持

不支持

多语种

2小时

`qwen3.5-omni-flash`

非实时

HTTP（OpenAI兼容）

Prompt上下文

支持

不支持

多语种

3小时 / 2GB

`qwen3-omni-flash-realtime`

实时

WebSocket

Prompt上下文

支持

不支持

多语种及方言

2小时

`qwen3-omni-flash`

非实时

HTTP（OpenAI兼容）

Prompt上下文

支持

不支持

多语种及方言

20分钟 / 100MB

**支持的语言**：Qwen3.5-Omni / Qwen3-Omni 不属于专用 ASR 模型，其支持的语言以各模型的用户指南和 API 文档为准。

### Paraformer

Paraformer 是较早一代的 ASR 模型，包括实时与非实时两类。若您的业务允许，建议迁移到前文推荐的 Fun-ASR 或 Qwen-ASR。

**模型**

**API**

**说明**

`paraformer-realtime-v2`

WebSocket

实时识别，中、英、日、韩、德、法、俄

`paraformer-realtime-v1`

WebSocket

实时识别，中、英、日、韩、德、法、俄

`paraformer-realtime-8k-v2`

WebSocket

实时识别，8kHz电话场景，中文

`paraformer-realtime-8k-v1`

WebSocket

实时识别，8kHz电话场景，中文

`paraformer-v2`

HTTP

录音文件识别，支持说话人分离，中、英、日、韩、德、法、俄

`paraformer-8k-v2`

HTTP

录音文件识别，8kHz电话场景，中文

`paraformer-v1`

HTTP

录音文件识别，支持说话人分离，中、英、日、韩、德、法、俄

`paraformer-8k-v1`

HTTP

录音文件识别，8kHz电话场景，中文

`paraformer-mtl-v1`

HTTP

录音文件识别，支持说话人分离，多语种

**支持的语言（按版本）**：

-   `paraformer-realtime-v2`、`paraformer-v2`：中文（普通话、粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话、江西话、云南话、上海话）、英文、日语、韩语、德语、法语、俄语
    
-   `paraformer-realtime-v1`、`paraformer-realtime-8k-v2`、`paraformer-realtime-8k-v1`、`paraformer-8k-v2`、`paraformer-8k-v1`：中文普通话
    
-   `paraformer-v1`：中文普通话、英文
    
-   `paraformer-mtl-v1`：中文（普通话、粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话）、英文、日语、韩语、西班牙语、印尼语、法语、德语、意大利语、马来语
    

### 其他（即将下线）

以下模型已计划下线，仅供存量业务参考，请尽快迁移到推荐模型。

**模型**

**API**

**说明**

`gummy-realtime-v1`

WebSocket

实时识别，中、英及方言

`gummy-chat-v1`

WebSocket

短音频实时识别（1分钟限制），多语种

`sensevoice-v1`

HTTP

录音文件识别，多语种

## 音频规格

下表汇总了**实时**和**非实时**两种模式下的音频规格（输入方式、格式、采样率、大小/时长）。各模型支持的语言（含方言）见上文“[所有模型](#asr-all02)”内对应系列子节。**Qwen3.5-Omni / Qwen3-Omni** 不属于专用 ASR，其音频规格请以各自模型的用户指南和 API 文档为准。

### 实时

**模型**

**输入方式**

**音频格式**

**采样率**

**大小/时长**

**Fun-ASR-Realtime / Fun-ASR-MTL-Realtime**（`fun-asr-realtime`、`fun-asr-mtl-realtime` 系列）

二进制（Binary）流

`pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr`

16 kHz

不限

**Fun-ASR-Flash-8K-Realtime**（`fun-asr-flash-8k-realtime` 系列）

二进制（Binary）流

同 Fun-ASR-Realtime

8 kHz

不限

**Qwen-ASR-Realtime**（`qwen3-asr-flash-realtime` 系列）

二进制（Binary）流

`pcm`、`opus`

8 kHz、16 kHz

不限

**Paraformer-Realtime**（`paraformer-realtime-v2/v1`、`paraformer-realtime-8k-v2/v1`）

二进制（Binary）流

同 Fun-ASR-Realtime

`paraformer-realtime-v2` 任意；`paraformer-realtime-v1` 16 kHz；`paraformer-realtime-8k-*` 8 kHz

不限

所有实时模型均为**单声道**输入。

### 非实时

**模型**

**输入方式**

**音频格式**

**采样率**

**文件大小/时长**

**Fun-ASR**（`fun-asr`、`fun-asr-mtl` 系列）

公网可访问的文件 URL，单次最多 100 个

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

任意

≤2 GB；≤12 小时（启用说话人分离建议 ≤2 小时）

**Paraformer**（`paraformer-v2/v1`、`paraformer-mtl-v1`、`paraformer-8k-v2/v1`）

同 Fun-ASR

同 Fun-ASR

`paraformer-v2/v1` 任意；`paraformer-8k-*` 仅 8 kHz；`paraformer-mtl-v1` 16 kHz 及以上

同 Fun-ASR

**Qwen3-ASR-Flash-Filetrans**（`qwen3-asr-flash-filetrans` 系列）

公网可访问的文件 URL，单次 1 个

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

`pcm` 必须 16 kHz；其他格式任意（服务端会重采样为 16 kHz 再识别）

≤2 GB；≤12 小时

**Qwen3-ASR-Flash**（`qwen3-asr-flash` 系列）

URL / Base64 / 本地文件绝对路径，单次 1 个

`aac`、`amr`、`avi`、`aiff`、`flac`、`flv`、`mkv`、`mp3`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

`pcm` 必须 16 kHz；其他格式任意（服务端会重采样为 16 kHz 再识别）

≤10 MB；≤5 分钟
