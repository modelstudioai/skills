# 实时交互 API 方案对比：Omni Realtime API 与 Realtime API

## 对比目的与背景

为帮助开发者在构建低延迟、多模态实时交互应用（如智能语音助手、会议实时纪要、音视频智能客服等）时做出精准技术选型，本文系统对比百炼平台当前两大核心实时交互 API 方案：**Omni Realtime API** 与 **Realtime API**。二者虽均面向流式、低时延场景，但在架构设计、能力边界、协议抽象层级及适用范式上存在本质差异。本对比基于最新文档（截至 2025 年 9 月）、实际接入约束与典型生产实践，聚焦可落地的技术维度，不涉及主观体验评价，旨在提供客观、可执行的选型决策依据。

---

## 关键维度对比表

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心定位** | **会话级多模态智能体 API**：以“语义会话”为中心，内置 VAD、工具调用、搜索、多模态协同等高级能力，强调端到端意图理解与主动响应 | **媒体流级基础通道 API**：以“原始音视频流处理”为核心，提供高保真、低抖动的流式编解码与传输通道，强调媒体帧级控制与时序精度 |
| **输入格式** | 支持结构化事件驱动输入：<br>• `input_audio_buffer.append`（PCM 音频流，支持单/双/四声道空间音频）<br>• `session.update`（动态配置）<br>• `response.create`（显式触发）<br>• 工具调用结果回传（`tool_result`） | 原始二进制媒体帧流：<br>• PCM 音频 chunk（如 `pcm-16k-1ch`）或 H.264 视频 chunk<br>• 每帧需携带 `seq` 序号与 `timestamp_ms`<br>• 无语义事件，纯媒体数据管道 |
| **输出格式** | 语义化、分层事件流：<br>• `conversation.item.created`（含文本/音频内容）<br>• `response.content_part.added`（流式音频片段，含 `audio_chunk` 和 `text_delta`）<br>• `response.done` / `response.cancel`<br>• `input_audio_buffer.speech_started/stopped`（VAD 事件） | 原始响应帧（Frame-based）：<br>• `text_delta`（增量文本）<br>• `audio_chunk`（PCM 音频二进制）<br>• `event`（如 `speech_start`, `speech_end`）<br>• 无会话状态封装，需客户端自行维护上下文 |
| **支持模型** | 专属 Omni 系列实时模型：<br>• `qwen3.8-omni-flash-realtime`（主力推荐）<br>• `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`<br>• `qwen3-omni-flash-realtime-2025-09-15`（实验版）<br>→ 全部为统一多模态大模型，支持文本+语音联合推理 | 专用媒体感知模型：<br>• `qwen-audio-realtime`（ASR+语义理解一体化）<br>• `qwen-vl-realtime`（音视频联合理解与事件检测）<br>→ 模型能力垂直聚焦，不支持通用文本生成或工具调用 |
| **API 端点与协议** | 多协议支持：<br>• WebSocket（推荐，SDK 封装完善）<br>• AOQ（阿里云消息队列，适合服务端集成）<br>• WebRTC（端到端音视频直连，低延迟首选）<br>→ 端点由 SDK 自动路由，开发者无需硬编码 URL | 单一协议：<br>• WebSocket（强制）<br>• 端点固定：`wss://dashscope.aliyuncs.com/realtime/v1/chat`<br>→ 客户端需严格管理连接生命周期、帧序列与心跳 |
| **计费方式** | 按 **会话时长（秒） + 输出 Token 数** 计费：<br>• 会话建立即开始计时（含静默等待期）<br>• 输出文本 Token、音频 Token（按等效文本长度折算）分别计费<br>• 支持并发会话数弹性伸缩（无单连接限制） | 按 **媒体流处理时长（秒） + 输入/输出音频帧数** 计费：<br>• 从首帧发送至连接关闭全程计费（含空闲期）<br>• 音频帧按采样点计费（如 16kHz × 1ch × 1s = 16000 点）<br>• 单连接独占，1 连接 = 1 计费单元 |
| **典型场景** | • 全双工语音助手（支持打断、多轮追问、语义静音判断）<br>• 智能客服坐席辅助（实时转写+知识库检索+话术建议）<br>• 会议实时纪要（语音输入 → 文本摘要+关键结论+行动项生成）<br>• 多模态 Agent 应用（语音指令 → 工具调用 → 音频反馈） | • 实时语音转写（高精度 ASR，低 WER）<br>• 直播/会议音视频流实时分析（人声分离、关键词触发、画面事件标注）<br>• 边缘设备音视频预处理（将原始流转发至百炼进行轻量理解）<br>• 自定义 TTS 合成引擎的后端语音合成服务（配合 AOQ SDK） |

---

## 适用场景建议

### ✅ 推荐选用 Omni Realtime API 当：
- 你需要构建一个**具备完整对话智能的终端应用**，而非仅做媒体转换；
- 场景要求**语义级交互能力**：如自动检测用户停顿（`semantic_vad_ec`）、根据上下文自主调用工具或搜索、支持多音色自然语音输出；
- 开发团队希望**降低协议复杂度**，复用 SDK 封装的会话管理、VAD、重连、错误恢复等能力；
- 业务逻辑依赖**多模态协同**（例如：用户说“把刚才PPT第3页的内容读出来”，需结合语音输入 + 视觉理解 + 文本生成）；
- 需要灵活配置会话生命周期（如动态切换音色、启用/禁用搜索、更新工具列表）。

### ✅ 推荐选用 Realtime API 当：
- 你的系统已具备成熟的**前端音频采集、VAD、信令控制模块**，只需百炼提供底层媒体理解能力；
- 场景对**媒体时序精度和帧级控制有硬性要求**（如工业级语音质检、实时唇形同步、AR眼镜音视频融合）；
- 需要处理**非标准音频格式或特殊采样率/声道配置**（但须严格匹配模型约束）；
- 架构采用**微服务解耦设计**：媒体流预处理服务（独立 VAD/降噪）→ Realtime API → 业务逻辑服务；
- 成本敏感且流量高度可控：可通过精细控制帧发送节奏与连接时长，优化计费粒度。

> ⚠️ 注意：二者**不可混用替代**。Omni Realtime API 不提供裸媒体帧接口；Realtime API 不支持 Function Calling 或语义搜索。若需组合能力（如：Realtime API 做 ASR → 结果送 Omni Realtime API 做推理），应通过服务端桥接实现。

---

## 技术选型参考（面向开发者）

| 决策因素 | Omni Realtime API | Realtime API | 建议动作 |
|----------|-------------------|--------------|----------|
| **开发效率优先级 > 性能极致化** | ✅ SDK 开箱即用，事件模型清晰，调试日志丰富 | ❌ 需手动处理帧序列、时间戳、重连逻辑，调试成本高 | 选 Omni |
| **已有成熟 VAD/ASR 模块，需替换为百炼增强能力** | ❌ 会覆盖/重复已有 VAD，增加冗余 | ✅ 可直接对接现有音频 pipeline，零侵入替换 | 选 Realtime |
| **必须支持四声道空间音频输入或语义级静音检测（`semantic_vad_ec`）** | ✅ 仅 `qwen3.8-omni-flash-realtime` 支持 | ❌ 不支持空间音频，VAD 仅基础声学级 | 选 Omni |
| **需在响应中嵌入结构化工具调用结果（如查天气后播报+播放语音）** | ✅ 原生支持 `type=function` / `type=mcp`，与音频输出无缝协同 | ❌ 不支持任何工具调用机制 | 选 Omni |
| **输入音频采样率为 8kHz 或 48kHz 单声道** | ❌ `qwen3.8` 强制 16kHz；`qwen3.5` 支持但需确认模型兼容性 | ✅ `qwen-audio-realtime` 仅支持 16kHz，其他采样率需前端重采样 | 若为 8kHz/48kHz → 需预处理；若为 16kHz → 两者均可，但 Omni 更易用 |
| **部署环境受限（如无法维持长 WebSocket 连接，仅支持 HTTP 轮询）** | ❌ 不支持 HTTP 轮询，必须长连接 | ❌ 同样不支持 HTTP 轮询 | 需评估网络基础设施，二者均不适用；考虑降级为普通 Streaming API |

**最终建议路径**：  
1. **MVP 阶段**：优先使用 Omni Realtime API + WebSocket SDK 快速验证交互逻辑与用户体验；  
2. **规模化/定制化阶段**：若出现性能瓶颈（如万级并发会话下的连接管理压力）或需深度控制媒体链路，再评估迁移到 Realtime API + 自研信令层；  
3. **混合架构场景**：用 Realtime API 处理高保真 ASR/VAD，结果 JSON 推送至 Omni Realtime API 会话中作为 `input_text` 触发智能响应——此模式已在多个金融客服项目中验证可行。

---  
*本文档持续更新，最新模型支持列表与参数约束请以百炼控制台「API 能力中心」及对应 SDK 版本说明为准。*

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


