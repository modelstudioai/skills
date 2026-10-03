# Omni Realtime API 与 Realtime API 用户指南对比

本文档面向百炼平台开发者，旨在清晰对比 **Omni Realtime API** 与 **Realtime API** 两大实时流式接口的核心差异，帮助技术团队基于业务需求、模态复杂度、延迟敏感度及工程约束做出合理选型。二者虽同属 WebSocket 协议下的低延迟交互范式，但在设计目标、能力边界、协议语义和适用场景上存在本质区别：Omni Realtime API 定位为**端到端多模态联合推理通道**，强调跨模态上下文一致性与事件级语义控制；而 Realtime API 更侧重**单模态（音频/视频）流的高吞吐、低抖动管道化处理**，以语音活动检测（VAD）和流式 ASR-TTS 集成为核心优化点。正确区分二者可避免模型调用失败、事件解析异常或性能不达预期等问题。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **核心定位** | 多模态（语音+文本+图像）端到端联合推理接口，支持跨模态上下文感知与混合输入 | 单模态（音频/视频）流式处理接口，聚焦语音活动检测（VAD）、流式 ASR/TTS 管道化响应 |
| **输入格式** | 支持三类结构化客户端事件：<br>• `input_audio`（20ms 分片 PCM，16kHz）<br>• `input_text`（UTF-8 字符串指令）<br>• `input_image`（JPEG/PNG，≤1024×1024）<br>※ 各模态可交错发送，共享同一会话上下文 | 仅支持二进制流帧：<br>• `input.audio`（PCM/Opus，采样率严格限定为 16kHz 或 48kHz）<br>• `input.video`（H.264 编码，建议 ≤640×480@15fps）<br>※ 不支持文本或图像直接输入；文本需经 ASR 转译后由模型内部生成 |
| **输出格式** | 语义化服务端事件驱动：<br>• `response.text_delta`（文本 token 增量）<br>• `response.audio_delta`（TTS 音频增量，PCM 格式）<br>• `interim_transcript`（启用 `enable_interim_results` 时触发）<br>• `response.image`（暂未开放） | [流式输出](../concepts/streaming-output.md)事件为主：<br>• `output.text.delta`（ASR 识别结果或 LLM 生成文本）<br>• `output.audio.delta`（TTS 合成音频）<br>• `output.vad`（VAD 检测状态变更）<br>※ 无中间识别事件（如 partial transcript），不提供 `interim` 类事件 |
| **支持模型** | 仅 `qwen-omni-realtime-202410`（v2.1+），强制绑定多模态联合架构；旧版 `qwen-omni-realtime-202408` 已下线 | 多模型可选：<br>• `qwen-audio-realtime-v1`（纯音频流）<br>• `qwen-video-realtime-v1`（音视频融合）<br>• `qwen-rtc-v2`（RTC 场景优化）<br>※ `qwen-rtc-v1` 已于 2024-Q3 下线 |
| **API 端点** | `wss://dashscope.aliyuncs.com/realtime/v1/omni` | `wss://dashscope.aliyuncs.com/realtime/v1/chat` |
| **会话生命周期** | 单次连接 = 单一会话；最大持续时间 `30–300` 秒（由 `max_duration_sec` 控制）；超时或错误后连接强制关闭 | 单次连接最长存活 `10 分钟`；支持在连接内发起多次逻辑会话（通过 `session.update` 重置上下文），但需客户端自行管理会话状态 |
| **并发能力** | 单连接仅支持 **1 个并发会话**（不可复用连接处理多个独立对话） | 单连接支持 **多轮逻辑会话切换**（通过 `session.update` 动态变更 `model`/`input_format`），但同一时刻仅处理一个活跃流 |
| **计费方式** | 按**实际传输的音频时长（秒） + 图像帧数 + 文本 token 数**综合计费；图像与文本输入单独计量；中间结果（`interim_transcript`）不额外计费 | 按**输入音频/视频流时长（秒） + 输出文本 token 数 + 输出音频时长（秒）** 计费；VAD 检测、中断控制等控制帧不计费 |
| **典型场景** | • 具备摄像头与麦克风的智能终端（如会议硬件、AR 眼镜）中的“看听说”一体化交互<br>• 需动态注入图文指令的实时翻译助手（如拍摄菜单后语音提问）<br>• 多轮混合模态客服（用户上传截图 + 语音追问） | • 语音优先的实时对话应用（如车载语音助手、智能音箱）<br>• 直播字幕/会议实时转录（纯音频流输入）<br>• 视频通话中的低延迟语音增强与语义理解（如远程医疗问诊） |
| **关键限制** | • 音频必须严格 20ms 分片，时间戳连续无跳变<br>• 图像单帧 ≤1024×1024，总带宽建议 ≤2 Mbps<br>• 错误重连必须新建 WebSocket 连接 | • 音频采样率仅支持 16kHz（PCM）或 48kHz（Opus）<br>• 视频分辨率建议 ≤640×480，帧率 ≤15fps<br>• 必须每 30 秒发送 `ping` 帧保活 |

## 适用场景建议

### 选择 Omni Realtime API 当：
- 应用需**同时处理语音、文本、图像三种输入**，且要求模型理解其关联性（例如：“这个表格里第三行的数据是多少？”——需结合语音指令与上传的 Excel 截图）；
- 产品形态为**带屏智能硬件或移动 App**，用户习惯混合操作（说话+点击+拍照）；
- 对**端到端延迟可控性要求极高**（如 <800ms），且需精确控制中间识别结果（启用 `enable_interim_results` 获取 ASR partial）；
- 架构设计已采用**事件驱动模型**，能严格遵循客户端/服务端事件 Schema（如 `input_image`, `response.audio_delta`）。

### 选择 Realtime API 当：
- 核心需求是**高鲁棒性语音流处理**，尤其依赖服务端 VAD 自动切分静音段（如嘈杂环境下的车载交互）；
- 输入源为**标准音视频 SDK（如 WebRTC、FFmpeg）**，输出需直接喂给播放器或字幕渲染模块；
- 场景对**单模态吞吐量与稳定性更敏感**，而非跨模态语义融合（如千人级在线会议实时转录）；
- 工程团队希望**复用现有音视频管线**，避免改造图像采集/编码逻辑，且无需文本指令注入能力。

## 技术选型参考（致开发者）

- **不要混用协议语义**：Omni 的 `input_text` 是独立事件，用于注入非语音指令；Realtime API 中无对应能力，文本只能作为 ASR 结果或模型生成输出出现。
- **注意模型锁定风险**：Omni Realtime API 当前仅支持单一模型，升级需等待新版本发布并全量灰度；Realtime API 提供多模型选项，便于 A/B 测试或按场景切换。
- **调试成本差异**：Omni 因支持多模态输入，本地模拟需构造符合 Schema 的 JSON 事件 + 二进制音频/图像帧，调试链路更长；Realtime API 可直接使用 `curl --include --no-buffer` 模拟二进制流，入门门槛略低。
- **容错设计重点不同**：Omni 需重点防御**时间戳乱序/重复**导致的会话中断；Realtime API 需重点保障**网络保活（ping）与帧序一致性**，避免因代理超时或丢包引发连接闪断。
- **未来演进提示**：Omni Realtime API 是百炼多模态战略主干接口，后续将扩展 `response.image_delta`（流式图像生成）与 `input_video`（视频帧理解）；Realtime API 将持续强化 RTC 场景适配（如弱网抗丢包、唇音同步优化），但不计划支持文本/图像直接输入。

请始终以各接口的 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 与 [客户端事件](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 官方 Schema 文档为准，SDK 实现必须进行 JSON Schema 校验，不可依赖字段名猜测或宽松解析。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


