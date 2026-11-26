# Qwen 基础大模型与 Qwen 机器翻译模型对比

本文旨在帮助开发者清晰区分百炼平台上两类核心能力：**通用基础大模型（Qwen 系列）** 与 **垂直领域专用模型（Qwen MT 翻译系列）**。二者虽同属 Qwen 技术体系，但在设计目标、输入输出范式、能力边界、调用协议及计费逻辑上存在本质差异。本对比聚焦技术选型关键维度，避免功能误用（如用 `qwen-max` 做文档翻译导致格式错乱、术语丢失），提升集成效率与生产稳定性。

## 关键维度对比

| 维度 | Qwen 基础大模型（`qwen-*`） | Qwen 机器翻译模型（`qwen-mt-*`） |
|------|-----------------------------|-----------------------------------|
| **核心定位** | 通用语言理解与生成（LLM），支持对话、推理、代码、工具调用等泛化任务 | 专业机器翻译（MT），聚焦多模态内容的高保真语义转换与格式重构 |
| **支持模型** | `qwen-max`（旗舰）、`qwen-plus`（均衡）、`qwen-turbo`（轻量）、`qwen-coder`（代码） | `qwen-mt-plus`（纯文本）、`qwen-mt-image-2.0`（图像）、`qwen-mt-uni`（全模态统一入口） |
| **输入格式** | 严格遵循对话消息数组：`messages: [{ "role": "user", "content": "..." }]`；支持多轮上下文、系统提示、工具定义 | 多样化：<br>• 文本：`source_texts`（数组）或 `input.source_texts`<br>• 图像/文档/音频：`input.fileUrl`（公网 HTTPS 链接）<br>• 不支持自由对话历史或系统角色指令 |
| **输出格式** | 自由文本生成（`output.text` 或 `choices[0].message.content`），可启用 JSON Mode 输出结构化数据 | 格式感知强输出：<br>• 文本 → 纯翻译结果（含术语/敏感词处理）<br>• 图像 → 翻译后重排版图像（base64 或 URL）<br>• PDF/DOCX → 原格式文件（含翻译文本+保留样式）<br>• **不返回原始 LLM 式“思考过程”或无关解释** |
| **API 端点** | 统一使用文本生成端点：<br>`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（DashScope）<br>或 OpenAI 兼容 `/v1/chat/completions` | 按模态分离：<br>• 文本：OpenAI 兼容 `/v1/chat/completions`（需 `extra_body`）<br>• 图像/文档/音频：`/api/v1/services/aigc/multimodal-generation/generation`（`qwen-mt-uni`）或 `/api/v1/services/aigc/image2image/image-synthesis`（`qwen-mt-image-*`） |
| **关键参数差异** | `temperature`, `top_p`, `max_tokens`, `tools`, `tool_choice`, `response_format`（JSON Schema） | `source_lang`, `target_lang`, `input.fileUrl` / `input.source_texts`, `ext.domainHint`, `ext.sensitives`, `ext.glossary`（术语表）；**无 temperature/top_p 等生成控制参数** |
| **异步支持** | 支持流式响应（`stream: true`），但无传统“异步任务”概念（所有请求同步返回） | 明确区分同步/异步：<br>• `qwen-mt-image` **必须异步**（`X-DashScope-Async: enable`）<br>• `qwen-mt-uni` / `qwen-mt-image-2.0` 同步/异步均可，大文件推荐异步 |
| **计费方式** | 按 **总 token 数（输入 + 输出）** 计费（单位：千 tokens） | 按 **模态类型细分计费**：<br>• `qwen-mt-plus`：按 token 总量计费<br>• `qwen-mt-image-*`：按 **图像请求数（image_count = 1）** 固定计费<br>• `qwen-mt-uni`：按 `input_tokens` 计费，并细分为 `document_tokens`、`image_tokens`、`audio_tokens` 等子项 |
| **典型场景** | 客服对话机器人、智能写作助手、代码补全、RAG问答、[函数调用](../concepts/function-calling.md)自动化 | 电商商品图多语种标注、技术文档本地化交付、PDF合同双语对照、会议字幕实时翻译、APP截图国际化 |

## 适用场景建议

### ✅ 推荐选用 Qwen 基础大模型（`qwen-*`）当：
- 需要**多轮上下文理解与动态响应**（如用户追问、修正、切换话题）；
- 任务涉及**逻辑推理、数学计算、编程、创意生成**等非翻译类能力；
- 需调用外部工具（搜索、数据库、API）完成复杂工作流；
- 输入为自然语言指令，且输出需保持**开放性、创造性或解释性**（如“请分析这份财报并给出三点建议”）；
- 已有 OpenAI SDK 流程，希望最小改造复用（如 `openai.ChatCompletion.create()`）。

### ✅ 推荐选用 Qwen 机器翻译模型（`qwen-mt-*`）当：
- 核心需求是**准确、保真、格式一致的跨语言转换**，尤其涉及图像、PDF、PPT 等富媒体；
- 要求**术语强制替换、敏感词原样保留、领域风格引导**（如医疗/法律术语库）；
- 输入源为**非纯文本格式**（扫描件、网页截图、产品说明书 PDF）；
- 需要**原格式输出**（如翻译后的 DOCX 仍可编辑、PDF 保持页眉页脚与表格结构）；
- 对翻译结果的**确定性、一致性、低幻觉率**要求极高（基础大模型易在长文档中漏译、错译、自创术语）。

### ⚠️ 明确不建议混用的情形：
- ❌ 用 `qwen-max` 翻译 50 页 PDF —— 会丢失格式、无法处理表格/图片、术语不可控、成本远高于 `qwen-mt-uni`；
- ❌ 用 `qwen-mt-plus` 实现客服对话 —— 不支持多轮状态管理、无 `system` 角色、无法调用工具；
- ❌ 在 `qwen-mt-uni` 请求中传入 `temperature=0.8` —— 参数被忽略，该模型无随机采样机制；
- ❌ 将图像 URL 中文路径（如 `https://example.com/产品图.jpg`）直接用于 `qwen-mt-image` —— 导致 400 错误（URL 必须为 ASCII 编码）。

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 | 注意事项 |
|----------|-----------|-----------|-----------|
| **快速接入一个支持中英互译的 API，输入是字符串数组，输出只需纯文本** | `qwen-mt-plus`（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)） | 专为文本翻译优化，支持术语表、敏感词、领域提示，比基础模型更准更稳 | 需通过 `extra_body` 传参，非标准 `messages` 字段 |
| **上传一张带中文文字的产品宣传图，返回翻译成西班牙语并重排版的 PNG** | `qwen-mt-uni`（同步调用） | 全模态统一入口，支持全部 55 语种互译，自动识别+重排版，无需预处理 | 图像 URL 必须公网可访问且无中文字符；推荐使用业务空间专属域名 |
| **批量处理 200 份英文技术手册 PDF（每份 100 页），输出带目录结构的中文 PDF** | `qwen-mt-uni`（异步调用） | 唯一支持 PDF 原格式输入/输出的模型，异步模式保障大文件稳定处理 | 需轮询任务状态；单文件 ≤200 页；计费按 `document_tokens` 细分 |
| **构建一个多轮对话式翻译助手（用户说“把上句翻成日语”，再问“再翻成法语”）** | `qwen-plus` + `qwen-mt-plus` **组合调用** | 基础模型处理对话逻辑与状态管理，调用 `qwen-mt-plus` 执行实际翻译（Function Calling） | 需自行实现工具调用解析与结果注入；不可直接用 `qwen-max` 生成翻译文本 |
| **已有 OpenAI SDK 项目，想零改造支持翻译功能** | `qwen-mt-plus`（OpenAI 兼容 `/chat/completions`） | 完全兼容 `openai.ChatCompletion.create()`，仅需将 `extra_body` 注入翻译参数 | `messages` 中 `content` 即原文，`model="qwen-mt-plus"`，其他参数（如 `temperature`）无效 |

> **最后建议**：  
> - **新项目优先评估 `qwen-mt-uni`** —— 它是当前百炼平台翻译能力的统一演进方向，已整合 `qwen-mt-image-2.0` 全语种能力，并持续扩展文档/音视频支持；  
> - **避免“用大模型凑翻译”** —— 基础模型在翻译任务上缺乏术语约束、格式保持和领域适配能力，长期维护成本高；  
> - **务必校验输入合规性** —— 特别是 `qwen-mt-*` 对 URL 编码、文件大小、图像尺寸的硬性限制，建议在客户端做前置校验。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


