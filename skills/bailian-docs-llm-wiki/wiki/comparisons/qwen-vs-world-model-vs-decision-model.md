# 核心推理模型对比：Qwen、世界模型与决策模型

为帮助开发者在百炼平台上高效选型，本文对三类面向不同推理范式的模型能力进行系统性对比：**Qwen 系列大模型**（通用强推理与多模态生成）、**世界模型**（动态场景建模与叙事演化）、**决策模型**（结构化、确定性、低延迟判断）。三者并非替代关系，而是互补的推理能力栈——Qwen 擅长“理解与表达”，世界模型专注“状态演化与因果推演”，决策模型专精“分类、判断与量化打分”。本对比基于当前（2024年Q3）百炼平台正式开放或灰度可用的能力，聚焦技术可行性、接口一致性与生产就绪度，不涉及未公开内测功能。

## 关键维度对比

| 维度 | Qwen 系列模型 | 世界模型 | 决策模型 |
|------|----------------|------------|------------|
| **核心定位** | 通用大语言模型（LLM）与多模态基础模型（MLLM），支持开放式文本/音视频生成、工具调用与复杂推理 | 面向动态世界模拟的专用推理引擎，建模角色行为、环境反馈与时间演化的因果链 | 轻量级结构化决策模型，仅输出分类标签、是非概率、有序评分及其置信度，**不生成任何自由文本** |
| **输入格式** | 多协议支持：<br>• OpenAI 兼容：`messages` 数组（支持 `text`/`image_url`/`video_url`/`input_audio` 等混合类型）<br>• Anthropic 兼容：`messages` + `system`（部分模型如 QwQ/QVQ 不支持）<br>• DashScope 原生：`input`（string/array）或专用字段（如 `multimodal-generation`） | 统一 JSON RESTful 请求体：<br>• 必填 `scene_context`（结构化对象，含时空、角色、状态等字段）<br>• 可选 `narrative_intent`、`max_steps` 等控制参数<br>• 无多模态原生支持（需预处理为文本描述） | TypeSafe System One 协议：<br>• `state`：原始上下文（string / object / array，自动序列化）<br>• `questions`：键值对字典，每个 value 含 `type`（`choice`/`noul`/`score`）、`instructions`、`criteria` |
| **输出格式** | 多协议差异显著：<br>• OpenAI 兼容：`choices[].message.content`（文本）或 `choices[].delta.content`（流式）<br>• Anthropic 兼容：`content[]` 中 `text` 或 `tool_use` 块<br>• DashScope 原生：`output.text` 或 `output.choices[0].message.content`<br>• 支持结构化 JSON Schema 输出（Anthropic 协议启用 `output_config.format`） | 固定 JSON 结构：<br>• `output.steps[]`：按时间戳排序的事件数组（每步含 `timestamp`、`event_type`、`description`）<br>• `next_context`：更新后的场景上下文对象（用于链式调用）<br>• **无流式响应**，`stream=true` 参数被忽略 |
| **支持模型/能力** | • 文本：`qwen3.8-max`、`qwen3.7-plus`、`qwen-turbo`、`qwen-coder-next`、`qwen-math`<br>• 多模态：`qwen3.8-omni-flash`（音视频）、`qwen3-vl-plus`、`QVQ`（视觉推理）<br>• 第三方直供：DeepSeek、Kimi、GLM、MiniMax<br>• 内置工具链（联网、代码解释器、知识库等） | • `adventure`：多分支剧情生成与玩家交互响应<br>• `directing`：角色行为调度、镜头编排、节奏控制<br>• `acting`（邀测中）：微表情、动作韵律建模（白名单访问）<br>• **无第三方模型接入**，纯百炼自研模块 |
| **API 端点（Base URL）** | • OpenAI 兼容：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>• Anthropic 兼容：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic`<br>• DashScope 原生：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1` | 统一域名：<br>`https://dashscope.aliyuncs.com/api/v1/world-model/{module}`<br>（`module` = `adventure` 或 `directing`） | TypeSafe 协议端点：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`<br>（需配置 `{WorkspaceId}` 与 `{region}`） |
| **计费方式** | • 按 **输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md)** 计费（多模态含图像/音频 [Token](../concepts/token.md) 折算）<br>• 不同模型单价差异显著（如 `qwen3.8-max` > `qwen-turbo`）<br>• 工具调用（如联网搜索）按次额外计费 | • 当前处于邀测/灰度阶段，**暂未开放正式计费策略**<br>• 实际调用按请求次数计费（非 Token），配额由平台统一管控<br>• 默认限流：5 QPS / API Key（运行时策略，非文档明示） | • 按 **单次请求** 计费（无论 `questions` 数量）<br>• 无 Token 消耗概念，不区分输入/输出长度<br>• 单次请求建议 ≤16 个问题以保障延迟（超量将线性增加 P95 延迟） |
| **典型场景** | • 智能客服对话（多轮+工具调用）<br>• 多模态内容理解（图/音/视频摘要、分析）<br>• 代码生成与数学解题<br>• 第三方模型网关（统一协议接入 DeepSeek/Kimi 等） | • 游戏 NPC 行为树与剧情分支引擎<br>• 虚拟制片中的 AI 导演原型（镜头调度、节奏规划）<br>• 互动小说实时状态演化与用户选择反馈<br>• 教育沙盒中的物理/社会规则模拟 | • 工单智能分流（“归属团队：A/B/C/其他”）<br>• 内容安全审核（“是否违规：yes/no”，附 P(yes)）<br>• 智能体路由决策（“下一跳服务：search/api/db”）<br>• 结果校验（“回答可信度：1–5 分”） |

## 适用场景建议

- **选择 Qwen 系列模型，当您需要**：  
  ✅ 开放式文本生成、多轮对话、复杂推理（数学/代码）；  
  ✅ 处理图像、音频、视频等多模态输入并生成语义描述；  
  ✅ 调用外部工具（搜索、执行代码、查知识库）完成闭环任务；  
  ❌ *避免用于纯结构化判断（如工单分类），因其开销高、延迟大、结果不可控。*

- **选择世界模型，当您需要**：  
  ✅ 对动态场景建模（如游戏角色状态、虚拟世界物理规则）；  
  ✅ 生成具有因果逻辑与时间演化的叙事事件链（非静态文本）；  
  ✅ 控制多个实体协同行为（导演视角下的角色调度与镜头语言）；  
  ❌ *避免用于单次静态问答、摘要、翻译等通用 NLP 任务；其输入必须是结构化场景上下文，且当前不支持长程状态持久化。*

- **选择决策模型，当您需要**：  
  ✅ 在毫秒级延迟下完成高并发、确定性的结构化判断（如每秒万级工单路由）；  
  ✅ 获取带概率分布与置信度的决策结果（而非“黑盒”文本输出）；  
  ✅ 批量处理异构问题（一次请求同时做分类+是非+打分）；  
  ❌ *避免用于需要自然语言解释、创造性生成或上下文深度理解的任务；它不生成任何文本，仅输出结构化数值。*

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 关键依据 |
|----------|-----------|-----------|
| **追求最低延迟与最高吞吐** | ✅ 决策模型 | 单次请求固定成本，无 Token 解码开销，P95 延迟 < 200ms（典型负载）；Qwen 与世界模型均需完整前向+采样，延迟波动大。 |
| **需处理图像/视频/音频输入** | ✅ Qwen（`qwen3.8-omni-flash`、`qwen3.5-Omni` 等） | 唯一提供原生多模态输入支持的模型；世界模型需人工预提取特征为文本；决策模型仅接受结构化 `state`。 |
| **需调用外部工具（搜索/代码/数据库）** | ✅ Qwen（OpenAI/Anthropic 兼容协议） | 内置工具链完整支持，且协议层已标准化；世界模型与决策模型无工具调用能力。 |
| **需构建动态状态机（如游戏、仿真）** | ✅ 世界模型（`adventure`/`directing`） | 专为状态演化设计，输出含时间戳事件链与可复用的 `next_context`；Qwen 需自行维护状态，决策模型无状态概念。 |
| **需严格可解释性与审计追踪** | ✅ 决策模型 | 所有输出必含 `probabilities` 与 `confidence`，支持概率溯源；Qwen 输出为文本，需额外解析；世界模型事件链虽可追溯，但内部推理过程不可见。 |
| **需快速集成第三方模型（如 Kimi、GLM）** | ✅ Qwen（OpenAI 兼容协议） | 唯一支持通过统一协议调用多家厂商模型的入口；世界模型与决策模型均为百炼专属能力。 |
| **项目处于早期验证阶段，资源有限** | ⚠️ 优先试用 Qwen Turbo / Decision Model Preview | Qwen `turbo` 与 `decision-model-preview` 均属低成本入门选项；世界模型当前邀测中，接入门槛高且无明确商用时间表。 |

> **重要提醒**：  
> - **协议迁移成本**：若已有 OpenAI 生态代码，Qwen 的 OpenAI 兼容协议可实现最小改动接入；世界模型与决策模型需完全重写客户端逻辑。  
> - **错误处理差异**：Qwen 返回标准 OpenAI/Anthropic 错误码；世界模型返回 `400`/`422`/`429` 等 HTTP 状态码；决策模型遵循 TypeSafe 协议错误规范（详见 `raw/model-api-reference/preparations/error-code.md`）。  
> - **未来演进提示**：Qwen 正加速融合世界模型能力（如 `qwen3.8-omni-flash` 已支持简单状态跟踪）；决策模型计划支持轻量级规则注入；世界模型 `acting` 模块预计 Q4 进入公测。建议关注百炼平台 Release Notes 获取最新能力图谱。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


