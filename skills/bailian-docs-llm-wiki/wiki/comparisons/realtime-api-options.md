# 实时API方案对比：Omni Realtime vs Realtime API

为帮助开发者在构建语音优先、多模态实时交互应用（如智能座舱助手、远程医疗问诊系统、高保真客服机器人）时做出高效、可扩展的技术选型，本文对百炼平台当前两大核心实时API方案——**Omni Realtime API** 与 **Realtime API**——进行系统性对比分析。二者均基于 WebSocket 实现低延迟双向流式通信，但在架构定位、能力边界、模型生态与工程适配性上存在显著差异。本对比聚焦实际开发视角，涵盖协议设计、功能覆盖、配置灵活性、运维约束及典型落地路径，旨在提供可直接用于技术决策的参考依据。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心定位** | 全栈式多模态实时会话引擎（ASR + LLM + TTS 一体化闭环），强调语义级交互控制与自然对话流管理 | 轻量级音频实时推理通道（ASR→LLM→TTS 流水线），侧重低延迟音频帧级吞吐与快速接入 |
| **输入格式** | 支持多通道 PCM（2/4 声道）、单声道 PCM/WAV；采样率支持 8k/16k/24k/48k Hz；格式可动态配置（`audio.input.format`） | **严格限定**：单声道 PCM、16-bit little-endian、16kHz；不支持 WAV 或其他采样率；格式不可变更 |
| **输出格式** | `["text", "audio"]`（默认）或 `["text"]`；音频输出支持 PCM（默认）或 WAV；采样率可设为 8k/16k/24k/48k Hz（部分模型支持） | 文本（`response_text_delta`）+ 音频（`response_audio_delta`）；**音频固定为 Opus 编码**（非原始 PCM），无采样率配置项 |
| **支持模型** | 多代 Omni 系列实时模型：<br>• `qwen3.8-omni-flash-realtime`<br>• `qwen3.5-omni-flash-realtime` / `plus-realtime`<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime`<br>（含 ASR 专用子模型 `qwen3-asr-flash-realtime`） | 仅两类音频专用模型：<br>• `qwen-audio-realtime-v1`<br>• `qwen2.5-audio-realtime-v1`<br>（`qwen-vl-realtime` 已下线，调用返回 404） |
| **语音活动检测（VAD）** | 支持双模式：<br>• `server_vad`（声学特征驱动）<br>• `semantic_vad`（语义有效性判断，仅限 Qwen3.8/Qwen3.5 系列）<br>可精细配置 `threshold`、`silence_duration_ms`、`idle_timeout_ms` | **不提供 VAD 能力**；需客户端自行实现语音端点检测并控制 `input_audio` 发送节奏 |
| **工具调用能力** | 支持混合工具调用：<br>• Function Calling（`type="function"`）<br>• MCP（`type="mcp"`，支持工具发现）<br>• `tools` 与 `enable_search` **互斥** | 仅支持 `tool_use` 类型工具调用（类 Function Calling）；**不支持 MCP**；不支持联网搜索 |
| **会话控制粒度** | 事件驱动架构，支持细粒度状态管理：<br>• `session.update` 动态调整模型/语音/VAD/工具等<br>• `input_audio_buffer.commit` 手动提交音频块<br>• `conversation.item.*` 精确控制消息生命周期 | 控制较粗粒度：<br>• `session_update` 仅支持初始化配置（不可热更新模型/语音等）<br>• 依赖 `interrupt` 强制终止响应<br>• 无显式音频缓冲区管理事件 |
| **API 端点** | 按模型区分 endpoint（如 `wss://dashscope.aliyuncs.com/omni/v1/realtime/qwen3.5-omni-flash-realtime`）；支持 WebSocket / AOQ / WebRTC 接入 | 统一 endpoint：<br>`wss://dashscope.aliyuncs.com/realtime/v1/audio`<br>（通过 URL 参数 `model=` 指定模型）；**仅支持 WebSocket / AOQ** |
| **计费方式** | 按 **会话时长（秒） + 输出 Token 数 + 输出音频时长（秒）** 组合计费；支持按模型分级定价（如 Turbo 模型单价更低） | 按 **连接时长（秒） + 输入音频时长（秒） + 输出音频时长（秒） + 输出 Token 数** 计费；模型间单价差异较小 |
| **典型场景** | • 需要语义级中断/恢复的复杂对话（如多轮追问、上下文修正）<br>• 要求音色/语速/情感精细调控的拟人化交互<br>• 集成 MCP 工具生态（如企业内部服务编排）<br>• 多声道音频输入（会议转录、立体声环境识别） | • 快速上线基础语音助手（如 IoT 设备唤醒应答）<br>• 对端到端延迟极度敏感的场景（如实时字幕生成）<br>• 客户端已具备成熟 VAD 和音频预处理能力<br>• 无需动态切换模型或语音参数的标准化服务 |

## 各方案适用场景建议

### ✅ 推荐选用 **Omni Realtime API** 当：
- 应用需**自然、拟人、高容错的对话体验**：例如客服系统中用户频繁打断、修正问题、或要求“用更慢语速再说一遍”，Omni 的 `semantic_vad`、动态 `session.update` 和 `conversation.item` 精细控制可显著提升交互流畅度；
- 需要**集成企业级工具链**：如调用内部 CRM 查询工单、触发审批流程（通过 MCP），且要求工具自动发现与安全鉴权（HTTPS server_url + headers）；
- 输入源为**多声道设备**（如会议室阵列麦克风、车载双麦系统），或需适配不同采样率硬件（如 48kHz 录音设备）；
- 产品规划支持**多模型灰度发布**（如先用 `qwen3.5-omni-plus-realtime`，再平滑切至 `qwen3.8-omni-flash-realtime`），利用其模型专属 endpoint 和热更新能力。

### ✅ 推荐选用 **Realtime API** 当：
- 团队追求**极简接入与快速验证**：统一 endpoint + SDK 自动编解码 + 标准化 PCM 格式，30 分钟内可跑通端到端语音问答；
- 场景对**首字延迟（First Token Latency）和音频帧延迟（Audio Chunk Latency）要求严苛**（如实时同传、游戏语音指令），且客户端已部署高性能 VAD；
- 业务逻辑简单、**模型与语音参数长期固定**，无需运行时动态调整（如固定使用 `qwen2.5-audio-realtime-v1` + `zhitian_emo` 音色）；
- 并发连接数可控（≤10），且单次会话时长稳定在 30 分钟以内（如每通电话平均 5 分钟）。

## 技术选型参考指南（面向开发者）

| 选型考量点 | Omni Realtime API | Realtime API | 建议动作 |
|------------|-------------------|--------------|----------|
| **是否需要语义级 VAD？** | ✅ 支持 `semantic_vad`（理解“嗯…”、“啊…”是否为有效语义起点） | ❌ 仅依赖声学能量阈值 | 若用户常有语气词、停顿、自我修正，选 Omni |
| **能否接受 Opus 音频输出？** | ✅ 可选 PCM/WAV（便于本地播放/后处理） | ❌ 仅 Opus（需客户端解码） | 若需直接喂给硬件 TTS 模块或做音频分析，选 Omni |
| **是否需在运行时切换模型/音色/VAD 参数？** | ✅ `session.update` 全量热更新 | ❌ `session_update` 仅初始化生效 | 若需 A/B 测试不同模型效果，选 Omni |
| **客户端是否已实现可靠 VAD？** | ✅ 可关闭 VAD，完全由客户端控制音频提交 | ⚠️ 必须自行实现，否则连接易超时 | 若 VAD 成熟，Realtime 更轻量；若无，Omni 内置 VAD 降低客户端复杂度 |
| **是否需 MCP 工具发现与调用？** | ✅ 原生支持，`tools` 数组可混用 function/mcp | ❌ 不支持 | 若对接内部微服务网关，必须选 Omni |
| **团队是否有 WebSocket 底层开发经验？** | ⚠️ 事件模型丰富（20+ 服务端事件），需处理状态机 | ✅ 事件精简（<10 类），SDK 封装完善 | 新团队建议从 Realtime SDK 入手，进阶再迁移到 Omni |

> **迁移提示**：从 Realtime API 迁移至 Omni Realtime API 通常需重构音频输入逻辑（适配多格式/多声道）、重写会话状态管理（从“连接生命周期”转向“会话生命周期”），但可复用大部分工具调用和上下文注入逻辑。反之迁移则需剥离语义 VAD、放弃 MCP、并强制统一音频格式。

---  
*最后更新：2024年10月*  
*本文档基于百炼平台 v2.4.0 版本 API 规范撰写，具体行为请以最新版 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 与 [服务端事件](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md) 文档为准。*

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


