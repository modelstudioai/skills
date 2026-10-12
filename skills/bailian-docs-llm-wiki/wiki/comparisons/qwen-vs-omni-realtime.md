# Qwen API 与 Omni Realtime API 对比

本文旨在为百炼平台开发者提供清晰、客观的技术选型参考，帮助其根据实际业务需求（如延迟敏感性、输入模态复杂度、交互形态、工程集成成本等）合理选择 API 方案。Qwen API 面向通用文本智能任务，强调模型能力广度与接口灵活性；Omni Realtime API 则专为低延迟、[多模态](../concepts/multi-modal.md)、双向流式实时交互场景深度优化。二者定位互补，**并非替代关系，而是分层协作关系**：典型架构中，Omni Realtime 可作为前端“实时感知层”，Qwen API 作为后端“决策与生成层”协同工作。

## 关键维度对比

| 维度 | Qwen API | Omni Realtime API |
|------|----------|-------------------|
| **核心定位** | 通用大语言模型推理服务（文本为中心） | 低延迟、[多模态](../concepts/multi-modal.md)、双向流式实时交互服务 |
| **通信协议** | HTTP/1.1（RESTful） | WebSocket（全双工、事件驱动） |
| **输入格式** | JSON 结构化请求体（`messages` 数组 + 可选 `tools`/`response_format` 等） | WebSocket 事件流（`session.update`、`input.text`、`input.audio`、`input.image` 等标准化事件） |
| **输出格式** | 同步响应（JSON）或流式 SSE（`data: {...}`）/ JSON Lines（DashScope） | 异步事件流（`output.text.delta`、`output.audio.delta`、`output.image` 等服务端推送事件） |
| **支持模型** | `qwen-max`（高性能）、`qwen-plus`（均衡）、`qwen-turbo`（高性价比） | `omni-realtime-202409`（唯一当前稳定版本，[多模态](../concepts/multi-modal.md)融合模型） |
| **核心能力** | 文本生成、多轮对话、结构化输出（JSON Schema）、工具调用（DashScope 原生支持）、Logprobs 控制 | 实时 ASR/TTS、多模态理解（文本+语音+图像）、端到端低延迟响应（P95 < 800 ms）、上下文感知流式生成 |
| **API 端点** | • OpenAI 兼容：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation` | `wss://dashscope.aliyuncs.com/api/v1/omni/realtime?model=omni-realtime-202409&api_key=...&stream=true` |
| **计费方式** | 按 token 用量计费（输入 + 输出 tokens），统一纳入百炼平台配额体系；免费额度按自然月重置 | 按连接时长（秒） + 音频处理时长（秒） + 图像处理次数计费；需单独开通 `realtime` 权限 scope；无自然月免费额度，按实际用量结算 |
| **典型延迟（P95）** | 同步调用：数百毫秒至数秒（取决于模型、上下文长度、网络）<br>流式首 token：~300–800 ms（DashScope） | 端到端 P95 < 800 ms（含音频编解码、传输、模型推理、TTS 合成全流程） |
| **上下文管理** | 客户端完全负责维护 `messages` 历史；Anthropic 接口内置有限历史管理 | 单连接内自动维护会话上下文；支持显式 `session.context` 注入长程记忆；不跨连接继承 |
| **多模态支持** | ❌ 不支持语音/图像输入；纯文本接口 | ✅ 原生支持文本、PCM/MP3/WAV 音频、JPEG/PNG 图像（≤10 MB）混合输入 |
| **流式能力** | 支持（OpenAI 兼容 & DashScope），但为单向响应流（server → client） | 支持（强制启用），为双向流式（client ↔ server），可实时中断、追加、切换输入模态 |

## 各方案的适用场景建议

### ✅ 选择 Qwen API 的典型场景：
- **后台批处理与异步任务**：如内容摘要、报告生成、代码补全、邮件/文档润色等对实时性要求不高的任务。
- **需要强结构化输出的系统集成**：如需严格返回 JSON Schema 格式数据（DashScope `response_format`），用于下游数据库写入或 API 响应。
- **复杂工具调用链路**：需自主编排多个外部工具（搜索、计算、数据库查询等）并进行结果聚合与反思（`thinking` 模式），且偏好 Anthropic Messages 接口语义。
- **已有 OpenAI 生态技术栈迁移**：快速对接现有基于 OpenAI SDK 的应用，仅需修改 endpoint 和认证方式。
- **成本敏感型长文本处理**：利用 `qwen-turbo` 处理万字级文档分析，单位 token 成本显著低于实时流式方案。

### ✅ 选择 Omni Realtime API 的典型场景：
- **实时语音交互应用**：如智能客服热线、车载语音助手、会议实时转录与摘要、无障碍语音交互设备。
- **音视频内容实时分析**：直播弹幕情感联动、在线教育课堂实时答题反馈、短视频内容即时理解与评论生成。
- **多模态沉浸式体验**：用户上传图片+语音提问（如“这张发票里金额是多少？读给我听”），要求毫秒级响应与 TTS 合成。
- **需要动态中断与上下文修正的交互**：用户在 AI 回答中途插入新指令（如“等等，改成英文回答”），Omni 支持实时 cancel 并重定向。
- **边缘-云协同架构**：前端轻量采集（麦克风/摄像头），通过 WebSocket 低开销上传原始流，由云端 Omni 模型完成高算力多模态理解。

## 技术选型参考（面向开发者）

| 选型考量因素 | 推荐方案 | 理由说明 |
|--------------|----------|----------|
| **是否必须支持语音/图像输入？** | Omni Realtime API | Qwen API 仅接受文本，无法处理原始音视频流或图像二进制数据。 |
| **端到端延迟能否容忍 > 1 秒？** | Qwen API | 若业务允许“发送→等待→接收”模式（如网页表单提交），Qwen 更简单；若需“边说边听、所见即所得”，必须选 Omni。 |
| **是否已使用 OpenAI SDK 或需最小化改造？** | Qwen API（[OpenAI 兼容接口](../concepts/openai-compatible-api.md)） | 可复用 `openai` Python SDK，仅替换 `base_url` 和 `api_key`，无需重写业务逻辑。 |
| **是否需要严格 JSON 输出用于自动化系统？** | Qwen API（DashScope `response_format`） | Omni 的 `output.text.delta` 是碎片化流，需客户端拼接；Qwen 原生支持完整 JSON 响应。 |
| **是否需在单次交互中混合多种输入（如先传图再语音追问）？** | Omni Realtime API | 其事件模型天然支持 `input.image` → `input.audio` → `input.text` 动态组合；Qwen 需预处理为文本描述。 |
| **是否需在响应中直接播放语音？** | Omni Realtime API | 内置 TTS，服务端直接推送 `output.audio.delta`（MP3/PCM），前端可直连 AudioContext；Qwen 仅输出文本，需额外集成 TTS 服务。 |
| **团队是否缺乏 WebSocket 开发经验？** | Qwen API | RESTful 接口调试简单（curl/postman），错误排查直观；Omni 需处理连接保活、事件序列、状态同步等复杂性。 |
| **是否需超长对话上下文（>32K tokens）？** | Qwen API（`qwen-max`） | Omni 当前上下文窗口未公开披露，且受连接时长（300s）限制；Qwen 支持 32768 tokens 上下文，适合长文档分析。 |

> **重要提示**：在构建端到端智能体（Agent）时，**推荐组合使用**——前端用 Omni Realtime 处理实时多模态输入与语音输出，后端调用 Qwen API 执行复杂推理、工具调用或生成长文本内容，再将结果交由 Omni 合成语音。此架构兼顾实时性、能力深度与工程可控性。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)


