# 语音合成、识别与翻译 API 对比

百炼平台围绕语音能力提供了三大类 API：语音合成（TTS）、语音识别（ASR）和语音翻译（Speech Translation）。三者分别面向"文本转语音""语音转文字""跨语种语音翻译"场景，在接口协议、模型选择、输入输出格式和计费逻辑上各有差异。本文从开发者技术选型角度，系统对比三类 API 的核心维度，帮助快速定位适合自身业务的接入方案。

## 核心维度对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
|------|----------------|----------------|----------|
| **功能定位** | 文本 → 语音 | 语音 → 文字 | 语音 → 翻译文本/语音 |
| **主要模型** | Qwen-TTS（qwen3-tts-flash）、CosyVoice、Sambert | Fun-ASR、Paraformer、Qwen-ASR | qwen3-livetranslate-flash（离线）、qwen3.5-livetranslate-flash-realtime（实时） |
| **接口协议** | HTTP REST（Qwen-TTS 非实时）、WebSocket（Qwen-TTS-Realtime / CosyVoice / Sambert） | WebSocket（实时识别）、RESTful 异步（录音文件识别） | OpenAI 兼容 HTTP 流式（离线）、WebSocket 事件协议（实时） |
| **输入格式** | 纯文本（含可选语音指令） | 二进制音频流（pcm/wav/mp3/opus/speex/aac/amr） | 音频 URL/Base64 或视频 URL（离线）；Base64 音频流 + 可选图像帧（实时） |
| **输出格式** | 二进制音频（pcm/wav/mp3/opus） | JSON 文本结果（含时间戳、逐字信息） | 流式文本 chunk + 可选 Base64 音频（离线）；事件流文本/音频（实时） |
| **流式支持** | 支持流式文本输入 + 流式音频输出 | 支持实时音频流输入 + 中间结果推送 | 离线模式仅[流式输出](../concepts/streaming.md)；实时模式双向流式 |
| **支持地域** | 北京、新加坡 | 北京（全系列）、新加坡（Fun-ASR / Qwen-ASR） | 北京、新加坡 |
| **多语种** | 中英日韩等 10 种语言 | 中英日粤及多种外语 | 多语种互译，目标语种必填 |
| **SDK 支持** | Python、Java | Python、Java、Android、iOS | Python、Java（OpenAI SDK 兼容） |
| **鉴权方式** | API Key（Bearer Token） | API Key（Bearer Token） | API Key（Bearer Token） |

## 接口协议与交互模式对比

| 对比项 | 语音合成 | 语音识别 | 语音翻译 |
|--------|---------|---------|---------|
| **HTTP REST** | Qwen-TTS 非实时模式，调用 MultiModalConversation 接口 | Paraformer 录音文件识别，异步提交 + 轮询结果 | 离线翻译，OpenAI 兼容 chat/completions 接口（stream=true） |
| **WebSocket（传统协议）** | CosyVoice（run-task / continue-task）、Sambert（run-task） | Fun-ASR / Paraformer 实时（run-task 协议） | 不适用 |
| **WebSocket（Realtime 事件协议）** | Qwen-TTS-Realtime（session.update 事件驱动） | Qwen-ASR（session 事件协议） | 实时翻译（session.update 事件驱动） |
| **典型延迟** | 低延迟（实时模式）到秒级（非实时） | 实时流式毫秒级；录音文件分钟级 | 实时同传毫秒级；离线翻译秒级 |

## 模型与引擎选择对比

### 语音合成引擎

| 引擎 | 协议 | 流式输入 | 特色 | 适用场景 |
|------|------|---------|------|---------|
| Qwen-TTS（非实时） | HTTP REST | 仅[流式输出](../concepts/streaming.md) | 指令控制语音风格（instruct 模型） | 短文本离线合成 |
| Qwen-TTS-Realtime | WebSocket Realtime API | 全双工 | ServerCommit/Commit 两种模式 | 实时交互、对话场景 |
| CosyVoice | WebSocket 传统协议 | continue-task 流式 | 自然度高，大模型驱动 | 实时流式合成 |
| Sambert | WebSocket 传统协议 | 不支持 | 多发音人，传统稳定 | 传统 TTS、固定音色 |

### 语音识别模型

| 模型系列 | 协议 | 地域限制 | 特色 | 适用场景 |
|---------|------|---------|------|---------|
| Fun-ASR 实时 | WebSocket | 北京、新加坡 | VAD 灵敏度可调 | 低延迟实时转写、会议 |
| Paraformer 实时 | WebSocket | 仅北京 | 稳定成熟 | 实时转写 |
| Qwen-ASR 实时 | WebSocket | 北京、新加坡 | VAD/Manual 双断句模式 | 多语种实时识别 |
| Paraformer 录音文件 | RESTful 异步 | 北京 | 支持长音频批量处理 | 离线批量转写 |

### 语音翻译模型

| 模型 | 协议 | 特色 | 适用场景 |
|------|------|------|---------|
| qwen3-livetranslate-flash | OpenAI 兼容 HTTP | 输入整段音视频 URL | 离线音视频翻译 |
| qwen3.5-livetranslate-flash-realtime | WebSocket 事件协议 | 支持声音复刻、ASR 原文、视频帧 | 直播同传、实时翻译 |

## 适用场景建议

- **智能客服 / 语音助手**：语音识别（Fun-ASR / Qwen-ASR 实时）+ 语音合成（Qwen-TTS-Realtime）组合使用，实现全双工语音交互。
- **音视频内容生产**：语音合成（Qwen-TTS 非实时或 CosyVoice）用于配音，语音识别（Paraformer 录音文件）用于字幕生成。
- **跨语种直播 / 同声传译**：直接使用实时语音翻译（qwen3.5-livetranslate-flash-realtime），一站式完成识别 + 翻译 + 可选语音输出。
- **离线音视频翻译**：使用离线翻译模型（qwen3-livetranslate-flash），通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)提交音视频 URL 即可获取翻译结果。
- **会议纪要 / 录音转写**：语音识别（Paraformer 录音文件异步 API）适合长音频批量处理，配合热词定制提升专业术语准确率。
- **有声读物 / 播报**：语音合成中 Sambert 提供丰富的固定音色，CosyVoice 提供更自然的大模型合成效果，按品质与成本需求选择。

## 技术选型参考

1. **实时性要求**：需要低延迟双向流式交互时，三类 API 均应选择 WebSocket 协议的实时模型；对延迟不敏感则可选 HTTP REST 或异步接口。
2. **地域合规**：Paraformer 实时识别仅支持北京地域，海外业务需选择 Fun-ASR 或 Qwen-ASR；语音合成和翻译的主要模型均已支持新加坡地域。
3. **协议统一性**：Qwen-TTS-Realtime、Qwen-ASR 和实时翻译均采用相似的 WebSocket Realtime 事件协议（session.update 风格），便于统一封装和维护。
4. **多语种需求**：语音翻译天然支持跨语种；语音合成的 Qwen-TTS 支持 10 种语言；语音识别建议根据语种选择对应模型系列。
5. **输出模态**：语音翻译可同时输出文本和音频（modalities 配置），语音合成仅输出音频，语音识别仅输出文本。如需"识别 + 翻译 + 合成"全链路，实时翻译 API 是最简集成方案。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)


