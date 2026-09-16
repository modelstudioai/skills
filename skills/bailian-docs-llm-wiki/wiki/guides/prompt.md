# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心机制，涵盖结构化模板、样例增强、自动优化及反馈式调优等多种能力。它支持开发者将业务逻辑与模型指令解耦，实现 Prompt 的集中管理、版本控制、团队协作与效果迭代。所有功能当前仅适用于华北2（北京）地域。

## 支持的模型/功能

百炼平台提供四类 Prompt 相关能力，面向不同场景需求：

- **Prompt 模板**：支持预置与自定义两类模板，覆盖文本生成、图片生成等任务类型。预置模板由阿里云提供并已优化，适用于通用场景（如营销文案、摘要抽取）；自定义模板支持通过控制台或 API 创建，适用于金融、医疗等强定制需求场景 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：通过少样本（few-shot）方式注入高质量问答对，引导模型输出风格与结构一致性。但该功能**已停止维护**，官方明确推荐迁移到 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与边界注入，提升清晰度与稳定性，**不计费且数据不用于训练** [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：利用用户提供的输入-输出样例（5–10 条）和评测数据（建议 ≥20 条），在推理模型（推荐千问-max）上多轮评估、反思并生成优化 Prompt，效果优于纯自动优化 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 和文档 6 明确指出 Prompt 样例库功能已下线，而文档 1 中仍将其列为可用功能之一。实际开发中应以文档 6 的迁移指引为准，**不得新建或依赖样例库**。

## 关键参数

| 参数 | 说明 | 取值范围/约束 | 来源 |
|------|------|----------------|------|
| `workspaceId` | 业务空间 ID，所有 Prompt 操作必需 | 由[获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)接口获取 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `promptTemplateId` | 模板唯一标识符，用于 GetPromptTemplate 等 API | 控制台模板卡片上直接复制；预置与自定义模板均适用 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板中声明的占位符列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可手动指定 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `recall_count` | RAG 表格库召回片段数（替代原样例库的“召回片段数”） | 默认 5，最大 10；需在应用配置中显式设置 | [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |
| `has_thoughts=true` | 启用调试模式，返回检索/思考过程详情 | 布尔值，仅限 API 调用时设置 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |

## 使用方式

### 控制台操作路径
- **模板管理**：`提示词` → `创建提示词`（支持文本/图片生成、自定义创建或基于 ICIO/CRISPE/RASCEF 框架创建）  
- **自动优化**：`提示词` → `自动优化` 页面粘贴原始 Prompt 并执行  
- **反馈优化**：`提示词` → `反馈优化` 页面上传样例与评测数据集  
- **RAG 表格库替代样例库**：`知识库` → 创建 `数据查询` 类型知识库 → 导入 Excel → 配置索引（建议关闭 `answer` 字段参与检索）→ 在智能体应用中启用  

### API 调用要点
- 获取模板：调用 `GetPromptTemplate`，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 字段后填充变量生成最终 Prompt。
- 使用模板：将填充后的 Prompt 作为 `system` 或 `user` 消息传入模型调用接口（如 `ChatCompletion`）。
- 启用 RAG：在智能体应用 API 请求中，确保 `knowledge_config.tables` 包含目标表格库 ID，并可选设 `has_thoughts=true` 查看召回详情。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库/RAG）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **模板长度**：控制台编辑器最大支持 6144 字符；API 无显式长度限制，但受模型上下文窗口约束。
- **样例库已弃用**：文档 3 明确声明“Prompt样例库功能已不再维护”，文档 6 提供完整迁移方案。继续使用将导致服务不可用或无法获得技术支持。
- **RAG 表格库配置差异**：迁移后需主动关闭 `answer` 字段的“参与检索”开关，否则可能降低匹配精度；默认相似度阈值 `0.20` 和最大召回数 `5` 可按需调整。
- **Token 成本影响**：启用 RAG 表格库或历史样例库会显著增加输入 Token（用户 query + 召回内容 + system prompt），需在成本与效果间权衡；计费项包含知识库运行时长、向量/排序模型调用（按 Token 计费）[Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **安全合规**：Prompt 自动优化过程中提交的数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)


