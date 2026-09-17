# 实时API方案对比：Omni Realtime API vs Realtime API User Guide

本文旨在帮助开发者清晰区分百炼平台当前两大实时交互接口方案——**Omni Realtime API** 与 **Realtime API User Guide（即标准 Realtime API）**，明确其定位差异、能力边界与适用约束。二者虽均面向低延迟[多模态](../concepts/multi-modal.md)交互场景，但在协议栈设计、模型支持粒度、接入复杂度、终端适配能力和运维模型上存在本质区别。本对比基于最新文档（截至2024年Q3）整理，聚焦技术选型关键决策点，不涉及历史兼容性或过渡方案。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **核心协议与传输层** | 纯 WebSocket（`wss://`），事件驱动，单连接全生命周期管理 | **三协议可选**：AOQ（Media over QUIC）、WebRTC、WebSocket；协议能力与模型支持强耦合 |
| **输入格式** | 支持 `input_audio_buffer.append`（PCM/WAV，采样率 8k–48k Hz）、`input_image_buffer.append`（Base64 JPG/JPEG，≤256KB，480p/720p 推荐） | 音频仅支持 `pcm` 格式（无 WAV）；**不支持图像输入**；视频仅 AOQ/WebRTC 支持采集，但 Realtime API 当前未开放图像理解能力 |
| **输出格式** | `["text"]` 或 `["text", "audio"]`；音频默认 `wav`（24 kHz），支持显式配置 `sample_rate` 和 `type`（`wav`/`pcm`）；支持 `response.audio_transcript.delta`（实时 ASR 转录） | `["text"]` 或 `["text","audio"]`；音频**仅支持 `pcm`**（文档明确限定）；无原生 ASR 转录流事件；`audio` 输出需客户端自行解码渲染 |
| **支持模型** | 专属模型族：<br>• `qwen3.5-omni-plus-realtime`<br>• `qwen3.5-omni-flash-realtime`<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime`<br>（全部为 Omni 系列，强绑定[多模态](../concepts/multi-modal.md)语音对话） | **广谱模型支持**：<br>• 全模态：`qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`<br>• 专用模型：`fun-asr-realtime`, `qwen-audio-3.0-tts-flash`, `qwen-audio-3.0-realtime-plus/flash`, `qwen3.5-livetranslate-flash-realtime`, `multimodal-dialog`<br>• **ASR/TTS 模型仅 AOQ/WebSocket 支持，WebRTC 不支持** |
| **语音活动检测（VAD）** | 双模式：<br>• `server_vad`（声学级，全模型支持）<br>• `semantic_vad`（语义级，仅 `qwen3.5-omni-realtime` 系列支持）<br>支持细粒度参数调节（`threshold`, `silence_duration_ms`, `idle_timeout_ms`） | 仅 `server_vad`（声学级），所有支持模型统一启用；参数调节能力弱，无 `semantic_vad` 或 `idle_timeout_ms` 等高级选项 |
| **扩展能力** | • 工具调用（`tools`）：支持 `function` 类型，模型自主触发<br>• 联网搜索（`enable_search`）：仅 `qwen3.5-omni-realtime` 系列支持，**与 `tools` 互斥**<br>• 声音复刻：需预注册音色，且驱动模型必须与注册时 `target_model` 严格一致 | • **不支持工具调用（`tools`）**<br>• **不支持联网搜索（`enable_search`）**<br>• 声音复刻能力未在文档中提及，当前不可用 |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`<br>**强烈推荐使用业务空间专属域名** | 协议决定端点：<br>• AOQ：`moq://` + Relay Endpoint（由服务端下发）<br>• WebRTC：`wss://` + 信令地址（如 `/api/v1/webrtc/realtime`）<br>• WebSocket：`wss://` + 统一入口（如 `/api-ws/v1/realtime`）<br>**建连需携带 `model` 查询参数与 `Authorization` 头** |
| **计费方式** | 按 **实际消耗的 [Token](../concepts/token.md) 数 + 音频处理时长（秒）** 计费；<br>• 文本 [Token](../concepts/token.md)：按输入+输出 token 计费<br>• 音频：按 `input_audio_duration` + `output_audio_duration`（秒）计费<br>• 图像：按次计费（每张 Base64 图片） | 按 **模型调用次数 + 音频处理时长（秒）** 计费；<br>• 每次 `session.create` 或连接成功视为一次调用<br>• 音频按 `input_seconds` + `output_seconds` 计费<br>• **ASR/TTS 独立计费项**（如 `fun-asr-realtime` 按音频秒数计费） |
| **典型场景** | • 高保真、低延迟语音助手（需语义 VAD 与自然中断）<br>• 智能客服（需工具调用处理订单/查询）<br>• [多模态](../concepts/multi-modal.md)交互应用（语音+图像联合理解）<br>• 需定制音色与高可控性的对话系统 | • 跨平台语音助手（Android/iOS/HarmonyOS/Windows/macOS/Linux）<br>• 弱网环境下的实时翻译/会议转录<br>• 浏览器端嵌入式客服（WebRTC）<br>• 快速验证原型（WebSocket）<br>• 分离式架构：ASR → LLM → TTS 管道编排 |

## 各方案适用场景建议

### ✅ 推荐选用 **Omni Realtime API** 当：
- 业务核心是 **端到端语音对话体验**，且对语音自然度、中断响应、语义级静音检测（`semantic_vad`）有严苛要求；
- 需要 **在对话中动态调用外部工具**（如查天气、订机票、读取数据库），且希望模型自主决策触发；
- 应用需支持 **语音+图像混合输入**（如“帮我看看这张发票金额是否正确”）；
- 已完成声音复刻并要求 **音色与模型版本强绑定**，追求极致音质一致性；
- 技术栈以 Web/服务端为主，**无需原生移动端深度音视频优化**，接受 WebSocket 连接模型。

### ✅ 推荐选用 **Realtime API User Guide** 当：
- 面向 **多终端（尤其移动端原生 App）交付**，需强弱网对抗、3A（回声消除/降噪/AGC）、低首包时延，**AOQ 是首选协议**；
- 场景需要 **模块化能力组合**，例如：前端用 WebRTC 采集 → 后端用 WebSocket 调用 `fun-asr-realtime` → 再调用 `qwen3.5-omni-plus-realtime` → 最后用 `CosyVoice` 合成，实现灵活编排；
- 业务已存在 WebRTC 基础设施（如自研音视频 SDK），希望 **最小改造接入 AI 对话能力**；
- 需要 **独立计量 ASR 或 TTS 成本**，或对不同模型（如翻译 vs 对话）进行差异化 SLA 管理；
- 开发团队具备跨平台 SDK 集成经验，能接受 AOQ SDK 的初始化与媒体流生命周期管理复杂度。

### ⚠️ 不建议混用或强行迁移的场景：
- 将 Omni Realtime API 用于纯 ASR/TTS 场景（能力缺失，成本不优）；
- 在 WebRTC 协议下尝试调用 `fun-asr-realtime`（文档明确不支持，将失败）；
- 为追求“简单”而对移动端项目选用 Omni Realtime API WebSocket 方案（将丢失弱网鲁棒性、3A、硬件加速等关键能力）；
- 在需要 `tools` 或 `enable_search` 的场景下选用 Realtime API（当前完全不支持）。

## 技术选型参考指南（面向开发者）

| 选型问题 | Omni Realtime API | Realtime API User Guide |
|----------|-------------------|--------------------------|
| **我是否需要语义级语音活动检测（理解用户是否真说完）？** | ✅ 是（`semantic_vad`） | ❌ 否（仅声学 VAD） |
| **我是否需要在对话中调用数据库/API 完成任务？** | ✅ 是（原生 `tools`） | ❌ 否（需服务端中转） |
| **我的 App 主要运行在 iOS/Android 原生环境？** | ⚠️ 可用但非最优（无 AOQ/3A） | ✅ 强烈推荐（AOQ SDK 提供最佳体验） |
| **我的前端是浏览器，且已有 WebRTC 基础？** | ⚠️ 可用（WebSocket） | ✅ 推荐（WebRTC 协议原生兼容） |
| **我需要分别采购和计量 ASR、TTS、LLM 能力？** | ❌ 否（全模态打包） | ✅ 是（独立模型、独立计费） |
| **我需要上传图片让模型看图说话？** | ✅ 是（`input_image_buffer`） | ❌ 否（当前不支持图像输入） |
| **我能否接受客户端自行管理音频编解码与播放？** | ✅ 是（WebSocket 纯数据流） | ⚠️ AOQ/WebRTC：SDK 托管；WebSocket：需自行处理 |
| **我是否希望快速启动一个网页 Demo 验证效果？** | ✅ 是（WebSocket 最简接入） | ✅ 是（WebSocket 同样可用） |

> **总结建议**：  
> - **选 Omni Realtime API** → 聚焦“**对话智能**”，适合以语音为核心、强调语义理解与动作执行的垂直应用；  
> - **选 Realtime API User Guide** → 聚焦“**传输智能**”，适合以多端交付、弱网鲁棒、能力解耦为优先的规模化生产系统。  
> 二者并非替代关系，而是百炼实时能力矩阵的两个正交切面。在复杂产品中，可结合使用：例如用 Realtime API（AOQ）承载端侧音视频管道，再将 ASR 结果通过 Omni Realtime API 发起带工具调用的深度对话。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


