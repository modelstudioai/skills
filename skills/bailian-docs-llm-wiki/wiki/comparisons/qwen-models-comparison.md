# Qwen 系列模型能力对比

为帮助开发者在阿里云百炼平台上高效选型，本文系统对比 Qwen 系列中三类核心能力模型：**通用大语言模型（Qwen-LLM）**、**专业机器翻译模型（Qwen-MT）** 和 **结构化决策模型（Decision Model）**。对比基于当前（2024年Q3）百炼平台正式发布的 API 能力与生产实践反馈，聚焦接口协议、输入输出范式、模型特性及工程适配性，旨在为技术架构设计、Agent 编排、企业级集成等场景提供可落地的选型依据。

---

## 关键维度对比

| 维度 | Qwen 通用大语言模型（Qwen-LLM） | Qwen 专业翻译模型（Qwen-MT） | 结构化决策模型（Decision Model） |
|------|----------------------------------|------------------------------|-----------------------------------|
| **输入格式** | • `messages` 数组（Chat/Anthropic）<br>• `string` 或 `array`（Responses）<br>• 支持 `input_audio`/`input_video`（仅 `qwen3.8-omni-flash`）<br>• 多模态输入需显式指定 `fps`/`total_pixels` 等预处理参数 | • 文本：`source_texts` 字符串或数组<br>• 图像：`image_url` 或 Base64<br>• 文档/音频：`fileUrl`（公网可访问 URL）<br>• 所有输入自动识别模态（`qwen-mt-uni`） | • `state`：任意类型（string/object/array），序列化为字符串送入模型<br>• `questions`：严格定义的 JSON 对象，含 `type`/`criteria`/`instructions`<br>• **不接受自由文本 prompt** |
| **输出格式** | • 自由文本生成（含思考链、工具调用响应）<br>• Anthropic 协议支持强约束 `json_schema` 输出<br>• Responses API 可返回结构化 `tool_calls` + `content` 混合结果 | • 同步：纯文本译文（`qwen-mt-plus`）、带排版保留的图像译图（`qwen-mt-image`）、重构后文档/音视频（`qwen-mt-uni`）<br>• 异步：返回 `task_id`，轮询获取最终文件 URL 或结构化结果 | • **纯结构化 JSON**：<br> – `choice`: `{ "selected": "...", "probabilities": {...}, "confidence": 0.92 }`<br> – `noul`: `{ "p_yes": 0.87, "confidence": 0.95 }`<br> – `score`: `{ "expected_score": 3.2, "probabilities": [0.05, 0.15, 0.65, 0.15], "confidence": 0.89 }`<br>• **无自由文本生成字段** |
| **支持模型** | • 主流 Qwen 系列：`qwen3.8-max`, `qwen3.8-flash`, `qwen3.7-plus`, `qwen3-vl-plus`, `qwen3.8-omni-flash` 等<br>• 开源模型：`qwen3.5-397b-a17b`, `qwen3.8-27b`<br>• 第三方直供模型（DeepSeek/Kimi/GLM/MiniMax） | • `qwen-mt-plus`：纯文本翻译<br>• `qwen-mt-image` / `qwen-mt-image-2.0`：图像翻译（后者支持 55 语种互译）<br>• `qwen-mt-uni`：全模态统一翻译（文本/文档/图像/音频） | • 唯一模型：`decision-model-preview`（预览版，无变体） |
| **API 端点** | • OpenAI 兼容：`/compatible-mode/v1/chat/completions`（Chat）、`/compatible-mode/v1/responses`（Responses）<br>• Anthropic 兼容：`/apps/anthropic/v1/messages`<br>• DashScope 原生：`/api/v1/services/aigc/text-generation/generation`（文本）、`/api/v1/services/aigc/multimodal-generation/generation`（多模态） | • `qwen-mt-plus`：OpenAI 兼容端点 `/compatible-mode/v1/chat/completions`（通过 `extra_body` 传参）<br>• `qwen-mt-image-*`：DashScope 专用 `/api/v1/services/aigc/image2image/image-synthesis`<br>• `qwen-mt-uni`：DashScope 统一端点 `/api/v1/services/aigc/multimodal-generation/generation` | • TypeSafe System One 协议端点：<br>`/compatible-mode/v1/systemone`（**唯一路径，不可复用其他协议端点**） |
| **计费方式** | • 按 **输入 Token + 输出 Token** 计费（含思考 Token，部分模型需单独控制 `thinking.budget_tokens`）<br>• 多模态输入按像素/时长折算 Token（如 `total_pixels` 影响计费） | • 按 **请求次数 + 输入规模** 计费：<br> – 文本：字符数<br> – 图像：宽×高像素数<br> – 文档/音频：文件大小（MB）<br>• 异步任务按完成量计费（非请求量） | • 按 **单次推理调用** 计费（flat fee）<br>• 与 `state` 长度、`questions` 数量、`criteria` 规模无关（但超限将拒绝） |
| **典型场景** | • 智能对话 Agent（支持工具调用、多轮上下文）<br>• 多模态理解（图文问答、视频摘要、音视频分析）<br>• 代码生成、逻辑推理、内容创作 | • 企业级本地化流水线（术语/记忆/领域控制）<br>• 扫描件/PDF/截图批量翻译（保留格式）<br>• 跨模态内容出海（PPT 翻译+排版重构、会议录音转双语字幕） | • 工单智能分派（“归属团队”+“紧急程度”+“是否合规”三问并行）<br>• 内容安全审核（“涉政”、“涉黄”、“涉暴”多标签置信度）<br>• Agent 任务路由决策（低延迟、高确定性要求） |

---

## 适用场景建议

### ✅ 选择 Qwen-LLM 当：
- 需要**生成自然语言响应**（如客服对话、报告撰写、创意文案）；
- 业务涉及**多模态输入理解**（上传图片提问、分析会议录像、听语音写纪要）；
- 要求**动态工具调用能力**（实时搜索、代码执行、网页提取）；
- 已有 OpenAI/Anthropic SDK 技术栈，追求**最小迁移成本**；
- 接受一定不确定性，需 `temperature`/`top_p` 等采样控制。

> ⚠️ 注意：避免用于强结构化输出需求（如固定字段 JSON），除非使用 Anthropic `json_schema` 并接受其严格校验开销；Qwen-Audio 模型仅支持 DashScope 原生协议。

### ✅ 选择 Qwen-MT 当：
- 核心诉求是**高质量、可控、保格式的翻译结果**，而非通用生成；
- 输入来源复杂（扫描PDF、手机截图、会议录音、电商商品图）；
- 需要**术语强制干预**（如产品名、品牌词）、**翻译记忆复用**（历史句对）、**领域风格引导**（`domainHint`）；
- 处理长文档/大图像/长音频，需**异步任务管理能力**；
- 语言对超出中英（如阿拉伯语↔日语），且需 `auto` 语言识别。

> ⚠️ 注意：`qwen-mt-plus` 不支持图像/文档；`qwen-mt-image` 限制中英文；推荐新项目直接使用 `qwen-mt-uni` 作为统一入口。

### ✅ 选择 Decision Model 当：
- 业务本质是**分类、判断、打分**，且需**概率分布与置信度**（非简单 yes/no）；
- 要求**毫秒级确定性响应**（无采样、无随机性），拒绝“幻觉”；
- 需在同一推理中**联合求解多个正交问题**（如同时判断“是否欺诈”+“风险等级”+“推荐处置动作”）；
- 系统已采用 TypeSafe 协议，或愿意引入 `typesafe-sdk` 提升解析鲁棒性；
- 审计/合规场景下，必须可追溯每个决策的置信依据。

> ⚠️ 注意：不适用于需要生成解释性文字的场景（如“为什么判定为高风险？”）；`state` 超 65536 token 将被截断，需前置摘要。

---

## 开发者技术选型参考

| 选型考量 | 推荐方案 | 理由 |
|----------|----------|------|
| **已有 OpenAI SDK，快速接入** | Qwen-LLM（OpenAI Chat/Responses） | 协议完全兼容，仅需切换 `base_url` 和 `model`，零代码改造即可启用 Qwen3.8 等新模型。 |
| **需强结构化输出（JSON Schema）且重视字段校验** | Qwen-LLM（Anthropic Messages） | `output_config.format.json_schema` 提供最严格的 JSON 类型/层级/必填校验，优于 OpenAI 的 `response_format`。 |
| **企业翻译流水线，强调术语/记忆/领域控制** | Qwen-MT（`qwen-mt-uni` + `glossary`/`tm_list`/`domainHint`） | 唯一支持三者协同的模型，且 `qwen-mt-uni` 统一接口大幅降低运维复杂度。 |
| **低延迟决策服务（<500ms），需概率与置信度** | Decision Model | 确定性前向推理，无 Token 采样开销；输出即解析结果，无需 NLP 后处理。 |
| **多模态理解 + 翻译一体化（如“看图翻译+生成摘要”）** | Qwen-LLM（`qwen3.8-omni-flash`） + Qwen-MT（`qwen-mt-uni`）组合调用 | Qwen-LLM 负责理解与规划，Qwen-MT 专注翻译，职责分离更健壮；避免在单一模型上堆砌非核心能力。 |
| **成本敏感型高频小文本翻译（如 App 内 UI 字符串）** | Qwen-MT（`qwen-mt-plus`） | 按字符计费，远低于 LLM 按 Token 计费模式；无多模态冗余开销。 |

> 💡 **最佳实践提示**：  
> - 所有模型均**优先使用业务空间专属域名**（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），保障性能与 SLA；  
> - 多模态场景务必设置 `total_pixels` 等参数防 Token 溢出；  
> - 决策模型首次上线前，务必通过 Playground 验证 `questions` 定义合理性；  
> - Qwen-MT 异步任务需实现幂等轮询逻辑，避免重复提交。  

---  
*本文档依据百炼平台 2024 年 Q3 版本 API 文档整理，能力细节请以控制台实际可用模型列表及最新 API 参考为准。*

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


