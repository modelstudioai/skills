# Prompt 工程

Prompt 工程是系统性设计、优化与管理大语言模型输入指令（Prompt）的方法论与实践体系，旨在通过结构化表达任务目标、角色设定、约束条件与输出格式，显著提升模型响应的准确性、一致性、可控性与业务适配性。在百炼平台中，它不是一次性技巧，而是可复用、可版本化、可自动迭代的工程能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）与工作流（Workflow）构建**：在 Flow Agent 可视化编排中，LLM 节点的核心即为 Prompt 工程——开发者可直接填写基础 Prompt，或绑定已发布的 Prompt 模板（`promptTemplateId`），实现提示词的统一管理与跨应用复用；Agent 2.0 的记忆机制与 RAG 注入也需通过 Prompt 显式引导模型如何融合上下文。
  
- **RAG 应用开发**：Prompt 是连接检索结果与生成质量的关键枢纽。例如，在客服助手场景中，需设计 Prompt 明确指示“仅基于以下知识库片段作答，若无依据则回答‘暂未获取相关信息’”，避免幻觉；RAG 表格库替代原样例库后，Prompt 需配合 `recall_count` 参数控制注入片段数量，并通过变量（如 `${retrieved_faq}`）动态拼接上下文。

- **低代码/无代码应用集成**：网站、微信公众号、钉钉等渠道的 AI 助手均依赖预设 Prompt 定义角色（如“你叫小助，专注解答产品问题”）、语气（“简洁专业，每句不超过20字”）和安全边界（“不回答政治、医疗建议类问题”），确保多端体验一致。

- **模型调用直连（API/SDK）**：开发者可绕过模板，直接构造 ChatML 格式 `messages`，其中 `system` 角色消息即为 Prompt 主体；支持启用 `enable_thinking` 或 `reasoning_effort` 等参数，将 Prompt 工程延伸至推理过程控制。

- **自动化优化闭环**：通过「反馈优化」功能，以真实 query-answer 样例驱动 Prompt 迭代——平台基于评测数据自动生成多个候选 Prompt，并筛选最优解，实现从人工调优到数据驱动的工程升级。

> ⚠️ 注意：原「Prompt 样例库」功能已下线，新项目请统一迁移至 RAG 表格库 + 结构化 Prompt 模板组合方案。

## 关键参数和配置

| 参数 | 说明 | 典型取值/建议 | 使用位置 |
|------|------|----------------|-----------|
| `promptTemplateId` | Prompt 模板唯一标识 | `pt-xxx`（控制台创建后生成） | 所有模板调用场景（API/SDK/Flow Agent） |
| `variables` | 模板中待填充的占位符列表 | `["user_query", "product_name"]`，对应 `${user_query}` 语法 | 模板定义与 API 调用时传入 `variables` 字段 |
| `recall_count` | RAG 表格库召回片段数 | `3`–`5`（平衡信息量与噪声） | RAG 表格库配置、Prompt 中变量引用逻辑 |
| `has_thoughts` | 启用调试信息输出 | `true`（响应中返回 `thoughts` 字段，含优化/检索过程） | 调试阶段 API 请求头或请求体 |
| `temperature` | 控制生成随机性 | `0.1`–`0.3`（确定性任务如客服问答） | LLM 节点配置、API 请求参数 |

## 面向开发者，简洁实用

- ✅ **起步推荐**：优先使用预置 Prompt 模板（`type=System`），再基于 [ICIO / CRISPE / RASCEF](raw/application-user-guide/prompt/prompt-custom-template.md) 框架微调，确保指令清晰、角色明确、输出可预期。  
- ✅ **必做验证**：所有自定义 Prompt 上线前，务必在控制台「测试」面板输入典型 `inputs`，检查输出格式、长度、安全性是否符合预期；开启 `has_thoughts=true` 查看上下文注入与推理链。  
- ✅ **迭代路径**：当效果不稳定时，优先走「反馈优化」流程（上传 5–10 条高质量样例 + ≥20 条评测集），而非反复手动改写；优化结果可一键保存为新模板。  
- ✅ **避坑提醒**：  
  - Prompt 中避免模糊表述（如“尽量准确”），改用可判定指令（如“答案必须来自以下三段文字之一”）；  
  - 变量名严格匹配 `${var}` 语法，且 `variables` 字段需为 JSON 数组（非对象）；  
  - 所有 Prompt 相关功能仅支持华北2（北京）地域，`workspaceId` 必须与该地域匹配。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application component api reference](../api/application-component-api-reference.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)


