# 语音合成、识别与翻译 API 对比

百炼平台在语音领域提供了三大类 API 能力：语音合成（TTS）、语音识别（ASR）和语音翻译（Speech Translation）。三者面向不同的业务场景，在接口协议、模型选择、输入输出格式和计费维度上各有差异。本文从开发者技术选型的角度，对三类 API 进行系统对比，帮助快速确定适合自身业务的接入方案。

## 核心能力对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
|------|----------------|----------------|---------|
| **核心功能** | 文本 → 语音 | 语音 → 文本 | 语音 → 翻译文本（可选译后语音） |
| **主要引擎/模型** | Qwen-TTS、CosyVoice、Sambert | Fun-ASR、Paraformer、Qwen-ASR | qwen3-livetranslate-flash（离线）、qwen3.5-livetranslate-flash-realtime（实时） |
| **接口协议** | HTTP REST + WebSocket | WebSocket + RESTful（异步） | OpenAI 兼容 HTTP + WebSocket 事件协议 |
| **实时/离线** | 均支持（Qwen-TTS 非实时为离线，Realtime/CosyVoice 为实时） | 实时流式（Fun-ASR/Paraformer/Qwen-ASR）+ 录音文件离线转写 | 离线整段翻译 + 实时流式翻译 |
| **输入格式** | 文本（纯文本/指令文本） | 音频流（pcm/wav/mp3/opus 等） | 音频 URL/Base64（离线）；音频流 + 可选视频帧（实时） |
| **输出格式** | 音频（pcm/wav/mp3/opus） | 结构化文本（含时间戳、逐字标注） | 翻译文本 + 可选合成语音（wav） |
| **流式能力** | 流式文本输入 + 流式音频输出 | 流式音频输入 + 流式文本输出 | 流式音频输入 + 流式文本/音频输出 |
| **多语种** | 中英日韩等 10 种语言 | 中英日粤及多种外语 | 多语种互译，支持自动源语种识别 |
| **支持地域** | 华北2（北京）、新加坡 | 华北2（北京）；Fun-ASR/Qwen-ASR 额外支持新加坡 | 华北2（北京）、新加坡 |

## 接口协议与端点对比

| 维度 | 语音合成 | 语音识别 | 语音翻译 |
|------|---------|---------|---------|
| **HTTP REST** | Qwen-TTS 非实时：MultiModalConversation 接口 | Paraformer 录音文件：异步 RESTful | 离线翻译：OpenAI 兼容 /chat/completions |
| **WebSocket** | Qwen-TTS-Realtime（Realtime API 协议）、CosyVoice/Sambert（run-task 协议） | Fun-ASR/Paraformer（run-task 协议）、Qwen-ASR（Realtime API 协议） | 实时翻译（Realtime 事件协议） |
| **北京端点** | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` 或 `/realtime` | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` 或 `/realtime` | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` 或 WebSocket |
| **鉴权方式** | API Key（Bearer Token） | API Key（Bearer Token） | API Key（Bearer Token） |
| **SDK 支持** | Python、Java | Python、Java、Android、iOS | Python、Java |

## 交互模式对比

| 维度 | 语音合成 | 语音识别 | 语音翻译 |
|------|---------|---------|---------|
| **实时 WebSocket 流程** | 建连 → run-task/session.update → 发送文本（continue-task/append） → 接收音频流 → finish | 建连 → run-task → 持续发送音频二进制流 → 持续接收识别文本 → finish-task | 建连 → session.update → 持续 append 音频 → 监听翻译文本/音频 → session.finish |
| **特色交互模式** | Qwen-TTS-Realtime 支持 ServerCommit/Commit 两种文本提交模式 | Qwen-ASR 支持 VAD（自动断句）和 Manual（手动断句）两种模式 | 支持声音复刻（once/always/never），可附带视频帧用于多模态翻译 |
| **任务管理** | 同一任务内 task_id 保持一致 | 同一任务内 task_id 保持一致 | 基于 session 生命周期管理 |

## 模型选型矩阵

| 场景需求 | 推荐模型 | 类别 | 说明 |
|---------|---------|------|------|
| 短文本离线语音合成 | qwen3-tts-flash | 语音合成 | HTTP 接口，简单易用 |
| 带情感/风格控制的合成 | qwen3-tts-instruct-flash | 语音合成 | 支持指令控制语音风格 |
| 实时对话 TTS（低延迟） | qwen3-tts-flash-realtime | 语音合成 | WebSocket 双工，支持流式文本输入 |
| 流式大段文本合成 | CosyVoice | 语音合成 | continue-task 多段流式输入 |
| 实时会议/对话转写 | fun-asr-realtime | 语音识别 | 低延迟，支持北京+新加坡 |
| 多语种实时识别 | qwen3-asr-flash-realtime | 语音识别 | 支持 VAD/Manual 断句 |
| 长音频批量转写 | paraformer-v2 | 语音识别 | 异步 RESTful，适合离线处理 |
| 整段音视频离线翻译 | qwen3-livetranslate-flash | 语音翻译 | [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，[流式输出](../concepts/streaming.md) |
| 直播/同传实时翻译 | qwen3.5-livetranslate-flash-realtime | 语音翻译 | WebSocket 实时双向，支持声音复刻 |

## 关键差异点

### 输入输出方向

- **语音合成**：单向，文本输入 → 音频输出。开发者提供文本，平台返回合成语音。
- **语音识别**：单向，音频输入 → 文本输出。开发者提供音频流，平台返回转写文本。
- **语音翻译**：可双向输出，音频输入 → 翻译文本 + 可选译后语音。翻译 API 在识别的基础上叠加了翻译和可选的语音合成能力。

### 协议选择

三类 API 均支持 WebSocket 实时协议，但存在两种协议风格：
- **run-task 协议**（传统）：CosyVoice/Sambert 合成、Fun-ASR/Paraformer 识别使用。通过 run-task/continue-task/finish-task 事件驱动。
- **Realtime API 协议**（新一代）：Qwen-TTS-Realtime、Qwen-ASR、语音翻译实时 API 使用。采用 session.update/input_buffer.append/session.finish 事件驱动，模型通过 URL 参数指定。

### 地域限制

Paraformer 实时识别仅支持华北2（北京）地域，不支持新加坡。其他大多数模型同时支持北京和新加坡地域，选型时需注意地域合规要求。

## 适用场景建议

- **智能客服/语音助手**：语音识别（实时 ASR）+ 语音合成（实时 TTS）组合使用，构建完整的语音交互链路。
- **会议纪要/字幕生成**：选择语音识别的实时或录音文件识别模型，按音频时长和时效要求决定实时或离线方案。
- **内容创作/有声读物**：选择语音合成，Qwen-TTS-Instruct 支持情感风格控制，CosyVoice 支持多音色流式合成。
- **跨语言直播/同传**：选择语音翻译实时 API，支持声音复刻和多模态（音频+视频帧）输入，适合低延迟场景。
- **音视频本地化**：选择语音翻译离线 API，输入整段音频/视频 URL，批量完成翻译。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)



