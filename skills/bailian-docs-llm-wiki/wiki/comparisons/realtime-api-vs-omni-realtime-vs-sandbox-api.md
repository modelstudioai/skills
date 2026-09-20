# 实时API、Omni实时API与沙箱API对比

本对比旨在帮助开发者清晰理解百炼平台三大核心 API 能力的定位差异、技术边界与适用场景，避免因选型不当导致开发返工、延迟超标或功能不可达。三者虽同属“实时交互”范畴，但设计目标、协议栈、数据形态与抽象层级存在本质区别：  
- **Realtime API** 聚焦**端到端语音流处理**，是低延迟语音交互的“原子通道”；  
- **Omni实时API** 构建**多模态智能对话体**，是具备语义理解、工具调度与VAD感知的“对话操作系统”；  
- **Sandbox API** 提供**安全可控的代码执行环境**，是AI Agent行动能力的“可信沙箱底座”。  
三者非替代关系，而是可协同演进的技术栈（例如：Omni实时API调用工具时，后端可由Sandbox API托管的Python沙箱执行；Realtime API输出的ASR文本可作为Omni会话的初始输入）。本文为技术选型提供结构化决策依据。

## 关键维度对比

| 维度 | Realtime API | Omni实时API | 沙箱API |
|------|--------------|--------------|-----------|
| **核心定位** | 语音流式处理通道（ASR/TTS/V2V） | 多模态实时对话引擎（语音+文本+工具+搜索） | 隔离式代码/模型执行环境（容器化运行时） |
| **通信协议** | WebSocket（双向流式） | WebSocket（事件驱动，严格状态机） | RESTful HTTP（同步请求） + WebSocket（实例连接时用于终端交互） |
| **输入格式** | 原始 PCM 音频帧（16kHz/16bit/单声道），每帧 ≤320 字节；不支持封装格式（如 WAV/MP3） | 支持 PCM 或 WAV 音频（16-bit 单声道），采样率支持 8k/16k/24k/48kHz；支持文本、图像（Base64/JPEG，≤256KB） | 无直接数据输入；通过 `POST /sandboxes` 创建实例时传入配置参数（如 `templateID`, `timeout`）；后续通过终端连接（WebSocket）或文件挂载（`mntConfig`）注入代码/数据 |
| **输出格式** | 流式事件：`response.text.delta`（文本片段）、`response.audio.delta`（PCM音频片段）、`response.audio_transcript.delta`（ASR预览）等 | 流式事件：`response.text.delta`、`response.audio.delta`（支持 PCM/WAV 输出）、`response.audio_transcript.delta`、`response.function_call_arguments.*`（工具调用）、`conversation.item.created`（上下文项）等 | 同步响应：创建/查询/操作接口返回 JSON 结构化结果（如实例 ID、连接域名、构建状态）；终端连接后通过 WebSocket 返回标准 Shell 输出（stdout/stderr）或文件内容 |
| **支持模型** | 专用语音模型：<br>• `qwen-audio-realtime-v1`（ASR）<br>• `qwen-tts-realtime-v1`（TTS）<br>• `qwen-v2v-realtime-v1`（V2V，Beta） | 多模态大模型：<br>• `qwen3.5-omni-plus-realtime`<br>• `qwen3.5-omni-flash-realtime`<br>• `qwen3-omni-flash-realtime`<br>• `qwen-omni-turbo-realtime` | **不提供模型推理能力**；仅提供运行环境。可在沙箱中自行部署任意开源模型（如 Llama、Qwen、Whisper）或执行 Python/Node.js 代码 |
| **API 端点** | `wss://dashscope.aliyuncs.com/realtime/v1/chat` | `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`（推荐业务空间专属域名） | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`（REST）<br>实例连接：`wss://{domain}/connect?token={token}`（WebSocket） |
| **计费方式** | 按**音频处理时长（秒）** 计费（ASR/TTS/V2V 分别计费），支持配额管理与 QPS 限流 | 按**会话时长（秒）** 计费（含语音输入、文本生成、音频合成全链路），支持按模型规格分档计价 | 按**沙箱实例运行时长（秒）** 计费（CPU/内存规格影响单价），支持自动暂停（`timeout`）与强制释放（`maxRunningTimeout`）控制成本 |
| **典型场景** | • 实时语音转文字（会议记录、直播字幕）<br>• 语音播报（导航、IoT设备反馈）<br>• 中英同传（V2V Beta） | • 智能语音助手（支持打断、多轮语义VAD、音色克隆）<br>• 全自动客服（自动触发订单查询、退款工具）<br>• 多模态交互应用（语音提问+图片辅助理解） | • AI Agent 执行层（调用外部API、解析PDF、运行SQL）<br>• 自动化工作流（CI/CD 中模型微调、数据清洗）<br>• 安全沙箱测试（第三方代码/模型安全评估） |
| **关键限制** | • 单连接仅支持 1 路音频流<br>• 不支持热词增强、批量离线任务<br>• 音频帧间隔需 ≤50ms，超时 200ms 断连 | • `enable_search` 与 `tools` 互斥<br>• `semantic_vad` 仅 qwen3.5 系列支持<br>• 图像输入 ≤256KB、≤1080p、建议 1 张/秒 | • 仅支持 `cn-beijing` 地域<br>• CPU/内存必须选用平台预设组合（如 `2/4096`）<br>• 模版构建未就绪（`buildStatus ≠ "ready"`）时无法创建实例 |

## 各方案的适用场景建议

### ✅ 选择 Realtime API 当：
- 你的核心需求是**极低延迟（<300ms）的纯语音流处理**，且无需语义理解或工具调用；
- 你已具备成熟的前端音频采集与预处理能力（如 Web Audio API 解封装、VAD 前置检测）；
- 场景明确限定于 ASR（语音识别）、TTS（语音合成）或 V2V（语音转译+合成）三类之一；
- 你需要对音频帧级精度进行强控制（如自定义静音检测、帧对齐渲染）；
- *典型用户*：音视频 SDK 开发者、智能硬件固件团队、实时字幕 SaaS 服务商。

### ✅ 选择 Omni实时API 当：
- 你需要构建一个**具备完整对话生命周期管理能力的语音助手或客服系统**；
- 要求支持**语义级语音活动检测（semantic_vad）**、**多模态混合输出（文本+音频）**、**自主工具调用** 或 **联网搜索**；
- 希望复用平台提供的音色克隆、VAD、会话状态机等高级能力，而非从零实现；
- 接受稍高一点的端到端延迟（通常 <800ms），以换取更强的语义交互能力；
- *典型用户*：智能座舱语音系统、企业级语音客服平台、多模态教育机器人开发者。

### ✅ 选择 沙箱API 当：
- 你的应用需要**安全、隔离、可编程地执行任意代码或模型**（如调用银行API、运行本地Llama模型、解析私有PDF）；
- 你正在构建 **AI Agent 的“行动层”**，需将大模型的规划（Plan）转化为真实世界动作（Act）；
- 你需要在 CI/CD 流程中自动化验证模型行为、数据处理脚本或第三方集成逻辑；
- 对执行环境的资源（CPU/内存）、网络策略（白名单/黑名单）、生命周期（自动暂停/释放）有精细化管控需求；
- *典型用户*：AI Agent 框架开发者、MLOps 工程师、金融/政务领域合规性要求高的应用架构师。

## 技术选型参考指南（面向开发者）

| 你的问题 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| “我需要把用户说话实时转成文字，延迟越低越好，不做其他事。” | ✅ Realtime API | 专为语音流优化，端到端延迟最低，无额外语义层开销 |
| “我要做一个能听懂用户说‘查一下我的订单’并自动调用订单API的语音助手。” | ✅ Omni实时API | 内置 `tools` 调用机制 + `semantic_vad` 支持自然打断，无需自己实现意图识别与工具路由 |
| “我的大模型回复里说‘我已帮你生成报告’，但我需要真正在后台跑 Python 脚本生成 PDF 并发邮件。” | ✅ 沙箱API | Realtime/Omni 均不执行代码；必须用沙箱承载实际执行逻辑，再将结果回传给对话系统 |
| “我想让语音助手用我自己的声音说话，且支持中英混说。” | ✅ Omni实时API（首选）或 Realtime API（次选） | Omni 支持声纹复刻与多语言 TTS；Realtime 也支持，但缺乏 Omni 的语义上下文与多模态协同能力 |
| “我需要批量处理 1000 小时录音，生成文字稿和摘要。” | ❌ 以上均不适用 → 请使用 [Batch API](../../raw/model-api-reference/batch-api-user-guide.md) | 三者均为实时流式接口，不适用于离线批量任务；Batch API 专为此类场景设计 |
| “我需要在网页上嵌入一个可执行 Python 代码的交互式控制台。” | ✅ 沙箱API | 可创建沙箱实例 → 获取 WebSocket 连接 → 将用户输入的代码发送至终端 → 流式返回 stdout/stderr |

> **协同使用提示**：生产级语音应用常采用分层架构：  
> **前端采集** → **Realtime API（ASR）** → **文本送入 Omni实时API（对话理解+工具调度）** → **Omni 触发工具时，调用沙箱API 创建实例执行真实动作** → **沙箱返回结果 → Omni 生成最终语音回复 → Realtime API（TTS）合成播放**。  
> 此模式兼顾低延迟、强语义与高安全性，是百炼平台推荐的最佳实践路径。

## 被对比主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [sandbox api](../api/sandbox-api.md)


