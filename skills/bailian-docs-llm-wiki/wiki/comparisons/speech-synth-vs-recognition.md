# 语音合成与语音识别对比

本页面旨在为开发者提供语音合成（TTS）与语音识别（ASR）两大核心音频能力的系统性对比，帮助在百炼平台（Model Studio）中快速完成技术选型。二者虽同属“语音理解与生成”技术栈，但在任务目标、数据流向、模型设计、调用范式及计费逻辑上存在本质差异。本文基于百炼平台当前（v3.1+）非实时音频 API 目录（`audio api directory`）与语音定制化能力（`voice customization api directory`）进行客观梳理，不涉及实时流式能力（如 `Realtime ASR/TTS`），亦不覆盖第三方模型或私有部署场景。

---

## 关键维度对比表

| 维度 | 语音识别（ASR） | 语音合成（TTS） |
|------|----------------|----------------|
| **核心任务** | 将输入的**语音信号**转换为**结构化文本**（含标点、段落、说话人分离等可选能力） | 将输入的**结构化文本**（支持 SSML/LaTeX）转换为**高质量语音波形**（含音色、语速、情感、韵律控制） |
| **典型输入格式** | • 同步：`input_audio` 字段（Base64 编码或 multipart/form-data 上传）<br>• 异步：`file_urls` 数组（公网可访问的音频 URL，如 OSS/HTTPS）<br>• 支持格式：`mp3`, `wav`, `m4a`, `flac`, `opus`（采样率 ≥8kHz） | • `text` 字段（纯文本或 SSML/LaTeX 标记文本）<br>• 可选：`voice`（音色 ID）、`format`（`mp3`/`wav`/`opus`）、`sample_rate`（16000/22050/48000 Hz）、`speed`/`pitch` 等韵律参数 |
| **典型输出格式** | • 同步：JSON 响应体含 `text`、`segments`（时间戳分段）、`speaker_labels`（多说话人）等<br>• 异步：返回 `transcription_url`（24 小时有效直链），内容为标准 JSON 或 SRT/VTT 字幕文件 | • 同步/异步均返回 `audio_info.url`（24 小时有效直链）<br>• 音频二进制流（同步调用时可直接响应）<br>• 支持 `X-DashScope-SSE: enable` 流式返回音频 chunk（部分模型） |
| **主流支持模型** | • `Qwen-Audio-ASR`（中短音频，支持 SSE 流式）<br>• `Qwen-Audio-ASR-Filetrans`（长音频异步专用）<br>• `Fun-ASR` / `Fun-ASR-Flash`（轻量高性价比）<br>• `Paraformer`（高精度开源，支持音轨选择、语气词过滤） | • `Qwen-Audio-TTS`（通用强鲁棒性，SSML 全支持）<br>• `CosyVoice-v3/v3.5`（自然度与情感表达领先，含 `plus`/`flash` 版本）<br>• 所有模型均兼容**语音定制化音色**（通过 `voice_id` 调用） |
| **API 主要端点** | • 同步：`POST /multimodal-generation/generation`（需 `model` + `input.messages[].input_audio`）<br>• 异步：`POST /transcription`（需 `X-DashScope-Async: enable`） | • 同步：`POST /multimodal-generation/generation`（需 `model` + `input.text` + `input.voice`）<br>• 异步：`POST /speech-synthesis`（统一异步路径，无需额外 header） |
| **计费方式** | • 按**音频时长（秒）** 计费<br>• 不同模型单价不同（如 `Fun-ASR-Flash` < `Paraformer` < `Qwen-Audio-ASR`）<br>• 异步任务按实际处理时长计费（非提交时长） | • 按**生成音频时长（秒）** 计费<br>• 音色定制化本身**不单独计费**，但使用定制音色的 TTS 请求按对应模型单价计费<br>• `CosyVoice-v3.5-plus` 等高保真模型单价高于基础 `Qwen-Audio-TTS` |
| **定制化能力集成** | • 支持**定制热词**（独立接口管理，提升领域专有名词识别率）<br>• **不支持音色定制**（ASR 无“音色”概念） | • **深度集成语音定制化**：<br> – 音色复刻（3–30 秒参考音频）<br> – 音色设计（文本描述生成新音色）<br>• 定制音色 ID 可直接作为 `input.voice` 参数传入任意 TTS 模型调用 |
| **典型延迟特征** | • 同步：≤10 分钟音频，端到端响应通常 < 3× 实时时长（如 5 分钟音频约 15 秒内返回）<br>• 异步：长音频（>30 分钟）任务排队+处理，平均耗时 1–5 分钟 | • 同步：文本长度主导延迟，短文本（<100 字）通常 < 2 秒；长文本支持流式生成<br>• 异步：任务创建后立即返回 `task_id`，结果生成时间与文本长度正相关（平均 1–3 秒/百字） |

---

## 适用场景建议

### ✅ 推荐优先选用语音识别（ASR）的场景：
- **会议纪要自动化**：录制会议音频 → 转写为带时间戳与发言人标记的文本 → 提取关键结论  
- **客服录音质检**：批量导入历史通话录音 → 识别服务话术合规性、客户情绪关键词、未覆盖 FAQ  
- **教育内容加工**：教师授课视频音频 → 生成双语字幕、知识点时间锚点、自动生成学习笔记  
- **无障碍辅助**：为听障用户提供实时字幕（注：此为*非实时*能力，适用于预录制视频字幕生成）  

> ⚠️ 注意：若需**毫秒级低延迟转写**（如直播字幕、实时会议翻译），请切换至 [Realtime ASR](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)，而非本目录模型。

### ✅ 推荐优先选用语音合成（TTS）的场景：
- **智能播报系统**：将新闻摘要、天气预报、订单状态等文本 → 合成为自然语音，推送至 IVR 或智能音箱  
- **有声内容生产**：小说/教材/知识库文本 → 批量生成高拟真有声书（支持多音色、章节停顿、情感强调）  
- **个性化语音交互**：结合语音定制化，为品牌打造专属 AI 声音（如银行客服音色、儿童教育音色）  
- **多语言本地化**：同一套产品文案 → 调用不同语种 TTS 模型（如 `zh`, `en`, `ja`, `ko`）生成本地化语音包  

> ⚠️ 注意：若需**实时驱动虚拟人唇形同步**或**超低延迟语音反馈**（<300ms），请评估 [Realtime TTS](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md) 或 `Qwen-Audio-Realtime` 模型。

---

## 开发者技术选型参考指南

| 选型维度 | 决策建议 | 依据说明 |
|----------|----------|----------|
| **首次接入，追求快速验证** | 优先尝试 `Qwen-Audio-ASR`（同步） + `Qwen-Audio-TTS`（同步） | 二者文档最完善、SDK 封装最成熟、错误提示最友好；支持完整调试流程（上传→调用→查看响应→下载音频） |
| **处理长音频（>30 分钟）且并发量高** | ASR 选 `Qwen-Audio-ASR-Filetrans` 或 `Paraformer`（异步）<br>TTS 一律使用异步模式（`/speech-synthesis`） | 避免同步请求超时；异步任务天然支持重试、轮询、失败告警；适合后台批处理作业 |
| **对识别准确率要求极高（如法律/医疗录音）** | ASR 必选 `Paraformer` + **定制热词**（提前注入专业术语）<br>禁用 `Fun-ASR-Flash` 等轻量模型 | `Paraformer` 在长时静音、多人交叉对话、专业词汇场景下 F1 值显著领先；热词可提升关键实体召回率 15%+ |
| **需要品牌专属声音** | TTS 必接 `voice customization api directory`：<br>• 有高质量录音 → 用**音色复刻**<br>• 无录音但需快速原型 → 用**音色设计**（文本描述生成） | 定制音色 ID 可无缝注入任一 TTS 模型调用，无需修改业务逻辑；`CosyVoice-v3.5-plus` 对定制音色还原度最高 |
| **成本敏感型项目（如海量客服质检）** | ASR 选用 `Fun-ASR` 系列（单价最低）<br>TTS 选用 `Qwen-Audio-TTS` 基础版（非 `CosyVoice-plus`） | `Fun-ASR` 在通用场景下 WER（词错误率）仅比 `Qwen-Audio-ASR` 高 2–3%，但成本可降低 40%+；适合对绝对精度容忍度较高的批量场景 |
| **需与现有系统深度集成（如 Java 微服务）** | 优先使用官方 **Java SDK**，调用 `client.audio.asr.jobs.create()` / `client.audio.tts.jobs.create()` 封装方法 | SDK 自动处理异步轮询、重试、鉴权、域名替换（`{WorkspaceId}`）、异常分类（如 `InvalidAudioFormatError`），大幅降低集成复杂度 |

> 💡 **终极建议**：在正式上线前，务必使用**相同测试集**（10–20 条典型音频/文本）横向对比至少 2 个候选模型的输出质量、延迟与费用，以数据驱动决策。百炼平台控制台提供「API 调用分析」看板，可直观对比各模型的 P95 延迟、成功率与单日消耗。

---  
*最后更新：2024年6月 | 百炼平台 v3.1.2 文档版本*

## 被对比主题页

- [audio api directory](../api/audio-api-directory.md)
- [voice customization api directory](../api/voice-customization-api-directory.md)


