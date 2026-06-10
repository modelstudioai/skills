# 语音合成 vs 语音识别

阿里云百炼平台同时提供语音合成（TTS，Text-to-Speech）与语音识别（ASR，Automatic Speech Recognition）能力，两者共同构成语音交互的核心链路。本文从技术维度对两类服务进行对比，帮助开发者理解其差异并在实际项目中做出合理选型。

## 核心差异概览

| 维度 | 语音合成（TTS） | 语音识别（ASR） |
| --- | --- | --- |
| **任务目标** | 文本 → 音频（合成语音） | 音频 → 文本（语音转写） |
| **输入格式** | 纯文本（支持自然语言指令控制语速、情绪等） | 音频流（PCM/WAV/MP3/Opus/Speex/AAC/AMR） |
| **输出格式** | 音频流（PCM/MP3/WAV 等，base64 或二进制） | 文本（含时间戳、逐字对齐、标点） |
| **典型模型** | Qwen-TTS、CosyVoice、Sambert、MiniMax Speech | Fun-ASR、Paraformer、Qwen-ASR |
| **协议支持** | HTTP（非实时）、WebSocket（实时流式） | WebSocket（实时）、RESTful（录音文件异步） |
| **地域覆盖** | 华北2（北京）、新加坡 | 华北2（北京）、新加坡（Paraformer 实时仅北京） |
| **计费方式** | 按合成字符数计费 | 按识别音频时长（秒）计费 |
| **延迟特性** | 首包延迟 200ms–1s（流式更低） | 实时识别延迟 < 500ms；录音文件为[异步任务](../concepts/async-task.md) |

## 模型家族对比

### 语音合成模型

| 模型系列 | 定位 | 协议 | 特色能力 |
| --- | --- | --- | --- |
| Qwen-TTS（非实时） | 离线/批量合成 | HTTP | 支持 `instruct` 模型通过自然语言控制语调、情绪 |
| Qwen-TTS Realtime | 实时对话 | WebSocket | ServerCommit/Commit 两种模式，低延迟 |
| CosyVoice | 高表现力流式 | WebSocket | 情感与韵律表现强，三段式事件协议 |
| Sambert | 多音色多端 | WebSocket | 音色库丰富，支持移动端 SDK，仅北京 |
| MiniMax Speech | 兼容 OpenAI 风格 | HTTP | 支持情绪标签 `(laughs)` `(happy)`、自定义词典 |

### 语音识别模型

| 模型系列 | 定位 | 协议 | 特色能力 |
| --- | --- | --- | --- |
| Fun-ASR 实时 | 低延迟实时转写 | WebSocket | 支持 VAD/语义断句、定制热词、多语种 |
| Paraformer 实时 | 北京地域实时 | WebSocket | 语义断句、静音阈值可调，仅北京 |
| Qwen-ASR 实时 | 多语种实时 | WebSocket | VAD/Manual 两种断句模式，支持中日粤英 |
| Paraformer 录音文件 | 长音频离线转写 | RESTful（异步） | 适合会议/录音批量处理，返回含时间戳结果 |

## 技术选型建议

### 选语音合成（TTS）的场景

- **智能客服/语音助手**：需要将回复文本实时合成为语音播报给用户，推荐 Qwen-TTS Realtime 或 CosyVoice，低延迟、表现力好。
- **有声读物/内容朗读**：批量将文本转为音频文件，推荐 Qwen-TTS 非实时（`instruct` 模型可精细控制语速语调）。
- **多音色需求**：需要丰富角色音色或移动端集成，推荐 Sambert。
- **OpenAI 兼容迁移**：已有 OpenAI TTS 代码，推荐 MiniMax Speech，接口风格兼容。

### 选语音识别（ASR）的场景

- **实时字幕/会议转写**：需要低延迟边说边出字，推荐 Fun-ASR 实时或 Qwen-ASR 实时。
- **录音文件批量处理**：长音频离线转写，推荐 Paraformer 录音文件识别（[异步任务](../concepts/async-task.md)）。
- **多语种识别**：涉及日语、粤语等外语，推荐 Qwen-ASR 实时。
- **北京地域专属**：对北京地域有合规要求，Paraformer 实时和 Fun-ASR 均可。

## 开发集成要点

### 鉴权与端点

两者共享 DashScope 鉴权体系（`Authorization: Bearer <api_key>`）与相同的地域端点（北京 `dashscope.aliyuncs.com`、新加坡 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`），可在同一项目中统一管理 API Key。

### SDK 支持

- **TTS**：官方提供 Python/Java SDK（`MultiModalConversation` 接口），WebSocket 流式场景需自行处理事件协议。
- **ASR**：官方提供 Python/Java/Android/iOS 全平台 SDK，录音文件识别支持 cURL 直接调用。

### 组合使用

典型的语音交互链路为：用户语音 → ASR 转写 → LLM 处理 → TTS 合成 → 语音回复。两者可串联使用，建议：

1. 实时对话场景：ASR 选 Fun-ASR/Qwen-ASR 实时 + TTS 选 Qwen-TTS Realtime/CosyVoice，全链路 WebSocket 流式。
2. 离线处理场景：ASR 选 Paraformer 录音文件 + TTS 选 Qwen-TTS 非实时，异步批量执行。

## 总结

语音合成与语音识别是互补的两类能力：TTS 解决"让机器说话"，ASR 解决"让机器听懂"。选型时首先明确业务是"输出语音"还是"输入语音"，再根据实时性、地域、语种、表现力等维度选择对应模型系列。两者共享鉴权体系与基础设施，可无缝组合构建完整的语音交互应用。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)


