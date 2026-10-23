# Omni Realtime API 与 Realtime API 用户指南对比

本对比旨在帮助开发者清晰理解百炼平台两类核心实时交互 API 的定位差异、能力边界与技术约束，避免因模型选型或协议误用导致延迟升高、功能缺失或集成失败。Omni Realtime API 是面向**多模态、低延迟、强交互性终端场景**的下一代实时接口；而 Realtime API 是面向**通用语音/文本流式交互**的成熟稳定方案，二者在架构设计、协议支持、模型能力及适用层级上存在系统性差异。本文基于最新（2025年Q3）文档规范整理，适用于新项目技术选型与存量系统迁移评估。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心定位** | 多模态实时交互引擎：语音+文本+工具+视频表征端到端同步处理，强调语义级 VAD 与音画协同输出 | 通用流式响应接口：聚焦低延迟文本生成与音频流接入，以“语音输入→文本输出”为主干链路 |
| **输入格式** | 支持多通道 PCM 音频（1/2/4 声道）、文本、工具调用请求；`input_audio_format` 严格限定为 `pcm`（服务端事件），但客户端可声明 `wav`（需自行编码）；采样率支持 8/16/24/48 kHz（依模型而异） | 仅支持单声道音频流，格式为 `"pcm16"`（默认）或 `"opus"`；采样率固定为 16 kHz（PCM）；不支持多通道或视频帧输入 |
| **输出格式** | 多模态混合输出：`["text", "audio"]`（默认）、`["text"]`、`["audio"]`；音频输出为 24 kHz PCM（默认）或可配采样率的 WAV；支持 `smooth_output` 控制口语化程度 | 仅支持文本[流式输出](../concepts/streaming-output.md)（`response.text.delta`）；**无原生音频合成（TTS）能力**；音频相关事件仅用于输入反馈（如 `input_audio_buffer.committed`） |
| **支持模型** | 专属 `qwen3.x-omni-*` 系列：<br>• `qwen3.8-omni-flash-realtime`（全能力：MCP + 多通道 + `semantic_vad_ec` + 视频压缩）<br>• `qwen3.5-omni-plus/flash-realtime`（Function Calling + `server_vad`/`semantic_vad`，无 MCP/多通道）<br>• `qwen3-omni-flash-realtime-2025-09-15`（新增 `smooth_output` + `Cherry` 音色） | 通用 `*-realtime` 系列：<br>• `qwen2.5-7b-realtime`、`qwen-audio-realtime`、`qwen-vl-realtime`（多模态需显式启用）<br>• **不支持任何 `qwen3.x-omni-*` 模型**；`qwen1.5-14b-realtime` 已下线 |
| **API 协议与连接方式** | 三协议并行：<br>• **AOQ**（QUIC over UDP，最低端到端延迟，需网络开放 UDP）<br>• **WebSocket**（广泛兼容，SDK 官方支持 Python/Java）<br>• **WebRTC**（浏览器直连，免 SDK，支持媒体协商） | **仅 WebSocket**：<br>• 固定端点 `wss://dashscope.aliyuncs.com/realtime/v1/chat`<br>• 强制 TLS 1.2+，不支持 HTTP 降级或 QUIC |
| **VAD（语音活动检测）能力** | 三级语义增强：<br>• `server_vad`（基础静音检测）<br>• `semantic_vad`（上下文感知断句）<br>• `semantic_vad_ec`（仅 Qwen3.8，支持回声消除协同） | 仅基础 `server_vad`（静音阈值检测），无语义级或回声消除集成 |
| **工具调用（Tool Calling）** | 全面支持：<br>• Function Calling（所有模型）<br>• **MCP（Model Control Protocol）**（仅 `qwen3.8-omni-flash-realtime`）<br>• 工具与联网搜索 `enable_search` **互斥**（不可共存） | **不支持任何工具调用**；无 `tools` 字段；无 MCP 或 Function Calling 接口定义 |
| **联网搜索** | 支持 `enable_search: true`（Qwen3.8/Qwen3.5 系列），但与 `tools` 冲突，启用后自动禁用工具调用 | **不支持联网搜索**；无相关参数或事件 |
| **会话生命周期管理** | 事件驱动模型：<br>• 自动 `session.created` → 可选 `session.update` → `input_audio_buffer.append`/`.commit` → `response.create`（Manual 模式）→ 监听 `response.content_part.added`/`.done` | 简化事件流：<br>• 连接即初始化 → `session.update` → `input_audio_buffer.append` 或 `input_text` → 监听 `response.text.delta`/`.done` |
| **计费方式** | 按 **实际消耗的输入 Token + 输出 Token + 音频时长（秒）** 分项计费；多通道音频、MCP 调用、视频表征压缩均产生额外计量单元 | 按 **输入 Token + 输出 Token** 计费；音频仅按传输时长计入网络带宽成本，**不单独计费音频处理** |
| **典型场景** | • 智能会议助手（实时转录+发言人分离+PPT摘要+工具调用）<br>• 语音交互终端（车载/家居，需多声道麦克风+本地 VAD+TTS 同步）<br>• 多模态客服坐席（语音+屏幕共享+知识库检索+操作自动化） | • 实时语音转写（会议记录、访谈速记）<br>• 文本流式对话机器人（客服问答、教育陪练）<br>• 音频内容摘要（播客/录音转文字） |

## 适用场景建议

### 选择 Omni Realtime API 当：
- ✅ 应用需**同步输出语音与文本**（如 TTS 朗读 + 屏幕字幕）；
- ✅ 输入源为**多麦克风阵列**（如会议设备、智能音箱），需 2/4 声道音频处理与 `semantic_vad_ec` 抗干扰；
- ✅ 业务逻辑依赖**深度工具集成**（如调用内部 CRM、执行数据库查询、触发 IoT 设备），且需 MCP 协议保障控制精度；
- ✅ 场景对**端到端延迟极度敏感**（目标 <300ms），可接受 AOQ 协议部署复杂度；
- ✅ 需要**视频表征压缩**（`representation_compact`）或**动态调整回复风格**（`smooth_output` 口语化/书面化）。

### 选择 Realtime API 当：
- ✅ 项目以**语音转文字（ASR）为核心需求**，无需 TTS 或多模态输出；
- ✅ 客户端环境受限（如老旧浏览器、企业内网禁 UDP），仅能使用标准 WebSocket；
- ✅ 业务逻辑简单，**无需工具调用、联网搜索或复杂 VAD**，仅需基础流式响应；
- ✅ 团队熟悉传统 WebSocket 开发模式，希望快速集成、最小学习成本上线；
- ✅ 对音频处理要求为**单声道、16kHz PCM 标准输入**，无多通道或高保真需求。

## 技术选型参考（面向开发者）

| 评估项 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| **新项目启动（智能硬件/会议SaaS）** | ✅ Omni Realtime API | 原生支持多通道音频、MCP 工具链、语义 VAD，避免后期因能力不足重构；AOQ/WebRTC 提供未来扩展性。 |
| **存量 ASR 服务升级（仅需提升转写质量）** | ⚠️ 优先 Realtime API | 若当前已用 WebSocket 实现 ASR，迁移到 Omni 需重写音频缓冲区管理与事件监听逻辑，ROI 较低；可先通过 `qwen-audio-realtime` 模型优化效果。 |
| **需要 TTS 合成且控制音色/语速** | ✅ Omni Realtime API | Realtime API **完全不提供 TTS**；Omni 支持 `voice`、`audio.output.format.type`、`smooth_output` 等精细控制。 |
| **企业内网部署（UDP 封禁）** | ✅ Realtime API 或 Omni（WebSocket 模式） | Omni 的 WebSocket 模式功能完整，但若需 WebRTC 或 AOQ 则不可行；Realtime API 无协议选项，天然适配。 |
| **需调用内部 API 执行业务动作** | ✅ Omni Realtime API（`qwen3.8-omni-flash-realtime`） | Realtime API 不支持工具调用；Omni 的 MCP 支持结构化指令下发与状态反馈，比 Function Calling 更适合原子化操作。 |
| **成本敏感型轻量应用（如小程序客服）** | ⚠️ Realtime API | Omni 的音频时长计费与多模态能力在纯文本场景中产生冗余成本；Realtime API Token 计费更透明、单价更低。 |

> **重要提醒**：  
> - **协议不可混用**：Omni 的 AOQ/WebRTC 连接无法调用 Realtime API 模型，反之亦然；  
> - **模型不可互通**：`qwen3.8-omni-*` 模型仅响应 Omni 协议，`qwen2.5-7b-realtime` 仅响应 Realtime 协议；  
> - **迁移路径**：从 Realtime 迁移至 Omni 需重写客户端音频流管理、事件监听器及会话状态机，但官方 Python/Java SDK 可显著降低工作量。  

如需进一步验证性能指标（如实测 P95 端到端延迟、不同网络下的 AOQ 丢包率），请参阅《[Omni Realtime API 性能基准测试报告](../../raw/model-api-reference/omni-realtime-api/performance-benchmark.md)》与《[Realtime API 延迟优化指南](../../raw/model-api-reference/realtime-api-user-guide/latency-optimization.md)》。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


