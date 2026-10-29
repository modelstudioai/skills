# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于定义任务目标、约束输出格式、注入领域知识及引导推理路径。通过结构化模板、样例增强与自动优化等能力，开发者可系统性地管理 Prompt 的设计、复用与迭代，显著提升模型输出的准确性、一致性与业务适配性。所有 Prompt 相关功能当前仅支持华北2（北京）地域。

## 支持的模型/功能

百炼平台提供三类 Prompt 增强能力，覆盖从基础指令到复杂任务编排的全链路需求：

- **Prompt 模板**：支持预置与自定义两类模板，适用于文本生成、图片生成等场景。预置模板由阿里云提供并已优化，开箱即用；自定义模板支持通过控制台或 API 创建，可基于 [ICIO / CRISPE / RASCEF](raw/application-user-guide/prompt/prompt-custom-template.md) 等 [Prompt 工程](../concepts/prompt-engineering.md)框架结构化构建，确保指令清晰、上下文完整、输出可控 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
  
- **Prompt 样例库（已下线）**：原用于少样本学习（Few-shot），通过注入高质量问答对引导模型风格与格式。**该功能已停止维护**，控制台入口不可见，不建议新项目使用。历史数据仍可通过提示词管理的反馈优化模块“从样例库选择”复用，但官方明确推荐迁移至 RAG 表格库 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。

- **Prompt 自动优化与反馈优化**：
  - *自动优化*：基于大模型对单条原始 Prompt 进行重写，强化角色设定、指令明确性与安全边界，不依赖用户数据 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - *反馈优化*：以用户提供的输入-输出样例（query-answer pairs）为优化依据，通过多轮评测与反思生成高保真 Prompt，适用于分类、结构化抽取等强对齐任务 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 和文档 4 明确指出 Prompt 样例库功能已下线，且迁移路径已标准化。若文档 1 中提及“样例库”作为可用功能（如“从样例库选择”），其实际含义仅限于历史数据复用入口，**不可新建或直接关联应用**，开发者应优先采用 RAG 表格库替代。

## 关键参数

| 参数 | 说明 | 取值/限制 | 来源 |
|------|------|-----------|------|
| `promptTemplateId` | 模板唯一标识符 | 字符串，由平台生成；预置模板 `type=System`，自定义模板 `type=Custom` | [原文标题](../../raw/application-user-guide/prompt/prompt-template.md) |
| `workspaceId` | 业务空间 ID | 必填，需通过 [获取APP ID 和 Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 | [原文标题](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板变量列表 | JSON 数组，如 `["platform", "topic"]`；变量名需符合 `${var}` 语法 | [原文标题](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts` | 启用调试信息 | API 调用时设为 `true`，响应中返回 `thoughts` 字段含检索/优化过程详情 | [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| `recall_count` | 召回片段数（RAG 表格库） | 默认 5，最大 10；控制注入上下文的样例数量，影响 [Token](../concepts/token.md) 消耗与效果 | [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |

## 使用方式

### 1. 模板创建与调用
- **控制台**：进入 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage)，选择“创建提示词”，按向导配置名称、类型（文本/图片）、输入模式（自定义/工程框架），保存后获取 `promptTemplateId`。
- **API**：调用 `GetPromptTemplate` 接口传入 `workspaceId` 和 `promptTemplateId` 获取模板内容与变量；再将业务数据填充至变量生成最终 Prompt，提交至模型 API。
- **SDK**：使用 OpenAPI 调试页生成的 SDK 示例代码，自动注入 `workspaceId` 和 `promptTemplateId`，支持 Java/Python 等主流语言 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。

### 2. 反馈优化工作流
1. 在提示词管理 → **反馈优化** 分类下点击 **新增优化包**；
2. 配置任务名称、推理模型（推荐千问-Max）、初始 Prompt；
3. 上传样例数据（5–10 条，覆盖各场景）与评测数据（≥20 条）；
4. 启动优化，平台生成候选 Prompt 并基于评测数据自动筛选最优解；
5. 将结果 **保存为 Prompt 模板** 或 **直接创建智能体应用**。

### 3. RAG 表格库替代样例库
- 导出历史样例库数据（如无法导出，联系阿里云支持）；
- 创建 **数据查询型** RAG 表格库，上传 Excel 文件（列名需为 `query`/`answer`）；
- 关闭 `answer` 字段的“参与检索”，确保仅基于问题匹配；
- 在智能体应用配置中移除样例库开关，添加该表格库，并调试召回策略 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **模板长度**：控制台 Prompt 输入框最大支持 6144 字符；API 提交的 `content` 字段无显式长度限制，但受模型上下文窗口约束。
- **样例库弃用**：Prompt 样例库已下线，新项目必须使用 RAG 表格库。迁移后效果通常更优，因 RAG 支持可配置的检索策略、无数量上限及向量语义匹配 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **[Token](../concepts/token.md) 成本**：启用样例库或 RAG 表格库会显著增加输入 [Token](../concepts/token.md)（样例内容 + 用户查询），直接影响计费。成本预估公式：`总输入 Token ≈ 用户查询 Token + 召回样例总 Token + 系统指令 Token`。
- **数据安全**：Prompt 自动优化与反馈优化过程中，用户提交的原始 Prompt 和样例数据**不会被存储或用于模型训练**，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


