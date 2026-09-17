# 实时API方案对比：Omni Realtime API vs Realtime API User Guide

为帮助开发者在构建语音助手、智能客服、实时音视频交互等低延迟多模态应用时做出高效、可靠的技术选型，本文对百炼平台当前两大核心实时能力接口——**Omni Realtime API** 与 **Realtime API User Guide（统称 Realtime API）** 进行系统性对比分析。二者虽均面向实时交互场景，但在协议架构、模型覆盖、接入方式、控制粒度及适用边界上存在显著差异。本对比基于最新文档（截至2024年Q3），聚焦可落地的技术事实，不依赖主观评价，旨在提供客观、可执行的选型依据。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **核心协议** | **仅 WebSocket**（强制 `wss://` 连接） | **三协议统一支持**：AOQ（推荐移动端）、WebRTC（推荐浏览器）、WebSocket（推荐服务端/通用环境）；通过 `x-dashscope-rtc-transport` 请求头显式指定 |
| **输入格式** | - 音频：`pcm`/`wav`，采样率 `8000–48000 Hz`（客户端可配置，但服务端可能覆盖）<br>- 文本：`text` 字段或 `input_text` 事件<br>- 图像：`input_image_buffer.append`（Base64 JPG/JPEG，≤256KB）<br>- 事件驱动：`input_audio_buffer.append`、`session.update` 等标准化事件 | - 音频：**仅 `pcm`**（硬性限制），采样率由模型决定（如 ASR/TTS 模型固定 `16000 Hz`）<br>- 文本：`input_text` 或 `session.update.instructions`<br>- **不支持图像输入**（无 `input_image_buffer` 相关事件）<br>- 协议层原生媒体流：AOQ/WebRTC 支持直接推送音频帧；WebSocket 仍需事件封装 |
| **输出格式** | - `["text"]` 或 `["text","audio"]`（可配）<br>- 音频：Base64 编码 `response.audio.delta`，**服务端固定 `24000 Hz` 输出**（客户端配置 `sample_rate` 无效）<br>- 文本：`response.text.delta`（流式）<br>- ASR 中间结果：`response.audio_transcript.delta`（支持实时语音转写反馈） | - `["text"]` 或 `["text","audio"]`（可配）<br>- 音频：Base64 `response.audio.delta`（WebSocket）或原生 PCM 帧（AOQ/WebRTC）<br>- 文本：`response.text.delta`（流式）<br>- **不提供 ASR 中间转写流**（无 `audio_transcript` 类事件） |
| **支持模型** | 仅 `qwen*-omni-*-realtime` 系列：<br>- `qwen3.5-omni-plus-realtime`（最强功能）<br>- `qwen3.5-omni-flash-realtime`<br>- `qwen3-omni-flash-realtime`<br>- `qwen-omni-turbo-realtime`（功能受限） | **全模型矩阵支持**：<br>- Omni 全模态系列（同上）<br>- 实时语音翻译（`qwen3.5-livetranslate-flash-realtime`）<br>- 多模态开发套件（`multimodal-dialog`）<br>- 实时 ASR（`Qwen-Audio-3.0-ASR-Flash-Streaming` 等）<br>- 实时 TTS（`CosyVoice`、`qwen-audio-3.0-tts-*`）<br>- 实时语音对话（`qwen-audio-3.0-realtime-*`）<br>⚠️ **协议兼容性差异**：ASR/TTS 仅 AOQ/WebSocket 支持，**WebRTC 不支持** |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime` | **协议差异化端点**：<br>- AOQ：`POST /api/v1/webrtc/realtime`（获取 [Token](../concepts/token.md)） + Relay 连接<br>- WebRTC：`POST /api/v1/webrtc/inference`（信令交换）<br>- WebSocket：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`（同 Omni，但鉴权与参数不同） |
| **计费方式** | 按 **会话时长（秒） + 音频处理量（分钟） + 工具调用次数** 计费；支持按量付费与资源包；**无免费额度** | 按 **模型调用类型分项计费**：<br>- Omni 模型：同 Omni Realtime API 计费逻辑<br>- ASR/TTS/翻译等独立模型：单独计费项，支持免费额度（如 ASR 首月 10 小时免费）<br>- **同一会话中混合调用多模型（如 ASR + Omni + TTS）将分别计费** |
| **典型场景** | - 高定制化语音助手（需语义 VAD、工具链深度集成）<br>- 需图像理解+语音交互的复合场景（如远程专家指导）<br>- 对端到端延迟敏感且接受 WebSocket 架构的 B端服务集成 | - 跨端统一接入（iOS/Android/Web/Windows/macOS）<br>- 弱网环境强鲁棒需求（AOQ 自适应重传、WebRTC NAT 穿透）<br>- 分离式架构：前端用 WebRTC 采集/播放，后端用 WebSocket 调用 ASR/TTS/LLM<br>- 快速验证多模型组合（如“语音输入→ASR→LLM→TTS→语音输出”流水线） |

## 各方案适用场景建议

### ✅ 推荐选用 **Omni Realtime API** 当：
- 应用场景**严格限定于 WebSocket 环境**（如 Node.js 后端服务、Electron 桌面应用、或已具备 WebSocket 基础设施的 Web 应用）；
- **必须使用图像理解能力**（如拍照问诊、AR 教学），且需与语音/文本在同一会话中协同处理；
- 需要 **`semantic_vad`（语义级静音检测）** 或 **联网搜索（`enable_search`）** 等高级功能，且明确不与工具调用共存；
- 已有成熟 WebSocket 客户端栈，希望最小化 SDK 依赖，直接对接事件协议；
- 对 ASR 中间转写流（`response.audio_transcript.delta`）有强依赖，用于实时字幕、说话人标注等。

### ✅ 推荐选用 **Realtime API User Guide** 当：
- 需要**一次开发、多端部署**（尤其需同时覆盖 iOS、Android、Chrome/Firefox 浏览器）；
- 应用运行在**弱网、高丢包、NAT 环境复杂**的终端（如车载设备、海外移动网络），需 AOQ 或 WebRTC 的底层抗性保障；
- 业务流程涉及**多个独立实时模型串联**（例如：用户语音 → ASR → 意图识别 → LLM 生成 → TTS → 播放），而非单模型全栈处理；
- 需要**精细控制音视频采集/播放管线**（如自定义降噪、混音、硬件加速播放），并利用 AOQ SDK 的 `isExternal=true` 模式接管底层帧；
- 希望利用 **ASR/TTS 等模型的免费额度** 降低成本，或需按模型类型精细化成本核算。

## 技术选型参考（面向开发者）

| 选型考量 | Omni Realtime API | Realtime API User Guide |
|----------|-------------------|--------------------------|
| **协议灵活性** | ❌ 单一 WebSocket，无法适配浏览器原生 WebRTC 或移动端 AOQ 优势 | ✅ 三协议可选，按场景动态切换，未来扩展性强 |
| **多模态能力广度** | ✅ 支持文本+音频+图像三模态联合推理 | ❌ 仅文本+音频，无图像理解能力 |
| **模型生态覆盖** | ❌ 仅 Omni 系列模型，无法调用 ASR/TTS/翻译等专用模型 | ✅ 全平台实时模型统一接入，支持混合编排 |
| **接入复杂度** | ⚠️ 事件协议需手动管理状态（如 `input_audio_buffer.commit`）、VAD 模式切换、工具调用生命周期 | ✅ SDK 封装完善（AOQ/WebRTC/WS 三套 SDK），提供 `enableSendMediaStream` 等安全开关，降低出错风险 |
| **弱网/跨平台鲁棒性** | ⚠️ WebSocket 在 NAT/防火墙/移动网络下易中断，无内置重连与自适应机制 | ✅ AOQ 内置拥塞控制与前向纠错（FEC），WebRTC 原生 NAT 穿透，浏览器零依赖 |
| **调试与可观测性** | ✅ 事件结构清晰（`session.created`, `response.audio.delta`），日志粒度细，便于问题定位 | ⚠️ 协议层抽象更高（尤其 AOQ/WebRTC），部分问题需结合信令日志与媒体流分析 |

> **最终建议**：  
> - 若项目是 **新启动的、以语音+图像为核心的垂直 SaaS 服务**，且团队具备 WebSocket 协议栈经验 → 优先评估 **Omni Realtime API**；  
> - 若项目需 **快速上线、覆盖全终端、容忍一定架构复杂度以换取稳定性与成本优势** → **Realtime API User Guide 是更稳妥、可持续的选择**；  
> - **绝不混合使用**：二者虽端点相似，但事件格式、鉴权逻辑、错误码体系完全不兼容，混用将导致连接失败或不可预测行为。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


