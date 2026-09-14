# Prompt 工程

Prompt 工程是系统性设计、构建、测试与优化提示词（Prompt）以精准引导大模型生成高质量、可复现、任务一致输出的技术实践。它不是简单的“写一句话”，而是融合语言建模理解、任务拆解、上下文编排、变量抽象与数据驱动迭代的工程化方法。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，Prompt 工程贯穿多个核心能力层，具体体现为：

- **Prompt 模板管理**：通过控制台或 API 创建结构化 Jinja2 模板（如 `{{ input }}`、`{{ history }}`、`{{ knowledge }}`），实现提示词的版本化、复用化与团队协作；模板可被 Skill、LLM 应用、RAG 流程等直接引用，确保行为统一。
  
- **Skill 封装中**：`prompt_template` 是 Skill 的必配字段，开发者在此完成角色设定、任务指令、约束条件（如 JSON 格式要求）、少样本示例（few-shot）及输出解析引导，使 Skill 成为可调试、可发布、带语义契约的 AI 能力单元。

- **LLM 应用开发中**：新版智能体（Agent 2.0）和工作流应用支持节点级 Prompt 编排，允许为不同工具调用、路由分支或后处理步骤配置专属提示词，实现多阶段逻辑控制；文件问答类应用则自动注入知识库检索结果到系统 Prompt 中，属隐式 Prompt 工程实践。

- **模型体验（Model Experience）调试中**：开发者可实时编辑 Prompt、调整参数（如 `temperature`）、上传图文混合输入并即时观察输出变化，是低门槛验证 Prompt 效果、定位表达歧义、探索多模态指令格式的核心沙箱环境。

- **RAG 与企业集成场景中**：Prompt 工程决定如何将检索片段（chunks）自然融入指令（如“根据以下资料回答…”）、如何抑制幻觉、如何强制引用来源；在企业微信/钉钉 Bot 集成中，还需适配消息协议（如@机器人触发词、卡片按钮文案），属于端到端 Prompt 工程落地。

- **自动优化能力中**：当启用 `optimize_mode="auto"` 或 `"feedback"` 时，平台基于历史调用日志与人工反馈，对原始 Prompt 进行重写（如强化指令明确性、补全隐含约束、重构 few-shot 示例），本质是将 Prompt 工程过程部分自动化——但需注意，该能力仅对 `qwen-max`、`qwen-plus`、`qwen-turbo` 生效。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 |
|------|----------|------|------|
| `template_id` | Prompt 模板调用 | string | 必填。模板唯一标识，用于 `/v1/prompt/render` 接口渲染。 |
| `variables` | Prompt 渲染 / Skill 调用 | JSON object | 必填（若模板含占位符）。键值对形式填充模板变量，如 `{"input": "用户问题", "history": [...]}`。 |
| `prompt_template` | Skill 创建 | string (Jinja2) | 必填。定义完整提示结构，支持 `{{ input }}`、`{{ history }}`、`{{ tools }}` 等上下文变量及条件语法 `{% if ... %}`。 |
| `optimize_mode` | Prompt 优化调用 | `"auto"` \| `"feedback"` | 可选。启用自动重写策略；`"feedback"` 要求已提交 ≥5 条有效人工反馈，否则降级。 |
| `X-Bailian-Prompt-Optimize: true` | HTTP 请求头 | header | 必须显式添加，且仅对模板路径（`/v1/prompt/render` + 优化模式）生效。 |
| `enable_retrieval` + `retrieval_context` | RAG 应用 | boolean / string | 非 Prompt 参数但强相关：开启后平台自动注入检索结果至系统 Prompt，开发者需在 `prompt_template` 中预留 `{{ retrieval_context }}` 占位符。 |

> ⚠️ 注意：所有 Prompt 渲染后总长度（含变量展开）不得超过 8192 token；超长将被截断并返回警告。建议在模板中合理控制 `{{ history }}` 长度或启用滑动窗口机制。

## 面向开发者，简洁实用

- **起步建议**：从「模型体验」页面开始——粘贴你的业务需求描述，手动迭代 Prompt，观察输出稳定性；确认效果后，复制最终 [prompt](../guides/prompt.md) 字符串，转为 Skill 的 `prompt_template` 或 Prompt 模板。
  
- **模板设计原则**：
  - 明确角色（Role）：`你是一个资深法律助理，专精劳动合同纠纷…`
  - 清晰任务（Task）：`请逐条分析以下条款是否违反《劳动合同法》第XX条，并标注依据原文。`
  - 约束输出（Format）：`严格按 JSON 格式返回：{"violations": [{"clause": "...", "law_article": "...", "explanation": "..."}]}`。
  - 提供示例（Few-shot）：在模板末尾添加 1–3 个高质量输入-输出对，显著提升泛化能力。

- **避坑提醒**：
  - 不要依赖模型“猜意图”：所有关键约束（如长度、格式、禁止内容）必须显式写出；
  - 变量命名保持语义清晰（如用 `{{ user_query }}` 而非 `{{ q }}`），便于协作与调试；
  - 使用 Skill 或 Prompt 模板时，避免在代码中拼接字符串构造 [prompt](../guides/prompt.md)——这会绕过所有平台优化能力；
  - `optimize_mode` 是辅助手段，不能替代人工设计；上线前务必在真实数据上 A/B 测试优化前后效果。

- **进阶动作**：
  - 将高频 Prompt 模板沉淀为组织级资产，在控制台「样例库」中共享；
  - 对关键业务 Prompt，开启 `optimize_mode=feedback` 并推动运营/客服人员提交反馈，持续提升准确率；
  - 结合 LlamaIndex 或自定义 RAG 流程，在 `prompt_template` 中动态注入 `{{ retrieval_context }}`，实现知识增强。

## 关联主题页

- [prompt](../guides/prompt.md)
- [skill](../guides/skill.md)
- [model experience](../guides/model-experience.md)
- [llm application](../guides/llm-application.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)


