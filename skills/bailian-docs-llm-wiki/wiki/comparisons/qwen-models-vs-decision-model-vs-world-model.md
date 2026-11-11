# 通义千问基础模型、决策模型与世界模型对比

本文旨在帮助开发者清晰理解百炼平台上三类核心 AI 能力——**通义千问基础模型（Qwen）**、**决策模型（Decision Model）** 和 **世界模型（World Model）** 的定位差异、能力边界与技术适配要点。随着大模型应用从通用对话向垂直场景深度演进，单一“文本生成”范式已无法满足工单路由、内容审核、游戏叙事、智能体编排等高确定性、强结构化或强状态感知的需求。本对比聚焦实际工程落地维度，涵盖协议设计、输入输出语义、调用约束及成本特征，为技术选型提供可操作的决策依据。

## 关键维度对比

| 维度 | 通义千问基础模型（Qwen） | 决策模型（Decision Model） | 世界模型（World Model） |
|------|--------------------------|----------------------------|---------------------------|
| **核心定位** | 通用大语言模型（LLM），支持多轮对话、代码、数学、多模态理解与生成 | 专用结构化推理模型，不生成文本，专注分类/是非/评分三类确定性决策 | 专用叙事与场景建模模型，面向动态世界状态演化（冒险、导演、角色行为） |
| **输入格式** | 多样化：<br>• OpenAI：`messages` 数组（含 `system`/`user`/`assistant`）<br>• Anthropic：`messages` + `system` 字符串/数组<br>• DashScope：`input`（字符串或结构化对象）<br>• 支持图像/音频/视频（Base64 或 URL） | 严格结构化：<br>• `state`：原始上下文（字符串/JSON/数组，序列化后送入）<br>• `questions`：对象字典，每个问题含 `type`（`choice`/`noul`/`score`）、`instructions`、`criteria`（格式强校验） | 模型专属结构：<br>• `input` 为 JSON 对象，字段依子模型而异：<br> - Adventure：`scene_state`, `user_action`, `history` 等<br> - Directing：`scene_context`, `camera_requirements`, `character_states` 等<br> - Acting：`character_profile`, `emotion_state`, `dialogue_input` 等 |
| **输出格式** | 自由文本生成为主（`content` 字段），支持流式（`stream: true`）；部分协议返回工具调用请求（`tool_calls`）、思考过程（`reasoning` 块） | **纯结构化 JSON**，无自由文本：<br>• `choice`: `{ "selected": "option_a", "probabilities": {"a":0.82,"b":0.18}, "confidence": 0.93 }`<br>• `noul`: `{ "probability_yes": 0.97, "confidence": 0.95 }`<br>• `score`: `{ "expected_score": 3.25, "probabilities": [0.05,0.15,0.65,0.15], "confidence": 0.89 }` | 混合格式：<br>• Adventure：`output.text`（故事文本）+ `output.branches`（分支选项）<br>• Directing：`output.directives`（结构化指令数组，如镜头切换、光照调整）<br>• Acting：`output.behavior`（动作/微表情描述）+ `output.emotion_delta`（情绪变化值）<br>• **默认启用流式响应（Adventure）**，Directing/Acting 可选 |
| **支持模型** | 全系列 Qwen（`qwen4-max-preview`, `qwen3.8-max`, `qwen3-vl-plus`, `qwen3.8-omni-flash` 等）+ Qwen-Coder/Qwen-Audio/Qwen-Math + 第三方模型（DeepSeek/Kimi/GLM/MiniMax） | 仅 `decision-model-preview`（当前唯一且固定） | 仅 HappyOyster 系列：<br>• `happyoyster-adventure`<br>• `happyoyster-directing`<br>• `happyoyster-acting`（邀测中） |
| **API 端点（Base URL + Path）** | • OpenAI 兼容：<br> `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br> `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses`<br>• Anthropic 兼容：<br> `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages`<br>• DashScope 原生：<br> `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation` | `/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`（TypeSafe System One 协议） | `https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model`（统一入口，`model` 参数区分子模型） |
| **计费方式** | 按 **输入 Token + 输出 Token** 计费（单位：千 Token），不同模型单价不同；多模态输入（图/音/视）按等效文本 Token 折算；缓存命中（`cache_control`）可降低输入费用 | 按 **单次请求** 计费（非 Token），与问题数量、`state` 长度正相关；无输出 Token 成本；高并发下具备显著成本优势 | 按 **输入 Token + 输出 Token** 计费，与 Qwen 基础模型同价体系；Adventure 流式响应按实际返回 Token 计费；Directing/Acting 因输出结构化程度高，平均 Token 消耗低于同等复杂度文本生成 |
| **典型场景** | • 客服对话机器人<br>• 文档摘要与问答<br>• 代码生成与解释<br>• 多模态内容理解（图文检索、音视频分析）<br>• 工具增强型智能体（联网搜索、代码执行） | • 工单自动分派（选择处理团队）<br>• 内容安全审核（是否违规、严重等级打分）<br>• 智能体任务路由（判断下一步执行哪个子技能）<br>• 用户意图完成度校验（是/否已完成目标） | • 交互式文字冒险游戏（动态生成剧情与分支）<br>• 虚拟制片预演（自动生成分镜脚本与镜头调度）<br>• 游戏 NPC 行为引擎（驱动角色实时反应与情绪表达）<br>• 教育模拟场景（如医疗问诊、危机谈判） |

## 各方案适用场景建议

### ✅ 选择通义千问基础模型，当：
- 任务本质是**开放生成、知识问答或复杂推理**（如写报告、解数学题、分析长文档）；
- 需要**多轮上下文记忆与自然语言交互**（如客服、助教）；
- 依赖**工具调用能力**（如实时搜索、执行代码、调用外部 API）；
- 输入/输出需**灵活支持多模态**（上传图片提问、分析视频关键帧）；
- 团队已有 OpenAI/Anthropic SDK 生态，追求**协议兼容性与迁移成本最低**。

### ✅ 选择决策模型，当：
- 业务逻辑要求**毫秒级响应、100% 结构化输出、零文本歧义**；
- 核心指标是**分类准确率、置信度阈值、决策一致性**（如金融风控、合规审核）；
- 需要**并行评估多个独立问题**（如一份工单同时判断：紧急度、所属部门、是否需人工复核）；
- 对延迟敏感且**拒绝任何“幻觉”风险**（不能接受模型编造答案）；
- 愿意为确定性付出**额外 schema 设计与 criteria 维护成本**。

### ✅ 选择世界模型，当：
- 构建的是**状态持续演化的交互式体验**（游戏、仿真、培训），而非单次问答；
- 需要模型**主动管理场景变量、角色状态、时间线与因果链**；
- 输出需**兼具叙事连贯性与可执行指令性**（如既生成一段剧情，又明确告诉渲染引擎“镜头拉远，聚焦左侧门”）；
- 接受**会话状态由客户端显式维护**（通过 `session_id` 或 `history` 字段传递）；
- 场景复杂度超出 LLM 的隐式状态跟踪能力，需要**专用建模层抽象**。

## 技术选型参考（致开发者）

| 选型考量 | Qwen 基础模型 | 决策模型 | 世界模型 |
|----------|----------------|------------|------------|
| **开发上手难度** | ⭐⭐⭐⭐☆（协议熟悉即可，SDK 支持完善） | ⭐⭐☆☆☆（需精读 `questions.criteria` 规范，schema 错误直接 400） | ⭐⭐⭐☆☆（子模型 `input` 结构差异大，需分别对接） |
| **调试可观测性** | 高（完整 token 统计、reasoning 日志、工具调用 trace） | 极高（所有结果附带 `probabilities` + `confidence` + `latency_ms` + `input_tokens`） | 中（Adventure 流式日志丰富；Directing/Acting 结构化输出易解析但 debug 信息较少） |
| **扩展性** | 强（支持插件、RAG、自定义工具、多模态扩展） | 弱（能力固化，仅支持三类问题，不可扩展新决策类型） | 中（子模型可独立升级，但跨模型协同需业务层编排） |
| **稳定性与 SLA** | 高（全链路重试、熔断、缓存，SLA 99.95%） | 极高（无文本生成环节，计算路径确定，P99 延迟 < 150ms） | 中（Adventure 流式对网络抖动敏感；Acting 邀测期 SLA 未公开） |
| **推荐首发验证路径** | 用 `qwen3.5-flash` 快速验证对话/摘要效果 → 切换 `qwen3.8-max` 提升质量 | 用 1 个 `choice` 问题 + 3 个选项最小闭环验证 → 扩展至 `noul`+`score` 多问题组合 | 从 Adventure 单场景开始（如“森林迷路”）→ 加入 `branching` 控制逻辑 → 集成 Directing 生成镜头指令 |

> **重要提醒**：  
> - **不要混用协议与模型**：Qwen-Audio 仅支持 DashScope 协议；QwQ/QVQ 模型禁用 `system` 消息；决策模型必须使用 `systemone` endpoint；世界模型不可用 OpenAI 兼容路径。  
> - **地域与域名强绑定**：三方模型（Kimi/DeepSeek）仅限华北2；世界模型 endpoint 为 `dashscope.aliyuncs.com`，与其他模型的 Workspace 专属域名不同。  
> - **成本优化提示**：对决策类任务强行使用 Qwen 生成 JSON 将导致 Token 浪费与解析开销；对叙事类任务使用决策模型则完全无法建模状态演化。**选型错误比模型调优带来的成本增幅更高。**  

请根据业务问题的本质（生成？决策？演化？）而非技术惯性进行选型。百炼平台的设计哲学是：**让每类问题匹配最合适的“思维引擎”，而非用一把锤子敲所有钉子。**

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [decision model](../api/decision-model.md)
- [world model api reference](../api/world-model-api-reference.md)


