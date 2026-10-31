# 通义千问系列模型能力对比

为帮助开发者在百炼平台上高效选型，本文系统对比通义千问（Qwen）系列中三类核心模型服务的能力边界：**通用文本生成模型（Qwen API）**、**多模态翻译模型（Qwen MT）** 和 **专用决策模型（Decision Model）**。三者虽同属 Qwen 技术生态，但在设计目标、输入输出范式、协议支持、参数控制粒度及适用场景上存在本质差异。本对比基于当前（2024年Q3）百炼平台正式发布的 API 行为与文档规范，聚焦可验证的技术事实，规避模糊描述，旨在为工程落地提供明确、可操作的选型依据。

## 关键能力维度对比

| 维度 | Qwen 通用文本生成模型（API） | Qwen 多模态翻译模型（MT） | 决策模型（Decision Model） |
|------|------------------------------|----------------------------|-----------------------------|
| **核心定位** | 通用大语言模型能力底座：对话理解、内容生成、工具调用、代码推理等 | 领域专用模型：端到端跨语言语义对齐与格式保真翻译 | 任务专用模型：结构化、确定性、高置信度的逻辑判断与分类决策 |
| **支持模型** | `qwen-turbo`, `qwen-plus`, `qwen-max`, `qwen-vl-plus`（多模态）等 | `qwen-mt`（文本）、`qwen-mt-image`（图像）、`qwen-mt-uni`（全模态） | `decision-model-preview`（当前唯一公开版本） |
| **输入格式** | 文本消息数组（`messages`），支持 `user`/`assistant`/`system` 角色；DashScope 接口支持多模态输入（如 `qwen-vl-plus` 的 base64 图片） | 多样化：<br>• `qwen-mt`: 纯文本字符串<br>• `qwen-mt-image`: Base64 图片或 OSS URL<br>• `qwen-mt-uni`: multipart/form-data 文件、file_url 或 JSON 封装的文本/音频/文档 | 纯文本字符串或字符串数组（`input`），**不支持图片、音频、文件等非文本输入** |
| **输出格式** | JSON 对象，含 `choices[0].message.content`（文本）、`tool_calls`（工具调用）、`usage`（token 统计）等字段；支持流式响应（`stream: true`） | JSON 对象，含 `output.text`（译文）、`output.format_preserved`（格式重建结果）、`output.ocr_result`（OCR 原始文本）等；**不支持流式响应** | JSON 对象，严格结构化：<br>`label`（字符串）、`score`（0–1 浮点）、`is_true`（布尔）、`probabilities`（对象）、`confidence`（标量）；**不支持流式响应** |
| **API 协议兼容性** | • OpenAI 兼容 `/v1/chat/completions`<br>• Anthropic 兼容 `/v1/messages`<br>• DashScope 原生接口（功能最全） | • 统一网关，但**不兼容 OpenAI/Anthropic 标准协议**<br>• 使用百炼专属 REST 接口（如 `/api/v1/services/aigc/text-to-text/text-generation`） | • **完全不兼容 OpenAI/Anthropic 协议**<br>• 使用专用 REST 接口 `/v1/models/{model_id}:predict`，遵循 System One 语义规范 |
| **关键特有参数** | • DashScope: `top_k`, `repetition_penalty`, `enable_search`<br>• Anthropic: `tools`, `tool_choice`<br>• OpenAI-Responses: `enable_code_interpreter`, `enable_web_search` | • `source_language` / `target_language`（必填）<br>• `preserve_format`（默认 true）<br>• `input_type`（显式声明输入类型） | • `top_k`（控制返回概率类别数）<br>• `threshold`（过滤低置信度概率）<br>• **不支持 `system_prompt`, `temperature`, `top_p` 等 LLM 控制参数** |
| **典型计费方式** | 按 **输入 + 输出 token 总数** 计费（单位：千 tokens）；不同模型单价不同（如 `qwen-turbo` < `qwen-plus` < `qwen-max`） | 按 **请求次数** 计费（与输入长度、模态复杂度解耦）；`qwen-mt-uni` 因含 OCR/ASR 步骤，单价高于 `qwen-mt` | 按 **单次调用** 计费（flat rate）；与输入长度、输出复杂度无关，体现“决策即服务”特性 |
| **上下文长度（最大）** | `qwen-turbo`: 8K, `qwen-plus`: 32K, `qwen-max`: 64K（输入+输出总和） | `qwen-mt` / `qwen-mt-image` / `qwen-mt-uni`: 输入文本 ≤ 8192 tokens；图像分辨率 ≤ 4096×4096；音频 ≤ 30 分钟 | 输入文本 ≤ 8192 tokens（以 [decision-model-preview 模型信息](../../raw/model-user-guide/support/model-studio-model-list/model-list-decision/decision-model-preview.md) 为准） |
| **工具调用能力** | • DashScope & Anthropic 接口：支持自定义工具函数注册与调用<br>• OpenAI 兼容-Responses：仅支持平台预置工具（搜索、代码解释器），不可扩展 | **不支持任何工具调用**；所有能力（OCR/ASR/翻译/排版）已内置于模型流水线中 | **不支持工具调用**；模型行为完全固化，无外部交互扩展点 |

## 各方案适用场景建议

### ✅ 选择 Qwen 通用文本生成模型（API）当：
- 需要构建智能对话助手、知识问答系统、内容创作工具或代码辅助应用；
- 业务逻辑依赖动态工具编排（如实时联网搜索、执行 Python 代码、解析网页）；
- 已有 OpenAI 或 Anthropic SDK 生态，追求最小迁移成本；
- 需要精细控制生成过程（如通过 `temperature` 调节创造性，`repetition_penalty` 抑制重复）；
- 场景对响应延迟敏感，且能接受[流式输出](../concepts/streaming-output.md)提升用户体验。

> **慎用提示**：若仅需简单问答或固定模板生成，`qwen-turbo` 性价比最优；若需强推理或长文档理解，应选用 `qwen-plus` 或 `qwen-max` 并注意其上下文窗口限制。

### ✅ 选择 Qwen 多模态翻译模型（MT）当：
- 核心需求是**高质量、格式保真的跨语言转换**，而非通用生成；
- 输入源高度异构：PDF 技术文档、带表格的扫描件、会议录音转文字、电商商品图等；
- 要求“所见即所得”翻译效果（如保留原文段落缩进、表格行列结构、图文相对位置）；
- 需要开箱即用的 OCR/ASR 能力，且不愿自行集成第三方服务；
- 业务流程中翻译是独立环节（如本地化流水线、合规审查前置步骤）。

> **慎用提示**：`qwen-mt` 仅处理纯文本，勿用于图片；`qwen-mt-uni` 功能最强但成本最高，建议先用 `qwen-mt-image` 验证图像翻译需求是否满足。

### ✅ 选择 决策模型（Decision Model）当：
- 任务本质是**二元判断或有限类别分类**，且结果需具备可解释性与高置信度（如：“该内容是否违规？”、“用户风险等级是高/中/低？”、“交易是否应拦截？”）；
- 需要将 AI 判断无缝嵌入自动化策略引擎（如风控规则链、内容审核工作流、AB 实验分流器）；
- 对输出格式有强约束：必须返回标准化 JSON 结构，便于下游系统直接解析 `label` 和 `confidence` 字段；
- 不需要自由文本生成，也无需模型“思考过程”，只需一次调用给出确定结论；
- 运维要求极简：无需管理 prompt 工程、温度参数或对话历史。

> **慎用提示**：该模型**不可用于开放域问答、创意写作、摘要生成等泛化任务**；其能力边界由预置决策逻辑严格限定，无法通过 prompt 扩展。

## 开发者技术选型参考指南

| 你的需求 | 推荐模型 | 关键理由 | 风险提示 |
|----------|-----------|-----------|-----------|
| 构建客服对话机器人，需接入企业知识库并调用内部 API | ✅ Qwen API（DashScope 原生） | 支持 `tool_use` 自定义函数、完整上下文管理、细粒度参数控制 | 避免使用 OpenAI 兼容-Responses，因其工具不可扩展且 `max_tokens` 行为特殊 |
| 将海外电商平台商品页（含 HTML 表格+多图）批量翻译为中文 | ✅ Qwen MT（`qwen-mt-uni`） | 原生支持 HTML/PDF/图片混合输入，自动 OCR+翻译+格式重建 | `qwen-mt` 无法处理图片，`qwen-mt-image` 无法处理 PDF，务必选 `uni` |
| 在支付风控系统中，实时判定一笔转账是否属于欺诈模式 | ✅ 决策模型 | 输出含 `is_true` 布尔值与 `confidence` 标量，可直接驱动拦截策略；无 token 计费波动风险 | 切勿用 Qwen API 替代——其输出为自由文本，需额外 NLP 解析，引入延迟与错误率 |
| 快速将现有 OpenAI 应用迁移到百炼，仅需替换 endpoint 和 key | ✅ Qwen API（OpenAI 兼容 `/v1/chat/completions`） | 完全遵循 OpenAI 规范，SDK 零修改即可运行 | 注意 `max_tokens` 在 OpenAI-Responses 接口中的实际含义差异，避免截断误判 |
| 为内部员工培训系统生成个性化学习路径（需理解课程文档并规划步骤） | ✅ Qwen API（`qwen-plus` 或 `qwen-max`） | 强大的长上下文理解与规划能力，支持多轮迭代生成 | `qwen-turbo` 上下文仅 8K，可能无法加载完整课程材料 |

> **终极原则**：  
> - **选“能力”而非“名字”**：`qwen-plus` 是通用模型，`qwen-mt-plus` 并不存在；MT 和 Decision 是独立模型家族，与 Qwen 主干模型无继承关系。  
> - **看输入输出契约**：若你的上游系统输出是 Base64 图片、下游系统消费的是 `{"label": "high_risk", "confidence": 0.98}`，则无需考虑其他选项。  
> - **计费模式决定 TCO**：高频短文本决策 → 决策模型更省；低频长文档翻译 → Qwen MT-uni 单次计费更稳；中等频率生成任务 → 按 token 计费的 Qwen API 更灵活。  

请始终以 [百炼官方 API 文档](https://help.aliyun.com/zh/dashscope) 中最新公布的接口行为为准，并在生产环境上线前完成全链路压测与异常 case 验证。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


