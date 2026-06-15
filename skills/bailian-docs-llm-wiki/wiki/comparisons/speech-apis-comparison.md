# 语音合成、识别与翻译 API 对比

百炼平台提供了完整的语音处理能力矩阵，涵盖语音合成（TTS）、语音识别（ASR）和语音翻译三大方向。三类 API 在接口协议、交互模式、支持的模型和适用场景上各有侧重。本文从开发者技术选型的角度，对三者进行系统对比，帮助快速定位所需能力并完成接入。

## 核心能力对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
|------|----------------|----------------|----------|
| **功能方向** | 文本 → 语音 | 语音 → 文本 | 语音 → 翻译文本/语音 |
| **主要模型** | Qwen-TTS、CosyVoice、Sambert | Fun-ASR、Paraformer、Qwen-ASR | qwen3-livetranslate-flash、qwen3.5-livetranslate-flash-realtime |
| **接口协议** | HTTP REST + WebSocket | WebSocket + RESTful（异步） | OpenAI 兼容 HTTP + WebSocket |
| **实时流式** | 支持（Qwen-TTS-Realtime、CosyVoice） | 支持（Fun-ASR、Paraformer、Qwen-ASR 实时） | 支持（realtime WebSocket） |
| **离线/批量** | 支持（Qwen-TTS 非实时 HTTP） | 支持（Paraformer 录音文件 RESTful） | 支持（OpenAI 兼容 HTTP 流式） |
| **多语种** | 中英日韩等 10 种 | 中英日粤及多种外语 | 多语种互译 |
| **地域支持** | 北京、新加坡 | 北京、新加坡（Paraformer 实时仅北京） | 北京、新加坡 |

## 接口协议与交互模式对比

| 维度 | 语音合成 | 语音识别 | 语音翻译 |
|------|---------|---------|----------|
| **HTTP REST** | Qwen-TTS 非实时（MultiModalConversation） | Paraformer 录音文件（异步 RESTful） | qwen3-livetranslate-flash（OpenAI 兼容，必须 stream=true） |
| **WebSocket（run-task 协议）** | CosyVoice、Sambert | Fun-ASR、Paraformer 实时 | — |
| **WebSocket（Realtime API 事件协议）** | Qwen-TTS-Realtime | Qwen-ASR 实时 | qwen3.5-livetranslate-flash-realtime |
| **数据流向** | 客户端发文本 → 服务端返音频流 | 客户端发音频流 → 服务端返文本 | 客户端发音频流 → 服务端返翻译文本/音频 |
| **SDK 支持** | Python、Java | Python、Java、Android、iOS | Python、Java |

## 模型与引擎对比

### 语音合成引擎

| 引擎 | 协议 | 流式输入 | 典型场景 |
|------|------|---------|---------|
| Qwen-TTS（非实时） | HTTP REST | 支持[流式输出](../concepts/streaming-output.md) | 短文本离线合成 |
| Qwen-TTS-Realtime | WebSocket Realtime API | 全双工 | 实时交互、低延迟 |
| CosyVoice | WebSocket run-task | 支持（continue-task） | 实时流式合成 |
| Sambert | WebSocket run-task | 不支持 | 传统 TTS、多发音人 |

### 语音识别引擎

| 引擎 | 协议 | 场景 | 地域限制 |
|------|------|------|---------|
| Fun-ASR 实时 | WebSocket | 低延迟实时转写 | 北京、新加坡 |
| Paraformer 实时 | WebSocket | 实时转写 | 仅北京 |
| Qwen-ASR 实时 | WebSocket Realtime API | 多语种实时识别 | 北京、新加坡 |
| Paraformer 录音文件 | RESTful 异步 | 长音频离线批量转写 | 仅北京 |

### 语音翻译模型

| 模型 | 协议 | 场景 |
|------|------|------|
| qwen3-livetranslate-flash | OpenAI 兼容 HTTP | 离线音视频翻译 |
| qwen3.5-livetranslate-flash-realtime | WebSocket 事件协议 | 直播、同声传译 |

## 服务端点对比

| API 类型 | 北京端点 | 新加坡端点 |
|---------|---------|-----------|
| TTS HTTP（Qwen-TTS） | DashScope REST API | DashScope REST API |
| TTS WebSocket（Realtime） | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime` |
| TTS WebSocket（CosyVoice/Sambert） | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference` |
| ASR WebSocket（Fun-ASR/Paraformer） | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference` |
| ASR WebSocket（Qwen-ASR） | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime` |
| ASR RESTful（录音文件） | `https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription` | — |
| 翻译 HTTP（离线） | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions` |
| 翻译 WebSocket（实时） | WebSocket Realtime API | WebSocket Realtime API |

## 计费与输入输出格式

| 维度 | 语音合成 | 语音识别 | 语音翻译 |
|------|---------|---------|----------|
| **输入格式** | 文本（纯文本/SSML） | 音频流（pcm/wav/mp3/opus 等） | 音频 URL/Base64 或实时音频流，可选视频帧 |
| **输出格式** | 音频流（pcm/wav/mp3/opus） | 结构化文本（含时间戳、逐字对齐） | 翻译文本 + 可选音频（wav） |
| **计费单位** | 按合成字符数 | 按识别音频时长 | 按 token 数（含 audio_tokens 和 text_tokens） |

## 特色能力对比

| 能力 | 语音合成 | 语音识别 | 语音翻译 |
|------|---------|---------|----------|
| 声音复刻 | 支持（CosyVoice、Qwen-TTS） | — | 支持（实时翻译可配置声音复刻频率） |
| 热词定制 | — | 支持（vocabulary_id） | 支持（translation.corpus.phrases） |
| 语音风格控制 | 支持（qwen3-tts-instruct 指令控制） | — | — |
| 多模态输入 | — | — | 支持音频 + 视频帧输入 |
| ASR 原文输出 | — | 核心功能 | 可选（配置 input_audio_transcription） |
| 语速调节 | 支持（speech_rate） | — | — |
| VAD 断句 | — | 支持（可配静音阈值） | — |

## 适用场景建议

- **智能客服/语音助手**：语音识别（Fun-ASR/Qwen-ASR 实时）+ 语音合成（Qwen-TTS-Realtime），构成完整的语音交互链路。
- **会议纪要/字幕生成**：语音识别（Paraformer 录音文件）适合长音频离线转写；实时场景用 Fun-ASR 实时。
- **有声内容制作**：语音合成（Qwen-TTS 非实时或 CosyVoice），支持多种音色和声音复刻。
- **直播同声传译**：语音翻译（qwen3.5-livetranslate-flash-realtime），支持实时音频输入和翻译输出，可同时返回 ASR 原文。
- **离线音视频翻译**：语音翻译（qwen3-livetranslate-flash），通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)提交整段音视频。
- **多语种实时识别**：Qwen-ASR 实时，支持 VAD/Manual 两种断句模式，覆盖多语种。

## 技术选型决策参考

1. **确定数据流向**：文本转语音选 TTS，语音转文本选 ASR，跨语种翻译选语音翻译。
2. **确定实时性需求**：低延迟实时场景选 WebSocket 协议的引擎，离线批量场景选 HTTP/RESTful 接口。
3. **确定地域要求**：如需新加坡部署，注意 Paraformer 实时仅支持北京地域。
4. **确定附加能力**：需要声音复刻选 CosyVoice 或实时翻译；需要热词定制选 Fun-ASR/Paraformer 或实时翻译；需要语音风格控制选 qwen3-tts-instruct。
5. **确定集成方式**：偏好 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)选离线翻译；偏好传统 WebSocket 选 CosyVoice/Fun-ASR；偏好 Realtime API 事件协议选 Qwen-TTS-Realtime/Qwen-ASR/实时翻译。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)


