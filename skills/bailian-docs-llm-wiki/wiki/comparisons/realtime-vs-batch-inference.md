# 实时推理与批量推理能力对比

本文档旨在帮助开发者清晰理解百炼平台中**实时推理（Real-time Inference）** 与**批量推理（Batch Inference）** 两类核心能力的定位、差异与适用边界。随着多模态交互场景爆发式增长，低延迟流式响应与高吞吐离线处理的需求并存——选择错误的推理模式将直接导致体验劣化、资源浪费或架构返工。本对比基于当前（2024年Q3）百炼平台正式发布的 API 能力，聚焦技术本质而非营销口径，为架构设计、SDK选型与成本优化提供可落地的决策依据。

## 关键维度对比

| 维度 | 实时推理（Realtime API） | 批量推理（Qwen API） |
|------|--------------------------|------------------------|
| **核心定位** | 端到端低延迟双向交互管道，强调“人机共时性” | 高吞吐、确定性、可重入的任务执行引擎，强调“结果准确性与资源效率” |
| **输入格式** | • WebSocket/AOQ/WebRTC：二进制音频帧（PCM/WAV）、base64图像帧、JSON结构化事件<br>• 支持混合模态流式注入（如边说边传图）<br>• 输入无固定长度限制，按帧/事件持续推送 | • HTTP JSON：`messages` 数组（文本）、`input` 字段（多模态）<br>• 图像/视频支持 URL、base64 Data URI 或文件上传（DashScope 原生接口）<br>• 单次请求输入有明确大小上限（如图像总像素 ≤ 4096×4096，视频帧数 ≤ 100） |
| **输出格式** | • 流式事件驱动：`response.text.delta`（语义级文本片段）、`response.audio.chunk`（TTS音频块）、`response.vision.result`（视觉分析结果）等<br>• 支持服务端主动推送状态事件（如 `speech.start`, `thinking`, `interrupted`）<br>• 输出无完整包概念，需客户端拼接与状态管理 | • 同步响应：完整 JSON 对象（含 `choices[0].message.content` 或 `output.text`）<br>• 流式响应（`stream=true`）仅返回 `delta` 文本片段，**不包含音频、视觉中间态或控制事件**<br>• 输出结构标准化，符合 OpenAI/Anthropic/DashScope 协议规范 |
| **支持模型** | • **严格限定**：仅支持专为实时场景优化的模型族<br>　– `qwen-omni-realtime`（全模态联合建模）<br>　– `qwen3.8-omni-flash-realtime`, `qwen3.5-livetranslate-flash-realtime`, `qwen-audio-3.1-realtime-plus` 等带 `-realtime` 后缀模型<br>　– ASR/TTS 模型（如 `Qwen-Audio-3.0-ASR-Flash-Streaming`, `CosyVoice`）仅在 AOQ/WebSocket 协议下可用 | • **广泛覆盖**：全量 Qwen 商业版、开源版及第三方直供模型<br>　– 文本：`qwen3.8-max`, `qwen3.7-plus`, `deepseek-v4-pro`, `glm-5.2`<br>　– 多模态：`qwen-vl-plus`, `qwen3.8-omni-flash`, `qwen2.5-vl`<br>　– 音频：`Qwen-Audio`（**仅 DashScope 原生接口支持**）<br>　– Agent：`qwen3.8-max` 等直供模型完整支持 Responses 接口工具调用 |
| **API 端点与协议** | • **协议层深度定制**：<br>　– AOQ（QUIC over UDP，弱网首选）<br>　– WebRTC（浏览器原生，免插件）<br>　– WebSocket（服务端集成友好）<br>• 端点示例：<br>　– `wss://dashscope.aliyuncs.com/api/v1/omni-realtime`（Omni Realtime）<br>　– `wss://dashscope.aliyuncs.com/api/v1/realtime`（通用 Realtime） | • **标准 HTTP RESTful**：<br>　– OpenAI 兼容：`POST /v1/chat/completions`<br>　– Anthropic 兼容：`POST /v1/messages`<br>　– DashScope 原生：`POST /api/v1/services/aigc/text-generation/generation`<br>• 全部支持 HTTPS + `Authorization: Bearer <API_KEY>` |
| **计费方式** | • **按实际消耗计量**：<br>　– 音频：按输入/输出秒数计费（ASR 秒数 + TTS 秒数）<br>　– 文本：按生成 token 计费（仅 LLM 部分）<br>　– 视觉：按单帧调用次数计费<br>• **会话时长不计费**，但超 10 分钟强制断连需重连（产生新会话） | • **按 token 精确计费**：<br>　– 输入 token + 输出 token（统一计价，无模态区分）<br>　– 多模态输入中，图像/视频按像素块（pixel block）折算为等效 token（如 `total_pixels=50176` ≈ 1568 tokens）<br>• 无连接时长、并发数等隐性费用 |
| **典型场景** | • 智能语音助手（实时打断、边说边想）<br>• 跨语言实时会议翻译（音视频双流同步）<br>• 远程医疗问诊（医生语音+患者检查图像实时分析）<br>• 游戏 NPC 语音交互（低延迟响应+声音复刻） | • 内容审核（批量图片/视频检测）<br>• 客服工单自动摘要（千条文本批量处理）<br>• 企业知识库问答（离线构建向量索引+批量召回）<br>• 代码生成与测试（CI/CD 流水线集成）<br>• AIGC 创作（批量生成图文/视频脚本） |

## 适用场景建议

### ✅ 优先选用实时推理（Realtime API）当：
- **延迟是硬约束**：端到端延迟需稳定 ≤ 800ms（AOQ 协议典型值），且用户对“思考停顿”敏感（如语音对话中等待超过 1.5 秒即感知卡顿）；
- **交互具有强状态依赖**：需维持多轮上下文、支持语音打断（VAD）、服务端主动触发音效/提示音（如“正在思考…”）；
- **输入天然为流式**：语音流、摄像头视频流、传感器数据流，无法预知总长度；
- **需多模态协同响应**：例如用户语音提问 + 实时拍摄图像，要求模型同步理解语音语义与图像内容并生成语音回答。

### ✅ 优先选用批量推理（Qwen API）当：
- **任务具备明确边界与可预测性**：输入数据已全部就绪（如上传完成的 PDF、截取的 10 张产品图、整理好的客服对话日志）；
- **追求确定性与可重入性**：需保证相同输入必得相同输出（用于审计、测试、A/B 实验），且支持失败重试、断点续跑；
- **吞吐量优先于单次延迟**：需每分钟处理数千条文本或数百张图像，可接受平均响应时间 2–5 秒；
- **需复杂后处理或工具链集成**：如调用 `web_search` 工具后解析结果、用 `code_interpreter` 执行 Python 脚本、将输出写入数据库或触发下游工作流。

### ⚠️ 明确不推荐的组合：
- ❌ 用批量 API 实现语音助手：`stream=true` 仅返回文本 delta，无法输出音频、无法响应中断、无 VAD 支持，用户体验断裂；
- ❌ 用实时 API 处理离线报告生成：会话 10 分钟上限导致长文档处理失败；无 `max_tokens` 等精细控制，易因超限中断；计费模型不经济（按秒计费 vs 按 token 计费）；
- ❌ 在 WebRTC 中调用 ASR 模型：WebRTC 协议明确不支持 ASR/TTS 类模型，必须切换至 AOQ 或 WebSocket。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 | 行动指引 |
|----------|-----------|-----------|-----------|
| **开发一款 iOS 语音记事本 App，支持说话实时转文字+高亮关键词** | `Realtime API` + **AOQ 协议** | AOQ 在弱网/移动网络下丢包率低于 WebSocket 30%，且原生支持 `Qwen-Audio-3.0-ASR-Flash-Streaming` 模型，提供毫秒级 ASR 结果流 | 1. 集成 AOQ iOS SDK<br>2. 调用 `/api/v1/realtime/token` 获取 `aoqTokenForClient`<br>3. 使用 `setAudioEncoderConfig` 设为 16kHz PCM<br>4. 监听 `asr.transcript` 事件获取实时文本 |
| **构建企业内部知识库问答机器人，支持上传 PDF/Word 并批量提取问答对** | `Qwen API` + **DashScope 原生接口** | DashScope 是唯一支持 `Qwen-VL` 系列模型处理文档图像的接口，且 `input` 字段可传入 PDF URL 或 base64 编码内容，`max_tokens=4096` 确保长文本摘要完整性 | 1. 使用 `POST /api/v1/services/aigc/multimodal-generation/generation`<br>2. `input` 中传入 `{"image": "data:application/pdf;base64,...", "text": "请提取所有问答对"}`<br>3. 设置 `parameters.max_tokens=4096` |
| **为客服系统增加“对话中实时推荐解决方案”功能，需结合当前对话文本+历史工单数据** | **混合架构**：<br>• 实时层：`Realtime API`（WebSocket）处理当前语音/文本流<br>• 批量层：`Qwen API`（Responses）异步调用知识库搜索工具 | 实时 API 保障对话流畅性；Responses 接口的 `previous_response_id` 和内置 `web_search` 工具可精准关联历史工单，避免实时会话中嵌入长上下文导致延迟飙升 | 1. 实时会话中监听 `response.text.delta` 渲染流式回复<br>2. 当用户发送完整问题后，后台发起 Responses 请求，`tools=[{"type":"web_search","query":"{当前问题} site:kb.example.com"}]`<br>3. 将搜索结果注入下一轮实时会话的 `system` 消息 |
| **需要生成 1000 条个性化营销短信，每条基于不同用户画像** | `Qwen API` + **OpenAI Chat 接口**（批量并发） | [OpenAI 兼容接口](../concepts/openai-compatible-api.md) SDK 生态成熟（Python/Node.js），支持 `asyncio` 并发请求；`temperature=0.3` 可控创意性，`max_tokens=128` 精确控制长度 | 1. 构建 1000 个 `messages` 数组，每个含 `system`（模板）+ `user`（用户画像）<br>2. 使用 `openai.AsyncOpenAI` 并发调用 `/v1/chat/completions`<br>3. 捕获 `rate_limit_exceeded` 错误并自动退避重试 |

> **重要提醒**：  
> - **不要混淆“流式响应”与“实时推理”**：Qwen API 的 `stream=true` 是 *响应传输方式*（减少前端等待），而 Realtime API 的流式是 *计算执行范式*（模型边接收边计算）。二者底层架构、计费、能力均不同。  
> - **声音复刻（Voice Cloning）仅 Realtime API 支持**：需提前上传参考音频生成 `voice_id`，批量 API 无此能力。  
> - **跨协议模型不可互换**：`qwen-omni-realtime` 无法在 Qwen API 调用；`qwen3.8-max` 无法在 Realtime API 加载。务必按文档标注的模型后缀与接口绑定关系选型。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [qwen api reference](../api/qwen-api-reference.md)


