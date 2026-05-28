# 语音合成、识别与翻译对比

在构建端到端语音交互、多语言音视频处理或智能客服系统时，开发者常需在阿里云百炼平台的语音能力矩阵中进行技术选型。本文档旨在清晰对比 **语音合成（TTS）**、**语音识别（ASR）** 与 **语音翻译（Speech Translation）** 三大核心服务在协议栈、模型能力、数据流向及适用边界上的差异，为开发者在架构设计、API 选型与 SDK 集成时提供明确的决策参考。详细接口规范请参阅对应主题页：[[语音合成API参考]]、[[语音识别API参考]] 与 [[语音翻译API参考]]。

## 核心维度对比矩阵

| 对比维度 | 语音合成 (TTS) | 语音识别 (ASR) | 语音翻译 (STT) |
|:---|:---|:---|:---|
| **输入格式** | 纯文本或 `[[SSML标记语言]]`（单请求通常 ≤20,000 字符） | 实时二进制音频流（PCM/Opus）或 公网 `HTTP(S)` 音频 URL | 实时 PCM 流（支持搭配 `JPG` 图像）或 音视频公网 URL |
| **输出格式** | 音频帧流（PCM/WAV/MP3/Opus），支持字级时间戳 | 文本转写结果（含标点、时间戳、说话人分离标签、情感识别） | 强制[[streaming-output|流式输出]]译文；可选同步返回目标语言音频流（默认 WAV/PCM） |
| **支持核心模型** | CosyVoice 系列、Qwen-TTS 系列、Sambert 系列、MiniMax 系列 | Qwen-ASR、Paraformer、Fun-ASR | `qwen3-livetranslate-flash`、`qwen3.5-livetranslate-flash-realtime` |
| **API 端点/协议** | HTTP 同步/SSE / 实时 WebSocket / `[[dashscope-sdk]]` 统一封装 | WebSocket 实时流 / RESTful HTTP 异步任务 / OpenAI 兼容 (`/chat/completions`) | WebSocket 实时接口 (`wss://.../realtime`) / OpenAI 兼容 HTTP 接口 |
| **计费方式** | 按调用次数、生成音频时长或模型 Token 计费（以控制台为准） | 按音频处理时长、任务数或实时并发路数计费（以控制台为准） | 按输入时长/调用次数、输出模态（文本/音频）计费（以控制台为准） |
| **典型场景** | 智能播报、有声读物、数字人驱动、个性化语音助手回复 | 会议纪要转写、语音指令控制、直播实时字幕、长录音文件归档 | 同声传译硬件、跨国多语言会议、海外视频内容本地化、交互式翻译 App |

---

## 🎯 各方案适用场景与选型建议

### 📢 语音合成 (TTS)
| 业务诉求 | 推荐方案 | 关键技术要点 |
|:---|:---|:---|
| **低延迟实时对话 / 语音助手** | `CosyVoice` 或 `Qwen-TTS Realtime` | 使用 WebSocket 长连接，支持 `server_commit`/`client_commit` 双模式。首字包延迟可压至 <300ms，适配双向语音交互。 |
| **高稳定性播报 / 资讯导航** | `Sambert 系列` 或 `Qwen-TTS 非实时` | 单向[[streaming-output|流式输出]]，支持 `word_timestamp_enabled` 获取精准对齐时间戳。Sambert 仅限北京地域，适合对稳定性要求极高的生产播报。 |
| **品牌定制音色 / 数字人驱动** | `[[声音设计]]` / `[[声音复刻]]` | 获取专属 `voice_id`。**注意**：定制音色必须与创建时的 `target_model` 严格绑定，跨模型请求将被拒绝。 |
| **精细化发音与情感控制** | 全模型（推荐 Qwen/CosyVoice） | 开启 `enable_ssml` 解析 `[[SSML标记语言]]`，支持调节 `pitch`、`rate`、`volume`，并注入停顿、多音字及情感标签。 |

### 🎙️ 语音识别 (ASR)
| 业务诉求 | 推荐方案 | 关键技术要点 |
|:---|:---|:---|
| **实时语音交互 / 智能终端** | `Qwen-ASR` 或 `Paraformer` 实时流 | 配置 `turn_detection: "server_vad"` 实现服务端自动断句。支持 Manual 模式由客户端精确控制语句边界。 |
| **海量录音归档 / 会议分析** | `Fun-ASR` 或 `Paraformer` 异步文件转写 | 严格遵循异步任务队列流程（`PENDING → RUNNING → SUCCEEDED`）。开启 `diarization_enabled` 可分离发言人（建议 ≤2 小时/文件）。 |
| **垂类领域术语优化** | Paraformer / Qwen-ASR | 通过 `[[custom-hot-words]]` 创建热词词表并传入 `vocabulary_id`，显著提升医疗、金融、法律等场景下的专有名词召回率。 |
| **存量 LLM 代码无缝迁移** | [[openai-compatible-api|OpenAI 兼容接口]] | 复用 `/chat/completions` 端点，将音频封装为 `input_audio` 消息体，设置 `stream: true` 即可兼容现有流式解析逻辑。 |

### 🌍 语音翻译 (Speech Translation)
| 业务诉求 | 推荐方案 | 关键技术要点 |
|:---|:---|:---|
| **离线文件/视频翻译流水线** | OpenAI 兼容 HTTP 接口 | 传入音视频公网 URL，配置 `modalities: ["text", "audio"]` 获取译文与配音。`stream` 强制为 `true`，适用于内容出海本地化。 |
| **实时同传设备 / 移动端交互** | `qwen3.5-livetranslate-flash-realtime` | 必须使用 WebSocket 接口。通过 `session.update` 动态下发 `translation` 配置与热词映射 (`corpus`)，实现毫秒级低延迟流式同传。 |
| **原文对照与音色克隆输出** | 实时接口 + 转录/克隆配置 | 设置 `input_audio_transcription` 同步获取源语言识别结果；结合 `[[voice-cloning-api]]` 开启 `enable_voice_clone`，译文输出可保留原说话人音色特征。 |

---

## ⚠️ 开发者集成关键注意事项

1. **地域与鉴权严格隔离**  
   中国内地（北京）与国际版（新加坡）的 API 端点、WebSocket 地址及 `[[api-key-management]]` 互不通用。初始化 SDK 或构造请求前，务必通过 `base_url` 显式指定路由，混用将直接触发鉴权失败。
2. **流式生命周期强制管理**  
   所有 WebSocket 双向流式服务（TTS/ASR/STT）均要求客户端在音频/文本发送完毕后，**必须显式发送结束指令**（如 `finish-task`、`session.finish` 或 SDK 的 `endSession()`/`streaming_complete()`）。否则服务端无法输出尾部数据，并可能导致连接挂起或内存泄漏。
3. **音频输入硬性约束**  
   * ASR/STT **不支持**本地文件直传或 Base64 编码。SDK 调用时**不支持** `oss://` 协议，必须使用公网可访问的 `http(s)://` URL。
   * 实时流输入默认要求 `16kHz 16bit PCM`。STT 图像输入仅限 JPG（单张 ≤500KB，≤2 FPS），且**必须在发送过至少一次音频流后**才允许追加图像事件。
4. **参数传递规范差异**  
   * 语音翻译的非标准参数（如 `translation_options`）在 Python OpenAI SDK 中必须置于 `extra_body` 对象内传递；原生 HTTP 或 Node.js SDK 需平铺至请求顶层。
   * ASR 情感识别（仅限 `paraformer-realtime-8k-v2`）需显式关闭语义断句（`semantic_punctuation_enabled=false`），否则标签将无法返回。
5. **SDK 版本演进提示**  
   百炼官方 Python/Java SDK 正持续收敛命名空间至 `dashscope.audio` 或 `MultiModalConversation`。历史独立调用方式（如旧版 `SpeechSynthesizer.call()`）可能在新版本中被标记为 `Deprecated`。强烈建议业务侧直接接入 `[[dashscope-sdk]]`，利用其内置的自动鉴权、连接复用、断线重连与流拼接能力，大幅降低工程维护成本。

## 被对比主题页

- [[speech-synthesis-api-reference|speech synthesis api reference]] — `../api/speech-synthesis-api-reference.md`
- [[speech-recognition-api-reference|speech recognition api reference]] — `../api/speech-recognition-api-reference.md`
- [[speech-translation-api-reference|speech translation api reference]] — `../api/speech-translation-api-reference.md`

