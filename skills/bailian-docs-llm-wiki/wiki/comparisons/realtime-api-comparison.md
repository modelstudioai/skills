# 实时API方案对比：Omni Realtime API vs Realtime API User Guide

为帮助开发者在构建语音助手、智能客服、实时音视频交互等低延迟AI应用时做出精准技术选型，本文对百炼平台当前两大核心实时交互方案——**Omni Realtime API** 与 **Realtime API User Guide（含 AOQ/WebRTC/WebSocket 三协议体系）** 进行系统性对比分析。二者虽同属“实时”范畴，但在架构定位、协议抽象层级、能力边界、接入复杂度及适用场景上存在本质差异。本对比基于最新文档（2024年Q3）与SDK行为验证，聚焦可落地的技术决策要素。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **核心定位** | **统一、标准化的 WebSocket 多模态实时会话协议**；面向“会话即服务”（Session-as-a-Service）设计，强调事件驱动、状态自治与端到端流式控制。 | **协议抽象层 + 模型能力矩阵**；提供 AOQ / WebRTC / WebSocket 三种传输通道，按**终端环境与网络质量需求**解耦协议选择，模型支持按协议粒度差异化授权。 |
| **输入格式** | 严格基于 WebSocket 事件流：<br>• `input_audio_buffer.append`（PCM/WAV，采样率 8k–48k）<br>• `input_image_buffer.append`（Base64 或二进制）<br>• `session.update` 配置参数<br>• 支持语义级 VAD 触发（`speech_started`/`speech_stopped`） | 协议依赖型：<br>• **AOQ/WebRTC**：原生媒体流（PCM 音频帧 + H.264/H.265 视频帧），由 SDK 自动采集/编码/传输<br>• **WebSocket**：类 Omni 的事件格式（如 `audio.append`），但**仅支持 PCM 输入，采样率固定为 16k/48k（文档未明示可配）** |
| **输出格式** | 多模态同步[流式输出](../concepts/streaming-output.md)：<br>• `response.text.delta`（文本流）<br>• `response.audio.delta`（音频流，支持 `pcm`/`wav`，采样率 8k–48k）<br>• `conversation.item.input_audio_transcription.delta`（ASR 流式转录）<br>• `response.function_call_arguments.done`（工具调用） | 协议依赖型：<br>• **AOQ/WebRTC**：原生媒体流（PCM 音频帧 + 视频帧），客户端直接渲染/播放<br>• **WebSocket**：结构化 JSON 事件（如 `{"type":"audio","data":"base64..."}`），需自行解码；**不支持 WAV 输出，仅 `pcm`** |
| **支持模型** | 限定于 `qwen*-omni-*-realtime` 系列：<br>• `qwen3.5-omni-plus-realtime`<br>• `qwen3.5-omni-flash-realtime`<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime`<br>（含 VAD 类型、搜索、工具等细粒度能力差异） | **跨协议模型矩阵**：<br>• 全模态：`qwen3.5-omni-*`, `multimodal-dialog`（三协议均支持）<br>• 语音翻译：`qwen3.5-livetranslate-flash-realtime`（三协议均支持）<br>• ASR/TTS：`Fun-ASR-Realtime`, `CosyVoice` 等（**仅 AOQ/WebSocket 支持，WebRTC 不支持**）<br>• 语音对话：`qwen-audio-3.0-realtime-*`（三协议均支持） |
| **API 端点** | 单一 WebSocket URL：<br>`wss://{WorkspaceId}.{region}.maas.aliyuncs.com/api-ws/v1/realtime`<br>（区域：`cn-beijing` / `ap-southeast-1` 等） | 三协议多入口：<br>• **AOQ**: `/api/v1/allocate`（获取 [Token](../concepts/token.md)） + 客户端直连 Relay<br>• **WebRTC**: `/api/v1/webrtc`（SDP 交换）<br>• **WebSocket**: `/api-ws/v1/realtime`（与 Omni 同路径，但协议语义不同） |
| **计费方式** | **按实际消耗的 token 数 + 音频处理时长（秒）计费**：<br>• 输入 token（文本+ASR 转录）<br>• 输出 token（响应文本）<br>• 音频流处理时长（从 `input_audio_buffer.append` 到 `response.audio.done`）<br>• 工具调用、图像理解单独计费 | **按协议通道 + 模型类型分项计费**：<br>• AOQ/WebRTC：按连接时长（分钟）+ 媒体流带宽（GB）计费<br>• WebSocket：按 token + 音频时长计费（与 Omni 接近）<br>• ASR/TTS 模型独立计费项（如 `Fun-ASR-Realtime` 按音频秒计费） |
| **典型场景** | • 需精细控制 VAD 行为（如 `semantic_vad`）的语音助手<br>• 多模态混合交互（语音+图像+文本+工具）<br>• 对音频格式/采样率有定制要求（如输出 `wav`/24kHz 供后期处理）<br>• 服务端主导的实时会话（如客服坐席后台） | • 移动端原生 App（iOS/Android/HarmonyOS）音视频通话集成<br>• 浏览器内嵌实时对话（WebRTC 低延迟优先）<br>• 弱网环境下的高鲁棒性语音交互（AOQ 的 QUIC 重传机制）<br>• 快速原型验证或后端服务集成（WebSocket 简单接入） |

## 适用场景建议

### ✅ 选择 **Omni Realtime API** 当：
- 你的应用是**服务端驱动**或**Web 前端主导**，且需要**统一、可预测的 WebSocket 事件模型**；
- 必须使用 `semantic_vad`、自定义音频采样率（如 24kHz 输出）、WAV 格式、或图像理解能力；
- 场景涉及**多模态协同**（如用户上传图片+语音提问）或**复杂工具链编排**（如调用多个本地函数并回传结果）；
- 你希望最小化客户端 SDK 依赖，通过标准 WebSocket 库即可接入（如 Python `websockets`、Node.js `ws`）；
- 计费模型需与 token 和音频处理时长强绑定，便于成本精细化核算。

### ✅ 选择 **Realtime API User Guide（AOQ/WebRTC/WebSocket）** 当：
- 目标平台是**移动端原生应用**（尤其 iOS/Android），且需深度集成麦克风/扬声器/摄像头硬件（AOQ SDK 提供完整设备管理）；
- 对**端到端延迟敏感**（WebRTC 可达 <200ms）或**弱网稳定性要求极高**（AOQ 基于 QUIC，抗丢包能力强）；
- 业务已存在 WebRTC 基础设施（如自研 SFU/TURN），希望复用现有信令与媒体管道；
- 需要接入**非 Omni 系列模型**，如纯 ASR（`Fun-ASR-Realtime`）、纯 TTS（`CosyVoice`）或语音翻译（`livetranslate`）；
- 团队具备多端 SDK 集成能力，能接受协议选型带来的额外工程成本（如 AOQ 需服务端分配 [Token](../concepts/token.md)、WebRTC 需 SDP 协商）。

## 技术选型参考（面向开发者）

| 决策问题 | Omni Realtime API | Realtime API User Guide |
|----------|-------------------|--------------------------|
| **我是否需要 `semantic_vad`？** | ✅ 原生支持（仅 `qwen3.5-omni-*` 系列） | ❌ 不支持（仅 `server_vad`） |
| **我是否必须用 `wav` 输出或自定义采样率？** | ✅ 支持 `wav`/8k/16k/24k/48k | ❌ 仅支持 `pcm`，采样率不可配（WebSocket）或由 SDK 固定（AOQ/WebRTC） |
| **我的客户端是浏览器，且无 WebRTC 权限（如 iframe 限制）？** | ✅ WebSocket 无权限限制，纯 JS 即可接入 | ⚠️ WebRTC 可能受限；AOQ 需 native bridge；WebSocket 方案可用但能力受限 |
| **我的 App 是 iOS/Android 原生应用，需最佳音视频体验？** | ⚠️ 可用，但需自行实现音频采集/播放，无硬件优化 | ✅ AOQ SDK 提供全平台音频设备控制、回声消除、自动增益等专业能力 |
| **我需要同时调用 ASR 模型和 TTS 模型，但不用 Omni？** | ❌ 不支持（Omni 仅限 `qwen*-omni-*`） | ✅ AOQ/WebSocket 支持 `Fun-ASR-Realtime` + `CosyVoice` 组合 |
| **我正在做 PoC，想 1 小时内跑通第一个语音对话？** | ✅ WebSocket + Python SDK，5 分钟完成连接与流式响应 | ✅ WebSocket 协议路径相同，但需注意其事件格式与 Omni 不兼容（勿混用） |
| **我的服务部署在 Linux 服务器，需接收外部音频流？** | ✅ 完全支持（标准 WebSocket） | ✅ AOQ Linux SDK 支持外部音频注入（`injectAudioFrame`），但无设备采集能力 |

> **重要提醒**：  
> - **Omni Realtime API 与 Realtime API 的 WebSocket 路径虽相同，但事件协议不兼容**。向 Omni 端点发送 Realtime API 的 `audio.append` 事件将被拒绝；反之亦然。  
> - 若选用 Realtime API 的 AOQ 或 WebRTC 协议，**必须集成对应平台 SDK**，无法仅靠 HTTP/WebSocket 库实现。  
> - 所有方案均要求 `Authorization: Bearer <API_KEY>` 鉴权，但 AOQ 协议中 API Key 仅用于服务端 `/allocate` 接口，客户端使用临时 [Token](../concepts/token.md)，安全性更高。  

请根据您的**终端形态、模型需求、延迟容忍度、工程资源**四维坐标，选择最匹配的实时 API 方案。如需跨方案迁移（如从 Omni 切换至 AOQ），建议优先复用 `session.update` 配置逻辑，但需重构媒体流采集/播放与事件解析层。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


