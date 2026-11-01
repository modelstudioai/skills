# 专用模型能力对比：Qwen MT 翻译模型与 Decision Model

## 对比目的与背景

在百炼平台的专用模型体系中，**Qwen MT 翻译模型**与**Decision Model（决策模型）** 分属两类截然不同的能力范式：前者聚焦于**多模态内容的语言转换与保真重构**，后者专精于**结构化业务逻辑的确定性推理与可解释判别**。二者虽同属“专用模型”，但设计目标、输入输出语义、调用协议及工程约束存在本质差异。

本对比旨在为开发者提供清晰的技术选型依据——避免将翻译模型误用于规则判别场景（如用 `qwen-mt-plus` 做工单分类），或错误期望决策模型生成自然语言（如要求 `decision-model-preview` 输出翻译结果）。通过系统梳理关键维度，帮助团队快速识别：**何时该用翻译模型？何时必须切换至决策模型？**

---

## 关键能力维度对比

| 维度 | Qwen MT 翻译模型系列 | Decision Model (`decision-model-preview`) |
|------|------------------------|---------------------------------------------|
| **核心定位** | 多模态内容的语言迁移与格式保真（文本/图像/文档/音频） | 结构化业务决策的轻量级并行推理（分类/是非/评分） |
| **输入格式** | • 文本：字符串或数组<br>• 图像：JPG/PNG URL 或 Base64（`qwen-mt-image` 仅支持 JPG）<br>• 文档/音视频：PDF/DOCX/MP3/WAV 等 URL（`qwen-mt-uni` 支持 10+ 格式）<br>• 所有输入需显式指定 `source_lang`/`target_lang` | • `state`：任意结构化上下文（字符串、JSON Object、Array），最大 65,536 tokens<br>• `questions`：定义待求解问题的对象（含 `type`/`criteria`），最多 16 个问题 |
| **输出格式** | • 同步模式：直接返回翻译结果（`translated_text`、`output.image_url`、`output.Data.TranslatedFileUrl` 等）<br>• 异步模式：返回 `task_id`，需轮询获取结果<br>• **始终返回自然语言或二进制资源** | • 固定 JSON 结构：<br> – `choices`: `[{question_id, type, answer, probabilities, confidence?}]`<br> – `noul`: `{question_id, type, probability_yes}`<br> – `score`: `{question_id, type, expected_score, probabilities}`<br>• **不生成任何自由文本，无 token [流式输出](../concepts/streaming-output.md)** |
| **支持模型** | • `qwen-mt-plus`（纯文本）<br>• `qwen-mt-image` / `qwen-mt-image-2.0`（图像）<br>• `qwen-mt-uni`（全模态统一） | • 仅 `decision-model-preview`（预览版，无其他变体） |
| **API 端点** | • 文本：`POST /compatible-mode/v1/chat/completions`（兼容 OpenAI）<br>• 图像/全模态：`POST /api/v1/services/aigc/{image2image|multimodal-generation}/generation`<br>• **端点因模型类型而异，协议不统一** | • 统一端点：`POST /compatible-mode/v1/systemone`（TypeSafe System One 协议）<br>• SDK 封装为 `client.decision.create()`（Python）或 `DecisionModel.call()`（Java） |
| **计费方式** | • 按**输入 token + 输出 token** 计费（文本类）<br>• 图像/文档/音频按**请求次数 + 文件大小（MB）** 计费（如 `qwen-mt-uni` 按 100 MB 分段计费）<br>• [异步任务](../concepts/asynchronous-task.md)按**成功完成次数**计费（失败不扣费） | • 按**单次请求**计费（无论包含 1 个或 16 个问题）<br>• **与输入长度、问题复杂度无关**（固定单价）<br>• 不产生输出 token 费用 |
| **典型场景** | • 技术文档本地化（PDF → 多语言 PDF）<br>• 电商商品图自动翻译（保留图文排版）<br>• 客服对话实时双语转译<br>• 内容出海多格式素材批量翻译 | • 工单智能分流（“归属团队：A/B/C”）<br>• 内容安全审核（“是否涉政：是/否”，置信度 0.98）<br>• 智能体任务完成度打分（1–4 级，期望得分 3.2）<br>• 用户意图路由（“需人工介入：是/否”） |
| **关键限制** | • 术语干预参数名不一致（`terms`/`terminologies`/`glossary`）<br>• 领域提示仅支持英文（`domains`/`domainHint`）<br>• `qwen-mt-image` **强制异步**，`qwen-mt-plus` 不支持敏感词过滤<br>• 文件 URL 不得含中文字符 | • `choice` 选项 ≤255 项；`score` 等级建议 3–7 级<br>• `noul` 类型**无 `confidence` 字段**<br>• `score` 返回小数期望值（如 `2.25`），需业务层映射<br>• 输入 `state` 超 65,536 tokens 直接拒绝 |

---

## 适用场景建议

### ✅ 选择 Qwen MT 翻译模型，当您需要：
- **跨语言内容交付**：将中文技术白皮书翻译为英文 PDF、将日文商品图中的文字翻译为西班牙语并保持排版。
- **多格式自动化处理**：批量上传 500 份 DOCX 合同，一键生成德语/法语/阿拉伯语版本。
- **高保真图文翻译**：电商运营需将含 Logo 和商品主体的宣传图翻译为多语种，且明确要求跳过人物/Logo 区域文字（启用 `imageSegment: true`）。
- **企业级定制能力**：需注入行业术语库（`glossary`）、复用历史翻译记忆（`tm_list`）、或对敏感词做完全匹配拦截（`sensitives`）。

### ✅ 选择 Decision Model，当您需要：
- **低延迟结构化判别**：客服系统每秒处理 200+ 工单，需在 <300ms 内判断“是否紧急”、“归属部门”、“预期解决时长等级”三类问题。
- **可审计的确定性输出**：内容审核结果必须附带各选项概率分布（如 `{"politics": 0.02, "violence": 0.89, "normal": 0.09}`），而非模糊文本描述。
- **规避幻觉风险**：业务逻辑严禁模型自由生成解释性文字（如“因为用户提到了XX，所以判定为高危”），只要干净的 `{"answer": "high", "confidence": 0.94}`。
- **成本敏感型高频调用**：日均百万次简单是非判断（如“用户消息是否含联系方式？”），需稳定单价与可预测账单。

### ⚠️ 明确不适用的情形：
- ❌ **勿用 Qwen MT 做决策**：`qwen-mt-plus` 的 `domains` 参数不能替代 `decision-model-preview` 的 `criteria`；其输出是自然语言，无法直接用于路由逻辑。
- ❌ **勿用 Decision Model 做翻译**：该模型无语言建模能力，不支持 `source_lang`/`target_lang`，输入非文本亦会失败。
- ❌ **勿混合调用协议**：`qwen-mt-plus` 使用 `/chat/completions`，而 `decision-model-preview` 必须走 `/systemone`；混用将导致 404 或 400 错误。

---

## 开发者技术选型参考

| 选型维度 | 推荐动作 |
|----------|----------|
| **接口一致性** | 若团队已深度集成 OpenAI 兼容 SDK，优先选用 `qwen-mt-plus`（文本）；若已采用 TypeSafe SDK 或需强类型校验，`decision-model-preview` 更契合。 |
| **调试效率** | `qwen-mt-*` 模型响应含丰富 `usage` 字段（`input_tokens`, `output_tokens`, `latency_ms`），适合性能压测；`decision-model-preview` 提供 `probabilities` 与 `latency_ms`，便于 A/B 测试置信度阈值。 |
| **错误处理** | `qwen-mt-*` 错误多与文件格式、URL 编码、参数命名相关（如误传 `glossary` 给 `qwen-mt-plus`）；`decision-model-preview` 错误集中于 `state` token 超限或 `criteria` 结构非法，SDK 层已做严格校验。 |
| **灰度发布** | `qwen-mt-uni` 支持同步/异步双模式，可先用同步模式验证小文件，再切异步处理大文档；`decision-model-preview` 无模式切换，建议直接全量上线（其稳定性已在阿里云内部大规模验证）。 |
| **合规要求** | 涉及敏感信息翻译时，必须选用 `qwen-mt-image` 或 `qwen-mt-uni`（支持 `sensitives` 过滤），`qwen-mt-plus` 无此能力；涉及金融/医疗等强监管决策，`decision-model-preview` 的概率化输出更易满足可解释性审计要求。 |

> **最后提醒**：两个模型均需配置地域专属 `DASHSCOPE_API_KEY`（北京/新加坡/弗吉尼亚 Key 不通用），且推荐使用工作空间专属域名（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`）以保障 SLA。请务必查阅各自 API 文档中的最新限制说明，避免因参数细微差异导致线上异常。

## 被对比主题页

- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [decision model](../api/decision-model.md)


