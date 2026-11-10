# 翻译模型与决策模型能力对比

本文旨在帮助开发者清晰区分百炼平台中两类关键能力模型——**翻译模型（Qwen-MT-Uni）** 与 **决策模型（decision-model-preview）** 的设计目标、技术边界与适用范式。二者虽同属 AIGC 服务，但底层任务定义、输入输出语义、调用机制及计费逻辑存在根本性差异。错误混用（如用决策模型做翻译、或用翻译模型做工单分类）将导致接口调用失败、结果不可解析、资源浪费甚至业务逻辑中断。本对比聚焦可落地的技术选型维度，为架构设计、API 集成与成本优化提供明确依据。

## 关键能力维度对比

| 维度 | 翻译模型（`qwen-mt-uni`） | 决策模型（`decision-model-preview`） |
|------|---------------------------|----------------------------------------|
| **核心任务类型** | 跨模态内容保形转换（语言+格式映射） | 结构化确定性推理（分类/是非/评分） |
| **输入格式** | 多模态：文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV（共10类）；支持 `fileUrl` 或 `source_texts` | 单一结构化上下文：`state`（任意 JSON 可序列化对象/字符串/数组），最大 65536 tokens；不接受二进制文件或 URL |
| **输出格式** | 严格对应输入模态：<br>• 文本 → `TranslatedTexts`（字符串/数组）<br>• 文件 → `TranslatedFileUrl`（HTTPS 下载链接）<br>• 图像/音频 → 原格式译后文件 | 纯结构化 JSON：<br>• `choice`: `{ "selected": "key", "probabilities": { "key": 0.92, ... }, "confidence": 0.98 }`<br>• `noul`: `{ "probability_yes": 0.73 }`<br>• `score`: `{ "expected_score": 2.4, "probabilities": [0.05, 0.22, 0.61, 0.12] }` |
| **支持模型** | 仅 `qwen-mt-uni`（无别名，无版本变体） | 仅 `decision-model-preview`（预览版，无其他型号） |
| **API 端点** | 同步/异步共用：<br>`POST /api/v1/services/aigc/multimodal-generation/generation`<br>（异步需 Header `X-DashScope-Async: enable`） | 统一端点：<br>`POST /compatible-mode/v1/systemone`<br>（仅同步阻塞调用，无异步模式） |
| **调用模式** | ✅ 同步（低延迟场景）<br>✅ 异步（大文档/长音频，需轮询 `/api/v1/tasks/{task_id}`） | ❌ 仅同步阻塞调用<br>❌ 不支持流式（`stream=true` 无效）<br>❌ 不支持[异步任务](../concepts/asynchronous-task.md)队列 |
| **计费方式** | 按 **实际消耗 token 数** 计费：<br>• `usage.input_tokens` + `usage.output_tokens`<br>• 含模态细分字段（如 `image_tokens_details`, `audio_tokens_details`） | 按 **单次请求** 计费：<br>• 无论 `questions` 数量（≤16）、`state` 大小（≤65536 tokens）或问题复杂度，均视为 1 次调用<br>• 无 token 粒度计费，无模态细分 |
| **典型场景** | • 多语言文档本地化（PDF 报告、PPT 方案、Excel 表格）<br>• 用户上传图片/截图的实时翻译<br>• 客服语音转写+翻译一体化处理<br>• 网页/Markdown 技术文档多语种发布 | • 工单智能分派（“归属团队：A/B/C/Other”）<br>• 内容安全审核（“是否含违规信息：yes/no/uncertain”）<br>• 智能体任务完成度判定（“完成度：1–5 分”）<br>• 对话意图路由（“用户诉求：咨询/投诉/退货”） |
| **关键扩展能力** | • 自动语言识别（`source_lang` 可省略）<br>• 领域提示（`domainHint`，**仅英文生效**）<br>• 术语表强制对齐（`glossary`）<br>• 敏感词原文保留（`sensitives`）<br>• 图像主体分割控制（`config.imageSegment`） | • 多问题并行决策（单请求最多 16 个 `questions`）<br>• 全类型概率分布返回（`probabilities`）<br>• 置信度量化（`confidence` for `choice`/`score`）<br>• 无文本生成（纯结构化输出，零幻觉） |

## 适用场景建议

### ✅ 推荐使用翻译模型（`qwen-mt-uni`）当：
- 输入是**真实业务文件或富媒体内容**（如合同 PDF、产品说明书 DOCX、培训 PPT、用户反馈截图 JPG、客服录音 MP3）；
- 输出需**保持原始排版、图表、公式、超链接等格式完整性**；
- 需要支持**混合语言自动识别**（如中英混排文档无需预标注源语言）；
- 有专业术语一致性要求（通过 `glossary` 强制对齐）；
- 处理耗时较长的任务（如 100 页 PDF 或 45 分钟会议录音），可接受异步轮询。

### ✅ 推荐使用决策模型（`decision-model-preview`）当：
- 输入是**结构化业务上下文**（如工单 JSON、对话历史数组、审核日志对象）；
- 输出需**机器可直接消费的确定性结构**（如数据库字段值、路由 key、置信度阈值判断）；
- 场景对**延迟敏感且结果必须可解释**（如实时风控拦截、客服会话中实时意图识别）；
- 需要**多维度并行判断**（如一次请求同时评估“是否紧急”、“是否需人工介入”、“推荐处理时长”）；
- 严禁文本生成（避免 LLM 幻觉干扰关键决策），只要概率分布与置信度。

### ⚠️ 明确不适用场景（避坑指南）：
- **勿用决策模型处理翻译需求**：它不接收文件、不输出译文、不理解语言转换规则，调用将直接报错 `InvalidParameter`。
- **勿用翻译模型做分类/评分**：其输出为自由文本或文件，无法直接提取 `confidence` 或 `probabilities`，且无结构化 schema 保证，下游解析成本高、可靠性低。
- **勿在决策模型中传入图像/音频 URL**：`state` 字段仅接受可 JSON 序列化的数据，二进制或 URL 将触发 `InvalidParameter`。
- **勿在翻译模型中省略 `target_lang`**：该参数为必填，缺失将导致 `MissingParameter` 错误（与决策模型的 `state`/`questions` 必填逻辑一致）。

## 技术选型参考（面向开发者）

| 选型考量点 | 翻译模型 | 决策模型 | 选型建议 |
|------------|----------|----------|----------|
| **输入数据形态** | 文件流/URL/多模态文本 | 纯 JSON 可序列化结构 | 若输入含二进制文件 → 选翻译模型；若输入为 API 返回的 JSON → 优先评估决策模型 |
| **输出集成方式** | 需下载文件或解析文本数组 | 直接读取 JSON 字段（如 `result.questions.q1.selected`） | 若下游是数据库写入/规则引擎 → 决策模型更轻量；若需交付给终端用户阅读 → 翻译模型 |
| **延迟容忍度** | 同步：≤2s（文本/小图）；异步：分钟级（大文件） | 同步：稳定 ≤800ms（实测 P95 < 600ms） | 实时交互场景（如聊天窗口内即时判断）→ 决策模型；离线批量处理 → 翻译模型异步更合适 |
| **SDK 依赖** | DashScope SDK 通用接口（`generation`） | 需 **特定版本 SDK**（Python ≥2.0.1 / Java ≥2.23.3） | 使用旧版 SDK 且无法升级 → 决策模型不可用，需改用通用 LLM + prompt engineering（不推荐） |
| **调试效率** | Playground 支持文件上传预览，但需注意格式限制（如 `.doc` 不支持） | Playground 提供预设模板（工单/审核/评分），支持 JSON 编辑与实时响应解析 | 初期验证推荐决策模型 Playground（零格式障碍）；翻译模型建议先用小文本测试再上文件 |
| **错误排查重点** | 关注 `code`（同步）或 `output.Success`（异步）+ `output.Code`；检查 `fileUrl` 合法性、格式兼容性 | 关注 `error.code`（如 `InvalidParameter`）、`questions` 数量超限、`state` token 超限（65536） | 翻译模型错误多源于**前置条件**（格式/URL/大小），决策模型错误多源于**参数结构**（JSON schema 违规） |

> **最后提醒**：两类模型均**不替代通用大语言模型（LLM）**。若业务需要生成解释性文本、摘要、创意文案或开放域问答，请选用 `qwen-max`、`qwen-plus` 等通用模型，并配合合适的 Prompt 工程与 RAG 架构。翻译与决策模型是百炼平台针对高频、确定性、高精度垂直场景提供的「能力原子」，善用它们可显著降低系统复杂度与推理成本。

## 被对比主题页

- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


