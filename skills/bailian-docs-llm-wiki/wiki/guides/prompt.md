# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心机制。它既可作为直接输入的文本指令，也可通过模板化、样例增强、自动优化等工程化手段进行系统性管理与迭代。合理设计和使用 Prompt 是保障模型输出质量、一致性与业务适配性的关键实践。

## 支持的模型/功能

百炼平台支持多种 Prompt 相关功能，覆盖从基础指令到高级工程化场景：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），适用于华北2（北京）地域 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。  
- **Prompt 样例库**：通过少样本学习注入高质量问答对，引导模型输出风格与结构一致的结果；但该功能**已停止维护**，官方明确推荐迁移到 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。  
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强等重写，不计费，且用户数据不会用于训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。  
- **Prompt 反馈优化**：利用用户提供的输入输出样例（5–10 条样例 + ≥20 条评测数据）驱动多轮评估与迭代，生成更贴合实际业务效果的 Prompt，推荐使用千问-max 作为推理模型 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。  

> **注意**：文档 2 明确声明“Prompt样例库功能已不再维护”，而文档 6 提供了完整的迁移路径；二者内容存在明确时效性冲突，开发者应以迁移方案为准，避免新建或依赖样例库。

## 关键参数

| 参数 | 说明 | 取值范围/约束 | 来源 |
|------|------|----------------|------|
| `workspaceId` | 业务空间 ID，调用 Prompt 相关 API 的必需参数 | 由[获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)接口获取 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `promptTemplateId` | 模板唯一标识符，用于 `GetPromptTemplate` 等接口 | 控制台模板卡片上直接复制；预置模板 ID 不可修改 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts` | 应用 API 调用参数，启用后响应中返回 `thoughts` 字段含检索/思考过程 | `true` / `false` | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 及 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |
| 召回片段数 | 样例库/RAG 表格库中单次请求注入上下文的样例数量 | 默认 5，最多 10（样例库）；RAG 表格库可通过“召回片段数”滑块调整 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |

## 使用方式

### 控制台操作
- **模板创建与使用**：在[提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)页面，选择“创建提示词”，按需配置文本生成（支持 ICIO/CRISPE/RASCEF 框架）或图片生成（正向/负向 Prompt）模板；创建后可直接“使用 prompt 创建应用”，变量（如 `${topic}`）将自动填充至智能体应用提示词区 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。  
- **自动优化**：进入[自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize)页面，粘贴原始 Prompt，点击“优化”后可复制或“保存为模板” [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。  
- **反馈优化**：在“提示词 > 反馈优化”页面，上传初始 Prompt、样例数据（5–10 条）和评测数据（≥20 条），启动多轮优化任务 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。  

### API/SDK 调用
- 获取模板：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，响应中包含 `variables` 数组与 `content` 字符串 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。  
- 应用调用：在智能体应用 API 请求中设置 `has_thoughts=true`，用于调试样例库或 RAG 表格库的检索行为 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。  

## 限制和注意事项

- **地域限制**：Prompt 模板与自定义模板功能仅限华北2（北京）地域，跨地域调用将失败 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)、[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。  
- **容量限制**：  
  - 单个 Prompt 模板内容最大 6144 字符（控制台编辑框右下角实时计数）；  
  - 单个样例库最多 300 条样例（已停用）；RAG 表格库无数量上限 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)、[Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。  
- **[Token](../concepts/token.md) 成本影响**：启用样例库或 RAG 表格库会显著增加输入 [Token](../concepts/token.md)（样例内容 + 用户查询），直接影响调用费用；成本预估公式为：`总输入 Token ≈ 用户查询 Token + 所有召回样例总 Token + 系统指令 Token` [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。  
- **安全与隐私**：Prompt 自动优化过程中提交的数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)


