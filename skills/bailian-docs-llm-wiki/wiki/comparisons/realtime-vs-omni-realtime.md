# 实时 API 与 Omni 实时 API 对比

本文档面向百炼平台开发者，旨在清晰对比 **Realtime API** 与 **Omni 实时 API** 的核心能力、技术边界与适用场景，辅助技术选型决策。两类接口均面向低延迟、流式交互场景设计，但定位存在显著差异：  
- **Realtime API** 是**轻量级、模型专用型实时推理通道**，聚焦单模态（文本/音频/视觉）的极致响应速度与确定性控制，适用于对协议简洁性、端侧资源敏感、需深度定制中断逻辑的嵌入式或垂直场景；  
- **Omni 实时 API** 是**全栈式多模态对话引擎接口**，内置 VAD、ASR、TTS、工具调用、联网搜索等完整对话链路能力，面向“开箱即用”的语音助手、智能客服等产品级应用，强调语义连贯性与交互完整性。

以下从关键维度展开结构化对比：

| 维度 | Realtime API | Omni 实时 API |
|------|--------------|----------------|
| **协议与传输方式** | 仅支持 WebSocket（`wss://dashscope.aliyuncs.com/realtime/v1/chat`） | 支持 **WebSocket、AOQ、WebRTC** 三种协议，可按网络环境与终端能力灵活选型（如 WebRTC 适用于浏览器原生音视频通话） |
| **输入格式** | • 文本：`input.text`（纯字符串）<br>• 音频：仅支持 `PCM`（16-bit, 16kHz, mono），单次分片 ≤ 64KB<br>• 不支持图像、视频输入 | • 文本：`conversation.item.create`（支持 `text`, `image_url`）<br>• 音频：`input_audio_buffer.append`，支持 `pcm`/`wav`，采样率 8k/16k/24k/48k Hz；`qwen3.8-omni-flash-realtime` 支持多声道空间音频<br>• 视频：仅 `qwen3.8-omni-flash-realtime` 支持（需启用 `video.input.representation_compact`） |
| **输出格式** | • 仅文本流：`output.delta`（token 级增量）、`output.end`<br>• 不支持原生音频输出（TTS 需自行对接）<br>• 无结构化事件（如工具调用结果、搜索摘要） | • 多模态输出：`["text"]` 或 `["text","audio"]` 可配<br>• 音频输出支持 `pcm`/`wav`（`qwen3.5+` 默认 `wav`，24 kHz）<br>• 结构化事件丰富：`response.content_part.added`（含 `type=text`/`type=audio`/`type=function_call`/`type=search_result`） |
| **支持模型** | • 模型命名统一含 `-realtime` 后缀：<br> `qwen-audio-realtime`、`qwen-vl-realtime`、`qwen2.5-7b-instruct-realtime`<br>• 模型能力垂直聚焦（如纯音频理解、纯图文理解），不跨模态融合 | • 全系 `qwen3` 多模态大模型：<br> `qwen3.8-omni-flash-realtime`、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、实验版 `qwen3-omni-flash-realtime-2025-09-15`<br>• 所有模型原生支持文本+语音双向交互、语义级 VAD、工具调用与联网搜索 |
| **语音活动检测（VAD）** | ❌ 不提供服务端 VAD；需客户端自行实现语音起止检测与分片边界控制 | ✅ 内置三级 VAD：<br> • `server_vad`：基础声学检测<br> • `semantic_vad`：语义有效性过滤（避免静音/噪声触发）<br> • `semantic_vad_ec`：客服增强版（仅 `qwen3.8`），支持上下文感知的打断容忍 |
| **工具调用与扩展能力** | ❌ 不支持 Function Calling、MCP 或联网搜索；系统指令需通过 `session.update.instructions` 静态注入 | ✅ 原生支持：<br> • `tools: [{type: "function"}]` 或 `[{type: "mcp"}]`<br> • `enable_search: true`（模型自主触发联网检索）<br> • 工具调用与搜索互斥，需按业务逻辑选择 |
| **API 端点** | `wss://dashscope.aliyuncs.com/realtime/v1/chat` | • WebSocket：`wss://dashscope.aliyuncs.com/omni/v1/chat`<br>• AOQ/WebRTC：详见对应接入指南（路径不同，协议语义一致） |
| **计费方式** | 按 **实际生成 token 数 + 输入 token 数** 计费（含音频转录 token）；无额外 VAD/ASR/TTS 单独计费项 | 按 **会话粒度综合计费**：<br> • 输入 token（文本/音频转录）<br> • 输出 token（文本 + 音频时长折算）<br> • VAD 调用次数、工具调用次数、搜索请求次数均单独计费（详见《Omni 实时 API 计费说明》） |
| **典型场景** | • 语音转文字实时字幕（低延迟要求 <300ms）<br>• 工业设备语音指令解析（固定指令集，无需语义理解）<br>• 视频流实时图文分析（如监控画面异常识别）<br>• 资源受限终端（如 IoT 设备）上的轻量级流式推理 | • 全双工语音助手（支持自然打断、多轮追问）<br>• 智能客服坐席辅助（实时转录+语义摘要+知识库检索+话术推荐）<br>• 远程会议实时记录与行动项提取（语音→文本→任务工具调用）<br>• 多模态交互应用（语音提问+拍照上传+生成报告） |

## 各方案适用场景建议

### ✅ 推荐选用 **Realtime API** 当：
- 场景为**单模态强实时任务**（如纯音频流 ASR、纯视频帧分析），且对端到端延迟要求极端严苛（P99 < 200ms）；
- 客户端已具备成熟的 VAD、音频预处理、TTS 合成能力，仅需百炼提供底层模型推理服务；
- 需要完全掌控流控逻辑（如自定义中断策略、精细 token 级响应节流）；
- 项目处于原型验证阶段，追求最小依赖、快速集成，无需复杂对话状态管理。

### ✅ 推荐选用 **Omni 实时 API** 当：
- 构建**完整对话式 AI 应用**，需同时处理语音输入、文本生成、语音合成、工具执行、联网搜索等环节；
- 要求开箱即用的**语义级交互能力**（如自动识别用户意图切换模式、根据上下文决定是否调用工具）；
- 目标终端多样（Web 浏览器、移动 App、智能硬件），需协议灵活性（WebRTC 适配原生音视频、AOQ 适配边缘网关）；
- 产品需快速上线，接受标准化对话事件模型（`response.created` → `content_part.added` → `done`），降低客户端开发复杂度。

## 技术选型参考（致开发者）

| 选型考量点 | Realtime API | Omni 实时 API | 建议动作 |
|------------|--------------|----------------|----------|
| **是否需要原生 TTS 输出？** | 否（需自行集成） | 是（内置高质量语音合成） | 若需语音播报，优先 Omni |
| **是否需模型自主触发联网搜索？** | 否 | 是（`enable_search`） | 若业务依赖实时信息，必须选 Omni |
| **是否需在响应中直接返回结构化工具结果？** | 否 | 是（`type=function_call` 事件） | 若需调用数据库/API，Omni 提供端到端闭环 |
| **客户端是否已实现 VAD？** | 是 → 适合 Realtime<br>否 → Omni 更省力 | VAD 全托管（含语义级） | 新项目无 VAD 积累，选 Omni 降本增效 |
| **是否需支持多声道/空间音频？** | 否 | 仅 `qwen3.8-omni-flash-realtime` 支持 | 如涉及会议系统、VR 场景，必须选 Omni + qwen3.8 |
| **是否需视频理解能力？** | 否 | 仅 `qwen3.8-omni-flash-realtime` 支持 | 视频交互场景锁定 Omni qwen3.8 |
| **对连接稳定性要求极高（如金融客服）？** | WebSocket 单连接，超时 300 秒 | 支持 WebRTC（NAT 穿透强）、AOQ（断线续传） | 关键业务推荐 Omni + WebRTC |

> **重要提示**：两类 API **不兼容互通**。Realtime API 的 `model_id`（如 `qwen2.5-7b-instruct-realtime`）无法在 Omni 接口使用；反之亦然。请严格依据模型文档选择对应 API 通道。迁移时需重写客户端通信逻辑与事件处理流程。

---  
*最后更新：2025年4月*

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


