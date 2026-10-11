# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心机制。它既可作为直接输入的文本指令，也可通过结构化模板、样例库或自动优化工具进行工程化管理。合理设计和使用 Prompt 能显著提升模型输出的准确性、一致性与可控性，是构建高质量 LLM 应用的关键实践。

## 支持的模型与功能

百炼平台支持在多种模型上使用 Prompt，包括通义千问系列（如 `qwen-plus-latest-128k`）、`qwen-max` 等主流文本模型，以及图像生成类模型（如 `wanx` 系列）。对应功能覆盖三类核心能力：

- **Prompt 模板**：提供预置与自定义两类模板，支持文本生成与图片生成场景。预置模板开箱即用，适用于通用文案、摘要、润色等任务；自定义模板支持基于 [ICIO、CRISPE、RASCEF](raw/application-user-guide/prompt/prompt-custom-template.md) 等 [Prompt 工程](../concepts/prompt-engineering.md)框架创建，适用于复杂业务逻辑（如多步骤策略生成、角色扮演对话）[原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与结构一致的结果。但需注意：> **注意**：该功能已停止维护，官方明确推荐迁移到 RAG 表格库，详见 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，无需人工 [Prompt 工程](../concepts/prompt-engineering.md)经验即可获得更稳定版本 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。进阶版「Prompt 反馈优化」则进一步结合用户提供的输入输出样例与评测数据集，在推理模型（如 `qwen-max`）上多轮评估迭代，生成高度适配实际业务场景的 Prompt [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

使用 Prompt 相关功能时，以下参数需重点关注：

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 模板、样例库、RAG 知识库均需归属指定 workspace。获取方式见 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) | 必填，API 调用必需 |
| `promptTemplateId` | 模板唯一标识符，控制台模板卡片右下角可复制。区分预置模板（系统分配）与自定义模板（用户创建） | 必填（模板调用场景） |
| `variables` | 模板变量列表（如 `["platform", "topic"]`），由 `GetPromptTemplate` 接口返回，用于运行时填充 | 仅模板生效时存在 |
| `has_thoughts=true` | API 调用时启用，使响应中包含 `thoughts` 字段，用于调试样例库/RAG 检索过程 | 仅调试验证阶段建议开启 |
| `recall_count` / `max_retrieval_count` | 样例库或 RAG 表格库召回片段数，默认 5，上限 10 | 控制上下文长度与 Token 成本平衡 |

## 使用方式

### 1. 控制台操作
- **模板**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，通过「创建提示词」选择「自定义创建」或「基于Prompt工程创建」；预置模板在 [提示词市场](https://bailian.console.aliyun.com/?tab=app#/plugin-market/prompt) 查看并一键复制或创建应用。
- **样例库（已弃用）**：访问 [样例库](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt-case)，手动输入或 Excel 批量导入（≤100 条/次，单库 ≤300 条）。
- **反馈优化**：在 [提示词 → 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimize) 页面上传初始 Prompt、样例数据（5–10 条）与评测数据（≥20 条），启动优化任务。

### 2. API 调用
- **模板管理**：调用 `CreatePromptTemplate`、`GetPromptTemplate`、`UpdatePromptTemplate` 等接口，需传入 `workspaceId` 与 `promptTemplateId`。
- **应用集成**：在智能体应用配置中启用「样例库」或「表格」知识源；调用应用 API 时，若需调试检索过程，设置 `has_thoughts=true`。
- **自动优化**：无独立 API，但可通过 `GetPromptTemplate` 获取优化后模板内容后，再用于下游模型调用。

### 3. SDK 集成
所有模板与样例库相关 API 均提供 Java/Python/Go 等语言 SDK 示例，可在 OpenAPI 调试页面选择「SDK示例」页签直接生成代码，自动填充 `workspaceId` 等参数 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能当前**仅支持华北2（北京）地域**，跨地域调用将失败。
- **模板字符限制**：控制台编辑 Prompt 模板时，输入框最大支持 **6144 个字符**；超出需精简或拆分逻辑。
- **样例库已停服**：> **注意**：Prompt 样例库功能自文档发布日起已停止维护，新项目请直接使用 RAG 表格库替代；存量应用须按 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 文档完成迁移，否则后续可能无法正常调用。
- **Token 成本影响**：启用样例库或 RAG 表格库会显著增加输入 Token（用户查询 + 召回样例/知识片段），直接影响计费。成本预估公式为：`总输入 Token ≈ 用户查询 Token + 所有召回内容 Token + 系统指令 Token`。
- **数据安全**：Prompt 自动优化功能**不存储、不训练、不共享**用户提交的原始 Prompt 数据，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


