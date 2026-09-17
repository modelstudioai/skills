# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，支持通过模板化、样例增强、自动优化等多种工程化手段进行结构化设计与持续迭代。其核心目标是将业务逻辑、领域知识和输出约束精准注入模型推理过程，在保障效果稳定性的同时提升开发效率与可维护性。所有 Prompt 相关功能当前仅适用于华北2（北京）地域。

## 支持的模型/功能

百炼平台提供三类 [Prompt 工程](../concepts/prompt-engineering.md)能力，覆盖从基础指令构造到专业场景适配的全链路需求：

- **Prompt 模板**：支持预置与自定义两类模板，适用于文本生成、图片生成等场景。预置模板由阿里云提供并已优化，开箱即用；自定义模板支持通过控制台或 API 创建，可基于 [Prompt工程框架详解](raw/application-user-guide/prompt/prompt-custom-template.md)（如 ICIO、CRISPE、RASCEF）进行结构化构建 [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与格式一致性。但需注意：> **注意**：该功能[已停止维护](raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方明确推荐迁移到 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 自动优化与反馈优化**：前者基于大模型重写原始 Prompt，提升指令清晰度与结构合理性；后者则结合用户提供的输入输出样例（query/answer 对）与评测数据集，进行多轮评估-反思-优化闭环，显著提升在特定任务上的准确率 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspaceId` | 业务空间 ID，调用 Prompt 相关 API 的必需参数 | 通过 [获取APP ID 和 Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 模板唯一标识符，用于 `GetPromptTemplate` 等接口 | 在控制台模板卡片上直接复制 |
| `variables` | 模板中声明的占位符列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可手动指定 |
| `has_thoughts` | API 调用时启用调试信息开关 | `true` / `false`；设为 `true` 时响应含 `thoughts` 字段，用于验证样例检索或 RAG 召回过程 |
| 召回片段数 | 应用配置中控制注入上下文的样例/RAG 片段数量 | 默认 5，最多 10（样例库）；RAG 表格库中可通过“最大召回数量”调整 |

## 使用方式

### 控制台操作
- **模板创建与管理**：访问 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，支持“自定义创建”或“基于Prompt工程创建”两种模式；图片生成模板需单独选择“图片生成”类型并分别填写正向/负向 Prompt。
- **样例库迁移**：因样例库已停用，新项目应直接使用 RAG 表格库。迁移路径为：导出旧样例 → 创建 RAG 表格库 → 上传数据表 → 关闭样例库开关并添加表格知识 → 调试发布。
- **自动优化**：在 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面粘贴原始 Prompt，点击“优化”后可直接复制或“保存为模板”。

### API/SDK 集成
- 模板调用：使用 `GetPromptTemplate` 接口（需 `workspaceId` + `promptTemplateId`），响应体包含 `content` 与 `variables`，开发者需自行完成变量填充（如 `content.replace('${topic}', 'AI')`）。
- 应用调用：在请求体中设置 `has_thoughts: true`，便于通过 `thoughts` 字段分析 RAG 或样例检索行为，辅助线上问题定位。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、自动优化）均仅支持华北2（北京）地域，跨地域调用将失败。
- **容量与配额**：
  - 单个 Prompt 模板内容最大 6144 字符；
  - 单个样例库最多 300 条样例（但该功能已废弃）；
  - 单个智能体应用最多关联 5 个知识源（RAG 表格库或旧样例库）；
  - RAG 表格库无条目上限，但单次召回受“最大召回数量”限制。
- **计费影响**：
  - Prompt 模板本身不额外计费；
  - 启用样例库或 RAG 表格库会显著增加输入 [Token](../concepts/token.md)（样例/RAG 内容被拼入上下文），直接影响模型调用费用；
  - RAG 表格库还产生向量模型（embedding）、排序模型（rerank）调用费用，按 [Token](../concepts/token.md) 用量计费。
- > **注意**：文档中关于样例库的使用说明（如“每个应用最多关联5个样例库”）虽技术上仍可配置，但因功能已下线，**不应作为新系统设计依据**；所有新项目必须采用 RAG 表格库替代方案 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


