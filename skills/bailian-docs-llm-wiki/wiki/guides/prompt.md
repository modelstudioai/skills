# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心机制。它既可作为直接输入的文本指令，也可通过模板化、样例增强、自动优化等工程化手段进行结构化管理与持续迭代。合理设计和使用 Prompt 是提升模型输出准确性、一致性与业务适配性的关键实践。

## 支持的模型/功能

百炼平台支持在多种模型上使用 Prompt，包括通义千问系列（如 `qwen-plus-latest-128k`）、`qwen-max` 等主流文本模型，以及图像生成类模型（如通义万相）。Prompt 相关功能覆盖全生命周期：  
- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（含文本生成与图片生成两类），均需在华北2（北京）地域使用 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)；  
- **Prompt 样例库**：已**停止维护**，官方明确推荐迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)；  
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色注入与指令增强，不计费且数据不用于训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；  
- **Prompt 反馈优化**：利用用户提供的输入-输出样例（5–10 条基础样例 + ≥20 条评测数据）驱动多轮评估与迭代，显著提升场景定制效果，推荐使用 `qwen-max` 作为推理模型 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 和文档 6 均指出 Prompt 样例库功能已下线，所有新项目应使用 RAG 表格库替代。若文档中仍存在“样例库可用”或“推荐使用样例库”的表述，属过时信息，以文档 6 的迁移指引为准。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspaceId` | 业务空间 ID，调用 Prompt 相关 API 的必需参数 | 需通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 模板唯一标识符，用于 `GetPromptTemplate` 等接口 | 预置或自定义模板卡片上直接获取 |
| `variables` | 模板变量列表（如 `["platform", "topic"]`），由 `GetPromptTemplate` 接口返回 | 必须在填充时提供全部变量值，否则生成失败 |
| `has_thoughts` | 应用 API 调用参数，启用后响应中返回 `thoughts` 字段（含样例检索或 RAG 召回详情） | `true` / `false`，调试必备 |
| `recall_count` | RAG 表格库召回片段数（原样例库“召回片段数”） | 默认 5，最大 10（见 [RAG 表格库配置](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)） |

## 使用方式

### 控制台操作
- **模板创建**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 单击 **+ 创建提示词** → 选择“文本生成”或“图片生成”，并指定“自定义创建”或“基于Prompt工程创建”（如 ICIO/CRISPE/RASCEF 框架）[自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)；  
- **样例库迁移**：导出旧样例库 → 创建 RAG 表格库（类型选“数据查询”）→ 上传 Excel 并关闭 `answer` 字段的“参与检索” → 在智能体应用中替换知识源 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)；  
- **调试验证**：在应用调试界面开启 `prompt样例检索` 或 `RAG 调试`，实时查看召回内容与 token 统计。

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析返回的 `content` 与 `variables` 后填充变量生成最终 Prompt；  
- **应用调用**：向智能体应用 API 发送请求时，设置 `has_thoughts=true` 可获取 `thoughts` 字段中的上下文注入详情（适用于样例库历史调试或 RAG 效果分析）；  
- **自动优化**：无独立 API，仅控制台功能，优化结果可手动保存为模板复用。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（含预置与自定义）仅支持华北2（北京）地域，跨地域调用将失败 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)；  
- **模板长度**：控制台编辑器最大支持 6144 字符，超长 Prompt 需拆分或精简；  
- **样例库容量**：单库上限 300 条，且已停服；RAG 表格库无数量限制，但单次召回最多 10 片段，需权衡效果与 token 成本；  
- **安全与隐私**：Prompt 自动优化过程不存储用户输入数据，亦不用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)；  
- **计费影响**：启用 RAG 表格库或历史样例库会增加输入 token（样例内容注入），从而提高模型调用费用；RAG 表格库本身按小时+向量/排序模型调用单独计费 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)


