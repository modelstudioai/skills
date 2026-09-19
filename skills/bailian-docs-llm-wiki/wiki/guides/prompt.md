# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心机制。它既可作为直接输入的文本指令，也可通过模板化、样例增强、自动优化等方式进行工程化管理，以提升输出的一致性、准确性与业务适配性。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台支持对多种模型应用 Prompt 策略，包括通义千问系列（如 `qwen-plus-latest-128k`）、千问-max 等文本生成模型，以及支持图片生成的[多模态](../concepts/multimodal.md)模型（需使用图片生成类 Prompt 模板）。核心 Prompt 功能包括：

- **Prompt 模板**：提供预置与自定义两类模板，支持变量插值（如 `${topic}`）和结构化填充，适用于营销文案、摘要抽取、风格改写等通用及垂直场景 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：通过少样本（few-shot）方式注入高质量问答对，引导模型复现特定解释结构或输出风格。> **注意**：该功能已停止维护，官方明确推荐迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定与指令增强，适用于快速提升模糊指令的效果 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：利用用户提供的输入-输出样例（5–10 条）和评测数据（≥20 条）进行多轮评估与迭代，生成更贴合实际业务效果的 Prompt，尤其适合分类、结构化输出等任务 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 取值/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 操作必需 | 通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 模板唯一标识符，用于 API 调用 | 在控制台模板卡片上直接复制；预置与自定义模板均有效 |
| `variables` | 模板中声明的变量名列表（如 `["platform", "topic"]`） | 由 `GetPromptTemplate` 接口返回，必须严格匹配填入 |
| `has_thoughts=true` | 启用样例库/RAG 检索过程日志输出 | 仅限 API 调用时设置，响应中 `thoughts` 字段包含召回详情 |
| `recall_count` | 应用配置中可调的召回片段数 | 默认 5，上限 10（样例库）；RAG 表格库中对应“最大召回数量” |

## 使用方式

### 控制台操作
- **模板使用**：在 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面创建/选择模板 → 单击 **使用prompt创建应用**，变量将自动填充至智能体应用提示词框；调试时右侧输入问题即可测试。
- **样例库（历史）**：在 [样例库](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt-case) 创建后，于智能体应用配置中开启 **样例库** 开关并关联，最多 5 个库（多路召回）。
- **RAG 表格库（当前推荐）**：迁移后，在智能体应用的 **知识** 配置面板 → **表格** 区域添加，可调相似度阈值、权重及拼装策略 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **自动优化**：进入 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面，粘贴原始 Prompt → 单击 **优化** → 可直接复制或 **保存为模板**。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 后执行变量替换。
- **调用应用**：在 `InvokeApplication` 请求体中，若启用 RAG 表格库，无需额外参数；若需调试检索过程，设置 `"has_thoughts": true`。
- **创建模板**：使用 `CreatePromptTemplate` 接口，`content` 字段支持 ICIO/CRISPE/RASCEF 等框架结构化输入（详见 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)）。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、优化）仅支持华北2（北京）地域，跨地域调用将失败。
- **模板长度**：控制台提示词编辑框最大支持 6144 字符；API 层面受模型上下文窗口限制（如 qwen-plus-128k 为 131072 tokens），但模板内容本身不计入模型 token 限额。
- **样例库弃用**：`Prompt样例库` 功能已下线，新项目严禁使用；存量应用须按 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 文档完成迁移，否则将无法保障服务稳定性。
- **安全与隐私**：Prompt 自动优化功能不存储用户输入数据，亦不用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；但反馈优化与 RAG 表格库涉及的数据上传，需确保符合企业数据合规要求。
- **计费影响**：启用样例库或 RAG 表格库会显著增加输入 token（因注入样例或检索结果），直接影响模型调用费用；RAG 表格库另产生向量/排序模型调用费与知识库运行时长费 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


