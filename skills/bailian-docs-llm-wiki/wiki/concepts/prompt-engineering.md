# Prompt 工程

Prompt 工程是百炼平台上系统化设计、管理与优化大语言模型输入指令（Prompt）的方法论与技术实践，其核心目标是通过结构化表达任务意图、约束条件与输出规范，显著提升模型响应的准确性、一致性、可控性与业务适配性。它不是一次性提示词编写，而是涵盖模板化、可复用、可评测、可迭代的全生命周期工程能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）与工作流应用**：在 Agent 2.0 或工作流的大模型节点中，系统提示词（System Prompt）和用户输入动态拼接逻辑均依托 Prompt 模板实现。开发者通过控制台选择预置模板（如“客服问答”“技术文档摘要”）或自定义模板，将业务变量（如 `{{product_name}}`、`{{user_intent}}`）注入结构化框架（如 CRISPE 或 RASCEF），确保每次调用语义一致、格式合规。

- **RAG 增强场景**：虽样例库（Few-shot）功能已停用，但 Prompt 工程仍深度融入 RAG 流程——通过模板统一构造检索后上下文注入格式（例如 `"根据以下知识片段回答：{retrieved_chunks}。问题：{query}"`），并配合 `prompt_extend=true` 启用大模型对原始查询的智能重写，提升召回相关性与答案生成质量。

- **多模态生成（文生图/文生视频）**：Prompt 工程体现为分层公式实践。例如万相 3.0 视频生成要求严格遵循“总体描述 + 分镜时间戳 + 运动/镜头关键词 + 负向清单”结构；文生图则需分离 `prompt`（正向）与 `negative_prompt`（负向），并通过 `prompt_extend` 自动补全美学与细节修饰词，降低人工调优成本。

- **Agenteval 评测与优化闭环**：在 `agenteval` 模块中，Prompt 工程是可观测与可优化的核心对象。开发者可基于 Trace 数据筛选低分对话样本，发起多版本 Prompt A/B 对比测试；或提交人工反馈（如“输出遗漏价格信息”），由平台驱动 Prompt 反馈优化流程，自动生成带边界说明与 Few-shot 示例的新版 Prompt。

- **模型评测与选型验证**：当使用模型评测功能评估不同 LLM 效能时，高质量 Prompt 是评测有效性的前提。平台推荐使用结构化 Prompt 框架构建评测数据集中的 `Prompt` 字段，并通过 `agenteval` 的 Prompt 优化能力持续提升基准 Prompt 质量，避免因 Prompt 缺陷导致模型能力误判。

## 关键参数和配置

- `workspaceId`：必填，标识业务空间，所有 Prompt 操作（模板调用、优化、关联知识库）均需指定。通过控制台「应用管理」或 API 获取。

- `promptTemplateId`：必填，模板唯一 ID。预置模板 ID 在控制台模板卡片底部显示；自定义模板 ID 由 `CreatePromptTemplate` 接口返回。

- `variables`：只读，由 `GetPromptTemplate` 接口返回，声明模板中支持的动态变量名（如 `["topic", "tone", "output_format"]`），不可自行增删，填充时需严格匹配。

- `prompt_extend`：布尔型，适用于文生图、文生视频等多模态模型请求体。设为 `true` 时，平台自动调用大模型对原始 Prompt 进行扩写与风格增强（默认启用）。

- `has_thoughts=true`：调试专用参数，仅用于 API 请求头或请求体。启用后响应中返回 `thoughts` 字段，展示样例检索、知识召回等中间过程，便于定位 Prompt 执行链路问题。

- 地域约束：所有 Prompt 工程能力（模板、优化、RAG 注入）**仅在华北2（北京）地域可用**，跨地域调用将失败。

## 面向开发者，简洁实用

- ✅ **优先用模板，而非硬编码**：即使简单任务，也应创建最小化模板（如 `{{query}}，请用中文、不超过100字回答。`），实现 Prompt 集中管理、灰度发布与快速回滚。

- ✅ **结构化是底线**：采用 ICIO（Input-Context-Instruction-Output）或 CRISPE（Capacity-Role-Insight-Statement-Personality-Experiment）等框架设计模板，明确区分背景、角色、约束与格式，避免模糊指令。

- ✅ **RAG 替代 Few-shot**：样例库已下线，新项目一律使用 RAG 表格库（上传 `query`/`answer` Excel）替代。在 Prompt 模板中用 `{retrieved_answer}` 占位符引用召回内容，保持逻辑清晰。

- ✅ **优化有路径，不靠玄学**：
  - 快速提效 → 用「Prompt 自动优化」API（无需样例）；
  - 业务强规则 → 用「Prompt 反馈优化」（需 ≥5 条问题样例 + ≥20 条评测数据）；
  - 持续改进 → 结合 `agenteval` 的 Trace 分析 + 多版本对比 + 人工反馈闭环。

- ⚠️ **注意限制**：单模板最大 6144 字符；所有操作必须在北京地域；高频动态 Prompt（如每请求变量超 20 个）若对延迟敏感，可权衡改用代码内联，但需自行承担维护成本。

## 关联主题页

- [prompt](../guides/prompt.md)
- [agenteval](../guides/agenteval.md)
- [use cases](../guides/use-cases.md)
- [llm application](../guides/llm-application.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


