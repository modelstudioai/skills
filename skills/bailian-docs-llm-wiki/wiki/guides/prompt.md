# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为单次调用的直接输入，也可通过模板化、样例增强、自动优化等方式进行工程化管理，从而提升输出质量、一致性与可维护性。所有 Prompt 相关功能均仅支持华北2（北京）地域。

## 支持的模型与功能

- **基础模型支持**：所有百炼托管的文本生成类大模型（如通义千问系列、Qwen-Max、Qwen-Plus 等）均原生支持 Prompt 输入；图片生成类模型（如 Wanx）支持正向/负向 Prompt 分离输入。
- **核心功能体系**：
  - **Prompt 模板**：支持预置模板（开箱即用，不可修改）和自定义模板（可编辑、可复用），覆盖文本生成、图片生成两大类型 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
  - **Prompt 样例库**：通过少样本（few-shot）方式注入高质量问答对，引导模型输出风格与结构一致的结果。> **注意**：该功能已停止维护，官方明确要求迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
  - **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强等重构，无需人工 [Prompt 工程](../concepts/prompt-engineering.md)经验 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - **Prompt 反馈优化**：利用用户提供的输入输出样例（query/answer 对）进行多轮评估与迭代优化，显著提升特定任务下的准确率，推荐使用 `qwen-max` 作为推理模型。

## 关键参数

| 参数名 | 说明 | 取值范围/约束 | 来源 |
|--------|------|----------------|------|
| `promptTemplateId` | 模板唯一标识符 | 字符串，由控制台或 API 创建时生成 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `workspaceId` | 业务空间 ID，用于鉴权与资源隔离 | 必填，需通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板中声明的占位符变量列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可手动指定 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts` | 控制是否在 API 响应中返回检索/思考过程详情 | `true` / `false`，调试时设为 `true` 可查看 `thoughts` 字段 | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| `recall_count` | RAG 表格库召回片段数（替代原样例库的“召回片段数”） | 默认 5，最大 10 | [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |

## 使用方式

### 1. 控制台操作
- **模板创建与管理**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，支持「自定义创建」或「基于 [Prompt 工程](../concepts/prompt-engineering.md)框架（ICIO/CRISPE/RASCEF）」创建文本生成模板，或分别配置正向/负向 Prompt 创建图片生成模板 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **自动优化**：在提示词管理页右上角进入 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面，粘贴原始 Prompt 即可一键生成优化版本。
- **反馈优化**：在提示词管理页选择「反馈优化」，上传初始 Prompt、样例数据（5–10 条，覆盖各类别）及评测数据（≥20 条），启动多轮自动化优化任务。

### 2. API 调用
- **模板调用流程**：  
  `CreatePromptTemplate` → `GetPromptTemplate`（获取 `variables`）→ 替换变量生成最终 Prompt → 发送给目标模型。
- **样例库/RAG 集成**：在智能体应用配置中启用知识库后，API 请求自动注入相关上下文；设置 `has_thoughts=true` 可调试检索逻辑。

### 3. SDK 示例
所有 Prompt 相关 API（如 `GetPromptTemplate`, `CreatePromptTemplate`）均提供 V2.0 SDK 示例，支持 Java/Python/Go 等主流语言，参数 `workspaceId` 和 `promptTemplateId` 可在调试页面自动填充并导出完整工程 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

## 限制和注意事项

- **地域限制**：全部 Prompt 功能（模板、优化、样例库）仅支持华北2（北京）地域，跨地域调用将失败。
- **容量限制**：
  - 单个自定义 Prompt 模板内容最大 6144 字符；
  - 单个 RAG 表格库无条目上限（原样例库上限为 300 条）；
  - 单个智能体应用最多关联 5 个 RAG 表格库。
- **功能弃用**：Prompt 样例库已下线，新项目禁止使用；存量用户须按 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 文档完成迁移，否则服务将不可用。
- **安全与计费**：
  - Prompt 自动优化不计费，且用户输入数据不会被用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；
  - 启用 RAG 表格库会增加 [Token](../concepts/token.md) 消耗（计入模型调用费用），并产生知识库运行时长、向量/排序模型调用等独立计费项。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


