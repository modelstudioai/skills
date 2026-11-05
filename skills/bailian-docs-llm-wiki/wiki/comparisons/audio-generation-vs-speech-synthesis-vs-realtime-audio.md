# 音频生成、语音合成与实时音频 API 对比

本文旨在帮助开发者清晰区分百炼平台中三类核心音频能力的技术定位、能力边界与适用场景，避免因概念混淆导致选型偏差。随着多模态交互需求增长，**语音合成（TTS）** 侧重“文本→高质量语音”的静态生成；**音频生成（Audio Generation）** 聚焦“文本/控制指令→创意音频内容”（如音效、旁白、风格化语音）；而**实时音频 API**（含 Omni Realtime 和 Realtime API）则面向端到端低延迟流式交互，强调语音输入识别、语义理解、语音输出的闭环协同。三者在输入输出范式、协议模型、计费逻辑和工程集成方式上存在本质差异。本对比基于当前（2025年Q3）生产环境最新文档与接口行为整理，所有限制以实际 API 响应为准。

## 关键维度对比表

| 维度 | 语音合成（TTS）<br>`/services/aigc/audio/speech-synthesis` | 音频生成（Audio Generation）<br>`/services/aigc/audio/audio-generation` | 实时音频 API（Omni Realtime） | 实时音频 API（Realtime API） |
|------|-------------------------------------------------------------|--------------------------------------------------------------------------|------------------------------|-----------------------------|
| **核心目标** | 将确定性文本转换为自然、可配置的语音输出 | 根据文本提示生成创意音频内容（旁白、音效、风格迁移等） | 多模态实时对话：语音输入→理解→语音/文本输出闭环 | 低延迟流式处理：语音/视频流实时转写、事件检测、上下文续写 |
| **输入格式** | `text` 字符串（≤5000字符），支持 `voice`/`speed`/`pitch` 等控制参数 | `prompt`（描述性文本）、`duration`（秒，≤30）、可选 `audio_url`（用于风格迁移） | WebSocket 连接 + 事件流：<br>• `input_audio_buffer.append`（Base64 PCM/WAV）<br>• `conversation.item.create`（文本） | WebSocket 连接 + 二进制帧：<br>• 音频流（PCM/WAV/Opus 分片）<br>• 视频流（H.264/H.265 分片） |
| **输出格式** | `wav` / `mp3` / `json`（含音频 URL 或 Base64）；流式仅支持 `wav` | `wav`（固定格式，非流式）；返回完整音频二进制或下载 URL | 事件驱动流式响应：<br>• `conversation.item.created`（含 `text` 或 `audio` 内容）<br>• `response.content_part.added`（增量音频 chunk）<br>• 输出音频为 PCM（可配采样率） | 事件驱动流式响应：<br>• `event: "text_delta"`（文本流）<br>• `event: "audio_chunk"`（PCM/WAV 二进制分片） |
| **支持模型** | `qwen2-audio-tts-01` 等专用 TTS 模型 | `qwen2-audio-gen-03` 等音频生成模型 | `qwen3.8-omni-flash-realtime`（推荐）、`qwen3.5-omni-plus-realtime` 等 | `qwen-audio-realtime`（ASR+理解）、`qwen-vl-realtime`（音视频多模态） |
| **API 端点** | `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/speech-synthesis` | `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/audio-generation` | WebSocket `wss://dashscope.aliyuncs.com/realtime/v1/omni`（需 AOQ/WebRTC/WS 协议） | WebSocket `wss://dashscope.aliyuncs.com/realtime/v1/chat`（需指定 `X-DashScope-Model`） |
| **认证方式** | HTTP Header `Authorization: Bearer <API_KEY>` | HTTP Header `Authorization: Bearer <API_KEY>` | WebSocket 连接时携带 `Authorization` Header | WebSocket 连接时携带 `Authorization` 和 `X-DashScope-Model` Header |
| **计费方式** | 按**合成音频时长（秒）** 计费（含静音段）；支持预付费包与后付费 | 按**生成音频时长（秒）** 计费（上限 30 秒/次）；按调用次数叠加 | 按**会话时长（秒）** + **输出 [Token](../concepts/token.md) 数** + **工具调用次数** 计费；VAD/搜索/空间音频等高级功能可能产生附加费用 | 按**流式音频处理时长（秒）** + **输出 [Token](../concepts/token.md) 数** 计费；视频流按分辨率与帧率加权计费 |
| **典型场景** | 有声书配音、客服IVR语音播报、APP内文字朗读 | 游戏音效生成、短视频旁白合成、品牌广告语音定制、AI播客开场音乐生成 | 智能语音助手（带唤醒与语义中断）、实时会议双语同传、车载语音交互系统 | 实时会议语音转写与摘要、直播流实时字幕、安防音视频事件检测、远程医疗语音记录 |

## 各方案适用场景建议

### ✅ 推荐选择「语音合成（TTS）」当：
- 输入是**确定、静态的文本**（如一段公告、说明书、新闻稿）；
- 对语音**自然度、音色一致性、发音准确性要求高**，且无需实时交互；
- 业务流程为**单向批量生成**（如每日生成100条语音通知），对延迟不敏感（秒级响应即可）；
- 需要精细控制语速、语调、停顿，或支持多语种混读。

### ✅ 推荐选择「音频生成（Audio Generation）」当：
- 输入是**创意性提示词**（如“科幻电影预告片旁白，紧张神秘，带轻微回声”）；
- 目标产出是**非人声主导的音频内容**（环境音效、背景音乐片段、拟声词）或**风格化语音**（非标准播音腔）；
- 需要**文本驱动的音频内容创作**，而非简单朗读；
- 单次生成时长 ≤30 秒，且接受非流式交付（生成完成后下载）。

### ✅ 推荐选择「Omni Realtime API」当：
- 构建**全链路语音交互产品**（如智能音箱、车载助手、AR眼镜语音界面）；
- 要求**端到端延迟 <800ms**，支持 VAD 自动启停、语义级打断、多轮语音上下文理解；
- 需要**同时输出文本与语音**，并集成工具调用（查天气、设闹钟）或联网搜索；
- 支持复杂音频输入（如双声道空间音频）或需要客服场景优化（`semantic_vad_ec`）。

### ✅ 推荐选择「Realtime API」当：
- 处理**持续音视频流**（如会议系统、直播平台、监控摄像头流）；
- 核心诉求是**高精度、低延迟的流式转写**，或**音视频联合分析**（如“检测到婴儿哭声+画面出现摇篮”）；
- 已有成熟流媒体基础设施，可自主管理 WebSocket 连接、帧编码/解码与状态同步；
- 不需要模型侧语义理解闭环，仅需将原始流转化为结构化文本/事件/音频分片。

## 技术选型参考指南（面向开发者）

| 选型考量点 | 推荐方案 | 说明 |
|------------|----------|------|
| **是否需要“说一句话就立刻得到回答”的交互感？** | Omni Realtime > Realtime API ≫ TTS / Audio Gen | TTS 和 Audio Gen 是请求-响应模式，无持续会话能力；Realtime API 支持流式但无内置语义理解；Omni Realtime 提供开箱即用的语音对话闭环。 |
| **输入是文件还是实时流？** | 文件 → TTS / Audio Gen；实时流 → Realtime API / Omni Realtime | TTS/Audio Gen 仅接受 `audio_url` 或文本；Realtime API 和 Omni Realtime 必须通过 WebSocket 流式推送音频数据。 |
| **是否需自定义语音风格（非音色）？** | Audio Generation > TTS | TTS 控制音色/语速/语调；Audio Generation 支持 `prompt` 描述情绪、场景、混响等抽象风格特征。 |
| **是否已有 WebSocket 客户端开发经验？** | Realtime API（轻量）或 Omni Realtime（功能重） | Realtime API 协议更简洁（二进制帧）；Omni Realtime 事件模型更丰富但需严格遵循 `session.update`/`input_audio_buffer` 等生命周期事件。 |
| **是否需长期会话状态维护？** | Omni Realtime（会话内状态自动维持） > Realtime API（需应用层管理 `conversation_id`） | Omni Realtime 在单次连接内自动维护对话上下文；Realtime API 的 `conversation_id` 仅为透传标识，服务端不保存状态。 |
| **成本敏感且调用量大？** | TTS（单位时长成本最低） > Audio Gen > Realtime API ≈ Omni Realtime | TTS 为纯生成，无 VAD/搜索/工具等附加模块；Omni Realtime 的高级功能显著提升单会话成本，适合高价值交互场景。 |

> **重要提醒**：  
> - 所有音频 API 均强制校验 `model` 参数，**不可省略或使用未文档化的模型 ID**；  
> - 流式响应（`stream=true`）**仅支持 `wav` 格式**，其他格式请求将返回 400 错误；  
> - Omni Realtime 的 `qwen3.8-omni-flash-realtime` 模型已强制要求 `audio.output.voice` 字段，弃用旧版 `session.voice`；  
> - Realtime API 单连接最长 300 秒，超时需客户端主动重建连接并恢复上下文；  
> - 音频生成服务端强制截断至 30 秒，文档中“60秒生成”为历史遗留描述，以实际响应为准。  

请根据实际业务需求、技术栈成熟度与成本预算综合决策。建议新项目优先评估 Omni Realtime（交互闭环）与 TTS（基础播报）的组合使用；音视频流处理类项目应首选 Realtime API；创意音频内容生产则聚焦 Audio Generation。

## 被对比主题页

- [audio api references](../api/audio-api-references.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


