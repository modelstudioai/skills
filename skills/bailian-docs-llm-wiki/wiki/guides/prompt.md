# prompt

阿里云百炼平台提供了一套完整的 [Prompt 工程](../concepts/prompt-engineering.md)工具链，涵盖 Prompt 模板管理、自动优化、基于样例的反馈优化以及样例库引导等功能。开发者可以通过控制台或 API 创建、管理和优化 Prompt，提升大模型应用的输出质量和一致性。

## Prompt 模板

Prompt 模板将固定结构与动态变量分离，支持创建可复用的模板以统一管理和高效生成 Prompt。模板分为两类：

- **预置模板**：由百炼平台提供，覆盖营销文案、摘要抽取、文案润色等通用场景，已经过优化，效果稳定，可直接调用。
- **自定义模板**：开发者通过控制台或 API 自行创建，适用于金融风控、医疗咨询等特定业务场景，支持文本生成和图片生成两种类型。

模板的基本工作流程为：创建模板并获取模板 ID → 通过 API（`GetPromptTemplate`）拉取模板内容 → 将业务数据填入模板变量生成最终 Prompt → 发送给目标模型。使用 API 管理模板的核心优势在于**逻辑与内容分离**——更新 Prompt 无需修改应用代码。详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

### 自定义创建模板

创建文本生成模板时支持两种输入模式：

1. **自定义创建**：直接输入已有 Prompt，系统提供一键优化。
2. **基于 [Prompt 工程](../concepts/prompt-engineering.md)创建**：选择内置框架（ICIO、CRISPE、RASCEF）进行结构化设计，适合复杂任务。

其中三种框架的适用场景：

| 框架 | 适用场景 |
|------|----------|
| ICIO | 简单明确的任务执行（数据分析、内容生成、文本摘要） |
| CRISPE | 需要 AI 扮演特定角色的交互（客服、创意写作） |
| RASCEF | 涉及多步骤的复杂业务流程（项目规划、战略分析） |

图片生成模板支持分别定义正向和负向 Prompt 来控制画面内容与风格。详见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。

## Prompt 自动优化

百炼提供两种 Prompt 自动优化方式，帮助开发者在不具备丰富 [Prompt 工程](../concepts/prompt-engineering.md)经验时也能获得高质量的 Prompt。

### 基础自动优化

在控制台的**提示词 > 自动优化**页面提交原始 Prompt，系统通过大模型进行结构重组、角色扮演引导、指令增强和安全边界注入等策略自动重写。优化后的 Prompt 可直接复制或保存为模板。

关键信息：

- **免费**：Prompt 自动优化功能不计费。
- **数据安全**：提交的数据不会被存储或用于模型训练。
- 优化失败通常由输入过长、触发内容审核或网络问题导致。

详见 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

### 基于样例的反馈优化

当基础优化无法满足特定业务场景需求时，可使用反馈优化。该功能根据开发者提供的输入输出样例，通过多轮自动化评估、反思和优化，生成更贴合实际场景的 Prompt。

操作流程：

1. 选择推理模型（推荐千问-max）
2. 输入初始 Prompt
3. 上传样例数据（建议 5-10 条，每种场景至少 1 条）
4. 上传评测数据（建议至少 20 条）
5. 启动优化

优化结果包含三部分：原始 Prompt、基于样例的 few-shot 示例、以及系统总结的内容提示。优化后可保存为模板或直接创建智能体应用。详见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## Prompt 样例库（已停止维护）

> **注意**：Prompt 样例库功能已不再维护，推荐将样例库数据迁移到 RAG 表格库中。

样例库通过 Few-shot learning 思路，从预定义的高质量问答对中检索相关样例作为模型参考，引导其生成更准确、风格更一致的回复。适用于智能客服、特定领域知识问答和格式化内容生成等场景。

使用方式：创建样例库 → 在智能体应用中关联样例库（最多 5 个） → 配置召回片段数（默认 5，最多 10）→ 发布应用。

主要限制：

| 限制项 | 上限 |
|--------|------|
| 单个样例库容量 | 300 条样例 |
| 应用关联样例库数 | 5 个 |
| 单次召回片段数 | 10 个 |
| 批量导入文件大小 | 20 MB（Excel），单次 100 条 |

样例库本身不收费，但召回的样例会增加输入 Token 消耗。详见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

## 选择建议

| 场景 | 推荐工具 |
|------|----------|
| 快速优化已有 Prompt | Prompt 自动优化 |
| 特定业务场景精准优化 | 基于样例的反馈优化 |
| 团队共享、版本管理 Prompt | Prompt 模板（API 管理） |
| 复杂任务结构化设计 | 自定义模板 + Prompt 工程框架 |

> **注意**：自定义 Prompt 模板功能和 Prompt 样例库功能仅适用于中国大陆版（北京地域）。

## 来源文档

- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


