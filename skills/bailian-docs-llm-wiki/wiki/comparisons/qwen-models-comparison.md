# 通义千问模型能力对比：Qwen API、Qwen-MT 与决策模型

本文旨在为百炼平台开发者提供清晰、可落地的技术选型参考，系统对比三类面向不同任务范式的通义千问能力服务：**通用大模型调用接口（Qwen API）**、**全模态智能翻译服务（Qwen-MT-Uni）** 和 **结构化决策推理服务（Decision Model）**。随着业务场景日益细分，单一“大模型通用接口”已难以兼顾翻译保真度、决策确定性与多模态工程效率。本对比基于最新正式文档（截至2024年10月），聚焦实际开发中高频关注的协议兼容性、输入输出约束、计费逻辑与部署适配性，帮助团队规避常见误用（如用 Qwen API 做合规审核、用 Qwen-MT 处理非翻译类文本生成等），提升集成效率与服务稳定性。

## 关键能力维度对比

| 维度 | Qwen API | Qwen-MT-Uni | 决策模型 |
|------|----------|-------------|-----------|
| **核心定位** | 通用大模型能力网关（文本生成、多模态理解、Agent 工具调用） | 全模态高保真翻译专用模型（支持文本/图像/音频/文档格式保持） | 结构化轻量推理服务（单次前向、确定性输出分类标签与置信度） |
| **输入格式** | `messages`（Chat）、`input`（Responses）、`system`+`messages`（Anthropic）或 `input`（DashScope）；支持文本、Base64 图像、URL 视频等；需按协议规范组织 | `input.source_texts`（字符串或数组）或 `input.fileUrl`（HTTPS URL）；支持 PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT/JPG/PNG/MP3/WAV；**不支持纯 JSON Schema 或函数定义输入** | `input`（纯文本字符串，≤8192 tokens） + `system_prompt`（非空字符串，≤512 字符）；**仅支持文本，不接受文件、图像、音频或多轮对话历史** |
| **输出格式** | 非结构化文本流（`content`）、工具调用请求（`tool_calls`）、多模态响应（`image_url`/`audio_url`）；需解析 `choices[0].message.content` 或 `tool_calls` 字段 | 同构输出：输入为字符串数组 → 输出同形状字符串数组；输入为 PDF → 输出 PDF URL；输入为 JPG → 输出 JPG URL；结果封装在 `output.Data` 下，含 `TranslatedTexts` 或 `TranslatedFileUrl` | 严格结构化 JSON：固定字段 `label`（string）、`score`（float, 0–1）、`is_true`（bool）、`probabilities`（object 数组）、`confidence`（float）；**无自由文本生成，无 content 字段** |
| **支持模型** | 多模型统一接入：<br>• 文本：`qwen3.8-max`, `qwen3.7-plus`, `qwen3.5-flash`<br>• 多模态：`Qwen-VL`, `Qwen-Omni`, `Qwen-Audio`（仅 DashScope）<br>• 第三方：`DeepSeek`, `Kimi`, `GLM`, `MiniMax`（北京地域限定） | **仅 `qwen-mt-uni` 单一模型**；无版本别名（如 `qwen-mt-base` 等均为过时表述） | **仅 `decision-model`（GA 版）**；预览版 `decision-model-preview` 不承诺 SLA，不建议生产使用 |
| **API 端点（推荐新域名）** | • OpenAI Chat：`/{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• Responses（Agent）：`/.../compatible-mode/v1/responses`<br>• Anthropic Messages：`/.../apps/anthropic/v1/messages`<br>• DashScope 原生：`/.../api/v1/services/aigc/text-generation/generation`（文本）或 `/multimodal-generation/generation`（多模态） | `/{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（同步）<br>异步需加 Header `X-DashScope-Async: enable`，结果轮询 `/api/v1/tasks/{task_id}` | `/{WorkspaceId}.{region}.maas.aliyuncs.com/v1/models/decision-model:predict`（System One 协议） |
| **计费方式** | 按 **token 使用量** 计费：<br>• `input_tokens` + `output_tokens`（基础文本）<br>• 多模态额外计费项（如 `image_tokens`, `video_frames`）<br>• 工具调用（`web_search`, `code_interpreter`）按次/时长计费 | 按 **`input_tokens`** 计费，但细粒度拆分：<br>• `character_tokens`（文本）<br>• `document_tokens`（PDF/DOCX 等）<br>• `image_tokens`（JPG/PNG）<br>• `audio_tokens`（MP3/WAV）<br>• **无 output_tokens 费用** | 按 **单次调用（per request）** 计费；与输入长度无关（只要 ≤8192 tokens）；**不按 token、不按输出、不按工具调用计费** |
| **典型场景** | • 智能客服对话机器人<br>• 多文档摘要与问答<br>• 视频内容理解与描述生成<br>• Agent 自动执行搜索/代码/网页抓取任务 | • 多语言产品文档本地化（PDF/DOCX 保持排版）<br>• 客服工单图片/语音转译（含水印区域控制）<br>• 网页/Markdown 技术博客批量双语发布 | • 内容安全审核（涉政/暴恐/色情标签判定）<br>• 金融风控初筛（欺诈/逾期/套现风险识别）<br>• A/B 测试策略路由（基于用户行为特征决策） |
| **关键限制** | • 上下文窗口因模型而异（如 `qwen3.8-max` 为 32K）<br>• Responses API 输入上下文 ≈ 模型窗口 × 80%（预留工具空间）<br>• `max_frames` 仅 DashScope 支持；`Qwen-Audio` 仅 DashScope 可用 | • 单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频 3s–60min<br>• `fileUrl` 不得含中文字符；旧版 `.doc`/`.ppt` 需转 OOXML<br>• `domainHint` 必须为纯英文 | • 输入 `input` >8192 tokens 静默截断（不报错）<br>• `system_prompt` 超长同样截断<br>• 不支持 streaming、logprobs、function calling、多模态输入 |

## 各方案适用场景建议

### ✅ 推荐使用 Qwen API 当：
- 业务需要**灵活的多轮对话、自由文本生成或复杂推理链路**（如“先查天气，再推荐穿搭，最后生成购物清单”）；
- 已有 OpenAI/Anthropic SDK 生态，希望**零改造迁移**至百炼（利用兼容协议）；
- 需要调用**联网搜索、代码解释器、网页抓取等内置工具**完成闭环任务；
- 处理**视频理解、图文混合问答、音频转写+摘要**等跨模态任务，且对帧数控制（`max_frames`）或像素精度（`min_pixels`）有硬性要求。

### ✅ 推荐使用 Qwen-MT-Uni 当：
- 核心诉求是**格式无损、语义保真、领域可控的翻译**，而非通用文本生成；
- 输入源多样：既有用户粘贴的文本片段，又有待发布的 PDF 手册、PPT 产品介绍、客服录音 MP3、带水印的截图 JPG；
- 需要**术语强一致**（通过 `glossary`）和**敏感词保留原文**（通过 `sensitives`）；
- 对延迟容忍度高：小文本/图片用同步，大文件/长音频用异步（`task_id` 24 小时有效，需主动轮询下载）；
- **不接受“翻译腔”或自由发挥**——Qwen-MT 的设计目标就是消除生成不确定性。

### ✅ 推荐使用 决策模型 当：
- 任务本质是**二分类/多分类信号提取**（如“是否违规？”、“属于哪类风险？”、“应路由至哪个策略组？”），而非生成解释性文字；
- 要求**毫秒级响应、100% 确定性输出**（`temperature=0.0` 强制禁用采样）；
- 输入数据结构清晰（如日志字段拼接、表单文本、规则引擎前置输出），无需多轮上下文；
- 需要**可解释的置信度**（`score`）和**完整概率分布**（`probabilities`）用于后续阈值调控或模型监控；
- 希望**成本可预测**——按次计费，避免因输入长度波动导致账单不可控。

## 开发者技术选型参考

| 选型问题 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **我的应用需要同时做客服对话 + 产品文档翻译 + 内容审核，该用几个服务？** | **三者并用** | Qwen API（对话）、Qwen-MT-Uni（文档翻译）、决策模型（审核）职责正交，混用无耦合风险；强行用 Qwen API 做翻译易失格式、做审核难保证确定性。 |
| **我已有 OpenAI SDK，想快速接入百炼，但需调用 Qwen-Audio** | **DashScope 原生协议** | Qwen-Audio 明确不支持 OpenAI 兼容协议；必须切换至 DashScope SDK 并使用 `/multimodal-generation/generation` 端点。 |
| **我需要翻译一份 150 页的 PDF，且要求保留目录层级和表格样式** | **Qwen-MT-Uni 异步模式** | 同步调用超页数限制（200 页上限内可行），但异步模式专为大文件设计；输出 PDF 与输入完全同构，格式保真度由模型原生保障。 |
| **我做金融风控，需对每笔贷款申请返回“HIGH_RISK/MEDIUM_RISK/LOW_RISK”及对应概率，延迟要求 <500ms** | **决策模型** | Qwen API 即使用 `qwen3.7-plus` 也存在生成不确定性、输出格式不统一、token 成本随输入长度飙升等问题；决策模型原生输出结构化三元组，SLA 保障低延迟。 |
| **我想用 Qwen-MT 翻译一段含数学公式的 LaTeX 文本** | **Qwen API（`qwen3-math`） + 后处理** | Qwen-MT-Uni 不解析 LaTeX 语义，会将 `$E=mc^2$` 当普通字符串直译；应选用 `qwen3-math` 模型，通过 DashScope 协议调用，并启用 `format: "latex"` 参数确保公式完整性。 |
| **我的系统需支持中→英、英→日、日→中三段式翻译流水线，能否复用一个模型？** | **Qwen-MT-Uni 单次调用即可** | `qwen-mt-uni` 原生支持任意源/目标语言对（见[语种列表](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages)），无需链式调用；三段式应改为“中→日”单步直达，避免误差累积。 |

> **重要提醒**：所有服务均需配置百炼业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`），旧域名（如 `dashscope.aliyuncs.com`）虽兼容但性能与稳定性不达新标准，**新项目务必使用新域名**。SDK 配置请严格参照各协议文档的 `base_url` / `workspace` / `region` 设置说明，参数命名与必填性因协议而异（如 `messages` 在 OpenAI Chat 中必填，在 Decision Model 中不存在）。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


