# 语音合成与语音识别对比

本页旨在帮助开发者清晰区分百炼平台中**语音合成（TTS）**与**语音识别（ASR）**两大核心音频能力的技术定位、使用边界与选型依据。二者虽同属语音处理范畴，但在数据流向、模型目标、接口设计及计费逻辑上存在本质差异。正确理解其异同，是构建高质量语音交互应用（如智能客服、无障碍服务、会议纪要系统）的前提。

---

## 关键维度对比

| 维度 | 语音识别（ASR） | 语音合成（TTS） |
|------|----------------|----------------|
| **核心目标** | 将**输入的语音信号**准确转换为对应文本（Speech → Text） | 将**输入的文本内容**生成自然、可懂的语音波形（Text → Speech） |
| **输入格式** | 音频文件或流：<br>• `input.audio_url`（推荐，OSS/公网可访问 URL）<br>• `input.audio_bytes`（Base64 编码，≤ 25 MB）<br>• 格式：WAV/MP3/OGG/M4A；采样率 ≥ 8 kHz（推荐 16 kHz），单声道优先 | 文本字符串：<br>• `input.text`（纯文本，支持中英文混合、标点、基础停顿符号）<br>• 可选结构化提示（如 `<prosody rate="1.2">`，需模型支持） |
| **输出格式** | 结构化 JSON 响应：<br>• `output.text`：识别出的完整文本<br>• `output.segments`（可选）：分段文本 + 时间戳（启用 `parameters.word_timestamps=true`）<br>• 无音频输出 | 结构化 JSON 响应：<br>• `output.audio_url`：生成语音的临时可下载 URL（有效期 24 小时）<br>• `output.duration`：音频时长（秒）<br>• 无文本输出（除调试日志外） |
| **支持模型（独立 API）** | • `paraformer-v1`（主力中文 ASR 模型）<br>• `whisper-large-v3`（多语种强泛化）<br>• `asr-telephony-v1`（电话信道优化） | • `cosyvoice-v1`（高拟真、多音色、支持情感控制）<br>• `tts-faster-v1`（低延迟、高吞吐场景）<br>• `qwen2-audio-tts`（Qwen2-Audio 系列专用 TTS） |
| **API 端点（RESTful）** | `POST /v1/audio/transcribe` | `POST /v1/audio/synthesize` |
| **API 端点（实时流式）** | • Omni Realtime API 中通过 `enable_asr=true` 启用<br>• Realtime API 中 `qwen2-audio` 模型原生支持音频流输入 | • Omni Realtime API 中通过 `enable_tts=true` 启用（返回 `output.audio.delta` 流）<br>• Realtime API 中 `qwen2-audio` 模型支持 `output.audio` [流式输出](../concepts/streaming-output.md) |
| **计费方式** | **按音频秒数计费**：<br>• 计费单位 = 输入音频总时长（秒），向上取整<br>• 例：上传 98.3 秒音频 → 计费 99 秒 | **按音频秒数计费**：<br>• 计费单位 = 生成音频总时长（秒），向上取整<br>• 例：输入文本生成 42.1 秒语音 → 计费 43 秒 |
| **典型场景** | • 会议录音转文字纪要<br>• 客服通话质检与话术分析<br>• 视频字幕自动生成<br>• 语音搜索与指令唤醒（前端 ASR） | • 智能音箱/车载语音播报<br>• 有声读物与教育课件配音<br>• IVR 语音导航与通知播报<br>• 无障碍阅读（视障辅助） |
| **延迟特性** | • RESTful 接口：异步处理，典型响应延迟 1–5 秒（取决于音频长度）<br>• 实时流式（Omni）：端到端延迟 < 800 ms（含网络+ASR+LLM+TTS 全链路） | • RESTful 接口：异步生成，典型响应延迟 2–8 秒（含编码+合成）<br>• 实时流式（Omni）：首包音频延迟 < 300 ms，持续[流式输出](../concepts/streaming-output.md) |

---

## 适用场景建议

### ✅ 选择语音识别（ASR）当：
- 你拥有**原始语音数据**（录音文件、实时麦克风流、电话录音），需要从中提取**可编辑、可搜索、可分析的文本信息**；
- 业务强依赖**时间对齐能力**（如字幕同步、关键词定位、说话人分离）；
- 场景对**识别鲁棒性要求高**（如嘈杂环境、带口音普通话、中英文混说），需选用 `paraformer-v1` 或 `whisper-large-v3`；
- 你正在构建**语音驱动的工作流起点**（例如：语音输入 → ASR → NLU → 业务决策 → TTS 输出）。

### ✅ 选择语音合成（TTS）当：
- 你已有**结构化文本内容**（新闻摘要、订单状态、教学脚本），需要将其转化为**自然、可信、符合角色设定的语音输出**；
- 应用对**音色一致性、情感表达、语速语调可控性**有明确要求（如品牌语音助手、虚拟主播），应选用 `cosyvoice-v1` 并配置 `parameters.voice` 与 `speech_rate`；
- 需要**低延迟语音反馈**（如实时对话机器人），必须采用 Omni Realtime API 的流式 TTS 能力，避免 RESTful 的请求往返开销；
- 你正在构建**语音交互闭环的终点**（例如：ASR → LLM → TTS），此时 TTS 是用户感知层的关键交付。

### ⚠️ 注意：避免常见误用
- ❌ 不要用 TTS 接口去“识别”语音——它不接受音频输入，会直接报错 `400 Bad Request`；  
- ❌ 不要用 ASR 接口去“生成”语音——它不返回任何音频，`output.audio_url` 字段不存在；  
- ❌ 不要在非流式场景下强行使用 Omni Realtime API 的 `qwen-omni` 模型替代独立 ASR/TTS——它强制绑定全链路（ASR+LLM+TTS），资源开销大、灵活性低，仅适用于**端到端实时对话**；  
- ❌ 不要忽略音频格式规范：ASR/TTS 均要求 16kHz 单声道 PCM/WAV 以获得最佳效果；非标准格式将显著降低质量或触发失败。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 理由 |
|----------|-----------|------|
| **批量处理历史录音（>1000 条）** | RESTful ASR (`/v1/audio/transcribe`) + 批量任务队列 | 成本可控、易并行、错误隔离好；避免 WebSocket 连接管理复杂度 |
| **实时语音助手（唤醒→听写→思考→播报）** | Omni Realtime API (`qwen-omni`) + `enable_asr=true` & `enable_tts=true` | 单连接完成全链路，端到端延迟最低，支持 `input.interrupt` 实时打断 |
| **仅需文本转语音（无识别/理解环节）** | RESTful TTS (`/v1/audio/synthesize`) + `cosyvoice-v1` | 接口简洁、参数明确、音质稳定；适合配音、通知等静态内容场景 |
| **高并发 IVR 语音播报（每秒数百路）** | RESTful TTS + `tts-faster-v1` 模型 + CDN 缓存 `audio_url` | 吞吐优先，牺牲部分表现力换取高 QPS；生成后 URL 可长期复用（如固定欢迎语） |
| **需 ASR + 自定义大模型推理 + 自选 TTS 音色** | 分离调用：<br>1. `/v1/audio/transcribe` → 获取文本<br>2. `/v1/chat/completions`（Realtime API）→ LLM 处理<br>3. `/v1/audio/synthesize` → 指定音色合成 | 最大自由度：可混搭最优 ASR 模型、最强 LLM、最适配音色，便于灰度发布与 A/B 测试 |

> 💡 **最佳实践提示**：  
> - 所有音频 API 均需在 Header 中携带 `Authorization: Bearer <API_KEY>`；  
> - 生产环境务必校验响应状态码（`200 OK`）与 `output` 字段完整性，避免空响应导致前端崩溃；  
> - 对于长音频（>60 秒），建议客户端主动分片（如按句子/段落切分），提升容错性与用户体验；  
> - 使用 `audio_url` 而非 `audio_bytes` 可显著降低请求体体积与超时风险，推荐接入阿里云 OSS 存储音频源。

---  
*最后更新：2024年10月*  
*文档依据：`api/audio-api-references.md`、`api/omni-realtime-api.md`、`api/realtime-api-user-guide.md`*

## 被对比主题页

- [audio api references](../api/audio-api-references.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


