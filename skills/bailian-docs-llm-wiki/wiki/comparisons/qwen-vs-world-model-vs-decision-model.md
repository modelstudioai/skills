# Qwen 模型、World Model 与 Decision Model 对比

## 背景与目的

在百炼平台面向智能体（Agent）、具身智能（Embodied AI）和自动化决策系统的技术演进中，Qwen 系列大模型、World Model（世界模型）与 Decision Model（决策模型）构成了三层互补的能力栈：  
- **Qwen** 是通用认知基座，擅长理解、生成与工具协同；  
- **World Model** 专注动态环境建模与多步因果推演，支撑“世界如何演化”的推理；  
- **Decision Model** 则剥离语言生成，聚焦低延迟、高确定性的结构化判断，回答“此刻该做什么”。  

本对比旨在为开发者提供清晰的技术选型依据——明确三者在定位、能力边界、接口设计与工程适配性上的本质差异，避免因模型误用导致性能浪费、逻辑错位或架构冗余。所有分析均基于百炼平台当前（2024年Q3）正式发布能力。

---

## 关键维度对比表

| 维度 | Qwen 模型（API） | World Model | Decision Model |
|------|------------------|-------------|----------------|
| **核心定位** | 通用大语言模型（LLM），支持多模态理解、长上下文对话、工具调用与复杂推理 | 具身智能专用模型，建模开放世界状态演化、角色行为规划与叙事结构控制 | 结构化轻量决策引擎，仅输出分类/是非/评分及其概率分布，不生成自由文本 |
| **输入格式** | 多协议支持：<br>• Responses API：`input`（string/array of `EasyInputMessage`），支持 `input_audio`/`input_video`<br>• Chat API：标准 `messages[]` 数组<br>• Anthropic：`messages[]` + `system[]`（数组支持显式缓存）<br>• DashScope：`input.messages` 封装 | 固定 JSON 对象：`{ "model": "...", "input": { "scene_state": {...}, "intent": string, ... } }`；`scene_state` 为结构化世界快照（非纯文本） | 固定 JSON 对象：`{ "model": "decision-model-preview", "state": ..., "questions": { "q1": { "type": "choice", "criteria": {...} }, ... } }`；`state` 可为任意类型（自动序列化） |
| **输出格式** | 文本流或完整响应体，含 `output_text` / `content` / `delta`；Responses 支持 `reasoning` 输出块、工具调用结果嵌套；Anthropic 支持 `format: "json"` 强约束 | 结构化推演结果：<br>• Adventure：`output.steps[]`（每步含 `state_delta`, `causal_reasoning`）<br>• Directing：`output.plan[]`（含角色调度、节奏标记）<br>• Acting：`output.behavior_sequence`（含微表情时序、动作帧级描述） | 纯结构化答案对象 `answers`：<br>• `choice`: `{ "choice": "team_a", "probabilities": {"team_a": 0.82, ...}, "confidence": 0.93 }`<br>• `noul`: `{ "noul": 0.76 }`（P(yes)）<br>• `score`: `{ "score": 2.35, "probabilities": [0.1, 0.65, 0.25, 0.0], "confidence": 0.88 }` |
| **支持模型** | 全系列千问模型（`qwen3.8-*`, `qwen3.7-*`, `qwen-vl`, `qwen-coder`, `qwen-omni`）及第三方直供模型（`deepseek-v4.*`, `glm-5.*`, `kimi-k3`） | 三类专用模型：<br>• `happyoyster-adventure`（开放世界演化）<br>• `happyoyster-directing`（叙事编排）<br>• `happyoyster-acting`（角色行为，邀测中） | 仅 `decision-model-preview`（预览版），无其他模型变体 |
| **API 端点** | 多端点并存：<br>• Responses：`POST /compatible-mode/v1/responses`（推荐 Agent 场景）<br>• Chat：`POST /compatible-mode/v1/chat/completions`<br>• Anthropic：`POST /apps/anthropic/v1/messages`<br>• DashScope：`POST /api/v1/services/aigc/{text-generation|multimodal-generation}/generation` | 统一端点：<br>`POST https://dashscope.aliyuncs.com/api/v1/world-models`（暂不支持 Workspace 域名） | 统一端点：<br>`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`（强制 Workspace 域名） |
| **计费方式** | 按 **输入 token + 输出 token** 计费（含音视频解码 token）；不同协议计费一致；`qwen3.8-omni-flash` 音视频处理有独立 token 折算规则 | 按 **请求次数 + 推演步数（`max_steps`）** 计费；Adventure/Directing 每步计费相同，Acting 按行为序列长度阶梯计费 | 按 **单次请求** 计费（flat fee），与问题数量、选项数、输入长度无关；但超限（如 >16 问题）将拒绝而非降级计费 |
| **典型场景** | • 智能客服多轮对话<br>• 多模态内容创作（图文生成、音视频摘要）<br>• Agent 工具链执行（联网搜索、代码解释、知识库问答）<br>• 长文档分析与总结 | • 游戏 NPC 行为推演与世界状态更新<br>• 虚拟制片中的分镜调度与冲突触发<br>• 教育模拟沙盒中的多角色交互演化<br>• 工业数字孪生中的故障传播链预测 | • 工单智能分流（“转技术组/客服组/法务组”）<br>• 内容安全审核（“涉政/涉黄/正常”三分类+置信度）<br>• Agent 路由决策（“调用搜索工具？还是查知识库？”）<br>• 任务完成度校验（“步骤1完成度：1–5分”） |
| **流式支持** | 全协议支持流式（SSE），Responses 使用自定义字段 `response.output_text.delta`，其余为标准 `data: {...}` | Adventure 和 Directing 支持流式（逐 step 返回），Acting **不支持**（HTTP 400） | **不支持流式**；单次请求必返回完整 `answers` 对象 |
| **上下文管理** | Responses API 提供 `previous_response_id`（服务端自动拼接历史）与 `store`（持久化开关）；Chat/Anthropic 需客户端维护 `messages` 数组 | 无隐式上下文；每次请求需完整提交 `scene_state`；`max_steps` 控制单次推演深度 | 无上下文概念；每个请求完全独立；`state` 字段承载全部决策依据 |

---

## 适用场景建议

### ✅ 选择 Qwen 模型当：
- 你需要**生成自然语言、代码、图像描述或音视频摘要**；  
- 应用涉及**多轮对话、工具调用（搜索/计算/读取）或混合模态输入**；  
- 构建通用 Agent、Copilot 或内容创作助手；  
- 需要灵活的推理强度控制（如 `reasoning.effort: xhigh`）或结构化 JSON 输出（Anthropic `format`）。  
> ⚠️ 注意：若仅需简单是非判断或固定选项分类，使用 Qwen 属过度设计——成本高、延迟高、结果不可控。

### ✅ 选择 World Model 当：
- 你正在构建**具身智能系统**，需对“环境如何随动作变化”进行因果建模；  
- 场景具有**强时空结构**：如游戏世界、虚拟制片、教育模拟、工业仿真；  
- 需要**多角色协同推演**（如导演模型调度多个 NPC 行为）或**多步状态演化**（如 Adventure 模型预测故障扩散路径）；  
- 输入可结构化为 `scene_state`（如 JSON 描述的物理位置、角色状态、资源库存等）。  
> ⚠️ 注意：World Model 不处理原始文本生成任务，也不替代 LLM 的语义理解能力——它依赖 Qwen 等模型预处理输入为结构化状态。

### ✅ 选择 Decision Model 当：
- 你的业务问题本质是**确定性分类、二元判断或有序评分**，且要求毫秒级响应；  
- 需要**可解释的概率分布**（如工单派发时展示各团队承接概率）；  
- 系统需高并发、低延迟决策（如每秒万级审核请求），且无法容忍 LLM 的随机性与长尾延迟；  
- 已有成熟规则引擎，希望用模型增强而非替换——Decision Model 可作为规则兜底或置信度加权模块。  
> ⚠️ 注意：它**不生成任何解释性文字**。若需“为什么选 A 而非 B”，必须额外调用 Qwen 进行归因分析。

---

## 开发者技术选型参考

| 选型考量 | 推荐方案 | 理由 |
|----------|----------|------|
| **构建一个能联网搜索、写周报、画流程图的 AI 助手** | ✅ Qwen（Responses API） | 唯一支持内置工具链（`web_search`, `code_interpreter`, `image_generation`）与多模态输入的协议；`previous_response_id` 简化多轮状态管理。 |
| **开发一款开放世界 RPG 游戏，NPC 需根据玩家行为实时改变态度与行动** | ✅ World Model（Adventure + Acting） | `scene_state` 可映射游戏实体状态，`intent` 接收玩家指令，推演结果直接驱动游戏逻辑；Acting 模型输出微表情时序，无缝对接动画系统。 |
| **为客服系统增加「是否需升级至专家坐席」的自动判断模块** | ✅ Decision Model | 输入工单文本（`state`）+ 问题定义（`questions: { "escalate": { "type": "noul" } }`），毫秒返回 P(escalate)，无需解析文本、无幻觉风险、成本恒定。 |
| **已有 OpenAI SDK 的对话应用，想快速迁移到百炼** | ✅ Qwen（Chat API） | 接口语义最接近 `chat/completions`，只需替换 endpoint 与 API Key；但放弃 Responses 的高级特性（如原生工具调用）。 |
| **需要同时做「用户意图识别（Decision）」+「生成回复文案（Qwen）」** | ✅ 组合使用：Decision Model → Qwen | 先用 Decision Model 快速路由（如“查知识库” or “走人工”），再将决策结果注入 Qwen 提示词，调用 Responses API 执行具体动作——兼顾效率与表现力。 |
| **对延迟极度敏感（<100ms），且输入固定为 JSON Schema** | ✅ Decision Model | 唯一满足 sub-100ms P99 延迟的模型；Qwen 最小延迟约 300ms（首 token），World Model 单步推演亦需 200ms+。 |

> 💡 **最佳实践提示**：  
> - **不要用 Qwen 做决策**：即使 [prompt](../guides/prompt.md) 写成“只输出 yes/no”，其输出仍可能包含解释、换行或标点，需额外正则清洗，且概率不可靠；Decision Model 的 `noul` 字段是经过校准的 P(yes)。  
> - **不要用 World Model 替代 LLM**：它不理解自然语言指令本身，`intent` 字段需由 Qwen 等模型预处理为标准化动作（如 `"player_moves_to_north"`）。  
> - **Workspace 域名是性能关键**：Qwen 与 Decision Model **必须使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`**；World Model 暂未支持，仍用 `dashscope.aliyuncs.com`。  

---  
*最后更新：2024年10月*

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


