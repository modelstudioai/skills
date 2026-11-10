# 音频生成、语音合成与语音识别对比

本页旨在为开发者提供清晰、可落地的技术选型参考，系统性对比百炼平台中三类核心音频AI能力：**音频生成（Audio Generation）**、**语音合成（Text-to-Speech, TTS）** 与 **语音识别（Automatic Speech Recognition, ASR）**。三者虽同属“音频智能处理”范畴，但在任务目标、技术原理、输入输出范式、模型架构及工程集成方式上存在本质差异。正确区分其边界与适用场景，是构建高可用语音应用（如智能客服、会议纪要、有声内容生产、实时交互系统）的前提。

以下对比基于百炼平台当前（2024年Q3）正式发布的非实时音频API能力体系，覆盖模型支持、调用路径、计费逻辑与典型实践约束，不包含实时流式（Realtime API）子集，相关能力请参见 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)。

## 关键维度对比

| 维度 | 音频生成（Audio Generation） | 语音合成（TTS） | 语音识别（ASR） |
|------|-----------------------------|------------------|------------------|
| **核心任务定义** | 根据文本、音效描述或参考音频，**从零生成全新音频内容**（含人声、背景音、音乐、环境声等），支持多音色混音、风格控制、时长可控等高级创作能力 | 将**结构化文本（纯文本/SSML/LaTeX）转换为自然语音波形**，聚焦发音准确性、韵律自然度与音色表现力，不生成语义无关声音 | 将**原始语音信号（音频文件或流）转换为对应文字转录结果**，核心目标是高准确率、低延迟、强鲁棒性（抗噪/口音/术语） |
| **典型输入格式** | • 文本提示（prompt），如 `"一位温暖女声朗读科普文章，背景轻柔钢琴伴奏"`<br>• 可选：参考音频（用于音色/风格锚定）、起始音频（inpainting）、BPM/时长约束<br>• 支持 `file_urls`（公网URL）或 Base64 内联 | • `text` 字段：纯文本、SSML（需 `enable_ssml=true`）、LaTeX 数学公式<br>• 必填参数：`voice`（音色ID）、`format`（`mp3`/`wav`/`opus`）、`sample_rate`<br>• 可选：`voice_prompt`（音色设计）、`speed`、`pitch` 等韵律控制 | • `file_urls`（数组，支持多个音频URL）<br>• 或 Base64 Data URI（`data:audio/wav;base64,...`）<br>• 可选：`custom_vocabulary`（定制热词）、`input_text`（上下文增强）、`language`（自动检测或显式指定） |
| **典型输出格式** | • 生成的完整音频文件（`mp3`/`wav`/`ogg`）<br>• 元数据：时长、采样率、声道数、生成置信度（部分模型）<br>• 异步模式返回 `task_id`，轮询获取结果 | • 音频二进制流（同步/流式）或 Base64 编码字符串<br>• HTTP 响应头含 `Content-Type: audio/mpeg` 等<br>• 流式响应（SSE）按 chunk 返回音频片段 | • 同步：JSON 结构化结果，含 `text`（主转录）、`segments`（时间戳分段）、`words`（词级对齐）<br>• 异步：`GET /api/v1/tasks/{task_id}` 返回完整 JSON，含 `status`、`result`、`error` 字段<br>• 支持 SRT/VTT 字幕导出（部分模型） |
| **主力支持模型** | • `qwen-audio-gen-v3`（通用高质量生成）<br>• `qwen-audio-gen-music`（音乐生成专用）<br>• `cosyvoice-gen-plus`（带音色控制的语音生成）<br>• *注：音频生成暂未开放音色复刻直连能力，需先通过 [Voice Customization API](api/voice-customization-api-directory.md) 创建音色后，在 prompt 中引用* | • `qwen-audio-tts`（通用高自然度）<br>• `cosyvoice-v3.5-plus`（情感丰富，支持数学公式）<br>• `cosyvoice-v3.5-flash`（低延迟，适合播报）<br>• 支持复刻音色（`voice_id`）与设计音色（`voice_prompt`） | • `qwen-audio-3.1-asr-flash`（短音频实时同步，<2min）<br>• `qwen-audio-3.1-asr-flash-filetrans`（长音频异步，>5min，推荐）<br>• `fun-asr-flash`（轻量快速）<br>• `paraformer-v2`（开源兼容性强） |
| **标准 API 端点** | `POST /api/v1/services/aigc/audio-generation/generation`（同步）<br>`POST /api/v1/services/audio/generation/jobs/create`（异步） | `POST /api/v1/services/audio/tts/http/synthesize`（同步）<br>`POST /api/v1/services/audio/tts/stream/synthesize`（流式）<br>`POST /api/v1/services/audio/tts/jobs/create`（异步批量） | `POST /api/v1/services/audio/asr/transcription`（同步）<br>`POST /api/v1/services/audio/asr/jobs/create`（异步）<br>`POST /api/v1/services/aigc/multimodal-generation/generation`（`qwen-audio-asr-flash` 同步专用） |
| **计费方式** | • 按**生成时长（秒）计费**（如：1秒音频 = 1单位）<br>• 不同模型单价不同（`gen-music` > `gen-v3` > `cosyvoice-gen`）<br>• 音色复刻创建本身免费，但调用时计入目标 TTS/Gen 模型用量 | • 按**合成时长（秒）计费**<br>• `qwen-audio-tts` 与 `cosyvoice` 系列独立计价<br>• 复刻/设计音色无额外费用，仅按合成时长计费<br>• SSML/LaTeX 解析不额外计费 | • 按**识别时长（秒）计费**<br>• `flash` 类模型单价低于 `filetrans` 类（因计算复杂度差异）<br>• 定制热词、上下文增强功能**不额外计费**<br>• [异步任务](../concepts/asynchronous-task.md)提交本身不计费，仅结果处理计费 |
| **典型场景** | • 制作播客开场/片尾音效<br>• 为短视频自动生成配乐+旁白混合音频<br>• 游戏NPC动态语音+环境音合成<br>• 教育课件中公式语音+动画音效联动生成 | • 智能硬件语音播报（天气、新闻）<br>• 电子书/文档无障碍朗读<br>• 客服IVR语音导航<br>• 多语言学习APP单词跟读反馈<br>• 数学/化学公式精准语音输出 | • 会议录音自动转写与摘要<br>• 客服通话质检与话术分析<br>• 视频字幕自动生成（SRT/VTT）<br>• 法庭庭审记录数字化<br>• 医疗问诊语音电子病历录入 |

## 各方案适用场景建议

### ✅ 推荐选择「音频生成」当：
- 你需要**创造全新的、非文本直接映射的音频内容**，例如：“生成一段30秒的中国风古筝BGM，节奏舒缓，用于冥想App背景”；
- 要求**多元素融合**（人声+音乐+音效），且各元素需协同控制（如人声语速匹配BPM）；
- 场景强调**创意性、风格化与不可预测性**，而非严格保真于输入文本；
- *不适用*：仅需将固定文案转成语音（此时TTS更高效精准）；需要高精度语音对齐（如唇形同步）。

### ✅ 推荐选择「语音合成（TTS）」当：
- 输入是**确定、结构化的文本**（含SSML标签或LaTeX公式），目标是**稳定、可复现、高保真地输出语音**；
- 对**发音准确性、专业术语读音、多音字处理、数学符号朗读规范性**有硬性要求（如金融报告、医学教材）；
- 需要**毫秒级可控的语速/停顿/重音**，或支持**多音色AB测试、A/B语音分流**；
- *不适用*：输入为模糊描述（如“听起来很兴奋”）；需生成非语音成分（如雷声、键盘声）。

### ✅ 推荐选择「语音识别（ASR）」当：
- 输入是**真实世界采集的语音信号**（录音文件、电话音频、会议录像音频），目标是**提取其中蕴含的文字信息**；
- 对**领域适配性、抗噪能力、方言/口音鲁棒性、长上下文理解**有高要求（如医疗会诊、法庭辩论）；
- 需要**精确时间戳对齐**（用于视频字幕、语音编辑、关键词定位）；
- *不适用*：输入是文本（应选TTS）；需生成语音（应选TTS或Audio Generation）；需实时流式交互（应选 Realtime API）。

## 开发者技术选型参考指南

| 选型考量点 | 音频生成 | 语音合成（TTS） | 语音识别（ASR） |
|------------|-----------|------------------|------------------|
| **首次集成复杂度** | ⚠️ 中高：需理解 prompt 工程、音频约束参数（时长/BPM）、结果异步轮询机制；音色复刻需额外调用 Voice Customization API | ✅ 低：HTTP POST + `text` + `voice` 即可快速出声；SDK 封装成熟（Python/Java） | ⚠️ 中：需区分同步（短音频）与异步（长音频）路径；`filetrans` 类必须轮询；定制热词需预注册 |
| **延迟敏感性** | ❌ 不适用实时场景：生成耗时长（秒级），无法满足 <500ms 响应要求 | ✅ 支持流式（SSE）与低延迟模型（`cosyvoice-flash`），端到端 <800ms 可达 | ✅ `flash` 系列支持同步低延迟（<300ms），`filetrans` 仅适用于离线批量 |
| **定制化能力** | • 高阶：Prompt 控制风格/情绪/乐器<br>• 中阶：通过复刻音色实现人声定制<br>• 低阶：无传统“热词”概念 | • 高阶：音色复刻（克隆真人声线）、音色设计（文本生成新声线）<br>• 中阶：SSML 控制停顿/语调/音量<br>• 低阶：无领域术语强化机制 | • 高阶：定制热词（提升专业词汇识别率）<br>• 中阶：上下文增强（`input_text` 提升对话连贯性）<br>• 低阶：无音色控制能力 |
| **地域与SDK限制** | • 所有模型均支持华北2（北京）、新加坡地域<br>• Python/Java SDK 全面支持 | • `qwen-audio-tts` / `cosyvoice` Java/Python SDK **仅限华北2（北京）**<br>• 移动端 SDK（Android/iOS/HarmonyOS）全地域支持 | • `qwen-audio-asr-flash` 同步接口全地域支持<br>• `fun-asr` / `paraformer` 异步接口在新加坡地域需确认模型可用性<br>• 移动端 SDK 对 `paraformer` 使用旧域名（注意迁移） |
| **错误排查重点** | • Prompt 描述模糊导致生成偏离预期<br>• 音频格式/时长超限（如参考音频>30s）<br>• `target_model` 与后续合成模型不一致（音色复刻场景） | • `voice_id` 未部署成功（状态非 `OK`）<br>• `sample_rate` 与 `format` 不兼容（如 `opus` + `48000`）<br>• SSML 语法错误导致静音 | • 音频采样率/位深不支持（推荐 16bit PCM WAV）<br>• `custom_vocabulary` 未在对应 Workspace 生效<br>• [异步任务](../concepts/asynchronous-task.md)未轮询或超时（有效期24h） |

> **重要提醒**：  
> - 所有音频类API均**强制使用业务空间专属域名**（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.ali

## 被对比主题页

- [audio api directory](../api/audio-api-directory.md)
- [voice customization api directory](../api/voice-customization-api-directory.md)


