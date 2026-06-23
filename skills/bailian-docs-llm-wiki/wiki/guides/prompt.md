# prompt

阿里云百炼平台提供了一套完整的 Prompt 管理与优化工具链，帮助开发者高效创建、管理和优化提示词。通过 Prompt 模板实现结构化复用，通过样例库引导模型输出风格，通过自动优化和反馈优化持续提升 Prompt 质量。

## 核心功能

百炼平台围绕 Prompt 提供四项核心能力：

| 功能 | 说明 | 适用场景 |
| --- | --- | --- |
| Prompt 模板 | 将固定结构与动态变量分离，创建可复用模板 | 统一管理、团队协作、跨应用复用 |
| Prompt 样例库 | 通过 Few-shot 样例引导模型输出 | 智能客服、领域问答、格式化内容生成 |
| Prompt 自动优化 | 大模型自动重构 Prompt，提升结构和清晰度 | 快速优化手写 Prompt |
| Prompt 反馈优化 | 基于输入输出样例的多轮自动评估优化 | 分类、提取等需精准匹配期望输出的任务 |

> **注意**：Prompt 样例库功能已不再维护，推荐将样例库数据迁移到 RAG 表格库中。详见[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## Prompt 模板

### 模板类型

百炼提供两类模板：

- **预置 Prompt 模板**：由阿里云百炼提供，涵盖营销文案、摘要抽取、文案润色等通用场景，效果已优化，开箱即用，不支持修改。
- **自定义 Prompt 模板**：用户通过控制台或 API 自行创建，适用于复杂业务需求（如金融风控、医疗咨询）或对输出格式有严格要求的场景。

### 创建自定义模板

自定义模板支持**文本生成**和**图片生成**两种类型。

**文本生成模板**有两种输入模式：

1. **自定义创建**：直接输入已有 Prompt，系统可自动优化。适合已有现成 Prompt 的情况。
2. **基于 [Prompt 工程](../concepts/prompt-engineering.md)创建**：选择框架（ICIO / CRISPE / RASCEF）进行结构化设计，适合构建高质量复杂任务的 Prompt。详见[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。

**图片生成模板**支持分别定义正向 Prompt（应包含内容）和负向 Prompt（应排除内容），精确控制生成画面。

### 使用方式

模板可通过以下方式使用：

- **控制台**：单击"创建应用"，模板内容自动填充到智能体应用的提示词编辑框中。
- **API**：通过 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId` 获取模板内容，再将业务数据填入模板变量生成最终 Prompt。
- **SDK**：支持 Java、Python 等语言，可在线运行示例或下载完整工程。

使用 API 管理 Prompt 的优势在于：逻辑与内容分离（无需重部署即可更新 Prompt）、集中管理便于团队协作、跨服务版本一致性保障。详见[Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

## Prompt 优化

### 自动优化

Prompt 自动优化通过大模型对原始 Prompt 进行分析和重写，优化策略包括：

- **结构重组**：调整整体结构使其更符合逻辑
- **角色扮演引导**：为模型设定明确的专家角色
- **指令增强**：将模糊指令具体化、步骤化
- **安全与边界注入**：增加输出格式、内容限制等边界条件

该功能**不计费**，且用户数据不会被存储或用于模型训练。详见[Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

### 反馈优化

相比自动优化仅重构 Prompt 文本，反馈优化引入了用户提供的**样例数据**和**评测数据**作为优化标准，通过多轮自动化评估、反思和优化生成更精准的 Prompt。

操作流程：

1. 选择推理模型（推荐千问-max）
2. 输入初始 Prompt
3. 上传样例数据（建议 5~10 条，每种场景至少 1 条）
4. 上传评测数据（建议至少 20 条，越多效果越好）
5. 启动优化

优化后可保存为模板或直接创建智能体应用。详见[基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## [Prompt 工程](../concepts/prompt-engineering.md)框架

百炼内置三种 [Prompt 工程](../concepts/prompt-engineering.md)框架，适用于不同复杂度的任务：

| 框架 | 组成要素 | 适用场景 |
| --- | --- | --- |
| **ICIO** | 指令 + 背景信息 + 补充数据 + 输出格式 | 简单明确的任务（数据分析、内容生成、文本摘要） |
| **CRISPE** | 角色与能力 + 背景信息 + 任务 + 输出风格 + 输出范围 | 需要 AI 扮演特定角色的交互（客服、创意写作） |
| **RASCEF** | 角色 + 行动 + 步骤 + 上下文 + 示例 + 格式 | 多步骤复杂业务流程（项目规划、战略分析） |

## 使用限制

- Prompt 模板变量最大支持 6144 个字符
- 样例库每库最多 300 条样例，每个应用最多关联 5 个样例库
- 单次请求最多召回 10 个样例片段
- 批量导入支持 20MB 以内的 Excel 文件，单次最多 100 条
- 样例库启用会增加输入 Token 消耗（总输入 Token ≈ 用户查询 + 召回样例 + 系统指令）
- 本文档仅适用于中国大陆版（北京地域）

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)




