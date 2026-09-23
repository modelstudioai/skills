# 实时交互API与应用调用API对比

为帮助开发者在构建智能语音助手、多模态客服、自动化工作流等场景时做出高效、可靠的技术选型，本文对百炼平台两大核心调用路径——**实时交互API（Omni Realtime API）** 与 **应用调用API（Application Call）** 进行系统性对比。二者定位不同：前者面向**低延迟、事件驱动、多模态流式交互**的端到端实时会话；后者面向**业务逻辑封装、应用级抽象、灵活编排与长期状态管理**的智能体/工作流调用。理解其差异是设计高可用、可扩展AI服务的关键前提。

## 关键维度对比

| 维度 | 实时交互API（Omni Realtime API） | 应用调用API（Application Call） |
|------|----------------------------------|----------------------------------|
| **核心定位** | 低延迟、全双工、多模态（音/文/视）实时会话引擎 | 智能体（Agent）、工作流（Workflow）等业务应用的统一调用入口 |
| **通信协议** | WebSocket / AOQ / WebRTC（长连接、事件驱动） | HTTP/HTTPS（RESTful + SSE 流式支持） |
| **输入格式** | 事件驱动：<br>• `session.update`（配置会话）<br>• `input_audio_buffer.append`（音频流分块）<br>• `user_message`（文本输入） | 请求体驱动：<br>• DashScope API：`prompt` / `messages` / `image_list` / `file_list`<br>• Responses API（OpenAI兼容）：`input`（字符串或消息数组） |
| **输出格式** | 服务端事件流：<br>• `conversation.item.created`（文本/工具调用）<br>• `output_audio_buffer.append`（PCM/WAV音频流）<br>• `input_audio_buffer.speech_started/stopped`（VAD事件） | 响应体驱动：<br>• 同步：JSON 结构化响应（含 `output.text` / `output.tool_calls` / `output.files`）<br>• 流式：SSE Chunk（`data: {...}`）或 OpenAI-style `delta`<br>• 异步：返回 `task_id`，需轮询查询结果 |
| **支持模型/能力** | 专属实时模型系列：<br>• `qwen3.8-omni-flash-realtime`（支持视频、MCP、语义VAD、多通道音频）<br>• `qwen3.5-omni-flash-realtime/plus-realtime`（Function Calling、server/semantic VAD）<br>• `qwen3-omni-flash-realtime` / `qwen-omni-turbo-realtime`（基础实时能力，部分参数不可调） | 通用模型+应用封装：<br>• 可调用任意已发布智能体（Agent 2.0/旧版）、工作流<br>• 底层可绑定 `qwen-max`/`qwen-plus`/`qwen-turbo`/VL系列/私有微调模型等<br>• 支持RAG知识库、[长期记忆](../concepts/memory.md)（`memory_id`）、插件/工具链（通过智能体配置） |
| **API 端点** | 协议级接入，需先获取动态连接地址：<br>• WebSocket: `wss://...`<br>• AOQ/WebRTC: 由 [模型接入方式文档](../../raw/model-api-reference/omni-realtime-api/omni-realtime-model-access.md) 提供 | 固定HTTP端点：<br>• DashScope原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• OpenAI兼容（Responses）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` |
| **会话生命周期管理** | **显式事件驱动**：<br>• 客户端发起 `session.update` → 服务端返回 `session.created` + `session.updated`<br>• 需主动处理 `input_audio_buffer` 流控、VAD事件、会话超时（`idle_timeout_ms`）<br>• 无自动上下文持久化，需自行维护 | **隐式/可选状态管理**：<br>• 通过 `session_id`（1小时有效期）或 `messages` 数组传入历史上下文<br>• 新版智能体支持 `memory_id` 实现跨会话[长期记忆](../concepts/memory.md)<br>• 工作流支持内置状态机与节点间数据传递 |
| **计费方式** | 按**实际音频时长（秒） + 文本[Token](../concepts/token.md)数 + 工具调用次数**计费<br>• 音频输入/输出均计费（按采样率、声道、时长折算）<br>• 支持细粒度控制（如 `sample_rate`, `channels`），直接影响成本 | 按**调用次数 + 输入/输出[Token](../concepts/token.md)数 + 文件解析页数 + RAG检索次数**计费<br>• 智能体/工作流调用本身计费，底层模型消耗计入应用配额<br>• 异步任务按完成计费（非请求即计费） |
| **典型场景** | • 实时语音助手（车载/家居）<br>• 智能客服电话坐席（全双工对话+实时转写+情绪识别）<br>• 多人会议实时摘要与发言分离<br>• AR/VR语音交互（低延迟音频闭环） | • 企业知识库问答机器人（网页/APP嵌入）<br>• 自动化审批工作流（表单解析→规则判断→邮件通知）<br>• 多步骤AI Agent（如“订机票→查天气→生成行程单”）<br>• 面向开发者的OpenAI生态快速迁移（Responses API） |

## 各方案适用场景建议

### ✅ 推荐使用 **实时交互API** 当：
- 业务强依赖**亚秒级端到端延迟**（如语音打断、实时回声消除、VAD驱动的自然停顿）；
- 需要**原生多模态流式I/O**：持续接收麦克风音频流 + 实时合成TTS音频流 + 可选视频帧输入；
- 场景涉及**复杂音频控制**：多声道输入、自定义采样率/位深、语义级语音活动检测（`semantic_vad`）；
- 架构已具备WebSocket/AOQ长连接运维能力，且团队熟悉事件驱动编程模型；
- 不需要跨会话[长期记忆](../concepts/memory.md)或复杂业务流程编排，聚焦“单次高质量实时对话”。

### ✅ 推荐使用 **应用调用API** 当：
- 目标是快速上线一个**功能完整的AI应用**（如客服机器人、合同审查助手），而非从零构建语音栈；
- 需要复用百炼平台的**高级能力封装**：RAG知识库、长期记忆、可视化工作流编排、插件市场集成；
- 调用方为Web前端、移动App或后端服务，偏好标准HTTP/REST接口与OpenAI SDK兼容性；
- 业务逻辑复杂，需**多步骤决策、条件分支、人工审核介入、异步长任务**（如文件批量处理）；
- 成本敏感且流量模式为“突发+离散”，无需为闲置长连接支付保活成本。

### ⚠️ 注意规避的误用情形：
- ❌ 用实时API实现纯文本问答机器人（过度复杂、成本高、无VAD收益）；  
- ❌ 用应用调用API实现全双工语音通话（HTTP无法满足实时音频流要求，必然卡顿）；  
- ❌ 在未启用`memory_id`或未透传`messages`的情况下，期望应用调用API自动维持多轮对话上下文；  
- ❌ 在实时API中尝试调用未在`tools`列表声明的函数，或同时启用`tools`与`enable_search`（二者互斥）。

## 技术选型决策参考

作为开发者，请按以下流程进行技术选型：

1. **明确核心SLA指标**：  
   → 若**端到端延迟 ≤ 300ms** 是硬性要求 → 选 **实时交互API**；  
   → 若延迟容忍度 ≥ 1s，且更关注**功能完整性与开发效率** → 选 **应用调用API**。

2. **评估输入模态需求**：  
   → 必须接入**原始音频流（PCM/WAV）并实时处理** → **实时交互API**；  
   → 输入为文本、图片URL、PDF文件等结构化/半结构化数据 → **应用调用API**（或搭配应用组件API）。

3. **审视业务抽象层级**：  
   → 你在构建一个**“能力组件”**（如语音SDK、TTS引擎）→ **实时交互API**；  
   → 你在交付一个**“业务应用”**（如“HR政策问答Bot”、“财务报销助手”）→ **应用调用API**。

4. **检查工程成熟度**：  
   → 团队具备WebSocket连接管理、音频编解码、流控重试经验 → 可驾驭实时API；  
   → 团队熟悉HTTP客户端、异步任务调度、OpenAI生态 → 应用调用API上手更快。

> 💡 **进阶组合建议**：在大型系统中，二者可协同使用——例如，前端通过**实时交互API**处理用户语音输入与TTS播报，后端将语音ASR文本结果经清洗后，通过**应用调用API**提交给智能体进行深度推理与业务决策，再将结构化结果交由实时API合成语音反馈。这种分层架构兼顾实时性与业务灵活性。

---  
*最后更新：2024年6月 | 百炼平台技术文档中心*

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)


