# Omni 实时 API 与实时 API 使用指南对比

百炼平台提供两套实时交互相关的文档体系：**Omni 实时 API**（Qwen-Omni-Realtime）聚焦于全模态实时对话模型的事件协议与 SDK 用法，属于 API 参考层；**Realtime API 使用指南**则从接入方案视角出发，覆盖 WebSocket、WebRTC、AOQ 三种传输协议的选型、鉴权、SDK 集成与接入流程。两者面向的开发决策不同——前者回答"用什么模型、发什么事件"，后者回答"用什么协议连、怎么集成到端侧"。本页从技术选型角度对二者进行关键维度对比。

## 关键维度对比

| 维度 | Omni 实时 API | Realtime API 使用指南 |
|------|--------------|----------------------|
| 文档定位 | API 参考（事件协议、参数、模型能力） | 接入指南（协议选型、鉴权、端侧集成） |
| 传输协议 | WebSocket（DashScope SDK 封装） | WebSocket / WebRTC / AOQ 三选一 |
| 支持模型 | qwen3.5-omni-plus/flash-realtime、qwen3-omni-flash-realtime、qwen-omni-turbo-realtime | 上述全模态模型 + qwen3.5-livetranslate-flash-realtime、multimodal-dialog、FunASR 系列、CosyVoice 系列、qwen-audio-3.0-realtime 等 |
| 输入模态 | 音频（16 kHz PCM）+ 图像（JPG Base64 ≤256KB）+ 文本 | 音频 + 视频流（由端侧 SDK 采集编码） |
| 输出模态 | 文本、音频（24 kHz PCM）或两者组合 | 取决于所选模型/应用类型 |
| 交互模式 | server_vad / semantic_vad / Manual（手动提交） | WebSocket 支持全部模式；WebRTC 仅支持 VAD 模式 |
| 鉴权方式 | API Key（随 WebSocket 建连） | API Key；AOQ 需 AppServer 代理换取临时 Token，Key 不下发端侧 |
| SDK | DashScope Python SDK（≥1.25.17）/ Java SDK | DashScope SDK（WebSocket）；AOQ Client SDK v1.0.1（Android .aar / iOS .framework / HarmonyOS .har）；WebRTC 使用浏览器原生 API |
| 弱网对抗 | 无（WebSocket 层面） | WebSocket 差 / WebRTC 良好 / AOQ 极致 |
| 回声消除与降噪 | 无，需业务自行处理 | WebRTC 和 AOQ 内置 |
| 高级能力 | 工具调用（tools）、联网搜索（enable_search）、语义 VAD、静默引导（idle_timeout_ms）、声音复刻、输入转录（含语言/情绪识别） | 侧重连接层能力：媒体门控、SDP 交换、Token 鉴权流程 |
| 端侧平台 | 全平台（任何支持 WebSocket 的环境） | WebSocket 全平台；WebRTC 浏览器/移动端；AOQ 仅 Android / iOS / HarmonyOS |

## 适用场景建议

### 选择 Omni 实时 API 文档的场景

- **服务端语音助手 / 电话客服**：通过 Python/Java SDK 在服务端建立 WebSocket 连接，精细控制事件流（如工具调用、联网搜索）。
- **需要图像理解的[多模态](../concepts/multimodal.md)对话**：需发送视频帧/图像并结合语音交互（如实时视频问答），Omni API 提供 `input_image_buffer.append` 等图像事件。
- **需要 Manual 模式（按下即说）**：WebRTC 协议不支持手动模式，若业务需要显式控制响应触发，应使用 WebSocket + Omni 实时 API。
- **需要工具调用或联网搜索**：仅 Qwen3.5-Omni-Realtime 系列通过 Omni API 的 `tools` / `enable_search` 参数支持。

### 选择 Realtime API 使用指南的场景

- **浏览器端实时对话**：使用 WebRTC 协议，利用内置回声消除和降噪，无需自建音频前处理管线。
- **移动端原生应用（弱网环境）**：AOQ 协议提供极致弱网对抗，适合户外、地铁等网络不稳定场景；但需部署 AppServer 做 Token 代理。
- **仅需 ASR 或 TTS 单能力**：FunASR（实时语音识别）和 CosyVoice（实时语音合成）仅通过 WebSocket 协议接入，参见使用指南的模型支持表。
- **已有 RTC 基础设施**：团队已有 WebRTC 媒体服务器或 SFU 架构，可直接复用现有管线。

## 技术选型决策参考

1. **确定模型需求**：若需要全模态（音频+图像+文本）对话能力，核心模型为 qwen3.5-omni 系列，两套文档均覆盖；若仅需 ASR/TTS，只看使用指南。
2. **确定部署形态**：纯服务端 → WebSocket + Omni API 事件协议；浏览器 → WebRTC；移动原生 → AOQ。
3. **确定交互模式**：需要 Manual 模式或工具调用 → 必须走 WebSocket（Omni API 协议层）；仅 VAD 自动对话 → 三种协议均可。
4. **确定音频前处理责任**：WebSocket 方案需业务自行实现回声消除与降噪；WebRTC/AOQ 内置该能力。
5. **安全合规**：移动端产品不应在客户端持有 API Key，AOQ 的 AppServer Token 代理模式是推荐做法；WebSocket/WebRTC 方案需自行在服务端代理建连请求。

两套文档互为补充：使用指南解决"怎么连"，Omni 实时 API 参考解决"连上之后说什么"。实际项目中通常需要同时参考两者——先按使用指南完成协议选型与建连，再按 Omni API 事件协议实现业务逻辑。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../guides/realtime-api-user-guide.md)


