# 通义大模型能力矩阵对比：通用大模型、机器翻译模型与决策模型

为帮助开发者在百炼平台上快速识别并选用最匹配业务需求的大模型服务，本文系统对比三类核心能力模型：**通用大模型（Qwen 系列）**、**专业机器翻译模型（Qwen-MT 系列）** 和 **专用决策模型（decision-model-preview）**。三者虽同属通义大模型生态，但在设计目标、输入输出契约、协议支持、能力边界及计费逻辑上存在本质差异。本对比聚焦技术可落地性，面向工程选型提供客观、可验证的参考依据。

## 能力矩阵对比表

| 维度 | 通用大模型（Qwen 系列） | 机器翻译模型（Qwen-MT 系列） | 决策模型（decision-model-preview） |
|------|------------------------|------------------------------|-----------------------------------|
| **核心定位** | 通用认知与生成能力：对话理解、内容创作、多模态推理、工具调用、代码生成等 | 专业语言转换能力：高保真、可定制、多模态（文本/图像/文档/音频）端到端翻译 | 专用逻辑判定能力：结构化分类、置信度评分、是非判断，面向风控、合规、策略路由等确定性任务 |
| **典型支持模型** | `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3-vl-plus`、`qwen3.8-omni-flash`、`deepseek-v4.1-flash`、`kimi-k3.1-pro` 等全系千问及第三方直供模型 | `qwen-mt-plus`（文本）、`qwen-mt-image-2.0`（图像）、`qwen-mt-uni`（全模态统一） | `decision-model-preview`（当前唯一公开可用型号） |
| **输入格式** | 多模态灵活组合：<br>• OpenAI 协议：`messages` 数组（含 `text`/`image_url`/`audio_url`）<br>• Responses 协议：`input` 对象（支持 `input_text`/`input_image`/`input_video` 等结构化字段）<br>• DashScope 协议：嵌套于 `input.messages` 的标准数组 | 按模型类型严格区分：<br>• `qwen-mt-plus`：纯文本字符串或数组，通过 `translation_options` 传参<br>• `qwen-mt-image-*`：图像二进制或 `image_url`（JPG/PNG 等）<br>• `qwen-mt-uni`：`fileUrl`（PDF/DOCX/JPG/MP3 等）或 `source_texts`（字符串/数组） | 严格单字段输入：<br>• `input`: 字符串（≤8192 字节，超长静默截断）<br>• 不支持图片、音频、文件 URL 或多轮上下文 |
| **输出格式** | 非结构化为主，支持可选结构化：<br>• 默认返回自由文本流或完整响应<br>• OpenAI/Anthropic 协议支持 `response_format: { "type": "json_object" }`（部分模型如 `deepseek-v4.1-flash` 不支持）<br>• Responses API 支持 `reasoning.effort` 控制思考深度 | 格式强绑定业务语义：<br>• `qwen-mt-plus`：返回 `choices[0].message.content` 中的译文字符串<br>• `qwen-mt-image-*`：返回带坐标信息的 `output.texts` 或 `output.image_url`<br>• `qwen-mt-uni`：同步返回 `TranslatedTexts` 或 `TranslatedFileUrl`，异步需轮询任务结果 | 严格结构化 JSON（System One 协议）：<br>• 必含字段：`label`（string）、`score`（float, 0.0–1.0）、`is_true`（boolean）<br>• 可选字段：`probabilities`（对象，仅当 `labels` 显式传入时返回） |
| **API 协议支持** | ✅ 全协议支持：<br>• OpenAI 兼容（`/compatible-mode/v1/chat/completions` / `/responses`）<br>• Anthropic 兼容（`/apps/anthropic/v1/messages`）<br>• DashScope 原生（`/api/v1/services/aigc/text-generation/generation` 等） | ⚠️ 协议受限：<br>• `qwen-mt-plus`：仅 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（通过 `extra_body.translation_options`）<br>• `qwen-mt-image-*` 与 `qwen-mt-uni`：仅 DashScope 原生接口（`/api/v1/services/aigc/image2image/...` / `/multimodal-generation/...`）<br>• **不支持 Anthropic 兼容协议** | ❌ 单一协议：<br>• 仅 System One 原生 HTTP 接口（`POST /api/v1/services/aigc/decision/decision`）<br>• **不兼容 OpenAI 或 Anthropic SDK**，需手动构造 JSON 请求体 |
| **关键控制参数** | `reasoning.effort` / `output_config.effort`（思考强度）<br>`stream`（流式）<br>`store` / `previous_response_id`（多轮管理）<br>`fps` / `max_pixels`（多模态预处理） | `source_lang` / `target_lang`（语种）<br>`glossary` / `terminologies`（术语干预）<br>`domainHint`（领域提示，英文）<br>`sensitives`（敏感词过滤）<br>`imageSegment`（图像主体跳过） | `labels`（显式候选标签集，**强烈建议必填**）<br>`threshold`（置信阈值，默认 0.5）<br>无 `stream`、`temperature`、`max_tokens` 等生成类参数 |
| **计费方式** | 按 token 计费：<br>• 输入 + 输出 tokens 总和计费<br>• 多模态输入按等效文本 token 折算（如图像按分辨率、帧率折算）<br>• 流式响应按实际返回 token 计费 | 按请求次数 + 内容规模分层计费：<br>• `qwen-mt-plus`：按字符数计费（千字单价）<br>• `qwen-mt-image-*`：按图像分辨率与尺寸阶梯计费<br>• `qwen-mt-uni`：按输入文件类型与大小计费（如 PDF 页数、音频时长） | 按成功调用次数计费：<br>• 每次返回合法 JSON（含 `label`/`score`/`is_true`）即计 1 次<br>• `is_true=false` 或 `score<0.5` 仍计费<br>• 4xx/5xx 错误请求不计费 |
| **典型场景** | • 智能客服对话引擎<br>• 多模态内容生成（图文混排报告、音视频摘要）<br>• Agent 工作流（联网搜索+代码执行+文件分析）<br>• 技术文档问答与代码辅助 | • 跨境电商商品详情页批量翻译<br>• 手册/合同/PPT 图像内嵌文字精准翻译<br>• 本地化流水线：自动识别 PDF/Word/MP3 并输出格式一致的译文文件 | • 金融信贷申请风险等级判定（high/medium/low）<br>• 社交平台内容安全审核（合规/可疑/违规）<br>• 客服工单自动路由（售前/售后/投诉） |

## 各方案适用场景建议

- **选择通用大模型（Qwen 系列）当且仅当**：  
  你的任务需要**开放性生成、多轮交互、工具协同或复杂推理**。例如构建一个能“先查天气、再推荐穿搭、最后生成购物清单”的智能助手；或对一份带图表的财报 PDF 进行总结并生成可视化建议。此时应优先使用 `qwen3.8-omni-flash`（多模态）或 `qwen3.8-max`（强推理），并通过 Responses API 启用 `web_search` 和 `file_search` 工具。

- **选择机器翻译模型（Qwen-MT 系列）当且仅当**：  
  你的核心诉求是**高精度、可干预、格式保真的语言转换**，且输入形态明确。例如：  
  ✓ 将 1000 份中英双语技术手册 PDF 自动翻译为日文，并保留目录结构与表格样式 → 用 `qwen-mt-uni`；  
  ✓ 对 App 截图中的按钮文案实时翻译，要求跳过 Logo 文字 → 用 `qwen-mt-image-2.0` + `imageSegment=true`；  
  ✗ 不要用于“根据用户提问生成一段英文解释”——这是通用模型的职责，非翻译任务。

- **选择决策模型（decision-model-preview）当且仅当**：  
  你的业务规则可被抽象为**有限、明确、互斥的分类标签**，且需要**确定性、低延迟、可审计的判定结果**。例如：  
  ✓ 判定一条用户评论是否含辱骂词汇（`label: "toxic"` / `"non-toxic"`）；  
  ✓ 根据交易流水特征输出反洗钱风险等级（`"low"`/`"medium"`/`"high"`）；  
  ✗ 不要用于“生成一段风控建议文案”或“解释判定理由”——该模型不产生自然语言解释，仅输出结构化决策信号。

## 开发者技术选型参考

| 选型问题 | 推荐答案 | 关键依据 |
|----------|----------|----------|
| **我的项目已用 OpenAI SDK，想最小改造接入** | 优先评估通用大模型（[OpenAI 兼容接口](../concepts/openai-compatibility.md)）或 `qwen-mt-plus`（OpenAI 兼容文本翻译）；避免 `qwen-mt-image`/`qwen-mt-uni` 和决策模型（需重写 HTTP 客户端） | `qwen-mt-plus` 是唯一支持 OpenAI 协议的翻译模型；决策模型无 SDK 兼容层 |
| **我需要处理 PDF/图片/音频等非文本输入** | 通用大模型（`qwen3-vl-plus`, `qwen3.8-omni-flash`）或 `qwen-mt-uni`；**不可用决策模型** | 决策模型仅接受字符串输入；通用模型与 `qwen-mt-uni` 均原生支持多模态解析 |
| **我要求输出必须是 JSON，且字段名/类型严格固定** | 决策模型（强制 System One schema）或通用模型（启用 `response_format: json_object`，但需确认模型支持） | `qwen-mt-plus` 输出为自由文本；`qwen-mt-uni` 输出结构依赖输入类型，不保证统一 schema |
| **我需要历史对话上下文管理** | 仅通用大模型（Responses API 的 `previous_response_id` 或手动拼接 `messages`） | 翻译与决策模型均为 stateless 单次请求，无上下文概念 |
| **我需对输出结果做 A/B 测试或灰度发布** | 通用大模型（可通过 `model` 参数动态切换 `qwen3.8-flash`/`qwen3.7-plus`）或 `qwen-mt-plus`（切换不同术语表 `tm_list`） | 决策模型当前仅 `decision-model-preview` 一个版本，无灰度能力；`qwen-mt-image`/`qwen-mt-uni` 无模型变体 |
| **我关注成本确定性与可预测性** | 决策模型（按次计费，无 token 波动） > `qwen-mt-plus`（按字符计费） > 通用大模型（token 数受 prompt/length/temperature 影响大） | 通用模型输出长度不可控，易因 `max_tokens` 设置不当导致意外高消耗；决策模型每次调用成本恒定 |

> **重要提醒**：所有模型均需通过百炼工作空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）调用以保障性能与稳定性；三方直供模型（DeepSeek/Kimi/GLM）仅在中国站华北2（北京）地域可用，且需在控制台单独开通服务。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


