# 语音合成、识别与翻译 API 对比

百炼平台提供了语音合成（TTS）、语音识别（ASR）和语音翻译（Translation）三大类语音 API，覆盖从文本到语音、语音到文本、以及跨语言音视频翻译等场景。三类 API 在接口协议、支持模型、输入输出格式及适用场景上各有差异。本文从开发者技术选型角度，对三者进行系统对比。

## 核心能力对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Translation） |
|------|----------------|----------------|------------------------|
| **核心功能** | 文本 → 语音 | 语音 → 文本 | 语音/视频 → 翻译文本/语音 |
| **模型系列** | Qwen-TTS、CosyVoice、Sambert | Fun-ASR、Paraformer、Qwen-ASR | qwen3-livetranslate-flash 系列 |
| **接口协议** | HTTP REST + WebSocket | WebSocket + RESTful（异步） | OpenAI 兼容 HTTP + WebSocket |
| **流式支持** | [流式输出](../concepts/streaming-output.md)（HTTP）；双工流式（WebSocket） | 实时流式识别（WebSocket） | [流式输出](../concepts/streaming-output.md)（HTTP）；双向事件流（WebSocket） |
| **支持地域** | 华北2（北京）、新加坡 | 华北2（北京）、新加坡（Paraformer 实时仅北京） | 华北2（北京）、新加坡 |
| **SDK 支持** | Python、Java | Python、Java、Android、iOS | Python、Java |
| **音频格式** | pcm、wav、mp3、opus | pcm、wav、mp3、opus、speex、aac、amr | pcm、opus（输入）；pcm（实时输出）；wav（离线输出） |

## 接口协议与交互模式对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Translation） |
|------|----------------|----------------|------------------------|
| **HTTP 接口** | Qwen-TTS 非实时：MultiModalConversation REST API | Paraformer 录音文件：RESTful 异步接口 | 离线翻译：OpenAI 兼容 chat/completions |
| **WebSocket 接口** | Qwen-TTS-Realtime（Realtime API 协议）；CosyVoice / Sambert（run-task 协议） | Fun-ASR / Paraformer 实时（run-task 协议）；Qwen-ASR（Realtime API 协议） | qwen3.5-livetranslate-flash-realtime（事件协议） |
| **WebSocket 端点风格** | Realtime API：URL 含 model 参数；传统：统一 inference 端点 | run-task：统一 inference 端点；Qwen-ASR：URL 含 model 参数 | Realtime API 风格，URL 含 model 参数 |
| **流式交互方式** | 文本输入 → 音频输出 | 音频输入 → 文本输出 | 音频（+视频）输入 → 文本/音频输出 |
| **[异步任务](../concepts/async-task.md)** | 不支持 | 支持（录音文件识别，需 X-DashScope-Async 头） | 不支持 |

## 模型与功能特性对比

| 特性 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Translation） |
|------|----------------|----------------|------------------------|
| **代表模型** | qwen3-tts-flash、cosyvoice-v2 | fun-asr-realtime、paraformer-realtime、qwen3-asr-flash-realtime | qwen3-livetranslate-flash、qwen3.5-livetranslate-flash-realtime |
| **多语种** | 中、英、日、韩等 10 种语言 | 中、英、日、粤语及多种外语 | 多语种互译，支持源语种自动识别 |
| **音色/发音人** | 支持系统音色、声音复刻、声音设计 | — | 支持预设音色、声音复刻（单人/多人模式） |
| **热词/定制** | 语音风格指令（instruct 模型） | 定制热词（vocabulary_id） | 热词表（translation.corpus.phrases） |
| **VAD/断句** | ServerCommit / Commit 两种模式（Realtime） | VAD 断句 / 语义断句 | 自动断句 |
| **视频支持** | 不支持 | 不支持 | 支持视频 URL 输入和实时图像帧 |

## 计费与调用方式

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译（Translation） |
|------|----------------|----------------|------------------------|
| **计费单位** | 按字符数 | 按音频时长 | 按 token 数（含 audio_tokens / text_tokens） |
| **鉴权方式** | API Key（Bearer Token） | API Key（Bearer Token） | API Key（Bearer Token） |
| **[业务空间](../concepts/workspace.md)** | 支持（X-DashScope-WorkSpace） | 支持（X-DashScope-WorkSpace） | 支持（X-DashScope-WorkSpace） |

## 适用场景建议

- **语音合成（TTS）**：适用于智能客服语音播报、有声读物生成、导航语音提示、虚拟主播等需要将文本转化为自然语音的场景。如需低延迟实时交互（如语音对话机器人），优先选择 Qwen-TTS-Realtime；如需高品质音色定制，可选用 CosyVoice；如需大量离线批量合成，Qwen-TTS 非实时接口更合适。

- **语音识别（ASR）**：适用于会议转写、语音搜索、字幕生成、语音指令解析等需要将语音转为文本的场景。实时转写场景推荐 Fun-ASR 或 Qwen-ASR；长音频离线批量处理推荐 Paraformer 录音文件识别。需注意 Paraformer 实时仅支持北京地域。

- **语音翻译（Translation）**：适用于直播同声传译、跨语言视频会议、音视频内容本地化等需要跨语言转换的场景。离线整段翻译选用 qwen3-livetranslate-flash；实时低延迟同传选用 qwen3.5-livetranslate-flash-realtime，后者还支持输入视频帧以提升翻译准确度。

## 技术选型决策参考

1. **只需文本与语音单向转换**：TTS 或 ASR 即可满足，无需翻译 API。
2. **需要跨语言能力**：语音翻译 API 集成了 ASR + 翻译 + 可选 TTS，一站式完成，避免多接口串联。
3. **延迟敏感的实时场景**：三类 API 均提供 WebSocket 实时方案，但协议细节不同——Qwen-TTS-Realtime 和 Qwen-ASR 采用 Realtime API 协议（session 管理 + 事件驱动），CosyVoice/Sambert 和 Fun-ASR/Paraformer 采用 run-task 协议。
4. **移动端接入**：语音识别提供 Android/iOS SDK，语音合成和翻译目前仅 Python/Java SDK，移动端需通过服务端中转。
5. **离线批量处理**：ASR 的 Paraformer 录音文件识别（RESTful 异步）和翻译的离线 HTTP 接口适合大批量任务；TTS 的 HTTP REST 接口同样支持批量调用。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)


