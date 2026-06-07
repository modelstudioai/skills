# 语音合成、语音识别与语音翻译 API 对比

百炼平台围绕语音场景提供了三大类 API：语音合成（TTS）、语音识别（ASR）和语音翻译（Speech Translation）。三者均以音频为核心媒介，但数据流向、模型家族和接入协议各有差异。本页从 API 维度对三者做横向对比，帮助开发者根据业务需求快速选型。

## 核心定位对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
| --- | --- | --- | --- |
| **数据流向** | 文本 → 音频 | 音频 → 文本 | 音频/视频 → 文本（可选 + 音频） |
| **主要模型族** | Qwen-TTS、CosyVoice、Sambert、MiniMax | Qwen-ASR、Paraformer、Fun-ASR | Qwen-LiveTranslate |
| **推荐新业务首选** | Qwen-TTS（非实时）/ Qwen-TTS-Realtime | Qwen-ASR（短音频）/ Paraformer-v2（长音频） | qwen3-livetranslate-flash（非实时）/ qwen3.5-livetranslate-flash-realtime（实时） |
| **典型场景** | 播报、有声读物、语音助手、IVR | 会议纪要、字幕生成、语音搜索、客服质检 | 同声传译、跨语言会议、视频字幕翻译 |

## 接入协议与交互形态

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
| --- | --- | --- | --- |
| **非实时 HTTP** | Qwen-TTS（MultiModalConversation）、CosyVoice HTTP、MiniMax HTTP | Qwen-ASR 同步（OpenAI 兼容 / DashScope）、三家族异步提交-轮询 | OpenAI 兼容 Chat Completions（流式 SSE），必须 `stream: true` |
| **实时 WebSocket** | Qwen-TTS-Realtime、CosyVoice WebSocket、Sambert WebSocket | Qwen-ASR-Realtime、Paraformer-Realtime、Fun-ASR-Realtime | Qwen-LiveTranslate Realtime WebSocket |
| **OpenAI 兼容协议** | 不支持 | Qwen-ASR 支持 | 非实时接口使用 OpenAI 兼容协议 |
| **[异步任务](../concepts/async-task.md)模式** | 不支持 | 支持（录音文件识别，提交-轮询） | 不支持 |

## 输入与输出格式

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
| --- | --- | --- | --- |
| **输入** | 纯文本（可附带风格指令） | 音频文件 URL 或实时 PCM/Opus 流 | 音频文件 URL/Base64 或实时音频流；也支持视频输入 |
| **输出** | PCM / WAV / MP3 / Opus 音频流 | 结构化文本（含时间戳、词级别对齐） | 翻译后文本（流式增量）；可选同时输出 WAV 语音 |
| **支持的音频编码** | WAV、MP3、PCM、Opus（因模型而异） | PCM 16-bit、Opus（实时）；异步支持更多容器格式 | 输入 MP3/WAV 等；输出仅 WAV |
| **采样率** | 22050 / 24000 / 48000 Hz（CosyVoice） | 8000 / 16000 Hz（Paraformer）；Qwen-ASR / v2 支持任意采样率 | 取决于输入音频 |

## 服务端点与地域

三类 API 共享相同的地域策略，但域名路径不同：

| 地域 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
| --- | --- | --- | --- |
| **北京（华北 2）** | HTTP: `dashscope.aliyuncs.com`；WS: `wss://dashscope.aliyuncs.com/api-ws/v1/inference` | HTTP: `dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription`；WS: `wss://dashscope.aliyuncs.com/api-ws/v1/inference` 或 `.../realtime` | HTTP: `dashscope.aliyuncs.com/compatible-mode/v1`；WS: `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` |
| **新加坡** | 新版: `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` | 新版同左；旧版: `dashscope-intl.aliyuncs.com`（即将下线） | HTTP: `dashscope-intl.aliyuncs.com/compatible-mode/v1`；WS 新版同左 |
| **API Key** | 北京与新加坡分别申请，不通用 | 同左 | 同左 |

> 三个 API 的新加坡旧版域名 `dashscope-intl.aliyuncs.com` 均计划下线，新接入请统一使用带 WorkspaceId 的新版域名。

## SDK 与客户端支持

| SDK / 客户端 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
| --- | --- | --- | --- |
| **Python** | 支持（全部模型族） | 支持（全部模型族） | 支持（DashScope OmniRealtimeConversation） |
| **Java** | 支持（全部模型族） | 支持（全部模型族） | 支持（DashScope OmniRealtimeConversation） |
| **Android / iOS** | CosyVoice、Sambert 支持 | Paraformer、Fun-ASR 支持 | 不支持 |
| **纯 HTTP** | MiniMax 仅 HTTP；其他可直接调用 | 可直接 RESTful 调用 | 可直接 OpenAI 兼容 HTTP 调用 |

## 增强能力

| 能力 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
| --- | --- | --- | --- |
| **自定义音色** | 声音设计（Voice Design）、声音复刻（Voice Clone） | 不适用 | 支持 voice 参数选择输出音色 |
| **风格/情感控制** | Qwen-TTS-Instruct 支持自然语言指令控制语速、语调 | 不适用 | 不适用 |
| **热词** | 不适用 | 三家族均支持热词增强 | 不适用 |
| **语言检测** | 需手动设 `language_type` | Qwen-ASR 自动检测；Paraformer/Fun-ASR 按模型 | source_lang 可留空自动检测 |
| **时间戳/词对齐** | 不适用 | 支持句级和词级时间戳 | 不适用 |
| **多语种** | 按模型支持中/英/日等 | 按模型支持中/英/日/粤等 | 支持多语种互译，target_lang 必填 |

## 选型建议

- **文本转语音（播报、助手、有声内容）**：选语音合成 API。新业务推荐 Qwen-TTS（离线场景）或 Qwen-TTS-Realtime（交互式低延迟场景）；需要丰富音色库可选 CosyVoice。
- **音频转文字（转写、字幕、质检）**：选语音识别 API。短音频/同步场景用 Qwen-ASR；长音频异步转写用 Paraformer-v2 或 Fun-ASR；实时流式场景三家族均可，推荐 Qwen-ASR-Realtime 或 Paraformer-Realtime-v2。
- **跨语言翻译（同传、视频翻译）**：选语音翻译 API。已录制文件用 qwen3-livetranslate-flash（非实时 OpenAI 兼容）；实时流式场景用 qwen3.5-livetranslate-flash-realtime（WebSocket）。
- **组合场景（如语音转语音翻译）**：可串联 ASR + 翻译，也可直接使用语音翻译 API 的 `modalities: ["text","audio"]` 模式一步到位输出翻译语音。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)


