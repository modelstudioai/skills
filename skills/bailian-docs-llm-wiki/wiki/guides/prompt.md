# prompt

阿里云百炼提供了一套完整的 Prompt 工程工具链，帮助开发者高效管理和优化提示词。核心能力包括 Prompt 模板（预置与自定义）、Prompt 自动优化、Prompt 样例库以及基于输入输出样例的 Prompt 反馈优化。这些功能覆盖了从模板创建、结构优化到少样本学习引导的完整流程，适用于文本生成、图片生成、智能客服等多种场景。

## Prompt 模板

Prompt 模板将提示词的固定结构与动态变量分离，实现可复用的统一管理。模板分为**预置模板**和**自定义模板**两类，详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

### 预置模板

由百炼平台提供，涵盖营销文案、摘要抽取、文案润色、商品评论等通用场景，已经过优化，效果稳定，无需额外开发即可通过控制台或 API 调用。预置模板不支持修改，但可通过"复制模板"创建自定义副本后编辑。

### 自定义模板

支持两种创建方式：

- **控制台创建**：在"提示词"页面直接创建，或从预置模板复制后修改。支持"自定义创建"和"基于 Prompt 工程创建"两种输入模式。
- **API 创建**：通过 `CreatePromptTemplate` 接口创建，需要提供 `workspaceId`（[业务空间](../concepts/workspace.md) ID）。

自定义模板支持文本生成和图片生成两种类型。文本生成模板可选择 ICIO、CRISPE、RASCEF 等 Prompt 工程框架进行结构化设计；图片生成模板支持分别定义正向和负向提示词。具体创建流程参见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。

### 模板使用方式

**控制台**：在模板卡片上点击"创建应用"，模板内容自动填充到[智能体应用](../concepts/agent-application.md)的提示词编辑框中。提示词最大支持 6144 个字符。

**API/SDK**：通过 `GetPromptTemplate` 接口拉取模板内容（需 `workspaceId` 和 `promptTemplateId`），将业务数据填入模板变量后生成最终 Prompt，再发送给目标模型。返回内容包含 `variables`（变量列表）、`content`（模板内容）等字段。

> **注意**：Prompt 模板功能目前仅适用于**华北2（北京）**地域。

## Prompt 自动优化

当手动编写高质量 Prompt 成本较高时，可使用自动优化功能。该功能利用大模型对原始 Prompt 进行分析和重写，优化策略包括：

- **结构重组**：调整整体结构使其更符合逻辑
- **角色扮演引导**：为模型设定明确的专家角色
- **指令增强**：将模糊指令具体化、步骤化
- **安全与边界注入**：增加输出格式、内容限制等边界条件

操作路径：**应用开发 > 组件管理 > 提示词 > 自动优化**。优化结果可直接复制使用或保存为模板。该功能**不[计费](../concepts/billing.md)**，且提交的数据不会被存储或用于模型训练。详见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## Prompt 反馈优化

相比普通自动优化，Prompt 反馈优化基于用户提供的**输入输出样例**进行多轮自动化评估和迭代，生成更贴合实际业务场景的 Prompt。其[工作流](../concepts/workflow.md)程为：

1. 选择推理模型（推荐千问-max）
2. 输入初始 Prompt（描述任务目标）
3. 上传样例数据（建议 5-10 条，每种场景至少 1 条）
4. 上传[评测](../concepts/evaluation.md)数据（建议至少 20 条，数据越多效果越好）
5. 系统自动进行多轮[评测](../concepts/evaluation.md)与优化

优化后的 Prompt 包含三部分：原始 Prompt、添加的样例（few-shot）、以及自动生成的内容提示（对分类边界等的补充说明）。优化结果可保存为模板或直接创建[智能体应用](../concepts/agent-application.md)。详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## Prompt 样例库

> **注意**：Prompt 样例库功能已不再维护，推荐将样例库数据迁移到 RAG 表格库中。

Prompt 样例库采用少样本学习（Few-shot learning）思路，从预定义的高质量问答对中检索相关样例注入模型上下文，引导模型生成更准确、风格更一致的回复。适用于智能客服、特定领域知识问答、格式化内容生成等场景。

### 使用限制

| 限制项 | 上限 |
|--------|------|
| 单个样例库容量 | 300 条样例 |
| 单应用关联样例库数 | 5 个 |
| 单次召回片段数 | 最多 10 个 |
| 批量导入文件大小 | 20MB（Excel） |
| 单次导入条数 | 100 条 |

### [计费](../concepts/billing.md)说明

样例库功能本身不收费，但启用后会增加大模型调用的 [Token](../concepts/token.md) 消耗。总输入 [Token](../concepts/token.md) 约等于：用户查询 [Token](../concepts/token.md) + 所有召回样例的总 [Token](../concepts/token.md) + 系统指令 [Token](../concepts/token.md)。

详见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## Prompt 工程框架

百炼平台内置三种 Prompt 工程框架，可在创建自定义文本生成模板时选用：

| 框架 | 组成要素 | 适用场景 |
|------|----------|----------|
| **ICIO** | 指令、背景信息、补充数据、输出格式 | 简单明确的任务，如数据分析、内容生成、文本摘要 |
| **CRISPE** | 角色与能力、背景信息、任务、输出风格、输出范围 | 需要 AI 扮演特定角色的交互，如客服、创意写作 |
| **RASCEF** | 角色、行动、步骤、上下文、示例、格式 | 多步骤复杂业务流程，如项目规划、战略分析 |

## 常见问题

**使用 `GetPromptTemplate` 接口和直接在代码中拼接字符串有什么区别？**

通过接口管理 Prompt 的优势在于：逻辑与内容分离（可在控制台更新 Prompt 无需重新部署代码）、集中管理与协作（团队共享和版本管理）、一致性保障（避免手动维护导致的不一致）。

**Prompt 自动优化失败的可能原因？**

输入内容超出 [Token](../concepts/token.md) 限制、触发安全审核策略、或网络/服务临时不可用。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
























