# Qwen大模型、世界模型与决策模型能力对比

本对比旨在帮助开发者在百炼平台技术选型中，清晰识别 **Qwen 大模型**（通用多模态大语言模型）、**世界模型**（面向具身智能与环境推演的专用模型）与 **决策模型**（面向结构化判断的轻量级推理模型）三类能力的本质差异、适用边界与集成路径。随着智能体系统复杂度提升，单一模型难以兼顾泛化性、环境交互性与确定性决策需求。本文基于当前（2024年中）百炼平台正式开放能力，从接口协议、输入输出语义、计算范式和工程约束等维度展开客观对比，为构建分层智能体架构提供技术依据。

## 关键能力维度对比

| 维度 | Qwen 大模型 | 世界模型（HappyOyster 系列） | 决策模型（`decision-model-preview`） |
|------|-------------|------------------------------|-------------------------------------|
| **核心定位** | 通用多模态基础模型（LLM），支持理解、生成、推理、工具调用 | 专用世界建模模型，聚焦场景状态推演、任务调度与具身动作生成 | 轻量级结构化决策引擎，专注分类、是非判断与有序评分 |
| **输入格式** | 多样化：<br>• 文本对话数组（`messages`）<br>• 多模态混合内容（图像/音频/视频 URL 或 base64）<br>• 结构化 `input` 对象（DashScope 原生） | 严格 JSON 对象（`input`），结构依子模型类型而异：<br>• `adventure`: 场景描述 + 初始状态 + 推演目标<br>• `directing`: 多智能体角色定义 + 协作目标 + 约束条件<br>• `acting`: 当前观测 + 动作空间定义（邀测中） | 强结构化 JSON：<br>• `state`: 待决策原始数据（字符串/对象/数组）<br>• `questions`: 键值对集合，每个值含 `type`/`criteria`/`instructions` |
| **输出格式** | 自由文本为主，支持：<br>• 流式文本片段（`stream: true`）<br>• 强约束 JSON Schema 输出（`response_format`）<br>• 多模态结果（如视频理解摘要、代码执行结果） | 非流式完整响应：<br>• `adventure`: 推演路径、因果链、未来状态预测（文本）<br>• `directing`: 分步指令序列（JSON 数组）<br>• `acting`: 细粒度动作指令（JSON 对象，邀测中） | **纯结构化输出，无自由文本**：<br>• `choice`: `{selected: "A", probabilities: {"A": 0.82, "B": 0.15, ...}, confidence: 0.93}`<br>• `noul`: `{p_yes: 0.97, confidence: 0.89}`<br>• `score`: `{expected_score: 3.2, level_probabilities: [0.01, 0.12, 0.65, 0.22], confidence: 0.85}` |
| **支持模型** | `qwen3.8-max`, `qwen3.8-omni-flash`, `qwen-vl-plus`, `qwen-math`, `deepseek-v4-pro`, `glm-5.3` 等数十种文本/多模态/第三方模型 | `happyoyster-adventure`, `happyoyster-directing`, `happyoyster-acting`（后两者功能完备，`acting` 仍需白名单开通） | 仅 `decision-model-preview`（预览版，无版本别名或变体） |
| **API 端点（统一域名模式）** | • OpenAI Chat: `/compatible-mode/v1/chat/completions`<br>• Anthropic Messages: `/apps/anthropic/v1/messages`<br>• DashScope 原生: `/api/v1/services/aigc/multimodal-generation/generation` | `/api/v1/services/aigc/world-model/invoke`（旧域名兼容，但推荐新业务空间专属域名） | `/compatible-mode/v1/systemone`（TypeSafe System One 协议） |
| **计费方式** | 按 **输入 token + 输出 token** 计费（多模态按等效文本 token 折算）；视频/图像有像素级附加费用 | 按 **单次请求调用次数** 计费（不区分 token 数）；无流式计费项 | 按 **单次请求调用次数** 计费（与问题数量、选项规模无关）；无 token 计费概念 |
| **流式响应** | ✅ 全面支持（OpenAI Chat / Responses / Anthropic / DashScope） | ❌ 不支持（强制同步等待完整响应） | ❌ 不支持（返回即为最终结构化结果） |
| **典型场景** | • 智能客服多轮对话<br>• 多模态内容分析（图文报告生成、视频摘要）<br>• 工具增强型 Agent（联网搜索、代码执行）<br>• 创意写作与代码生成 | • 游戏 AI NPC 长期行为规划<br>• 工业仿真中设备故障传播推演<br>• 多机器人协同调度指令生成<br>• 具身智能体（Robot/VR）动作序列生成 | • 客服工单自动分级与路由（“紧急/高/中/低”）<br>• 内容安全审核（“违规/边缘/合规”+置信度）<br>• 智能体任务完成度校验（“未开始/进行中/基本完成/完全完成”）<br>• A/B 测试结果倾向性判断（P(胜出)） |

## 各方案适用场景建议

### ✅ 选择 Qwen 大模型，当您需要：
- **泛化性与创造力**：处理开放域问答、创意生成、跨模态理解等非结构化任务；
- **多轮交互与上下文记忆**：构建具备[长期记忆](../concepts/memory.md)、个性化风格的对话 Agent；
- **工具链集成**：依赖内置搜索、代码解释器、知识库检索等扩展能力；
- **多模态原生支持**：直接输入音视频文件并获取语义级理解结果（如“视频中人物情绪变化趋势”）。

> ⚠️ 注意：若业务对输出格式确定性要求极高（如必须返回 JSON），请启用 `response_format` 并配合 Schema 校验；避免将 Qwen 用于高频、低延迟、确定性优先的判断类任务（如实时风控规则引擎），其 token 成本与延迟远高于决策模型。

### ✅ 选择世界模型，当您需要：
- **环境动态建模**：在仿真、游戏、数字孪生等场景中，对物理/社会规则驱动的状态演化进行长程推演；
- **多智能体协作编排**：将高层目标（如“30分钟内完成仓库盘点”）自动分解为可执行的、带时序与资源约束的指令序列；
- **具身动作生成**：为机器人、虚拟化身等实体生成符合物理约束的细粒度操作指令（需开通 Acting 白名单）；
- **因果推理优先**：关注“如果…那么…”类反事实推演，而非单纯文本生成。

> ⚠️ 注意：世界模型不替代 LLM 的通用能力，而是作为 LLM 的“认知外挂”——典型架构为：Qwen 理解用户意图 → 调用世界模型推演环境状态 → Qwen 生成自然语言反馈。其输入需精心构造领域语义，非简单文本拼接。

### ✅ 选择决策模型，当您需要：
- **毫秒级结构化判断**：在 SLA < 500ms 的高并发场景（如 API 网关内容过滤）中，返回带概率分布的确定性答案；
- **可解释性与可控性**：下游系统需基于置信度做阈值拦截（如 `confidence < 0.85` 时转人工）、或基于概率分布做加权决策；
- **零文本生成开销**：无需任何解释性文字，只关心“选哪个”、“是不是”、“打几分”；
- **标准化决策流水线**：将工单、日志、用户行为等异构 `state` 映射到统一 `questions` 模板，实现跨业务决策逻辑复用。

> ⚠️ 注意：决策模型 **不支持** 自由文本生成、多轮对话、工具调用或任何形式的 reasoning trace。若需“为什么选 A？”的解释，请由 Qwen 模型基于决策结果二次生成，而非强求决策模型输出文本。

## 技术选型参考指南（面向开发者）

| 您的问题 | 推荐模型 | 理由说明 |
|----------|-----------|-----------|
| “如何根据用户上传的故障视频，自动生成维修建议报告？” | ✅ Qwen（`qwen3.8-omni-flash`） | 需视频理解 + 文本生成 + 可能调用知识库，属典型多模态生成任务 |
| “在自动驾驶仿真中，预测前方交叉口 10 秒内所有车辆可能的轨迹组合？” | ✅ 世界模型（`happyoyster-adventure`） | 强依赖物理规则建模与长程状态推演，非文本生成问题 |
| “每条客服对话消息，实时判断是否需升级至专家坐席（是/否/不确定）？” | ✅ 决策模型（`decision-model-preview`） | 低延迟、二元判断、需置信度用于降级策略，完美匹配其设计范式 |
| “让 AI 主持一场 30 分钟的线上技术分享，实时响应观众提问并演示代码？” | ✅ Qwen（`qwen3.8-max` + 工具链） | 需多轮对话管理、代码执行、知识检索，世界模型与决策模型均无法支撑 |
| “将‘优化仓储拣货路径’这一目标，分解为 5 台 AGV 的具体移动指令序列？” | ✅ 世界模型（`happyoyster-directing`） | 属多智能体任务调度，需输出结构化、有时序依赖的指令数组 |
| “对 10 万条用户评论批量打标：情感极性（正面/中性/负面）及置信度？” | ✅ 决策模型（`decision-model-preview`） | 高吞吐、结构化输出、需概率分布做质量监控，Qwen 成本过高且不可控 |

> 💡 **最佳实践提示**：  
> - **分层架构更健壮**：生产级智能体常组合使用三者——用决策模型做入口路由（“该请求走 Qwen 还是世界模型？”），用 Qwen 做用户交互与工具协调，用世界模型处理底层环境推演。  
> - **性能压测必做**：Qwen 的 `max_tokens` 实际影响显著（尤其多模态）；世界模型对 `input` 长度敏感（≤8192 tokens）；决策模型虽快，但 `questions` > 16 个时延迟明显上升。  
> - **调试优先使用 Playground**：Qwen 用 [百炼 Playground](https://bailian.console.aliyun.com/playground)；世界模型用 [Adventure Playground](https://bailian.console.aliyun.com/happyoyster_adventure_playground)；决策模型用 [SystemOne Playground](https://bailian.console.aliyun.com/systemone_playground) —— 可视化验证输入结构与输出语义。  
> - **SDK 选型建议**：Qwen 优先用 OpenAI SDK（兼容性好）；世界模型用原生 `requests` 或封装好的 `worldmodel-sdk`；决策模型**必须使用 `typesafe-sdk`**（自动处理 TypeSafe 协议解析）。  

通过明确三类模型的能力边界与成本特征，开发者可避免“用大炮打蚊子”或“用螺丝刀拧螺母”的误配，构建出高性能、低成本、可维护的下一代 AI 应用。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


