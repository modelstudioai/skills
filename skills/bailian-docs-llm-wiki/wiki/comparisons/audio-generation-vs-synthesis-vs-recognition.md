# 语音生成、语音合成与语音识别对比

## 目的与背景

在百炼平台的音频能力体系中，“语音生成”“语音合成”和“语音识别”常被开发者混用或误判，导致技术选型偏差、API 调用失败或计费异常。本文旨在厘清三者在**技术本质、输入输出语义、平台实现路径及工程约束**上的根本差异，为开发者提供清晰、准确、可落地的技术选型参考。需特别强调：  
- **语音识别（ASR）** 是 *听觉理解* 过程（音频 → 文本）；  
- **语音合成（TTS）** 是 *文本发声* 过程（文本 → 音频），属狭义“语音生成”的子集；  
- **语音生成（Audio Generation）** 在百炼平台特指 *非文本驱动的端到端音频内容创建*（如音效生成、音乐生成、带情感/场景的语音生成等），目前尚未开放通用 API，其能力主要通过 **音色定制 + TTS 协同实现**（如复刻音色+SSML控制生成拟人化播报），或由未来发布的 `qwen-audio-gen` 等模型承载。  
本文对比聚焦于当前**已正式发布、稳定可用的音频处理能力**，即 ASR 与 TTS（含音色定制支撑链路），并明确标注“语音生成”在当前平台的实际定位与替代方案。

---

## 关键维度对比表

| 维度 | 语音识别（ASR） | 语音合成（TTS） | 语音生成（当前平台定位） |
|------|------------------|-------------------|----------------------------|
| **核心任务** | 将语音信号转换为可读文本（Speech-to-Text） | 将结构化文本转换为自然语音（Text-to-Speech） | *暂无独立通用 API；实际能力通过「音色定制 + TTS」组合实现，用于生成高个性化、场景化语音内容* |
| **典型输入格式** | 音频文件（MP3/WAV/OPUS/FLAC），支持 URL 或 Base64；部分模型要求 16kHz 单声道（如 Paraformer） | 纯文本、SSML（启用 `enable_ssml=true`）、LaTeX 数学表达式；不接受音频输入 | 无直接输入；依赖上游：① 音色复刻：30–60 秒人声样本（WAV/MP3）；② 音色设计：文本 prompt（≤200 字符）或参考音频 URL |
| **典型输出格式** | JSON 结构化文本结果（含 `text`、`segments`、`timestamps` 等）；流式 SSE 返回分片文本 | 音频二进制流（HTTP 响应体）或 Base64 编码字符串；支持格式：`mp3`/`wav`/`opus`；采样率按模型支持（如 CosyVoice 仅支持 8k–48k） | 无直接输出；最终产出为 **TTS 接口调用时指定 `voice_id` 后生成的音频**（格式/采样率同 TTS） |
| **平台支持模型** | • Qwen-Audio-ASR（高精度，支持上下文）<br>• Qwen-Audio-ASR-Filetrans（长音频异步）<br>• Fun-ASR / Fun-ASR-Flash（轻量低延迟）<br>• Paraformer（开源高性能）<br>• 定制热词（`speech-biasing`） | • Qwen-Audio-TTS（全功能，多音色/SSML/LaTeX）<br>• CosyVoice（v3.5-plus/v3-flash，仅华北2）<br>• Qwen-TTS / MiniMax（第三方集成） | • 音色复刻：`sound-reengraving-v1`（支持中/英/日三语样本）<br>• 音色设计：`voice-design-v1`（文本描述或风格迁移） |
| **核心 API 端点** | • 同步：`POST /api/v1/audio/asr`（Qwen-Audio-ASR）<br>• 异步：`POST /api/v1/audio/asr/filetrans`（提交） + `GET /api/v1/tasks/{task_id}`（轮询） | • 同步：`POST /api/v1/audio/speech`（Qwen-Audio-TTS/CosyVoice）<br>• *注：音色定制本身使用独立端点 `POST /v1/voice-customization/jobs`* | • 音色定制统一入口：<br>  `POST /v1/voice-customization/jobs`（创建复刻/设计任务）<br>  `GET /v1/voice-customization/jobs/{job_id}`（轮询状态）<br>• *定制音色需在 TTS 请求中通过 `voice_id` 引用* |
| **地域限制** | 全地域支持（除定制热词在新加坡不可用） | • Qwen-Audio-TTS：全地域<br>• CosyVoice 及其 SDK：**仅华北2（北京）**，HTTP 调用也需显式配置 `cn-beijing` 地域 | • 音色定制 API：全地域<br>• 但生成的 `voice_id` 仅在其创建地域的 TTS 服务中有效（如在北京创建的音色，只能在北京调用 TTS 使用） |
| **计费方式** | 按**音频时长（秒）** 计费（如 Qwen-Audio-ASR：0.003 元/秒）；异步任务按实际转写时长计费 | 按**合成音频时长（秒）** 计费（如 Qwen-Audio-TTS：0.005 元/秒）；SSML 解析不额外计费 | • 音色复刻/设计任务：**按次计费**（如复刻 20 元/次，设计 15 元/次）<br>• 后续使用该音色调用 TTS：**仍按音频时长计费**（与普通 TTS 一致） |
| **典型场景** | 会议录音转文字、客服对话分析、视频字幕生成、课堂笔记整理 | 智能播报（天气/新闻）、有声书制作、IVR 语音导航、AI 助手语音回复 | • 企业品牌语音（复刻 CEO 声音做产品介绍）<br>• 虚拟主播（设计“科技感女声”播报财报）<br>• 游戏 NPC（为角色定制方言/情绪化语音） |

---

## 各方案适用场景建议

### ✅ 选择语音识别（ASR）当：
- 你需要将**已有音频内容转化为可编辑、可搜索、可分析的文本**；
- 输入是会议录音、访谈视频、教学音频等**离线批量文件**；
- 对准确率要求高，且需支持专业术语（可通过定制热词提升）；
- 需要实时性反馈（选 `Fun-ASR-Flash` + SSE 流式）或处理超长文件（选 `Filetrans` 异步）。

### ✅ 选择语音合成（TTS）当：
- 你有**确定的文本脚本**，需要将其转化为自然流畅的语音输出；
- 需要快速集成、标准化发音（如客服 IVR、无障碍阅读）；
- 对音色多样性要求不高，使用平台预置音色即可满足；
- 需要精细控制停顿、重音、数学公式朗读（启用 SSML/LaTeX）。

### ✅ 选择音色定制（作为“语音生成”的实际路径）当：
- 你**没有现成文本，但有明确的声音形象需求**（如“复刻销售总监声音讲解产品”）；
- 你需要**超越预置音色的情感表现力、个性特征或语言风格**（如“设计一位带粤语口音的幽默客服”）；
- 业务对品牌一致性要求极高，需**专属、可控、可复用的语音资产**；
- ⚠️ 注意：音色定制是**一次性建模过程**，后续所有语音产出均依赖 TTS 接口调用，**不替代 TTS，而是增强 TTS**。

### ❌ 不建议混淆或误用：
- 将 ASR 用于“生成语音”——它只输出文本，无法发声；
- 将 TTS 用于“识别语音”——它不接收音频输入；
- 将音色定制 API 当作“直接生成语音”的接口——它只生成 `voice_id`，必须配合 TTS 才能产出音频；
- 在非华北2地域调用 CosyVoice SDK 或未配置地域的 HTTP 请求——必然失败。

---

## 开发者技术选型参考指南

| 你的需求 | 推荐方案 | 关键操作提示 |
|----------|-----------|----------------|
| “把一段 2 小时的会议录音转成文字” | `Qwen-Audio-ASR-Filetrans`（异步） | ① 调用 `/api/v1/audio/asr/filetrans` 提交音频 URL；② 轮询 `/api/v1/tasks/{task_id}` 直至 `status=succeeded`；③ 下载结果 JSON |
| “让 App 用标准普通话朗读用户输入的新闻标题” | `Qwen-Audio-TTS`（同步） | ① 构造 `input.text` 为标题文本；② 设置 `format=mp3`, `sample_rate=24000`；③ 直接 POST 到 `/api/v1/audio/speech` 获取音频流 |
| “为客户定制一个专属客服语音，并用于每日播报” | `音色复刻 + Qwen-Audio-TTS` | ① 上传 45 秒高质量客户语音 → `/v1/voice-customization/jobs`；② 轮询获取 `voice_id`；③ 后续所有 TTS 请求中加入 `"voice": {"voice_id": "xxx"}` 参数 |
| “需要低延迟识别用户 10 秒内的语音指令” | `Fun-ASR-Flash`（同步 + SSE） | ① 设置 `X-DashScope-SSE: enable`；② 确保音频 ≥60 秒才启用分片（否则退化为同步）；③ 处理 SSE EventStream 中的 `data:` 分片文本 |
| “生成一段带笑声和停顿的营销话术语音” | `Qwen-Audio-TTS + SSML` | 使用 `<break time="500ms"/>`、`<prosody pitch="high">`、`<say-as interpret-as="interjection">哈哈</say-as>` 等 SSML 标签，`enable_ssml=true` |

> **重要提醒**：  
> - 所有音频类 API 均需严格匹配 **Workspace 所在地域** 配置 SDK 或 HTTP Host（如 `xxx.cn-beijing.maas.aliyuncs.com`）；  
> - API Key 必须与地域一致，跨地域调用将返回 `401 Unauthorized`；  
> - 音频 URL 必须公网可访问（200 OK），不支持私有 COS 签名直传；  
> - 流式（SSE）与异步模式不可混用，需根据模型文档明确支持类型；  
> - 首次使用音色定制前，请务必阅读 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 和 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 的完整参数说明与示例。  

---  
*本文档依据百炼平台 2024 年 Q3 版本 API 规范编写，模型能力与计费策略可能随版本更新调整，请以控制台最新文档为准。*

## 被对比主题页

- [audio api directory](../api/audio-api-directory.md)
- [voice customization api directory](../api/voice-customization-api-directory.md)


