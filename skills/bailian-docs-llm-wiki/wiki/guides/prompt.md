# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心输入，用于明确任务目标、设定角色、提供上下文及约束输出格式。通过模板化、样例增强与自动优化等机制，开发者可系统性地管理 Prompt 的设计、复用与迭代，提升模型输出的准确性、一致性与可控性。该能力深度集成于控制台与 OpenAPI，支持文本生成、图片生成及智能体应用等多种场景。

## 支持的模型/功能

- **模板化支持**：提供预置 Prompt 模板（如营销文案生成、摘要抽取、文案润色）和自定义 Prompt 模板两类，均通过统一的 `promptTemplateId` 管理，适用于通义千问系列（Qwen-Plus-La[test 1](test-1.md)28K 等）、Qwen-VL 等支持文本/多模态输入的模型 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **图片生成专用模板**：支持正向/负向 Prompt 分离配置，适配 Stable Diffusion、Qwen-VL 等图像生成模型，需在创建时显式选择“图片生成”类型 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **样例增强（已下线）**：原 Prompt 样例库功能基于少样本学习注入问答对，但**自 2024 年起已停止维护，控制台入口下线**；官方推荐迁移至 RAG 表格库实现更灵活的知识增强 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **自动优化**：调用专用大模型对原始 Prompt 进行结构重组、角色注入与指令强化，输出可直接使用的优化版本，不产生额外计费 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

> **注意**：文档 3 明确指出“Prompt样例库功能已不再维护”，而文档 5 进一步说明其控制台入口已下线且数据导出功能不可用。因此，任何依赖样例库实时检索的线上应用必须完成向 RAG 表格库的迁移，否则将无法继续使用该能力。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 操作必需 | 通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 模板唯一 ID，区分预置（`type=System`）与自定义模板 | 预置模板 ID 通过 `ListPromptTemplates`（`type=System`）获取；自定义模板 ID 在控制台卡片或 `CreatePromptTemplate` 响应中返回 |
| `variables` | 模板中声明的占位符列表（如 `["platform", "topic"]`），用于运行时填充 | 由 `GetPromptTemplate` 接口返回，不可在调用模型时动态增删 |
| `has_thoughts=true` | 启用调试模式，返回 `thoughts` 字段含样例检索或 RAG 召回详情 | 仅适用于智能体应用 API 调用，非 Prompt 模板接口参数 |

## 使用方式

### 控制台操作
- **创建模板**：进入 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage)，点击“创建提示词”，选择“文本生成”或“图片生成”，并指定输入模式（自定义创建 / 基于 [Prompt 工程](../concepts/prompt-engineering.md)框架如 ICIO、CRISPE）[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **复用预置模板**：在预置模板卡片点击“··· → 复制到自定义模板”，获得可编辑副本，避免修改原模板 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **自动优化**：在提示词管理页切换至“自动优化”分类，粘贴原始 Prompt（≤10000 字符），点击“优化”后可复制或“保存为模板” [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

### API 调用
1. **获取模板内容**：调用 `GetPromptTemplate`，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables`；
2. **填充变量**：将业务数据代入 `${variable}` 占位符，生成最终 Prompt 字符串；
3. **调用模型**：将生成的 Prompt 作为 `system` 或 `user` 消息传入 `ChatCompletion` 接口（如 `qwen-plus`）；
4. **（智能体应用）启用知识增强**：迁移后，在应用配置中关闭样例库开关，改用 RAG 表格库，并通过 `has_thoughts=true` 验证召回效果 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（创建、管理、调用）**仅支持华北2（北京）地域**，跨地域 workspaceId 不可用 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **字符限制**：控制台 Prompt 输入框最大支持 6144 字符；API 层级以模型自身 token 限制为准（如 Qwen-Plus 支持 128K tokens），但模板内容过长可能导致 `GetPromptTemplate` 响应截断。
- **模板不可变性**：预置 Prompt 模板**不支持修改或删除**；自定义模板可编辑，但修改后需重新发布应用才能生效。
- **安全与隐私**：Prompt 自动优化过程不存储用户输入，**不会用于模型训练**，符合阿里云数据隐私政策 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **迁移强制要求**：因样例库已下线，所有依赖该功能的应用必须迁移至 RAG 表格库；RAG 表格库无单库 300 条样例上限，且支持召回策略配置（相似度阈值、最大召回数等），但会产生向量/排序模型调用费用 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)


