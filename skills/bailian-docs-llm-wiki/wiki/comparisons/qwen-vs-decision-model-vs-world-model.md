# Qwen大模型、决策模型与世界模型能力对比

## 背景与目的  
在百炼平台日益丰富的AI能力矩阵中，Qwen大模型、决策模型（Decision Model）与世界模型（World Model）分别面向**通用智能生成**、**确定性结构化判断**和**交互式叙事建模**三大范式。开发者常面临选型困惑：何时用Qwen做自由推理？何时该切换至轻量决策接口以保障低延迟与可解释性？又在何种游戏/剧情场景下必须依赖世界模型的多层级状态演化能力？本页旨在从技术协议、能力边界、部署约束与业务语义四个维度进行横向对比，为架构设计与API集成提供清晰、可落地的技术选型依据。

---

## 关键能力维度对比

| 维度 | Qwen大模型（API） | 决策模型（Decision Model） | 世界模型（World Model） |
|------|-------------------|----------------------------|--------------------------|
| **核心定位** | 通用大语言模型能力平台，支持文本、代码、多模态、Agent工具调用等广谱任务 | 专用结构化决策引擎，输出分类/是非/评分三类确定性结果，**不生成自由文本** | 面向交互叙事的多模态世界状态建模系统，支持剧情演进、镜头调度、角色行为三级控制 |
| **输入格式** | 灵活：`messages`（对话数组）、`input`（纯文本或结构化对象）、多模态内容（图像URL/视频base64/音频二进制）；支持`state`上下文缓存（Responses API） | 严格结构化：`state`（原始上下文，JSON/object/array）、`questions`（含`type`/`criteria`的键值对集合） | 强约束结构化：`world_state`（必填JSON对象，描述当前世界快照）、`context_window`（token数）、模型特有字段（如`character_id`） |
| **输出格式** | 自由文本为主，支持流式`text/event-stream`；Anthropic Messages API可强制JSON Schema输出；Responses API返回含`tool_calls`的完整Agent响应 | **纯结构化**：仅返回`answers`（含`choice`/`noul_score`/`score_expectation`等）、`confidence`、`probabilities`；无`text`/`content`字段 | 结构化JSON：含`next_world_state`（更新后的世界状态）、`narrative_actions`（动作指令列表）、`reasoning_trace`（可选推理路径）；不返回自然语言段落 |
| **支持模型** | 全系列Qwen（`qwen3.8-max`, `qwen3-vl-plus`, `qwen3.8-omni-flash`等）、第三方模型（DeepSeek/GLM/Kimi/MiniMax，限华北2地域） | 仅`decision-model-preview`（预览版），无历史版本或别名 | HappyOyster系列：`adventure`（剧情演进）、`directing`（镜头调度）、`acting`（角色行为，邀测中） |
| **API端点（典型）** | • OpenAI兼容：`/compatible-mode/v1/chat/completions`<br>• Responses（Agent增强）：`/compatible-mode/v1/responses`<br>• Anthropic兼容：`/apps/anthropic/v1/messages`<br>• DashScope原生：`/api/v1/services/aigc/text-generation` | `/compatible-mode/v1/systemone`（TypeSafe System One 协议） | • Adventure：`/api/v1.1/adventure/step`<br>• Directing：`/api/v1.1/directing/generate`<br>• Acting：`/v1.2/acting/generate`（邀测，版本独立） |
| **计费方式** | 按**输入+输出Token总数**计费（不同模型单价不同），多模态输入按像素/帧数折算Token；流式响应按实际返回Token结算 | 按**单次请求**计费（无论`questions`数量），费用固定，与`state`长度、问题复杂度无关 | 按**单次请求**计费（Adventure/Directing统一单价），Acting模型暂未公开计费策略（邀测期免费） |
| **典型场景** | 客服对话、报告生成、代码补全、知识库问答、多模态理解（图文/音视频分析）、Agent自动化流程 | 工单自动分派（选择处理团队）、内容安全审核（是否违规）、智能体路由（选择下一步工具）、规则合规校验（是否满足X条件） | 游戏剧情动态生成、互动小说分支决策、虚拟演出实时编排、数字人角色微表情驱动、沙盒世界状态演化 |
| **延迟与吞吐** | 中高延迟（数百ms–数秒），受模型大小、输入长度、`max_tokens`影响；支持高并发，但需关注Token配额 | **超低延迟**（通常 <200ms），批量问题处理近线性增长；专为高QPS场景优化 | 中等延迟（500ms–3s），受`world_state`复杂度与`temperature`影响；`acting`模型因邀测限制，吞吐待验证 |
| **状态管理** | Responses API支持`previous_response_id`与`x-dashscope-session-cache`实现会话级上下文缓存 | 无状态：每次请求独立，`state`需客户端完整传入 | **完全无状态**：`world_state`必须由客户端显式维护并每次全量提交，服务端不持久化任何会话数据 |
| **地域与部署约束** | 支持多地域（华北2、新加坡、中国香港等），推荐使用业务空间专属域名；三方模型仅限华北2可用 | 必须与Workspace地域严格一致（如`cn-beijing`），否则返回403/404；无三方模型支持 | 当前仅通过`dashscope.aliyuncs.com`统一域名访问（尚未支持业务空间专属域名）；`acting`模型仅支持中文 |

---

## 各方案适用场景建议

### ✅ 选择 Qwen 大模型当：
- 任务需要**开放域生成能力**（如撰写文案、解释概念、创作诗歌）；
- 需要**多轮对话记忆**与**上下文长程依赖建模**（如客服助手、个人知识助理）；
- 涉及**多模态输入理解**（上传图片问“图中人物在做什么？”）或**工具调用**（联网搜索、执行代码）；
- 技术栈已深度集成 OpenAI/Anthropic SDK，追求协议兼容性与迁移成本最小化。

### ✅ 选择 决策模型 当：
- 业务逻辑本质是**离散选择、二元判断或有序打分**（如“该工单应派给A/B/C组？”、“是否涉政？”、“风险等级1–5分”）；
- 对**响应延迟（<300ms）与结果可解释性（概率分布+置信度）有硬性要求**；
- 需要**高并发、低成本批量决策**（单次请求处理16个问题比16次调用Qwen更经济稳定）；
- 系统架构要求**输出强Schema约束**，下游无需NLP后处理即可直连数据库或规则引擎。

### ✅ 选择 世界模型 当：
- 构建**强交互性叙事产品**（如文字冒险游戏、AI导演助手、虚拟偶像直播系统）；
- 需要**跨时间步的世界状态一致性维护**（如角色关系变化、场景环境演变、物品持有状态转移）；
- 场景涉及**多粒度协同控制**：宏观剧情（Adventure）→ 中观调度（Directing）→ 微观行为（Acting）；
- 接受**客户端承担状态管理责任**，且能按规范构造符合语义的`world_state` JSON结构。

---

## 开发者技术选型参考

| 选型考量 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **是否需要生成自然语言文本？** | 是 → Qwen；否 → 决策模型 或 世界模型 | 决策模型严格禁用文本输出；世界模型输出为结构化动作指令，非叙述性文本 |
| **输入是否高度结构化且问题类型固定？** | 是 → 决策模型；否 → Qwen 或 世界模型 | `state`+`questions`范式天然适配表单/工单/审核等结构化数据源 |
| **是否需维护跨请求的世界状态演化？** | 是 → 世界模型；否 → Qwen（Responses缓存）或 决策模型 | 世界模型要求客户端全量传递`world_state`，Qwen Responses仅缓存单一会话上下文 |
| **是否已有OpenAI/Anthropic SDK集成？** | 是 → 优先Qwen OpenAI/Anthropic兼容接口；否 → 评估DashScope原生或Decision/World专用SDK | 百炼提供`openai`/`anthropic`/`typesafe-sdk`三套官方SDK，降低接入门槛 |
| **对延迟敏感度 >500ms即不可接受？** | 是 → 决策模型；否 → Qwen/世界模型 | 决策模型实测P99延迟<200ms，Qwen/世界模型P95普遍>800ms |
| **是否涉及音视频端到端理解（如语音指令+画面反馈）？** | 是 → Qwen（`qwen3.8-omni-flash`）；否 → 其他 | Omni系列为Qwen独有，决策/世界模型均不支持多模态输入 |

> **重要提醒**：  
> - **不要混用场景**：用Qwen做工单分流（低效且不可控），或用决策模型写营销文案（功能不支持），将导致开发失败与资源浪费；  
> - **注意地域一致性**：决策模型与Qwen业务空间专属域名均要求`region`与Workspace严格匹配，世界模型暂不支持该特性；  
> - **邀测模型谨慎评估**：`acting`模型处于白名单邀测阶段，功能、稳定性与SLA尚未正式发布，生产环境请优先选用`adventure`/`directing`。  

---  
*最后更新：2024年10月 | 文档依据：`api/qwen-api-reference.md`、`api/decision-model.md`、`api/world-model-api-reference.md`*

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [decision model](../api/decision-model.md)
- [world model api reference](../api/world-model-api-reference.md)


