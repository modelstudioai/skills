# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心机制。它既可作为直接输入的文本指令，也可通过模板化、样例增强、自动优化等工程化方式构建和管理，从而提升输出质量、一致性和开发效率。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供多种 [Prompt 工程](../concepts/prompt-engineering.md)能力，覆盖从基础指令到高级推理增强的全链路：

- **Prompt 模板**：支持预置与自定义两类模板，适用于文本生成、图片生成等场景。预置模板由阿里云提供并已优化，开箱即用；自定义模板支持基于 ICIO、CRISPE、RASCEF 等框架结构化创建，详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库（已停用）**：曾支持通过少样本问答对引导模型输出风格与结构，但该功能[已不再维护](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方明确推荐迁移至 RAG 表格库。
- **RAG 表格库**：替代样例库的增强型知识注入方案，支持无数量上限的数据表导入、可配置的检索策略（如相似度阈值、召回数）、多轮对话改写与重排，是当前推荐的知识增强方式。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，不计费且数据不用于训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入输出样例（5–10 条）与评测数据（≥20 条），在指定推理模型（推荐 `qwen-max`）上进行多轮评估与迭代优化，显著提升业务场景适配性 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 2 中描述的 Prompt 样例库功能已被废弃，其能力由 RAG 表格库全面覆盖；若文档中仍提及“样例库可用”，请以本文档及 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 为准。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspaceId` | 业务空间 ID，所有 Prompt 模板与样例库操作必需 | 通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 模板唯一标识符，用于 `GetPromptTemplate` 等 API 调用 | 控制台模板卡片上可见，长度为 32 位十六进制字符串 |
| `variables` | 模板中声明的动态变量名列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可在调用时新增 |
| `recall_count` | RAG 表格库召回片段数（原样例库“召回片段数”） | 默认 5，最大 10；在应用配置中可调 |
| `max_tokens`（图片生成） | 图片生成模板中正向/负向 Prompt 的总长度限制 | 单字段建议 ≤ 1024 字符，避免截断 |

## 使用方式

### 控制台操作
- **模板创建**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 点击 **+ 创建提示词** → 选择类型（文本/图片生成）与输入模式（自定义 / 基于 [Prompt 工程](../concepts/prompt-engineering.md)）→ 编辑并保存。
- **样例库迁移**：按 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 流程导出旧数据 → 创建 RAG 表格库 → 上传并配置索引 → 在智能体应用中替换知识源。
- **反馈优化**：进入 [提示词 → 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimize) → 上传样例与评测数据 → 选择推理模型 → 启动优化 → 保存结果为模板或直接创建应用。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 字段后填充变量生成最终 Prompt。
- **应用集成**：在智能体应用配置中启用 RAG 表格库后，调用应用 API 时无需额外参数；如需调试检索过程，设置请求体 `has_thoughts: true`，响应中 `thoughts` 字段将包含召回详情。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板、自定义 Prompt、自动优化等功能**仅支持华北2（北京）地域**，跨地域调用将失败。
- **模板容量**：单个 Prompt 模板内容（`content` 字段）最大支持 6144 字符（控制台编辑框右下角实时计数）。
- **RAG 表格库限制**：
  - 单次上传 Excel 文件 ≤ 20 MB，单表行数无硬性上限，但建议单表 ≤ 10 万行以保障检索性能；
  - 向量/排序模型调用按 Token 计费，需关注 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。
- **安全与合规**：
  - 用户提交至自动优化、反馈优化功能的 Prompt 与样例数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策；
  - 所有 Prompt 内容须遵守内容安全规范，触发审核策略将导致优化失败或 API 返回 400 错误。
- **版本兼容性**：预置 Prompt 模板不支持修改；自定义模板修改后需重新发布应用才能生效，历史版本无自动回滚机制。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


