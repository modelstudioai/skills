# Qwen 大模型、World Model 与 Decision Model 对比

本对比旨在帮助开发者在百炼平台技术选型中，清晰区分三类核心能力模型的定位、能力边界与适用场景。Qwen 系列代表通用大语言/多模态生成能力，World Model 聚焦动态世界状态建模与因果推演，Decision Model 则专为确定性结构化决策设计。三者并非替代关系，而是面向不同抽象层级（生成 → 推演 → 判定）的互补能力组件。理解其差异有助于避免误用（如用 Qwen 做工单分流导致延迟高、成本高、结果不可控），并支持构建分层智能系统（例如：Decision Model 路由请求 → Qwen 生成响应 → World Model 模拟用户行为反馈）。

## 关键维度对比

| 维度 | Qwen 大模型 | World Model | Decision Model |
|------|-------------|-------------|----------------|
| **核心范式** | 生成式（Generative）：基于上下文生成自然语言、代码、图像描述、音视频理解结果等 | 推演式（Simulative）：基于初始世界状态，按规则/因果逻辑演化多步状态，输出状态变更与推理轨迹 | 判定式（Discriminative）：对给定上下文进行结构化分类、是非判断或有序评分，**不生成文本** |
| **输入格式** | 多协议支持：<br>• OpenAI Chat：`messages: [{role, content}]`，`content` 支持 `text`/`image_url`/`video_url` 等<br>• DashScope 原生：`input` 包裹 `messages`，`image`/`video` 为独立字段<br>• Anthropic Messages：`messages` + `system` 字符串/数组 | JSON 结构化对象：<br>• 必填 `scene_state`（符合预定义 schema 的世界快照，含 `entities`、`world_rules` 等）<br>• 必填 `task_type`（`"adventure"`/`"directing"`/`"acting"`）<br>• 可选 `max_steps` | JSON 结构化对象：<br>• 必填 `model: "decision-model-preview"`<br>• 必填 `state`（文本/JSON/数组，最大 65536 token）<br>• 必填 `questions`（键值对，每个值定义 `type`/`instructions`/`criteria`） |
| **输出格式** | 文本流或完整响应（含 `choices[0].message.content` 或 `content` 字段）；多模态任务返回结构化结果（如 `video_frames`、`tool_calls`）；支持 `reasoning_trace`（需启用） | JSON 对象：<br>• `next_state`（更新后的世界状态快照）<br>• `reasoning_trace`（可选，需 `enable_trace=true`）<br>• 无自由文本生成字段 | 纯结构化 JSON：<br>• `choice`: `{selected, probabilities, confidence}`<br>• `noul`: `{noul}`（P(yes) 浮点值）<br>• `score`: `{expected_score, probabilities, confidence, legend}`<br>• **无 `content`、`text`、`reasoning` 等文本字段** |
| **支持模型** | 全系列千问模型：<br>• 文本：`qwen3.8-max`、`qwen3.7-plus`、`qwen-coder-next` 等<br>• 多模态：`qwen3-vl-plus`、`Qwen-Omni`、`QVQ` 等<br>• 第三方：DeepSeek、Kimi、GLM、MiniMax（限华北2） | HappyOyster 系列：<br>• `HappyOyster-Adventure`（剧情/状态推演）<br>• `HappyOyster-Directing`（多角色调度/镜头生成）<br>• `HappyOyster-Acting`（邀测中，动作/微表情联合生成） | 仅 `decision-model-preview`（预览版，无其他别名或 GA 版本） |
| **API 端点（示例，华北2）** | • OpenAI Chat：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• Responses：`/compatible-mode/v1/responses`<br>• Anthropic Messages：`/apps/anthropic/v1/messages`<br>• DashScope 原生：`/text-generation/generation` 或 `/multimodal-generation/generation` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/v1/world-model/{task_type}`（如 `/v1/world-model/adventure`） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone` |
| **计费方式** | 按 token（输入+输出）计费，多模态任务按像素/帧数额外计费；不同模型单价不同（如 `qwen3.8-max` > `qwen-turbo`）；OpenAI/Anthropic 协议调用统一计入 Qwen 计费体系 | 按请求次数（per call）计费；`max_steps` 增加不额外计费（但影响延迟与资源消耗）；`acting` 类型因计算密集，单价高于 `adventure`/`directing` | 按请求次数（per call）计费；**批量提交多个问题仍计为 1 次调用**；单价显著低于 Qwen 和 World Model，适合高频低延迟场景 |
| **典型场景** | • 智能客服对话生成<br>• 多模态内容理解（图/视频问答）<br>• 代码生成与解释<br>• 文档摘要与改写<br>• Agent 工具调用（通过 Responses API） | • 游戏引擎中的 NPC 行为推演与世界状态更新<br>• 虚拟制片中导演指令到镜头序列的生成<br>• 互动叙事应用的剧情分支模拟与因果验证<br>• 数字孪生环境中的动态响应仿真 | • 工单自动分级与路由（如「紧急/高/中/低」）<br>• 内容安全审核（「违规/边缘/合规」三分类）<br>• 智能体任务分发（「交由 A 处理 / B 处理 / 需人工」）<br>• 结果置信度校验（如 LLM 输出是否可信） |

## 各方案的适用场景建议

- **选择 Qwen 大模型，当您需要**：  
  ✅ 生成自然语言、代码、数学解题步骤、创意文案等开放性内容；  
  ✅ 处理图像、视频、音频等多模态输入并产出语义理解结果；  
  ✅ 构建具备工具调用能力的 AI Agent（推荐使用 Responses API）；  
  ✅ 快速迁移现有 OpenAI/Anthropic 应用栈；  
  ❌ 不适用于对延迟敏感（>500ms）、要求确定性输出或需严格结构化结果的场景。

- **选择 World Model，当您需要**：  
  ✅ 在虚拟环境中模拟实体交互与状态演化（如游戏角色移动、物品状态变化）；  
  ✅ 将高层指令（“让主角避开守卫到达密室”）转化为多步可执行动作序列；  
  ✅ 验证叙事逻辑一致性或生成导演级镜头调度方案；  
  ✅ 构建具备“世界心智”的交互式体验（如教育模拟、沙盒游戏）；  
  ❌ 不适用于单轮问答、文本摘要、简单分类等非状态推演任务；`acting` 类型暂不支持流式，需等待完整动作序列。

- **选择 Decision Model，当您需要**：  
  ✅ 在毫秒级完成高并发结构化判定（如每秒处理数千条工单）；  
  ✅ 获取带概率分布与置信度的确定性决策（而非模糊文本解释）；  
  ✅ 批量处理同类判定问题（如同时评估 10 条评论的合规性）；  
  ✅ 作为智能系统“决策中枢”，为 Qwen 或 World Model 提供前置路由或后置校验；  
  ❌ 不适用于任何需要生成解释、理由、摘要或自由文本的场景；无法处理开放式问题。

## 面向开发者的选型参考

1. **先明确任务本质**：  
   - 问题是“**生成什么？**” → 选 **Qwen**；  
   - 问题是“**接下来会发生什么？状态如何演变？**” → 选 **World Model**；  
   - 问题是“**这属于哪一类？是/否？打几分？**” → 选 **Decision Model**。

2. **关注性能与成本约束**：  
   - 若 SLA 要求 P99 < 300ms 且 QPS > 100，优先评估 Decision Model 或 Qwen Turbo；World Model 的 `max_steps=3` 推演通常 > 800ms。  
   - 若预算敏感且任务为高频二分类，Decision Model 单次调用成本约为 Qwen Turbo 的 1/20，是更优解。

3. **注意协议与生态兼容性**：  
   - 已集成 OpenAI SDK？→ 直接复用 `openai` 客户端调用 Qwen Chat/Responses；  
   - 已使用 Anthropic SDK？→ 切换 `base_url` 即可接入 Qwen Anthropic Messages；  
   - 需要精细控制视频抽帧（如 `max_frames`）？→ 必须选用 DashScope 原生协议；  
   - 需要结构化 Schema 输出？→ Qwen Anthropic Messages 或 Decision Model 原生支持，Qwen OpenAI Chat 需依赖 `response_format`（部分模型支持有限）。

4. **组合使用是最佳实践**：  
   - 示例架构：`Decision Model` 先判定用户意图类型 → 路由至 `Qwen`（对话）或 `World Model`（游戏指令）；  
   - 示例增强：`Qwen` 生成回复后，用 `Decision Model` 校验其安全性得分；  
   - 示例协同：`World Model` 输出 `next_state` 后，交由 `Qwen` 生成该状态下的自然语言描述。

> **重要提醒**：所有模型均需通过业务空间专属域名接入（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐使用。认证统一采用 `Authorization: Bearer <API_KEY>`。请务必查阅各模型文档中的参数细节（如 Anthropic 协议 `temperature` 范围差异、Decision Model `legend` 键类型为字符串等），避免因参数误配导致异常。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


