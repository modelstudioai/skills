# 实时API方案对比：Omni Realtime API vs Realtime API User Guide

本文旨在帮助开发者清晰区分百炼平台当前提供的两类核心实时交互能力——**Omni Realtime API** 与 **Realtime API（User Guide 所述方案）**，明确其定位差异、技术边界与适用约束。随着多模态实时交互需求激增（如语音助手、会议实时转写+摘要、AI陪练等），选择错误的底层协议或模型接口将导致集成成本陡增、功能不可达、延迟超标甚至计费异常。本对比基于最新稳定文档（截至2024年10月），聚焦可落地的技术事实，不依赖过时示例或实验性特性。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|-------------------|--------------------------|
| **设计目标** | 面向**端到端多模态实时对话闭环**优化：语音输入→语义理解→工具调用/联网搜索→文本+语音合成输出，强调低延迟 VAD、自然话轮切换与会话状态自治 | 面向**流式音视频内容处理与增量响应**优化：支持音频/视频帧级输入 + token/audio chunk 级[流式输出](../concepts/streaming-output.md)，强调客户端强控制（中断、暂停）、时间戳对齐与跨模态输入兼容性 |
| **输入格式** | 支持 `pcm`（默认）或 `wav`；采样率灵活（`qwen3.5-*`：8k/16k/24k/48k；`qwen3.8-*`：仅16k）；支持单/多声道；**必须通过 `input_audio_buffer.*` 事件分块写入** | 支持 `"pcm"`、`"wav"`、`"mp4"`；采样率硬约束（PCM/WAV：仅16kHz；MP4内音频：仅48kHz）；**通过 `audio_input` / `video_input` 事件逐帧发送（每帧≤200ms音频或1s视频）** |
| **输出格式** | 文本（`text_delta`） + 音频（`audio_output`）双模态[流式输出](../concepts/streaming-output.md)；音频格式支持 `pcm`/`wav`；输出采样率可配（`qwen3.5-*`：8k/16k/24k/48k；`qwen3.8-*`：固定24k） | 文本（`response.text_delta`） + 音频（`response.audio_output`）[流式输出](../concepts/streaming-output.md)；**音频仅支持 `pcm` 格式，采样率固定为16kHz（无配置项）**；视频输出暂未开放 |
| **支持模型** | 专属 `-realtime` 后缀多模态模型：<br>• `qwen3.8-omni-flash-realtime`<br>• `qwen3.5-omni-plus-realtime`<br>• `qwen3.5-omni-flash-realtime` | 通用实时推理模型：<br>• `qwen-audio-realtime-v1`（语音理解）<br>• `qwen-video-realtime-v1`（视频理解）<br>• `qwen2.5-7b-instruct-realtime`（纯文本流式）<br>• *注：`qwen1.5-4b-realtime` 已下线* |
| **核心能力** | ✅ 内置端到端 VAD（`server_vad`/`semantic_vad`）<br>✅ 动态话轮检测（`idle_timeout_ms`）<br>✅ 工具调用（Function Calling + MCP）<br>✅ 联网搜索（`enable_search`）<br>✅ 多音色可选（Tina/Cherry等）<br>❌ 不支持视频输入 | ✅ 客户端主动中断（`interrupt`）<br>✅ 响应时间戳（`timestamp`）与音频分块ID（`audio_chunk_id`）<br>✅ 显式会话复用（`session_id`）<br>✅ 视频流输入（`video_input`）<br>❌ 无内置 VAD，需客户端预处理<br>❌ 不支持工具调用与联网搜索 |
| **API 协议** | 支持 **AOQ、WebSocket、WebRTC** 三协议接入；推荐 WebSocket（含官方 Python/Java SDK） | **仅支持 WebSocket**（`wss://dashscope.aliyuncs.com/realtime/v1/chat`）；无 WebRTC 或 AOQ 支持 |
| **连接生命周期** | 无显式超时限制（依赖底层协议稳定性）；会话参数可通过 `session.update` 动态调整 | 单连接最长 **10 分钟**；超时断连后需重连并传入原 `session_id` 续接上下文；`session_id` 30分钟无活动自动清理 |
| **计费方式** | 按 **实际处理的音频时长（秒） + 输出文本 [Token](../concepts/token.md) 数 + 输出音频时长（秒）** 分项计费；工具调用、联网搜索单独计费 | 按 **输入音频/视频时长（秒） + 输出文本 [Token](../concepts/token.md) 数 + 输出音频时长（秒）** 计费；`interrupt` 不产生额外费用，但已消耗的资源仍计费 |
| **典型场景** | • 智能语音客服（自动应答+工单创建）<br>• 多轮语音助手（提问→查天气→播新闻→设提醒）<br>• 实时会议助手（发言识别→语义VAD→摘要生成→语音播报）<br>• 教育陪练（发音纠正+实时反馈） | • 实时语音转写（ASR+标点恢复）<br>• 音视频内容分析（直播评论情感流分析）<br>• 低延迟文本流式生成（代码补全、写作辅助）<br>• 需精确控制响应节奏的工业HMI交互 |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 你的应用需要 **开箱即用的语音对话闭环**，无需自研 VAD、话轮检测或 TTS 集成；
- 必须支持 **工具调用（如查数据库、调第三方API）或联网搜索**，且要求这些能力与语音流深度耦合；
- 需要 **多音色、高保真语音输出**，并对输出采样率（如24kHz）有明确要求；
- 场景涉及 **复杂多轮状态管理**（如客服中“先查订单→再改地址→最后确认”），依赖模型侧语义级话轮判断；
- 技术栈允许接入 WebRTC（如Web端音视频通话场景）或需极致端到端延迟（<300ms）。

### 选择 Realtime API（User Guide 方案）当：
- 你已有成熟的 **前端音频预处理链路**（如自研 VAD、降噪、回声消除），只需模型提供低延迟 ASR/NLU/LLM 能力；
- 应用需 **精确控制响应时机**（如用户说话中途打断、暂停生成、跳过某段回复）；
- 需处理 **视频流输入**（如监控画面理解、在线教育板书分析）；
- 对 **时间同步精度要求极高**（如字幕打点、唇音同步），依赖服务端返回的 `timestamp` 和 `audio_chunk_id`；
- 场景以 **纯文本流式生成为主**，或仅需基础语音理解（无TTS、无工具调用），追求轻量接入与快速上线。

## 技术选型参考（致开发者）

- **不要混用模型与协议**：`qwen3.5-omni-plus-realtime` 仅在 Omni Realtime API 中可用；`qwen-audio-realtime-v1` 无法在 Omni 接口调用。模型名后缀（`-omni-*` vs `-realtime-v1`）是关键标识。
- **VAD 是分水岭**：若需服务端自动切分“用户说一段→模型说一段”，选 Omni；若需客户端完全掌控音频缓冲区（如 Web Audio API 精确截断），选 Realtime API。
- **参数可配置性差异显著**：Omni 的 `temperature` 等采样参数在 `qwen-omni-turbo-*` 系列中**完全不可调**；Realtime API 的对应参数（如 `temperature`）在 `qwen2.5-7b-instruct-realtime` 中**支持配置**（详见各模型文档）。
- **音频格式兼容性需前置验证**：Omni 对 `qwen3.8-*` 输入强制 16kHz PCM；Realtime API 对 MP4 封装要求严格（48kHz 音频轨道）。务必按文档约束准备数据，避免 `400 Bad Request`。
- **SDK 优先级**：Omni 提供 Python/Java 官方 SDK，封装了 `session.update`、`input_audio_buffer.commit` 等复杂事件；Realtime API 推荐直接使用 WebSocket 原生库（如 `websocket-client`）或 AOQ SDK，灵活性更高但集成成本略升。

> ⚠️ 重要提醒：所有 `qwen-omni-turbo-*` 系列模型（如 `qwen3.5-omni-turbo-realtime`）在 Omni Realtime API 中**禁用全部采样参数**（`temperature`/`top_p`/`max_tokens` 等），此为硬性限制。若需调节生成确定性，请选用 `qwen3.5-omni-plus-realtime` 或 `qwen3.8-omni-flash-realtime`。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


