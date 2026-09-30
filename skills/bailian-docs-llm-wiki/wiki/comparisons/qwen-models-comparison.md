# Qwen系列大模型能力对比

为帮助开发者在百炼平台上高效选型，本文系统对比 Qwen 系列中三类核心能力模型的调用方式、能力边界与适用场景：  
- **通用大语言模型（Qwen3.x 系列）**：面向开放生成、多轮对话、工具协同等综合任务；  
- **全模态翻译模型（Qwen-MT-Uni）**：专注端到端、保格式、跨模态的高保真翻译；  
- **结构化决策模型（decision-model-preview）**：专为低延迟、高确定性、非生成类判断任务设计。  

对比聚焦实际开发关切点——协议兼容性、输入/输出形态、模型灵活性、计费逻辑与工程约束，避免概念泛化，直击技术选型关键决策因子。

---

## 关键维度对比表

| 维度 | Qwen 通用大模型（如 `qwen3.8-max`, `qwen3-vl-plus` 等） | Qwen-MT-Uni 翻译模型 | decision-model-preview 决策模型 |
|------|--------------------------------------------------------|------------------------|----------------------------------|
| **输入格式** | • OpenAI 兼容：`messages` 数组（支持 `text`/`image_url`/`video_url`/`input_audio`）<br>• DashScope 原生：`input`（`string` 或 `array`），支持 `ResponseOutputMessage` 多轮结构<br>• Anthropic 兼容：`messages` + `tools` schema | • 同步：`input.source_texts`（字符串或数组）或 `input.fileUrl`（HTTPS 公开 URL）<br>• 异步：仅支持 `input.fileUrl`<br>• 支持 PDF/DOCX/PPTX/XLSX/HTML/Markdown/JPG/PNG/MP3/WAV 等 10+ 格式 | • `state`：任意结构化数据（JSON 对象/数组/字符串），最大 65536 token<br>• `questions`：键值对对象，每个 question 定义 `type`（`choice`/`noul`/`score`）、`criteria`（选项集/评分描述） |
| **输出格式** | • OpenAI 兼容：标准 `choices[].message` + `usage`<br>• Anthropic 兼容：`content[]`（含 `tool_use`/`tool_result`）+ `usage`<br>• 结构化输出：支持 `output_config.format.type = "json_schema"`（强校验）或提示词驱动 JSON | • 同步：`output.Data.TranslatedTexts`（文本数组）或 `output.Data.TranslatedFileUrl`（文件 URL）<br>• 异步：轮询 `/api/v1/tasks/{task_id}` 获取 `TranslatedFileUrl`（24 小时有效）<br>• 输出严格保持原始格式（如 `.pdf` → `.pdf`） | • 严格结构化 JSON：<br>  – `choice`: `{selected: key, probabilities: {key: prob}, confidence: 0.0–1.0}`<br>  – `noul`: `{probability_yes: float}`<br>  – `score`: `{expected_score: float, level_probabilities: [p1,p2,...], confidence: float}`<br>• **无任何自由文本生成** |
| **支持模型** | • 全量 Qwen 系列：`qwen3.8-max`, `qwen3.7-plus`, `qwen3.5-flash`, `qwen3-vl-plus`, `qwen3-coder-next`, `qwen3.8-omni-flash` 等<br>• 第三方模型：DeepSeek、GLM、Kimi（需控制台开通）<br>• **Qwen-Audio 仅 DashScope 原生协议支持** | • **唯一模型**：`qwen-mt-uni`（无别名，不支持其他 Qwen 变体） | • **唯一模型**：`decision-model-preview`（预览版，无历史版本或别名） |
| **API 端点** | • OpenAI 兼容：`/compatible-mode/v1/chat/completions`（Chat）或 `/compatible-mode/v1/responses`（带工具）<br>• Anthropic 兼容：`/v1/messages`<br>• DashScope 原生：`/text-generation/generation`（文本）或 `/multimodal-generation/generation`（多模态） | • 统一端点：`/api/v1/services/aigc/multimodal-generation/generation`<br>• 通过请求头 `X-DashScope-Async: enable` 切换同步/异步模式 | • 统一端点：`POST /compatible-mode/v1/systemone`（固定路径，无 `/v1/models` 发现接口） |
| **计费方式** | • 按 `input_tokens + output_tokens` 计费<br>• `usage` 中细分：`cached_tokens`（缓存命中）、`reasoning_tokens`（思考过程）、`document_tokens`/`image_tokens`/`audio_tokens`（多模态） | • 按 `input_tokens + output_tokens` 总量计费<br>• `usage.input_tokens_details` 显式区分 `document_tokens`/`image_tokens`/`audio_tokens`/`character_tokens`，支持细粒度成本归因 | • 按 `input_tokens` 计费（**output 不计费**）<br>• `usage.input_tokens` 为实际消耗 token 数，超长 `state` 截断后按截断后长度计费 |
| **典型场景** | • 智能客服多轮对话<br>• 多模态内容理解（图文问答、视频摘要）<br>• 工具增强型 Agent（代码执行、网页搜索）<br>• 结构化数据生成（JSON Schema 输出） | • 跨语言文档本地化（PDF 技术手册→日文）<br>• 会议纪要音频转译+翻译<br>• PPT/Excel 批量双语交付<br>• 含敏感词/术语的合规翻译（支持 `glossary` 与 `sensitives`） | • 工单智能分派（“归属团队：A/B/C”）<br>• 内容安全审核（“是否违规：yes/no”）<br>• 用户意图路由（“下一步动作：查询/退款/投诉”）<br>• 服务质量评分（“响应及时性：1–4 分”） |

---

## 各方案适用场景建议

### ✅ 选择 Qwen 通用大模型（`qwen3.x` 系列）当：
- 任务需要**开放式文本生成**（如创作、摘要、改写）；
- 输入包含**混合模态**（图像+文本、视频+语音、多图对比）且需联合推理；
- 需要**内置工具调用能力**（如实时搜索、代码沙箱执行）；
- 已有 OpenAI/Anthropic SDK 生态，追求**最小迁移成本**；
- 要求**强结构化输出保障**（如金融报告字段提取，需 `json_schema` 校验）。

> ⚠️ 注意：若仅需纯翻译，Qwen 通用模型效果与效率均显著低于 `qwen-mt-uni`；若仅需是非判断，其延迟与成本远高于 `decision-model-preview`。

### ✅ 选择 Qwen-MT-Uni 当：
- 核心目标是**保格式、保结构、保语义的端到端翻译**（非简单文本替换）；
- 输入源为**真实业务文档**（PDF 合同、PPT 方案、XLSX 表格、含图表的 HTML）；
- 需处理**长音频（≤60 分钟）或大文档（≤200 页）**，且接受异步工作流；
- 有**领域术语强约束**（如医疗器械术语表）或**敏感信息过滤需求**（如客户姓名脱敏）；
- 要求输出与输入**格式完全一致**（如翻译后的 `.docx` 仍可直接编辑）。

> ⚠️ 注意：不适用于需要生成解释、润色或上下文扩展的翻译任务；不支持自定义模型或微调。

### ✅ 选择 decision-model-preview 当：
- 任务本质是**确定性分类/判断/打分**，且**无需生成解释性文字**；
- 对**延迟敏感**（P99 < 500ms）与**高并发稳定**有硬性要求（如每秒万级工单分流）；
- 需要**可解释的概率分布**（如“选择 A 的置信度为 92%”，而非模糊的“可能选 A”）；
- 输入数据已高度结构化（如工单 JSON、用户行为日志），无需 NLU 解析；
- 追求**极致成本效益**——相同决策任务，其 token 消耗仅为通用模型的 1/10～1/5。

> ⚠️ 注意：不支持流式响应；不支持自由文本输出；`score` 类型强烈建议使用 3–7 级量表以保障置信度。

---

## 开发者技术选型参考

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我已有 OpenAI SDK，想快速接入 Qwen 最强模型做客服对话” | ✅ Qwen 通用模型（OpenAI 兼容 `/responses`） | 协议零改造，自动获得 `web_search`/`code_interpreter` 工具链，`qwen3.8-max` 提供当前最高综合能力 |
| “我要把 500 页英文产品手册 PDF 翻译成中文，并保留所有目录、表格和图片位置” | ✅ Qwen-MT-Uni（异步调用） | 唯一支持 PDF→PDF 端到端保格式翻译的模型，自动识别版式，术语表与敏感词策略完备 |
| “我需要实时判断用户消息是否含欺诈关键词，并路由到风控团队，P99 延迟必须 < 300ms” | ✅ decision-model-preview | 专用决策模型，无文本生成开销，`noul` 类型直接返回 `probability_yes`，延迟稳定且可预测 |
| “我想让模型看一张商品图，再回答‘这个是否符合欧盟 CE 认证标准？’并给出依据” | ✅ Qwen 通用模型（`qwen3-vl-plus` 或 `qwen3.8-omni-flash`） | 多模态理解 + 开放推理 + 文本生成三位一体，`qwen3.8-omni-flash` 还支持视频/音频输入扩展 |
| “我需要将一段中文语音转文字后再翻译成英文，但不想自己拼接 ASR+MT 服务” | ✅ Qwen-MT-Uni（同步调用，传 `input.fileUrl` MP3） | 全模态统一入口，自动完成语音识别→翻译→输出英文文本，省去中间格式转换与状态管理 |

**最后建议**：  
- **优先验证 API 协议匹配度**：检查现有 SDK 是否原生支持 OpenAI/Anthropic/DashScope 协议，避免手动封装成本；  
- **务必压测 Token 消耗**：通用模型的 `input_tokens` 在多模态场景下增长极快（尤其高分辨率图/长视频），Qwen-MT-Uni 和 decision-model-preview 的计费结构更可预测；  
- **生产环境强制启用缓存**：Qwen 通用模型通过 `x-dashscope-session-cache: enable`（OpenAI）或 `cache_control`（Anthropic）可显著降本，Qwen-MT-Uni 与 decision-model-preview 本身无缓存机制，需应用层实现。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


