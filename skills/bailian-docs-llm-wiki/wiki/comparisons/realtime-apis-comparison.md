# 实时交互 API 对比：Omni Realtime API 与 Realtime API 用户指南

本文档面向百炼平台开发者，旨在清晰对比两类核心实时交互 API 的技术定位、能力边界与工程实践差异，帮助团队在语音助手、音视频智能体、多模态对话系统等场景中做出精准的技术选型。随着 Qwen-Omni 系列模型的演进，平台已形成**面向全链路多模态实时交互的 Omni Realtime API** 与**面向通用流式文本/音频推理的 Realtime API** 两大技术路径。二者虽均基于 WebSocket 实现低延迟双向通信，但在协议语义、模型支持、事件模型、输入输出控制粒度及适用范式上存在本质区别。本对比不替代具体文档，而是提供结构化决策依据。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **协议与连接模型** | 基于 WebSocket（主推）、AOQ 或 WebRTC；**强会话生命周期管理**，需显式处理 `session.created` → `session.updated` → `response.done` 事件流；支持长连接保活（默认无硬超时，依赖业务心跳） | 基于 WebSocket（`wss://dashscope.aliyuncs.com/realtime/v1/chat`）；**轻量会话模型**，连接即会话，300 秒自动过期（含空闲）；无显式 session 初始化事件，配置通过首条 `session.update` 消息传递 |
| **输入格式** | 结构化事件驱动：<br>• 音频：`input_audio_buffer.append`（Base64 PCM/WAV，支持 1/2/4 声道，采样率 8k–48k）<br>• 文本/图像：`conversation.item.create`<br>• VAD 控制：`turn_detection.type`（`server_vad`/`semantic_vad`/`semantic_vad_ec`） | 分片流式消息驱动：<br>• 音频：`input.audio`（仅支持单通道 PCM，**强制 16kHz**）<br>• 文本：`input.text`（≤ 8192 Unicode 字符/次）<br>• 无原生图像输入支持（`qwen-vl-realtime-v1` 为独立模型路径，非同一接口扩展） |
| **输出格式** | 双模态同步生成：<br>• `modalities: ["text", "audio"]`（默认）或 `["text"]`<br>• 音频输出格式可自由配置（`type`: `pcm`/`wav`；`sample_rate`: 8000–48000 Hz）<br>• 支持 `smooth_output` 风格控制（口语化/书面化） | 模态解耦输出：<br>• `output.text.delta`（token 级增量文本）<br>• `output.audio.chunk`（PCM 音频分块，**固定 16kHz 单通道**）<br>• 无统一模态开关，由模型能力决定输出类型（如 `qwen-audio-realtime-v1` 输出音频，`qwen2.5-7b-instruct-realtime` 仅输出文本） |
| **支持模型** | 专有 Omni 系列模型：<br>• `qwen3.8-omni-flash-realtime`（主力，支持 MCP、`semantic_vad_ec`、视频表征压缩、`smooth_output`）<br>• `qwen3.5-omni-plus/flash-realtime`（兼容，无 MCP/视频/`semantic_vad_ec`）<br>• `qwen3-omni-flash-realtime-2025-09-15`（快照版，启用 `smooth_output`）<br>• ASR 固定使用 `qwen3-asr-flash-realtime` | 通用 Realtime 模型族：<br>• `qwen-audio-realtime-v1`（音频流式 I/O）<br>• `qwen2.5-7b-instruct-realtime`（文本流式 + Function Calling）<br>• `qwen-vl-realtime-v1`（多模态 VL，需单独接入）<br>• **无 Omni 系列模型支持** |
| **API 端点** | 地域化 WebSocket endpoint（如 `wss://dashscope.aliyuncs.com/omni-realtime/v1`），需按部署区域选择；支持 AOQ/WebRTC 备选协议 | 统一 WebSocket endpoint：<br>`wss://dashscope.aliyuncs.com/realtime/v1/chat`（全球可用） |
| **计费方式** | 按 **实际消耗的输入音频时长（秒） + 输出音频时长（秒） + 输入文本 token + 输出文本 token** 分项计费；MCP 工具调用、联网搜索（`enable_search`）另计费用 | 按 **输入 token + 输出 token** 计费；音频输入/输出按等效 token 折算（详见计费文档），**不单独计量音频时长** |
| **典型场景** | • 全栈语音助手（端到端 ASR+LLM+TTS，支持客服语义 VAD）<br>• 多声道会议实时转录与摘要<br>• 需视频表征理解的音视频智能体（如远程医疗问诊）<br>• 要求“说话即响应、停顿即思考”的自然对话流 | • 快速集成的语音聊天机器人（单麦输入+单声道 TTS）<br>• 文本优先的实时客服对话（辅以简单音频播报）<br>• 需要 Function Calling 的自动化工作流（如订单查询）<br>• 轻量级多模态理解（`qwen-vl-realtime-v1` 单独调用） |
| **高级功能支持** | ✅ 语义 VAD（含客服增强版 `semantic_vad_ec`）<br>✅ MCP 工具调用（需公网 HTTPS 443 endpoint）<br>✅ 联网搜索（`enable_search`）<br>✅ 视频表征压缩（`representation_compact`）<br>✅ 多通道音频输入（1/2/4 声道）<br>❌ 不支持跨连接共享会话状态 | ✅ Function Calling（`enable_function_calling`）<br>✅ 跨请求会话状态（`stateful_session`）<br>❌ 不支持 MCP<br>❌ 不支持语义 VAD / 多通道音频 / 视频输入<br>❌ 不支持自定义音频采样率（固定 16kHz） |

## 各方案的适用场景建议

### 选择 Omni Realtime API 当：
- 你的产品是**专业级语音/音视频交互应用**，要求端到端低延迟（<300ms P95）、自然对话节奏（依赖 `semantic_vad_ec` 精准检测用户意图停顿）；
- 需要**多声道音频处理能力**（如双耳录音、会议多源分离）或**视频流理解**（如远程教育白板互动）；
- 业务深度依赖 **MCP（Model Control Protocol）生态工具**（如调用企业内部 CRM、ERP 系统），且工具服务部署在公网 HTTPS 443 端口；
- 对语音输出质量与风格有精细化要求（如客服场景需 `smooth_output=true` 的口语化应答）；
- 工程团队具备 WebSocket 长连接状态管理、事件生命周期处理（如 `response.cancel`、`input_audio_buffer.clear`）的开发经验。

### 选择 Realtime API 当：
- 你正在构建**快速验证型 MVP 或轻量级集成应用**，追求最小接入成本与稳定交付；
- 核心需求是**文本流式生成 + 基础音频播报**（单麦输入+单声道 TTS），无需复杂 VAD 或多模态理解；
- 业务逻辑重度依赖 **Function Calling**（如电商导购、IT 帮助台），且工具 schema 相对静态；
- 运行环境受限（如部分浏览器或 IoT 设备），需依赖 AOQ SDK 提供的自动重连、序列号校验等健壮性保障；
- 团队更熟悉传统 REST/流式 API 模式，希望避免深度定制 WebSocket 事件处理逻辑。

## 技术选型参考（面向开发者）

| 决策因素 | 推荐方案 | 说明 |
|----------|----------|------|
| **是否需要语义级语音活动检测（尤其客服场景）？** | ✅ Omni Realtime API | `semantic_vad_ec` 是 Omni 独有特性，Realtime API 仅提供基础声学 VAD（`server_vad`） |
| **是否需调用 MCP 协议工具（非标准 OpenAPI）？** | ✅ Omni Realtime API | Realtime API 仅支持 Function Calling（OpenAPI Schema），不兼容 MCP |
| **是否必须支持 24kHz/48kHz 高保真音频输出？** | ✅ Omni Realtime API | Realtime API 强制 16kHz，无法提升采样率 |
| **是否已有成熟 AOQ SDK 集成经验？** | ⚠️ Realtime API（优先） | AOQ SDK 对 Realtime API 支持最完善；Omni Realtime API 的 AOQ 封装仍在增强中 |
| **是否需在单次会话中混合处理图像+语音+文本？** | ✅ Omni Realtime API（推荐）<br>⚠️ Realtime API（需组合调用） | Omni 原生支持 `conversation.item.create` 添加图像；Realtime API 中 `qwen-vl-realtime-v1` 需单独建立连接，无法与音频模型同会话混用 |
| **是否对计费透明度要求极高（如需精确按音频秒计费）？** | ✅ Omni Realtime API | 其分项计费模型（音频秒+token）比 Realtime API 的 token 折算更直观可审计 |
| **是否追求最快上线速度（<1人日）？** | ✅ Realtime API | 统一 endpoint、简化参数、丰富 SDK 示例，显著降低初上手门槛 |

> **重要提醒**：  
> - **不要混用两种 API 的模型**：`qwen3.8-omni-flash-realtime` 仅在 Omni Realtime API 中可用；`qwen2.5-7b-instruct-realtime` 仅在 Realtime API 中可用。模型 ID 不互通。  
> - **音频编解码兼容性**：Omni Realtime API 明确支持 `s16le`、`interleaved` PCM 格式；Realtime API 文档未声明编码细节，实践中建议严格遵循 16kHz 单通道 PCM。  
> - **错误处理差异**：Omni Realtime API 使用 `error` 事件携带结构化 code/message；Realtime API 使用 `session.error` 事件，部分错误码（如 `429`）需结合 HTTP 握手阶段响应判断。  
> - **未来演进**：Omni Realtime API 是百炼平台多模态实时交互的战略主干，新能力（如视频流、3D 空间音频）将优先在此路径发布；Realtime API 定位为通用流式基座，保持轻量与稳定。  

请根据上述对比，结合自身产品形态、技术栈成熟度与长期演进规划，审慎选择。如需进一步评估，可联系百炼技术支持获取 PoC 环境与性能压测报告。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


