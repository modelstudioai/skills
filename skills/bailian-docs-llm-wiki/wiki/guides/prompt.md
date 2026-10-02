# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为直接输入的文本字符串，也可通过结构化模板、样例库或自动优化工具进行工程化管理。合理设计与管理 Prompt 能显著提升模型输出的准确性、一致性与可控性，是构建高质量 LLM 应用的关键环节。

## 支持的模型/功能

百炼平台支持对多种模型（如通义千问系列）使用 Prompt，且提供分层能力以适配不同复杂度需求：

- **Prompt 模板**：支持预置与自定义两类模板，适用于文本生成、图片生成等场景。预置模板覆盖营销文案、摘要抽取、风格改写等通用任务；自定义模板支持基于 ICIO、CRISPE、RASCEF 等 [Prompt 工程](../concepts/prompt-engineering.md)框架创建，详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库（已停用）**：曾通过少样本（few-shot）方式注入问答对以约束输出风格与格式，但该功能**已停止维护**，官方明确推荐迁移至 RAG 表格库 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **Prompt 自动优化**：基于大模型重写原始 Prompt，增强指令清晰度、角色设定与边界约束，不计费，适用于快速迭代基础 Prompt [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：利用用户提供的输入-输出样例（5–10 条）和评测数据（≥20 条）驱动多轮评估与优化，效果优于纯自动优化，特别适合高精度分类、格式化生成等专业场景 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 5 明确声明“Prompt样例库功能已不再维护”，而文档 3 和文档 5 均指向同一迁移路径。因此，任何新项目均不应依赖样例库，应直接使用 RAG 表格库替代。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间 ID，调用 Prompt 相关 API（如 `GetPromptTemplate`）的必需参数 | 见 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `promptTemplateId` | 预置或自定义 Prompt 模板的唯一标识符，用于模板拉取与变量填充 | 在控制台模板卡片上直接获取 |
| `variables` | 模板中定义的占位符列表（如 `["topic", "platform"]`），需在运行时传入对应值 | 由 `GetPromptTemplate` 接口返回，见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) 示例响应 |
| `has_thoughts=true` | API 请求参数，启用后响应中将包含 `thoughts` 字段，用于调试 RAG 表格库或（历史）样例库的检索过程 | 文档 3 与文档 5 均要求此参数用于验证召回逻辑 |

## 使用方式

### 控制台操作
- **模板创建与管理**：在 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，选择“创建提示词”，指定类型（文本生成/图片生成）及输入模式（自定义创建或基于 [Prompt 工程](../concepts/prompt-engineering.md)框架）。
- **样例库迁移**：若原使用样例库，须按 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 流程导出数据、创建 RAG 表格库、更新智能体配置并发布。
- **反馈优化任务**：在 [提示词 → 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimize) 页面上传初始 Prompt、样例数据（5–10 条）与评测数据（≥20 条），启动优化。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析返回的 `content` 与 `variables` 后执行变量替换。
- **应用调用**：在智能体应用 API 请求中，若启用知识增强，需确保 `has_thoughts=true` 以获取调试信息；RAG 表格库配置通过应用后台完成，无需在请求体中重复传递样例。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（含预置与自定义）**仅支持华北2（北京）地域**，跨地域调用将失败 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **容量与性能**：
  - 单个 Prompt 模板内容最大支持 **6144 字符**（控制台编辑框右下角显示计数）。
  - RAG 表格库无条目数量上限；而已停用的样例库曾限制单库 ≤300 条、单应用最多关联 5 个库、单次召回 ≤10 片段。
- **安全与合规**：
  - Prompt 自动优化过程中的用户输入**不会被存储或用于模型训练**，符合数据隐私政策 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - 图片生成模板需谨慎设置负向 Prompt，避免触发内容安全策略（如禁止生成违法、违规或敏感图像）。
- **成本影响**：
  - 使用 RAG 表格库会产生知识库运行时长、向量/排序模型调用费用；样例库虽不单独计费，但会增加输入 [Token](../concepts/token.md) 消耗 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
  - Prompt 自动优化功能本身**不计费** [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


