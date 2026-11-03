# 实时 API 方案对比：Omni Realtime vs Realtime User Guide

## 对比目的与背景

为帮助开发者在百炼平台中快速、准确地选择适合业务需求的实时语音/[多模态](../concepts/multi-modal.md)交互方案，本文对两类核心实时 API 进行系统性对比分析：  
- **Omni Realtime API**（`api/omni-realtime-api.md`）：面向下一代[多模态](../concepts/multi-modal.md)智能体（语音+文本+图像+视频）的高扩展性 WebSocket 接口，强调语义级交互控制与模型能力深度集成；  
- **Realtime API User Guide**（`api/realtime-api-user-guide.md`）：面向传统语音场景（ASR/TTS/语音对话）的轻量级流式接口，聚焦低延迟、高稳定性与开箱即用。

二者定位不同：Omni Realtime 是「智能体原生」的实时交互协议，而 Realtime User Guide 是「语音管道原生」的实时媒体处理协议。本对比旨在从技术架构、能力边界、接入成本和适用阶段三个维度，为开发者提供可落地的技术选型依据。

---

## 关键维度对比表

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **协议与连接方式** | WebSocket（支持 AOQ/WebRTC/WebSocket 多入口），需显式管理会话生命周期（`session.created` → `session.updated` → `response.done`） | WebSocket（固定端点 `wss://dashscope.aliyuncs.com/api/v1/realtime`），连接即会话，参数通过 query string 传递，服务端硬限 120 秒 |
| **输入格式** | ✅ [多模态](../concepts/multi-modal.md)：<br>• 音频：PCM/WAV（Base64 编码），支持 `8k/16k/24k/48k`（Qwen3.5）、`16k`（Qwen3.8）<br>• 图像：Base64 JPEG/PNG<br>• 视频：H.264（Qwen3.8+，需启用 `video.input.representation_compact`） | ❌ 单模态仅音频：<br>• 原始 PCM 帧（无 WAV 头），**强制 `16kHz` 单声道**，不支持 Base64 封装，不支持图像/视频 |
| **输出格式** | ✅ 多模态[流式输出](../concepts/streaming-output.md)：<br>• `text.delta`（流式文本）<br>• `audio.delta`（流式音频 chunk）<br>• `audio.done`（完整音频片段）<br>• 支持多通道空间音频（2/4 声道） | ✅ 流式结构化事件：<br>• `event: "text"`（识别/生成文本）<br>• `event: "audio"`（TTS 音频二进制帧）<br>• `event: "interim"`（ASR 中间结果，当 `enable_interim_results=true`）<br>• **不返回结构化消息项或工具调用事件** |
| **支持模型** | • `qwen3.5-omni-flash-realtime` / `qwen3.5-omni-plus-realtime`（文本+音频）<br>• `qwen3.8-omni-flash-realtime`（新增视频、MCP、semantic_vad_ec）<br>• `qwen3-omni-flash-realtime-2025-09-15`（预发布，含 `smooth_output`） | • `qwen-audio-realtime-asr-v1`（纯 ASR）<br>• `qwen-audio-realtime-tts-v1`（纯 TTS）<br>• `qwen-audio-realtime-conversation-v1`（ASR+LLM+TTS 端到端流水线）<br>• **所有模型均无图像/视频理解能力，无 Function Calling/MCP** |
| **API 端点** | 按地域区分（如 `wss://realtime-dashscope.aliyuncs.com/ws/v1`），需配合 [Omni Realtime 模型接入方式](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 使用 | 固定统一端点：<br>`wss://dashscope.aliyuncs.com/api/v1/realtime?model=xxx&audio_format=pcm&sample_rate=16000` |
| **计费方式** | 按 **实际消耗 [Token](../concepts/token.md) 数** 计费（含输入音频 [Token](../concepts/token.md)、图像 [Token](../concepts/token.md)、视频 Token、输出文本 Token、输出音频 Token）；多通道音频按声道数倍增 Token；视频 `representation_compact=none` 消耗最高 | 按 **连接时长 + 音频处理时长** 计费（单位：秒），与 Token 无关；ASR/TTS/Conversation 模型单价不同，但均不因内容复杂度浮动 |
| **核心交互能力** | • 语义级 VAD（`semantic_vad` / `semantic_vad_ec`）<br>• 自动打断（`auto_interrupt`）、静默超时引导（`idle_timeout_ms`）<br>• Function Calling + MCP 工具集成<br>• 联网搜索（`enable_search`，与 tools 互斥）<br>• 输入音频转录（ASR 内置，不可关闭） | • 基础 server-side VAD（隐式触发）<br>• 仅支持 `enable_interim_results` 控制中间识别<br>• **无工具调用、无联网搜索、无上下文状态持久化（跨请求）**<br>• ASR/TTS 可独立使用，Conversation 模型内置简单状态机 |
| **典型场景** | • 智能会议助手（实时音视频分析+摘要+动作建议）<br>• 多模态客服机器人（用户上传截图+语音提问）<br>• 教育陪练应用（学生朗读+摄像头反馈+实时纠错）<br>• 具身智能体远程控制（语音+画面指令同步解析） | • 电话客服语音转写（ASR）<br>• IVR 语音导航播报（TTS）<br>• 实时语音翻译耳机（ASR+TTS 管道）<br>• 简单语音问答设备（单轮问答，无需工具或视觉） |

---

## 各方案适用场景建议

### ✅ 推荐选用 **Omni Realtime API** 当：
- 业务需要 **融合语音、文本、图像或视频** 的联合理解与响应（例如：用户说“这个表格哪里错了？”，同时上传 Excel 截图）；
- 要求 **深度可控的交互逻辑**：如自定义 VAD 策略、主动打断、多轮工具调用（查天气→订机票→发短信）、空间音频输出；
- 已具备 WebSocket 客户端开发能力，或正在构建自有智能体 SDK/框架；
- 愿意为更高表达力与灵活性承担稍高的接入复杂度与 Token 成本；
- 场景对 **语义连贯性、上下文一致性、多模态对齐精度** 有强要求（如医疗问诊辅助、工业质检指导）。

### ✅ 推荐选用 **Realtime API User Guide** 当：
- 核心诉求是 **极简、稳定、低延迟的语音管道**（ASR 或 TTS 或二者串联），无多模态或复杂逻辑需求；
- 项目处于 MVP 阶段，需快速验证语音交互可行性，或嵌入资源受限终端（如低端 IoT 设备）；
- 已使用 AOQ 官方 SDK（Web/iOS/Android），希望复用其自动重连、帧缓冲、心跳保活等成熟能力；
- 对合规性有明确要求：需规避任何含 PCI-DSS/HIPAA 敏感字段的语音上传（该方案明确禁止此类行为，Omni Realtime 未作同等声明）；
- 成本敏感且语音流量大：按秒计费在长时语音场景下可能显著低于 Omni 的 Token 计费模式。

> ⚠️ 注意：二者**不兼容互换**。Omni Realtime 不支持 `conversation-v1` 类模型；Realtime API User Guide 无法处理图像/视频事件或 `response.content_part.added` 等结构化响应。

---

## 技术选型参考（面向开发者）

| 评估项 | Omni Realtime | Realtime User Guide | 选型建议 |
|--------|----------------|------------------------|-----------|
| **接入门槛** | ⚠️ 中高：需理解事件驱动模型、手动管理 session 生命周期、处理嵌套配置（如 `audio.input.format`）、适配多模态事件流 | ✅ 低：参数扁平化（query string）、SDK 封装完善、文档示例即开即用 | MVP/资源紧张 → Realtime；长期智能体建设 → Omni |
| **调试体验** | ✅ 强：服务端返回丰富事件（`session.updated`, `input_audio_buffer.committed`, `function_call`），便于精准定位 VAD、ASR、LLM 各阶段问题 | ⚠️ 弱：仅返回 `text`/`audio`/`error` 三类事件，中间过程黑盒，ASR 错误难归因 | 需深度可观测性 → Omni；仅需功能通路 → Realtime |
| **扩展性与未来演进** | ✅ 极高：已预留 MCP、视频、多声道、风格控制（`smooth_output`）等扩展点，模型迭代路径清晰 | ⚠️ 有限：定位为稳定语音管道，新增能力（如图像）需全新 API，非向后兼容升级 | 规划 12 个月以上产品路线 → Omni；短期交付 → Realtime |
| **合规与安全** | 文档未明确禁止敏感语音字段，需客户自行评估数据出境与存储策略 | ✅ 明确禁止上传 PCI-DSS/HIPAA 敏感语音，并在概述页强调合规约束 | 金融/医疗强监管场景 → 优先 Realtime（或严格审计 Omni 使用方式） |
| **推荐起步模型** | `qwen3.8-omni-flash-realtime`（平衡能力与稳定性，支持视频/MCP/semantic_vad_ec） | `qwen-audio-realtime-conversation-v1`（一站式语音对话，免 ASR/TTS 分离集成） | — |

> 💡 **一句话决策指南**：  
> **要“智能”——选 Omni Realtime；要“稳快”——选 Realtime User Guide。**  
> 若业务正从语音管道向多模态智能体演进，建议以 Realtime 快速上线 V1，再平滑迁移至 Omni Realtime 实现 V2 能力跃迁。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


