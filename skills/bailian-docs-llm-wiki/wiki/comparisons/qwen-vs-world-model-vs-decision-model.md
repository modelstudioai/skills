# Qwen 大模型、World Model 与 Decision Model 对比

为帮助开发者在百炼平台中快速识别并选用最匹配业务需求的 AI 能力，本文对三类核心模型服务——**Qwen 大模型（通用大语言模型）**、**World Model（叙事与交互式内容生成专用模型）** 和 **Decision Model（结构化决策推理模型）** 进行系统性对比分析。三者定位迥异：Qwen 是通用智能底座，World Model 聚焦多模态叙事编排，Decision Model 专精确定性结构化判断。选型不当易导致性能浪费、延迟超标或语义失准。本对比基于当前（2024年Q4）百炼平台正式可用能力，覆盖协议设计、能力边界、工程约束与典型落地路径。

## 关键维度对比

| 维度 | Qwen 大模型 | World Model | Decision Model |
|------|-------------|-------------|----------------|
| **核心定位** | 通用大语言模型（LLM），支持文本生成、多模态理解、工具调用与复杂推理 | 专用世界建模引擎，面向动态世界观构建、角色行为编排与沉浸式内容生成 | 轻量级结构化决策模型，输出分类/是非/评分三类确定性结果，**不生成自然语言** |
| **输入格式** | 多样化：<br>• 文本（`messages` / `input`）<br>• 图像/视频/音频（URL 或 base64，依模型支持）<br>• 工具调用请求（`tool_choice`, `tools`）<br>• 上下文状态（`previous_response_id`, `conversation`） | JSON 结构化对象：<br>• `model`（固定值如 `"happyoyster/adventure"`）<br>• `input`（类型强绑定：`setting`+`characters` for Adventure；`scene_script`+`camera_angles` for Directing）<br>• `parameters`（深度/时长等控制参数） | JSON 结构化对象：<br>• `state`（原始业务上下文，文本/JSON/数组）<br>• `questions`（键值对集合，每个含 `type`、`instructions`、`criteria`）<br>• 无自由文本 prompt 字段 |
| **输出格式** | 自然语言为主，支持：<br>• 流式 token（`text/event-stream`）<br>• 结构化 JSON（Anthropic `output_config.format: "json"`）<br>• 工具调用响应（`tool_calls`）<br>• 使用统计（`usage`） | JSON 格式，严格 Schema 化：<br>• `adventure`：返回 `world_graph`, `character_relations`, `branch_points` 等字段<br>• `directing`：返回 `shot_list`, `timing_map`, `character_actions`<br>• `acting`（邀测）：返回 `emotion_state`, `dialogue_refinement`, `gesture_sequence` | 纯结构化 JSON，**零文本生成**：<br>• `choice`：`{"selected": "option_a", "probabilities": {"option_a": 0.82, ...}, "confidence": 0.93}`<br>• `noul`：`{"p_yes": 0.71, "confidence": 0.88}`<br>• `score`：`{"expected_score": 2.43, "probabilities": [0.05, 0.32, 0.51, 0.12], "confidence": 0.91}` |
| **支持模型** | • Qwen 系列：`qwen3.8-max`, `qwen3.7-plus`, `qwen3-vl-plus`, `qwen3-coder-flash` 等<br>• 开源模型：`qwen3.5-397b-a17b`, `qwen3.8-27b`<br>• 第三方模型：`deepseek-v4.1-flash-1017`, `kimi-k3.1-pro`, `glm-5.3` | • 单一模型族：`happyoyster/adventure`, `happyoyster/directing`, `happyoyster/acting`（邀测）<br>• 无第三方模型接入，无版本迭代标识（如 v1.2/v1.3）仅接口路径差异 | • 唯一模型：`decision-model-preview`（预览版，暂无其他型号）<br>• 模型能力由 `questions.type` 动态决定，非模型实例切换 |
| **API 端点** | 多协议共存：<br>• OpenAI 兼容：`/compatible-mode/v1/chat/completions`（Chat）<br>• `/compatible-mode/v1/responses`（增强 Agent）<br>• Anthropic 兼容：`/apps/anthropic/v1/messages`<br>• DashScope 原生：`/api/v1/services/aigc/.../generation` | 统一 RESTful 端点：<br>• `POST https://dashscope.aliyuncs.com/api/v1/world-model`<br>• **不支持兼容协议**，无 OpenAI/Anthropic 适配层 | 统一 TypeSafe System One 端点：<br>• `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`<br>• SDK 封装为 `client.decision.create()`（Python）或 `client.system_one(...)`（TypeSafe） |
| **计费方式** | • 按 **输入 tokens + 输出 tokens** 计费<br>• 多模态输入按像素/帧数折算为 tokens（如 `video_url` 按 `fps × duration × resolution_factor` 计费）<br>• 工具调用（`web_search`, `code_interpreter`）单独计费 | • 按 **单次 API 请求** 计费（无论输入长度或输出复杂度）<br>• `adventure`/`directing` 同价；`acting` 邀测期免费，正式商用将独立定价 | • 按 **单次请求 + 问题数量** 计费<br>• 每个 `questions` 条目计为 1 个决策单元<br>• `state` 长度不影响单价，但超限（65536 tokens）直接拒绝 |
| **典型场景** | • 智能客服对话<br>• 多文档摘要与问答<br>• 代码生成与解释<br>• 图文/音视频内容理解与创作<br>• Agent 自主规划与工具执行 | • 游戏剧情动态生成与分支管理<br>• 虚拟制片分镜脚本自动生成<br>• 互动小说世界观初始化与一致性校验<br>• AI 导演辅助镜头调度（Directing）<br>• 角色实时情绪驱动表演（Acting，邀测） | • 工单自动分级与路由（如“紧急/高/中/低”）<br>• 内容安全审核（“违规/边缘/合规”三档概率）<br>• 智能体任务完成度判定（“未开始/进行中/基本完成/完全完成”）<br>• 客服会话意图置信度打分（用于人工介入阈值） |

## 各方案适用场景建议

- **选择 Qwen 大模型，当您需要**：  
  ✅ 生成连贯、富有创造性的自然语言（如文案、故事、邮件）；  
  ✅ 理解并推理多模态输入（图像描述、视频摘要、语音转写）；  
  ✅ 构建具备自主工具调用能力的 AI Agent（如搜索+计算+文件分析）；  
  ❌ 不适合：对延迟极度敏感（>500ms）、需 100% 确定性输出、或禁止任何文本生成的合规场景。

- **选择 World Model，当您需要**：  
  ✅ 在游戏、影视、教育等垂直领域构建**可演进、可交互的虚拟世界**；  
  ✅ 实现角色驱动的叙事逻辑（而非单轮问答），且需保证多角色行为一致性；  
  ✅ 将导演意图（如“紧张感递增”、“特写切近景”）转化为可执行的镜头序列；  
  ❌ 不适合：通用问答、知识检索、代码编写等非叙事类任务；也**不适用于无明确创作范式（如冒险/导演/表演）的业务**。

- **选择 Decision Model，当您需要**：  
  ✅ 在毫秒级内完成高置信度结构化判断（P95 延迟 < 300ms）；  
  ✅ 输出可被下游系统直接解析的概率分布（用于 A/B 测试、阈值熔断、不确定性加权）；  
  ✅ 规避 LLM 的幻觉风险，确保“工单是否升级”“内容是否涉政”等关键决策有明确数学依据；  
  ❌ 不适合：需要解释性文本（如“为什么判为违规？”）、开放性生成、或涉及复杂上下文推理（如跨多轮对话的状态聚合）。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **已有 OpenAI SDK 且需最小改造上线** | ✅ Qwen（OpenAI 兼容 Chat/Responses） | 直接复用 `openai` Python 包，仅需替换 `base_url` 和 `api_key`；Responses API 内置工具链大幅降低 Agent 开发成本。 |
| **需严格控制首字节延迟（<200ms）且输出为离散标签** | ✅ Decision Model | 无文本生成开销，纯向量化推理；SDK 提供 `latency_ms` 字段便于监控 SLA；`confidence` 字段天然支持灰度发布。 |
| **构建互动叙事产品（如文字冒险游戏、AI 剧本助手）** | ✅ World Model（Adventure + Directing） | 专为叙事状态机设计，`world_id` 支持客户端维护长程一致性；`max_world_depth` 等参数提供可控的复杂度调节能力。 |
| **需同时处理图文+语音+文本，并生成带引用的报告** | ✅ Qwen（DashScope 原生协议 + `qwen3-vl-plus`） | 唯一支持 `input_audio` + `image_url` + `messages` 混合输入的协议；`file_search` 工具可直接关联上传文档。 |
| **要求输出符合 JSON Schema 且避免任何自由文本** | ⚠️ Qwen（Anthropic Messages + `output_config.format: "json"`）<br>✅ Decision Model（原生结构化） | Qwen 的 JSON 模式需额外提示词约束且存在越界风险；Decision Model 的输出 Schema 由模型强制保证，无需后处理校验。 |
| **预算敏感，需最大化 tokens 利用率** | ✅ Decision Model（按问题计费）<br>⚠️ Qwen（按 tokens 计费，长输出成本高） | Decision Model 单次请求 16 个问题成本≈Qwen 生成 200 tokens；World Model 按请求计费，适合低频高价值生成。 |

> **重要提醒**：  
> - World Model 当前为**邀测服务**，需在百炼控制台提交申请并通过审核方可调用；  
> - Decision Model 为 `preview` 版本，接口与能力可能随小版本迭代调整，请关注 `dashscope` SDK 更新日志；  
> - Qwen 的 `max_tokens` 行为因协议与模型而异（如 Anthropic 中限制“思考+回复”总长），务必在压测中验证实际输出长度。  

通过以上对比，开发者可依据自身业务的**输出形态（文本/结构化/多模态）**、**实时性要求（延迟容忍度）**、**确定性等级（是否允许幻觉）** 及**工程成熟度（SDK 支持、协议迁移成本）**，做出精准技术选型。百炼平台持续演进，三类模型能力边界亦将动态融合（如未来 Qwen 可能集成轻量 World Model 模块），建议定期查阅各模块最新 API 文档与 Release Notes。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


