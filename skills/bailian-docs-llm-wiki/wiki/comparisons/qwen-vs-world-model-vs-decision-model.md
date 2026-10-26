# Qwen大模型、世界模型与决策模型对比

## 背景与目的  
在百炼平台日益丰富的模型服务生态中，Qwen大模型、世界模型（World Model）与决策模型（Decision Model）分别面向不同层级的智能任务：Qwen 侧重通用语言理解与生成，世界模型聚焦多模态场景建模与动态推演，决策模型则专精于确定性、结构化、可审计的规则型判断。本页旨在为开发者提供清晰、客观、可落地的技术选型参考，从接口设计、能力边界、工程约束和典型用例等维度进行横向对比，避免因模型语义混淆或 API 行为差异导致集成失败或性能偏差。

---

## 关键维度对比表

| 维度 | Qwen 大模型 | 世界模型（HappyOyster 系列） | 决策模型（`decision-model-preview`） |
|------|-------------|------------------------------|-------------------------------------|
| **核心定位** | 通用大语言模型（LLM），支持开放式文本生成、多轮对话与工具协同 | 多模态世界建模引擎，支持叙事推演、镜头调度、角色行为生成等具身智能任务 | 专用结构化决策引擎，执行单次前向推理并同步输出分类标签、置信度与是非判断 |
| **输入格式** | `messages` 数组（含 `role`/`content`），支持 `system` 提示、`tools` 定义；部分接口要求 `tools` 为 JSON Schema | `input` 字段为严格结构化 JSON 对象，schema 因模型而异（如 Adventure 需 `scene`+`characters`+`goal`；Directing 需镜头语义+坐标；Acting 需 `pose_quaternion` 骨骼状态） | `input` 为纯文本字符串（必填）；`system_prompt` 为可选规则声明字符串（非指令式 prompt，实际生效受模型微调限制） |
| **输出格式** | 非流式：`output.text`；流式：SSE chunk（含 `delta.content`、`tool_calls` 等）；格式依接口而异（OpenAI 兼容 vs DashScope 原生） | 非流式 JSON 响应，结构高度模型专属（如 Adventure 返回 `branches: [...]`，Directing 返回 `shots: [...]`）；仅 Adventure 支持流式（逐 step 推演） | 标准化 JSON：固定字段 `category`（string）、`score`（float, 0.0–1.0）、`yes_no`（boolean 或 null）、`confidence`（object，含各结果置信分布） |
| **支持模型** | `qwen-max`、`qwen-plus`、`qwen-turbo`（功能与性能有差异） | `happyoyster/adventure`（公开）、`happyoyster/directing`（公开）、`happyoyster/acting`（邀测中，白名单访问） | `decision-model-preview`（当前唯一公开可用决策模型） |
| **API 端点** | • DashScope 原生：`POST /api/v1/services/aigc/text-generation/generation`<br>• OpenAI 兼容：`POST /v1/chat/completions`<br>• Anthropic 兼容：`POST /v1/messages` | `POST /world-models/invoke`（统一入口，通过 `model` 参数路由） | `POST /v1/models/decision-model-preview:predict`（专用路径） |
| **计费方式** | 按 token 计费（输入 + 输出 token），不同模型单价不同；所有接口共享同一配额体系 | 按调用次数计费（非 token）；Adventure/Directing/Acting 分属独立计费项；Acting 邀测期间暂不计费 | 按调用次数计费（非 token）；与 Qwen、世界模型计费账户隔离，需单独开通配额 |
| **流式响应支持** | 全部接口支持，但字段命名与语义存在差异（如 OpenAI-Responses 的 `delta.tool_calls` 不兼容标准 OpenAI） | 仅 `happyoyster/adventure` 支持流式（返回每步推演状态）；Directing 与 Acting **不支持** | **不支持流式**；强制同步返回完整结构化结果 |
| **上下文长度** | 最大 32768 token（含系统提示、工具描述、历史消息） | 无统一 token 概念；以 `input` JSON 大小限制为准（最大 128KB） | 最大 8192 tokens（纯文本 `input`，超限直接报 `400`，不截断） |
| **状态管理** | 无内置会话状态；需开发者自行缓存 `messages` 历史 | 无内置状态持久化；长周期推演需显式传递 `state_id` 并自行维护状态快照 | **完全无状态**；每次请求均为独立决策，不依赖历史或上下文 |
| **典型场景** | 智能客服、代码辅助、内容创作、RAG 应用、Agent 工具调用编排 | 游戏剧情生成、虚拟制片运镜规划、数字人实时动作驱动、仿真环境交互推演 | 内容安全审核（涉政/暴恐/违禁词）、交易风控（异常频次/金额判定）、合规策略执行（GDPR/广告法条款匹配） |

---

## 适用场景建议

### ✅ 选择 Qwen 大模型，当您需要：
- 开放式语言生成与多轮对话能力；
- 动态调用外部工具（搜索、计算器、数据库等）构建 Agent；
- 快速迁移现有 OpenAI/Anthropic 应用（注意接口行为差异）；
- 对推理过程可控性要求高（推荐优先选用 DashScope 原生接口，支持 `tool_choice` 显式控制与流式中间步骤）。

### ✅ 选择世界模型，当您需要：
- 在游戏、影视、仿真等垂直领域实现**因果驱动的动态推演**（如“主角受伤后，工厂警报触发，门禁关闭”）；
- 将抽象语义指令（如“营造压迫感”）转化为**符合专业语法的镜头参数序列**；
- 驱动 3D 角色完成**物理合理、意图明确的动作生成**（需接入 `.fbx` 骨骼绑定）；
- 构建具备“世界心智”的智能体，而非仅响应式 LLM。

### ✅ 选择决策模型，当您需要：
- **低延迟、高确定性、可审计**的二元/多类判断（如“是否违规？”、“属于哪类风险？”）；
- 下游系统能直接消费结构化 JSON 字段（无需 NLP 解析或正则提取）；
- 规则逻辑需与模型能力解耦（通过 `system_prompt` 声明，由模型内化执行）；
- 避免通用大模型的幻觉、发散或非确定性输出对关键业务造成影响。

---

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 说明 |
|----------|----------|------|
| **需要最高灵活性与生态兼容性** | Qwen（DashScope 原生接口） | 支持最全参数、唯一支持工具调用流式中间步骤、`qwen-max` 增强推理默认启用；适合构建复杂 Agent。 |
| **需要严格结构化输出且无歧义** | 决策模型 | `category`/`score`/`yes_no` 字段定义明确，无 token 截断风险，响应格式零解析成本；风控、审核类系统首选。 |
| **需要跨模态场景建模与动态演化** | 世界模型（Adventure 或 Directing） | 当前唯一提供因果链推演与电影级运镜生成能力的 API；不可被 Qwen 或其他 LLM 替代。 |
| **需快速验证原型，但无强一致性要求** | Qwen（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)） | 利用现有 SDK 快速接入，但须注意：不原生支持工具调用结构化响应、`max_tokens` 含义不同、增强推理能力被禁用。 |
| **需驱动 3D 角色动画** | 世界模型（Acting，邀测中） | 仅此模型支持骨骼关键帧映射；务必确认输入骨架为 `.fbx` 格式，并使用 `pose_quaternion` 字段。 |
| **需长程记忆或多轮上下文推理** | ❌ 三者均不原生支持 | 所有模型均为无状态设计；必须由应用层实现 history 缓存（Qwen）、`state_id` 管理（World Model）或规则聚合（Decision Model）。 |

> **重要提醒**：  
> - **勿混用接口语义**：例如，将决策模型的 `system_prompt` 当作 Qwen 的 system message 使用，或将世界模型的 `input` 直接塞入 Qwen 的 `messages`，将导致 400 错误或不可预测输出。  
> - **务必校验响应字段空值**：决策模型的 `yes_no` 在 `system_prompt` 模糊时可能为 `null`；世界模型的 `Acting` 输出在拓扑不匹配时可能为空数组——生产环境必须做防御性解析。  
> - **计费隔离**：三类模型使用独立配额与计费单元，请在百炼控制台分别配置预算告警，避免某类模型调用激增导致其他服务中断。  

---  
*本文档依据截至 2024 年 Q3 百炼平台公开 API 文档与实测行为编写，具体能力以控制台最新模型列表及 API 响应为准。*

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


