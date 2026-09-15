# 实时API方案对比：Omni Realtime API vs Realtime API用户指南

本对比旨在帮助开发者清晰理解百炼平台当前两大实时交互接口的技术定位、能力边界与适用约束，避免因协议误选、模型不兼容或功能错配导致集成失败或体验降级。Omni Realtime API 是面向**极致低延迟多模态对话**的专用 WebSocket 接口；而 Realtime API 是覆盖更广场景的**统一实时接入层**，通过 AOQ/WebRTC/WebSocket 三协议抽象，兼顾终端适配性、安全合规性与能力扩展性。二者并非简单替代关系，而是分层协作：Omni Realtime API 可视为 Realtime API 在 WebSocket 协议下针对 Qwen-Omni 系列模型的深度优化子集，而 Realtime API 提供跨协议一致的抽象、企业级鉴权与全栈能力支持（如 ASR/TTS/翻译等）。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API 用户指南 |
|------|-------------------|------------------------|
| **核心定位** | 专为 Qwen-Omni 系列模型设计的**轻量、高响应、事件驱动型 WebSocket 接口**，聚焦语音助手、智能客服等强交互对话场景。 | 百炼平台统一的**实时能力接入层**，提供 AOQ/WebRTC/WebSocket 三协议支持，覆盖对话、ASR、TTS、翻译、音视频通话等全栈实时能力。 |
| **传输协议** | **仅 WebSocket**（`wss://.../api-ws/v1/realtime`） | **AOQ（推荐移动端/弱网）、WebRTC（推荐浏览器音视频通话）、WebSocket（推荐服务端集成/快速验证）**，需通过 `x-dashscope-rtc-transport` Header 显式指定。 |
| **输入格式** | 支持 `pcm`（裸 PCM）和 `wav`（WAV 封装），采样率支持 `8000/16000/24000/48000 Hz`；通过 `audio.input.format` 配置。 | **当前仅支持 `pcm` 格式**（文档明确限定），采样率未公开说明，默认与模型要求对齐（通常为 16000 Hz）。 |
| **输出格式** | 支持 `pcm` 和 `wav`，采样率同输入；可动态配置 `audio.output.format`；默认同时输出 `text` + `audio`。 | **当前仅支持 `pcm` 输出格式**；`modalities` 控制是否返回 `audio`，但格式不可选。 |
| **支持模型** | 仅限 Qwen-Omni 系列实时模型：<br>• `qwen3.5-omni-plus-realtime`<br>• `qwen3.5-omni-flash-realtime`<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime`<br>（`qwen3.5-omni-realtime` 系列独占 `semantic_vad`/`enable_search`/完整工具调用） | **全模型谱系支持**：<br>• 全模态：`qwen3.5-omni-plus/flash-realtime`<br>• 语音翻译：`qwen3.5-livetranslate-flash-realtime`<br>• ASR：`Qwen-Audio-3.0-ASR-Flash-Streaming` 等（**AOQ/WebSocket 支持，WebRTC 不支持**）<br>• TTS：`CosyVoice`/`qwen-audio-3.0-tts-*`（**AOQ/WebSocket 支持，WebRTC 不支持**）<br>• 对话：`qwen-audio-3.0-realtime-plus/flash` |
| **语音活动检测（VAD）** | 支持双模式：<br>• `server_vad`（声学特征，全系列支持）<br>• `semantic_vad`（语义有效性，**仅 `qwen3.5-omni-realtime` 系列支持**） | 仅支持 `server_vad`（声学 VAD），无语义级 VAD 能力；配置方式与 Omni 一致（`turn_detection` 对象）。 |
| **工具调用与联网搜索** | ✅ 完整支持：<br>• 工具调用（`tools` 参数）<br>• 联网搜索（`enable_search`，与 `tools` 互斥，仅 `qwen3.5-omni-realtime` 系列支持） | ❌ **不支持**：Realtime API 当前未开放工具调用与联网搜索能力，所有函数执行需由客户端或服务端前置处理。 |
| **声音复刻集成** | ✅ 原生支持：可直接在 `voice` 参数中传入通过 `qwen-voice-enrollment` 创建的自定义音色 ID，**要求音色模型与调用模型严格一致**。 | ⚠️ **有限支持**：需通过 AOQ SDK 的自定义音频播放路径（`setAudioFrameObserver`）接收 PCM 后，由客户端调用独立的声音复刻服务合成并注入；无原生 `voice` 参数映射。 |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.{Region}.maas.aliyuncs.com/api-ws/v1/realtime` | 动态端点，由鉴权服务返回：<br>• AOQ：`aoqTokenForClient` + Relay 地址<br>• WebRTC：`webrtcToken` + SFU 地址<br>• WebSocket：`wss://.../api-ws/v1/realtime`（与 Omni 相同，但协议行为不同） |
| **计费方式** | 按 **实际消耗的 token 数（输入+输出） + 音频时长（秒）** 计费；语音转录（`enable_input_audio_transcription`）单独计费。 | 按 **模型调用次数 + 音频时长（秒） + ASR/TTS 字数（如启用）** 计费；不同协议、不同模型单价独立；AOQ/WebRTC 的信令与媒体流调度不额外计费。 |
| **典型场景** | • 语音助手（手机/车机/硬件）<br>• 低延迟智能客服坐席辅助<br>• 实时音视频会议中的 AI 旁听与摘要<br>• 需要语义 VAD 或联网搜索的对话机器人 | • 跨平台音视频 App（Web/Android/iOS/HarmonyOS）<br>• 弱网环境下的移动语音交互（AOQ）<br>• 浏览器内嵌实时翻译/字幕（WebRTC）<br>• 服务端批量 ASR/TTS 处理（WebSocket）<br>• 多模态对话 + 独立 ASR/TTS 流水线编排 |

## 适用场景建议

### 选择 Omni Realtime API，当您：
- ✅ **已确定使用 Qwen-Omni 系列模型**，且业务强依赖其 `semantic_vad`、`enable_search` 或完整工具调用能力；
- ✅ 客户端具备 WebSocket 连接能力（如 Node.js 服务、Electron 桌面应用、支持 WebSocket 的移动端 SDK），且网络环境稳定；
- ✅ 追求**最低端到端延迟**（典型 <300ms），无需跨协议兼容性，可接受单协议技术栈；
- ✅ 需要灵活控制音频格式（如直接输出 `wav` 供前端播放，或 `48kHz` 高保真音频）；
- ✅ 已完成声音复刻音色训练，并希望在实时对话中**一键切换音色**（`voice: "MyCustomVoice"`）。

### 选择 Realtime API，当您：
- ✅ **需支持多终端、多网络环境**：例如同一产品需覆盖 Web（WebRTC）、iOS（AOQ）、Android（AOQ）及后台服务（WebSocket）；
- ✅ **业务涉及 ASR 或 TTS 独立能力**（如录音转文字、文本转语音播报），且必须与对话模型解耦或混用；
- ✅ **对安全性与合规性要求严格**：需通过服务端代理鉴权（AOQ 的 `aoqTokenForClient` 机制），杜绝 `API_KEY` 泄露风险；
- ✅ **需深度定制音视频流**：如接入第三方麦克风/摄像头、自定义音频处理（降噪/混音）、将 TTS 输出直连扬声器、或叠加视频画面；
- ✅ **项目处于早期验证阶段**，需快速在浏览器中用 WebRTC 搭建原型，或在弱网下测试移动端鲁棒性。

## 技术选型参考（致开发者）

| 选型考量 | 推荐方案 | 说明 |
|----------|-----------|------|
| **模型锁定 Qwen-Omni 且需语义 VAD/搜索/工具** | ✅ Omni Realtime API | Realtime API 当前不支持这些高级能力，Omni 是唯一选择。 |
| **需同时调用 ASR + Omni 对话 + TTS** | ✅ Realtime API（WebSocket 协议） | 可在同一连接中按需切换模型（如先 ASR，再对话，再 TTS），Omni API 无法调用 ASR/TTS 模型。 |
| **Web 应用，需原生浏览器音视频通话** | ✅ Realtime API（WebRTC 协议） | Omni 不支持 WebRTC；WebRTC 提供 NAT 穿透、回声消除等浏览器原生能力。 |
| **移动端 App，弱网/高丢包环境** | ✅ Realtime API（AOQ 协议） | AOQ 基于 QUIC 优化，抗丢包能力强；Omni 的 WebSocket 在弱网下易断连。 |
| **服务端集成，快速验证模型效果** | ⚖️ 两者均可，推荐 Omni Realtime API | Omni 接口更简洁（纯 WebSocket + JSON 事件），无鉴权代理开销；Realtime WebSocket 协议行为更复杂（需处理 Token 获取、Relay 调度）。 |
| **已有成熟 WebSocket 客户端，仅需升级模型** | ✅ Omni Realtime API | 兼容性好，事件模型一致，参数迁移成本低。 |
| **需满足等保/密评要求，禁止客户端持有长期凭证** | ✅ Realtime API（AOQ/WebRTC） | 强制服务端鉴权，客户端仅持短期 Token；Omni 要求客户端管理 `API_KEY`（不推荐）。 |

> **重要提醒**：  
> - **不要混合使用**：Omni Realtime API 与 Realtime API 的 WebSocket 端点虽地址相似，但事件结构、状态机、错误码完全不兼容，不可共用 SDK 或客户端逻辑。  
> - **版本演进关注点**：Omni Realtime API 未来将向 Realtime API 的协议抽象层收敛；当前差异是阶段性能力分层，非长期割裂。建议新项目优先评估 Realtime API 的三协议能力矩阵，再按需选用子集。  
> - **调试建议**：Omni 推荐使用 `wscat` 或 Python SDK 快速抓包；Realtime API 推荐使用官方 AOQ/WebRTC SDK 内置日志，因其包含信令、媒体、模型三层上下文，便于定位跨协议问题。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


