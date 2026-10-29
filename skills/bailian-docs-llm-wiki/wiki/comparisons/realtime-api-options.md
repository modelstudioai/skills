# 实时交互API方案对比：Omni Realtime API 与 Realtime API 用户指南

本对比旨在帮助开发者在百炼平台多模态实时交互场景中，清晰识别 **Omni Realtime API** 与 **Realtime API 用户指南** 两类核心流式接口的技术定位、能力边界与适用约束，避免因模型选型或协议误用导致集成失败、功能缺失或计费异常。二者虽均基于 WebSocket 实现低延迟双向通信，但在设计哲学、输入/输出模态、控制粒度、模型架构及工程适配复杂度上存在本质差异：Omni Realtime API 面向**统一多模态会话引擎**（语音+文本+图像+视频+工具协同），强调事件驱动与状态可编程；而 Realtime API 更聚焦于**轻量级语音闭环链路**（ASR→LLM→TTS），以极简协议支持快速落地语音助手类应用。

---

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API 用户指南 |
|------|-------------------|------------------------|
| **核心定位** | 多模态实时会话引擎（语音+文本+图像+视频+工具调用） | 轻量级语音交互闭环（ASR + LLM + TTS 串联） |
| **通信协议** | WebSocket（主推）、AOQ、WebRTC（见接入方式文档） | WebSocket（强制 `wss://dashscope.aliyuncs.com/api/v1/realtime`） |
| **输入格式** | 结构化事件驱动：<br>• `input_audio_buffer.append`（PCM/WAV Base64）<br>• `input_image_buffer.append` / `video.input.representation_compact`（Qwen3.8+）<br>• 支持多通道音频（2/4声道）、空间音频 | 原始音频帧流：<br>• Base64 编码 PCM chunk（≤20ms/帧，推荐320字节@16kHz）<br>• 仅支持单声道语音输入 |
| **输出格式** | 异步事件流：<br>• `response.content_part.added`（文本流）<br>• `response.audio.delta`（PCM 音频流）<br>• `conversation.item.created`（结构化对话项）<br>• 支持 `text` 或 `text+audio` 混合模态输出 | 结构化响应事件：<br>• `response.text`（识别文本或大模型回复）<br>• `response.audio.delta`（合成音频流）<br>• `response.done`（响应结束）<br>• 输出模态由模型决定，不可动态切换 |
| **支持模型** | • Qwen3.8-Omni-Flash-Realtime（全能力：视频、MCP、多通道音频、semantic_vad_ec）<br>• Qwen3.5-Omni-Plus/Flash-Realtime（语音+文本+Function Calling+搜索）<br>• 版本化模型（如 `qwen3-omni-flash-realtime-2025-09-15`） | • `qwen-audio-realtime-v1`（ASR+LLM混合）<br>• `qwen-tts-realtime-v2`（纯TTS）<br>• 模型能力固定，不支持视频、图像、工具调用或VAD配置 |
| **API 端点** | 多端点支持：<br>• WebSocket：`wss://dashscope.aliyuncs.com/api/v1/omni-realtime`（主推）<br>• AOQ/WebRTC：见[模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) | 单一端点：<br>• `wss://dashscope.aliyuncs.com/api/v1/realtime?model={model}&api_key={token}&sample_rate=16000` |
| **会话控制方式** | 全事件驱动：<br>• `session.update` 配置全局参数（模态、音色、VAD、tools等）<br>• `input_audio_buffer.commit`（Manual VAD）或自动 commit（VAD 模式）<br>• `response.create` 显式触发生成<br>• `response.cancel` 中断响应 | 简化控制帧：<br>• 首帧必须为 `{"type": "session.update", ...}` 设置 `input_audio_format`/`output_audio_format`<br>• 无显式触发/取消机制，依赖语音输入自然结束或超时 |
| **VAD（语音活动检测）** | • 支持 `server_vad`（Qwen3.5）、`semantic_vad`（Qwen3.5）、`semantic_vad_ec`（Qwen3.8）<br>• 可配置 `idle_timeout_ms`、`threshold` 等精细参数<br>• 支持语义级静音判断与端点优化 | • 仅隐式 VAD（由 ASR 模型内部处理）<br>• 无客户端可配置参数，无法调整灵敏度或超时逻辑 |
| **工具调用能力** | • 支持 Function Calling（`type=function`）<br>• 支持 MCP（`type=mcp`，需公网 HTTPS server_url）<br>• `tools` 与 `enable_search` 互斥 | • **不支持任何工具调用或外部函数集成**<br>• 不支持联网搜索 |
| **计费方式** | • 按 **输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md) + 输出音频时长（秒）** 分项计费<br>• 多通道音频按声道数倍增 [Token](../concepts/token.md) 计费（如2声道=2×单声道）<br>• 视频输入按 `representation_compact` 级别折算 Token | • 按 **会话时长（秒）** 计费（从连接建立到 `session.end` 或超时）<br>• 与 Token 数量、音频大小无关<br>• 单连接最长计费 15 分钟 |
| **典型场景** | • 智能会议助手（实时转录+发言人分离+PPT图像理解+会议纪要生成）<br>• 多模态客服终端（用户上传截图+语音提问+调用订单系统MCP）<br>• 语音交互机器人（空间音频输入+视频反馈+多轮工具协同） | • 智能座舱语音助手（“打开空调”→识别→执行→合成反馈）<br>• IVR 电话客服（语音导航+简单问答闭环）<br>• 实时字幕生成（ASR 输出直出，无需LLM推理） |

---

## 各方案适用场景建议

### ✅ 推荐选用 **Omni Realtime API** 当：
- 应用需融合**语音、文本、图像、视频**任意两种及以上模态；
- 要求**细粒度会话控制**：如动态切换音色、实时调整 VAD 灵敏度、手动提交音频块、取消进行中响应；
- 需集成**外部系统能力**：通过 Function Calling 调用内部 API，或通过 MCP 连接标准化工具服务（如 CRM、ERP）；
- 场景对**低延迟与高保真音频**有严苛要求：如支持 48kHz 输出采样率、空间音频、多通道输入；
- 开发团队具备 WebSocket 事件状态机开发经验，能处理 `session.created` → `response.done` 全生命周期事件流。

### ✅ 推荐选用 **Realtime API 用户指南** 当：
- 应用聚焦**纯语音交互闭环**（ASR识别后直接合成反馈），无需图像/视频理解或外部工具；
- 追求**最快集成路径**：仅需发送音频帧 + 解析 `response.text`/`response.audio.delta`，无会话状态管理负担；
- 对**成本确定性要求高**：按秒计费，无 Token 波动风险，适合短时高频调用（如每通电话平均 30 秒）；
- 目标部署环境受限：如车载嵌入式设备，需最小化 SDK 体积与内存占用（Realtime API 协议更轻量）；
- 当前阶段无需语义 VAD 或自定义静音策略，接受模型默认端点检测行为。

---

## 技术选型参考（面向开发者）

| 选型考量点 | Omni Realtime API | Realtime API 用户指南 | 建议动作 |
|------------|-------------------|------------------------|----------|
| **是否需要图像/视频理解？** | ✅ 支持（Qwen3.8+） | ❌ 不支持 | 若含视觉需求，**必须选 Omni** |
| **是否需调用数据库/API/第三方服务？** | ✅ 支持 Function Calling & MCP | ❌ 不支持 | 若需业务系统联动，**必须选 Omni** |
| **是否要求输出 48kHz 高清音频？** | ✅ 支持（`audio.output.format.sample_rate=48000`） | ❌ 仅支持 24kHz（文档未声明更高采样率） | 若为专业音频场景，**优先 Omni** |
| **团队是否熟悉事件驱动编程？** | ⚠️ 需维护会话状态机（`session`, `item`, `response` 多对象生命周期） | ✅ 协议极简（帧进→事件出） | 若团队无 WebSocket 状态管理经验，**Realtime API 上手更快** |
| **对计费模型敏感度？** | ⚠️ Token 成本波动大（视频/多声道显著抬升） | ✅ 固定每秒单价，可精准预估 | 若预算严格受限且语音为主，**Realtime API 更可控** |
| **是否需支持方言/小语种 ASR？** | ⚠️ 当前文档未明确列出方言支持列表（以 Qwen-Omni 系列 ASR 能力为准） | ✅ 明确支持中文普通话、英文及部分方言 | 若方言是刚需，**优先验证 Realtime API 的方言覆盖度** |

> **重要提醒**：  
> - **不要混用两类 API 的参数与事件**：`session.update` 在 Omni 中是 JSON 对象，在 Realtime 中是顶层控制帧；`response.audio.delta` 在 Omni 中属于 `response.content_part.added` 子事件，在 Realtime 中是独立顶级事件。  
> - **认证方式不同**：Omni Realtime API 使用标准 DashScope `Authorization: Bearer <api_key>`（Header）或 JWT `access_token`（WebSocket 查询参数，具体见接入文档）；Realtime API **强制要求 `api_key` 查询参数**（非 `access_token`），且有效期仅 5 分钟。  
> - **错误处理范式不同**：Omni 统一返回 `error` 事件并携带 `param` 字段（如 `"session.modalities"`）便于精确定位；Realtime API 错误多表现为连接拒绝或帧解析失败，需结合日志与连接参数排查。  

请根据实际产品需求、技术栈成熟度与长期演进规划，审慎选择。如需跨方案迁移，建议优先复用音频采集与播放模块，重点重构会话控制层与事件处理器。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


