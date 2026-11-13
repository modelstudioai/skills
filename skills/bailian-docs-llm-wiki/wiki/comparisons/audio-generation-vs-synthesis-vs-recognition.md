# 语音生成、语音合成与语音识别对比

本页面旨在为开发者提供清晰、准确的技术选型参考，系统性对比百炼平台中三类核心音频处理能力：**语音生成（Audio Generation）**、**语音合成（Text-to-Speech, TTS）** 和 **语音识别（Automatic Speech Recognition, ASR）**。三者虽同属“语音AI”范畴，但在任务目标、技术原理、输入输出范式、模型架构及适用场景上存在本质差异。本文基于当前非实时音频 API（`api/audio-api-directory.md`）与音色定制 API（`api/voice-customization-api-directory.md`）的最新能力定义，结合实际调用约束与工程实践，进行结构化对比分析。

---

## 关键维度对比

| 维度 | 语音生成（Audio Generation） | 语音合成（TTS） | 语音识别（ASR） |
|------|------------------------------|------------------|------------------|
| **核心任务** | 从零生成具有语义或风格意图的原始音频（如音乐、音效、带情感的拟声、多说话人对话片段等），**不依赖文本输入**或仅以提示词（prompt）驱动 | 将**结构化文本（含SSML/LaTeX）转换为自然语音波形**，强调发音准确性、韵律自然性与音色可控性 | 将**原始语音信号（音频文件或流）转换为对应文本内容**，强调转写准确率、抗噪鲁棒性与上下文理解能力 |
| **典型输入格式** | - `prompt`: 描述性文本（如“欢快的8-bit电子游戏背景音乐，BPM=120”）<br>- `reference_audio`（可选）：用于风格迁移或音色锚定的参考音频（Base64或URL）<br>- `duration`, `bpm`, `instrument` 等控制参数（依模型而定） | - `text`: 待合成文本（支持中文/英文/混合，含SSML标签）<br>- `voice`: 音色ID（预置音色或通过`voice-enrollment`定制）<br>- `format`, `sample_rate`, `speed`, `pitch` 等音频参数 | - `file_urls`: 公网可访问音频URL数组（推荐）<br>- `audio`: Base64编码的原始音频数据<br>- `messages`（仅`Qwen-Audio-ASR`）：上下文对话历史（`user`/`assistant`轮次）用于增强识别一致性 |
| **典型输出格式** | - 同步：返回音频二进制数据或直连下载URL（`mp3`/`wav`/`opus`）<br>- 异步：返回`task_id`，轮询获取结果对象（含音频URL、元信息、时序标注） | - 同步/流式：SSE分片返回音频chunk（`X-DashScope-SSE: enable`）<br>- 同步/非流式：返回完整音频二进制或URL<br>- 输出格式由`format`参数指定（`mp3`, `wav`, `opus`, `flac`） | - 同步：返回JSON结构化结果（含`text`, `segments`, `words`等字段）<br>- 异步（Filetrans/Paraformer）：返回`task_id`，轮询获取含逐句/逐词时间戳的完整转写结果<br>- 流式（`Qwen-Audio-ASR`）：SSE返回中间识别结果（`partial`/`final`类型） |
| **平台支持模型** | - `Qwen-Audio-Gen`（通用音频生成）<br>- `Qwen-Music-Gen`（专业音乐生成）<br>- `CosyVoice-AudioGen`（音效/配音生成）<br>（注：具体模型列表见 [音频生成API参考](raw/model-api-reference/audio-api-directory/audio-generation-api.md)） | - `Qwen-Audio-TTS`（高保真、支持上下文）<br>- `CosyVoice`（含`v3.5-plus`等多版本，支持声音复刻/设计）<br>- 所有TTS模型均兼容`voice-enrollment`定制音色 | - `Qwen-Audio-ASR`（上下文增强，支持流式）<br>- `Qwen-Audio-ASR-Filetrans`（长文件异步专用）<br>- `Fun-ASR` / `Fun-ASR-Flash`（轻量高效）<br>- `Paraformer`（开源强鲁棒性）<br>- `Qwen-ASR`（需注意：仅音频专用变体有效，通用`qwen-3`不支持ASR） |
| **API 端点（非实时）** | `/audio/generation`（同步）<br>`/audio/generation/jobs`（异步） | `/audio/tts/http`（同步/流式）<br>`/audio/tts/jobs`（异步批量） | `/audio/asr/transcription`（异步，Filetrans/Paraformer）<br>`/multimodal-generation/generation`（同步/流式，`Qwen-Audio-ASR`） |
| **计费方式** | 按**生成时长（秒）+ 模型复杂度**计费；音乐生成单价高于普通音效生成；[异步任务](../concepts/asynchronous-task.md)按最终输出音频时长结算 | 按**合成文本字数（中文字符/英文token）或输出音频时长（秒）** 计费；CosyVoice高级音色、复刻音色调用额外计费；流式与非流式同价 | 按**输入音频时长（秒）** 计费；`Qwen-Audio-ASR`流式调用按实际传输音频时长计费；[异步任务](../concepts/asynchronous-task.md)（Filetrans）按提交音频总时长计费；上下文增强不额外计费 |
| **调用模式支持** | 同步（短生成）、异步（长音频/高保真） | 同步、流式（SSE）、异步（批量） | 同步（短音频）、流式（`Qwen-Audio-ASR` ≥1分钟）、异步（长文件/批量） |
| **音色定制集成** | ✅ 支持通过`voice-enrollment`定制音色作为生成参考（如“用张三的声音说‘欢迎光临’并配轻快钢琴伴奏”） | ✅ 深度集成：所有TTS模型均可直接使用`voice-enrollment`创建的音色ID（`{model}-{prefix}-{id}`） | ❌ 不适用：ASR是理解语音，不涉及音色输出 |

---

## 各方案适用场景建议

### ✅ 语音生成（Audio Generation）
- **适用场景**：  
  - 创意内容生产：AI作曲、短视频BGM生成、游戏音效库扩充、播客片头/转场音频定制  
  - 多模态应用：为图文/视频自动生成匹配音效（如“雷雨声”、“人群欢呼”）  
  - 无障碍辅助：为无语音能力用户生成个性化提示音、情绪化反馈音  
- **慎用场景**：  
  - 对文本精确性要求极高的配音（应优先选TTS）  
  - 实时交互场景（当前为非实时API，延迟不可控）  
  - 需严格对齐时间轴的影视配音（缺乏精细时序控制接口）

### ✅ 语音合成（TTS）
- **适用场景**：  
  - 有声内容自动化：电子书朗读、新闻播报、客服IVR语音、课件配音  
  - 品牌语音资产建设：定制企业专属音色（客服声、品牌代言人声）  
  - 个性化交互：智能硬件（音箱、车载）的拟人化应答  
- **慎用场景**：  
  - 需要生成非语言声音（如笑声、咳嗽、环境音）——应选**语音生成**  
  - 超长文本（>10万字）一次性合成——建议分段调用或使用异步批量接口  

### ✅ 语音识别（ASR）
- **适用场景**：  
  - 会议纪要自动化：录制音频→转文字→摘要提炼  
  - 教育/医疗场景：课堂录音转写、问诊记录数字化  
  - 内容审核：对UGC语音内容进行敏感词检测与合规审查  
- **慎用场景**：  
  - 实时字幕/同传（需低延迟）——应选用[Realtime API](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md)  
  - 强噪音/远场/多人重叠语音（需前端降噪或专用模型）——优先测试`Fun-ASR-Flash`或`Qwen-Audio-ASR`上下文模式  

---

## 开发者技术选型参考指南

| 你的需求 | 推荐方案 | 关键依据 | 注意事项 |
|----------|-----------|-----------|-----------|
| “我要把一篇公众号文章变成播客音频” | ✅ **TTS**（`CosyVoice-v3.5-plus` + 定制音色） | 文本明确、需高自然度与品牌一致性；支持SSML控制停顿/重音 | 使用`format=mp3`兼顾体积与音质；启用`enable_preprocess=true`提升合成稳定性 |
| “客户上传了一段1小时会议录音，需要完整文字稿” | ✅ **ASR**（`Qwen-Audio-ASR-Filetrans` 或 `Paraformer`） | 长音频、离线处理、需高准确率与分段时间戳 | 必须用异步接口；建议拆分为30分钟以内分段提交以提升成功率；开启`language_hints=["zh"]` |
| “为APP生成一段‘支付成功’提示音，带金币掉落音效和温暖女声旁白” | ✅ **语音生成**（`Qwen-Audio-Gen`） + **TTS**（组合调用） | 需融合语音与非语音元素；纯TTS无法生成音效 | 先用TTS生成旁白，再用语音生成生成音效，最后用FFmpeg混音；或尝试`CosyVoice-AudioGen`单次生成复合音频 |
| “想让AI用我本人的声音朗读任意文本” | ✅ **TTS**（`CosyVoice`） + **音色复刻**（`voice-enrollment`） | 核心诉求是“我的声音”，本质是TTS音色定制 | 参考音频需≥10秒安静环境录音；复刻后音色ID格式为`cosyvoice-v3.5-plus-{prefix}-{id}`，直接传入TTS `voice`参数 |
| “需要实时监听客服通话并显示字幕” | ❌ 本页所有方案均不适用 → ✅ **Realtime API** | 非实时API平均延迟>2s，无法满足实时性 | 查阅 [Realtime API 概述](raw/model-api-reference/realtime-api-directory/realtime-api-overview.md) 并选用`Qwen-Audio-Realtime` |

> **重要提醒**：  
> - **模型前缀即能力标识**：所有音频模型均以 `qwen-audio-*` 或 `cosyvoice-*` 开头，通用大模型（如 `qwen-3`）**不支持音频处理**；  
> - **地域与Workspace强绑定**：北京/新加坡地域的域名、API Key、Workspace ID **完全隔离**，跨地域调用必失败；  
> - **流式≠实时**：`X-DashScope-SSE: enable` 仅表示服务端分片推送，仍属非实时API范畴，端到端延迟受网络与音频长度影响；  
> - **调试优先用同步接口**：开发阶段建议先用同步API验证模型效果与参数配置，再迁移到异步/流式生产环境。

---  
*文档更新日期：2024年6月*  
*依据百炼平台 v3.1 音频能力规范编写*

## 被对比主题页

- [audio api directory](../api/audio-api-directory.md)
- [voice customization api directory](../api/voice-customization-api-directory.md)


