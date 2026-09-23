# Prompt 工程

Prompt 工程是系统化设计、测试、优化和管理提示词（Prompt）的技术实践，旨在通过结构化指令、上下文注入、角色设定、格式约束与迭代反馈等手段，稳定提升大模型在特定任务上的输出质量、一致性、可控性与可维护性。它既是调用大模型的起点，也是 AI 应用效果调优的核心杠杆。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）与工作流（Workflow）**：Prompt 是智能体行为逻辑的“大脑指令”，直接决定其角色定位、工具调用策略、响应风格与输出结构；在工作流中，大模型节点的 Prompt 可绑定变量（如 `{{query}}`、`{{context}}`），实现动态上下文注入，配合 RAG 检索结果完成精准生成。
- **模板化生产**：通过「Prompt 模板」功能，将高频任务（如客服应答、报告摘要、代码评审）封装为可复用、可版本化、可跨应用共享的资产；支持基于 ICIO/CRISPE/RASCEF 等工程框架快速创建，降低人工编写门槛。
- **多模态生成**：文生图（万相）、文生视频（Vidu、万相视频）严格区分 `prompt`（正向描述）与 `negative_prompt`（负向排除），并支持 `prompt_extend=true` 自动扩写，提升画面完整性与美学表现力。
- **AI 应用可观测与优化闭环（[agenteval](../guides/agenteval.md)）**：Prompt 工程深度融入 `agenteval` 体系——通过 Trace 沉淀真实用户 Prompt → 自动归集至评测集 → 多评估器打分 → 基于人工反馈（如“缺少步骤说明”“未按 JSON 格式输出”）驱动 Prompt 智能重构 → 调试验证后发布生效，形成“观测→评测→优化”闭环。
- **RAG 替代演进**：原 Prompt 样例库（few-shot）已下线，其能力由 RAG 表格库承接；此时 Prompt 工程重点转向设计高质量检索增强指令（如 `"请严格依据以下知识片段回答，禁止编造"`），并控制 `recall_count`（默认 5，最大 10）平衡相关性与噪声。

## 关键参数和配置

| 参数名 | 说明 | 开发者须知 |
|--------|------|------------|
| `promptTemplateId` | 模板唯一 ID，用于 API 调用时指定模板 | 必须通过 `GetPromptTemplate` 接口获取，不可硬编码；模板内容变更后 ID 不变，但需重新发布才生效。 |
| `workspaceId` | 业务空间 ID，所有 Prompt 操作均需显式传入 | 控制台调试页可自动填充；跨 workspace 调用将鉴权失败，务必校验当前环境。 |
| `variables` | 模板中声明的占位符列表（如 `["topic", "format"]`） | 由 `GetPromptTemplate` 返回，开发者需据此构造 `inputVariables` 对象，**不可自行拼接字符串**，避免注入风险。 |
| `has_thoughts` | 是否返回思考链/检索过程详情（含 `thoughts` 字段） | 调试阶段设为 `true`；上线前必须设为 `false`，避免泄露内部逻辑或敏感上下文。 |
| `recall_count` | RAG 表格库召回片段数（替代原样例库） | 默认 5，建议根据知识密度调整：高精度问答可设为 3–5；开放摘要类任务可设为 8–10。 |
| `enable_thinking` / `preserve_thinking` | 控制模型是否启用推理链及是否跨轮次保留 | 仅部分模型（如 `qwen-max`, `kimi-k2.6+`, `glm-5.2+`）支持；开启后需解析 `reasoning_content` 字段，且 `preserve_thinking=true` 时需确保 `historyList` 正确传递。 |

## 面向开发者，简洁实用

- ✅ **优先用模板，而非硬编码 Prompt**：所有生产环境 Prompt 必须走 `CreatePromptTemplate` → `GetPromptTemplate` → 变量替换流程，保障可灰度、可回滚、可审计。
- ✅ **调试必开 `has_thoughts=true`**：在控制台或 SDK 调试时开启，快速定位是 Prompt 表达不清、RAG 检索不准，还是模型理解偏差。
- ✅ **优化不靠直觉，靠 `agenteval` 闭环**：从线上 Trace 抽取 bad case → 创建评测任务 → 人工标注问题 → 发起反馈优化 → **必须验证回归**（原问题+正常流程+边界输入）→ 再发布。
- ⚠️ **地域强约束**：全部 Prompt 功能（模板、优化、RAG 集成）**仅支持华北2（北京）地域**，跨地域调用会返回 `InvalidRegionId` 错误。
- ⚠️ **字符上限严守**：单个自定义 Prompt 模板内容 ≤ 6144 字符（含空格与换行），超长需精简指令或拆分为多阶段工作流。
- ⚠️ **负向 Prompt 不是万能**：万相图生图中 `negative_prompt` 对抽象概念（如“低质量”“不专业”）效果有限，应聚焦具体可识别元素（如 `"blurry, deformed hands, extra fingers, text, watermark"`）。

## 关联主题页

- [prompt](../guides/prompt.md)
- [agenteval](../guides/agenteval.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)
- [use cases](../guides/use-cases.md)


