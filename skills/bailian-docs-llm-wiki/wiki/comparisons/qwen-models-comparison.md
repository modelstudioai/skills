# 通义千问模型能力对比：基础Qwen API、MT翻译模型与决策模型

## 背景与目的  
在百炼平台中，通义千问系列模型面向不同业务目标提供了三类高度专业化的能力路径：  
- **基础Qwen API**：通用大语言模型服务，强调对话理解、多模态感知与复杂推理；  
- **Qwen-MT-Uni 翻译模型**：全模态、格式保真的端到端翻译引擎，聚焦跨语言语义对齐与文档结构还原；  
- **决策模型（`decision-model-preview`）**：轻量级结构化推理模型，专为低延迟、高确定性、零文本生成的决策任务设计。  

本对比旨在帮助开发者基于**输入类型、输出需求、性能约束、集成成本与计费逻辑**等核心维度，快速识别最适合当前场景的模型方案，避免误用通用模型处理专用任务（如用 Qwen3.7-plus 做工单分级导致延迟高、成本高、结果不可控），提升工程效率与业务效果。

---

## 关键维度对比表

| 维度 | 基础Qwen API | MT翻译模型（`qwen-mt-uni`） | 决策模型（`decision-model-preview`） |
|------|--------------|-----------------------------|----------------------------------------|
| **核心定位** | 通用大模型能力底座（对话、创作、工具调用、多模态理解） | 全模态高保真翻译引擎（文本/图像/音视频/文档） | 结构化轻量决策引擎（分类/是非/打分，不生成文本） |
| **输入格式** | • `messages` 数组（Chat/Anthropic）<br>• `input` 字符串或数组（Responses）<br>• 支持 `image_url`/`video_url`/`input_audio` 等多模态内容<br>• 支持 `system` 角色与工具声明 | • `input.fileUrl`（HTTPS URL）<br>• 或 `input.source_texts`（字符串或字符串数组）<br>• 支持 PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown/JPG/PNG/MP3/WAV 等10+格式<br>• 需显式指定 `target_lang` | • `state`：任意结构化上下文（字符串、JSON 对象、数组），最大 65536 token<br>• `questions`：定义问题类型（`choice`/`noul`/`score`）及判定标准（`criteria`）<br>• 最多 16 个问题 |
| **输出格式** | • JSON 格式响应，含 `choices[0].message.content`（文本）或 `choices[0].message.content` + 多模态附件<br>• Responses 协议支持结构化 `output_config.format` 输出<br>• Anthropic 协议支持 `tool_use`/`tool_result` 工具交互流 | • 同步：`output.Data.TranslatedTexts`（文本）或 `output.Data.TranslatedFileUrl`（文件下载链接）<br>• 异步：通过 `task_id` 查询，成功后返回相同结构<br>• 严格保持输入格式（如 DOCX → DOCX，JPG → JPG） | • 纯结构化 JSON：<br> – `choice`: `{ "selected": "option_a", "probabilities": {"option_a": 0.82, ...}, "confidence": 0.93 }`<br> – `noul`: `{ "noul": 0.74 }`（P(yes)）<br> – `score`: `{ "score": 2.25, "probabilities": [0.1, 0.65, 0.25], "confidence": 0.88 }`<br>• **无任何自由文本生成字段** |
| **支持模型** | `qwen3.8-max`, `qwen3.7-plus`, `qwen3-vl-plus`, `qwen3-coder-flash`, `qwen3.7` 等全系主流 Qwen 模型（含多模态与代码专用版） | 仅 `qwen-mt-uni`（当前唯一发布版本） | 仅 `decision-model-preview`（预览版，功能稳定，接口冻结） |
| **API 端点（典型）** | • OpenAI 兼容：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• DashScope 原生：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation` | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`<br>（同步）<br>或添加 Header `X-DashScope-Async: enable`（异步） | `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`<br>（TypeSafe System One 兼容协议） |
| **计费方式** | • 按 `input_tokens` + `output_tokens` 计费<br>• 多模态输入按像素/帧/音频时长折算为 token（如 `image_tokens`, `video_tokens`）<br>• 不同模型单价不同（如 `qwen3.8-max` > `qwen3.7-plus`） | • 仅按 `input_tokens` 计费（不含输出）<br>• 细粒度拆分：`document_tokens` / `image_tokens` / `audio_tokens` / `character_tokens`<br>• 文件解析、OCR、格式重构等隐式处理均计入 `input_tokens` | • 按**单次请求**计费（固定单价），与 `state` 长度、问题数量、选项规模无关<br>• 无 `token` 概念，不因输出变长而增费<br>• 成本极低且可预测（适合高频调用） |
| **典型场景** | • 智能客服对话机器人<br>• 多轮 Agent 编排（联网搜索+代码执行+文档摘要）<br>• 图像/视频内容理解与描述<br>• 技术文档生成与润色 | • 多语言产品说明书批量翻译（PDF→PDF）<br>• 客服录音转文字+实时翻译（MP3→TXT）<br>• PPT 汇报稿中英双语自动排版（PPTX→PPTX）<br>• 扫描件图片中的表格文字精准翻译（JPG→JPG） | • 工单智能分流（“归属团队：A/B/C/other”）<br>• 内容安全审核（“是否涉政：yes/no/uncertain”）<br>• 智能体任务完成度校验（“完成度：1~5 分”）<br>• 用户意图置信度分级（“购买意向：low/medium/high”） |
| **多轮对话支持** | • Chat：需手动维护 `messages` 数组<br>• Responses：支持 `previous_response_id` 自动拼接或 `x-dashscope-session-cache` 缓存<br>• Anthropic：依赖消息顺序，无内置状态管理 | ❌ 不支持多轮；每次调用为独立翻译任务 | ❌ 不支持多轮；每次请求为独立决策快照 |
| **工具调用能力** | ✅ 支持（Responses 协议内置 `web_search`/`code_interpreter`；Anthropic 协议支持 `tool_use`） | ❌ 不支持工具调用；所有翻译逻辑内建封装 | ❌ 不支持工具调用；纯前向推理，无外部交互 |

---

## 适用场景建议（面向开发者的技术选型指南）

### ✅ 选择 **基础Qwen API** 当：
- 你需要**开放域生成能力**（如写文案、编代码、讲故事）；  
- 输入/输出需**强交互性与灵活性**（如多轮对话、用户随时中断重试）；  
- 任务涉及**多步骤协同**（例如：先看图识物 → 再搜索商品 → 最后比价推荐）；  
- 你已有 OpenAI/Anthropic 生态技术栈，希望**最小改造迁移**；  
- 可接受毫秒级至数秒级延迟，且愿意为高质量生成支付对应 token 成本。

> ⚠️ 注意避坑：勿用于高并发、低延迟、确定性要求强的决策任务（如每秒万次工单路由），Qwen API 的非确定性输出、长尾延迟与 token 成本将显著抬高系统负担。

---

### ✅ 选择 **Qwen-MT-Uni 翻译模型** 当：
- 核心诉求是**跨语言语义准确 + 格式完全一致**（如合同翻译必须保留页眉页脚、表格行列、图片位置）；  
- 输入源为**真实业务文档**（PDF 报告、Word 合同、PPT 方案、扫描件 JPG）；  
- 需要**领域适配**（如医疗术语、金融条款）或**敏感词/术语强管控**；  
- 文件体积较大（>10 MB）或处理耗时较长（>10 秒），需使用**异步模式**并管理 `task_id` 生命周期；  
- 你追求**翻译质量稳定性**，而非创造性表达（该模型不“润色”，只“精准转译”。

> ⚠️ 注意避坑：勿用于纯文本简单短句翻译（如 UI 字符串），此时基础 Qwen API 更轻量、更经济；勿尝试用其做 OCR 或语音识别——它只处理已知模态内容，不替代 ASR/Vision 前处理。

---

### ✅ 选择 **决策模型** 当：
- 你的问题是**封闭、结构化、有明确定义答案空间**的（如：3 个选项、2 种判断、5 级量表）；  
- 业务要求**亚秒级响应、100% 确定性输出、零文本幻觉**（如风控拦截必须返回明确 yes/no）；  
- 你已在下游构建了**阈值过滤、置信度融合、AB 测试分流**等决策链路；  
- 调用量极大（日均百万+），需要**可预测、线性扩展、无 token 波动**的成本模型；  
- 你愿意用少量配置（`criteria` 描述）换取开箱即用的统计级可靠性，而非自行微调 LLM。

> ⚠️ 注意避坑：勿用于开放式问答（如“请解释量子计算原理”）、创意生成（如“写一首唐诗”）或需要上下文记忆的任务；该模型无 stateful 能力，每次请求必须携带完整 `state`。

---

## 总结：一句话选型口诀  
> **要“说人话”——选基础 Qwen API；  
> 要“翻得准”——选 Qwen-MT-Uni；  
> 要“判得快、判得稳、判得省”——选 decision-model-preview。**  

所有模型均运行于百炼平台统一基础设施，共享 Workspace 域名、API Key 认证与监控告警体系。建议新项目优先采用业务空间专属域名（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），以获得最佳性能与长期兼容性保障。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


