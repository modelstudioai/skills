# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心控制机制。它既可作为静态指令直接调用，也可通过模板化、样例增强、自动优化等方式实现工程化管理。合理设计和使用 Prompt 能显著提升输出质量、格式一致性与业务适配性，是构建稳定可靠大模型应用的关键环节。

## 支持的模型/功能

百炼平台提供多种 Prompt 相关功能，覆盖从基础提示词构造到高级工程化优化的全链路：

- **自定义 Prompt 模板**：支持文本生成与图片生成两类模板，其中文本生成模板提供「自定义创建」和「基于 [Prompt 工程](../concepts/prompt-engineering.md)创建」两种模式，并内置 ICIO、CRISPE、RASCEF 等结构化框架 [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)；
- **预置 Prompt 模板**：由阿里云官方提供并已验证效果的通用场景模板（如营销文案生成、摘要抽取等），开箱即用，不支持修改 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)；
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（few-shot）与评测数据集，通过多轮自动化评估与反思生成优化 Prompt，推荐使用千问-max 作为推理模型 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)；
- **Prompt 自动优化**：对单条原始 Prompt 进行结构重组、角色注入、指令增强等重写，不依赖样例数据，且**不计费** [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

> **注意**：Prompt 样例库功能已下线，[原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) 明确说明“该功能已不再维护”，所有新项目应迁移至 RAG 表格库；迁移指南见 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | 必填，长度固定，控制台模板卡片中可获取 |
| `workspaceId` | 业务空间 ID，用于鉴权与资源隔离 | 必填，需通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `variables` | 模板中声明的占位符变量列表（如 `${topic}`） | 由 `GetPromptTemplate` 接口返回，调用前需确认变量名与业务数据匹配 |
| `has_thoughts` | API 请求参数，启用后响应中返回 `thoughts` 字段，含样例检索或 RAG 召回详情 | 布尔值，默认 `false`；调试时建议设为 `true` |
| 召回片段数 | 控制注入上下文的样例/RAG 片段数量 | 默认 5，最多 10（样例库）；RAG 表格库中可通过滑块配置 |

## 使用方式

### 控制台操作
- **创建模板**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 单击 **创建提示词** → 选择类型（文本/图片生成）与输入模式（自定义 / [Prompt 工程](../concepts/prompt-engineering.md)）→ 编辑并保存；
- **复用预置模板**：在 [提示词市场](https://bailian.console.aliyun.com/?tab=app#/plugin-market/prompt) 中选择模板 → 单击 **... → 创建应用**，内容将自动填充至智能体提示词编辑框；
- **优化 Prompt**：在提示词管理页右上角进入 **[自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize)** → 输入原始 Prompt → 单击 **优化** → 复制或保存为模板。

### API 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 字段；
- **生成最终 Prompt**：将业务数据按 `variables` 列表顺序或名称替换 `content` 中对应占位符（如 `${topic}` → `"杭州亚运会"`）；
- **调用模型**：将生成的完整 Prompt 作为 `system` 或 `user` 消息传入模型 API（如 `ChatCompletion`）；
- **启用调试**：请求中设置 `has_thoughts=true`，便于分析样例召回或 RAG 检索过程。

## 限制和注意事项

- **地域限制**：自定义 Prompt 模板与预置模板功能**仅支持华北2（北京）地域**，跨地域调用将失败 [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)；
- **模板容量**：单个自定义 Prompt 模板内容最大支持 **6144 字符**（控制台编辑框右下角实时统计）；
- **样例库已弃用**：Prompt 样例库功能停止维护，存量应用须迁移至 RAG 表格库；迁移后可突破原 300 条/库上限，并支持召回策略配置 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)；
- **Token 成本影响**：启用样例库（已弃用）或 RAG 表格库会显著增加输入 Token，直接影响调用费用；成本公式为：`总输入 Token ≈ 用户查询 Token + 召回内容 Token + 系统指令 Token`；
- **模型兼容性**：Prompt 反馈优化明确推荐使用 `qwen-max` 作为推理模型，其他模型可能无法达到同等优化效果 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


