# 实时 API 对比：Omni Realtime API vs Realtime API User Guide

本对比旨在帮助开发者清晰区分百炼平台当前并存的两类[实时交互](../concepts/realtime.md) API 能力体系——**Omni Realtime API**（面向多模态、高可控性、端到端低延迟交互场景）与 **Realtime API User Guide 所述的传统 Realtime API**（面向轻量级流式语音/文本交互的通用实时接口）。二者虽同属“实时”范畴，但在协议栈深度、模态支持粒度、会话控制能力、模型架构定位及适用边界上存在本质差异。本文提供结构化技术对比与选型建议，助力团队基于业务需求精准选择接入路径。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **核心定位** | 多模态原生[实时交互](../concepts/realtime.md)引擎：语音+文本+视频输入 × 文本+音频混合输出，强调语义级交互闭环（如 VAD 驱动轮转、工具调用嵌入响应流） | 通用流式推理通道：以低延迟传输为核心，支持音频/文本流式输入与 token 级增量输出，侧重协议兼容性与快速接入 |
| **输入格式** | • 支持多通道 PCM（2/4 声道，仅 `qwen3.8-omni-flash-realtime`）<br>• 单/双/四通道音频需显式配置 `audio.input.format`（`type=pcm`, `sample_rate=16000`, `s16le`, `interleaved`）<br>• 文本通过 `conversation.item.create` 发送 | • 严格单声道（mono）<br>• 仅支持 16kHz/16bit PCM 或 WAV（`input_format="audio/wav"`）<br>• 纯文本需设 `input_format="text/plain"`，不支持混合模态输入流 |
| **输出格式** | • 可配置 `["text"]` 或 `["text","audio"]` 混合输出<br>• 音频输出支持 `pcm`/`wav`，采样率可配（默认 24kHz）<br>• 流式事件细粒度：`response.audio.delta`（音频 chunk）、`conversation.item.created`（消息/工具调用） | • 输出为纯文本 token 流（`delta` 事件）或 TTS 音频流（`audio.delta`）<br>• 音频仅支持 `audio/pcm`（默认）或 `audio/mp3`（需显式指定 `output_format`）<br>• 无结构化消息类型（如 function_call），需自行解析 |
| **支持模型** | • 专属 Omni 系列实时模型：<br> `qwen3.8-omni-flash-realtime`（主力推荐）<br> `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`<br> `qwen3-omni-flash-realtime-2025-09-15`（实验版）<br>• 所有模型均需通过 `session.update` 显式指定 | • 传统 Realtime 模型族：<br> `qwen-audio-realtime`（语音优先）<br> `qwen-vl-realtime`（视觉语言）<br> `qwen2.5-7b-realtime`（轻量文本）<br>• 模型由 `X-DashScope-Model` Header 或 Init Frame 中 `model` 字段指定，不可动态切换 |
| **API 端点与协议** | • 支持三协议接入：<br> WebSocket（`wss://.../omni-realtime/v1/chat`）<br> AOQ（AI over QUIC，更低延迟/抗丢包）<br> WebRTC（端到端加密音视频直连）<br>• 事件驱动模型（`session.created` → `session.update` → `input_audio_buffer.append` → `response.create`） | • 仅 WebSocket 协议：<br> `wss://dashscope.aliyuncs.com/realtime/v1/chat`<br>• 帧驱动模型（Init Frame → Audio/Data Frame → Delta Frame → End Frame）<br>• 不支持 AOQ/WebRTC |
| **会话控制能力** | • 全生命周期事件控制：<br> `session.update` 动态调整模型/VAD/工具/音色等<br> `response.cancel` 中断生成<br> `input_audio_buffer.clear` 清空缓冲区<br>• 内置双模式 VAD（`server_vad`/`semantic_vad`），支持灵敏度与静音时长精细调节 | • 仅基础控制帧：<br> `cancel` 帧可中断当前响应<br> 无 VAD 配置能力，依赖客户端预切分或服务端默认声学检测（不可调）<br>• 无会话参数动态更新机制，所有配置需在 Init Frame 一次性声明 |
| **高级功能支持** | • ✅ 工具调用（Function Calling + MCP）<br>• ✅ 联网搜索（`enable_search=true`，含来源标注）<br>• ✅ 音色定制（`audio.output.voice`，支持数十种音色）<br>• ✅ 多通道音频输入（2/4 channel）<br>• ✅ 上下文感知的平滑输出（`smooth_output` 实验参数） | • ❌ 不支持工具调用（无 function/mcp 事件）<br>• ❌ 不支持联网搜索<br>• ⚠️ 音色控制有限（仅部分模型支持基础 voice 参数，无官方音色列表）<br>• ❌ 仅支持单声道音频输入<br>• ❌ 无平滑输出等高级生成控制 |
| **计费方式** | • 按实际消耗 Token 计费（含输入音频 Token）<br>• 多通道音频输入按声道数倍增 Token 消耗（如 4 声道 = 4× 单声道）<br>• 音频输出按秒计费（PCM/WAV 时长） | • 按输入 Token + 输出 Token 计费<br>• 音频输入按原始字节数折算 Token（固定换算率，无声道倍增）<br>• TTS 输出按字符数或音频时长计费（依模型而定） |
| **典型场景** | • 智能会议助手（多麦阵列拾音 + 实时纪要 + 搜索问答 + 发言人音色区分）<br>• 全双工虚拟客服（VAD 驱动无缝打断 + 工具调用查订单 + 合成自然语音）<br>• 教育陪练应用（视频输入分析 + 语音反馈 + 个性化音色） | • 语音转文字实时字幕（低延迟 ASR+LLM）<br>• 简单语音问答机器人（单麦设备 + 快速响应）<br>• 音频流摘要（对长录音分块流式处理） |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 你的产品需要 **真正的全双工、多模态交互体验**（如用户说话时系统可随时插入、追问、调用工具）；
- 输入源为 **专业麦克风阵列、会议系统或带视频的终端设备**，需利用多通道音频提升识别鲁棒性；
- 业务逻辑强依赖 **实时工具调用**（如查天气、订机票、读取数据库）或 **联网搜索增强**（如回答时效性问题）；
- 对语音输出质量、音色多样性、响应自然度有较高要求（如数字人、品牌客服）；
- 团队具备 WebSocket/AOQ/WebRTC 接入经验，或愿意使用官方 Python/Java SDK 封装复杂事件流。

### 选择 Realtime API User Guide 当：
- 你正在构建 **轻量级、快速验证型语音应用**（如内部 demo、IoT 设备语音控制）；
- 输入源为 **普通手机/耳机单声道音频**，且无需复杂 VAD 或多轮上下文管理；
- 场景以 **ASR+LLM 流式转译/问答为主**，不涉及外部系统集成或搜索增强；
- 项目时间紧、资源有限，需最小成本接入（仅需标准 WebSocket 客户端 + JSON 帧解析）；
- 对模型迭代速度敏感，需快速切换不同轻量级 Realtime 模型（如从 `qwen2.5-7b-realtime` 切至 `qwen-vl-realtime`）。

## 技术选型参考（致开发者）

| 评估项 | 推荐方案 | 说明 |
|---------|-----------|------|
| **是否需要多通道音频输入？** | ✅ Omni Realtime API | Realtime API 仅支持单声道，无法利用阵列麦克风优势 |
| **是否必须支持 Function Calling/MCP？** | ✅ Omni Realtime API | Realtime API 无对应事件类型，需自行封装 HTTP 调用，破坏流式体验 |
| **是否要求 VAD 灵敏度/静音时长可调？** | ✅ Omni Realtime API | Realtime API 的 VAD 为黑盒策略，不可配置 |
| **是否已使用 AOQ/WebRTC 技术栈？** | ✅ Omni Realtime API | 复用现有基础设施，获得更低延迟与更好弱网表现 |
| **是否仅需 1~2 天完成 PoC？** | ✅ Realtime API User Guide | 协议简单、文档清晰、SDK 封装成熟，适合快速验证 |
| **是否部署在资源受限的边缘设备？** | ⚠️ Realtime API User Guide | Omni SDK 依赖更多运行时能力（如 WebRTC 库），边缘适配成本略高 |
| **是否需长期维护高 SLA 的生产服务？** | ✅ Omni Realtime API | 提供更完善的会话状态管理、错误恢复机制与企业级监控事件 |

> **重要提示**：Omni Realtime API 是百炼平台面向下一代智能交互的演进方向，其模型能力、协议支持与生态工具持续快速迭代；Realtime API User Guide 作为稳定基线接口，将长期维护但功能扩展趋于收敛。新项目建议优先评估 Omni 方案，存量项目迁移可参考 [Omni 迁移指南](../../raw/model-api-reference/omni-realtime-api/migration-guide.md)。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


