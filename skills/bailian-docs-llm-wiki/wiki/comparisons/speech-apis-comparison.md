# 语音合成、识别与翻译 API 对比

百炼平台围绕语音场景提供三类核心 API：语音合成（TTS）、语音识别（ASR）和语音翻译（Speech Translation）。三者在数据流向、模型家族、交互协议等方面差异显著，开发者需要根据业务场景准确选型。本页从 API 维度系统对比三类能力的关键差异，帮助开发者快速定位适合的接入方案。

## 核心维度对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Speech Translation） |
| --- | --- | --- | --- |
| **数据流向** | 文本 → 音频 | 音频 → 文本 | 音频/视频 → 文本（可选音频） |
| **主要模型族** | Qwen-TTS、CosyVoice、Sambert、MiniMax | Qwen-ASR、Paraformer、Fun-ASR | Qwen-LiveTranslate |
| **非实时协议** | HTTP（DashScope MultiModalConversation / 同步） | DashScope 异步 RESTful（提交-轮询）、OpenAI 兼容同步 | OpenAI 兼容 Chat Completions（流式 SSE） |
| **实时协议** | WebSocket（DashScope 协议） | WebSocket（DashScope 协议 / Realtime 协议） | WebSocket（客户端/服务端事件） |
| **SDK 覆盖** | Python / Java / Android / iOS / HTTP | Python / Java / Android / iOS | Python SDK / Java SDK / HTTP |
| **输入格式** | 纯文本（部分支持 SSML 标记） | PCM / WAV / MP3 / Opus / AMR 等音频 | 音频文件 URL / Base64、视频文件 URL / Base64 |
| **输出格式** | WAV / MP3 / PCM / Opus 音频流 | JSON 结构化文本（含时间戳、词级别） | 增量文本 chunk；可选 WAV 音频输出 |
| **计费单位** | 按字符数计费 | 按音频时长计费 | 按音频/视频时长计费 |
| **典型延迟** | 实时流式首包 < 300ms；非实时视文本长度而定 | 实时流式延迟 < 500ms；录音文件异步数分钟 | 实时毫秒级；非实时视文件时长而定 |

## 接入端点对比

| 地域 | 语音合成 | 语音识别 | 语音翻译 |
| --- | --- | --- | --- |
| **北京（华北 2）HTTP** | `https://dashscope.aliyuncs.com` | `https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| **北京 WebSocket** | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | `wss://dashscope.aliyuncs.com/api-ws/v1/inference`（Paraformer/Fun-ASR）；`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`（Qwen-ASR） | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |
| **新加坡（新版）** | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime` |

> 所有端点统一通过 `Authorization: Bearer <API_KEY>` 鉴权，北京与新加坡的 API Key 不通用，需分别申请。新加坡旧版 `dashscope-intl.aliyuncs.com` 域名即将下线，建议尽快迁移到带 WorkspaceId 的新版域名。

## 模型选型参考

| 场景需求 | 推荐 API | 推荐模型 | 理由 |
| --- | --- | --- | --- |
| 文本转语音播报（离线） | 语音合成 - 非实时 | `qwen3-tts-flash` | 新一代模型，音质好，支持多音色 |
| 交互式对话语音输出 | 语音合成 - 实时 | `qwen3-tts-flash-realtime` / `cosyvoice-v3.5-plus` | 低延迟[流式输出](../concepts/streaming-output.md)，适合对话场景 |
| 自定义音色品牌化 | 语音合成 - 声音复刻 | `voice-enrollment` | 复刻专属音色，品牌一致性 |
| 会议/通话录音转写 | 语音识别 - 录音文件 | `qwen3-asr-flash-filetrans` / `paraformer-v2` | 异步处理，支持长音频，准确率高 |
| 实时字幕/语音输入 | 语音识别 - 实时 | `qwen3-asr-realtime` / `paraformer-realtime-v2` | 流式识别，低延迟 |
| 多语种录音文件翻译 | 语音翻译 - 非实时 | `qwen3-livetranslate-flash` | 支持音频/视频文件，自动检测源语言 |
| 同声传译/实时会议翻译 | 语音翻译 - 实时 | `qwen3.5-livetranslate-flash-realtime` | 毫秒级响应，支持流式音频输入 |

## 协议与交互模式差异

### 语音合成

- **非实时**：单次 HTTP 请求返回完整音频，适合短文本离线生成。Qwen-TTS 使用 MultiModalConversation 接口；MiniMax 使用独立 HTTP 同步接口。
- **实时**：WebSocket 双向通信，客户端分段发送文本，服务端流式返回音频 chunk。CosyVoice 使用 `run-task` / `continue-task` / `finish-task` 事件模型；Qwen-TTS-Realtime 使用 `session.update` / `input_text.append` / `response.create` 事件模型。

### 语音识别

- **录音文件**：异步"提交-轮询"模式。提交音频 URL 后获得 `task_id`，轮询直到状态为 `SUCCEEDED`。Qwen-ASR 额外支持 OpenAI 兼容同步接口（仅短音频）。
- **实时**：WebSocket 流式上传 PCM/Opus 音频帧，服务端增量返回识别结果（含中间结果和最终结果）。

### 语音翻译

- **非实时**：使用 OpenAI 兼容的 Chat Completions 接口，必须开启 `stream: true`，通过 SSE 接收翻译文本增量。支持同时输出翻译音频。
- **实时**：WebSocket 事件驱动，客户端持续发送 `input_audio_buffer.append`，服务端返回翻译文本和可选音频。支持同时传入图像帧用于视频翻译。

## 增强能力对比

| 增强能力 | 语音合成 | 语音识别 | 语音翻译 |
| --- | --- | --- | --- |
| 热词/关键词增强 | 不适用 | 支持（Paraformer / Fun-ASR / Qwen-ASR） | 不支持 |
| 语种自动检测 | 部分支持（需指定 language_type） | 支持（Fun-ASR mtl 多语种模型） | 支持（source_lang 可留空） |
| 时间戳输出 | 不适用 | 支持（句级/词级） | 支持（句级） |
| 说话人分离 | 不适用 | 支持（Paraformer / Fun-ASR） | 不支持 |
| 情感/风格控制 | 支持（Qwen-TTS-Instruct instructions 参数） | 不适用 | 不适用 |
| 自定义音色 | 支持（声音复刻/声音设计） | 不适用 | 支持（输出音频时可选 voice） |
| ITN（逆文本正则化） | 不适用 | 支持 | 不适用 |

## 技术选型建议

1. **明确数据流向**：文本变声音选 TTS，声音变文字选 ASR，跨语言选 Translation。
2. **实时性要求**：对话/直播等低延迟场景选实时 WebSocket 接口；离线批处理选非实时 HTTP/异步接口。
3. **模型家族选择**：新项目优先选 Qwen 系列（qwen3-tts / qwen3-asr / qwen3-livetranslate），架构更新、能力更全；存量系统如已接入 Paraformer / CosyVoice 可继续使用。
4. **SDK vs 原生协议**：Python / Java 项目推荐使用 DashScope SDK 减少协议处理代码；移动端（Android / iOS）TTS 和 ASR 有专用 SDK，翻译暂无移动端 SDK。
5. **地域选择**：国内业务用北京端点；海外业务用新加坡新版域名（带 WorkspaceId），注意 API Key 需分别申请。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)


