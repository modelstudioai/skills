# Prompt 工程

Prompt 工程是系统化设计、验证、优化和管理提示词（Prompt）的方法论与实践体系，旨在通过结构化框架、自动化工具与数据驱动反馈，持续提升大模型输出的准确性、一致性、可控性与业务适配性。它超越了单次手工编写提示词的范畴，覆盖从模板构建、变量注入、样例增强到 A/B 对比、可观测调试与闭环迭代的全生命周期。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体与工作流应用**：在 Agent 2.0 或工作流配置中，通过 `prompt_template` 字段接入结构化 Prompt 模板（如 ICIO、CRISPE），支持 Jinja2 变量渲染；系统自动将用户输入、工具结果、记忆上下文等注入模板，实现动态提示组装。
- **RAG 增强场景**：Prompt 工程与 RAG 深度协同——模板中预置「检索上下文注入区」（如 `${retrieved_chunks}`），配合 RAG 表格库召回片段，确保模型在精准知识约束下生成答案；避免已弃用的样例库，统一使用 RAG 表格库实现可配置、可扩展的上下文增强。
- **多模态生成（文生图/文生视频）**：万相、Vidu 等模型要求 Prompt 具备分镜语法、正负向控制、参考素材编号（如“图1”“音频2”）等工程化表达；`prompt_extend=true` 可触发平台自动扩写，本质是轻量级 Prompt 工程服务。
- **质量保障闭环（[agenteval](../guides/agenteval.md)）**：Prompt 工程是 [agenteval](../guides/agenteval.md) “观测 → 评测 → 优化” 闭环的核心执行层。开发者基于 Trace 中的真实失败样本，通过「调试&反馈优化」功能提交问题描述与期望行为，平台自动生成优化版 Prompt，并支持版本对比验证。
- **API 集成与高代码开发**：调用 `ChatCompletion` 或 `POST /v1/applications/{app_id}/chat` 时，最终传入模型的 `system` 或 `user` 消息即为 Prompt 工程产出物——由模板 + `variables` 替换 + RAG 注入 + 调试增强后生成的完整、可复现、可审计的字符串。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取内容 | 控制台模板卡片中直接可见；调用 `GetPromptTemplate` 后需解析其 `content` 和 `variables` 字段 |
| `variables` | 模板中声明的占位符列表（如 `${topic}`, `${retrieved_chunks}`） | 必须严格按名称匹配业务数据；缺失或类型错误将导致渲染失败或空值注入 |
| `has_thoughts` | 请求级开关，启用后响应含 `thoughts` 字段，展示样例检索/RAG 召回详情 | **调试必开**：用于验证上下文是否命中、片段是否相关、注入位置是否正确 |
| `retrieval_config`（Agent/文件问答） | 控制 RAG 召回数量（默认 5）、重排序策略、知识库权重 | 影响 Prompt 输入长度与 Token 成本；建议结合 `has_thoughts` 分析实际召回质量再调优 |
| `prompt_extend`（文生图/视频） | 是否启用大模型智能扩写原始 Prompt | 仅适用于万相、Vidu 等支持该能力的模型；扩写结果会参与计费，需评估 ROI |

> ⚠️ 注意：所有 Prompt 工程操作均受地域限制——**仅华北2（北京）地域支持自定义模板、预置模板及自动优化功能**；跨地域调用将返回 403 错误。

## 面向开发者，简洁实用

- ✅ **起步建议**：新项目优先选用「基于 Prompt 工程创建」模板模式，内置 CRISPE/ICIO 框架可快速对齐角色、背景、指令、示例、格式五大要素；避免从零手写模糊指令。
- ✅ **调试黄金组合**：`has_thoughts=true` + `stream=false` + 控制台「调试」页查看完整输入，三者结合可 100% 还原模型看到的 Prompt 内容。
- ✅ **成本控制要点**：RAG 注入每增加 1 个片段（默认最多 10 个），输入 Token 显著上升；若业务允许，优先用 Code 评估器替代 LLM 评估器做格式校验，零 Token 成本。
- ✅ **避坑清单**：
  - 不再使用已下线的 Prompt 样例库，迁移至 RAG 表格库；
  - 单模板内容 ≤ 6144 字符（控制台右下角实时统计）；
  - `variables` 名称区分大小写，`${Topic}` ≠ `${topic}`；
  - 文生视频 Prompt 必须严格按 `[分镜1（00:00-00:03）：...]` 语法书写，否则解析失败。

Prompt 工程不是一次性的技巧，而是百炼平台上可版本化、可评测、可自动化的基础设施能力。每一次 `优化`、每一次 `调试反馈`、每一次 `A/B 对比`，都在沉淀你业务专属的提示资产。

## 关联主题页

- [prompt](../guides/prompt.md)
- [agenteval](../guides/agenteval.md)
- [use cases](../guides/use-cases.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


