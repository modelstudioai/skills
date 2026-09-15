# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于定义任务目标、约束输出格式、注入领域知识及引导推理路径。通过结构化模板、样例库、自动优化等能力，开发者可实现 Prompt 的工程化管理与持续迭代，显著提升模型输出的准确性、一致性与业务适配性。所有 Prompt 相关功能当前仅支持华北2（北京）地域。

## 支持的模型/功能

百炼平台提供三类 Prompt 增强能力，面向不同阶段的开发需求：

- **Prompt 模板**：支持预置与自定义两类模板，适用于文本生成、图片生成等场景。预置模板覆盖营销文案、摘要抽取、风格改写等通用任务；自定义模板支持基于 ICIO、CRISPE、RASCEF 等 Prompt 工程框架构建，详见 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：通过少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与结构一致的结果。但需注意：> **注意**：该功能已停止维护，官方明确推荐迁移到 RAG 表格库，详见 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **Prompt 自动优化**：分为两类：
  - *基础版*：基于单条原始 Prompt，由大模型进行结构重组、角色设定与指令增强，不依赖用户数据；
  - *反馈优化版*：基于用户提供的输入输出样例（5–10 条）和评测数据（≥20 条），在推理模型（推荐千问-max）上多轮评估迭代，生成高保真 Prompt。该能力在 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md) 中有详细说明。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspaceId` | 业务空间 ID，所有 Prompt 操作必需 | 通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 模板唯一标识符，用于 GetPromptTemplate 等 API | 控制台模板卡片或 API 响应中直接获取 |
| `variables` | 模板变量列表（如 `["topic", "platform"]`），用于运行时填充 | 由 `GetPromptTemplate` 接口返回，不可手动指定 |
| `has_thoughts` | API 调用参数，启用后响应中返回 `thoughts` 字段，含样例检索或 RAG 召回详情 | `true` / `false`，仅对智能体应用 API 有效 |
| `recall_count` | RAG 表格库召回片段数（非样例库） | 默认 5，最大 10（控制台可配置） |

> **注意**：文档 3 中提及的样例库“召回片段数”默认为 5、最多 10，但该参数在已停用的样例库中不可调；而迁移后的 RAG 表格库中对应参数名为 `recall_count`，且支持显式配置，二者逻辑一致但归属系统不同。

## 使用方式

### 控制台操作
- **模板创建**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面，选择“创建提示词”，按向导配置类型（文本/图片）、输入模式（自定义/基于框架）并保存。
- **样例库迁移**：对于存量样例库，必须执行四步迁移流程——导出 → 创建 RAG 表格库并导入 → 更新智能体配置（关闭样例库开关、添加表格库）→ 测试发布，详见 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **自动优化**：在 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面粘贴原始 Prompt，点击“优化”即可获得增强版本，并支持一键“保存为模板”。

### API/SDK 调用
- **模板调用**：使用 `GetPromptTemplate` 接口（[API 文档](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-prompt-engineering/api-bailian-2023-12-29-getprompttemplate.md)）传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 后，用业务数据填充生成最终 Prompt。
- **智能体调用**：在应用 API 请求中设置 `has_thoughts=true`，可调试样例检索或 RAG 召回过程；若使用 RAG 表格库，还需确保请求中包含已配置的知识库引用。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、优化）均仅支持华北2（北京）地域，跨地域调用将失败。
- **容量限制**：
  - 单个自定义 Prompt 模板内容最大 6144 字符（控制台编辑框右下角实时计数）；
  - RAG 表格库无单库条目上限，但样例库历史限制为 300 条（已停用，仅作兼容参考）；
  - 单次批量导入样例库文件 ≤20MB，最多 100 条（同上，迁移后不再适用）。
- **安全与合规**：
  - Prompt 自动优化过程不存储用户输入，亦不用于模型训练，符合数据隐私政策；
  - 所有 Prompt 内容需遵守内容安全规范，触发审核策略将导致优化失败或 API 返回错误码（参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）。
- **成本影响**：
  - Prompt 模板本身不产生额外费用；
  - 启用 RAG 表格库会增加 [Token](../concepts/token.md) 消耗（召回内容计入输入），并产生知识库运行时长、向量/排序模型调用费用，详见 [知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


