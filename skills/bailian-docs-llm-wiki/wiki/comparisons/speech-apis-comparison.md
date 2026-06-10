# 语音合成、语音识别与语音翻译对比

百炼平台围绕语音提供三大类 API：语音合成（TTS）将文本转为语音，语音识别（ASR）将语音转为文本，语音翻译则在识别的基础上叠加跨语种翻译能力。三者在输入输出、协议、模型选择和典型场景上存在显著差异，本文从技术选型角度进行系统对比，帮助开发者根据业务需求选择合适的 API。

## 核心维度对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 语音翻译 |
| --- | --- | --- | --- |
| **功能方向** | 文本 → 语音 | 语音 → 文本 | 语音 → 翻译文本（可选输出音频） |
| **输入格式** | 纯文本（支持指令控制语速、情绪等） | 音频流（PCM/WAV/MP3/OPUS 等）或音频文件 URL | 音频流（PCM/OPUS）或音频/视频文件 URL |
| **输出格式** | 音频流（PCM/WAV/MP3 等） | 结构化文本（含时间戳、逐字信息） | 翻译文本 + 可选音频（WAV） |
| **主要协议** | HTTP（非实时）/ WebSocket（实时流式） | WebSocket（实时）/ RESTful（录音文件异步） | OpenAI 兼容 HTTP（离线）/ WebSocket（实时） |
| **代表模型** | Qwen-TTS、CosyVoice、Sambert、MiniMax Speech | Fun-ASR、Paraformer、Qwen-ASR | qwen3-livetranslate-flash、qwen3.5-livetranslate-flash-realtime |
| **支持地域** | 北京、新加坡（Sambert 仅北京） | 北京、新加坡（Paraformer 实时仅北京） | 北京、新加坡 |
| **鉴权方式** | DashScope API Key（Bearer Token） | DashScope API Key（Bearer Token） | DashScope API Key（Bearer Token） |
| **多语种支持** | 中文、英文等（因模型而异） | 中文、英文、日语、粤语及多种外语 | 多语种，支持自动语种识别 |

## 模型系列与协议对比

| API 类型 | 模型系列 | 协议 | 实时/离线 | 流式能力 |
| --- | --- | --- | --- | --- |
| 语音合成 | Qwen-TTS（非实时） | HTTP | 离线 | 支持[流式输出](../concepts/streaming.md) |
| 语音合成 | Qwen-TTS Realtime | WebSocket | 实时 | 流式文本输入 + 流式音频输出 |
| 语音合成 | CosyVoice | WebSocket | 实时 | 三段式事件协议，流式文本输入 |
| 语音合成 | Sambert | WebSocket | 实时 | 一次性文本输入，流式音频输出 |
| 语音合成 | MiniMax Speech | HTTP | 同步/流式 | 支持[流式输出](../concepts/streaming.md) |
| 语音识别 | Fun-ASR / Paraformer 实时 | WebSocket | 实时 | 流式音频输入 + 实时文本输出 |
| 语音识别 | Qwen-ASR | WebSocket | 实时 | 流式音频输入，支持 VAD/Manual 断句 |
| 语音识别 | Paraformer 录音文件 | RESTful | 离线异步 | 提交任务 + 轮询结果 |
| 语音翻译 | qwen3-livetranslate-flash | OpenAI 兼容 HTTP | 离线 | 仅[流式输出](../concepts/streaming.md)（stream 必须为 true） |
| 语音翻译 | qwen3.5-livetranslate-flash-realtime | WebSocket | 实时 | 双向事件流 |

## 交互协议对比

| 特性 | 语音合成 | 语音识别 | 语音翻译 |
| --- | --- | --- | --- |
| **WebSocket 事件模型** | run-task / continue-task / finish-task（CosyVoice）；session 事件协议（Qwen-TTS Realtime） | run-task / finish-task | session.update / input_audio_buffer.append / session.finish |
| **HTTP 接口风格** | DashScope MultiModalConversation（Qwen-TTS）；OpenAI 兼容（MiniMax） | RESTful [异步任务](../concepts/async-task.md)（Paraformer 录音文件） | OpenAI 兼容 chat/completions |
| **连接复用** | 支持（CosyVoice 建议复用连接处理多任务） | 支持 | 支持 |
| **心跳保活** | 视模型而定 | 支持（heartbeat 参数避免静音超时断连） | 无需（持续发送音频数据） |

## 特色能力对比

| 能力 | 语音合成 | 语音识别 | 语音翻译 |
| --- | --- | --- | --- |
| **音色定制** | 支持（多音色库 + 声音复刻） | 不适用 | 支持预设音色与声音复刻 |
| **情绪/语调控制** | Qwen-TTS instruct 模型支持自然语言指令；MiniMax 支持情绪标签 | 不适用 | 不适用 |
| **热词定制** | 不适用 | 支持（vocabulary_id） | 支持（translation.corpus.phrases） |
| **语义断句** | 不适用 | 支持（semantic_punctuation_enabled） | 不适用 |
| **时间戳输出** | 不适用 | 支持（逐字时间戳 + 句级时间戳） | 不适用 |
| **视频输入** | 不适用 | 不适用 | 实时翻译支持图像帧输入 |
| **ASR + 翻译联合** | 不适用 | 不适用 | 可同时返回源语言 ASR 结果与翻译文本 |

## 适用场景建议

**选择语音合成（TTS）的场景：**

- 智能客服、语音播报、有声读物等需要将文本转为自然语音的应用
- 需要精细控制语速、语调、情绪的交互式对话场景（推荐 Qwen-TTS instruct 或 CosyVoice）
- 批量离线音频生成（推荐 Qwen-TTS 非实时或 MiniMax HTTP 接口）
- 需要低延迟实时语音输出的场景（推荐 Qwen-TTS Realtime 或 CosyVoice）

**选择语音识别（ASR）的场景：**

- 实时会议转写、直播字幕、语音输入法等需要低延迟的实时转写场景（推荐 Fun-ASR 或 Qwen-ASR）
- 长音频离线批量转写，如录音回放、客服质检（推荐 Paraformer 录音文件识别）
- 需要多语种支持或精细 VAD 控制的场景（推荐 Qwen-ASR，支持 VAD/Manual 两种断句模式）

**选择语音翻译的场景：**

- 直播同声传译、跨语种实时会议等低延迟翻译场景（推荐 qwen3.5-livetranslate-flash-realtime）
- 整段音视频的离线翻译与字幕生成（推荐 qwen3-livetranslate-flash）
- 需要翻译文本与翻译语音同时输出的场景
- 视频会议中需要结合画面理解辅助翻译的场景（实时翻译支持视频帧输入）

## 技术选型决策参考

1. **明确数据流向**：文本到语音选 TTS，语音到文本选 ASR，语音到另一语言选语音翻译。
2. **实时性要求**：需要低延迟流式处理选 WebSocket 协议的实时模型；可接受延迟选 HTTP/RESTful 离线接口。
3. **地域合规**：部分模型仅支持北京地域（如 Sambert、Paraformer 实时），海外部署需确认新加坡地域的模型可用性。
4. **组合使用**：语音翻译内置了 ASR 能力，无需单独调用 ASR 再翻译；但如果只需转写不需翻译，直接使用 ASR 更高效。TTS 可与 ASR 或语音翻译搭配，实现完整的语音交互链路。

## 被对比主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)


