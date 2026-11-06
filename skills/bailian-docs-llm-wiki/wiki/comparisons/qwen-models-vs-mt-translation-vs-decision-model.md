# 通义大模型、机器翻译专用模型与决策模型对比

为帮助开发者在百炼平台上快速识别不同模型能力边界、技术约束与业务适配性，本文对三类核心 AI 能力进行横向对比分析：**通义大模型（Qwen 系列）**、**机器翻译专用模型（Qwen-MT 系列）** 和 **决策模型（`decision-model-preview`）**。该对比聚焦实际工程落地维度，涵盖协议兼容性、输入输出范式、调用成本、性能特征及典型适用场景，旨在为技术选型提供清晰、可操作的决策依据。

---

## 关键维度对比

| 维度 | 通义大模型（Qwen 系列） | 机器翻译专用模型（Qwen-MT 系列） | 决策模型（`decision-model-preview`） |
|------|--------------------------|-----------------------------------|----------------------------------------|
| **输入格式** | 多样化：<br>• 文本：`messages` 数组（Chat）、`input` 字符串/数组（Responses）<br>• 多模态：Base64 图像/视频帧、音频（仅 DashScope 协议）、PDF/DOCX（需预处理）<br>• 结构化上下文：支持 `system`、工具调用参数、缓存控制等 | 严格按任务类型区分：<br>• `Qwen-MT`：纯文本（`input.text`，≤8192 Unicode 字符）<br>• `Qwen-MT-Image`：Base64 编码图像 + `source_language`/`target_language`<br>• `Qwen-MT-Uni`：Base64 文档（PDF/DOCX，≤50 MB）或文本，不支持原始音频（需客户端先 ASR） | 结构化 JSON：<br>• `state`：任意业务上下文（文本、JSON 对象、数组），序列化后送入（≤65536 token）<br>• `questions`：定义问题类型（`choice`/`noul`/`score`）及对应 `criteria`，最多 16 个问题 |
| **输出格式** | 自由文本生成为主：<br>• Chat/Responses：标准 `choices[].message.content`<br>• Anthropic/DashScope：支持结构化输出（JSON Schema）、深度思考日志、工具调用结果<br>• 多模态：含 `fps`/`total_pixels` 等元信息的增强响应 | 格式强绑定任务：<br>• `Qwen-MT`：纯译文字符串（`output.text`）<br>• `Qwen-MT-Image`：带坐标、字体、颜色等样式元数据的结构化 JSON（启用 `preserve_format=true`）<br>• `Qwen-MT-Uni`：与源类型对齐的结构化输出（如 PDF 翻译后保留页码/段落结构） | **纯结构化，零文本生成**：<br>• `choice`：`{ "selected": "option_key", "probabilities": { "a": 0.82, ... }, "confidence": 0.93 }`<br>• `noul`：`{ "probability_yes": 0.97, "confidence": 0.91 }`<br>• `score`：`{ "expected_score": 2.25, "legend": ["低", "中", "高"], "confidence": 0.88 }` |
| **支持模型** | 全系 Qwen 商业版与开源版：<br>• 文本：`qwen3.8-max`, `qwen3.7-plus`, `qwen3.5-flash`, `qwen-coder-flash`<br>• 多模态：`qwen3-vl-plus`, `qwen3.8-omni-flash`, `QVQ`, `Qwen2.5-VL`<br>• 第三方直供（华北2）：`deepseek-v4.1-flash`, `kimi-k3.1-pro`, `glm-5.3`, `MiniMax-M2.5` | 专用模型族：<br>• `qwen-mt`（文本）<br>• `qwen-mt-image`（图像内嵌文本）<br>• `qwen-mt-uni`（文档/混合模态）<br>※ 不支持第三方模型 | 唯一模型：<br>• `decision-model-preview`（预览版，能力稳定） |
| **API 端点** | 多协议统一接入：<br>• OpenAI 兼容：`/v1/chat/completions`（Chat）、`/v1/responses`（Responses）<br>• Anthropic 兼容：`/v1/messages`<br>• DashScope 原生：`/api/v1/services/aigc/text-generation` 等<br>• **推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`） | 统一 RESTful 端点：<br>• `https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-translation/<model-name>`<br>• 模型名直接拼接（如 `/qwen-mt-image`）<br>• 不支持业务空间专属域名（固定旧域名） | 固定 TypeSafe System One 端点：<br>• `POST /compatible-mode/v1/systemone`<br>• 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`） |
| **计费方式** | 按 **[Token](../concepts/token.md) 消耗量** 计费：<br>• 输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md)（流式/非流式一致）<br>• 多模态模型按图像/视频像素、帧数额外计费（如 `total_pixels` 影响费用）<br>• 支持显式缓存（`cache_control`）降低重复请求成本 | 按 **请求次数 + 输入规模** 计费：<br>• `Qwen-MT`：按字符数阶梯计费（≤8192 字符/次）<br>• `Qwen-MT-Image`：按图像分辨率与页数计费<br>• `Qwen-MT-Uni`：按文档页数与解析复杂度计费（PDF >200 页可能超时）<br>• **无 Token 计费概念** | 按 **单次请求** 计费：<br>• 与输入长度、问题数量、输出结构复杂度无关<br>• 单次请求含最多 16 个问题，费用固定<br>• **无 Token、无流式、无缓存相关费用** |
| **典型场景** | • 开放域对话与知识问答<br>• 多轮 Agent 协作（工具调用、Web Search）<br>• 代码生成与解释<br>• 视频/图像理解与描述<br>• 长文本摘要与创作 | • 高保真跨语言内容本地化（网站、APP、文档）<br>• 扫描件/截图中的多语言文字实时翻译<br>• PDF 报告、合同、说明书的端到端格式保持翻译<br>• 跨语言客服工单语义转译（需预处理） | • 工单智能分流（“归属团队：A/B/C”）<br>• 内容安全审核（“是否违规：yes/no”，置信度）<br>• Agent 任务完成度判定（“完成度：1–5 分”）<br>• 客服对话情绪强度评分（“愤怒程度：低/中/高”） |

---

## 各方案适用场景建议

### ✅ 推荐选择 **通义大模型（Qwen）** 当：
- 业务需要**开放性生成能力**（如撰写文案、编写代码、推理问答）；
- 场景涉及**多轮交互、工具调用或外部系统协同**（如搜索+计算+总结）；
- 输入包含**图像、视频、音频或复杂文档**，且需语义级理解而非单纯翻译；
- 团队已使用 OpenAI/Anthropic SDK，追求**协议平滑迁移**；
- 可接受一定延迟与 Token 成本，重视**表达丰富性与灵活性**。

### ✅ 推荐选择 **机器翻译专用模型（Qwen-MT）** 当：
- 核心目标是**高精度、格式保真、领域适配的翻译**，而非通用生成；
- 输入明确为**文本、图片或文档**，且需结构化输出（如带坐标的 OCR 翻译结果）；
- 对**确定性、低歧义、术语一致性**要求极高（如法律合同、医疗说明书）；
- 需要批量处理大量静态内容（如整站网页、产品手册），且可预处理 ASR；
- 希望规避大模型“幻觉”风险，拒绝任何自由发挥，只要**精准映射**。

### ✅ 推荐选择 **决策模型（`decision-model-preview`）** 当：
- 任务本质是**结构化判断**（分类/是非/打分），无需生成自然语言；
- 对**延迟敏感**（毫秒级响应）、**吞吐量高**（万级 QPS）、**结果可解释性强**（概率分布+置信度）；
- 业务逻辑依赖**多问题并行求解**（如一个工单同时判断“紧急度”、“归属部门”、“是否需人工介入”）；
- 已有成熟规则引擎，需轻量 AI 模块替代硬编码分支（如 `if...else` 替换为 `choice` 选项）；
- 运维要求**零文本输出审计风险**（如金融合规场景），仅需结构化决策证据。

---

## 技术选型参考（面向开发者）

| 选型考量点 | Qwen 大模型 | Qwen-MT 系列 | 决策模型 |
|------------|--------------|----------------|------------|
| **SDK 集成难度** | ★★☆（OpenAI/Anthropic SDK 可直接复用，仅需切换 base_url） | ★★★（需按模型类型构造不同 input 结构，无高级封装） | ★★（DashScope SDK ≥2.0.1 提供 `client.decision.create()` 封装，但版本强约束） |
| **调试效率** | 高（Playground 支持多协议、多模态实时调试；支持 `stream` 流式观察） | 中（Playground 仅支持文本/图像基础翻译，文档类需线下测试） | 高（[SystemOne Playground](https://bailian.console.aliyun.com/systemone_playground) 提供预设场景与可视化概率图） |
| **错误排查成本** | 中高（Token 截断、温度越界、多模态参数缺失易导致静默降级） | 中（语言代码错误、图像 DPI 不足、PDF 加密等会返回明确错误码） | 低（参数校验严格，`questions` 类型不匹配立即报错；无隐式行为） |
| **可观测性** | 强（返回 `usage`、`prompt_filter_results`、`finish_reason` 等完整元信息） | 弱（仅返回 `output` 与基础 `code`/`message`） | 强（每个问题均返回 `confidence`、`probabilities`、`reasoning_trace`（调试模式）） |
| **长期演进风险** | 低（Qwen 系列为百炼核心战略，持续迭代） | 中（MT 系列功能收敛，新增语言对/格式支持节奏较慢） | 中高（`preview` 标识表明接口/能力可能调整，需关注版本通告） |

> 💡 **关键提醒**：  
> - **勿混用场景**：用 Qwen-MT 翻译长对话可能丢失上下文连贯性；用决策模型生成客服回复将直接失败（无文本输出能力）；  
> - **协议陷阱**：Qwen-Audio 仅 DashScope 协议支持；QwQ/QVQ 模型禁用 `system` 消息；Qwen-MT-Uni 文档 API 实际不支持原始音频；  
> - **性能兜底**：高并发决策场景务必压测 `decision-model-preview` 的 16 问题上限；Qwen-MT-Image 低 DPI 图像建议前端预增强；  
> - **成本优化**：Qwen 多轮对话优先用 Responses API 的 `previous_response_id` 管理上下文，避免重复传 `messages`；Qwen-MT 批量文本翻译请合并请求（单次 ≤8192 字符）。  

如需进一步验证模型效果，建议优先使用百炼控制台提供的 [Qwen Playground](https://bailian.console.aliyun.com/playground)、[MT Playground](https://bailian.console.aliyun.com/mt_playground) 和 [SystemOne Playground](https://bailian.console.aliyun.com/systemone_playground) 进行零代码沙箱测试。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


