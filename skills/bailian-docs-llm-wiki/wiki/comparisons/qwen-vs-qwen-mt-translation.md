# 通义千问基础模型与机器翻译专用模型对比

为帮助开发者在百炼平台上高效选型，本文系统对比通义千问（Qwen）系列**通用基础大模型**（如 `qwen3.8-max`、`qwen3.7-plus` 等）与**Qwen-MT 机器翻译专用模型**（如 `qwen-mt-plus`、`qwen-mt-uni` 等）的核心能力差异。二者虽同属通义生态，但设计目标、架构优化、协议支持及工程约束存在本质区别：基础模型面向通用语言理解与生成，而 MT 模型聚焦高精度、强可控、多模态的端到端翻译任务。本对比基于当前（2024Q3）百炼平台正式发布的 API 行为与文档规范，适用于新项目技术评估与存量系统迁移决策。

## 关键维度对比

| 维度 | 通义千问基础模型（Qwen Text/Multimodal） | Qwen-MT 机器翻译专用模型 |
|------|------------------------------------------|---------------------------|
| **核心定位** | 通用大语言模型（LLM），支持对话、推理、代码、多模态理解与生成等泛化任务 | 垂直领域专用模型（SOTA MT），专为高保真、低延迟、可干预的翻译任务深度优化 |
| **输入格式** | 支持结构化 `messages` 数组（含 `system`/`user`/`assistant` 角色）、纯文本字符串、图像/视频/音频 URL（需 `type: "image_url"` 等）；多模态输入需显式声明类型与分辨率参数（如 `min_pixels`） | 按模型细分：<br>• `qwen-mt-plus`：仅支持 `messages`（`role: "user", content: string`）<br>• `qwen-mt-image*`：强制 `input.image_url`（JPG 格式）<br>• `qwen-mt-uni`：支持 `input.source_texts`（文本）、`input.fileUrl`（PDF/DOCX/JPG/MP3 等 10+ 格式） |
| **输出格式** | 自由文本生成，无固定 schema；多模态模型可返回带 `content` 的 `message` 或 `tool_calls`；Responses API 可返回结构化工具结果 | **严格结构化 JSON 输出**：<br>• 文本/图像：`{ "translated_text": "...", "source_lang": "...", "target_lang": "..." }`<br>• 文档/音频：额外包含 `format_preserved_output`（HTML/PDF/Base64）、`segments`（时间戳对齐）等字段；所有模型均保证输出字段名稳定、语义明确 |
| **支持模型** | `qwen3.8-max`, `qwen3.7-plus`, `qwen3.5-flash`, `qwen-plus`, `qwen3.8-omni-flash`, `qwen3.7-vl-plus`, `QVQ`, `Qwen2.5-VL`, `qwen3-coder-flash`, `qwen3.5-math` 等全系模型 | `qwen-mt-plus`（文本）、`qwen-mt-image` / `qwen-mt-image-2.0`（图像）、`qwen-mt-uni`（全模态统一）——**不支持基础模型 ID 直接调用翻译能力** |
| **API 协议与端点** | 多协议兼容：<br>• OpenAI Chat：`/compatible-mode/v1/chat/completions`<br>• Responses（Agent）：`/compatible-mode/v1/responses`<br>• DashScope 原生：`/api/v1/services/aigc/text-generation/generation`（文本）或 `/multimodal-generation/generation`（多模态）<br>• Anthropic Messages：`/apps/anthropic/v1/messages` | **统一 DashScope 原生协议**：<br>• `qwen-mt-plus`：`/api/v1/services/aigc/text-generation/generation`（复用文本端点，但需传 `model=qwen-mt-plus`）<br>• `qwen-mt-image*`：`/api/v1/services/aigc/image2image/image-synthesis`<br>• `qwen-mt-uni`：`/api/v1/services/aigc/multimodal-generation/generation`<br>**不支持 OpenAI/Anthropic 兼容协议**（无 `chat/completions` 或 `messages` 路径） |
| **关键控制参数** | `temperature`, `top_p`, `max_tokens`, `tools`, `system`（部分模型生效），多模态专属参数（`fps`, `min_pixels`, `max_frames`） | 领域强相关参数：<br>• `source_lang`/`target_lang`（必填，`auto` 仅部分模型稳定）<br>• `domainHint`（**英文，≤200 单词**，统一替代过时的 `domains`）<br>• `terminologies`/`glossary`（术语干预）<br>• `sensitives`（敏感词过滤）<br>• `imageSegment`（图像主体跳过）<br>• `translation_options`（仅 `qwen-mt-plus`） |
| **计费方式** | 按 **[Token](../concepts/token.md) 数量计费**（输入 + 输出 tokens），不同模型单价不同；多模态输入按像素/帧数折算为等效 tokens；第三方模型单独定价 | 按 **请求次数 + 输入规模分层计费**：<br>• 文本：按字符数阶梯计价<br>• 图像：按分辨率（像素数）和尺寸（长宽比）计价<br>• 文档/音频：按页数/时长计价<br>**无 token 概念，不因输出长度增加费用** |
| **典型场景** | • 多轮智能客服对话<br>• 技术文档摘要与问答<br>• 代码生成与解释<br>• 图文内容理解与创作<br>• Agent 工具调用（联网搜索、计算器等） | • 电商商品描述批量中英互译<br>• 手册/合同/财报等专业文档格式保留翻译<br>• App 截图/宣传海报 OCR+翻译一体化处理<br>• 客服录音转写+实时翻译<br>• 含行业术语、品牌名、敏感词的合规翻译 |

## 适用场景建议

### ✅ 推荐选用 **Qwen 基础模型** 当：
- 任务本质是**开放生成或复杂推理**（如：“根据用户投诉邮件生成3种安抚话术，并评估每种话术的情绪倾向”）；
- 需要**多轮上下文强依赖**（如：持续追问、状态跟踪、个性化推荐）；
- 输入/输出需**高度自由格式**（如：生成 Markdown 技术方案、编写 Python 脚本、创作营销文案）；
- 已有 OpenAI/Anthropic SDK 生态，追求**零改造迁移**；
- 需调用**内置工具链**（如 `web_search`, `code_interpreter`）辅助翻译前的信息检索或数据验证。

### ✅ 推荐选用 **Qwen-MT 专用模型** 当：
- 核心需求是**翻译质量、一致性与可控性优先**（如：金融年报术语统一、医疗说明书无歧义转换）；
- 输入为**非纯文本模态**（PDF 表格、带水印截图、会议录音 MP3），且要求**保留原始排版/时间轴**；
- 必须满足**企业级定制能力**：术语表强制生效、敏感词原样保留、领域风格精准引导（`domainHint`）；
- 对**延迟与成本确定性要求高**：拒绝因模型“自由发挥”导致输出长度不可控而引发意外计费；
- 需要**异步处理大文件**（如：200页PDF翻译、60分钟会议录音），并获取结构化任务状态（`task_id` 轮询）。

### ⚠️ 明确不建议混用的情形：
- **勿用基础模型做专业翻译**：`qwen3.8-max` 虽能翻译，但无法保障术语一致性、敏感词过滤、格式还原，且 `system` 提示易被忽略，输出长度不可控，成本不可预测；
- **勿用 Qwen-MT 模型做通用对话**：`qwen-mt-plus` 不支持 `assistant` 角色、不维护对话历史、无 `tools` 能力，强行用于客服将导致体验断裂；
- **勿跨协议调用**：`qwen-mt-uni` 无法通过 `/chat/completions` 调用；`qwen3.8-omni-flash` 无法响应 `terminologies` 参数。

## 开发者技术选型参考

| 决策问题 | 判断依据 | 推荐方案 |
|----------|----------|----------|
| **我的输入主要是 PDF/DOCX/图片/音频？** | 是 → 需格式识别与重构能力 | ✅ `qwen-mt-uni`（首选）或 `qwen-mt-image-2.0`（纯图） |
| **我的文本需嵌入100+条专业术语且必须100%生效？** | 是 → 基础模型提示词难以保证术语强制替换 | ✅ `qwen-mt-plus`（`terms`）或 `qwen-mt-uni`（`ext.glossary`） |
| **我需要用户提问→联网查资料→生成回答的完整 Agent 流程？** | 是 → 依赖 `responses` 协议的工具调度能力 | ✅ `qwen3.8-max` + `/responses` 端点 |
| **我已有 OpenAI SDK，且只做简单句子翻译？** | 是 → 追求最小改造成本 | ⚠️ 可用 `qwen3.7-plus` + `/chat/completions`（但质量/可控性弱于 Qwen-MT）；**长期建议迁移到 `qwen-mt-plus` + DashScope SDK** |
| **我的服务 SLA 要求首字响应 <500ms，且文本长度波动极大？** | 是 → 基础模型 `max_tokens` 设置不当易超时或浪费 | ✅ `qwen-mt-plus`（同步调用，响应时间稳定） |
| **我需翻译结果直接嵌入 HTML 页面并保持原有 CSS 样式？** | 是 → 需要格式感知与结构化输出 | ✅ `qwen-mt-uni`（返回 `format_preserved_output` 字段） |

> **重要提醒**：所有 Qwen-MT 模型**仅通过 DashScope 原生协议提供服务**，不兼容 OpenAI/Anthropic 接口。若项目已深度绑定 OpenAI SDK，请使用百炼提供的 [DashScope Python SDK](https://help.aliyun.com/zh/dashscope/developer-reference/quick-start) 或封装适配层，而非尝试修改 `base_url` 为 OpenAI 路径——该路径下 `qwen-mt-*` 模型不可见且会返回 404。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


