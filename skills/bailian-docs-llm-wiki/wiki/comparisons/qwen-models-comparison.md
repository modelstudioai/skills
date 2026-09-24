# Qwen系列模型能力对比（基础、多模态、翻译、决策）

## 背景与目的  
为帮助开发者在百炼平台上高效选型，本文系统对比 Qwen 系列中四类核心能力模型：**基础大语言模型（LLM）**、**多模态理解模型（VL / Audio / Video）**、**全模态机器翻译模型（MT）** 和 **结构化决策模型（Decision）**。对比聚焦实际工程落地维度——包括输入/输出范式、协议支持、计费逻辑、性能边界与典型适用场景，避免仅罗列参数，强调“什么任务该用什么模型+什么接口”。

所有模型均运行于百炼平台统一基础设施，共享业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）与 API Key 认证体系，但**协议层、数据流设计与语义目标存在本质差异**。本对比不覆盖训练/微调能力，仅面向推理调用场景。

---

## 关键能力维度对比表

| 维度 | 基础文本模型（Qwen LLM） | 多模态理解模型（Qwen VL / Audio / Video） | 全模态翻译模型（Qwen-MT-Uni） | 结构化决策模型（decision-model-preview） |
|------|---------------------------|---------------------------------------------|----------------------------------|---------------------------------------------|
| **核心能力定位** | 通用文本生成、对话、推理、代码、工具调用 | 图像/视频/音频内容理解、图文问答、跨模态检索 | 文本/文档/图像/音频的端到端高保真翻译（保持格式） | 工单分流、内容审核、智能体路由等确定性结构化判定（非生成） |
| **代表模型** | `qwen3.8-max`, `qwen3.7-plus`, `qwen3.5-flash`, `qwen-coder-next` | `qwen3.8-omni-flash`, `qwen3-vl-plus`, `qwen-vl-max`, `qwen3.8-audio`, `QVQ` | `qwen-mt-uni`（唯一可用） | `decision-model-preview`（唯一可用） |
| **输入格式** | `messages[]`（text-only 或含 `image_url`/`video_url`/`input_audio`）；支持纯文本、图文混合、音视频帧列表 | 同左，但**必须显式包含多模态内容块**（如 `{"type":"image_url","image_url":{"url":"..."}}`）；`qwen3.8-audio` 仅 DashScope 协议支持 | `input.source_texts`（文本数组）或 `input.fileUrl`（PDF/DOCX/PPTX/XLSX/TXT/HTML/MD/PNG/JPG/MP3/WAV）；自动识别模态 | `state`（任意结构化数据：字符串/JSON对象/数组） + `questions`（定义 `choice`/`noul`/`score` 问题） |
| **输出格式** | 自由文本流（stream）或完整响应；支持 JSON Schema 强约束（Anthropic 协议） | 结构化 JSON（含 `content` 字段解析结果）；不返回原始媒体文件 | 严格对应输入格式：<br>• 文本 → `output.Data.TranslatedTexts[]`<br>• 文件 → `output.Data.TranslatedFileUrl`（新 URL） | **纯结构化结果**：<br>• `choice`: `{selected, probabilities[], confidence}`<br>• `noul`: `{probability_yes: 0.92}`<br>• `score`: `{expected_score: 2.25, probabilities[], legend[], confidence}`<br>**无任何自由文本生成** |
| **支持协议** | ✅ OpenAI 兼容（Chat / Responses）<br>✅ Anthropic 兼容（Messages）<br>✅ DashScope 原生 | ✅ OpenAI 兼容（Chat / Responses）<br>✅ Anthropic 兼容（Messages）<br>✅ DashScope 原生（**唯一支持 `qwen3.8-audio` 和 `max_frames` 的协议**） | ❌ 仅 DashScope 原生协议（`/api/v1/services/aigc/multimodal-generation/generation`） | ❌ 专用 TypeSafe System One 协议（`POST /compatible-mode/v1/systemone`） |
| **API 端点示例** | `https://{ws}.cn-beijing.maas.aliyuncs.com/v1/chat/completions`（OpenAI Chat） | `https://{ws}.cn-beijing.maas.aliyuncs.com/v1/messages`（Anthropic）<br>`https://{ws}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（DashScope） | `https://{ws}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（同步/异步共用） | `https://{ws}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone` |
| **计费方式** | 按 `input_tokens` + `output_tokens` 计费（单位：千 [Token](../concepts/token.md)）；不同模型单价不同 | 同左；**多模态输入额外计费**：<br>• 图像：按像素数折算 tokens<br>• 视频：按帧数 × 分辨率计费<br>• 音频：按时长折算 tokens | 按 `usage.input_tokens` 计费；`input_tokens_details` 拆分统计：<br>• `document_tokens`（PDF/DOCX 等）<br>• `image_tokens`（OCR+理解）<br>• `audio_tokens`（ASR+翻译）<br>• `character_tokens`（纯文本） | 按**单次请求**计费（固定单价），与 `state` 长度、问题数量无关；**不按 token 计费** |
| **典型延迟（P95）** | 300–2000 ms（取决于模型大小、`max_tokens`、是否流式） | 500–5000 ms（视频/长音频显著更高） | • 同步：≤3 s（文本/小图/短音频）<br>• 异步：任务创建 <100 ms，处理耗时依文件大小而定（PDF 200 页约 30–120 s） | ≤150 ms（稳定低延迟，与输出复杂度无关） |
| **多轮对话支持** | ✅ OpenAI Responses（`previous_response_id`）<br>✅ Anthropic Messages（`messages` 数组）<br>✅ 所有协议支持 `x-dashscope-session-cache` 缓存 | 同左（需手动维护 `messages` 或使用 Responses Session） | ❌ 不支持多轮；每次调用为独立翻译任务 | ❌ 不支持多轮；每次请求为独立决策事件 |
| **工具调用能力** | ✅ OpenAI Responses：内置 `web_search`/`code_interpreter`<br>✅ Anthropic Messages：自定义 Function Call<br>❌ OpenAI Chat / DashScope：需自行集成 | 同左（多模态输入可作为工具输入） | ❌ 不支持工具调用 | ❌ 不支持工具调用；纯判定，无执行环节 |

---

## 适用场景建议（面向开发者的技术选型指南）

### ✅ 选择 **基础文本模型（Qwen LLM）** 当：
- 需要构建通用对话机器人、知识问答、内容创作、代码辅助等**自由文本生成任务**；
- 要求灵活接入现有 OpenAI/Anthropic 生态（SDK、LangChain、LlamaIndex）；
- 需要**动态调用外部工具**（搜索、计算器、数据库）完成复杂 Agent 流程；
- 场景对输出格式无强约束，或可通过 JSON Schema 显式声明结构。

> **避坑提示**：避免用 LLM 做确定性分类（如“是否违规”），其概率输出不稳定；勿用 `qwen3.8-audio` 的 OpenAI 接口（不支持）。

---

### ✅ 选择 **多模态理解模型（Qwen VL / Audio / Video）** 当：
- 输入含**图像、短视频、语音片段**，需理解其中语义（如“图中是否有危险物品？”、“视频里人物说了什么？”）；
- 构建跨模态检索、图文生成、音视频摘要、教育题库解析等应用；
- 需精细控制视频处理（如指定 `max_frames`、`fps`）或调用语音理解（`qwen3.8-audio`）；
- 可接受较高延迟与多模态 token 成本。

> **避坑提示**：QVQ 模型禁用 `system` 消息；`qwen3.8-audio` 必须用 DashScope 协议；视频输入需预处理为帧列表或公开 URL。

---

### ✅ 选择 **全模态翻译模型（Qwen-MT-Uni）** 当：
- 需翻译**带格式的文档（PDF/DOCX/PPTX）、截图（PNG/JPG）、会议录音（MP3/WAV）或批量文本**，且要求**保留原始排版、表格、图片位置**；
- 支持术语强制替换（`glossary`）与敏感词原样保留（`sensitives`）；
- 面向企业级本地化流水线，需[异步处理](../concepts/asynchronous-processing.md)大文件（如整本技术手册）；
- 对译文一致性、领域适配（`domainHint`）有明确要求。

> **避坑提示**：不支持 `.doc`/`.ppt` 等旧格式，需转 OOXML；URL 中禁止中文字符；`source_lang` 建议显式指定以规避自动识别误差。

---

### ✅ 选择 **结构化决策模型（decision-model-preview）** 当：
- 任务本质是**确定性判定**：工单自动分派（`choice`）、内容安全审核（`noul`）、用户投诉严重度分级（`score`）；
- 要求**毫秒级响应、高并发、结果可解释**（提供各选项概率与置信度）；
- 无需生成描述性文本，拒绝“幻觉”风险；
- 已有结构化上下文（如工单 JSON、对话历史数组），只需注入问题定义即可获得答案。

> **避坑提示**：不可用于摘要、改写、创作等生成任务；`score` 等级强烈建议设为 3–7 级；单次请求问题数建议 ≤16 以保障延迟。

---

## 总结：一句话选型口诀  
> **要“说人话” → 选 Qwen LLM；要“看懂图/听清声” → 选 Qwen VL/Audio；要“翻得准、排版好” → 选 Qwen-MT-Uni；要“快判断、给分数” → 选 decision-model-preview。**  
> 所有模型均通过百炼平台统一管控，优先使用业务空间专属域名与最新 SDK（`dashscope` / `typesafe-sdk`），避免硬编码旧域名。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


