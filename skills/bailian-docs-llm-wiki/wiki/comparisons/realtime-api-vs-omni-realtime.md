# 实时 API 与 Omni Realtime API 对比

百炼平台中的“实时 API”与“Omni Realtime API”都面向低延迟语音、视频和[多模态](../concepts/multimodal.md)交互，但两者定位层级不同：实时 API 更像一套实时交互接入方案，覆盖 WebSocket、WebRTC、AOQ 等多种传输协议与多类实时模型；Omni Realtime API 则是其中面向 Qwen-Omni-Realtime 模型的事件驱动 WebSocket 接口规范，重点描述会话参数、客户端事件、服务端事件和模型交互流程。开发者选型时，应先判断业务需要的是“端到端接入通道与端侧能力”，还是“直接控制 Omni 实时模型的消息协议”。

## 关键维度对比

| 维度 | 实时 API | Omni Realtime API | 选型提示 |
|---|---|---|---|
| 定位 | 面向实时交互场景的总体接入方案，覆盖多协议、多端侧和多模型类型 | 面向 Qwen-Omni-Realtime 系列模型的实时[多模态](../concepts/multimodal.md)对话 API | 若需要选择接入协议、端侧 SDK 或弱网方案，优先看实时 API；若已确定使用 Omni 实时模型并需要事件协议细节，查看 Omni Realtime API |
| 传输协议 | 支持 WebSocket、WebRTC、AOQ 三类接入方式 | 主要基于 WebSocket 长连接的事件驱动协议 | 浏览器/移动端实时媒体链路可考虑 WebRTC/AOQ；服务端直接对接模型事件流可使用 Omni Realtime API |
| 端侧适配 | WebSocket 适合全平台服务端集成；WebRTC 适合浏览器和已有 RTC 基础设施；AOQ 适合 Android、iOS、HarmonyOS 等移动端原生应用 | 更偏向客户端或服务端按事件协议发送音频、图像、会话配置和响应控制事件 | 需要端侧 SDK、媒体采集播放、回声消除、降噪和弱网对抗时，实时 API 的 WebRTC/AOQ 更完整 |
| 输入格式 | 取决于协议和模型类型，可覆盖音频、视频、[多模态](../concepts/multimodal.md)输入，以及 FunASR、CosyVoice、音频对话等实时能力 | 通过事件提交输入，典型包括 `input_audio_buffer.append`、`input_image_buffer.append`、`session.update` 等；音频输入固定为 16 kHz 单声道 PCM | 若需要精细控制音频缓冲区、图片输入、会话参数和轮次提交，Omni Realtime API 更直接 |
| 输出格式 | 取决于所选协议和模型；可通过媒体流、DataChannel 或 WebSocket 事件获得模型响应 | 服务端返回事件，如 `response.audio.delta`、`response.audio_transcript.delta`、转录增量、工具调用参数和 `response.done` | 需要逐事件处理转录、音频增量、工具调用和错误信息时，Omni Realtime API 的事件模型更清晰 |
| 支持模型 | 覆盖 qwen3.5-omni 实时全模态、livetranslate、多模态开发套件、FunASR、CosyVoice、qwen-audio 实时语音对话等 | 聚焦 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime` 等 Omni 实时模型 | 如果业务不只用 Omni 模型，还涉及 ASR、TTS、实时翻译或音频对话，应从实时 API 的支持矩阵开始选型 |
| API 端点 | WebRTC/AOQ 常见端点形态为 `https://{endpoint}/api/v1/webrtc/realtime?model=<模型名>`；WebSocket 走对应 DashScope 接入 | 通过 WebSocket 长连接与事件协议交互，围绕会话、音频缓冲区、响应和对话项事件展开 | 端点与建连方式随协议不同而变化，接入前需确认目标协议和模型是否兼容 |
| 鉴权方式 | 三种协议均使用 [API Key](../concepts/api-key.md) 建连鉴权；AOQ 推荐 AppServer 使用 [API Key](../concepts/api-key.md) 换取临时 Token 下发给客户端 | 通常通过 [API Key](../concepts/api-key.md) 建立 WebSocket 连接，后续在连接内用事件更新会话 | 端侧应用尤其应避免将 API Key 写入客户端；移动端原生场景优先采用 AOQ 的临时 Token 模式 |
| 会话控制 | WebRTC 有媒体门控和 `session.created` 后恢复媒体发送等要求；AOQ 建连前需关闭媒体发送，`session.updated` 后再开启 | 通过 `session.update` 配置 `modalities`、`voice`、`turn_detection`、`tools`、`enable_search`、采样参数等 | 需要大量动态调整模型行为、VAD、工具或联网搜索时，应重点参考 Omni Realtime API 的会话参数 |
| VAD / 手动模式 | WebRTC 仅支持 VAD 模式；不同协议对媒体提交方式有差异 | 支持 `server_vad`、部分模型支持 `semantic_vad`；`turn_detection: null` 可启用 Manual 模式 | “按下即说”等明确轮次控制场景更适合使用支持 Manual 模式的 Omni Realtime API WebSocket 事件协议 |
| 工具调用与联网搜索 | 实时 API 作为接入方案层面描述较少，具体能力取决于模型和 API | 支持 Function Calling、联网搜索等；`tools` 与 `enable_search` 互斥 | 如果业务需要工具调用闭环、回传 `function_call_output`，应按 Omni Realtime API 的事件流程实现 |
| 弱网、回声消除、降噪 | WebSocket 弱网能力较弱且无内置 AEC/降噪；WebRTC 良好且内置；AOQ 弱网对抗最强且内置 | API 侧主要定义事件交互，端侧音频处理与网络对抗能力不作为核心协议能力 | 移动端语音/视频通话、复杂网络环境或需要内置音频处理时，优先选择实时 API 的 AOQ/WebRTC 方案 |
| SDK 与集成复杂度 | WebSocket 可用 [DashScope SDK](../concepts/dashscope-sdk.md)；AOQ 需集成 Android/iOS/HarmonyOS SDK 及音频插件；WebRTC 需处理 SDP、DataChannel、媒体轨道 | 需要按事件协议自行管理音频编码、缓冲区提交、响应取消、工具调用和错误处理 | 快速服务端原型可用 WebSocket；高质量端侧体验需投入 WebRTC/AOQ 集成；精细模型控制需实现 Omni 事件协议 |
| 计费方式 | 文档切片未给出独立计费细节，通常应以所选模型、协议和百炼计费说明为准 | 文档切片未给出独立计费细节，通常按 Omni 实时模型用量和官方计费规则执行 | 不应仅凭 API 名称判断成本，正式上线前需核对目标模型的最新计费规则、音频/文本/多模态计量口径 |
| 典型场景 | 实时语音/视频对话、移动端弱网通话、浏览器实时互动、ASR/TTS、实时翻译、多模态开发套件接入 | Omni 实时多模态对话、语音 VAD/Manual 轮次控制、工具调用、联网搜索、声音与会话参数控制 | 若目标是“搭建实时交互产品”，先选实时 API 协议；若目标是“驱动 Omni 模型完成对话与工具调用”，重点实现 Omni Realtime API |

## 适用场景建议

### 优先选择实时 API 的场景

- 需要在 WebSocket、WebRTC、AOQ 之间做协议选型，或者同一业务需要覆盖服务端、浏览器端和移动端原生应用。
- 业务重点是实时音视频链路质量，例如弱网对抗、回声消除、降噪、媒体采集播放、端侧 SDK 集成等。
- 移动端原生应用不希望暴露 API Key，需要通过 AppServer 换取临时 Token，并使用 AOQ SDK 建连。
- 除 Omni 实时模型外，还需要接入实时 ASR、实时 TTS、实时语音对话、实时翻译或多模态开发套件。
- 团队更关心“如何把实时能力接入产品端”，而不是逐个事件控制模型交互细节。

### 优先选择 Omni Realtime API 的场景

- 已明确使用 Qwen-Omni-Realtime 系列模型，需要按 WebSocket 事件协议直接控制会话和响应。
- 需要精细处理 `session.update`、音频缓冲区追加/提交/清空、响应创建/取消、对话项创建等事件。
- 需要实现 Function Calling，并根据 `response.function_call_arguments.done` 执行业务工具后回传结果。
- 需要使用 `server_vad`、`semantic_vad` 或 Manual 模式控制对话轮次，尤其是“按下即说”一类交互。
- 需要启用联网搜索、配置音色、调整输出文本/音频模态、处理转录增量和音频增量等模型级能力。

## 开发者选型路径

1. **先确定产品形态**：如果是移动端实时通话、浏览器实时对话或多端音视频产品，先从实时 API 的协议能力开始；如果是服务端或客户端直接驱动 Omni 实时模型，则从 Omni Realtime API 的事件协议开始。
2. **再确定模型范围**：如果只使用 Qwen-Omni-Realtime 系列，Omni Realtime API 能提供更细的参数和事件说明；如果还涉及 ASR、TTS、实时翻译或 qwen-audio，实时 API 的模型矩阵更适合作为入口。
3. **评估网络与音频处理要求**：弱网、AEC、降噪和端侧媒体链路是 WebRTC/AOQ 的优势；纯 WebSocket 事件接入更适合服务端集成和精细协议控制。
4. **评估安全边界**：任何客户端方案都不应硬编码 API Key。移动端原生优先采用 AppServer 换取 Token 的 AOQ 模式；浏览器 WebRTC 的 SDP 交换也建议由 AppServer 代理。
5. **评估交互控制复杂度**：如果需要工具调用、联网搜索、Manual 模式、响应取消和细粒度错误处理，应按 Omni Realtime API 的事件流设计状态机。

## 总结

实时 API 是“接入实时能力的方案层入口”，帮助开发者在协议、端侧平台、弱网能力和模型类型之间做选择；Omni Realtime API 是“驱动 Omni 实时模型的协议层接口”，强调会话参数、事件类型、VAD/Manual 轮次、工具调用和响应流处理。实际项目中两者并非互斥：可以先用实时 API 选择合适的传输方案，再按 Omni Realtime API 实现具体模型交互。对于追求端侧体验和网络鲁棒性的应用，优先关注 WebRTC/AOQ；对于追求模型事件控制和业务编排能力的应用，优先关注 Omni Realtime API。

## 被对比主题页

- [realtime api user guide](../guides/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


