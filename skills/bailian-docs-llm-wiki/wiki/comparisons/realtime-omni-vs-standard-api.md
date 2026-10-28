# 实时交互能力对比：Omni Realtime API 与标准实时 API

本文旨在帮助开发者清晰理解百炼平台两类核心实时交互接口的定位差异与技术边界，为语音助手、智能客服、会议纪要、多模态交互等低延迟场景提供可落地的技术选型依据。Omni Realtime API 是面向**端到端全链路实时性与多模态协同**深度优化的新一代协议；而标准 Realtime API（以下简称“标准实时 API”）是面向**流式 ASR+LLM 协同推理**的通用实时接口，设计更轻量、接入更直接。二者在协议栈、能力纵深、模型支持及工程约束上存在系统性差异，不可简单互换。

## 关键维度对比

| 维度 | Omni Realtime API | 标准实时 API |
|------|-------------------|--------------|
| **协议栈支持** | 支持 AOQ、WebSocket、WebRTC 三协议，WebRTC 原生支持音视频双向低延迟传输（<200ms 端到端） | 仅支持 WebSocket（`wss://.../realtime/v1/chat`），无 WebRTC 或 AOQ 原生支持 |
| **输入格式** | 多模态混合输入：<br>• 音频：`pcm`（全模型）或 `wav`（Qwen3.5 系列）；采样率支持 `8k/16k/24k/48k`（Qwen3.5）、强制 `16k`（Qwen3.8 多通道）<br>• 文本、图像、视频（Qwen3.8-Omni-Flash-Realtime 支持 `video.input.representation_compact`） | 仅支持音频流输入：<br>• 严格限定 `pcm` 格式、`16kHz` 单声道<br>• 不支持视频、图像、文本混入（需预处理为音频或分通道调用） |
| **输出格式** | 可配置模态组合：<br>• `["text"]`（纯文本）或 `["text","audio"]`（TTS 音频 + 文本）<br>• 音频输出支持 `pcm` / `wav`，采样率 `8k/16k/24k/48k`（Qwen3.5）、默认 `24k`（Qwen3.8） | 仅支持文本[流式输出](../concepts/streaming-output.md)：<br>• `output.text.delta` 事件逐 token 返回<br>• **不生成音频**，无 TTS 能力；ASR 结果亦不返回原始转录文本（需额外调用 ASR 接口） |
| **支持模型** | 专属 Omni 系列实时模型：<br>• `qwen3.8-omni-flash-realtime`（主力推荐）<br>• `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`<br>• 实验性版本（如 `2025-09-15`） | 专用实时 ASR+LLM 模型：<br>• `qwen-audio-realtime-*`（语音理解为主）<br>• `qwen-vl-realtime-*`（视觉语言流式理解）<br>• **不兼容 Omni 系列模型** |
| **API 端点** | 多协议入口：<br>• WebSocket: `wss://dashscope.aliyuncs.com/omni-realtime/v1/chat`<br>• WebRTC: 通过信令服务协商 ICE/SDP<br>• AOQ: 专有长连接网关 | 单一 WebSocket 端点：<br>• `wss://dashscope.aliyuncs.com/realtime/v1/chat?model=...&api_key=...&stream=true` |
| **会话控制能力** | 强会话生命周期管理：<br>• `session.update` 动态重配 VAD、音色、工具、搜索等<br>• 支持 `server_vad` / `semantic_vad` / `semantic_vad_ec` 三级语音活动检测<br>• `idle_timeout_ms`（部分模型）、`smooth_output`（实验性）等细粒度控制 | 基础会话控制：<br>• `session.update` 仅支持 system [prompt](../guides/prompt.md)、input format 等上下文配置<br>• **无 VAD 配置能力**，依赖客户端静音检测或服务端固定策略<br>• 不支持运行时修改音色、输出格式、工具等 |
| **高级功能支持** | 全面支持：<br>• 工具调用（Function Calling & MCP）<br>• 联网搜索（`enable_search`，仅限指定模型）<br>• 输入音频自动转录（内置 `qwen3-asr-flash-realtime`）<br>• 多轮对话状态保持与中断恢复 | **完全不支持**：<br>• 无 Function Calling / MCP<br>• 无联网搜索<br>• 无内置 ASR 转录（需前置调用独立 ASR API）<br>• 无工具集成能力 |
| **计费方式** | 按 **实际消耗的输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md) + 音频时长（秒）** 分项计费：<br>• 文本 [Token](../concepts/token.md) 按标准模型计费规则<br>• 音频输入按采样点数折算（16kHz PCM ≈ 16000 pts/sec）<br>• 音频输出按生成时长（秒）计费<br>• 工具调用、搜索等附加能力单独计费 | 按 **连接时长（秒） + 输入音频时长（秒） + 输出文本 Token** 计费：<br>• 连接建立即开始计时（含握手、空闲期）<br>• 音频输入按实际接收字节数折算（16kHz PCM 单声道 = 16000 × 2 bytes/sec）<br>• 文本输出 Token 按标准规则计费<br>• **无音频输出费用（因不生成音频）** |
| **典型场景** | • 全双工语音助手（用户说话时模型实时思考并打断）<br>• 视频会议实时纪要（音视频同步输入 + TTS 总结播报）<br>• 智能客服坐席辅助（语义 VAD 过滤客户语气词，工具调用查订单）<br>• 多模态教育交互（学生举手视频 + 提问语音 → 图文+语音反馈） | • 语音会议转写与摘要（ASR 后接 LLM 流式摘要）<br>• 单向语音指令执行（如“播放新闻”，无 TTS 反馈）<br>• 实时音视频内容理解（摄像头帧流 + 旁白语音分析）<br>• 轻量级语音 Bot（仅需文本响应，无需语音合成） |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 产品需要 **端到端语音交互闭环**（语音输入 → 模型理解 → TTS 语音输出 + 文本），且对首字延迟（TTFT）和端到端延迟（E2E Latency）敏感（目标 < 800ms）；
- 场景涉及 **多模态融合输入**（如视频画面 + 用户语音 + 文本指令），或需 **语义级语音活动检测**（如客服场景中精准识别客户情绪停顿）；
- 业务逻辑依赖 **实时工具调用**（查库存、改订单、发通知）或 **联网动态信息获取**（查天气、搜新闻）；
- 架构允许采用 WebRTC 或 AOQ 协议，并具备相应客户端 SDK 集成能力（如 Web、iOS、Android 原生 App）；
- 团队具备事件驱动编程经验，能妥善处理 `response.content_part.added`、`input_audio_buffer.commit` 等细粒度事件。

### 选择标准实时 API 当：
- 核心需求是 **高吞吐、低成本的流式语音转写+理解**，且无需模型语音反馈（TTS）；
- 输入源单一（纯音频流），且采样率、声道数严格可控（16kHz 单声道 PCM）；
- 项目处于快速验证阶段，需最小化接入成本，优先使用官方 WebSocket SDK 并复用现有 ASR 流水线；
- 场景对 VAD 精度要求不高，可接受客户端静音检测或服务端基础策略；
- 无工具调用、联网搜索等扩展需求，纯文本推理即可满足业务闭环。

## 技术选型参考（面向开发者）

| 评估项 | 推荐方案 | 说明 |
|--------|----------|------|
| **是否需要 TTS 音频输出？** | ✅ Omni Realtime API | 标准实时 API 完全不提供音频生成能力 |
| **是否需 WebRTC 原生支持（如浏览器免插件音视频通话）？** | ✅ Omni Realtime API | 标准实时 API 仅 WebSocket，无法满足 P2P 音视频传输需求 |
| **输入是否含视频/图像？** | ✅ Omni Realtime API（Qwen3.8+） | 标准实时 API 仅支持音频流，多模态需拆分为独立请求 |
| **是否需语义级 VAD（如过滤“呃…”、“啊…”等填充词）？** | ✅ Omni Realtime API（`semantic_vad` / `semantic_vad_ec`） | 标准实时 API 无 VAD 配置接口，仅基础静音检测 |
| **是否需运行时调用外部工具（API、数据库）？** | ✅ Omni Realtime API | 标准实时 API 明确不支持 Function Calling 或 MCP |
| **是否需联网实时搜索最新信息？** | ✅ Omni Realtime API（指定模型） | 标准实时 API 不支持 `enable_search` 参数 |
| **是否追求最低接入门槛与最快上线？** | ✅ 标准实时 API | WebSocket 协议简单，事件模型扁平（`input.audio` → `output.text.delta`），SDK 封装成熟 |
| **是否已有成熟 ASR 流水线，只需 LLM 流式理解？** | ✅ 标准实时 API | 可将 ASR 结果作为 `input.text` 注入，避免 Omni 内置 ASR 的冗余计算与计费 |
| **是否对连接稳定性与心跳管理要求极高（如金融级会话）？** | ⚠️ Omni Realtime API（WebRTC 更优）<br>⚠️ 标准实时 API（需严格实现 ping/pong） | Omni 的 WebRTC 协议自带 NAT 穿透与重传机制；标准 API 要求客户端每 20s 主动 ping，否则断连风险高 |

> **重要提醒**：  
> - **模型不可混用**：Omni Realtime API 仅接受 `qwen*-omni-*` 系列模型；标准实时 API 仅接受 `qwen-*-realtime-*` 系列。错误模型 ID 将返回 `400 Bad Request`。  
> - **计费差异显著**：若误用 Omni Realtime API 仅做纯文本流式推理（禁用音频 I/O），仍将产生音频通道保活费用；反之，标准实时 API 无法规避连接时长计费。请根据真实流量特征测算成本。  
> - **文档以运行时为准**：参数行为（如 `temperature` 是否生效、`audio.output.format.sample_rate` 支持范围）请以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 和 [Realtime API 事件协议](../../raw/model-api-reference/realtime-api-user-guide.md) 的最新字段定义为准，静态文档可能存在滞后。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


