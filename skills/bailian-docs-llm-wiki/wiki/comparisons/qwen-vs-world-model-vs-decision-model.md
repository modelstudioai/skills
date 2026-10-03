# Qwen大模型、World Model与Decision Model对比

本文旨在帮助开发者在百炼平台上进行技术选型时，清晰理解三类核心能力模型的定位差异、能力边界与适用场景。Qwen大模型代表通用多模态生成能力，World Model聚焦具身智能与动态环境建模，而Decision Model则专为确定性结构化决策任务设计。三者并非替代关系，而是面向不同抽象层级（生成 → 推演 → 判定）的互补能力组件。本对比基于当前（2024年Q3）百炼平台正式可用的API能力，涵盖协议兼容性、输入输出范式、部署约束及工程实践要点。

## 关键维度对比

| 维度 | Qwen大模型 | World Model | Decision Model |
|------|-------------|--------------|----------------|
| **核心定位** | 通用大语言/多模态基础模型，支持开放式文本生成、理解与工具调用 | 面向具身智能的动态世界建模引擎，支持环境状态演化、角色行为推演与多智能体协同 | 轻量级结构化决策推理模型，仅输出分类、是非判断或有序评分及其概率分布 |
| **输入格式** | 多样化：<br>• OpenAI `/chat/completions`：`messages` 数组（含 `text`/`image_url`/`video` 块）<br>• `/responses`：支持扁平字符串或 `EasyInputMessage`<br>• Anthropic：`role`+`content`（支持 `image`/`video` 块）<br>• DashScope：按服务类型区分（`text-generation`/`multimodal-generation`） | 结构化 JSON：<br>• 必填 `scene_id`（预注册场景ID）<br>• `context_window`（可选）<br>• `enable_state_tracking`（可选）<br>• 输入内容嵌入请求体，无标准消息数组结构 | 严格结构化 JSON：<br>• 必填 `state`（文本/JSON对象/数组）<br>• 必填 `questions`（键值对，每个值含 `type`/`instructions`/`criteria`）<br>• `model` 固定为 `"decision-model-preview"` |
| **输出格式** | 文本为主，支持流式响应：<br>• OpenAI/Anthropic：标准 `choices[0].message.content` + `tool_calls`<br>• `/responses`：含 `previous_response_id` 支持上下文链路<br>• DashScope：`output.text` + `output.choices` | 同步非流式 JSON：<br>• `state_id`（用于状态追溯）<br>• `next_action`（动作指令）<br>• `world_state_snapshot`（可选，当 `enable_state_tracking=true`）<br>• **不支持流式响应（`stream` 参数强制忽略）** | 纯结构化非文本输出：<br>• 每个 `question_id` 对应一个答案对象：<br> – `choice`: `{ "choice": "A", "probabilities": {"A": 0.82, "B": 0.15}, "confidence": 0.93 }`<br> – `noul`: `{ "probability_yes": 0.76, "probabilities": {"yes": 0.76, "no": 0.18, ...}, "confidence": 0.89 }`<br> – `score`: `{ "expected_score": 2.25, "probabilities": [0.1, 0.65, 0.22, 0.03], "confidence": 0.91 }`<br>• **零文本生成，无 `content` 字段** |
| **支持模型** | • 文本：`qwen3.8-max`、`qwen3.7-plus`、`qwen-turbo`、`qwen-coder-next` 等<br>• 多模态：`qwen3.8-omni-flash`、`qwen3-vl-plus`、`QVQ`<br>• 第三方直供：DeepSeek-v4、Kimi-k3、GLM-5.3、MiniMax-M2.5（限华北2） | • `HappyOyster-Adventure`（开放世界演化）<br>• `HappyOyster-Directing`（多角色叙事调度）<br>• `HappyOyster-Acting`（单角色实时行为，邀测中） | • 仅 `decision-model-preview`（预览版），无其他型号 |
| **API 端点（华北2示例）** | • OpenAI Chat：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• OpenAI Responses：`/compatible-mode/v1/responses`<br>• Anthropic：`/apps/anthropic/v1/messages`<br>• DashScope：`/api/v1/services/aigc/text-generation/generation` 等 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/v1/world-model/adventure`<br>`/v1/world-model/directing`<br>`/v1/world-model/acting`（邀测） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone` |
| **计费方式** | 按 **输入 token + 输出 token** 计费（单位：千token）<br>• 多模态输入按等效文本 token 折算（如图像按分辨率/帧数折算）<br>• `/responses` 中思考 token 单独计费（需显式配置） | 按 **每次请求（per call）** 计费<br>• 与输入长度、输出复杂度无关<br>• 不区分 token，统一单价 | 按 **每次请求（per call）** 计费<br>• 与 `state` 长度、`questions` 数量、输出等级数均无关<br>• 成本恒定，适合高并发场景 |
| **典型场景** | • 智能客服对话生成<br>• 多模态内容理解（图文问答、视频摘要）<br>• 工具增强型应用（联网搜索、代码执行）<br>• AI 编程助手、创意文案生成 | • 游戏NPC行为仿真与剧情驱动<br>• 教育沙盒模拟（物理实验、历史事件推演）<br>• 影视分镜自动编排与角色调度<br>• 工业数字孪生中的设备交互推演 | • 工单智能分流（→ 技术/售后/合规团队）<br>• 内容安全审核（涉政/暴恐/违禁分级）<br>• 智能体路由决策（选择下一步调用哪个Agent）<br>• A/B测试结果置信度校验 |

## 各方案的适用场景建议

### ✅ 选择 Qwen大模型 当：
- 任务需要**开放式文本生成、自由问答或创造性输出**（如写诗、编故事、生成报告）；
- 输入包含**图像、音频、视频等多模态数据**，且需跨模态理解（如“分析这张财报截图并总结风险点”）；
- 应用需集成**外部工具能力**（如实时搜索、运行Python代码、调用API）；
- 场景对**上下文长度、多轮对话连贯性、流式响应体验**有较高要求；
- 开发团队已熟悉 OpenAI 或 Anthropic 生态，希望复用现有 SDK 和[提示工程](../concepts/prompt-engineering.md)经验。

### ✅ 选择 World Model 当：
- 构建**具身智能系统**（如机器人控制、虚拟人交互、游戏AI），需建模“环境状态如何随动作变化”；
- 需要**长周期、多步骤因果推演**（如：“若用户点击按钮A，NPC会如何反应？3步后场景状态为何？”）；
- 设计**多角色协同叙事系统**（如影视剧本生成、教育对话模拟），强调角色一致性与事件逻辑链；
- 场景具备明确的**预定义场景ID（`scene_id`）和状态生命周期管理需求**（如30分钟自动清理）；
- 可接受**同步阻塞调用、无流式响应、更高单次延迟**，以换取强状态一致性保障。

### ✅ 选择 Decision Model 当：
- 业务逻辑本质是**确定性分类/打分/二元判断**（如“是否违规？”、“严重度1–4级？”、“分配至哪个部门？”）；
- 对**延迟敏感、需高并发低抖动**（如每秒处理数千工单），且不能容忍生成式模型的不确定性延迟；
- 要求**可解释性与置信度量化**（如返回各选项概率、整体置信分数），用于下游阈值控制或贝叶斯融合；
- 输入上下文虽长（≤65536 token），但**只需一次前向计算完成全部问题联合推理**，无需分步生成；
- 团队希望**规避文本生成幻觉风险**，确保输出始终是结构化、可验证、可审计的决策结果。

## 面向开发者的选型参考

- **不要用 Qwen 替代 Decision Model**：即使 Qwen 能通过 [prompt](../guides/prompt.md) 实现类似分类，其输出不可控、成本随输出长度增长、无内置概率分布、无法保证确定性，不适用于 SLA 严格的决策流水线。
  
- **World Model 不是“更强的 Qwen”**：它不擅长自由文本生成，也不支持工具调用；其价值在于状态演化建模能力。若只需回答问题或生成文案，请优先使用 Qwen。

- **组合使用是最佳实践**：  
  ▶ 典型架构：`用户输入 → Qwen（理解与摘要） → Decision Model（路由决策） → World Model（执行推演） → Qwen（生成自然语言反馈）`  
  ▶ 示例：智能客服中，Qwen 解析用户问题 → Decision Model 判断是否需转人工/升级 → 若需推演解决方案，则调用 World Model 模拟处置流程 → 最终由 Qwen 将推演结果转化为用户可读回复。

- **工程注意事项**：  
  • Qwen 的 `max_tokens` 在不同协议下语义不同（尤其 `/responses` vs Anthropic），务必查阅对应协议文档；  
  • World Model 的 `scene_id` 必须提前注册，且状态超时（30分钟）后需重建，不适合无状态短连接场景；  
  • Decision Model 的 `questions` 建议 ≤16 个，`score` 等级强烈推荐 3–7 级——超出将显著降低 `confidence` 可靠性；  
  • 所有模型均需通过业务空间专属域名访问，`{WorkspaceId}` 须从百炼控制台获取，不可硬编码。

> 提示：首次集成建议从 Decision Model 入手——接口最简洁、成本最低、效果最确定；再逐步引入 Qwen 实现表达层，最后按需扩展 World Model 构建智能体行为层。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


