# 语音合成、识别与翻译 API 对比

百炼平台提供了完整的语音 AI 能力矩阵，涵盖语音合成（TTS）、语音识别（ASR）和语音翻译三大方向。三类 API 在接口协议、模型体系、交互模式和适用场景上各有特点。本文从开发者技术选型角度，对三者进行系统对比，帮助快速判断应选用哪类 API 以及具体模型。

## 核心能力对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
|------|----------------|----------------|---------|
| **核心功能** | 文本 → 语音 | 语音 → 文本 | 语音 → 翻译文本/翻译语音 |
| **模型系列** | Qwen-TTS、CosyVoice、Sambert | Fun-ASR、Paraformer、Qwen-ASR | qwen3-livetranslate-flash（离线）、qwen3.5-livetranslate-flash-realtime（实时） |
| **接口协议** | HTTP REST + WebSocket | WebSocket + RESTful（异步） | OpenAI 兼容 HTTP + WebSocket |
| **实时流式** | 支持（Qwen-TTS-Realtime、CosyVoice） | 支持（Fun-ASR、Paraformer、Qwen-ASR 实时） | 支持（realtime 模型） |
| **离线/批量** | 支持（Qwen-TTS 非实时 HTTP） | 支持（Paraformer 录音文件识别） | 支持（qwen3-livetranslate-flash） |
| **多语种** | 中英日韩等 10 种 | 中英日粤及多种外语 | 多语种互译 |
| **地域支持** | 北京、新加坡 | 北京、新加坡（Paraformer 实时仅北京） | 北京、新加坡 |

## 接口协议与端点对比

| API 类型 | 协议 | 端点示例（北京） | 认证方式 |
|----------|------|-----------------|---------|
| TTS — Qwen-TTS 非实时 | HTTP REST | OpenAI 兼容或 DashScope REST | API Key (Bearer) |
| TTS — Qwen-TTS-Realtime | WebSocket | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime` | API Key |
| TTS — CosyVoice | WebSocket | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | API Key |
| TTS — Sambert | WebSocket | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | API Key |
| ASR — Fun-ASR / Paraformer 实时 | WebSocket | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | API Key |
| ASR — Qwen-ASR 实时 | WebSocket | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model>` | API Key |
| ASR — Paraformer 录音文件 | RESTful（异步） | `POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription` | API Key + X-DashScope-Async |
| 翻译 — 离线 | OpenAI 兼容 HTTP | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | API Key |
| 翻译 — 实时 | WebSocket | WebSocket 事件协议（Realtime API） | API Key |

## 交互流程对比

| 维度 | TTS | ASR | 翻译 |
|------|-----|-----|------|
| **输入** | 文本（支持流式追加） | 二进制音频流 | 音频/视频 URL 或 Base64（离线）；音频流+可选视频帧（实时） |
| **输出** | 二进制音频流（pcm/wav/mp3/opus） | 结构化文本（含时间戳、逐字信息） | 翻译文本 + 可选翻译音频 |
| **WebSocket 事件模型** | run-task / continue-task / finish-task（CosyVoice）；session 事件驱动（Qwen-TTS-Realtime） | run-task / 二进制音频 / finish-task | session.update / input_audio_buffer.append / session.finish |
| **流式粒度** | 音频片段实时返回 | 中间结果 + sentence_end 最终结果 | 增量文本 chunk + 增量音频 chunk |

## 模型选型指南

### 语音合成（TTS）

| 模型/引擎 | 推荐场景 | 特点 |
|-----------|---------|------|
| Qwen-TTS（非实时） | 离线批量合成、短文本朗读 | HTTP 接口简单，支持指令控制语音风格 |
| Qwen-TTS-Realtime | 实时对话、低延迟交互 | 双工流式，支持 ServerCommit 智能断句 |
| CosyVoice | 实时流式合成、长文本朗读 | 大模型音质，continue-task 流式输入 |
| Sambert | 传统 TTS、多发音人选择 | 稳定成熟，一次性文本输入 |

### 语音识别（ASR）

| 模型系列 | 推荐场景 | 特点 |
|----------|---------|------|
| Fun-ASR 实时 | 会议转写、实时对话 | 低延迟，支持北京+新加坡，VAD 灵敏度可调 |
| Paraformer 实时 | 实时转写（北京地域） | 仅北京，语义断句可选 |
| Qwen-ASR 实时 | 多语种实时识别 | 支持 VAD/Manual 两种断句模式 |
| Paraformer 录音文件 | 长音频离线批量转写 | RESTful 异步接口，适合大规模处理 |

### 语音翻译

| 模型 | 推荐场景 | 特点 |
|------|---------|------|
| qwen3-livetranslate-flash | 整段音视频离线翻译 | [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，支持音频+视频输入 |
| qwen3.5-livetranslate-flash-realtime | 直播、同声传译 | 实时双向事件流，支持声音复刻跟随 |

## SDK 与开发语言支持

| API 类型 | Python | Java | Android | iOS | cURL |
|----------|--------|------|---------|-----|------|
| TTS（Qwen-TTS） | 支持 | 支持 | — | — | 支持 |
| TTS（Qwen-TTS-Realtime） | 支持（≥1.25.11） | 支持（≥2.22.7） | — | — | — |
| TTS（CosyVoice/Sambert） | 支持 | 支持 | — | — | — |
| ASR（Fun-ASR/Paraformer） | 支持 | 支持 | 支持 | 支持 | — |
| ASR（Qwen-ASR） | 支持 | 支持 | — | — | — |
| ASR（Paraformer 录音文件） | 支持 | 支持 | 支持 | 支持 | 支持 |
| 翻译（离线） | 支持（OpenAI SDK） | — | — | — | 支持 |
| 翻译（实时） | 支持 | — | — | — | — |

## 音频格式与采样率对比

| API 类型 | 支持的音频格式 | 采样率 |
|----------|--------------|--------|
| TTS 输出 | pcm、wav、mp3、opus | 8000/16000/24000/48000 Hz |
| ASR 输入 | pcm、wav、mp3、opus、speex、aac、amr | 8000/16000 Hz（因模型而异） |
| 翻译输入 | pcm、opus（实时）；wav、mp3 等（离线） | 16000 Hz（实时默认） |
| 翻译输出 | pcm（实时）；wav（离线） | — |

## 技术选型建议

1. **文本转语音**：选 TTS API。追求低延迟实时交互用 Qwen-TTS-Realtime；离线批量合成用 Qwen-TTS 非实时 HTTP 接口；需要流式长文本朗读用 CosyVoice。
2. **语音转文字**：选 ASR API。实时转写优先 Fun-ASR（支持双地域）；长音频离线转写用 Paraformer 录音文件识别（RESTful 异步）。
3. **跨语言翻译**：选翻译 API。直播同传用 qwen3.5-livetranslate-flash-realtime；离线整段翻译用 qwen3-livetranslate-flash（[OpenAI 兼容接口](../concepts/openai-compatible-api.md)，接入成本低）。
4. **组合使用**：语音翻译 API 内部已集成 ASR + 翻译 + 可选 TTS，无需手动串联 ASR 和 TTS。若需要定制化流水线（如先识别再翻译再合成），可分别调用各 API 组合。
5. **地域合规**：Paraformer 实时仅限北京地域；其他 API 均支持北京和新加坡双地域部署，跨境业务需注意 API Key 不互通。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)


