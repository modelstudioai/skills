# 语音合成与语音识别对比

本页旨在为开发者提供语音合成（TTS）与语音识别（ASR）两大核心音频能力的系统性对比，帮助在实际项目中快速理解二者的技术定位、接口差异与选型逻辑。随着智能语音交互场景日益丰富（如客服机器人、会议纪要、无障碍应用、有声内容生成等），准确区分 TTS 与 ASR 的能力边界、输入输出范式及工程约束，是构建稳定、低延迟、高可用音频链路的前提。

以下对比基于百炼平台当前（2024年Q4）正式发布的 API 规范，涵盖标准 RESTful 接口与实时流式接口（Realtime API / Omni Realtime API），所有信息均以控制台可选模型和官方文档为准，不包含已下线或实验性功能。

## 关键维度对比表

| 维度 | 语音识别（ASR） | 语音合成（TTS） |
|------|----------------|----------------|
| **核心任务** | 将**语音信号**转换为**结构化文本**（含标点、说话人标签、时间戳等） | 将**自然语言文本**转换为**高质量语音波形**（支持音色、语速、情感调节） |
| **输入格式** | • `audio_url`（公开可访问的 WAV/MP3/PCM 链接）<br>• 或 `audio_bytes`（Base64 编码的原始音频数据）<br>• 强制要求：单声道，推荐采样率 `16000 Hz`，时长 ≤ 60 秒 | • `input.text`（UTF-8 文本字符串）<br>• 可选 `input.ssml`（支持简单 SSML 标签，如 `<prosody rate="1.2">`）<br>• 无音频输入要求 |
| **输出格式** | • `json`：返回 `text`、`segments`（含 start/end 时间、speaker）、`punctuated_text` 等字段<br>• `stream`（仅实时 ASR）：SSE 流式返回中间结果（`is_final=false`）与终态结果（`is_final=true`） | • `json`：返回 `audio_url`（托管音频链接）或 `audio_bytes`（Base64 编码 WAV）<br>• `stream`（TTS 流式）：SSE 返回分块音频二进制数据（`audio.delta`），支持边生成边播放 |
| **主流支持模型** | • `paraformer-v1`（通用高精度）<br>• `qwen-audio`（Realtime API 中的端到端语音理解模型）<br>• `qwen-omni-realtime-*`（Omni 实时接口中集成 ASR 子模块） | • `cosyvoice-v1`（多音色、高自然度）<br>• `qwen-omni-realtime-*`（Omni 接口中内置 TTS 引擎，支持声音复刻）<br>• *注：`qwen-audio` 仅支持 ASR，不提供 TTS 能力* |
| **API 端点（RESTful）** | `POST /api/v1/audio/transcribe` | `POST /api/v1/audio/synthesize` |
| **API 端点（实时流式）** | • Realtime API：`wss://.../realtime/v1/qwen-audio`（需传音频帧）<br>• Omni Realtime：`wss://.../api/v1/omni-realtime`（自动协同 ASR+TTS） | • Omni Realtime：`wss://.../api/v1/omni-realtime`（服务端直接推送 `response.audio.delta`）<br>• *标准 Realtime API 不提供独立 TTS 流式端点* |
| **计费方式** | • 按**音频时长（秒）** 计费（向上取整）<br>• 支持并发调用，但单次请求音频 ≤ 60 秒 | • 按**生成语音时长（秒）** 计费（以最终输出音频时长为准）<br>• 声音复刻（Voice Cloning）另计「克隆实例」费用，与合成时长分离 |
| **典型场景** | • 会议录音转文字纪要<br>• 客服通话语音质检<br>• 视频字幕自动生成<br>• 实时语音输入法 | • 有声书/播客内容生成<br>• IVR 语音导航播报<br>• AI 助手语音应答（配合 LLM）<br>• 个性化语音通知（如带姓名的快递提醒） |
| **流式能力支持** | ✅ 全面支持：<br>– RESTful `response_format=stream`（适合短音频）<br>– Realtime API（WebSocket，低延迟音频帧流）<br>– Omni Realtime（端到端流式协同） | ✅ 支持，但路径受限：<br>– RESTful `response_format=stream`（返回分块 Base64）<br>– **仅 Omni Realtime API 提供原生二进制音频流（`audio.delta`）**，延迟最低（<300ms 端到端）<br>– Realtime API 无独立 TTS 流式能力 |
| **特殊能力扩展** | • 多语种识别（中/英/日/韩等）<br>• 说话人分离（Speaker Diarization）<br>• 静音过滤与信噪比自适应 | • 多音色选择（男/女/童声/角色音）<br>• 语速/音调/停顿精细调节<br>• 声音复刻（需上传 30s+ 参考音频，生成专属音色） |

## 各方案适用场景建议

| 场景需求 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| **离线批量处理长录音（如 45 分钟会议）** | RESTful ASR（`paraformer-v1` + `audio_url`） | 支持最大 60 秒分片上传，配合服务端自动拼接；计费清晰，无需维护长连接；适合后台异步任务队列。 |
| **实时语音输入法（用户边说边出字）** | Realtime API（`qwen-audio`） | WebSocket 协议保障 <500ms 端到端延迟；支持音频帧级流式输入与中间结果（`interim_results`）；无需预切分音频。 |
| **全双工语音助手（听—思—说闭环）** | Omni Realtime API（`qwen-omni-realtime-*`） | **唯一支持 ASR+LLM+TTS 全链路流式协同的接口**：语音输入 → 实时识别 → LLM 推理 → 语音合成 → 音频流直推，全程共享上下文与状态，避免多次 API 调用引入延迟与错误累积。 |
| **生成高拟真有声内容（如企业宣传音频）** | RESTful TTS（`cosyvoice-v1` + `input.ssml`） | 支持 SSML 精细控制停顿与重音；输出高保真 WAV；适合对音质、节奏要求严苛的成品制作；可预生成并 CDN 分发。 |
| **定制化语音播报（如银行APP客户专属语音）** | Omni Realtime API + `voice_clone_id` | 声音复刻能力仅在此接口开放；支持将客户授权语音克隆为播报音色，兼顾安全性与个性化；流式合成确保自然连贯。 |
| **轻量级 Web 应用嵌入语音播报（无后端）** | RESTful TTS（`cosyvoice-v1` + `response_format=json`） | 前端可直接调用，获取 `audio_url` 后交由 `<audio>` 标签播放；免流式解析复杂度，开发成本最低。 |

## 技术选型参考指南（面向开发者）

- **优先选择 Omni Realtime API 当且仅当**：您的场景需要 **“实时性” + “闭环交互” + “个性化音色”** 三者同时满足。它是目前百炼平台唯一能在一个 WebSocket 连接内完成“语音输入→识别→理解→生成→合成→播放”的方案。若仅需其中一环（如只做识别），请勿过度使用 Omni，以免增加不必要的连接管理与并发配额消耗。

- **RESTful 接口仍是主力选择**：对于非实时、可容忍秒级延迟、需高稳定性和易调试性的场景（如后台批处理、管理后台字幕生成），RESTful `/transcribe` 和 `/synthesize` 接口成熟、文档完善、错误码明确，应作为默认起点。

- **警惕 Realtime API 的能力边界**：`qwen-audio` 是 Realtime API 中唯一的语音模型，但它**只做 ASR，不做 TTS**。若你试图在 Realtime 中实现“语音问答”，必须自行调用 TTS 接口（或降级为 RESTful），这将破坏流式体验。此时请直接评估 Omni Realtime 是否更合适。

- **计费敏感型项目注意**：  
  - ASR 计费按**输入音频时长**，TTS 按**输出语音时长**。例如：输入 10 秒嘈杂录音 → ASR 输出 8 秒精简文本 → TTS 生成 12 秒润色后播报音频，则 ASR 计 10 秒，TTS 计 12 秒。  
  - Omni Realtime 按**会话时长（秒）** 统一计费（从 `session.init` 到连接关闭），无论内部 ASR/TTS 调用多少次，适合高频短交互；而 RESTful 按每次调用独立计费，适合低频长任务。

- **音频工程注意事项**：  
  - 两者均**强制单声道**。双声道音频需预处理（如 ffmpeg `-ac 1`），否则可能静音左/右通道导致识别失败或合成异常。  
  - 采样率不匹配会触发自动重采样（可能轻微劣化音质），强烈建议前端统一采集/编码为 `16kHz PCM`，与平台最优实践对齐。  
  - 流式场景下，Omni Realtime 要求音频帧 ≤20ms（即每帧 320 字节 @16kHz/16bit），需客户端严格分帧，不可整段发送。

如需进一步验证模型效果，建议使用百炼控制台「API 调试」工具，上传真实业务音频样本进行端到端测试，并结合 [语音识别](https://help.aliyun.com/zh/model-studio/speech-recognition-api-reference) 与 [语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis-api-reference) 的最新参数说明文档调整配置。

## 被对比主题页

- [audio api references](../api/audio-api-references.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


