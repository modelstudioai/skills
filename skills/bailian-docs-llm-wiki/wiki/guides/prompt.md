# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为简单文本直接调用模型，也可通过模板化、样例增强、自动优化等机制实现结构化、可复用、可迭代的工程化管理。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型与功能

百炼平台支持对多种通义系列模型（如 `qwen-plus-latest-128k`、`qwen-max` 等）应用 Prompt，覆盖文本生成、代码生成、知识问答、对话交互等场景。核心 Prompt 功能包括：

- **Prompt 模板**：支持预置与自定义两类模板，实现固定结构与动态变量（如 `${topic}`）分离，便于集中管理与跨应用复用 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)；
- **Prompt 样例库**：通过少样本（few-shot）方式注入高质量问答对，引导模型输出风格与格式一致的结果（*注意：该功能已停止维护*）；
- **RAG 表格库替代方案**：Prompt 样例库功能已被 RAG 表格库全面取代，后者提供无数量上限、可配置召回策略、支持多轮改写与重排的增强能力 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)；
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，提升效果稳定性 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；
- **Prompt 反馈优化**：基于用户提供的输入输出样例（query/answer 对）和评测数据集，通过多轮评估与反思生成高适配性 Prompt，适用于分类、结构化输出等强约束任务。

> **注意**：文档 3 中描述的 Prompt 样例库功能已明确标注“不再维护”，且文档 4 明确要求迁移至 RAG 表格库。开发者应避免新建样例库，现有应用须按文档 4 完成迁移。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 操作（模板获取、样例库关联、RAG 知识库绑定）均需指定 | [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `promptTemplateId` | 预置或自定义 Prompt 模板唯一标识符，用于 `GetPromptTemplate` 接口调用 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板中声明的占位符列表（如 `["platform", "topic"]`），调用时需传入对应值 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 的 API 响应示例 |
| `has_thoughts=true` | API 调用时启用该参数，可在响应 `thoughts` 字段中查看样例检索或 RAG 召回的详细过程 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 与 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |
| `recall_count`（RAG） | RAG 表格库配置项，控制单次请求最大召回片段数（默认 5，上限 10） | [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |

## 使用方式

### 控制台操作
- **模板创建与管理**：访问 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，支持「自定义创建」或「基于Prompt工程创建」（ICIO/CRISPE/RASCEF 框架）；图片生成模板需分别配置正向/负向 Prompt [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)；
- **自动优化**：在提示词管理页右上角进入「自动优化」页面，粘贴原始 Prompt 即可生成优化版本，并支持一键保存为模板 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；
- **反馈优化**：在「提示词 → 反馈优化」页面，上传初始 Prompt、样例数据（5–10 条，覆盖各类别）及评测数据（≥20 条），启动多轮自动化优化 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)；
- **RAG 表格库集成**：在智能体应用配置中关闭旧样例库开关，于「知识 → 表格」区域添加新创建的 RAG 表格库，并可调试召回效果 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

### API/SDK 调用
- 获取模板：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析返回的 `content` 并填充 `variables`；
- 创建模板：调用 `CreatePromptTemplate` 接口，需指定 `name`、`type`（`text_generation` 或 `image_generation`）、`content`（或 `positive_prompt`/`negative_prompt`）等字段；
- 应用调用：在 `InvokeApplication` 请求中，若已配置 RAG 表格库，无需额外参数即可触发知识增强；如需调试召回细节，设置 `has_thoughts=true`。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库、RAG）仅支持华北2（北京）地域；
- **模板长度**：控制台提示词编辑框最大支持 6144 字符 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)；
- **样例库容量**：单个样例库最多 300 条样例（*但该功能已停用，仅作历史参考*）；
- **RAG 表格库限制**：单次召回最大 10 片段；向量/排序模型调用按 Token 计费，详见[知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)；
- **数据安全**：Prompt 自动优化过程中提交的数据不会被存储或用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；
- **模型选择建议**：Prompt 反馈优化推荐使用 `qwen-max` 作为推理模型，以获得更可靠的多轮评估效果 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


