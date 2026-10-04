# 实时 API 与 Omni 实时 API 对比

本文旨在帮助开发者清晰理解百炼平台两类核心实时推理接口的定位差异、能力边界与技术约束，为语音交互、多模态智能体、车载系统、AI 坐席等低延迟场景下的技术选型提供客观、可落地的决策依据。Realtime API 聚焦**高保真语音与强上下文文本协同**，而 Omni 实时 API 定位为**统一事件驱动的多模态流式底座**，二者在协议设计、模型生态、安全模型与工程适配路径上存在系统性差异。

## 关键维度对比

| 维度 | Realtime API | Omni 实时 API |
|------|--------------|----------------|
| **协议与连接方式** | WebSocket 长连接；需手动管理帧序列与会话生命周期；依赖 `session_id` 显式标识会话 | WebSocket 长连接；基于标准化事件（`event` 字段）驱动；会话由连接上下文隐式建立，无显式 `session_id` 管理要求 |
| **输入格式** | 支持结构化帧类型：`input.audio`（PCM/WAV）、`input.text`、`input.tool_result`；音频须严格满足 16kHz/单声道/16-bit PCM | 支持事件化输入：`input_audio`（仅 16kHz 单声道 `int16` PCM 分片）、`input_text`、`input_image`（Base64 编码 JPEG/PNG）；支持多模态混合输入（如语音+截图同步发送） |
| **输出格式** | 流式帧响应：`output.text.delta`、`output.audio.chunk`（ulaw/alaw）、`tool_call` 等；支持 token 级别增量返回与控制帧注入 | 流式事件响应：`output_text_delta`、`output_audio_chunk`、`output_image`、`tool_use_request`；所有输出均带 `event` 类型标识，语义更明确 |
| **支持模型** | 专用实时优化模型：<br>• `qwen-audio-realtime-v1`（语音端到端）<br>• `qwen2.5-7b-instruct-realtime-v1`（文本交互）<br>• *不支持图文模型或跨模态联合推理* | 统一多模态实时模型：<br>• `omni-realtime-202409` 及后续版本<br>• 内置 ASR/TTS/VLM/LLM 四合一能力，支持动态模态组合（如“听用户说话 + 看屏幕内容 + 生成回复”） |
| **API 端点** | `wss://dashscope.aliyuncs.com/realtime/v1/chat`<br>（需 `Authorization` Header + `X-DashScope-Model` Header） | `wss://dashscope.aliyuncs.com/api/v1/omni/realtime?model=...&api_key=...`<br>（认证参数通过 URL Query 传递） |
| **计费方式** | 按 **实际消耗 token 数 + 音频处理时长（秒）** 双维度计费；工具调用单独计费 | 按 **总处理时长（秒） + 输出 token 数 + 多模态附加单元（如图像解析次数）** 综合计费；输入图像、并发音频流等触发额外计量项 |
| **典型场景** | • 语音助手（纯语音对话闭环）<br>• 客服坐席实时话术建议（麦克风流 + 文本提示）<br>• 需强中断控制（`input_interrupt`）与工具同步反馈的交互系统 | • 智能座舱（语音指令 + 中控屏截图分析）<br>• 远程协作白板（实时语音 + 手写笔迹图像识别）<br>• 视频会议 AI 助手（ASR + 关键帧理解 + TTS 总结） |
| **客户端 SDK 支持** | 提供 AOQ 官方 SDK（Python/JS），封装帧序列化、重连逻辑、会话状态机 | 无官方 SDK；推荐基于标准 WebSocket 库自行封装事件处理器；社区已有 TypeScript/Go 的轻量事件适配器示例 |
| **安全与部署约束** | 允许浏览器直连（`api_key` 可置于 Header）；但生产环境仍建议后端代理 | **禁止浏览器直连**；`api_key` 必须通过服务端代理中转，否则视为高危泄露（文档强制要求） |
| **会话生命周期** | 单连接最长 30 分钟；`session_id` 不可跨连接复用；超时需重建连接并新建会话 | 单次会话最长 300 秒（5 分钟）；支持主动 `ping/pong` 维持连接；无 `session_id`，会话状态由服务端自动关联上下文 |

## 各方案适用场景建议

### ✅ 选择 Realtime API 当：
- 场景以**语音为核心输入输出通道**，且对语音质量、端到端延迟（<300ms）、中断响应（如用户说“等等”立即停音）有严苛要求；
- 业务逻辑依赖**确定性工具调用流程**（如查天气 → 调用天气 API → 同步返回结果 → 继续对话），需客户端精确控制 `tool_use_request` 与 `input.tool_result` 时序；
- 已有成熟 WebSocket 客户端框架，且团队熟悉帧协议开发（如自研语音 SDK 集成）；
- 不涉及图像、视频等非文本/语音模态，无需跨模态联合理解。

### ✅ 选择 Omni 实时 API 当：
- 场景需**融合多种输入模态**（例如：用户边说话边用手机拍摄设备故障部位，系统需同步理解语音指令与图像内容）；
- 架构倾向**事件驱动、松耦合设计**，希望用统一事件模型（`input_text`/`input_image`/`output_audio_chunk`）降低客户端适配复杂度；
- 需要**内置 ASR/TTS/VLM 能力开箱即用**，避免自行集成多个独立模型服务；
- 项目具备服务端代理能力，可规避 `api_key` 前端暴露风险；
- 会话时长较短（<5 分钟），且能接受服务端主导的上下文生命周期管理。

## 技术选型参考（面向开发者）

| 评估项 | Realtime API | Omni 实时 API | 建议动作 |
|--------|--------------|----------------|----------|
| **是否需要图像理解？** | ❌ 不支持 | ✅ 原生支持 `input_image` | 若含图像需求，直接排除 Realtime API |
| **是否必须浏览器直连？** | ✅ 支持（Header 认证） | ❌ 强制后端代理 | 若无法部署代理服务，优先 Realtime API |
| **是否需毫秒级语音中断？** | ✅ 支持 `input_interrupt` 帧，响应延迟 <100ms | ⚠️ 中断通过 `cancel` 事件实现，平均延迟约 200–400ms | 对中断敏感场景（如儿童教育机器人），Realtime API 更可靠 |
| **是否需跨模态上下文对齐？** | ❌ 各模态独立处理 | ✅ 支持语音+图像+文本在同一 context window 内联合建模 | 如“这个按钮在哪？”（语音）+ 截图，必须选 Omni |
| **团队 WebSocket 开发经验** | 中等（需处理帧协议、重连、会话冲突） | 较低（事件 JSON 结构简单，文档定义清晰） | 新团队可优先 Omni 降低接入门槛 |
| **长期演进预期** | 模型扩展聚焦语音/文本实时优化，多模态非重点方向 | 百炼主推的下一代实时底座，持续增强 VLM 时延与多源融合能力 | 新项目建议评估 Omni 的长期兼容性 |

> **重要提醒**：两类 API **不互为替代，亦不兼容迁移**。Realtime API 的 `qwen-audio-realtime-v1` 与 Omni 的 `omni-realtime-202409` 是完全不同的模型架构与服务栈。请勿尝试将 Realtime 的 `session_id` 或帧格式用于 Omni 接口，反之亦然。首次接入前，务必通过 [快速开始指南](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 与 [实时多模态入门](../../raw/model-api-reference/omni-realtime-api/omni-realtime-quick-start.md) 完成最小可行验证。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


