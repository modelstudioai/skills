# 通义大模型、机器翻译模型与决策模型能力对比

本文旨在为百炼平台开发者提供清晰的技术选型参考，系统对比通义大模型（Qwen 系列）、Qwen-MT-Uni 机器翻译模型与 `decision-model-preview` 决策模型在核心能力维度上的差异。三者定位迥异：**通义大模型是通用生成式智能底座**，面向开放性语言理解与创作；**Qwen-MT-Uni 是垂直领域专用的全模态翻译引擎**，聚焦格式保真与多源输入处理；**决策模型则是轻量级结构化推理服务**，专为低延迟、高确定性的业务判断场景设计。正确区分其能力边界，可避免误用导致的性能浪费、结果不可靠或计费异常。

## 关键能力维度对比

| 维度 | 通义大模型（Qwen 系列） | 机器翻译模型（Qwen-MT-Uni） | 决策模型（`decision-model-preview`） |
|------|------------------------|----------------------------|-------------------------------------|
| **核心定位** | 通用大语言模型（LLM），支持对话、推理、代码、多模态生成等综合能力 | 全模态机器翻译专用模型，端到端完成“识别→翻译→格式重构”闭环 | 轻量级结构化决策模型，仅输出分类/是非/评分等确定性判定结果 |
| **输入格式** | 多样化：<br>• 文本：`messages` 数组（Chat/Anthropic/DashScope）或 `input` 字符串（Responses）<br>• 多模态：图像 URL / base64 / 文件对象（各协议字段名不同）；音频/视频需 DashScope 协议支持 `Qwen-Audio`<br>• 支持[工具调用](../concepts/tool-calling.md)上下文（Responses API） | 全模态统一入口：<br>• 文本：`source_texts`（字符串或数组）<br>• 文件：`fileUrl`（HTTPS 链接，≤100 MB）<br>• 格式：PDF/DOCX/PPTX/XLSX/HTML/MD/图片/音频（3s–60min）<br>• 支持 `ext.domainHint`（英文）、`ext.glossary` 等增强参数 | 严格结构化：<br>• `state`：原始业务上下文（JSON 对象/字符串/数组，≤65536 token）<br>• `questions`：定义待决问题的对象（最多 16 个），含 `type`（`choice`/`noul`/`score`）、`criteria` 等字段 |
| **输出格式** | 自由文本生成为主：<br>• Chat/Anthropic/DashScope：返回 `content` 字段的自然语言响应<br>• Responses API：额外支持 `tool_calls`、`response_id` 等结构化元信息<br>• 多模态输出含 `image_url`、`audio_url` 等 | 格式保真输出：<br>• 文本输入 → `TranslatedTexts`（字符串或数组）<br>• 文件输入 → `TranslatedFileUrl`（带签名的 HTTPS 下载链接，保持原始排版与样式）<br>• 同步/异步模式均返回标准化 `output.Data` 结构 | 纯结构化判定结果：<br>• 无任何自由文本生成<br>• 输出 `answers` 对象，包含：<br>  - `choice`: `{selected, probabilities, confidence}`<br>  - `noul`: `{p_yes, confidence}`<br>  - `score`: `{weighted_index, probabilities, confidence}` |
| **支持模型** | • Qwen 系列：`qwen4-max`, `qwen3.8-plus`, `qwen3.7-flash`, `qwen3-vl-plus`, `qwen3-coder-flash` 等<br>• 第三方模型：`deepseek-v4.1-flash`, `kimi-k3.1-pro`, `glm-5.3`, `MiniMax-M2.5`<br>• 特殊能力：`Qwen-Audio` 仅 DashScope 协议支持 | • 唯一公开模型：`qwen-mt-uni`（无 base/pro 变体）<br>• 所有功能（文档翻译、图像OCR翻译、音频转译）均由该模型统一承载 | • 唯一可用模型：`decision-model-preview`（预览版）<br>• 无其他型号或变体 |
| **API 端点（典型）** | • OpenAI Chat：`/compatible-mode/v1/chat/completions`<br>• Responses（推荐生产）：`/compatible-mode/v1/responses`<br>• Anthropic Messages：`/apps/anthropic/v1/messages`<br>• DashScope 原生：<br>  - 文本：`/api/v1/services/aigc/text-generation/generation`<br>  - 多模态：`/api/v1/services/aigc/multimodal-generation/generation` | • 统一端点（DashScope 协议）：<br>`/api/v1/services/aigc/multimodal-generation/generation`<br>• 异步需加 Header：`X-DashScope-Async: enable` | • 统一端点（System One 协议）：<br>`/compatible-mode/v1/systemone`<br>• 仅此一个接口，不区分任务类型 |
| **计费方式** | • 按 `input_tokens` + `output_tokens` 计费（单位：千 tokens）<br>• 不同模型单价不同（如 `qwen4-max` > `qwen3.7-flash`）<br>• Responses API 的[工具调用](../concepts/tool-calling.md)（联网搜索、知识库检索等）按次额外计费 | • 按 `usage.input_tokens` 计费（单位：千 tokens）<br>• **注意**：`input_tokens` 包含 OCR 识别、音频转写、文档解析等前置处理消耗，非仅翻译文本长度<br>• 文件类任务无论大小，均按实际解析后文本 token 计费 | • 按**请求次数**计费（非 token）<br>• 单次请求含最多 16 个问题，费用固定<br>• 与输出长度、token 数完全无关，成本高度可预测 |
| **典型场景** | • 智能客服对话、内容创作、代码生成与解释<br>• 多轮 Agent 编排（Responses API 支持 `previous_response_id`）<br>• 图像理解（VL 模型）、语音理解（Audio 模型）<br>• 需要自由文本输出的任意生成任务 | • 跨语言文档本地化（PDF/Word/PPT 等格式不变）<br>• 会议录音实时字幕+翻译<br>• 商品图/说明书图片文字翻译（保留图文布局）<br>• 多语种网页/Markdown 内容批量翻译 | • 工单自动分流（“归属技术部/客服部/法务部？”）<br>• 内容安全审核（“是否含违规信息？置信度？”）<br>• 智能体执行完成度校验（“任务是否已完成？Yes/No/Uncertain”）<br>• 服务等级评估（“用户满意度：1–5 分，概率分布？”） |

## 各方案适用场景建议

- **选择通义大模型（Qwen）当且仅当**：  
  ✅ 任务需要**开放性语言生成、复杂推理、多轮交互或创造性输出**（如写文案、编代码、分析长文档、扮演角色对话）；  
  ✅ 需要集成外部工具（联网搜索、知识库、计算器）构建 Agent；  
  ✅ 输入/输出本质是自然语言，且对格式保真无硬性要求；  
  ❌ 避免用于纯结构化判断（如二分类）、高并发低延迟决策（LLM 延迟波动大）、或需 100% 确定性结果的场景。

- **选择 Qwen-MT-Uni 机器翻译模型当且仅当**：  
  ✅ 任务核心是**跨语言转换，且必须保持原始文件格式、排版、图表位置、超链接等结构信息**；  
  ✅ 输入源多样（扫描件PDF、会议录音、PPT课件、网页HTML），需“一键翻译”而非分步处理；  
  ✅ 需要领域适配（通过 `domainHint`）或术语强控（通过 `glossary`）；  
  ❌ 避免用于非翻译类任务（如摘要、改写、问答）；不适用于仅需简单短句翻译且无格式要求的场景（此时 Qwen 文本模型更灵活经济）。

- **选择决策模型（`decision-model-preview`）当且仅当**：  
  ✅ 任务本质是**高确定性、低延迟、可枚举的业务判断**，且结果必须为结构化数据（非文本）；  
  ✅ 需要**概率分布与置信度**支撑下游阈值过滤、多模型融合或风险预警；  
  ✅ 场景具备明确评判标准（`criteria`），如工单规则、审核策略、评分量表；  
  ❌ 绝对禁止用于任何需要生成自然语言描述、解释原因、或自由发挥的任务；不适用于输入超长（>65536 token）或问题数超限（>16）的复杂决策。

## 开发者技术选型参考

作为百炼平台开发者，请按以下流程进行选型：

1. **明确任务本质**：  
   - 若输出是**一段话、一篇报告、一行代码、一张图的理解描述** → 选 **通义大模型**；  
   - 若输出是**一份中文版PDF、一张翻译后的商品图、一段带中文字幕的视频** → 选 **Qwen-MT-Uni**；  
   - 若输出是**一个 JSON 对象，含 `{"selected": "tech_team", "confidence": 0.92}` 或 `{"p_yes": 0.87, "confidence": 0.81}`** → 选 **决策模型**。

2. **评估输入与约束**：  
   - 输入含大量非文本数据（PDF/音视频）且需格式还原？→ **Qwen-MT-Uni** 是唯一解；  
   - 输入是纯 JSON/文本但需多轮上下文管理？→ 优先用 **Responses API**（支持 `store` 和 `previous_response_id`）；  
   - 输入超长（如整本合同）且只需关键条款判断？→ **决策模型**（65536 token 上限）或 **Qwen 大模型 + RAG 切片**（需自行处理）；  
   - 对延迟敏感（<500ms P95）、QPS 高（>1000）、结果必须 100% 可预测？→ **决策模型**（固定耗时）优于 LLM。

3. **验证计费合理性**：  
   - 频繁调用小文本生成？→ `qwen3.7-flash` 成本最低；  
   - 大量文档翻译？→ Qwen-MT-Uni 的 `input_tokens` 计费比先 OCR 再调用 Qwen 翻译更优；  
   - 每秒数千次工单路由？→ 决策模型按次计费远低于同等 QPS 的 LLM 调用。

4. **接入路径建议**：  
   - 已有 OpenAI/Claude 生态？→ 用 **OpenAI Chat** 或 **Anthropic Messages** 协议快速迁移；  
   - 追求生产稳定性与工具链？→ **Responses API** 是通义大模型首选；  
   - 需要最高控制粒度（如图像像素限制）？→ 用 **DashScope 原生协议**；  
   - 翻译任务需异步处理大文件？→ 务必使用 `X-DashScope-Async` Header；  
   - 决策任务需快速验证？→ 直接使用 [Playground](https://bailian.console.aliyun.com/systemone_playground) 在线调试。

> **重要提醒**：三者能力正交，不可互相替代。错误混用（如用 Qwen-MT-Uni 做客服问答、用决策模型生成产品描述）将导致功能失效、计费异常或结果不可用。请始终以**输出形态**和**业务语义**为第一选型依据。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


