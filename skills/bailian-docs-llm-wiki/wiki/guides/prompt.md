# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心机制。它既可作为直接输入的文本指令，也可通过结构化模板、样例库或自动优化工具进行工程化管理。合理设计和使用 Prompt 能显著提升模型在特定任务（如分类、文案生成、术语解释）中的准确性、一致性与可控性，是构建稳定、可维护 LLM 应用的关键环节。

## 支持的模型与功能

- **模型支持**：所有百炼托管的文本生成类大模型（如通义千问系列 Qwen-Plus、Qwen-Max 等）均原生支持 Prompt 输入；图片生成类模型（如万相）支持正向/负向 Prompt 分离输入。
- **核心功能**：
  - **Prompt 模板**：支持预置与自定义两类模板，实现逻辑与内容分离，适用于营销文案、摘要抽取、风格改写等通用及垂直场景 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
  - **Prompt 样例库**：基于少样本学习（Few-shot），通过用户提供的高质量问答对引导模型输出，适用于术语解释、客服应答等需强格式/风格约束的场景。> **注意**：该功能已停止维护，官方明确推荐迁移到 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
  - **Prompt 自动优化**：利用大模型对原始 Prompt 进行结构重组、角色注入与指令增强，适用于快速提升模糊 Prompt 的效果稳定性 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - **Prompt 反馈优化**：基于用户提供的输入输出样例（query/answer 对）与评测数据集，通过多轮评估与反思生成高适配性 Prompt，特别适合分类、结构化输出等任务 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 取值范围/约束 | 来源 |
|------|------|----------------|------|
| `promptTemplateId` | 模板唯一标识符 | 字符串，由控制台或 API 创建时生成 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `workspaceId` | 业务空间 ID，用于权限与资源隔离 | 必填，需通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板中声明的占位符变量名列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可手动指定 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts` | 控制是否在 API 响应中返回检索/推理过程详情（如样例召回、RAG 思考链） | `true` / `false`，调试时设为 `true` | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| `recall_count` | RAG 表格库召回片段数（替代旧样例库的“召回片段数”） | 默认 5，最大 10 | [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |

## 使用方式

### 1. 控制台操作
- **模板创建与管理**：访问 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，支持“自定义创建”或“基于Prompt工程创建”（ICIO/CRISPE/RASCEF 框架）[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **样例库迁移**：若仍在使用旧样例库，必须按 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 文档完成迁移，否则功能将失效。
- **自动优化入口**：在提示词管理页右上角点击 **[自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize)**，粘贴原始 Prompt 即可一键生成优化版本。

### 2. API 调用
- **模板调用流程**：  
  `CreatePromptTemplate` → `GetPromptTemplate`（获取 `variables`）→ 替换变量生成最终 Prompt → 发送给目标模型（如 `ChatCompletion` 接口）。  
  完整示例见 [GetPromptTemplate - 获取Prompt模板](../../raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md)。
- **RAG 表格库集成**：在智能体应用配置中启用“表格”知识源，无需修改 Prompt 内容，系统自动注入检索结果。

### 3. SDK 集成
- 所有 Prompt 相关 API（`CreatePromptTemplate`, `GetPromptTemplate`, `OptimizePrompt`）均提供 V2.0 SDK 示例（Java/Python/Go 等），参数自动填充，可直接运行调试 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 限制与注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、自动优化）当前仅支持 **华北2（北京）** 地域，跨地域调用将失败。
- **容量限制**：
  - 单个 Prompt 模板内容最大 6144 字符（控制台编辑框显示计数）。
  - RAG 表格库无单库条目上限；旧样例库已停用，其 300 条/库限制不再适用。
- **功能弃用**：`Prompt 样例库` 功能已下线，新项目严禁使用，存量项目须按 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 迁移，否则应用将无法获得样例增强能力。
- **安全与隐私**：Prompt 自动优化服务不存储用户输入数据，且不用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **计费影响**：启用 RAG 表格库会增加 [Token](../concepts/token.md) 消耗（检索内容注入上下文），并产生向量/排序模型调用费用，需关注 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


