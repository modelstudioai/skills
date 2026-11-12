# 语音合成与语音识别对比

本页旨在为开发者提供语音合成（TTS）与语音识别（ASR）两大核心音频处理能力的系统性对比，帮助在百炼平台进行技术选型时快速把握关键差异。二者虽同属“语音—文本”双向转换范畴，但在数据流向、模型设计、调用范式、资源约束及业务适配性上存在本质区别。本文基于百炼平台当前（v3.1+）非实时音频 API 能力整理，聚焦离线/批量场景，不涵盖实时流式交互（如 WebSocket 实时 ASR/TTS）。

## 关键维度对比

| 维度 | 语音识别（ASR） | 语音合成（TTS） |
|------|----------------|----------------|
| **核心功能** | 将输入的**音频信号**转换为**结构化文本**（含标点、段落、说话人分离等） | 将输入的**文本内容**（支持 SSML/LaTeX）转换为**高质量语音音频流或文件** |
| **典型输入格式** | 公网可访问的音频 URL 数组（`file_urls`），或 Base64 编码音频（部分模型支持）；格式支持 wav/mp3/opus/pcm；单文件 ≤200 MB，时长 ≤2 小时（异步） | 纯文本字符串（`text` 字段），支持 SSML 标签（如 `<prosody>`、`<break>`）和 LaTeX 数学公式；长度 ≤5000 字符（Qwen-Audio-TTS） |
| **典型输出格式** | JSON 结构化结果：含 `text`（识别文本）、`segments`（时间戳分段）、`speaker_labels`（说话人标识）、`language_code` 等；异步任务需轮询获取完整结果 | 音频二进制流（同步/流式）或直传 OSS 的音频文件 URL（异步）；支持格式：`mp3`（默认）、`wav`、`opus`、`pcm`；采样率可配（如 `16000`、`22050`、`44100` Hz） |
| **主流支持模型** | `Qwen-Audio-ASR`（上下文增强/SSE 流式）、`Qwen-Audio-ASR-Filetrans`（长音频优化）、`Fun-ASR` / `Fun-ASR-Flash`（高精度/低延迟）、`Qwen-ASR`（OpenAI 兼容协议）、`Paraformer`（华北2 专属） | `Qwen-Audio-TTS`（多音色/高自然度）、`CosyVoice`（强情感表现/多语言混合）；均支持系统音色、复刻音色（需提前定制）、设计音色 |
| **API 端点（HTTP）** | 同步/流式：`POST /api/v1/services/audio/asr`<br>异步提交：`POST /api/v1/services/audio/asr/jobs`<br>异步轮询：`GET /api/v1/tasks/{task_id}` | 同步/流式：`POST /api/v1/services/audio/tts`<br>异步提交：`POST /api/v1/services/audio/tts/jobs`（部分 SDK 封装）<br>音色管理独立端点：`POST /api/v1/services/audio/tts/customization` |
| **调用模式** | • 同步：适用于 ≤1 分钟短音频，即时返回<br>• SSE 流式：仅 `Qwen-Audio-ASR` / `Fun-ASR-Flash` 支持，音频 ≥1 分钟时自动启用<br>• 异步（提交-轮询）：推荐用于长音频（>10 分钟），任务有效期 24 小时 | • 同步：默认模式，返回完整音频二进制<br>• SSE 流式：需设置 `X-DashScope-SSE: enable`，逐块返回音频片段，降低首字节延迟<br>• 异步：SDK 层封装支持，适合大文本批量合成（如有声书） |
| **计费方式** | 按**音频时长（秒）** 计费：<br>• Qwen-Audio-ASR / Fun-ASR 系列：¥0.003/秒（标准价）<br>• Paraformer：¥0.0025/秒（华北2 专享）<br>• 定制热词调用单独计费（¥0.01/次） | 按**合成语音时长（秒）** 计费：<br>• Qwen-Audio-TTS：¥0.004/秒（标准音色），复刻音色 +¥0.001/秒<br>• CosyVoice：¥0.005/秒（含情感增强）<br>• 音色定制（`voice-enrollment`）按次计费（¥1.5/次） |
| **地域约束** | • `Paraformer`：仅支持 `cn-beijing`（华北2）<br>• 定制热词：新加坡地域不可用<br>• `Qwen-ASR` OpenAI 兼容模式：美国地域不可用 | • 全模型均支持 `cn-beijing`、`ap-southeast-1`（新加坡）等主流地域<br>• 音色定制 API 必须与目标 TTS 模型地域一致（如 `cosyvoice-v3.5-plus` 在新加坡创建，则只能在新加坡调用） |
| **典型场景** | • 会议录音转文字纪要<br>• 教育课程视频字幕生成<br>• 客服通话质检与关键词提取<br>• 法律/医疗口述记录归档 | • 智能客服语音播报<br>• 有声读物/电子书朗读<br>• 导航语音提示（多语种切换）<br>• 个性化语音助手（使用复刻音色） |

## 适用场景建议

- **选择 ASR 当且仅当**：  
  ✅ 输入源是**已录制的音频文件**（如 MP3/WAV），目标是获取其**准确、带时间信息的文本内容**；  
  ✅ 需要分析语音中的语义、情绪、说话人角色（依赖 `Qwen-Audio-ASR` 或 `Fun-ASR-Flash` 的高级能力）；  
  ❌ 不适用于实时对话流（应选用 Realtime API）、纯文本生成需求、或需控制语音韵律/音色的场景。

- **选择 TTS 当且仅当**：  
  ✅ 输入源是**结构化文本**（含 SSML 控制停顿、重音、语速），目标是生成**可播放、可下载的语音音频**；  
  ✅ 需要品牌化语音形象（通过 `voice-enrollment` 复刻专属音色）或跨语言自然播报（`CosyVoice` 多语种混合）；  
  ❌ 不适用于将语音转文字、音频内容分析、或无文本输入的纯声音生成（应选用 Audio Generation API）。

> ⚠️ **重要提醒**：ASR 与 TTS **不可互换使用**。尝试用 TTS “反向识别” 音频将导致完全错误的结果；同样，用 ASR “合成” 文本会返回空或乱码。二者是严格单向、不可逆的转换过程。

## 开发者技术选型参考

| 选型考量点 | 推荐方案 | 说明 |
|------------|----------|------|
| **首次集成，追求开箱即用** | ✅ `Qwen-ASR`（ASR） + `Qwen-Audio-TTS`（TTS） | 提供 OpenAI 兼容协议（ASR）与统一 SDK 封装（Python/Java），文档最全，调试成本最低；适合 PoC 和中小规模应用。 |
| **长音频（>30 分钟）批量处理** | ✅ `Qwen-Audio-ASR-Filetrans`（ASR） + 异步 TTS 调用 | `Filetrans` 专为长音频优化，支持分段识别与上下文连贯；TTS 异步模式可并行提交数百任务，避免连接超时。 |
| **低延迟敏感型应用（如实时字幕预处理）** | ✅ `Fun-ASR-Flash`（ASR） + `Qwen-Audio-TTS` 流式（SSE） | `Fun-ASR-Flash` 平均响应 <800ms（1 分钟音频）；TTS SSE 流式可实现 200ms 内首音频块返回，适合准实时播报链路。 |
| **需要高度个性化语音形象** | ✅ `CosyVoice`（TTS） + `voice-enrollment` 音色定制 | `CosyVoice` 对情感、语气建模更强；音色定制支持 10 秒级快速复刻，且 `cosyvoice-v3.5-plus` 支持中英混读自然切换。 |
| **合规与安全要求极高** | ✅ 全流程使用**业务空间专属域名** + **临时 API Key** | 所有请求必须使用 `{WorkspaceId}.{region}.maas.aliyuncs.com` 域名；高风险调用务必生成 60 秒有效期临时 Key，禁用硬编码。 |

**最后建议**：  
- 在正式上线前，务必使用真实业务音频样本进行**端到端压测**（尤其关注 `Paraformer` 地域限制、`Qwen-ASR` OpenAI 协议兼容性）；  
- 所有音频输入请严格遵循[音频规格文档](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)预处理（推荐 `ffmpeg -i input.mp3 -ac 1 -ar 16000 -f mp3 -`）；  
- 错误处理应覆盖异步任务失败重试（需新 `task_id`）、TTS 流式中断重连、以及 `429 RateLimit` 的指数退避策略。

## 被对比主题页

- [audio api directory](../api/audio-api-directory.md)
- [voice customization api directory](../api/voice-customization-api-directory.md)


