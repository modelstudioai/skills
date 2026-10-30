# 实时 API 与 Omni 实时 API 对比

本文旨在帮助开发者清晰区分百炼平台两类核心实时交互接口——**Realtime API**（基础音频实时接口）与 **Omni Realtime API**（多模态增强型实时接口），明确其定位差异、能力边界与技术约束，从而在语音助手、智能客服、会议纪要、音视频交互等场景中做出高效、可持续的技术选型决策。二者虽均基于 WebSocket 协议、采用事件驱动模型、支持流式 ASR/TTS 与[函数调用](../concepts/function-calling.md)，但在模型能力、协议灵活性、输入模态、配置粒度及适用复杂度上存在系统性差异。

## 关键维度对比

| 维度 | Realtime API | Omni Realtime API |
|------|--------------|-------------------|
| **核心定位** | 专注**单模态语音实时交互**的轻量级低延迟通道，强调稳定、确定性与快速接入 | 面向**多模态（语音+文本+视频）、高交互密度、强语义理解**场景的增强型实时平台，强调扩展性、上下文深度与行为可控性 |
| **输入格式** | 仅支持 `LINEAR16` PCM 音频（16-bit, 16kHz, mono）；文本输入需通过 `conversation.item.create` 事件，但非主路径；**不支持图像/视频输入** | 支持多通道音频（1/2/4 声道，严格 `s16le` + `16000Hz` interleaved）、文本、Base64 编码图像（部分模型）、视频帧表征（`representation_compact`）；支持混合模态并发输入 |
| **输出格式** | 文本流（`response.text.delta`） + 音频流（`response.audio.delta`，16kHz PCM）；输出模态由 `modalities` 控制，**无视频输出能力** | 文本流 + 可配采样率音频流（8k/16k/24k/48kHz PCM）；支持 `smooth_output` 渐进式音频合成；**部分模型支持视频表征生成与压缩输出**（如 `qwen3.8-omni-flash-realtime`） |
| **支持模型** | 仅 `qwen-audio-7b`、`qwen2-audio-7b`（纯音频理解/生成模型） | 多层级模型族：<br>• `qwen3.8-omni-flash-realtime`（旗舰：MCP、语义 VAD、视频表征、`smooth_output`）<br>• `qwen3.5-omni-plus/flash-realtime`（主力：基础 VAD、Function Calling、联网搜索）<br>• `qwen3-omni-flash-realtime-2025-09-15`（实验版：高随机性，禁用工具） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://dashscope.aliyuncs.com/realtime/v1/audio` | 统一接入，但协议可选：<br>• WebSocket（推荐）：`wss://dashscope.aliyuncs.com/realtime/v1/omni`<br>• AOQ / WebRTC（需额外 SDK 支持） |
| **计费方式** | 按**会话时长（秒） + 音频输入 token 数 + 文本输出 token 数**计费；无模型调用次数维度 | 按**实际消耗 token 数（含多通道音频折算） + 会话时长 + 功能开关（如 MCP、search）** 计费；多通道音频按声道数线性折算 token（如 2 声道 = 2×单声道） |
| **典型场景** | • 轻量级语音助手（车载、IoT 设备）<br>• 实时字幕转录（单人讲话）<br>• 语音指令控制（确定性高、上下文短）<br>• 需快速上线、资源受限的嵌入式终端 | • 多人会议实时纪要（声源分离 + 多轮总结）<br>• 全能型 AI 客服（语音+图文+知识库+工具链）<br>• 视频内容实时分析与解说（直播/教育）<br>• 高保真语音交互（情感化 TTS、VAD 精准启停） |
| **VAD（语音活动检测）能力** | 无内置 VAD；依赖客户端分段提交音频或外部 VAD 预处理 | 内置多种 VAD：<br>• `server_vad`（基础服务端检测）<br>• `semantic_vad`（语义级启停）<br>• `semantic_vad_ec`（带环境噪声鲁棒性的语义 VAD，仅旗舰模型支持） |
| **工具调用能力** | 支持标准 `tool_choice` 与[函数调用](../concepts/function-calling.md)（Function Calling） | 支持 Function Calling；旗舰模型额外支持 **MCP（Model Calling Protocol）**，可对接外部服务并透传认证头；`tools` 与 `enable_search` 互斥（除旗舰模型外） |
| **会话生命周期** | 强制 300 秒超时，不可续期；无状态恢复机制 | 无硬性超时限制（受配额与连接稳定性影响）；支持更灵活的会话状态管理（如 `session.updated` 确认、`response.cancel` 中断） |
| **SDK 支持** | 官方 AOQ 客户端 SDK（Python/JS），封装连接、心跳、事件解析 | 提供专用 Python/Java SDK，深度集成 AOQ/WebRTC 协议、MCP 流程、VAD 事件监听与多模态输入管理 |

## 各方案的适用场景建议

### ✅ 推荐选用 **Realtime API** 当：
- 项目目标是**快速验证语音交互 MVP**，且仅需处理单人、清晰语音输入；
- 终端设备算力/带宽受限（如 MCU、低端 IoT 设备），需最小化协议开销与音频预处理复杂度；
- 业务逻辑简单，无需图像理解、视频分析、多轮复杂工具编排；
- 对音频输出采样率、VAD 精度、多声道支持无定制需求；
- 团队希望复用现有 PCM 音频采集链路，避免引入新编码/解码模块。

### ✅ 推荐选用 **Omni Realtime API** 当：
- 场景涉及**多人对话、嘈杂环境、远场拾音或需要声源分离**（依赖多通道音频与 `semantic_vad_ec`）；
- 产品需融合**文本、图片、视频等多种输入模态**（如拍照问答、视频会议摘要）；
- 要求**高阶交互能力**：自主调用外部 API（MCP）、实时联网搜索、结构化数据生成；
- 对语音合成质量有严苛要求（如 `smooth_output` 降低卡顿感、多采样率适配不同播放设备）；
- 架构设计面向长期演进，需预留视频理解、多智能体协作等扩展能力。

## 技术选型参考（面向开发者）

| 选型考量点 | Realtime API | Omni Realtime API | 建议动作 |
|------------|--------------|-------------------|----------|
| **开发周期** | ⏱️ 极短（小时级接入） | ⏱️ 中等（1–3 天，需理解多事件流与 VAD 状态机） | 若需快速上线 PoC，优先 Realtime；若规划 3 个月以上产品迭代，直接 Omni |
| **维护成本** | 🛠️ 低（固定模型、固定格式、少参数） | 🛠️ 中高（多模型特性差异大、参数组合多、需处理更多 error 事件类型） | 建议使用官方 SDK 并严格遵循 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 文档校验参数 |
| **调试难度** | 🐞 低（事件类型少，日志清晰） | 🐞 中（需跟踪 `input_audio_buffer.speech_started/stopped`、`session.updated` 等多状态流转） | Omni 开发者应启用 `debug: true` 模式并监听所有 `error` 事件，重点关注 `error.param` 字段 |
| **未来兼容性** | 📈 有限（模型已冻结，无新增音频模型计划） | 📈 高（Omni 是百炼实时交互演进主干，新能力（如视频、3D 音频）将首先在此发布） | 新项目强烈建议以 Omni 为基线，Realtime 仅作降级备选或遗留系统对接 |
| **成本敏感度** | 💰 更优（token 计费更透明，无 MCP/search 溢价） | 💰 需精细管控（多通道音频、MCP 调用、高采样率输出均显著增加 token 消耗） | 在 Omni 中，务必通过 `modalities=["text"]` 关闭非必要音频输出，并为 `qwen3.5` 系列禁用 `enable_search` 除非必需 |

> **重要提醒**：二者**不兼容混用**。Realtime API 的 `qwen-audio-7b` 无法调用 Omni 的 MCP 工具；Omni 的 `qwen3.8-omni-flash-realtime` 也不接受 Realtime 的旧版 `input_audio_format` 参数。请严格依据所选 API 的文档初始化会话与发送事件。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


