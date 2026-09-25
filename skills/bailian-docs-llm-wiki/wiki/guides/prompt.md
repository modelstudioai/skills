# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于定义任务目标、上下文、约束条件与输出格式。通过结构化设计（如模板、样例库、自动优化等机制），开发者可实现 Prompt 的可复用、可管理、可迭代，从而提升模型输出的准确性、一致性与业务适配性。所有 Prompt 相关能力均仅在华北2（北京）地域可用。

## 支持的模型/功能

百炼平台提供多层次 [Prompt 工程](../concepts/prompt-engineering.md)支持能力，覆盖从基础指令构造到高级知识增强的全链路：

- **Prompt 模板**：支持预置与自定义两类模板，适用于文本生成、图片生成等场景。预置模板由阿里云提供并已优化，开箱即用；自定义模板支持通过控制台或 API 创建，可基于 [Prompt工程框架详解](raw/application-user-guide/prompt/prompt-custom-template.md)（如 ICIO、CRISPE、RASCEF）进行结构化构建 [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与结构一致的结果。但需注意：> **注意**：该功能[已停止维护](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)，官方明确推荐迁移至 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与边界注入，无需人工标注数据，适合快速提升基础 Prompt 质量 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：利用用户提供的输入-输出样例（至少 5~10 条）和评测数据（建议 ≥20 条），在推理模型（推荐千问-max）上多轮评估与反思，生成带 few-shot 示例与分类边界说明的高精度 Prompt，适用于强业务规则场景 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspaceId` | 业务空间 ID，所有 Prompt 操作（模板调用、样例库关联等）均需指定 | 必填；通过 [获取APP ID 和 Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 预置或自定义 Prompt 模板唯一标识符 | 必填；在控制台模板卡片或 API 响应中获取 |
| `variables` | 模板中声明的动态变量名列表（如 `["topic", "platform"]`） | 由 `GetPromptTemplate` 接口返回，不可自定义 |
| `has_thoughts=true` | API 调用时启用，返回 `thoughts` 字段含样例检索/知识召回详情 | 仅用于调试；见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| 召回片段数 | 应用配置中可调参数，默认 5，最大 10 | 影响 [Token](../concepts/token.md) 消耗与响应延迟；见 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |

## 使用方式

### 控制台操作
- **模板创建/管理**：访问 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，支持“自定义创建”或“基于Prompt工程创建”；图片生成模板需分别填写正向/负向 Prompt。
- **样例库迁移**：因样例库已停用，新项目请直接使用 RAG 表格库——在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 中选择“数据查询”类型，上传 Excel 文件（列名为 `query`/`answer`），并关闭 `answer` 字段的“参与检索”以复现原样例库行为 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **应用集成**：在智能体应用配置中，通过“表格”区域添加 RAG 表格库，或（历史项目）通过“样例库”开关关联（已弃用）。

### API/SDK 调用
- **模板调用**：调用 `GetPromptTemplate` 接口（需 `workspaceId` + `promptTemplateId`），解析响应中的 `content` 并填充变量后发送至目标模型。
- **应用调用**：启用知识增强时，在请求体中设置 `has_thoughts: true`，通过 `thoughts` 字段验证检索逻辑。
- **模板创建**：使用 `CreatePromptTemplate` 接口，需提前获取 `workspaceId`。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、优化）仅支持华北2（北京）地域，跨地域调用将失败。
- **容量限制**：
  - 单个 Prompt 模板内容最大 6144 字符（控制台编辑框显示计数）；
  - 单个样例库最多 300 条样例（但该功能已停用）；
  - RAG 表格库无数量上限，推荐按主题拆分知识表以提升检索精度。
- **兼容性注意**：
  > **注意**：文档中提及的 `GetPromptTemplate` 接口与直接拼接字符串的区别在于逻辑/内容分离、集中管理与一致性保障，但若业务需高频动态生成 Prompt（如每请求一变），模板机制可能引入额外 RTT 开销，此时应权衡是否采用纯代码内联方式 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **安全与计费**：
  - Prompt 自动优化功能免费，且用户数据**不用于模型训练**；
  - 启用样例库或 RAG 表格库会显著增加输入 [Token](../concepts/token.md)（样例内容 + 检索结果），直接影响模型调用费用；
  - RAG 表格库本身按小时计费（标准版/旗舰版）及向量/排序模型调用计费，需关注账户余额。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


