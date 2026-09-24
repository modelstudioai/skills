# 实时API方案对比（Omni Realtime vs Realtime User Guide）

## 背景与目的

为帮助开发者在百炼平台中快速、准确地选择适合业务需求的实时推理方案，本文对两类主流实时API能力进行系统性对比：  
- **Omni Realtime API**（`api/omni-realtime-api.md`）：面向端到端多模态实时交互的下一代统一接口，深度集成ASR/TTS/LLM/VAD/工具调用，强调“感知-理解-生成-反馈”闭环；  
- **Realtime User Guide API**（`api/realtime-api-user-guide.md`）：面向通用流式推理场景的基础实时接口，聚焦低延迟文本/音频流处理，设计更轻量、协议更收敛。

本对比旨在厘清二者在能力边界、接入复杂度、模型覆盖、运维成本及适用阶段上的本质差异，避免因选型偏差导致开发返工、功能缺失或计费异常。

---

## 关键维度对比表

| 维度 | Omni Realtime API | Realtime User Guide API |
|------|-------------------|--------------------------|
| **核心定位** | 多模态实时交互操作系统（语音助手、智能会议、全链路客服） | 通用流式推理通道（实时转写、轻量对话、音视频分析） |
| **输入格式** | 支持 `PCM`/`WAV`（采样率 8k/16k/24k/48k）、文本、视频帧（未来扩展）；通过 `input_audio_buffer.append` 增量注入；支持多通道音频（需显式声明） | 仅支持 `pcm16`（16kHz 单声道小端序）或 `opus`；音频帧严格 ≤20ms，每秒 ≤20帧；文本输入通过 `input.text` 事件 |
| **输出格式** | 可配置 `["text"]` 或 `["text","audio"]`；音频支持 `pcm`/`wav`，采样率最高 48kHz；含 ASR 实时识别流（`input_audio_transcription.delta`）和 TTS 流（`output.audio.delta`） | 固定[流式输出](../concepts/streaming-output.md)：`output.text.delta`（token级）、`output.audio.delta`（仅 audio/vl 模型）；音频仅支持 `pcm16`（16kHz），无采样率自定义能力 |
| **支持模型** | `qwen3.8-omni-flash-realtime`（推荐）、`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`；**仅限 Omni 系列多模态模型** | `qwen-audio-realtime-v1`（语音）、`qwen2.5-7b-realtime`（文本）、`qwen-vl-realtime-v1`（视觉语言）；**不支持 Omni 系列模型** |
| **协议支持** | AOQ（推荐，最低端到端延迟）、WebSocket、WebRTC（浏览器直连） | **仅 WebSocket**（`wss://dashscope.aliyuncs.com/realtime/v1/{model}`） |
| **会话管理** | 全生命周期事件驱动：`session.update` → `session.created` → `conversation.item.*` → `session.ended`；支持动态参数更新（如中途切换 voice/VAD） | 连接即会话，`session.update` 仅初始化；**不支持运行时修改模型参数或模态配置**；单连接最长 300 秒，超时需重建 |
| **VAD 能力** | ✅ 原生支持 `server_vad`（声学）与 `semantic_vad`（语义级静音检测，可过滤“嗯”“啊”等填充词）；`semantic_vad` 仅 Qwen3.8/Qwen3.5-Omni 系列可用 | ❌ 无内置 VAD；需客户端自行实现语音活动检测并控制 `input.audio` 发送节奏 |
| **工具调用** | ✅ 同时支持 Function Calling（`tools` 数组）与 MCP（`type: "mcp"`）；但 `tools` 与 `enable_search` 互斥 | ✅ 支持 `tools`（Function Calling），但暂未开放 MCP；`system_prompt` 和 `tools` 是少数被服务端实际生效的参数 |
| **联网搜索** | ✅ `enable_search: true` 可启用自主搜索，支持 `search_options.enable_source` 返回引用来源 | ❌ 不支持联网搜索能力 |
| **音频控制粒度** | ⭐ 极高：独立配置 `audio.input.format` / `audio.output.format`；音色（`voice`）支持多档定制（`Cherry`/`Tina`/`Chelsie`/`longanlingxin`）；支持 `idle_timeout_ms` 控制静默超时 | ⚠️ 有限：`audio_format` 仅声明编码类型（`pcm16`/`opus`），无采样率/位深/声道控制；**无音色选项**；无静默超时机制 |
| **参数可调性** | ✅ 大部分参数（`temperature`/`top_p`/`max_tokens`/`repetition_penalty` 等）在多数模型上可动态设置（Turbo 系列除外） | ⚠️ 有限：`temperature`/`top_p` 在 v202407+ 版本中**已被服务端忽略**；仅 `max_output_tokens`、`system_prompt`、`tools` 确认生效 |
| **API 端点** | 多协议入口：<br>• AOQ: `aoq://...`（需 SDK）<br>• WebSocket: `wss://dashscope.aliyuncs.com/aoq/v1/omni-realtime`<br>• WebRTC: 浏览器直连信令地址 | 单一 WebSocket：<br>`wss://dashscope.aliyuncs.com/realtime/v1/{model}`（如 `qwen-audio-realtime-v1`） |
| **计费方式** | 按 **实际消耗的 input/output tokens + 音频时长（秒）** 分项计费；多模态输出（text+audio）产生双重计费；VAD/搜索/工具调用不额外计费 | 按 **input/output tokens** 计费；音频输入按帧折算为 token 当量（具体换算规则见计费文档）；无音频时长独立计费项 |
| **典型场景** | • 全双工语音助手（用户边说边听，无缝打断）<br>• 智能会议纪要（实时转写+摘要+行动项提取+发言归因）<br>• 多轮语音客服（ASR→意图识别→[函数调用](../concepts/function-calling.md)→TTS播报→VAD轮转） | • 单向语音转写（会议录音实时转文字）<br>• 文本流式问答（客服聊天窗口逐字显示回复）<br>• 简单音视频分析（如短视频语音内容提取） |

---

## 适用场景建议

### ✅ 优先选用 Omni Realtime API 当：
- 业务要求 **全双工、低延迟、多模态闭环**（如用户说话时模型已开始思考并生成TTS，无需等待说完）；
- 需要 **语义级静音检测**（`semantic_vad`）提升交互自然度，避免误触发或漏响应；
- 必须支持 **定制化音色** 或 **高保真音频输出**（如 24kHz/48kHz TTS）；
- 依赖 **联网搜索** 或 **复杂工具链编排**（MCP + Function Calling 混合调度）；
- 客户端环境多样：需兼容 **Web 浏览器（WebRTC）**、移动端（AOQ SDK）及服务端（WebSocket）；
- 已使用 Qwen3.8/Qwen3.5-Omni 系列模型，且追求最新多模态能力。

### ✅ 优先选用 Realtime User Guide API 当：
- 场景相对简单，仅需 **单向[流式输出](../concepts/streaming-output.md)**（如语音转文字后送下游NLU）或 **轻量文本对话**；
- 客户端为标准 WebSocket 环境（如 Node.js 后端、Electron 应用），**无需 WebRTC 或 AOQ 专用协议**；
- 对 **接入速度与维护成本敏感**：协议简单、文档收敛、错误码明确、调试链路短；
- 音频输入格式严格可控（16kHz 单声道 PCM），且无需 VAD 或音色定制；
- 当前仅需 `qwen-audio-realtime-v1` 或 `qwen2.5-7b-realtime` 等基础模型能力，无 Omni 系列升级计划。

> ⚠️ 注意：若项目初期采用 Realtime User Guide，后续需升级至 Omni Realtime，将涉及协议迁移（WebSocket → AOQ/WebRTC）、事件模型重构（`input.text` → `input_audio_buffer.append`）、VAD 逻辑下移至服务端等显著改造。建议在架构设计阶段即评估长期演进路径。

---

## 技术选型参考（致开发者）

| 你的需求 | 推荐方案 | 理由 |
|----------|-----------|------|
| “我要做一个能随时打断、带声音反馈的车载语音助手” | **Omni Realtime** | 全双工、VAD 轮转、TTS 音色定制、低延迟 AOQ 协议缺一不可 |
| “我只需把客服电话录音实时转成文字，存入数据库” | **Realtime User Guide** | `qwen-audio-realtime-v1` 开箱即用，无需管理会话状态与音频格式细节 |
| “我们做教育APP，学生朗读英语，AI实时评分+发音纠正” | **Omni Realtime** | 需同时处理音频输入（ASR）、文本分析（语法/流利度）、TTS 模范朗读（多音色）、VAD 判断朗读是否完成 |
| “后台服务调用大模型做流式摘要，输入是文本，输出是文本” | **Realtime User Guide**（`qwen2.5-7b-realtime`） | 协议轻量、连接稳定、token 计费透明；Omni Realtime 在纯文本场景无优势且成本更高 |
| “客户要求支持浏览器直接访问，不装App、不走代理” | **Omni Realtime**（WebRTC） | Realtime User Guide 仅 WebSocket，浏览器受限于 CORS 与证书策略，WebRTC 是唯一合规直连方案 |
| “团队刚接触实时API，希望最快跑通 Hello World” | **Realtime User Guide** | 连接 URL 明确、参数极少、错误提示清晰（如 `input_invalid` 直接指出采样率错误），学习曲线平缓 |

**最后建议**：  
- 新项目启动，请优先评估 **Omni Realtime** —— 其设计代表百炼实时能力的演进方向，长期兼容性与功能扩展性更强；  
- 现有 Realtime User Guide 项目如无强交互需求，可维持现状，但应关注 Omni Realtime 的灰度开放节奏，预留升级路径；  
- 所有方案均需通过 [百炼控制台](https://dashscope.console.aliyun.com) 获取有效 API Key，并确保 endpoint 与 Key 所属 Region 严格一致。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


