# 实时 API 方案对比：Omni Realtime API vs Realtime API User Guide

本对比旨在帮助开发者在百炼平台实时语音与多模态交互场景下，清晰识别 **Omni Realtime API** 与 **Realtime API（User Guide 所述传统方案）** 的核心差异，明确技术边界、能力纵深与适用约束，从而做出高效、可持续的架构选型决策。随着智能交互向低延迟、多模态、强可控方向演进，两类 API 在协议设计、模型抽象、控制粒度和工程集成方式上已形成显著分野——前者面向“会话级智能体”，后者聚焦“管道级音视频流”。

---

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API（User Guide） |
|------|-------------------|----------------------------|
| **定位与范式** | 会话驱动的多模态智能体 API：以 `session` 为上下文单元，支持语义理解、工具调用、联网搜索与混合输出，强调**端到端意图闭环** | 流式音视频处理管道 API：以 `audio frame` 为数据单元，提供 ASR/TTS/轻量对话能力，强调**低延迟媒体流转发与编解码** |
| **输入格式** | 支持多模态混合输入：<br>• 音频：`pcm`/`wav`（Qwen3.5 系列支持 8k/16k/24k/48k；Qwen3.8 多通道强制 16k）<br>• 文本、图像（通过 `conversation.item.create`）<br>• 视频（仅 `qwen3.8-omni-flash-realtime`，启用 `video.input.representation_compact`） | 仅支持音频流输入：<br>• 格式：`pcm`（小端、16bit、单声道）或 `wav`（无头裸 PCM）<br>• 采样率：固定 `16000 Hz`（`sample_rate` 参数仅用于校验）<br>• 不支持文本/图像/视频直接输入 |
| **输出格式** | 混合模态[流式输出](../concepts/streaming-output.md)：<br>• 必含 `text`；可选 `audio`（`pcm` 或 `wav`）<br>• `audio.output.format.sample_rate` 可动态配置（8k/16k/24k/48k，默认 24k）<br>• 输出含完整 WAV 头（当 `format=wav`） | 单一模态事件流输出：<br>• `text_delta`（UTF-8 字符串增量）<br>• `audio_chunk`（裸 PCM 流，16kHz/16bit/mono，**无 WAV 头**）<br>• 不支持 `wav` 封装或自定义采样率输出 |
| **支持模型** | 专属 `-realtime` 后缀多模态大模型：<br>• `qwen3.8-omni-flash-realtime`（支持视频输入）<br>• `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`<br>• 实验版 `qwen3-omni-flash-realtime-2025-09-15`（含 `smooth_output` 等新参数） | 专用轻量模型栈：<br>• ASR：`qwen-audio-realtime-v1`（GA）<br>• TTS：`qwen-tts-realtime-v2`（GA）<br>• 混合模型：`qwen-audio-realtime-v1` 启用 `enable_interactive_mode`<br>• **不支持任何 Qwen3 系列大模型或 Omni 架构** |
| **协议与连接模型** | 三协议可选：<br>• AOQ（推荐用于高可靠控制信令）<br>• WebSocket（主流接入方式，支持全事件流）<br>• WebRTC（端到端媒体直连，超低延迟）<br>• 连接生命周期由 `session.start` → `session.end` 显式管理 | 仅支持标准 WebSocket（`wss://`）：<br>• URL 中携带 `model`、`api_key` 等查询参数<br>• 无会话状态维护：超时（180s）即断连，**服务端不保存 session 上下文**<br>• 重连需客户端完全重建连接与初始化 |
| **VAD 与语音控制** | **双模式 VAD 可控**：<br>• `server_vad`（声学级，低延迟）<br>• `semantic_vad`（语义级，可过滤“嗯”“啊”及背景音）<br>• 支持精细配置：`silence_duration_ms`（200–6000ms）、`threshold` 等 | **VAD 完全服务端托管**：<br>• `vad_enabled` 参数当前无效<br>• 无客户端可调参数<br>• 切句逻辑黑盒，依赖服务端声学模型，易受环境噪声干扰 |
| **高级能力** | ✅ 全面支持：<br>• 工具调用（Function Calling + MCP）<br>• 联网搜索（`enable_search`，支持来源返回）<br>• 输入音频转录（固定使用 `qwen3-asr-flash-realtime`）<br>• 细粒度会话控制（`instructions`、`temperature`、`max_tokens` 等） | ❌ 不支持：<br>• 无工具调用机制<br>• 无联网搜索能力<br>• 无系统提示词（`instructions`）注入点<br>• 采样参数（`temperature`/`top_p`）不可配置，响应风格固定 |
| **API 端点** | 统一接入点（协议无关）：<br>`wss://dashscope.aliyuncs.com/omni-realtime/v1/audio`（WebSocket）<br>`wss://dashscope.aliyuncs.com/omni-realtime/v1/aoq`（AOQ）<br>`webrtc://...`（WebRTC） | 模型绑定端点：<br>`wss://dashscope.aliyuncs.com/realtime/v1/audio?model=qwen-audio-realtime-v1&api_key=xxx`<br>不同模型需更换 URL |
| **计费方式** | 按 **实际消耗 Token 数 + 音频处理时长（秒）** 双维度计费：<br>• 输入 Token（文本/ASR 转录结果）<br>• 输出 Token（LLM 生成文本）<br>• 音频处理时长（从 `input_audio_buffer.append` 开始到 `response.done` 结束） | 按 **音频处理时长（秒）** 单维度计费：<br>• 从首个 `input.audio` 到连接关闭（或超时）的总时长<br>• 无论是否触发 LLM、是否产生文本输出，均按连接存活时间计费 |
| **典型场景** | • 全双工语音助手（支持随时打断、语义续聊）<br>• 实时会议智能纪要（语音→文字+摘要+行动项+搜索验证）<br>• 多轮客服机器人（调用 CRM 工具 + 实时播报结果）<br>• 教育陪练（语音问答+发音反馈+知识拓展） | • 实时字幕生成（ASR → text_delta）<br>• IVR 语音导航（TTS 播报 + 简单关键词识别）<br>• 边说边播的朗读应用（`enable_interactive_mode` 下 token 级 TTS）<br>• 低算力终端的轻量语音前端（仅需音频流透传） |

---

## 适用场景建议

### ✅ 选择 **Omni Realtime API** 当：
- 业务需要 **语义理解 + 行动执行** 的完整链路（如：“查我昨天的订单，然后告诉我要不要退货”）；
- 要求 **多模态输入支持**（如：用户上传产品图片 + 语音提问）或 **视频实时分析**（如：远程看护中结合画面与语音判断跌倒）；
- 对 **VAD 精准度要求高**，需过滤口语填充词、适应嘈杂环境（必须用 `semantic_vad`）；
- 需要 **严格控制响应风格**（书面/口语化）、**定制化音色与语速**，或 **审计搜索来源**；
- 架构已采用 AOQ/WebRTC 基础设施，追求端到端可控性与企业级可靠性。

### ✅ 选择 **Realtime API（User Guide）** 当：
- 场景本质是 **高质量 ASR/TTS 管道**，无需大模型推理（如：会议录音转写存档、语音播报通知）；
- 客户端资源受限（如嵌入式设备），仅需最小依赖（标准 WebSocket + Base64 PCM）；
- 对 **首次响应延迟（TTFB）极度敏感**，且交互极简（单轮问答，无上下文依赖）；
- 已有成熟 WebSocket 音频采集模块，希望零改造接入语音能力；
- 成本敏感且交互时长短（<30 秒），避免 Omni 的 Token 计费带来的不确定性。

> ⚠️ 注意：二者**不可混用**。Omni 是独立协议栈与模型体系，Realtime API 的模型无法在 Omni 端点调用，反之亦然。

---

## 技术选型参考（致开发者）

| 你的需求 | 推荐方案 | 理由 |
|----------|-----------|------|
| “我要做一个能查天气、订外卖、讲笑话的全双工语音助手” | **Omni Realtime API** | 唯一支持工具调用 + 多轮会话 + 语义 VAD + 混合输出的方案 |
| “我只需要把客服电话录音实时转成文字，存进数据库” | **Realtime API** | 成本更低、接入更轻量，无需 LLM Token 开销 |
| “我的 App 要支持用户说话时，屏幕同步显示文字+合成语音播放” | 优先 **Realtime API**（`enable_interactive_mode`）；若需回答复杂问题则升 **Omni** | Realtime 的 token 级 `text_delta` + `audio_chunk` 更匹配 UI 渲染节奏；Omni 在复杂语义下更鲁棒 |
| “我要在网页中实现 200ms 内可打断的语音交互” | **Omni Realtime API + WebRTC** | WebRTC 提供最短媒体路径；Omni 的 `semantic_vad` 保障打断精准性 |
| “我用 Python 写后台服务，希望 SDK 封装好重连、VAD、流聚合” | **Omni Realtime API**（官方 Python/Java SDK 已深度封装会话生命周期与事件流） | Realtime API 的 SDK 仅提供基础 WebSocket 封装，重连、流聚合、错误恢复需自行实现 |

**最后建议**：  
- 新项目默认评估 **Omni Realtime API** —— 其抽象层级更高、扩展性更强，长期维护成本更低；  
- 遗留系统迁移或 PoC 快速验证，可先用 **Realtime API** 验证音频链路，再平滑升级至 Omni；  
- 所有生产环境务必启用 **AOQ 协议**（Omni）或 **带 `stream_id` 的事件关联**（Realtime），确保故障可追溯、响应可归因。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


