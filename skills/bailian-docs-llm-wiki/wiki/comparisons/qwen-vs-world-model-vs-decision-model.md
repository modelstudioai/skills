# Qwen大模型、世界模型与决策模型能力对比

为帮助开发者在百炼平台上快速识别并选用最适合业务需求的模型能力，本文对三类核心推理服务——**Qwen大模型**（通用多模态大语言模型）、**世界模型**（面向动态场景建模与推演的专用模型）和**决策模型**（面向结构化判断的轻量级确定性模型）——进行系统性能力对比。该对比基于当前（2024年Q3）百炼平台正式开放的功能范围、API 设计范式与工程约束，聚焦实际集成中的关键技术维度，旨在为架构设计、接口选型与性能优化提供可落地的参考依据。

## 关键能力维度对比

| 维度 | Qwen大模型 | 世界模型 | 决策模型 |
|------|------------|----------|----------|
| **核心定位** | 通用多模态大语言模型（LLM），支持开放式生成、复杂推理与工具协同 | 专用世界建模引擎，聚焦场景状态理解、因果推演与叙事行为生成 | 轻量级结构化决策引擎，专注高确定性、低延迟的分类/判断/评分任务 |
| **输入格式** | 多协议灵活支持：<br>• OpenAI 兼容：`messages` 数组（含 `system`/`user`/`assistant` 角色）或 `/responses` 专用 `input` 字符串/对象<br>• Anthropic 兼容：`messages` + `system` 消息<br>• DashScope 原生：`input` 对象（支持图像 URL、base64、视频帧序列、音频 blob 等细粒度控制） | 统一 JSON 对象，结构严格按模型类型定义：<br>• `adventure`：`{"world_state": {...}, "goal": "..."}`<br>• `directing`：`{"timeline": [...], "characters": [...]}`<br>• `acting`：`{"scene_state": {...}, "directing_output_id": "..."}` | 严格结构化 JSON：<br>• `state`: 任意业务上下文（字符串/对象/数组，JSON 序列化后 ≤65536 tokens）<br>• `questions`: 键值对对象，每个值含 `type`（`choice`/`noul`/`score`）、`instructions`、`criteria`（按需） |
| **输出格式** | 自由文本生成为主，支持流式（`stream: true`）；<br>• `/responses` 可返回结构化工具调用结果、多轮上下文 ID（`response_id`）及输入项引用；<br>• Anthropic `/messages` 支持 `tool_use` 输出块；<br>• DashScope 多模态端点可返回图像 base64 或视频帧 URL | 固定 JSON Schema 输出：<br>• `adventure`：返回 `{"branches": [{"reasoning": "...", "next_state": {...}}, ...]}`<br>• `directing`：返回 `{"events": [...], "timeline_updates": [...]}`<br>• `acting`：返回 `{"actions": [{"type": "gesture", "duration_ms": 1200, ...}, ...]}`<br>• **不支持流式响应** | 严格 Schema 化输出，**零自由文本**：<br>• `choice`: `{ "selected": "option_a", "probabilities": {"option_a": 0.82, ...}, "confidence": 0.93 }`<br>• `noul`: `{ "p_yes": 0.76, "confidence": 0.89 }`<br>• `score`: `{ "expected_score": 3.2, "probabilities": [0.05, 0.25, 0.60, 0.10], "confidence": 0.85 }` |
| **支持模型** | 全系列 Qwen 模型：<br>• 文本：`qwen3.8-max`, `qwen3.7-plus`<br>• 多模态：`qwen3-vl-plus`<br>• 音频：`qwen-audio`（**仅 DashScope 原生支持**）<br>• 第三方模型（部分兼容） | HappyOyster 系列专用模型：<br>• `happyoyster/adventure`<br>• `happyoyster/directing`<br>• `happyoyster/acting`（邀测中） | 单一预览模型：<br>• `decision-model-preview`（无版本别名） |
| **API 端点** | 多协议多端点：<br>• OpenAI 兼容：`/{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• OpenAI `/responses`：`.../compatible-mode/v1/responses`<br>• Anthropic 兼容：`.../apps/anthropic/v1/messages`<br>• DashScope 原生：`.../api/v1/text-generation/generation` 或 `/multimodal-generation/generation` | 统一端点：<br>• `https://dashscope.aliyuncs.com/api/v1/world-models/invoke`（**不支持 WorkspaceId 域名**） | 统一端点（TypeSafe System One 协议）：<br>• `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/systemone`（**WorkspaceId 必填**） |
| **计费方式** | 按 token 计费（输入 + 输出）：<br>• 不同模型单价不同（如 `qwen3.8-max` 高于 `qwen3.7-plus`）<br>• 多模态输入（图像/视频/音频）按像素/帧/时长额外计费<br>• `/responses` 工具调用（如联网搜索）单独计费 | 按请求次数计费：<br>• `adventure` / `directing`：统一单价<br>• `acting`：独立单价（邀测期可能免费）<br>• **不按 token 或内容长度计费** | 按请求次数计费：<br>• 单次请求无论含 1 个或最多 16 个 `questions`，均计为 1 次调用<br>• **与 `state` 长度、问题复杂度无关** |
| **典型场景** | • 智能客服对话（多轮、带知识库）<br>• 多模态内容理解（图文问答、视频摘要）<br>• Agent 自主规划（调用工具完成复杂任务）<br>• 代码生成与解释<br>• 创意写作与文案生成 | • 游戏 AI NPC 行为推演（“玩家进入森林后，狼会如何反应？”）<br>• 影视/游戏叙事调度（“生成未来30秒内角色冲突事件链”）<br>• 虚拟人实时动作合成（基于导演指令生成微表情+手势序列）<br>• 开放世界沙盒模拟（物理+社会规则联合推演） | • 客服工单自动分级（严重度 1–4 分）<br>• 内容安全审核（是否涉政？是否含违禁词？置信度？）<br>• Agent 任务路由（“该用户问题应转交售前/售后/技术？”）<br>• 任务完成度校验（“用户是否已提供全部必要信息？” P(yes) = ?） |

## 各方案适用场景建议

- **选择 Qwen 大模型，当您需要**：  
  ✅ 开放式语言生成、多轮对话管理、跨模态理解（图文/音视频）、复杂推理与工具协同；  
  ✅ 构建通用 AI Agent、智能助手、创作型应用；  
  ❌ 不适合对延迟极度敏感（如毫秒级响应）、输出必须严格结构化、或需规避任何自由文本生成的场景。

- **选择世界模型，当您需要**：  
  ✅ 在动态、状态化的虚拟环境中进行因果推演、时间线编排或角色行为建模；  
  ✅ 将抽象叙事指令（如“制造一场意外冲突”）转化为具体、连贯、符合世界观的动作序列；  
  ✅ 构建游戏 AI、交互式叙事引擎、虚拟仿真训练环境；  
  ❌ 不适合处理纯文本问答、通用知识检索、非场景化逻辑判断；且当前 `acting` 模型处于邀测阶段，生产环境需谨慎评估可用性。

- **选择决策模型，当您需要**：  
  ✅ 在高并发、低延迟要求下，对结构化业务问题做出**确定性、可审计、零歧义**的判断；  
  ✅ 输出直接用于下游系统路由、告警触发或数据标注（无需 NLP 后处理）；  
  ✅ 显著降低 [Token](../concepts/token.md) 成本与响应延迟（相比用 Qwen 做相同判断，延迟低 5–10 倍，成本低 3–8 倍）；  
  ❌ 不适合需要生成解释性文字、处理模糊语义、或需模型主动提出新选项的场景。

## 面向开发者的选型参考

| 选型考量点 | 推荐方案 | 说明 |
|------------|----------|------|
| **是否需要生成自然语言回复？** | ✅ Qwen | 世界模型与决策模型均不生成自由文本。若需“回答用户问题”，Qwen 是唯一选择。 |
| **输入是否含图像/视频/音频？** | ✅ Qwen（DashScope 原生端点） | 世界模型仅接受结构化状态描述；决策模型仅接受文本/结构化 `state`。多模态理解必须用 Qwen。 |
| **是否需在虚拟世界中做多步因果推演？** | ✅ 世界模型（Adventure/Directing） | Qwen 可模拟但缺乏内置世界规则与状态演化机制；决策模型完全不支持推演。 |
| **是否需将“是/否/未知”或“1–5分”等判断结果直接写入数据库？** | ✅ 决策模型 | 输出即结构化 JSON，字段名与含义稳定，无需正则提取或 LLM 解析，审计友好。 |
| **是否需调用外部工具（搜索、计算器、知识库）？** | ✅ Qwen（OpenAI `/responses` 或 Anthropic `/messages`） | 世界模型与决策模型均无工具调用能力。 |
| **是否需极低延迟（<200ms P95）与确定性吞吐？** | ✅ 决策模型 > Qwen > 世界模型 | 决策模型专为低延迟优化；Qwen 受模型大小与 token 数影响；世界模型因多步推演，延迟相对最高。 |
| **是否需跨请求维持长期世界状态？** | ⚠️ 世界模型（需自行维护） | 所有模型均无服务端状态持久化。世界模型要求开发者在每次请求中完整传入 `world_state`；Qwen `/responses` 支持 `previous_response_id` 实现轻量上下文串联；决策模型无状态概念。 |

> **最佳实践提示**：  
> - **混合架构常见**：例如，用 Qwen 处理用户自然语言输入 → 提取结构化意图 → 输入决策模型做路由判断 → 若需推演，则调用世界模型生成行为 → 最终由 Qwen 将结果润色为用户可读回复。  
> - **务必使用 WorkspaceId 专属域名**：Qwen 与决策模型均强烈依赖 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，旧版 `dashscope.aliyuncs.com` 域名将导致性能下降或功能不可用。  
> - **调试优先使用 Playground**：Qwen 的 [OpenAI 兼容 Playground](https://bailian.console.aliyun.com/playground/openai)、世界模型的 [HappyOyster Playground](https://bailian.console.aliyun.com/worldmodel_playground) 和决策模型的 [SystemOne Playground](https://bailian.console.aliyun.com/systemone_playground) 均提供免代码验证，强烈建议集成前完成端到端流程测试。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [world model api reference](../api/world-model-api-reference.md)
- [decision model](../api/decision-model.md)


