# Omni Realtime API 与 Realtime API 用户指南对比

本对比旨在帮助开发者清晰区分百炼平台两大实时交互接口——**Omni Realtime API** 与 **Realtime API** 的能力边界、技术特性与适用约束，避免因模型选型或协议误用导致集成失败、延迟超标或功能缺失。二者虽同属“实时流式交互”范畴，但在设计目标、多模态支持深度、协议灵活性、模型演进路径及工程实践要求上存在系统性差异。本文基于当前（2024年Q3）正式发布的文档与 SDK 行为进行客观比对，所有结论均以服务端实际响应逻辑为准。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **定位与设计目标** | 面向**全链路低延迟多模态实时交互**的下一代统一协议；强调端到端语音+文本+视频联合理解与生成，支持空间音频、语义级 VAD、MCP 工具生态等前沿能力 | 面向**高可靠语音/视频流实时处理**的基础实时接口；聚焦音频/视频流的稳定接入、上下文保持与基础工具调用，强调协议轻量性与兼容性 |
| **输入模态支持** | ✅ 文本 + 多通道 PCM 音频（16 kHz，支持 1/2/4 声道）<br>✅ WAV 封装音频<br>✅ 视频帧（仅 `qwen3.8-omni-flash-realtime`）<br>✅ 空间音频元数据（`qwen3.8-omni-flash-realtime`） | ✅ 单声道 PCM 音频（严格 `16000 Hz`, `signed-16-bit little-endian`）<br>✅ Opus 编码音频（`opus-16k`）<br>✅ H.264/AV1 视频流（`h264-30fps`, `av1-30fps`）<br>❌ 不支持多通道音频、WAV 封装、空间音频、视频帧级控制 |
| **输出模态支持** | ✅ 文本（`text.delta`）<br>✅ 合成语音流（`response.audio.delta`），支持 `pcm`/`wav` 输出格式与可配置采样率（最高 48 kHz）<br>✅ 工具调用结果（`function_call`, `mcp_*` 事件） | ✅ 文本增量流（`output.text.delta`）<br>✅ 工具调用触发（`tool.use`）<br>❌ **不提供合成语音输出能力**（需客户端自行 TTS）<br>❌ 不支持音频格式/采样率配置 |
| **支持模型** | `qwen3.8-omni-flash-realtime`（最新主力）、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime`（参数受限） | `qwen-audio-realtime-v1`、`qwen-video-realtime-v1`、部分 `qwen2.5-*` 实时系列模型（非 Omni 命名体系） |
| **传输协议** | ✅ WebSocket（推荐）<br>✅ WebRTC（端到端加密、超低延迟）<br>✅ AOQ（阿里云自研轻量协议，SDK 封装） | ✅ WebSocket（唯一官方支持协议）<br>❌ 不支持 WebRTC 或 AOQ 接入 |
| **API 端点** | WebSocket: `wss://dashscope.aliyuncs.com/omni-realtime/v1/chat`<br>（需使用 Omni 专用鉴权与握手流程） | WebSocket: `wss://dashscope.aliyuncs.com/realtime/v1/chat`<br>（通用 Realtime 鉴权 header：`Authorization: Bearer <api_key>`） |
| **核心 VAD 能力** | ✅ `server_vad`（声学端点检测）<br>✅ `semantic_vad`（语义级静音判断，更抗噪声）<br>✅ 可精细调节 `threshold`（-1.0~1.0）与 `silence_duration_ms`（200~6000 ms） | ✅ 基础中断检测（`enable_interruption`）<br>❌ 无显式 VAD 配置项；中断行为由服务端固定策略决定，不可调参 |
| **工具调用能力** | ✅ Function Calling（`type=function`）<br>✅ MCP 工具集成（`type=mcp`，支持动态 server_url 注册）<br>⚠️ `tools` 与 `enable_search` 互斥 | ✅ Function Calling（`tool.use` 事件）<br>❌ 不支持 MCP 协议<br>❌ 不支持联网搜索（`enable_search`） |
| **联网搜索** | ✅ 仅 `qwen3.8-omni-flash-realtime` 与 `qwen3.5-omni-realtime` 系列支持，需显式设置 `enable_search: true` | ❌ 完全不支持 |
| **会话生命周期** | ⏳ 无硬性连接超时限制（依赖底层传输稳定性）；支持长时会话与上下文累积 | ⏳ **单连接最大存活 300 秒**（含握手与空闲期），超时必须重连；每次连接为独立会话，不共享 state |
| **关键参数可配置性** | ✅ `temperature` / `top_p` / `top_k` / `max_tokens`（除 turbo 系列外）<br>✅ `audio.input.format` / `audio.output.format`（采样率、编码）<br>✅ `voice`（音色）<br>✅ `instructions`（系统提示） | ❌ `temperature` / `top_p` **不可配置**（服务端固定策略）<br>✅ `max_output_tokens`（1–4096）<br>✅ `audio_format` / `video_format`（格式声明）<br>✅ `enable_interruption` |
| **计费方式** | 按 **实际消耗 [Token](../concepts/token.md) 数 + 音频/视频处理时长（秒）** 双维度计费：<br>- 输入 [Token](../concepts/token.md)（含音频转写、视频帧编码开销）<br>- 输出 [Token](../concepts/token.md)（文本）<br>- 合成语音时长（秒）<br>（详见 [计费说明](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)） | 按 **输入 Token + 输出 Token** 计费：<br>- 输入 Token（音频/视频流解码后文本化 token）<br>- 输出 Token（文本 delta）<br>❌ 不对媒体处理时长或合成语音单独计费（因其不提供语音输出） |
| **典型场景** | • 全双工智能语音助手（支持随时打断+自然恢复）<br>• 多语种会议实时纪要（含发言人分离+内容摘要+语音播报）<br>• 空间音频交互应用（如 VR 语音导航）<br>• 需 MCP 集成的自动化工作流（如实时调用内部 CRM） | • 语音客服 IVR 流程（单向播报+按键/语音应答）<br>• 视频会议实时字幕与摘要<br>• 音频流内容审核（敏感词/情绪识别）<br>• 轻量级语音指令控制（如智能家居） |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 你的产品需要 **端到端语音交互闭环**（用户说话 → 模型理解 → 合成语音回复），且对回复自然度、延迟、音色可控性有明确要求；
- 场景涉及 **多通道音频**（如立体声会议录音）、**空间音频** 或 **视频帧级理解**（如手势识别辅助）；
- 需要 **语义级 VAD**（例如在嘈杂环境准确判断用户是否说完）或 **精细 VAD 参数调优**；
- 必须集成 **MCP 工具协议**（对接企业内部系统）或启用 **联网搜索** 功能；
- 项目处于中长期演进阶段，需面向 Qwen-Omni 系列模型持续升级（如未来支持图像输入）；
- 团队具备 WebSocket/WebRTC 开发经验，或可采用官方 Python/Java SDK 快速集成。

### 选择 Realtime API 当：
- 核心需求是 **稳定、低门槛接入音频/视频流**，并获取结构化文本响应（如字幕、摘要、指令解析），**无需模型合成语音**；
- 场景对连接时长要求不高（≤ 5 分钟），或可接受自动重连机制；
- 需快速验证语音/视频理解能力，使用 `qwen-audio-realtime-v1` 等成熟模型；
- 已有基于 WebSocket 的流媒体处理框架，希望最小化改造成本；
- 对生成多样性参数（`temperature` 等）无定制需求，接受服务端默认策略；
- 预算敏感，且无需语音合成或 MCP 等高级能力（计费成本更低）。

## 技术选型参考（致开发者）

- **不要混淆协议层级**：Omni Realtime API 是 Realtime API 协议的**超集演进**，二者端点、鉴权、事件命名、参数结构均不兼容。混用将导致连接拒绝或事件解析失败。
- **语音输出是分水岭**：若业务流中**必须由模型直接输出可播放语音流**（而非客户端调用第三方 TTS），则 Omni Realtime API 是唯一选择；Realtime API 仅输出文本，TTS 需额外集成。
- **关注模型锁定风险**：Omni 系列模型（如 `qwen3.8-omni-flash-realtime`）功能强大但迭代快，部分参数（如 `qwen-omni-turbo` 的温度控制）被主动禁用；Realtime API 模型相对稳定，但功能扩展慢。
- **VAD 选型影响体验**：`semantic_vad` 在会议、车载等复杂声学场景下显著优于 `server_vad`，但仅 Omni 支持；Realtime API 的中断检测更适合安静环境下的确定性指令。
- **生产环境必读限制**：Omni 的 `audio.input.format` 必须在首帧音频前配置；Realtime API 的 PCM 格式（`16k, signed-16-le`）和视频关键帧间隔（≤2s）是硬性校验项，不满足将直接断连。
- **SDK 优先原则**：官方 Python/Java SDK 已封装 Omni 的 WebRTC/AOQ 接入、事件序列化、重试与错误降级逻辑；Realtime API 推荐使用 AOQ SDK（v1.2+）简化开发。手动实现 WebSocket 协议需严格遵循各文档中的二进制帧格式与心跳规则。

> 提示：新项目强烈建议从 Omni Realtime API 启动，其统一协议设计、持续模型演进与完整多模态能力更能支撑未来产品需求。仅当存在明确的轻量、低成本、短时长、纯文本响应场景时，再评估 Realtime API 的适用性。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


