# 语音合成与语音识别对比

本文旨在帮助开发者清晰区分百炼平台中**语音合成（TTS）**与**语音识别（ASR）**两项核心音频能力的技术定位、使用边界与选型逻辑。二者虽同属“语音↔文本”双向转换范畴，但在数据流向、模型目标、接口设计及工程实践上存在本质差异。正确理解其异同，是构建稳定、低延迟、高可用语音应用（如智能客服、无障碍交互、会议纪要系统）的前提。

---

## 关键维度对比

| 维度 | 语音合成（TTS） | 语音识别（ASR） |
|------|----------------|----------------|
| **核心功能** | 将结构化文本（Text）转换为自然语音波形（Audio） | 将原始语音信号（Audio）转换为可读文本（Text） |
| **输入格式** | `input.text`（UTF-8 字符串），支持带标点、停顿标记（如 `<break time="300ms"/>`）；部分模型支持 SSML（需参数启用） | `input.audio_url`（HTTPS 公开 URL）或 `input.audio_bytes`（Base64 编码 PCM/MP3/M4A，≤10 MB）；要求采样率 16kHz/44.1kHz，单声道优先 |
| **输出格式** | `output.audio_url`（生成语音的临时 HTTPS 下载链接）或 `output.audio_bytes`（Base64 编码 WAV/MP3）；支持流式响应（`Accept: text/event-stream`）返回音频分块 | `output.text`（识别结果文本）、`output.words`（带时间戳的词级对齐）、`output.punctuation`（自动加标点结果）；支持流式返回增量识别结果（实时 ASR） |
| **主流支持模型** | `cosyvoice-300m`（多音色、情感可控）、`qwen-tts-v1`（Qwen 系列原生 TTS）、`sambert-zh-cn`（中文高拟真） | `paraformer-realtime-v1`（低延迟流式）、`paraformer-v2`（高精度离线转写）、`whisper-large-v3`（多语种强泛化） |
| **API 端点** | `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio`（统一音频 API） | `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio`（同一端点，通过 `model` 参数区分） |
| **计费方式** | 按**合成语音时长（秒）**计费（例：1 分钟语音 = 60 秒 × 单价）；支持按字符数折算（仅限部分模型，详见定价页） | 按**识别音频时长（秒）**计费（例：1 分钟音频 = 60 秒 × 单价）；流式识别按实际处理时长累计，非请求时长 |
| **典型场景** | • 智能播报（天气、新闻朗读）<br>• 有声书/课件自动配音<br>• IVR 语音导航提示<br>• 个性化语音助手回复 | • 会议录音转文字纪要<br>• 客服通话实时转写与质检<br>• 视频字幕自动生成<br>• 语音搜索与指令控制 |
| **流式能力支持** | ✅ 支持（需设置 `Accept: text/event-stream`，返回 `audio.chunk` 事件）<br>• 适用于长文本分段合成、低延迟播放 | ✅ 支持（`paraformer-realtime-v1` 等模型专为流式优化）<br>• 支持 WebSocket 连接下实时音频帧输入与增量文本输出 |
| **多模态集成路径** | • 在 `omni realtime api` 中作为 `output.audio.chunk` 输出环节<br>• 在 `realtime api` 中需配合 AOQ 模型 + 音频输出扩展启用 | • 在 `omni realtime api` 中作为 `input.audio` 输入环节<br>• 在 `realtime api` 中需启用 `input_audio_format` 并申请 ASR 权限 |

> 💡 **注意**：  
> - TTS 与 ASR **共用同一 RESTful 端点**，但模型标识符（`model`）互斥，不可混用；  
> - `omni realtime api` 是唯一将 ASR+LLM+TTS **深度耦合为原子操作**的接口，适合端到端语音对话；而独立 TTS/ASR API 更适合解耦、可插拔的模块化架构；  
> - 所有音频 API 均要求音频格式为 WAV（PCM）、MP3 或 M4A，**不支持 FLAC、AMR、OPUS 等格式**。

---

## 适用场景建议

### ✅ 推荐选择 **语音合成（TTS）** 当：
- 你已有结构化文本内容（如知识库问答结果、通知消息、脚本台词），需将其转化为自然语音输出；
- 应用对语音表现力有明确要求：需指定音色（如“知性女声”“儿童音”）、调节语速/语调/停顿，或启用情感渲染（`cosyvoice-300m`）；
- 场景涉及个性化声音复刻（Voice Cloning）：需提前注册声纹并传入 `voice_id`（仅 `qwen-omni` 支持）；
- 构建播客生成、AI 教师讲解、无障碍阅读等“文本→语音”单向服务。

### ✅ 推荐选择 **语音识别（ASR）** 当：
- 你拥有原始语音数据（如会议录音、用户语音指令、客服通话），需提取其中语义信息；
- 要求高准确率与强鲁棒性：支持中英文混合、方言口音、背景噪音抑制（推荐 `paraformer-v2`）；
- 需要实时交互反馈：如语音输入搜索、实时字幕、语音控制面板（推荐 `paraformer-realtime-v1` + 流式）；
- 后续流程依赖文本：如转交 LLM 进行摘要、分析、翻译，或存入文本数据库检索。

### ⚠️ 需谨慎评估或组合使用的场景：
- **全双工语音对话系统**：  
  → 不建议分别调用独立 TTS+ASR（存在状态同步、延迟叠加、上下文断裂风险）；  
  → **首选 `omni realtime api`**：天然支持 ASR→LLM→TTS 全链路流式闭环，内置会话管理与音频编解码适配。  
- **需同时处理语音输入与输出，但逻辑复杂（如多轮工具调用+语音反馈）**：  
  → 可选用 `realtime api`（WebSocket），通过 `tools` + `output.audio.delta` 实现灵活编排，但需自行处理音频格式转换与流控。  
- **批量离线处理（如万条录音转写）**：  
  → 优先使用 RESTful ASR（`paraformer-v2`），避免 WebSocket 连接管理开销；TTS 同理，批量合成推荐异步任务队列模式。

---

## 技术选型参考（面向开发者）

| 选型考量项 | 推荐方案 | 说明 |
|------------|----------|------|
| **入门级快速验证** | RESTful TTS / ASR | 无需 WebSocket 开发，标准 HTTP POST 即可调通；适合 PoC、脚本自动化、后台批处理 |
| **低延迟实时交互（<500ms 端到端）** | `omni realtime api`（`qwen-omni`） | 最小化链路跳转，服务端统一调度 ASR/TTS 编解码与缓冲，实测平均首字延迟 <300ms |
| **高定制化语音输出（音色/情感/节奏）** | `cosyvoice-300m`（RESTful）或 `qwen-omni`（实时） | `cosyvoice` 提供丰富 voice preset 与细粒度参数（`emotion`, `breathiness`）；`qwen-omni` 支持 voice_id 复刻 |
| **强抗噪/多方言/高精度转写** | `paraformer-v2`（RESTful 离线）或 `paraformer-realtime-v1`（流式） | `paraformer-v2` 在嘈杂环境与专业术语场景准确率显著优于通用模型；流式版支持 16kHz 实时帧输入 |
| **与大模型深度协同（如语音提问→文本思考→语音回答）** | `omni realtime api` > `realtime api` > 独立 API 串联 | `omni` 提供原生多模态事件总线；`realtime` 需手动桥接 audio/text 通道；独立 API 串联需自行维护 session state 与错误重试 |
| **成本敏感型长文本合成（如电子书）** | `qwen-tts-v1`（RESTful） | 单位时长成本较低，基础音质满足通用播报需求；避免为高拟真音色支付溢价 |

> 📌 **最后提醒**：  
> - 所有音频 API 均受 **单次请求音频时长 ≤ 60 秒** 限制（音乐生成除外），超长内容请分段处理；  
> - 音频 URL 必须支持 `HEAD` 请求且无鉴权跳转，否则返回 `400 InvalidAudioUrl`；  
> - 生产环境务必配置重试机制（针对 `5xx` 服务端错误）与降级策略（如 TTS 失败时 fallback 文本提示）；  
> - 调试建议开启 `debug: true` 参数（若模型支持），获取更详细的中间过程日志与 trace ID。

---  
*文档更新日期：2024年6月*  
*依据百炼平台 v2.3.0 音频 API 规范整理*

## 被对比主题页

- [audio api references](../api/audio-api-references.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)


