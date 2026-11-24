# Qwen 基础模型与 Qwen MT 翻译模型对比

本文旨在帮助开发者清晰区分百炼平台上两类核心能力：**通用大语言模型（Qwen 基础模型）** 与 **专业机器翻译模型（Qwen MT 系列）**。二者虽同属 Qwen 技术体系，但在设计目标、输入输出范式、协议支持、计费逻辑及适用场景上存在本质差异。本对比基于百炼平台最新 API 规范（2024 年 Q4 版本），聚焦技术选型关键决策点，避免功能误用或架构冗余。

## 关键维度对比

| 维度 | Qwen 基础模型（如 `qwen4-max`、`qwen3.8-plus`、`qwen3-vl-plus` 等） | Qwen MT 翻译模型（`qwen-mt-plus`、`qwen-mt-image-2.0`、`qwen-mt-uni`） |
|------|------------------------------------------------------------------|------------------------------------------------------------------------|
| **核心定位** | 通用人工智能底座：支持文本生成、多模态理解、工具调用、深度推理、代码执行等泛化任务 | 专业翻译引擎：面向生产级本地化需求，提供高精度、可定制、多模态的端到端翻译服务 |
| **输入格式** | - OpenAI/Anthropic 协议：`messages` 数组（含 `role`/`content`/`tool_calls` 等）<br>- DashScope 协议：`input` 字符串或结构化对象（支持 `image`/`video`/`audio` 字段） | - `qwen-mt-plus`：纯文本字符串或数组，通过 `translation_options` 携带参数<br>- `qwen-mt-image*`：图像 URL 或 Base64，需 `X-DashScope-Async` 控制同步/异步<br>- `qwen-mt-uni`：支持 `input.fileUrl`（PDF/DOCX/JPG/MP3 等）或 `input.source_texts`（文本数组） |
| **输出格式** | - Chat/Responses/Anthropic：标准 JSON，含 `choices[0].message.content` 或 `content` 数组<br>- DashScope：`output.text` 或 `output.choices[0].message.content`，多模态结果嵌套在 `output` 中 | - 同步调用（`qwen-mt-plus`）：返回 `translated_text` 字符串或数组<br>- 异步调用（`qwen-mt-image*`/`qwen-mt-uni`）：返回 `task_id`，需轮询 `GET /api/v1/tasks/{id}` 获取结果；成功时返回 `TranslatedTexts`（文本）或 `TranslatedFileUrl`（文件） |
| **支持模型** | `qwen4-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3-vl-plus`、`qwen3.8-omni-flash`、`qwen-audio`、`qwen-math` 等全系列基础模型 | `qwen-mt-plus`（文本）、`qwen-mt-image`/`qwen-mt-image-2.0`（图像）、`qwen-mt-uni`（全模态统一模型）——**不支持基础模型 ID 直接用于翻译任务** |
| **API 端点** | - OpenAI 兼容：`POST /compatible-mode/v1/chat/completions`<br>- Responses：`POST /compatible-mode/v1/responses`<br>- Anthropic：`POST /apps/anthropic/v1/messages`<br>- DashScope：`POST /api/v1/services/aigc/text-generation/generation` 等 | - `qwen-mt-plus`：复用 OpenAI Chat 端点（`/chat/completions`），但 `model=qwen-mt-plus`<br>- `qwen-mt-image*` 与 `qwen-mt-uni`：DashScope 原生端点：<br> ✓ 图像：`POST /api/v1/services/aigc/image2image/image-synthesis`<br> ✓ 全模态：`POST /api/v1/services/aigc/multimodal-generation/generation` |
| **计费方式** | 按 **输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md)** 计费（单位：千 [Token](../concepts/token.md)），多模态输入按像素/帧数折算为等效 Token；音频/视频按时长分段计费 | 按 **请求次数 + 文件大小/页数/时长** 计费：<br>- 文本：按字符数（UTF-8 编码）计费<br>- 图像：按分辨率（像素）和尺寸（MB）阶梯计费<br>- 文档/音视频：按文件大小（MB）和页数/时长综合计费<br>**不按 Token 计费** |
| **关键定制能力** | - 工具调用（联网搜索、代码解释器、知识库检索）<br>- `system` 提示与 `thinking` 推理块<br>- 显式缓存（`cache_control`）与会话缓存（`x-dashscope-session-cache`） | - 术语强制干预（`terms`/`glossary`/`terminologies`）<br>- 领域提示（`ext.domainHint`，仅英文）<br>- 敏感词过滤（`ext.sensitives`）<br>- 图像主体分割（`ext.config.imageSegment`）<br>- 翻译记忆（`tm_list`） |
| **典型场景** | - 智能客服对话系统<br>- 多步骤 Agent（如旅行规划、数据分析）<br>- 代码生成与解释<br>- PDF/图像内容摘要与问答<br>- 数学推理与公式求解 | - 跨语言文档本地化（PDF/Word/PPT 批量翻译）<br>- App 截图/宣传图自动中英互译<br>- 电商商品图多语种标签生成<br>- 会议字幕实时翻译（音频输入）<br>- 法律/医疗等垂直领域术语一致性翻译 |

## 适用场景建议

### ✅ 选择 Qwen 基础模型，当您需要：
- 构建具备**上下文理解、多轮交互、自主决策**能力的 AI 应用（如智能助手、Agent 工作流）；
- 对非结构化内容（如长文档、复杂图表、短视频）进行**开放式分析、总结、改写或问答**；
- 调用外部工具链（如搜索、计算、数据库查询）完成复合任务；
- 利用 `reasoning.effort` 或 `thinking.type` 控制深度推理强度；
- 使用 `previous_response_id` 实现可追溯、可审计的多轮会话管理。

### ✅ 选择 Qwen MT 翻译模型，当您需要：
- 实现**高保真、低延迟、强可控**的专业翻译，尤其涉及排版还原（图像）、格式保留（文档）、术语统一（行业）；
- 处理**多模态混合输入**（如一张含中英双语的说明书 PDF + 附带的 JPG 示意图），期望统一接口、一致输出；
- 在翻译中**强制注入客户专属术语表**（如品牌名、产品型号、合规表述），并确保 100% 覆盖；
- 对敏感内容（如政治、宗教、隐私字段）执行**原文透传策略**，避免误译风险；
- 批量处理企业级文档资产（>1000 页 PDF、数百张产品图），要求异步队列、失败重试与文件直链下载。

### ⚠️ 避免混淆的典型误区：
- ❌ 不要用 `qwen4-max` 模型调用 `/chat/completions` 端点去“硬提示”做翻译（如 `"请将以下中文翻译成英文：..."`）——效果不稳定、无术语控制、不支持图像/文档、Token 成本高、无敏感词过滤；
- ❌ 不要将 `qwen-mt-plus` 模型用于非翻译类任务（如问答、摘要）——其架构未优化通用生成，响应质量与鲁棒性远低于基础模型；
- ❌ 不要期望 `qwen-mt-uni` 支持 `tool_use` 或 `system` 提示——它专为翻译流水线设计，无通用 LLM 的指令遵循能力。

## 技术选型参考（面向开发者）

| 您的业务需求 | 推荐方案 | 关键依据 |
|--------------|----------|----------|
| 需要为海外用户构建多语言客服机器人，支持中英日韩切换，并能根据对话历史推荐产品 | ✅ Qwen 基础模型（`qwen4-max` + Responses API）<br>❌ Qwen MT | 客服需理解意图、调用知识库、生成自然回复；MT 模型无法处理对话状态与工具调用 |
| 需将公司官网 HTML 页面（含图片、表格、CSS 样式）一键翻译为西班牙语，保持原始布局与超链接 | ✅ Qwen MT `qwen-mt-uni`<br>❌ Qwen 基础模型 | `qwen-mt-uni` 原生支持 HTML 输入与格式保留输出；基础模型需先提取文本再拼接，丢失结构且无法处理内嵌图片文字 |
| 开发一款手机 App，用户拍照上传菜单图片，实时返回带翻译文字的标注图 | ✅ Qwen MT `qwen-mt-image-2.0`<br>❌ Qwen 基础模型（`qwen3-vl-plus`） | `qwen-mt-image-2.0` 内置 OCR+重排版+翻译一体化流水线，输出即用标注图；VL 模型仅能返回翻译文本，需额外开发图像合成模块 |
| 为内部研发团队提供一个“代码注释翻译器”，将 Python 源码中的中文 docstring 自动转为英文，同时保留函数签名与缩进 | ✅ Qwen 基础模型（`qwen3.8-flash` + Chat API）<br>✅ 或 `qwen-mt-plus`（若仅需纯文本且强调术语一致性） | 若需理解代码上下文（如变量作用域、类继承关系）以提升注释准确性，选基础模型；若仅做字面翻译且已有严格术语表，`qwen-mt-plus` 更轻量、成本更低、支持 `tm_list` |
| 构建跨境电商后台系统，需批量翻译 5000+ 商品描述（含标题、详情、规格表），并确保品牌词（如 “X-Tech Pro”）100% 不变 | ✅ Qwen MT `qwen-mt-plus`（文本）或 `qwen-mt-uni`（含附件图）<br>❌ 基础模型 | `qwen-mt-plus` 支持 `translation_options.terms` 精确干预，且按字符计费更透明；基础模型无法保证术语零误差，且 Token 成本不可控 |

> **最后建议**：对于混合型需求（如“先用 Qwen VL 理解图像内容，再调用 MT 模型翻译其中文字”），应采用**组合调用模式**——通过百炼工作流（Workflow）或自建服务编排，分别调用最适配的模型，而非强行让单一模型承担全部职责。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


