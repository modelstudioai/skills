# Prompt 工程

Prompt 工程是系统化设计、验证与优化大语言模型输入指令（Prompt）的方法论与实践体系，其核心目标是通过结构化表达业务逻辑、领域知识和输出约束，显著提升模型响应的准确性、一致性与可控性，同时保障工程可维护性与迭代效率。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，Prompt 工程不是抽象理论，而是直接落地为三类可配置、可复用、可度量的生产级能力，全部聚焦于华北2（北京）地域：

- **Prompt 模板**：最常用载体。支持预置模板（开箱即用，已适配文生文、文生图等高频场景）与自定义模板（推荐基于 CRISPE、RASCEF 等框架构建）。模板中声明变量（如 `${topic}`），由开发者在调用时动态填充，实现“一次定义、多处复用”。图片生成需单独配置正向/负向 Prompt 字段。
  
- **Prompt 自动优化**：面向效果提效。开发者粘贴原始 Prompt 后，平台调用大模型自动重写，提升指令清晰度、消除歧义、增强结构合理性；支持一键保存为新模板，适用于快速迭代冷启动阶段的提示词。

- **Prompt 反馈优化（推荐替代旧样例库）**：面向任务定制。基于用户提供的高质量 query/answer 样例对 + 评测数据集，平台执行“评估→反思→重写→再评估”闭环，持续优化 Prompt 在特定业务指标（如准确率、格式合规率）上的表现。该能力已取代停用的 Prompt 样例库，与 RAG 表格库协同使用效果更佳。

> ⚠️ 注意：Prompt 样例库功能已正式下线，所有新项目必须使用 RAG 表格库替代。迁移路径为：导出历史样例 → 创建 RAG 表格库 → 上传结构化数据表 → 关联至应用并调试发布。

## 关键参数和配置

| 参数 | 说明 | 开发者操作建议 |
|------|------|----------------|
| `workspaceId` | 业务空间 ID，所有 Prompt 相关 API 的必需身份标识 | 控制台「应用」页或 API 文档中获取，务必校验地域（仅华北2有效） |
| `promptTemplateId` | 模板唯一 ID，用于 `GetPromptTemplate` 等接口 | 控制台模板卡片上直接复制，勿手动构造 |
| `variables` | 模板中声明的占位符列表（如 `["topic", "platform"]`） | **不可手动指定**；调用 `GetPromptTemplate` 后解析响应体获取，再按需填充内容 |
| `has_thoughts` | 调试开关，启用后响应中返回 `thoughts` 字段 | 生产环境设为 `false`；调试 RAG 召回或样例注入逻辑时设为 `true`，便于定位上下文拼接问题 |
| 最大召回数量（RAG 表格库） | 控制注入 Prompt 上下文的检索片段数 | 默认 5，上限 10；根据任务复杂度调整，但需权衡 [Token](token.md) 成本与效果增益 |

## 面向开发者，简洁实用

- ✅ **模板优先**：新项目一律从「预置模板」起步，再基于业务微调；避免从零手写模糊 Prompt。
- ✅ **变量填充要安全**：使用 `content.replace()` 填充变量时，务必对用户输入做基础转义（如去除控制字符），防止指令注入。
- ✅ **调试必开 `has_thoughts`**：线上效果异常时，第一排查项是检查 `thoughts` 字段——确认 RAG 是否召回了预期知识、样例是否被正确拼入。
- ✅ **警惕 [Token](token.md) 成本**：RAG 表格库内容会完整拼入 Prompt 上下文，单次调用 [Token](token.md) 消耗 = 模板长度 + 所有召回片段长度 + 用户输入。建议监控 `usage.input_tokens` 并设置告警。
- ✅ **不依赖样例库**：已停用功能不提供 SLA 保障，新代码禁止调用相关 API（如 `/v1/prompt/sample-library/*`），请使用 `/v1/knowledge/rag-table/*` 替代。

> 💡 提示：所有 Prompt 工程能力均不额外计费，但 RAG 表格库会触发 embedding 和 rerank 模型调用，产生独立费用。成本敏感场景建议结合显式缓存（`cache_key`）复用高频查询结果。

## 关联主题页

- [prompt](../guides/prompt.md)
- [start using](../guides/start-using.md)
- [use cases](../guides/use-cases.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


