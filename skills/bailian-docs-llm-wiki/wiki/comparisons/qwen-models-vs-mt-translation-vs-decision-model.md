# 通义大模型家族：基础语言模型、机器翻译模型与决策模型对比

为帮助开发者在百炼平台上快速识别并选用最匹配业务需求的通义大模型能力，本文对三类核心模型服务——**基础语言模型（Qwen LLM）**、**机器翻译模型（Qwen-MT）** 和 **决策模型（Decision Model）** 进行系统性对比分析。三者虽同属通义大模型生态，但在设计目标、输入输出范式、协议支持、计费逻辑及适用场景上存在本质差异。本对比基于当前（2024年Q4）百炼平台正式发布的 API 文档与实测行为，聚焦技术选型关键维度，不涉及训练细节或内部架构。

## 关键维度对比

| 维度 | 基础语言模型（Qwen LLM） | 机器翻译模型（Qwen-MT） | 决策模型（Decision Model） |
|------|--------------------------|---------------------------|------------------------------|
| **核心定位** | 通用文本生成与理解，支持多轮对话、工具调用、多模态推理 | 专业级跨语言内容转换，覆盖文本/图像/文档/音频全模态输入 | 结构化判断引擎，专注分类、是非、评分等确定性决策任务，**不生成自然语言** |
| **典型输入格式** | `messages` 数组（含 text/image_url/audio_url/video_url 等多模态元素），或 `input` 字符串（Responses API） | • `qwen-mt-plus`：纯文本字符串 + `translation_options`<br>• `qwen-mt-image-*`：图像 URL 或 base64<br>• `qwen-mt-uni`：文件 URL（PDF/DOCX/JPG/MP3等）或 `source_texts` 数组 | `state`（字符串/对象/数组，描述业务上下文） + `questions`（字典，定义多个 `choice`/`noul`/`score` 问题） |
| **典型输出格式** | 自然语言文本流或完整响应（JSON），支持 `stream=true` SSE 流式；Responses API 含 `tool_calls` 字段 | • `qwen-mt-plus`：翻译后文本字符串<br>• `qwen-mt-image-*`：带坐标标注的译后图像 URL 或 base64<br>• `qwen-mt-uni`：结构化 JSON（含 `translated_text`、`file_url`、`pages` 等字段） | 纯结构化 JSON：含 `choices`（选项概率）、`noul`（`P(yes)` 浮点值）、`score`（期望等级索引+各等级概率分布），**无自由文本生成字段** |
| **支持模型（代表）** | `qwen3.8-max`, `qwen3.7-plus`, `qwen3.5-flash`, `qwen3-vl-plus`, `qwen3.8-omni-flash`, `qwen3.8-audio` | `qwen-mt-plus`, `qwen-mt-image`, `qwen-mt-image-2.0`, `qwen-mt-uni` | `decision-model-preview`（唯一预览版模型） |
| **主流 API 协议** | OpenAI 兼容（Chat/Responses）、Anthropic 兼容（Messages）、DashScope 原生 | OpenAI 兼容（仅 `qwen-mt-plus`）、DashScope 原生（全部） | TypeSafe System One 协议（通过 `/compatible-mode/v1/systemone` 调用），**不兼容 OpenAI/Anthropic** |
| **API 端点（推荐）** | `POST /compatible-mode/v1/chat/completions`（Chat）<br>`POST /compatible-mode/v1/responses`（Agent）<br>`POST /api/v1/services/aigc/text-generation/generation`（DashScope 原生） | `POST /compatible-mode/v1/chat/completions`（`qwen-mt-plus`）<br>`POST /api/v1/services/aigc/image2image/image-synthesis`（图像）<br>`POST /api/v1/services/aigc/multimodal-generation/generation`（`qwen-mt-uni`） | `POST /compatible-mode/v1/systemone`（TypeSafe System One） |
| **计费方式** | 按 **输入 Token + 输出 Token** 计费（含图像/视频帧转码 Token）；多模态输入 Token 消耗显著高于纯文本 | 按 **请求次数 + 输入规模** 计费：<br>• 文本：按字符数或 Token 数<br>• 图像/文档/音频：按文件大小（MB）或页数/时长分级计费<br>• [异步任务](../concepts/asynchronous-task.md)额外收取队列等待费 | 按 **单次请求** 计费（无论 `questions` 数量 ≤16）；费用与 `state` 长度正相关，超 65536 tokens 直接拒绝（不计费） |
| **典型场景** | 智能客服对话、内容创作、代码生成、Agent 工具编排、多模态理解（看图说话、音视频摘要） | 多语种网站本地化、电商商品图翻译、合同文档双语对照、会议录音实时字幕翻译 | 工单自动分派（→ 技术/售后/合规团队）、UGC 内容安全审核（→ 违规/模糊/正常）、智能体执行结果校验（→ 成功/失败/需重试）、服务满意度打分（1–5 分） |

## 各方案适用场景建议

### ✅ 选择基础语言模型（Qwen LLM）当：
- 你需要**生成连贯、富有创造性的自然语言**（如文案、报告、邮件、故事）；
- 业务流程依赖**多轮上下文感知对话**或**动态工具调用**（搜索、计算、API 调用）；
- 输入包含**图像、音频、视频等非文本模态**，且需跨模态语义理解；
- 已有 OpenAI/Anthropic 技术栈，追求**最小迁移成本**；
- 场景对**响应延迟容忍度中等**（通常 500ms–3s），可接受[流式输出](../concepts/streaming-output.md)。

> ⚠️ 注意：若仅需简单问答或摘要，优先选用轻量模型（如 `qwen3.5-flash`）以降低成本；若需强结构化输出（如 JSON Schema），应选 Anthropic Messages 协议并配置 `output_config.format`。

### ✅ 选择机器翻译模型（Qwen-MT）当：
- 核心诉求是**高保真、领域适配的跨语言转换**，而非语言生成；
- 输入源多样：网页文本、扫描PDF、手机截图、会议录音等，需**开箱即用的全模态支持**；
- 需要**术语强干预、翻译记忆复用、敏感词过滤**等企业级本地化能力；
- 对**排版还原度要求高**（如图像翻译需保留文字位置与字体样式）；
- 支持**异步处理大文件**（如百页合同、1小时音频），且可接受分钟级延迟。

> ⚠️ 注意：`qwen-mt-plus` 适合高频、低延迟文本翻译；`qwen-mt-uni` 是统一入口，但复杂文档解析可能略慢于专用模型；图像翻译必须使用 `qwen-mt-image-*` 系列，`qwen-mt-plus` 不支持。

### ✅ 选择决策模型（Decision Model）当：
- 任务本质是**离散判断或量化评估**，结果需**可解释、可审计、低方差**；
- 业务 SLA 要求**极低延迟（<100ms）与高并发确定性**（如每秒万级工单路由）；
- 输入为结构化/半结构化数据（JSON 日志、表单字段、对话摘要），无需生成新文本；
- 需要**一次请求完成多个关联判断**（例如：同时判断“是否涉政”、“是否含联系方式”、“严重程度”）；
- 安全合规场景下，**禁止模型自由发挥**（避免幻觉导致误判），必须严格遵循预设选项与标准。

> ⚠️ 注意：该模型**不适用于开放式问答、创意写作、摘要生成等任何文本生成任务**；`state` 超长将直接报错，务必前置做摘要或切片；`questions` 设计需严谨，`criteria` 描述越清晰，置信度越高。

## 开发者技术选型参考

| 你的需求 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| “我有一个 Python Flask 应用，已用 OpenAI SDK 实现客服聊天，想迁移到百炼” | ✅ Qwen LLM（OpenAI Chat API） | 协议完全兼容，只需替换 `base_url` 和 `model`，零代码改造；支持 `qwen3.7-plus` 等主力模型 |
| “我要为跨境电商 App 添加商品图一键翻译功能，用户拍照上传 JPG，返回带翻译文字的 PNG” | ✅ Qwen-MT（`qwen-mt-image-2.0` + DashScope 原生） | 唯一支持图像输入+排版保留的专用模型；`imageSegment=false` 可跳过人物/Logo 区域 |
| “我们每天处理 50 万条用户投诉工单，需自动分派到 8 个团队，并标记紧急程度（1–3 级）” | ✅ Decision Model | 单次请求可并行处理 `choice`（分派团队）+ `score`（紧急度），延迟稳定 <80ms，结果概率可追溯 |
| “需要将公司内部知识库（Markdown+PDF）批量翻译成英文，保留目录结构和表格” | ✅ Qwen-MT（`qwen-mt-uni` + 异步模式） | 支持 Markdown/PDF 输入，输出含结构化 `pages` 字段；异步模式规避超时风险 |
| “构建一个能联网查天气、写周报、订会议室的 AI Agent” | ✅ Qwen LLM（Responses API） | 内置 `web_search`/`code_interpreter` 等工具链，`previous_response_id` 自动管理会话状态 |
| “审核短视频字幕，判断是否含违禁词并打分（1=轻微，5=严重）” | ✅ Decision Model + ✅ Qwen-MT（`qwen-mt-uni`）组合 | 先用 `qwen-mt-uni` 提取字幕文本，再送入 Decision Model 判断；避免 LLM 在审核任务中产生不可控输出 |

> **终极选型口诀**：  
> **要“说” → 选 Qwen LLM**（生成语言）  
> **要“翻” → 选 Qwen-MT**（转换语言）  
> **要“判” → 选 Decision Model**（输出结构化决策）  
> 三者可组合使用（如 MT 提取文本 → Decision 判定 → LLM 生成处置建议），但**严禁混用协议调用同一模型**（如用 Anthropic 协议调 `qwen-mt-plus`）。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


