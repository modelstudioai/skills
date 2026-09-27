# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于定义任务目标、约束输出格式、注入领域知识及引导推理路径。通过模板化、样例增强、自动优化等机制，百炼支持从简单文本提示到复杂结构化工程的全生命周期管理，兼顾开发效率与效果可控性。所有功能均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供三类 Prompt 相关能力，覆盖不同抽象层级的需求：

- **Prompt 模板**：支持预置与自定义两类模板，适用于文本生成和图片生成场景。预置模板由阿里云提供并已优化，开箱即用；自定义模板支持通过控制台或 API 创建，可基于 [Prompt工程框架详解](raw/application-user-guide/prompt/prompt-custom-template.md)（如 ICIO、CRISPE、RASCEF）进行结构化设计 [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。  
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与结构一致性。但该功能**已停止维护**，官方明确推荐迁移到 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。  
- **Prompt 自动优化与反馈优化**：前者基于大模型重写原始 Prompt，提升指令清晰度与结构合理性；后者则结合用户提供的输入-输出样例（5–10 条）与评测数据（建议 ≥20 条），在千问-max 等推理模型上多轮评估迭代，生成更贴合业务场景的 Prompt [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 和文档 6 均指出 Prompt 样例库已下线，且迁移路径明确。若其他文档（如文档 1）仍描述其可用性，应以文档 3 和文档 6 的停用声明为准。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspaceId` | 业务空间 ID，所有 Prompt 操作必需 | 通过 [获取APP ID 和 Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 模板唯一标识符，用于 `GetPromptTemplate` 等接口 | 控制台模板卡片中直接复制；预置模板 ID 不可修改 |
| `variables` | 模板中定义的占位符列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可自定义命名规则 |
| `has_thoughts` | API 调用时启用调试信息开关 | `true` 时响应含 `thoughts` 字段，用于验证样例检索或 RAG 召回过程 |
| 召回片段数 | RAG 表格库/原样例库中注入上下文的样例数量 | 默认 5，最大 10（应用配置中可调） |

## 使用方式

### 控制台操作
- **模板创建**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 单击 **+ 创建提示词** → 选择“文本生成”或“图片生成”，再选“自定义创建”或“基于Prompt工程创建”。  
- **样例库迁移**：按 [Prompt 样例库迁移到 RAG 表格库](raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 文档执行四步流程（导出→建表→配置→发布）[原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。  
- **自动优化**：在提示词管理页右上角进入 **[自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize)**，粘贴原始 Prompt 后点击“优化”，支持一键保存为模板。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，响应中包含 `content`（模板字符串）与 `variables`（变量名数组）。  
- **应用集成**：在智能体应用配置中，关闭已弃用的“样例库”开关，改用“表格”区域添加 RAG 表格库，并通过 `has_thoughts=true` 调试召回逻辑。  
- **反馈优化任务**：通过 `CreatePromptFeedbackOptimizationTask`（非公开文档名，参见文档 5 流程）提交初始 Prompt、样例集与评测集，系统返回优化后 Prompt。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能仅支持华北2（北京）地域，跨地域调用将失败。  
- **容量限制**：  
  - 单个 RAG 表格库无条目上限（替代原样例库的 300 条硬限制）；  
  - 单次请求注入上下文的召回片段数上限为 10；  
  - 批量导入 Excel 文件 ≤ 20MB，单次最多 100 条（仅适用于历史样例库导入，新流程应使用 RAG 表格库）。  
- **安全与计费**：  
  - Prompt 自动优化不计费，且用户输入数据**不会用于模型训练**；  
  - 启用 RAG 或样例库会显著增加输入 [Token](../concepts/token.md) 消耗（计入模型调用费用），成本 ≈ 用户查询 [Token](../concepts/token.md) + 召回内容 [Token](../concepts/token.md) + 系统指令 Token；  
  - RAG 表格库按小时计费，含知识库运行、向量/排序模型调用费用，详情见 [知识库计费说明](raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。  
- **版本兼容性**：预置 Prompt 模板不支持修改；自定义模板副本命名规则为“原名_副本_时间戳”，避免 ID 冲突。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)


