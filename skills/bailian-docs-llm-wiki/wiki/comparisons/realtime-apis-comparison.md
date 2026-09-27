# 实时类API对比：Omni Realtime API vs Realtime API

本文旨在帮助开发者清晰区分百炼平台两大实时语音交互接口——**Omni Realtime API** 与 **Realtime API**，明确其定位差异、能力边界与技术约束，从而在智能客服、语音助手、会议纪要、音视频分析等低延迟场景中做出高效、稳健的技术选型决策。二者虽同属“实时”范畴，但在架构设计、协议支持、模态能力、会话模型及扩展性上存在本质差异：Omni Realtime API 是面向**多模态原生交互**的下一代会话引擎，而 Realtime API 是面向**轻量流式响应**的经典实时推理接口。

---

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心定位** | 多模态原生实时会话引擎（文本+音频同步生成/理解），支持语义级VAD、工具调用与联网搜索 | 轻量级流式语音-文本双向接口，聚焦低延迟token级响应与客户端主动控制 |
| **输入格式** | 支持 `PCM` / `WAV` 音频流（`8000–48000 Hz`，单/双/四声道）；支持纯文本输入；支持视频表征压缩（仅 `qwen3.8-omni-flash-realtime`） | 仅支持 `PCM`（小端、16-bit、单声道、16kHz，默认）或带标准 RIFF 头的 `WAV`；不支持视频输入 |
| **输出格式** | 可配置 `["text"]` 或 `["text", "audio"]`；音频支持 `pcm`/`wav` 输出，采样率最高 `24000 Hz`（实测支持） | 固定混合输出：文本 token 流 + 可选音频流（需模型支持）；音频仅限 `pcm`（无 wav 支持）；无采样率自定义能力 |
| **支持模型** | 专属 `-realtime` 系列 Omni 模型：<br>• `qwen3.8-omni-flash-realtime`<br>• `qwen3.5-omni-plus/flash-realtime`<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime` | 通用实时模型：<br>• `qwen-audio-2-realtime`（替代旧 `qwen-audio-realtime`）<br>• `qwen-vl-realtime`<br>• `qwen2.5-7b-instruct-realtime` |
| **协议支持** | ✅ AOQ（异步队列）<br>✅ WebSocket<br>✅ WebRTC（端到端媒体传输） | ❌ 仅支持 WebSocket（强制 `wss://.../realtime/v1/chat`） |
| **会话模型** | 基于 **Session 生命周期管理**：需显式 `session.update` 配置模态、VAD、工具等；事件驱动（`session.created`, `input_audio_buffer.speech_started`, `conversation.item.created`） | 基于 **Session ID 绑定**：通过 `session_id` 复用上下文；初始化即发 `init` 消息；事件类型较简（`response.start`, `token`, `response.stop`, `interrupt`） |
| **语音活动检测（VAD）** | ✅ 支持双模式：<br>• `server_vad`（声学级，全模型支持）<br>• `semantic_vad`（语义级，过滤背景音/回应语，仅 `qwen3.8/qwen3.5-omni-*` 支持） | ❌ 不提供 VAD 能力；需客户端自行实现语音端点检测 |
| **工具调用（Function Calling / MCP）** | ✅ 支持 `tools` 数组（含 `type: "mcp"`）；与 `enable_search` 互斥 | ❌ 不支持任何工具调用机制 |
| **联网搜索（Search）** | ✅ `enable_search: true`（仅 `qwen3.8/qwen3.5-omni-*` 支持），可启用来源返回 | ❌ 不支持联网搜索 |
| **音频通道支持** | ✅ 单/双/四声道 PCM 输入（仅 `qwen3.8-omni-flash-realtime`） | ❌ 仅支持单声道 |
| **生成控制参数** | 支持 `temperature`/`top_p`/`top_k`/`max_tokens`/`repetition_penalty` 等（`turbo` 系列除外） | 仅支持 `temperature` 和 `max_output_tokens`（上限 2048）；不支持 `top_p`/`repetition_penalty` 等高级采样参数 |
| **连接生命周期** | 无硬性超时限制（依赖业务层心跳与会话保活）；支持长时会话（如整场会议） | ⚠️ 单连接最长 300 秒；超时必须重连并重建会话 |
| **计费方式** | 按 **实际消耗 [Token](../concepts/token.md) + 音频处理时长（秒）** 计费；多模态输出（含音频）产生额外音频处理费用 | 按 **输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md)** 计费；音频流按帧数折算为等效 Token，无独立音频时长计费项 |
| **典型场景** | • 全双工语音助手（边说边听边思考）<br>• 智能会议纪要（实时转写+摘要+行动项生成+搜索验证）<br>• 多轮语音客服（带工具调用查订单/改预约）<br>• 无障碍交互终端（语义VAD抗噪） | • 实时字幕/语音转写（低延迟文本流）<br>• 简单语音问答（单轮查询+快速回答）<br>• 音视频内容实时分析（如直播评论情感流）<br>• 轻量级IoT语音控制（需快速中断/暂停） |

---

## 适用场景建议

### ✅ 选择 **Omni Realtime API** 当：
- 你需要**真正的全双工、多模态实时交互**（例如用户说话时模型已开始生成音频回复）；
- 场景要求**语义级语音端点检测**（如过滤空调声、键盘声、嗯啊等填充词），提升交互自然度；
- 业务逻辑需深度集成外部系统（如调用 CRM 查询订单、调用天气 API、执行 MCP 工作流）；
- 需要**联网搜索增强回答可信度**（如会议中实时验证数据、引用权威来源）；
- 面向专业终端（如会议硬件、车载系统、医疗录音设备），需支持**多声道音频输入**或**视频轻量表征**；
- 项目周期较长，需构建**高鲁棒性、可扩展的会话引擎**（WebRTC/AOQ 提供部署灵活性）。

### ✅ 选择 **Realtime API** 当：
- 你追求**极简接入与快速上线**，仅需稳定获取低延迟文本流或基础音频响应；
- 客户端已具备成熟 VAD/ASR 能力，只需后端模型完成“理解→生成”环节；
- 场景为**单轮或短轮次交互**（如语音搜索、指令控制），无需复杂会话状态管理；
- 对成本敏感且流量以**纯文本为主**，希望避免多模态带来的音频处理费用；
- 技术栈受限（如仅支持 WebSocket，无法引入 WebRTC 或 AOQ SDK）；
- 需要**强客户端控制能力**（如精确 `interrupt` 中断生成、`pause/resume` 流控）。

---

## 技术选型参考（面向开发者）

| 评估项 | 推荐方案 | 说明 |
|----------|-----------|------|
| **首次集成复杂度** | Realtime API 更低 | 仅需 WebSocket 连接 + `init` + 二进制音频帧，无 Session 配置事件流 |
| **长期维护成本** | Omni Realtime API 更优 | 事件驱动模型更易调试（明确 `speech_started`/`item.created`）；AOQ/WebRTC 提供容灾与边缘适配能力 |
| **功能扩展性** | Omni Realtime API 显著领先 | 工具调用、搜索、多声道、视频支持均为未来场景预留接口；Realtime API 无演进路径 |
| **延迟敏感度（P95 端到端）** | 两者均达 <500ms（典型配置下），但 Omni 在语义VAD+全双工下**感知延迟更低** | Omni 的 `semantic_vad` 可减少无效等待，`server_vad` 与音频解码深度协同优化 |
| **SDK 支持** | 两者均有官方 SDK（Python/JS），但 Omni SDK 封装了 `session.update`、VAD 事件监听、工具调用自动序列化等高级能力 | Realtime SDK 更侧重帧收发与基础事件解析 |
| **错误排查效率** | Omni Realtime API 更高 | 丰富服务端事件（如 `input_audio_buffer.speech_stopped`、`tool.use_failed`）提供精准归因；Realtime 错误多聚合为 `4xx/5xx` 状态码 |

> 💡 **一句话决策建议**：  
> 若你的产品目标是「像人一样自然对话」——选 **Omni Realtime API**；  
> 若你的需求是「把语音快速变成文字或简单回答」——选 **Realtime API**。  
> 二者非替代关系，而是**能力分层**：Realtime API 是实时能力的「基座」，Omni Realtime API 是面向下一代交互的「操作系统」。

---  
*最后更新：2024年6月*

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


