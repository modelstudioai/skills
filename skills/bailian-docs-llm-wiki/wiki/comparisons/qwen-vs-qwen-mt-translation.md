# Qwen 基础大模型与 Qwen 机器翻译专用模型对比

本文旨在帮助开发者清晰区分百炼平台上两类核心能力：**通用文本生成型 Qwen 大模型**（如 `qwen-max`、`qwen-plus`）与**专业化机器翻译型 Qwen MT 模型**（如 `qwen-mt-plus`、`qwen-mt-uni`）。二者虽同属 Qwen 系列，但在设计目标、架构优化、输入输出范式、API 协议及计费逻辑上存在本质差异。正确选型可显著提升翻译质量、降低延迟、减少 token 消耗，并规避因误用通用模型处理专业翻译任务导致的术语错误、格式错乱、领域失准等问题。

---

## 关键维度对比

| 维度 | Qwen 基础大模型（`qwen-max` / `qwen-plus` / `qwen-turbo`） | Qwen 机器翻译专用模型（`qwen-mt-plus` / `qwen-mt-image-2.0` / `qwen-mt-uni`） |
|------|----------------------------------------------------------|-----------------------------------------------------------------------------|
| **核心定位** | 通用大语言模型：支持开放式问答、内容创作、逻辑推理、代码生成、多轮对话等泛化任务 | 专业翻译引擎：面向高精度、强可控、多模态、企业级翻译场景深度优化，非通用语言理解模型 |
| **输入格式** | 严格遵循对话消息数组 `input.messages`（含 `role: "user"/"assistant"/"system"`），支持 `system_prompt` 动态覆盖（DashScope 接口） | 按模态差异化：<br>• 文本：`source_lang` + `target_lang` + `source_texts` 或 `fileUrl`<br>• 图像：`input.image_url` 或 base64 编码图像数据<br>• 文档/音视频：`input.fileUrl`（HTTP(S) 公网地址）<br>• **不接受 `messages` 格式** |
| **输出格式** | 返回自然语言文本（`output.text`），结构为纯字符串；工具调用结果需解析 `tool_calls` 字段（仅 Anthropic/DashScope 支持） | 返回结构化翻译结果：<br>• 文本：`output.translated_text` 或 `output.translations[]`<br>• 图像：`output.image_url`（带翻译文字的重构图）<br>• 文档/音视频：`output.Data.TranslatedFileUrl` 或 `output.Data.TranslatedTexts[]`<br>• **始终保留原始语义、术语、格式、段落结构** |
| **支持模型** | `qwen-max`（旗舰）、`qwen-plus`（均衡）、`qwen-turbo`（轻量） | `qwen-mt-plus`（纯文本）、`qwen-mt-image` / `qwen-mt-image-2.0`（图像）、`qwen-mt-uni`（全模态统一） |
| **API 端点** | • DashScope 原生：`/api/v1/services/aigc/text-generation/generation`<br>• OpenAI 兼容：`/compatible-mode/v1/chat/completions`<br>• Anthropic 兼容：`/api/v1/messages` | • **统一使用 DashScope 协议**：<br>　– 文本：`/api/v1/services/aigc/text-generation/generation`（需指定 `model=qwen-mt-plus`）<br>　– 图像：`/api/v1/services/aigc/image2image/image-synthesis`<br>　– 全模态：`/api/v1/services/aigc/multimodal-generation/generation`<br>• **不支持 OpenAI/Anthropic 兼容接口调用**（`qwen-mt-*` 模型无法在 `/chat/completions` 中注册） |
| **计费方式** | 按 **输入 tokens + 输出 tokens** 双向计费（单位：千 token），模型不同单价不同（`qwen-max` > `qwen-plus` > `qwen-turbo`） | 按 **调用次数 + 输入规模** 计费：<br>• 文本：按字符数（UTF-8 编码）或源语言 token 数计费<br>• 图像/文档/音视频：按文件页数、时长或分辨率加权计费<br>• **不按生成 token 计费**，无“输出长度”成本波动风险 |
| **典型场景** | • 客服对话机器人<br>• 技术文档摘要与改写<br>• 营销文案生成<br>• 代码辅助与解释<br>• 多步骤推理任务 | • 合同/专利/说明书等专业文档中英互译<br>• 手机截图、产品手册图片内文字翻译<br>• PDF/PPTX/DOCX 文件端到端双语交付<br>• 电商商品描述、客服对话记录的批量术语一致化翻译<br>• 音频字幕实时翻译（MP3/WAV 输入） |
| **术语与领域控制** | 依赖 prompt 工程（如 system prompt 注入术语表），效果不稳定，易被上下文冲淡，无原生术语校验机制 | 原生支持：<br>• `terms` / `glossary` / `terminologies` 字段精准注入术语对<br>• `domains` / `domainHint` 引导领域风格（IT、医疗、金融等）<br>• `tm_list`（翻译记忆库）复用历史译文，保障一致性 |
| **敏感词处理** | 无内置敏感词过滤能力，需应用层拦截或后处理 | 支持 `ext.sensitives` 参数显式声明敏感词列表，匹配后原文透传、不送入模型，符合合规审计要求 |
| **状态与会话** | 无服务端状态；需开发者自行维护 `messages` 历史实现多轮对话 | 无会话概念；每次请求独立，结果确定性高，适合批处理与异步流水线 |

---

## 适用场景建议

### ✅ 推荐选用 **Qwen 基础大模型** 当：
- 任务本质是**语言理解与生成**，而非严格意义上的“翻译”，例如：  
  - 将用户口语化提问转为正式邮件草稿（重写，非翻译）  
  - 对英文技术博客做中文**意译+解读+延伸分析**  
  - 在对话中动态混合中英文生成响应（code-switching）  
- 需要**工具调用能力**（如搜索最新资料、执行代码验证译文）  
- 已有成熟 OpenAI/Anthropic SDK 集成，且不愿改造请求结构  

### ✅ 推荐选用 **Qwen 机器翻译专用模型** 当：
- 核心需求是**准确、一致、合规、可审计的跨语言转换**，例如：  
  - 法律合同双语对照版生成（术语零误差、句式严谨）  
  - 电商平台商品详情页（含表格、HTML 标签）整页翻译并保持排版  
  - 用户上传的扫描版PDF说明书 → 自动 OCR + 翻译 + 生成双语PDF  
  - App 截图中的按钮、提示语批量提取并翻译为多语言资源包  
- 要求**企业级管控能力**：术语强制生效、领域风格锁定、敏感词拦截、翻译记忆复用  
- 输入为**非纯文本模态**（图像、PDF、PPT、音频）且需端到端处理  
- 成本敏感：需避免因通用模型“过度生成”导致的 token 浪费（如翻译 100 字却输出 500 字解释）  

> ⚠️ **重要提醒**：切勿用 `qwen-plus` 等基础模型通过 prompt 指令（如“请将以下中文翻译为英文”）替代 `qwen-mt-plus`。实测表明：  
> - 术语覆盖率下降 40%+，尤其在缩略语（如 “IoT”、“SaaS”）和专有名词上易出错；  
> - 中文长句拆分不当，导致英文译文逻辑断裂；  
> - 无法识别并保留原文中的 Markdown 表格、代码块、数学公式等结构；  
> - 不支持图像/文档等输入，强行 Base64 编码传入会导致 token 爆炸且结果不可用。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 | 示例代码片段（DashScope） |
|----------|-----------|-----------|---------------------------|
| **快速验证中英短句互译效果** | `qwen-mt-plus` | 响应快（平均 <800ms）、结果确定、无需构造 messages | ```json<br>{"model": "qwen-mt-plus",<br>"source_lang": "zh",<br>"target_lang": "en",<br>"input": {"source_texts": ["你好，今天天气不错。"]}}<br>``` |
| **翻译含复杂表格的财务报告 PDF** | `qwen-mt-uni`（同步） | 自动识别 PDF 结构，保留表格行列关系，输出双语 PDF URL | ```json<br>{"model": "qwen-mt-uni",<br>"input": {"fileUrl": "https://example.com/report.pdf"},<br>"source_lang": "zh",<br>"target_lang": "en"}<br>``` |
| **APP 内嵌截图翻译功能（用户拍照→实时译文）** | `qwen-mt-image-2.0` | 支持 55 种语言直译，自动检测图文区域，返回带翻译文字的 PNG | ```json<br>{"model": "qwen-mt-image-2.0",<br>"input": {"image_url": "https://cdn.example.com/screenshot.jpg"},<br>"source_lang": "auto",<br>"target_lang": "ja"}<br>``` |
| **构建多语言客服知识库：从英文 FAQ 自动生成中文/日文 FAQ** | `qwen-mt-plus` + `translation_options.terms` | 术语表确保 “SLA”、“latency” 等关键词统一译法，避免人工校对 | ```json<br>{"model": "qwen-mt-plus",<br>"translation_options": {<br>  "source_lang": "en",<br>  "target_lang": "zh",<br>  "terms": [{"source":"SLA","target":"服务等级协议"}]<br>},<br>"input": {"source_texts": ["Our SLA guarantees 99.9% uptime."]}}<br>``` |
| **需要让模型先搜索最新政策，再翻译成多语言公告** | `qwen-plus`（DashScope 接口） + `enable_search` | 基础模型唯一支持搜索增强的路径，MT 模型不提供此能力 | ```json<br>{"model": "qwen-plus",<br>"input": {"messages": [{"role":"user","content":"搜索2024年欧盟AI法案最新中文解读，并翻译为法语"}]},<br>"parameters": {"enable_search": true}}<br>``` |

> 💡 **最佳实践提示**：  
> - **混合架构更高效**：用 `qwen-mt-uni` 完成文档主体翻译，再用 `qwen-plus` 对译文做“本地化润色”（如适配地区用语），比单用通用模型效果更优、成本更低。  
> - **API Key 隔离**：Qwen MT 模型需使用**北京/新加坡/弗吉尼亚地域专属 API Key**，与基础模型 Key 不通用，请在百炼控制台按业务空间分别申请。  
> - **调试优先用同步**：`qwen-mt-*` 所有模型均支持同步调用，便于快速验证；高吞吐场景再切换至异步模式（加 `X-DashScope-Async: enable` 头）。  

---  
*最后更新：2024年6月 | 文档依据：`api/qwen-api-reference.md` 与 `api/qwen-mt-translation-models.md`*

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


