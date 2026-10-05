# 通义千问基础模型、机器翻译模型与决策模型对比

本文旨在帮助开发者在阿里云百炼平台上快速识别并选用最适合业务需求的模型能力。随着 Qwen 系列模型生态持续扩展，平台已形成三类定位清晰、能力互补的核心能力栈：  
- **通义千问基础模型**（Qwen General-purpose LLM）：面向通用文本生成与多模态理解的“全能型”大语言模型；  
- **机器翻译模型**（Qwen MT 系列）：专注跨语言语义转换的垂直领域模型，覆盖文本、图像、文档、音视频等多模态输入；  
- **决策模型**（Decision Model）：轻量、确定、低延迟的结构化推理引擎，专为分类、是非判断与有序评分等确定性任务设计。  

本对比聚焦技术选型关键维度，不涉及性能压测或成本精算，而是从接口协议、输入输出契约、模型边界与工程实践角度提供可落地的决策依据。

## 关键维度对比

| 维度 | 通义千问基础模型（Qwen LLM） | 机器翻译模型（Qwen MT） | 决策模型（Decision Model） |
|------|-----------------------------|--------------------------|----------------------------|
| **核心定位** | 通用大语言模型：文本生成、多模态理解、工具调用、复杂推理 | 垂直领域模型：高保真、强可控的跨语言语义转换 | 结构化轻量推理模型：非生成式、确定性分类/判断/评分 |
| **支持模型** | `qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen3-vl-plus`、`qwen3.8-omni-flash`、`qwen3.5-ocr`、`qwen-audio`（仅 DashScope）等全系列 Qwen 模型 | `qwen-mt-plus`（文本）、`qwen-mt-image` / `qwen-mt-image-2.0`（图像）、`qwen-mt-uni`（全模态统一） | 仅 `decision-model-preview`（预览版，无其他别名或版本） |
| **输入格式** | 多样化：<br>• 文本：`messages[]`（Chat/Anthropic）、`input`（DashScope）、`prompt`（Responses）<br>• 多模态：`image_url`、`video_url`、`input_audio`、`input_video`、`video`（帧列表）等<br>• 工具调用：`tool_use`（Anthropic）、内置工具（Responses） | 按模型类型严格区分：<br>• `qwen-mt-plus`：纯文本字符串或数组，置于 `messages[0].content`<br>• `qwen-mt-image-*`：`input.image_url`（DashScope）<br>• `qwen-mt-uni`：`input.fileUrl`（PDF/DOCX/JPG/MP3等）或 `input.source_texts`（文本） | 结构化 JSON：<br>• `state`：原始上下文（string/object/array，JSON 序列化后送入）<br>• `questions`：对象，每个 key 为问题 ID，value 含 `type`（`choice`/`noul`/`score`）、`criteria` 等<br>• `instructions`（可选但推荐）：评判标准说明 |
| **输出格式** | 自由文本生成为主，支持：<br>• 流式 token（`stream: true`）<br>• 强约束 JSON Schema（Anthropic 接口 + `output_config.format.type = "json_schema"`）<br>• 工具调用结果（`tool_result`） | 格式严格对齐输入：<br>• 文本 → 翻译后文本（含术语干预、敏感词过滤结果）<br>• 图像 → 带翻译标注的图像（PNG/JPEG）<br>• 文档/音视频 → 同格式翻译文件（URL 下载）<br>• 异步任务返回 `task_id`，需轮询获取 `TranslatedFileUrl` | 纯结构化 JSON，**零文本生成**：<br>• `choice`：`selected`, `probabilities`, `confidence`<br>• `noul`：`probability_yes`, `probabilities`（含 `true`/`false`）<br>• `score`：`score`（浮点期望值）、`probabilities`, `confidence`<br>• 所有类型均返回完整概率分布 |
| **API 协议与端点** | 多协议支持：<br>• OpenAI 兼容：`/compatible-mode/v1/chat/completions`（Chat）、`/compatible-mode/v1/responses`（Responses）<br>• Anthropic 兼容：`/apps/anthropic/v1/messages`<br>• DashScope 原生：`/api/v1/services/aigc/{text-generation\|multimodal-generation}/generation` | 协议按能力解耦：<br>• `qwen-mt-plus`：OpenAI 兼容 Chat 端点 `/compatible-mode/v1/chat/completions`<br>• `qwen-mt-image-*`：DashScope 原生 `/api/v1/services/aigc/image2image/image-synthesis`<br>• `qwen-mt-uni`：DashScope 统一多模态端点 `/api/v1/services/aigc/multimodal-generation/generation` | 专用协议：<br>• TypeSafe System One：<br>`/compatible-mode/v1/systemone`（仅此端点） |
| **计费方式** | 按 **输入 + 输出 Token 总量** 计费（含多模态编码开销，如图像像素转 token）；流式响应按实际返回 token 计费；`qwen-audio` 等特殊模型可能有额外音频时长因子 | 按 **请求次数 + 输入资源规模** 计费：<br>• 文本：按字符数或 token 数（依模型而定）<br>• 图像/文档/音视频：按文件大小（MB）或页数/时长（如 PDF ≤200 页、音频 ≤60 分钟）计费<br>• 异步任务成功后下载 `TranslatedFileUrl` 不额外计费 | 按 **请求次数 + `state` token 数 + 问题数量** 计费：<br>• `state` 超长（>65536 token）将被截断，仍按截断后长度计费<br>• `questions` 中每增加一个问题，计算开销线性增长；≥16 个问题时延迟显著上升，建议分批 |
| **典型场景** | • 智能客服对话<br>• 技术文档摘要与问答<br>• 多模态内容理解（图/视频/音频分析）<br>• 代码生成与调试<br>• 数学与逻辑推理 | • 官网/APP 多语言本地化<br>• 扫描件/PDF 合同双语对照<br>• 社交媒体截图实时翻译（保留排版）<br>• 教育课件、会议录音跨语言转译<br>• 电商商品图多语种标签生成 | • 工单自动分级（P0–P3）与路由（售前/售后/技术）<br>• 内容安全审核（涉政/色情/暴恐 二分类）<br>• AI Agent 动作选择（`choose_action: [search, calculate, reply]`）<br>• 用户反馈情感强度评分（1–5 分期望值） |

## 各方案适用场景建议

### ✅ 选择通义千问基础模型，当您需要：
- **开放性生成能力**：回答开放式问题、撰写创意文案、生成代码、进行多步推理；
- **多模态融合理解**：同时处理图文混合输入、分析视频中的视觉+语音信息（Qwen-Omni）、OCR 提取图像文字后进一步解读；
- **动态工具协同**：在对话中按需调用搜索、代码解释器、文件解析等工具完成复杂任务；
- **灵活输出控制**：要求 JSON Schema 校验、流式响应、温度/Top-p 精细采样调控。

> ⚠️ 注意：若任务本质是“翻译”，即使使用 Qwen LLM（如 `qwen3.8-max`）提示工程实现，其专业性、术语一致性、排版保持能力及合规性（敏感词过滤）远低于 Qwen MT 系列，**不推荐替代**。

### ✅ 选择机器翻译模型，当您需要：
- **高精度、可管控的跨语言转换**：尤其涉及法律、医疗、金融等专业领域，需强制术语映射（glossary）、敏感词屏蔽、领域风格引导（`domainHint`）；
- **非纯文本输入**：待翻译内容存在于图像（截图/海报）、PDF（合同/说明书）、PPT（产品介绍）、音频（会议记录）等载体中；
- **格式保真输出**：要求翻译结果严格复现原文排版（图像标注位置、文档段落结构、表格对齐）；
- **批量[异步处理](../concepts/asynchronous-processing.md)**：处理百页级文档或小时级音频，接受任务队列与回调机制。

> ⚠️ 注意：`qwen-mt-image` 存在明确语种限制（源或目标必须含中文或英文），若需日↔韩、法↔西等非中/英语种直译，请务必选用 `qwen-mt-image-2.0` 或 `qwen-mt-uni`。

### ✅ 选择决策模型，当您需要：
- **毫秒级、高并发、确定性判断**：如每秒处理数千条工单/评论，要求响应延迟 <500ms，且结果必须可重复、可审计；
- **结构化输出即最终结果**：下游系统直接消费 `confidence` 或 `probabilities` 做阈值拦截（如 `confidence < 0.85` 则转人工），无需后续 NLP 解析；
- **规避幻觉风险**：任务本质是分类/打分，绝不允许模型“自由发挥”生成解释性文本；
- **轻量部署与低成本**：相比加载完整 LLM，该模型体积小、推理快、Token 消耗极低（仅编码 `state` 和 `questions`）。

> ⚠️ 注意：决策模型 **不支持文本生成、不支持多轮对话状态维护、不支持工具调用**。若任务需“先判断再生成回复”，应组合使用：先调用决策模型获取 `choice`，再以该结果为条件调用 Qwen LLM 生成自然语言响应。

## 面向开发者的选型参考

| 您的问题 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| “我要把用户上传的英文PDF说明书翻译成中文，保留所有图表和表格格式” | ✅ `qwen-mt-uni` | 唯一支持 PDF 输入+同格式输出的模型；自动处理图文混排；支持术语表与敏感词过滤 |
| “我需要分析一段带字幕的短视频，总结关键事件并提取发言者情绪” | ✅ 通义千问基础模型（`qwen3.8-omni-flash`） | Qwen-Omni 独家支持音视频联合理解；可通过 `video_url` + `input_audio` 输入；后续用 `web_search` 工具补充背景 |
| “客服系统收到一条用户消息，需自动判断应分配给‘退款组’‘物流组’还是‘技术组’，并给出置信度” | ✅ 决策模型 | `choice` 类型完美匹配；`confidence` 直接用于路由阈值；延迟低、成本低、结果确定 |
| “我的 App 需要实时翻译用户拍摄的菜单照片，且必须支持日语→法语” | ✅ `qwen-mt-image-2.0` | `qwen-mt-image` 不支持日→法；`qwen-mt-image-2.0` 支持全部 55 种语言任意互译 |
| “我想让模型根据用户提问，先搜索知识库，再运行 Python 代码计算，最后生成带图表的报告” | ✅ 通义千问基础模型（Responses API） | Responses 接口原生集成 `web_search`、`code_interpreter` 工具；支持多步骤自动编排 |
| “我有一批 10 万条用户评论，需批量打上‘正面/中性/负面’标签，并输出每条的概率分布” | ✅ 决策模型（`score` 或 `choice`） | 可批量提交 `questions` 数组；返回结构化 `probabilities`，便于统计分析；比调用 LLM 生成文本再解析更高效、更稳定 |

**最后建议**：  
- **优先验证输入输出契约**：在选型前，用最小 payload 调用各模型的沙箱环境，确认输入字段嵌套、输出 JSON 结构是否符合下游系统预期；  
- **关注协议迁移成本**：Qwen LLM 与 Qwen MT 的 `qwen-mt-plus` 共享 OpenAI 兼容 Chat 端点，但 `qwen-mt-image` 和决策模型需切换至 DashScope 或 System One 协议，客户端需适配新 endpoint 与认证头；  
- **善用专属域名与 WorkspaceId**：所有模型均通过 `{WorkspaceId}.{region}.

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


