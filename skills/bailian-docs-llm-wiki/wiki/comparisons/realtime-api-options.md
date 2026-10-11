# 实时 API 方案对比：Omni Realtime 与 Realtime User Guide

本文档面向百炼平台开发者，旨在清晰对比两种主流实时 API 方案——**Omni Realtime API** 与 **Realtime API User Guide（简称 Realtime User Guide）** 的核心能力、技术边界与适用场景。随着多模态实时交互需求激增（如语音优先的智能座舱、低延迟虚拟助手、音视频融合客服），选型需兼顾协议灵活性、模型能力深度、控制粒度及工程落地成本。本对比基于当前（2025年Q3）生产环境最新文档与 SDK 行为，聚焦可验证的技术事实，避免概念性描述，为架构决策提供客观依据。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime User Guide |
|------|-------------------|---------------------|
| **定位与目标场景** | 面向**端到端多模态实时交互闭环**（ASR → LLM → TTS + 工具调用），强调语义级控制与会话状态持久化 | 面向**原始音视频流的低延迟管道式处理**，聚焦媒体帧注入与事件反馈，弱语义、强时序 |
| **输入格式** | 支持结构化事件驱动：<br>• `input_audio_buffer.append`（PCM/WAV，支持单/双/四通道，需显式配置 `channels`/`channel_layout`）<br>• `conversation.item.create`（文本消息）<br>• 视频输入通过 `representation_compact` 表征聚合 | 仅支持二进制媒体流帧：<br>• `audio_chunk`（PCM/WAV，强制单通道、16kHz、16bit）<br>• `video_chunk`（MP4/H.264，≤720p）<br>• **不接受文本或结构化事件输入** |
| **输出格式** | 结构化 JSON 事件流（WebSocket）：<br>• `response.text.delta` / `response.audio.delta`（流式分块）<br>• `function_call` / `mcp_approval_request`（工具事件）<br>• `input_audio_buffer.speech_stopped`（VAD 状态）<br>• 支持 `output_audio_format: "wav"` 封装（开箱即播） | JSONL 格式纯事件流（每行一个 JSON 对象）：<br>• `response_chunk`（含 base64 编码音频/文本）<br>• `event: "speech_started"` 等轻量状态<br>• **无结构化工具调用事件，无 VAD 语义反馈** |
| **支持模型** | 专用实时多模态大模型：<br>• `qwen3.8-omni-flash-realtime`<br>• `qwen3.5-omni-plus-realtime`<br>• `qwen3.5-omni-flash-realtime`<br>• 实验性模型（如 `qwen3-omni-flash-realtime-2025-09-15`） | 专用实时感知模型（非大语言模型）：<br>• `qwen-audio-realtime-v1`（语音理解+简单响应）<br>• `qwen-video-realtime-v1`（视频理解+简单响应）<br>• **不支持任何通用文本大模型（如 qwen-max）或 Omni 系列模型** |
| **API 协议与接入方式** | 多协议支持：<br>• WebSocket（主推，含完整握手与事件规范）<br>• WebRTC（端到端加密，适合 P2P 场景）<br>• AOQ（阿里自研低延迟协议，SDK 封装） | **仅 WebSocket**：<br>• 固定端点：`wss://dashscope.aliyuncs.com/realtime/v1/chat`<br>• 握手消息为 `init`（非标准 HTTP Upgrade）<br>• **不支持 WebRTC 或 AOQ** |
| **核心能力** | ✅ 全链路多模态：ASR + LLM 推理 + TTS + VAD（server_vad / semantic_vad）<br>✅ 工具调用：Function Calling & MCP（含权限审批流）<br>✅ 联网搜索：特定模型支持自主触发<br>✅ 会话状态持久化（跨 `response.create` 保持上下文） | ❌ 无 ASR/TTS 集成（需客户端自行处理）<br>❌ 无 LLM 级推理（仅轻量感知与模板响应）<br>❌ 无工具调用、无搜索能力<br>✅ 原始媒体流低延迟透传（端到端 <300ms 典型值）<br>✅ 主动中断：`interrupt` 消息可即时终止响应流 |
| **关键参数控制粒度** | 极高：<br>• VAD 精细配置（`silence_duration_ms`, `semantic_vad`）<br>• 音频 I/O 格式动态指定（采样率 8k–48k，封装格式）<br>• 生成控制（`temperature`, `repetition_penalty=0` 等）<br>• 工具白名单、MCP server_url 安全校验 | 有限：<br>• `max_latency_ms`（软性延迟上限，100–2000ms）<br>• `session_id`（会话关联）<br>• `input_format`/`output_format`（仅限预设枚举）<br>• **无 VAD、无生成参数、无音频格式调节能力** |
| **计费方式** | **按 Token 计费**：<br>• 输入 Token（含音频转录文本、上下文、工具描述）<br>• 输出 Token（文本 + 音频等效 Token）<br>• 符合大模型通用计费逻辑 | **按传输字节数计费**：<br>• 仅计算 WebSocket 上传/下载的**原始音视频帧字节数**（不含文本、事件头）<br>• 与模型推理复杂度解耦，适合长时媒体流场景 |
| **典型场景** | • 全双工智能客服（用户说话时 AI 实时思考并准备回答）<br>• 多轮语音助手（支持打断、追问、工具调用如查天气）<br>• 教育陪练（语音输入+视频观察+实时反馈+发音纠正）<br>• 会议实时纪要（多说话人音频+内容摘要+行动项提取） | • 实时语音转写服务（纯 ASR 后处理）<br>• 监控视频流异常检测（`qwen-video-realtime-v1` 分析帧序列）<br>• 低延迟音视频通话中的元数据增强（如发言人标签、静音检测）<br>• 边缘设备音视频预处理管道（仅需原始帧转发） |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 你需要构建**具备完整对话智能的实时应用**，而非单纯媒体处理；
- 业务依赖**语义理解、上下文记忆、工具执行或联网搜索**（例如：“帮我订明天北京到上海的高铁票”）；
- 要求**精细控制语音交互体验**：如自定义 VAD 灵敏度、混合多通道音频输入、WAV 直播输出；
- 开发团队具备处理**复杂事件状态机**的能力（如处理 `mcp_approval_request` → 执行 → `conversation.item.create` → `response.create` 的完整闭环）；
- 愿意接受稍高的 Token 成本，换取端到端的 AI 能力集成。

### 选择 Realtime User Guide 当：
- 你的核心需求是**超低延迟的原始音视频流处理**，且已有成熟的 ASR/TTS/前端渲染模块；
- 场景本质是**媒体管道增强**（如给视频流打时间戳标签、对音频流做声纹聚类），无需 LLM 参与决策；
- 需要严格保障**端到端延迟 ≤300ms**，且能接受牺牲语义能力换取确定性时延；
- 架构已基于 WebSocket 构建，且**拒绝引入新协议（WebRTC/AOQ）或复杂事件模型**；
- 成本敏感于**长时媒体流传输**（如 10 分钟监控视频分析），此时按字节计费显著优于 Token 计费。

## 技术选型参考（致开发者）

| 选型考量 | Omni Realtime API | Realtime User Guide |
|----------|-------------------|---------------------|
| **开发复杂度** | ⚠️ 高：需实现事件驱动状态机、处理 VAD 状态跃迁、管理工具调用生命周期 | ✅ 低：接近传统 WebSocket 流式读写，`audio_chunk` → `response_chunk` 线性映射 |
| **调试友好性** | ✅ 高：所有事件含明确类型（`input_audio_buffer.speech_stopped`）、错误码、trace_id；SDK 提供日志钩子 | ⚠️ 中：JSONL 事件较简略（如仅 `"event": "speech_started"`），缺乏上下文字段 |
| **扩展性** | ✅ 强：支持新增模型、工具类型、VAD 算法，协议设计预留扩展字段 | ❌ 弱：模型与功能绑定紧密，`qwen-audio-realtime-v1` 升级即视为新接口 |
| **容错与恢复** | ✅ 会话级恢复：连接断开后，若携带 `session_id` 可续接未完成响应（部分模型支持） | ❌ 无状态：断连即丢失全部上下文，必须重建连接并重传缓冲帧 |
| **合规与安全** | ✅ 支持 MCP 工具的 `server_url` HTTPS 强制校验、`authorization` 字段隔离 | ✅ 传输层加密（WSS），但无应用层工具安全策略 |

> **重要提醒**：  
> - 若项目需同时满足“低延迟”与“强语义”，**不可混用两套 API**。Omni Realtime 已内置优化的端到端延迟（实测 P95 < 450ms），无需额外对接 Realtime User Guide 做底层透传。  
> - Realtime User Guide 文档中提及的“支持任意 Qwen 模型”为历史遗留描述，**当前生产环境严格限定为两个专用模型**，请以控制台可用模型列表为准。  
> - Omni Realtime 的 `qwen3.8-omni-flash-realtime` 模型支持 `repetition_penalty=0`，适合生成重复性内容（如播报列表），此能力在 Realtime User Guide 中不存在。  

根据实际需求，建议优先使用 Omni Realtime API 构建新一代实时智能体；仅当现有系统已深度耦合 Realtime User Guide 且无语义升级计划时，维持其使用。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


