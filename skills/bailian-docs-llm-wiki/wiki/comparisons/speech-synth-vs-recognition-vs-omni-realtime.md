# 语音合成、语音识别与实时语音交互 API 对比

为帮助开发者快速理解百炼平台音频类能力的定位差异，避免模型误用、接口错配或计费偏差，本文对三类核心语音 API —— **语音合成（TTS）**、**语音识别（ASR）** 和 **实时语音交互（含 Omni Realtime 与 Realtime API）** 进行系统性对比分析。对比基于当前（2024年10月）生产环境可用能力，覆盖调用方式、能力边界、技术约束与成本模型，旨在为实际项目中的技术选型提供可落地的决策依据。

---

## 关键维度对比表

| 维度 | 语音合成（TTS） | 语音识别（ASR） | 实时语音交互（含 Omni Realtime & Realtime API） |
|------|----------------|----------------|---------------------------------------------|
| **核心能力** | 将文本转为自然语音（Text-to-Speech） | 将语音转为文本（Speech-to-Text），支持标点恢复、说话人分离 | 端到端流式语音对话：ASR → LLM推理 → TTS 全链路低延迟协同，支持动态干预与中间结果流式返回 |
| **输入格式** | `text`（UTF-8 字符串，≤500 字符）；可选 `sample_rate`、`voice`、`speed` 等控制参数 | `audio_url`（公网可访问 URL）或 `audio_bytes`（Base64 编码的 `wav`/`mp3`/`flac`）；支持 `diarization`、`punctuation` 等增强参数 | **Omni Realtime**：WebSocket 流式 `audio_chunk`（PCM, 16kHz, Base64）；<br>**Realtime API**：WebSocket 流式 `input_audio`（PCM, 16kHz, Base64）或 `input_text` 事件；均需严格遵循事件协议 |
| **输出格式** | `output.audio_url`（1小时有效期直链）或 `output.audio_bytes`（Base64）；格式由 `response_format` 指定（`wav`/`mp3`/`pcm`） | `output.text`（识别文本）、`output.segments`（带时间戳分段）、`output.speakers`（说话人标签，启用 `diarization` 时） | **Omni Realtime**：服务端推送 `transcript`（ASR结果）、`response_text`（LLM回复）、`tts_audio`（PCM, 24kHz）等独立事件；<br>**Realtime API**：流式返回 `output_text_delta`、`output_audio`（原始 PCM 帧）、`output_finished` 等结构化事件 |
| **支持模型** | `qwen2-audio-tts-v1`（默认，非流式）；部分场景支持 `qwen2-audio-tts-stream-v1`（流式） | `qwen2-audio-asr-v1`（默认，支持中英文混合、标点、说话人分离） | **Omni Realtime**：仅 `qwen-omni-realtime-202410`（单模型全栈集成）；<br>**Realtime API**：`qwen-audio-realtime-v1`（音频专用）、`qwen-video-realtime-v1`（音视频融合）；不兼容 TTS/ASR 独立模型 |
| **API 端点** | `POST https://dashscope.aliyuncs.com/api/v1/audio/speech-synthesis` | `POST https://dashscope.aliyuncs.com/api/v1/audio/speech-recognition` | **Omni Realtime**：`wss://dashscope.aliyuncs.com/realtime/v1/omni`（WebSocket）；<br>**Realtime API**：`wss://dashscope.aliyuncs.com/api/v1/realtime?model=...`（WebSocket + query 参数） |
| **调用模式** | 同步 RESTful（支持 `stream=true` 的流式 TTS 接口有限） | 同步 RESTful（非流式，整段音频一次性提交） | **纯流式双向通信**：必须使用 WebSocket，无 HTTP 替代方案；客户端需实现事件监听与状态管理 |
| **计费方式** | 按**合成音频时长（秒）** 计费（以输出 `duration` 为准） | 按**输入音频时长（秒）** 计费（以 `audio_url` 或 `audio_bytes` 解析的实际时长为准） | **Omni Realtime**：按**会话连接时长（秒）** 计费（从 `start` 到连接关闭）；<br>**Realtime API**：按**会话连接时长（秒）** 计费（最长 600 秒/连接）；<br>※ 注意：二者均**不按 token 或字符计费**，与 LLM 接口计费逻辑隔离 |
| **典型时延（P95）** | 首字节响应：300–800 ms（非流式）；流式 TTS 首包约 500 ms | 整体响应：800–2000 ms（取决于音频长度与网络） | **端到端语音交互延迟 ≤ 1.2 秒**（从语音输入结束到 TTS 音频首帧输出）；ASR 中间结果可在 300 ms 内返回 |
| **上下文能力** | 无上下文（单次请求独立） | 无上下文（单次请求独立） | **强上下文感知**：自动维护会话内多轮对话历史（Omni Realtime 依赖客户端透传 `session_id`；Realtime API 自动维护 30 分钟无活动过期会话） |
| **地域限制** | 全地域可用 | 全地域可用 | **Omni Realtime**：仅 `cn-shanghai` 和 `ap-southeast-1`；<br>**Realtime API**：全地域可用（需确认控制台开通权限） |

---

## 各方案适用场景建议

| 方案 | 推荐场景 | 不推荐场景 | 关键原因 |
|------|----------|------------|----------|
| **语音合成（TTS）** | • 有声读物、课件配音、IVR 语音播报<br>• 静态内容批量生成（如客服知识库语音版）<br>• 需精细控制语速、停顿、音色的离线合成任务 | • 实时对话中的动态回复播报<br>• 需与 ASR 结合构建闭环交互系统<br>• 超长文本（>500 字）需分段合成且要求无缝衔接 | 输入为静态文本，无语音输入处理能力；不维护会话状态；流式支持有限，难以匹配实时交互节奏 |
| **语音识别（ASR）** | • 会议录音转写、语音笔记整理、客服通话质检<br>• 批量音频文件离线转录（≤60 秒/段）<br>• 需要高精度标点与说话人分离的后处理分析 | • 实时语音输入即刻反馈（如语音搜索、实时字幕）<br>• 需在识别过程中动态中断或修正<br>• 单次音频超 60 秒（需前端分片） | 同步阻塞式调用，无法流式返回中间识别结果；无实时 VAD（语音活动检测）与打断机制；单次请求时长硬限制 60 秒 |
| **实时语音交互（Omni Realtime）** | • 轻量级智能语音助手（如车载、IoT 设备）<br>• 需极低延迟与端侧轻量集成的嵌入式场景<br>• 多模态融合需求弱，聚焦纯语音闭环交互 | • 需要复杂视觉理解（如看图说话）、图像生成等扩展能力<br>• 超长会话（>3 分钟）且无法接受重连<br>• 需要自定义 ASR/TTS 模型组合（如替换为第三方 TTS） | 单一固定模型，不可拆解替换组件；连接强制 180 秒超时；不支持图像输入；TTS 输出为 24kHz PCM，需客户端自行解码播放 |
| **实时语音交互（Realtime API）** | • 专业级语音对话应用（如虚拟坐席、AI 教师、实时翻译耳机）<br>• 需要动态插入文本指令（如“暂停”、“换种说法”）<br>• 支持音视频融合的智能体（如远程医疗问诊） | • 简单播报类需求（TTS 已足够）<br>• 无 WebSocket 支持的老旧环境（如部分企业内网）<br>• 对连接稳定性要求极高且无法容忍 10 分钟重连 | 依赖 WebSocket 基础设施；最大连接时长 600 秒；需客户端实现完整事件协议解析；并发连接数默认限 5 路 |

---

## 技术选型参考（面向开发者）

请按以下流程进行决策：

1. **明确核心诉求**  
   - 若只需「文本→语音」单向生成 → 选 **TTS**；  
   - 若只需「语音→文本」单向转录 → 选 **ASR**；  
   - 若需「语音输入 → 智能理解 → 语音输出」闭环，且对**端到端延迟敏感**（目标 < 1.5 秒）→ 进入下一步。

2. **评估部署与集成约束**  
   - ✅ 支持 WebSocket + 客户端可维护 `session_id` → 优先选 **Realtime API**（功能最全、会话管理最强、地域支持广）；  
   - ⚠️ 受限于设备算力/网络，需最小化客户端逻辑，且接受 3 分钟会话上限 → 选 **Omni Realtime**（协议更轻量，握手简单）；  
   - ❌ 无法使用 WebSocket（如纯浏览器前端无 ws 支持、或内网策略限制）→ **不可直接使用实时交互 API**，需退回到 TTS+ASR 组合 + 自建调度层（但延迟与体验将显著下降）。

3. **验证关键能力匹配度**  
   - 检查是否需要 **说话人分离** → ASR 支持，Omni/Realtime 当前不提供显式说话人标签；  
   - 检查是否需要 **中英文混合高精度识别** → ASR 与 Realtime API 均支持，Omni Realtime 在混合场景可能降级；  
   - 检查是否需要 **自定义音色/语速/情感** → TTS 支持，Omni/Realtime 的 TTS 组件为固定音色（`qwen2-audio-dialog-tts-v1`），不可配置；  
   - 检查是否需要 **跨模型热切换**（如 ASR 用 A 模型，TTS 用 B 模型）→ Realtime API 不支持，Omni Realtime 与 TTS/ASR 独立接口组合更灵活。

4. **成本与运维考量**  
   - 高频短会话（如每次 < 10 秒）→ Realtime API 按连接时长计费更经济；  
   - 低频长音频转写（如 30 分钟会议）→ ASR 分片调用（每片 ≤60 秒）比维持长连接更省；  
   - 需长期运行服务 → Realtime API 的 600 秒连接上限要求设计优雅的重连与上下文续接逻辑，增加开发复杂度。

> **重要提醒**：所有音频 API 均需通过 `Authorization: Bearer <api_key>` 认证，且 `model` 参数不可省略。切勿复用模型名（如 `qwen2-audio-tts-v1` 不能用于语音对话场景），否则将返回 `ModelNotSupported` 错误。建议在控制台开启「API 调用日志」并结合 `x-request-id` 追踪问题。

---  
*最后更新：2024年10月*

## 被对比主题页

- [audio api references](../api/audio-api-references.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


