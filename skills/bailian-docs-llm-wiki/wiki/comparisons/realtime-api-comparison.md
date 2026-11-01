# 实时 API 方案对比：Omni Realtime 与 Realtime API

本文旨在为百炼平台开发者提供清晰、可落地的技术选型参考，系统对比两类核心实时 API 方案——**Omni Realtime API** 与 **Realtime API**。随着智能座舱、实时音视频分析、多模态人机交互等场景对低延迟、高保真、多源协同能力的要求持续提升，选择适配业务本质需求的实时接口至关重要。二者虽均基于 WebSocket 实现流式双向通信，但在设计哲学、能力边界、协议抽象层级及适用范式上存在显著差异。本对比聚焦可验证的技术事实，避免主观倾向，助力团队在架构设计初期做出高效、可持续的决策。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API |
|------|-------------------|--------------|
| **协议与连接方式** | WebSocket（`wss://dashscope.aliyuncs.com/realtime/v1/omni`），需携带 `Authorization: Bearer <api_key>` 请求头 | WebSocket（`wss://dashscope.aliyuncs.com/realtime/v1/audio`），所有认证与配置通过 URL 查询参数传递（如 `model`, `api_key`） |
| **输入格式** | 结构化事件驱动：<br>• `input.audio`（PCM，16-bit 小端，16k/48k Hz）<br>• `input.image`（原始 RGB/BGR 帧，需指定 `frame_rate`/`resolution`）<br>• `input.text`（UTF-8 JSON 字符串）<br>• 不支持压缩音频/图像（如 MP3、JPEG） | 二进制帧 + 控制帧混合：<br>• 音频：纯 PCM 二进制帧（16-bit 小端，单声道，16kHz）<br>• 控制指令：JSON 文本帧（如 `session.update`, `turn_detection`）<br>• **不支持图像或文本直接输入** |
| **输出格式** | 结构化服务端事件：<br>• `output.text.delta`（流式文本片段）<br>• `output.audio.chunk`（合成音频 PCM 块）<br>• `output.image.analysis`（视觉理解结果）<br>• `event.latency_exceeded` 等状态通知 | 混合类型响应：<br>• JSON 控制帧（如 `{"type": "transcript", "text": "..."}`）<br>• 二进制 PCM 音频帧（TTS 输出）<br>• **无结构化视觉或跨模态联合输出事件** |
| **支持模型** | • `qwen2-audio-realtime-v1`（音频流多轮理解+生成）<br>• `qwen2-vl-realtime-v1`（视觉-语言联合流式推理）<br>→ **原生支持多模态融合建模** | • `qwen-audio-realtime-v1`（ASR+LLM 串联）<br>• `qwen-tts-realtime-v2`（情感化 TTS）<br>→ **聚焦语音单模态，LLM 作为后处理环节接入** |
| **核心能力定位** | **端到端多模态实时会话引擎**：<br>• 帧级 ASR + 实时语义理解 + 图像帧理解 + 流式 LLM 生成 + 音频合成<br>• 内置上下文保持、中断恢复、多轮意图跟踪 | **高性能语音管道（ASR/TTS 专用）**：<br>• 极致优化的语音识别与合成链路<br>• LLM 推理需显式串联（如 ASR 输出 → 调用独立 LLM API → TTS 输入），非原生一体化 |
| **典型延迟指标（P95）** | 端到端 ≤ 400ms（含多模态对齐开销），`max_latency_ms` 可配置（建议 300–800ms） | 端到端 ≤ 300ms（纯语音路径），静音检测与 turn 切换优化更成熟 |
| **会话生命周期** | 最长 10 分钟；需显式发送 `session.terminate`；异常断连后服务端 30 秒自动清理 | 最长 15 分钟；依赖客户端心跳与 turn detection 驱动生命周期管理 |
| **并发限制** | 同一 API Key 下最多 5 个并发会话 | 受项目级配额控制（具体数值见配额文档），通常高于 Omni Realtime 的硬限制 |
| **计费方式** | 按**实际处理的音频时长（秒） + 图像帧数 + 生成 token 数**分项计费；多模态能力按使用模块分别计量 | 按**语音输入时长（秒） + 语音合成时长（秒）** 计费；LLM 调用若独立发起，另行计费 |
| **错误处理粒度** | 细粒度事件码：<br>• `invalid_input_format`（格式不符）<br>• `model_unavailable`（模型不可用）<br>• `latency_exceeded`（超时）<br>• 所有错误均通过标准服务端事件推送 | 标准 WebSocket 错误码（如 `429`）+ 自定义 JSON 错误帧（`{"type": "error", "code": "invalid_audio"}`） |

## 适用场景建议

### ✅ 推荐选用 **Omni Realtime API** 当：
- 业务需**同时处理语音、摄像头画面、用户文本输入**（如：AR 远程协作中边说话边圈选屏幕内容、智能眼镜实时翻译+场景描述）；
- 要求**多模态语义对齐与联合推理**（例如：根据用户语音指令“把刚才拍的红色汽车照片发给张三”，系统需同步理解语音、定位图像中的目标并执行操作）；
- 架构追求**协议统一、减少胶水代码**，希望在一个 WebSocket 连接内完成全链路交互，而非拼接多个独立 API；
- 对**中间结果实时性要求高**（如 ASR 中间词、图像关键帧分析结果需即时反馈给前端 UI）；
- 团队具备事件驱动开发经验，能妥善处理结构化事件流的状态机逻辑。

### ✅ 推荐选用 **Realtime API** 当：
- 核心需求是**超高性能、超低抖动的语音交互闭环**（如车载语音助手、呼叫中心实时转写+应答）；
- 技术栈已深度集成**PCM 音频采集/播放管线**，且无需图像或文本混合输入；
- 需要**极致可控的静音检测（VAD）与对话轮次（turn）管理**，对 `turn_detection` 参数（如 `threshold`, `delay`）有精细化调优需求；
- 团队偏好**轻量级二进制帧协议**，希望最小化 JSON 解析开销，或已有成熟 SDK 封装（如 AOQ 客户端 SDK）；
- 成本敏感且业务纯语音为主，希望规避多模态能力带来的额外计费项。

## 技术选型参考指南（面向开发者）

1. **先明确输入模态组合**：  
   若输入仅含语音 → 优先评估 Realtime API；若确定需音+视+文任意组合 → Omni Realtime 是唯一选择。

2. **审视延迟预算与稳定性要求**：  
   Realtime API 在纯语音路径下 P95 延迟更低（≤300ms），且 turn 切换更鲁棒；Omni Realtime 多模态对齐引入少量额外调度开销（P95 ≤400ms），但提供更丰富的中间反馈能力。

3. **评估工程复杂度**：  
   Realtime API 协议更“贴近硬件”（二进制帧），适合嵌入式/移动端深度优化；Omni Realtime 使用 JSON 事件，调试友好、易与 Web 前端集成，但需处理更复杂的事件状态机（如 `session.update` → `input.*` → `output.*` → `session.terminate` 序列约束）。

4. **关注长期演进路径**：  
   Omni Realtime 是百炼平台面向 AGI 交互范式的下一代实时接口，将持续扩展多模态模型（如视频流、3D 点云）；Realtime API 作为成熟语音专项通道，将保持高稳定性与向后兼容性，但功能迭代侧重语音体验深化（如方言增强、抗噪算法）。

5. **务必进行真实环境压测**：  
   - 使用生产级网络（含弱网模拟）测试两种方案的连接建立成功率、断连恢复时间、长会话内存占用；  
   - 验证多并发场景下的资源隔离性（尤其注意 Omni Realtime 的 5 会话硬限）；  
   - 对比相同语音样本在两种 API 下的识别准确率与响应一致性（部分模型底层共享 ASR 引擎，但上下文处理逻辑不同）。

> **最后提醒**：二者**不互斥**。典型架构中，可由 Realtime API 承担前端语音采集与基础 ASR，再将识别文本 + 关键图像帧转发至 Omni Realtime 进行多模态融合决策，实现能力分层与成本优化。请依据场景本质需求，而非技术新鲜度，做出理性选择。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


