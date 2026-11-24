# 音频生成、语音合成与语音识别能力对比

本 Wiki 页面旨在帮助开发者清晰区分百炼平台中三类核心音频处理能力——**音频生成（Text-to-Audio）**、**语音合成（TTS）** 和 **语音识别（ASR）** 的技术定位、能力边界与适用场景。尽管三者均作用于音频信号，但在任务目标、输入输出范式、模型架构、实时性要求及计费逻辑上存在本质差异。本文基于当前（2024年Q3）正式发布的非实时音视频 API 目录与音色定制能力文档，提供结构化对比与选型建议，避免因概念混淆导致接口误用或架构设计偏差。

---

## 关键维度对比

| 维度 | 音频生成（Audio Generation） | 语音合成（Speech Synthesis, TTS） | 语音识别（Speech Recognition, ASR） |
|------|-----------------------------|-----------------------------------|-------------------------------------|
| **核心任务** | 根据文本/提示词生成全新音频（含人声、环境音、音乐等），支持风格迁移 | 将结构化文本转换为自然、可控的人声语音（无背景音） | 将原始语音音频转录为可编辑文本，并支持时间戳分段 |
| **典型输入格式** | `prompt`（描述性文本，如“清晨鸟鸣与咖啡馆轻音乐”）、可选参考音频（用于风格迁移） | `text`（纯文本，支持SSML标签）、`speaker`（音色ID）、语速/情感/停顿等控制参数 | `audio_url` 或 `file`（WAV/MP3/FLAC/M4A）、`language`（可选，如 `"zh"`、`"en"`）、`response_format`（`json`/`srt`） |
| **典型输出格式** | `audio_url`（生成音频的临时下载链接，格式为 WAV/MP3）、`duration`、`prompt_used` | `audio_url`（合成语音的临时下载链接，格式为 WAV/MP3/PCM）、`segments`（若启用分段）、`text`（原文回显） | `text`（完整转录文本）、`segments`（含 start/end 时间戳与子句文本）、`language_detected`（自动识别语种） |
| **支持模型（示例）** | `qwen-audio-gen-v1`, `qwen-audio-gen-music-v2` | `qwen-tts-zh-01`, `cosyvoice-v3.5-plus`, `qwen-audio-3.1-tts-plus` | `qwen-audio-asr-zh`, `qwen-audio-asr-en`, `qwen-audio-asr-multilingual` |
| **API 端点** | `POST /api/v1/audio/generation` | `POST /api/v1/audio/tts` | `POST /api/v1/audio/asr` |
| **是否支持音色定制** | ❌ 不直接支持；但可通过风格迁移复用已定制音色的参考音频（需配合音色复刻流程） | ✅ 完全支持：可传入 `speaker`（音色ID）调用已创建的复刻/设计音色（见 [Voice Customization](api/voice-customization-api-directory.md)） | ❌ 不适用；ASR 仅建模语音→文本映射，不涉及音色建模 |
| **计费方式** | 按**请求次数 + 生成时长**计费（例：1次请求生成30秒音频 ≈ 1单位）；免费额度按千次请求折算 | 按**合成语音时长（秒）** 计费（例：生成1分钟语音 ≈ 60秒 × 单价）；支持按音色类型差异化定价 | 按**输入音频时长（秒）** 计费（例：上传2分钟音频 ≈ 120秒 × 单价）；多语种/高噪模式不额外加价 |
| **单次处理上限** | ≤ 5 分钟音频（生成结果时长） | ≤ 30 分钟（合成文本对应语音时长） | ≤ 30 分钟（输入音频时长） |
| **异步支持** | ✅ 异步返回（响应含 `job_id`，需轮询 `/jobs/{id}` 获取结果） | ✅ 异步返回（大文本或高保真合成时默认异步） | ✅ 异步返回（所有请求均异步，响应含 `job_id`） |
| **典型延迟（P95）** | 8–25 秒（取决于 prompt 复杂度与生成长度） | 3–12 秒（同步模式下≤3秒；异步模式同 ASR） | 4–15 秒（取决于音频质量与语种） |
| **是否支持[流式输出](../concepts/streaming-output.md)** | ❌ 否（非实时批处理） | ⚠️ 仅 `qwen-audio-realtime` 模型支持流式（属独立实时 API，**不在此 audio-api-directory 范围内**） | ❌ 否（非实时批处理；实时流式 ASR 属未来规划能力） |

> **注**：  
> - 所有接口均需 `Authorization: Bearer <API_KEY>` 鉴权，`Content-Type` 根据载荷类型选择 `application/json`（纯文本）或 `multipart/form-data`（含文件）。  
> - “音色定制”能力（音色复刻/设计）本身**不构成独立音频处理服务**，而是为 TTS 提供音色供给层，其 API（`/api/v1/services/audio/tts/customization`）与 TTS 接口解耦，需先创建音色再在 TTS 请求中引用 `speaker`。  
> - 音频打标（Audio Captioning）与音视频翻译（A/V Translation）虽同属 `audio-api-directory`，但因任务目标不同（生成结构化标签 / 双语语义翻译），未纳入本表对比，详见对应文档。

---

## 各方案适用场景建议

| 场景需求 | 推荐能力 | 关键理由 | 注意事项 |
|----------|-----------|-----------|-----------|
| **为短视频/播客生成背景音乐+环境音效** | ✅ 音频生成 | 原生支持文生音、风格迁移，可脱离人声生成纯音频内容 | 不适合生成精准对齐台词的配音；需人工校验音效合理性 |
| **将客服话术、知识库文章批量转为语音播报** | ✅ 语音合成（TTS） | 支持多音色、语速/情感控制、SSML精细排版，输出语音自然度高、时长可控 | 若需专属品牌音色，须提前通过 [Voice Customization](api/voice-customization-api-directory.md) 创建并绑定 `speaker` |
| **将会议录音、访谈音频转为可搜索、可编辑的文字稿** | ✅ 语音识别（ASR） | 多语种、抗噪能力强，支持 SRT 字幕导出，满足合规存档与内容分析需求 | 输入音频需保证基础信噪比；方言/专业术语建议搭配自定义热词提升准确率 |
| **需要“克隆某位专家声音”并用于课程讲解** | ✅ TTS + 音色复刻组合 | 先用音色复刻 API 创建专属音色，再在 TTS 请求中指定该 `speaker` | 复刻需高质量参考音频（10–30秒安静人声）；审核通过后方可使用（状态 `OK`） |
| **根据用户文字描述（如“温柔女声读诗”）即时生成试听样音** | ✅ 音色设计 + TTS 组合 | 无需采集真人录音，通过 `voice_prompt` + `preview_text` 快速生成预览音频 | 当前仅 CosyVoice 及部分 Qwen-TTS 模型支持；不适用于 Realtime 系列 |
| **实时直播字幕或在线语音助手交互** | ❌ 三者均不适用 | 当前 `audio-api-directory` 下所有能力均为**非实时批处理**，不支持低延迟流式 I/O | 请关注平台后续发布的 `realtime-asr` / `realtime-tts` 专项 API（不在本文档覆盖范围） |

---

## 面向开发者的选型参考

### ✅ 优先选择音频生成（Audio Generation）当：
- 输入是**创意性描述文本**（非脚本台词），目标是生成**非语音类音频**（BGM、音效、氛围声）；
- 需要将一段现有音频（如老电影片段）**迁移至新风格**（如“黑白片转赛博朋克风”）；
- 接受 5–30 秒级处理延迟，且无需精确时间对齐。

### ✅ 优先选择语音合成（TTS）当：
- 输入是**确定性文本脚本**，需输出**高自然度、高可控性的人声语音**；
- 要求支持**品牌音色复刻**、**多角色对话**、**语速/重音/停顿精细化调节**；
- 需与 ASR 结果联动（如：ASR 输出文本 → TTS 生成带情感反馈的语音回复）。

### ✅ 优先选择语音识别（ASR）当：
- 输入是**原始语音文件**（录音、会议、采访），目标是获取**结构化文本结果**；
- 需要**时间戳分段**（用于字幕、重点摘要、说话人分离）；
- 处理场景含**中英文混杂、专业领域术语、一定背景噪音**。

### ⚠️ 避免误用的关键红线：
- **勿用 TTS 替代音频生成**：TTS 无法生成无语音的纯环境音/音乐；强行输入非文本 prompt（如“雨声”）将导致不可预测输出或报错。  
- **勿用 ASR 实现“语音克隆”**：ASR 仅提取文本信息，不保留声纹特征；音色复刻必须通过 `voice-customization-api-directory` 完成。  
- **勿将 `qwen3-livetranslate-flash` 当作实时 API**：其名称含 “live” 易引发误解，实为**非实时批处理**，与本表三项能力同属离线架构。  

如需进一步集成指导，请查阅：  
- [音频生成 API 参考](raw/model-api-reference/audio-api-directory/audio-generation-api.md)  
- [语音合成 API 参考](raw/model-api-reference/audio-api-directory/speech-synthesis-api-reference.md)  
- [语音识别 API 参考](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference.md)  
- [音色定制全流程指南](api/voice-customization-api-directory.md)

## 被对比主题页

- [audio api directory](../api/audio-api-directory.md)
- [voice customization api directory](../api/voice-customization-api-directory.md)


