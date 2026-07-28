# Omni Realtime API 与 Realtime API 使用指南对比

百炼平台提供了两套面向实时[多模态](../concepts/multimodal.md)交互的接入体系：**Omni Realtime API**（Qwen-Omni-Realtime 系列模型的 WebSocket 事件协议接口）和 **Realtime API 使用指南**（覆盖 WebSocket / WebRTC / AOQ 三种传输协议的整体接入方案）。两者定位不同——前者是模型级 API 参考，聚焦事件协议与参数细节；后者是平台级接入指南，聚焦传输协议选型、端侧 SDK 集成与鉴权流程。本页从开发者技术选型角度梳理两者的关键差异与适用场景。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API 使用指南 |
| --- | --- | --- |
| 文档定位 | 模型 API 参考（事件协议、参数、SDK 方法） | 平台接入指南（协议选型、端侧集成、鉴权） |
| 传输协议 | 仅 WebSocket | WebSocket、WebRTC、AOQ（AI over QUIC） |
| 支持模型 | qwen3.5-omni-realtime 系列、qwen3-omni-flash-realtime、qwen-omni-turbo-realtime | 上述模型 + qwen3.5-livetranslate-flash-realtime、multimodal-dialog、FunASR 系列、CosyVoice 系列、qwen-audio-3.0-realtime 等 |
| 输入模态 | 音频（16 kHz PCM）、图像（JPG Base64 ≤256KB）、文本 | 音频、视频流（含摄像头实时画面）、文本 |
| 输出模态 | 文本、音频（24 kHz PCM），可配置 modalities | 文本、音频（内置 Opus 编解码可选） |
| 交互模式 | server_vad / semantic_vad / Manual（手动提交） | WebSocket 支持全部模式；WebRTC 仅支持 VAD 模式 |
| 鉴权方式 | WebSocket 建连时 [API Key](../concepts/api-key.md) 鉴权 | WebSocket/WebRTC 使用 [API Key](../concepts/api-key.md)；AOQ 通过 AppServer 换取临时 [Token](../concepts/token.md)，[API Key](../concepts/api-key.md) 不下发端侧 |
| 端侧 SDK | DashScope Python/Java SDK（OmniRealtimeConversation 类） | [DashScope SDK](../concepts/dashscope-sdk.md)（WebSocket）+ AOQ Client SDK v1.0.1（Android .aar / iOS .framework / HarmonyOS .har） |
| 弱网对抗 | 无（依赖 WebSocket 本身） | WebSocket 差；WebRTC 良好；AOQ 极致 |
| 回声消除/降噪 | 无，需业务侧自行处理 | WebRTC 和 AOQ 内置；WebSocket 无 |
| 工具调用 | 支持（仅 qwen3.5 系列，含 function_call_output 回传流程） | 未涉及工具调用细节，依赖底层模型能力 |
| 联网搜索 | enable_search（仅 qwen3.5 系列，与 tools 互斥） | 未涉及 |
| 声音复刻 | 支持 | 未涉及 |
| 采样参数配置 | 详细（temperature / top_p / top_k / presence_penalty / seed 等，各模型默认值不同） | 未涉及参数细节 |
| 目标平台 | 服务端（Python/Java 后端集成） | 全平台：服务端、浏览器、Android / iOS / HarmonyOS 原生应用 |

## 适用场景建议

### 选择 Omni Realtime API 的场景

- **服务端语音助手 / 电话客服**：后端通过 Python/Java SDK 建立 WebSocket 长连接，精细控制会话参数（VAD 阈值、采样参数、音色）。
- **需要工具调用或联网搜索**：仅 Omni Realtime API 文档描述了完整的 function call 事件流与回传协议。
- **图像+音频[多模态](../concepts/multimodal.md)理解**：需要在对话中发送视频帧截图（Base64 图像）进行实时分析。
- **需要声音复刻**：自定义音色能力仅在此 API 层面有说明。
- **快速原型验证**：单协议（WebSocket）、单 SDK 依赖，上手最快。

### 选择 Realtime API 使用指南的场景

- **浏览器端实时对话**：通过 WebRTC 协议直接在浏览器建立音视频通道，内置回声消除与降噪，无需服务端中转音频流。
- **移动端原生应用（弱网环境）**：AOQ 协议针对移动弱网深度优化，SDK 提供 Android / iOS / HarmonyOS 原生组件，含 Opus 编解码插件。
- **安全合规要求高**：AOQ 方案的 [Token](../concepts/token.md) 鉴权机制确保 [API Key](../concepts/api-key.md) 不暴露到客户端，适合正式发布的 C 端产品。
- **仅需流式 ASR 或 TTS**：FunASR / CosyVoice 系列仅通过 Realtime API 指南中的 WebSocket 方案接入，不属于 Omni Realtime API。
- **实时同传**：qwen3.5-livetranslate-flash-realtime 模型在 Realtime API 指南中有明确的协议支持矩阵。

## 技术选型参考

1. **协议优先级**：移动端弱网 → AOQ；浏览器 → WebRTC；服务端集成/快速原型 → WebSocket。三者共享同一套事件语义（session.created / session.updated 等），切换协议时业务逻辑迁移成本低。
2. **模型选择**：需要工具调用、联网搜索、semantic_vad 等高级能力时，必须选用 qwen3.5-omni-realtime 系列（plus 或 flash）；仅需基础语音对话可考虑 qwen-omni-turbo-realtime（注意其采样参数不可修改）。
3. **鉴权架构**：正式产品建议统一走 AppServer 代理模式——即使使用 WebSocket/WebRTC，也避免在客户端硬编码 [API Key](../concepts/api-key.md)。
4. **音频格式注意**：Omni Realtime API 输入固定 16 kHz PCM、输出固定 24 kHz PCM，不支持自定义采样率；AOQ/WebRTC 方案由 SDK 处理编解码（Opus），开发者无需手动重采样。
5. **组合使用**：两者并非互斥。典型架构为——移动端通过 AOQ SDK 建连（Realtime API 指南），会话内使用 Omni Realtime API 定义的事件协议（session.update、response.create 等）进行交互控制。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../guides/realtime-api-user-guide.md)



