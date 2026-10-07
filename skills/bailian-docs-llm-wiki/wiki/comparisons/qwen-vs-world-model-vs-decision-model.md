# Qwen 大模型、World Model 与 Decision Model 对比

本文旨在帮助开发者在百炼平台上进行技术选型时，清晰理解 **Qwen 大模型**（通用生成式AI）、**World Model**（具身智能环境建模）与 **Decision Model**（结构化决策推理）三类能力的本质差异、适用边界与工程约束。随着AI应用从单轮文本生成向多模态交互、具身规划与确定性决策纵深演进，准确区分这三类模型的定位，是构建高可靠、低延迟、可扩展AI系统的关键前提。

---

## 关键维度对比

| 维度 | Qwen 大模型 | World Model | Decision Model |
|------|-------------|-------------|----------------|
| **核心定位** | 通用大语言/多模态基础模型，支持开放式内容生成与理解 | 面向具身智能的环境状态建模与行为规划模型，聚焦“世界如何演化”与“角色如何协作” | 专用于结构化决策任务的轻量级推理模型，输出确定性分类/判断/评分，**不生成文本** |
| **输入格式** | 多协议支持：<br>• OpenAI Chat：`messages: [{role, content}]`，`content` 支持 `text`/`image_url`/`video_url` 等结构化类型<br>• DashScope 原生：`input.messages` + 扁平 `image`/`video` 字段，支持 `input_audio`<br>• Anthropic Messages：`content` 为 `text`/`image`/`video` 对象 | JSON 对象，`input` 字段结构严格依子模型而异：<br>• Adventure：`{"world_state": {...}, "goal": "..."}`<br>• Directing：`{"task": "...", "roles": [...]}`<br>• Acting（邀测）：含 `action_sequence`、`timing_constraints` 等物理执行参数 | JSON 对象，固定字段：<br>• `state`: 任意结构化业务上下文（String/Object/Array）<br>• `questions`: `{question_id: {type, instructions, criteria}}`，支持 `choice`/`noul`/`score` 三类问题并行提交 |
| **输出格式** | 文本流或完整 JSON：<br>• `choices[0].message.content`（Chat）<br>• `output.text`（Responses）<br>• `content` 数组（Messages）<br>• 多模态输出含 `image_url`/`audio_url` 等字段 | 完整 JSON 对象（**不支持流式响应**）：<br>• Adventure：`{"next_state": {...}, "reasoning": "..."}`<br>• Directing：`{"steps": [{"role": "...", "action": "..."}]}`<br>• Acting：`{"actions": [...], "timing": [...]}`（邀测中） | 纯结构化 JSON（**无文本生成**）：<br>• `choice`: `{selected: "opt1", probabilities: {"opt1": 0.82, ...}, confidence: 0.93}`<br>• `noul`: `{probability_yes: 0.97, confidence: 0.95}`<br>• `score`: `{expected_score: 3.2, probabilities: {"0": 0.05, "1": 0.12, "2": 0.68, "3": 0.15}, confidence: 0.89}` |
| **支持模型** | 全系列千问模型：<br>• 文本：`qwen3.8-max`, `qwen3.5-flash`, `qwen-coder-next`<br>• 多模态：`qwen3.8-omni-flash`, `qwen3-vl-plus`, `QVQ`<br>• 专用：`qwen3.5-math`, `qwen3.5-audio`（仅 DashScope）<br>• 第三方：`deepseek-v4-pro`, `glm-5.3`, `kimi-k3`（华北2限定） | HappyOyster 系列：<br>• `happyoyster-adventure`（探索建模）<br>• `happyoyster-directing`（指令编排）<br>• `happyoyster-acting`（动作执行，邀测中） | 仅 `decision-model-preview`（当前唯一可用模型） |
| **API 端点** | 多协议共存：<br>• OpenAI 兼容：`/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/v1/chat/completions`<br>• Responses：`/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/v1/responses`<br>• Anthropic：`/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/v1/messages`<br>• DashScope 原生：`/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/qwen/invoke` | 统一端点：<br>`https://dashscope.aliyuncs.com/api/v1/services/aigc/world-model/invoke`（所有子模型复用） | TypeSafe System One 协议端点：<br>`/{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`（按地域替换域名） |
| **计费方式** | 按 **输入 token + 输出 token** 计费（不同模型单价不同），多模态输入（图像/视频/音频）按像素/时长折算 token；音频模型 `qwen3.5-audio` 单独计价 | 按 **每次 API 调用** 计费（无论输入大小或输出长度），无 token 计费概念；Acting 模型邀测期间可能有特殊资费策略 | 按 **每次 API 调用** 计费（与问题数量、选项数量无关）；因无文本生成，成本极低且高度可预测 |
| **典型场景** | • 智能客服对话<br>• 多模态内容理解（图文摘要、音视频分析）<br>• 代码生成与解释<br>• Agent 工具调用与自主规划<br>• 数学推理与逻辑推演 | • 游戏/NPC 行为仿真与状态推演<br>• 工业数字孪生中的设备协同调度<br>• 教育场景中的多角色互动剧情生成<br>• 机器人任务规划（如“移动→抓取→放置”序列） | • 工单自动分派（选择最优处理团队）<br>• 内容安全审核（是否违规？严重程度？）<br>• AI Agent 路由决策（该请求应交由哪个子Agent处理？）<br>• 结果一致性校验（LLM 输出是否符合事实？置信度多少？） |

---

## 各方案的适用场景建议

### ✅ 选择 **Qwen 大模型** 当：
- 你需要**开放式文本生成、多轮对话、复杂推理或跨模态理解**；
- 应用需兼容 OpenAI/Anthropic 生态，或已有基于这些协议的 SDK/框架；
- 场景涉及**工具调用（function calling）、代码执行、数学证明、长文档摘要**等高级能力；
- 你愿意为高质量生成结果承担可变的 token 成本，并接受非确定性输出。

> ⚠️ 注意：避免将其用于纯结构化决策（如“是/否”判断），因其生成开销大、延迟高、结果不可控。

---

### ✅ 选择 **World Model** 当：
- 你的系统需要模拟**动态环境状态演化**（如玩家位置变化、物体交互结果）；
- 你正在构建**具身智能体（Embodied Agent）**，需将高层目标分解为角色协同的动作序列；
- 场景具有明确的**时空约束与物理规则**（如机器人路径规划、游戏关卡推进）；
- 你能接受**单次调用、完整响应、无[流式输出](../concepts/streaming-output.md)**的交互范式，且已申请所需子模型权限（尤其是 Acting）。

> ⚠️ 注意：它不替代 LLM 的通用理解能力，而是作为 LLM 的“认知外挂”，提供环境建模与行为编排支持；不可用于文本创作或问答。

---

### ✅ 选择 **Decision Model** 当：
- 你的任务本质是**高并发、低延迟、确定性的结构化判断**；
- 输出必须是**可解析、可审计、可置信度量化**的结构化数据（而非自然语言）；
- 你希望规避 LLM 的幻觉风险，对结果一致性与成本稳定性有强要求；
- 场景可明确定义为 `choice`（多选一）、`noul`（是非）、`score`（有序打分）三类之一；
- 你已在百炼控制台开通 `decision-model-preview` 权限，并使用 `typesafe-sdk` 进行集成。

> ⚠️ 注意：它无法处理开放性问题（如“请解释量子纠缠”），也不支持上下文记忆或多轮决策链；所有决策均基于单次 `state` 输入独立完成。

---

## 面向开发者的选型参考

| 你的需求 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| “我要做一个客服机器人，支持图片上传答疑” | ✅ Qwen（`qwen3-vl-plus` + OpenAI Chat） | 唯一支持 `image_url` 结构化输入的协议，且具备强图文理解能力 |
| “我需要让AI根据用户语音描述生成一段短视频脚本” | ✅ Qwen（`qwen3.8-omni-flash` + DashScope 原生） | 唯一支持端到端音视频理解与生成的模型，且 DashScope 协议支持 `input_audio` |
| “我在开发一个虚拟导演系统，需为多角色分配台词和走位” | ✅ World Model（`happyoyster-directing`） | Directing 模型专为多角色协作指令编排设计，输出结构化动作序列 |
| “我想实时判断用户上传的视频是否含违禁动作，并给出 1–5 级严重度” | ✅ Decision Model（`score` 类型） | 纯结构化输出、毫秒级延迟、可返回每级概率与置信度，远优于用 Qwen 生成文本再解析 |
| “我有一个工单系统，需自动分派给最合适的工程师团队（A/B/C/D）” | ✅ Decision Model（`choice` 类型） | 并行评估多选项、返回概率分布与整体置信度，便于后续路由策略优化 |
| “我需要在游戏里模拟 NPC 的[长期记忆](../concepts/memory.md)与环境反应（如‘门被炸毁后，NPC 不再尝试开门’）” | ✅ World Model（`happyoyster-adventure`） | Adventure 模型专精于世界状态持续推演，支持 `world_state` 显式建模与更新 |
| “我的 Agent 需要调用搜索工具查天气，再写一封邮件总结” | ✅ Qwen（`/responses` 协议） | Responses 协议原生支持 `tools` 与 `function_call`，且自动管理上下文缓存 |

> 💡 **最佳实践提示**：  
> - **组合使用更强大**：例如，用 Qwen 理解用户模糊指令 → 用 Decision Model 判断意图类别 → 用 World Model 规划执行步骤 → 用 Qwen 生成最终自然语言反馈。  
> - **性能敏感场景优先 Decision Model**：任何可形式化的判断任务，都应优先评估是否可用 Decision Model 替代 LLM，通常可降低 90%+ 延迟与成本。  
> - **务必检查地域与权限**：第三方模型（Kimi/DeepSeek）仅限华北2；Acting 模型需邀测；Decision Model 需开通 `systemone` 权限。  

---  
*本文档依据百炼平台截至 2024 年 Q3 的公开 API 规范编写，具体参数与行为请以各模型最新版 API 参考文档为准。*

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


