# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于定义任务目标、上下文、约束条件与输出格式。通过结构化设计（如模板化、样例引导、框架化工程）和自动化优化手段，开发者可显著提升模型输出的准确性、一致性与可控性，降低人工调优成本。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供多层次 Prompt 支持能力，覆盖从基础指令构造到高级工程化管理的全链路：

- **Prompt 模板**：支持预置模板（开箱即用，效果稳定）和自定义模板（可编辑、可复用），适用于文本生成与图片生成两类场景。预置模板通过 `ListPromptTemplates` 接口（`type=System`）获取，自定义模板可通过控制台或 [CreatePromptTemplate](raw/_short/api-bailian-2023-12-29-createprompttemplate-1194e536beb0529a.md) API 创建 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **[Prompt 工程](../concepts/prompt-engineering.md)框架**：内置 ICIO、CRISPE、RASCEF 三类结构化框架，分别适配简单任务执行、角色化交互与多步骤复杂流程，帮助开发者系统化构建高质量 Prompt [原文标题](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **Prompt 样例库（已下线）**：该功能已停止维护，控制台入口不可见；既有数据仅可在提示词管理的反馈优化中通过“从样例库选择”有限复用。官方推荐迁移至 RAG 表格库以获得更强检索能力与灵活性 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（.xlsx/.xls）与评测数据，自动迭代生成更贴合业务预期的 Prompt，支持保存为模板或直接创建智能体应用 [原文标题](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **Prompt 自动优化**：对单条原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，不依赖样例数据，适合快速提效 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)。

> **注意**：文档 3 和文档 4 明确指出 Prompt 样例库功能已下线，且迁移路径已明确指向 RAG 表格库；而文档 1 和文档 2 中仍存在对该功能的引用（如“样例库”菜单项、关联配置说明），这些内容已过时，实际开发中应忽略样例库独立配置路径，统一采用 RAG 表格库替代方案。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspaceId` | 业务空间唯一标识，所有 Prompt 操作必需 | 需通过 [获取APP ID 和 Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `promptTemplateId` | 模板唯一 ID，用于拉取与渲染 | 预置模板 ID 由平台分配；自定义模板 ID 在创建后生成 |
| `variables` | 模板中声明的占位符列表（如 `${topic}`） | 必须在填充时全部提供，否则生成失败 |
| `max_tokens`（API 调用） | 控制模型输出长度 | 受所选模型最大输出长度限制 |
| `has_thoughts=true`（API 调用） | 启用调试模式，返回 `thoughts` 字段含检索/推理过程 | 仅用于调试，生产环境建议关闭 |

## 使用方式

### 控制台操作
- **模板管理**：进入 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage)，按类型筛选（文本生成/图片生成）、搜索或使用“创建提示词”入口。预置模板支持“复制到自定义模板”，自定义模板支持编辑、复制、删除。
- **模板填充与测试**：在模板卡片点击 `···` → “创建应用”，模板内容自动填入智能体应用提示词区；右侧输入测试问题，实时查看输出与 token 统计。
- **自动优化**：在“自动优化”分类页粘贴原始 Prompt，点击“优化”获取改写结果，支持“复制”或“保存为模板”。
- **反馈优化**：在“反馈优化”分类页创建优化包，上传样例数据（≤100 条）与评测数据（≥20 条），提交后系统自动产出最优 Prompt。

### API/SDK 调用
- **模板生命周期**：使用 `CreatePromptTemplate`、`GetPromptTemplate`、`ListPromptTemplates`（`type=System` 或 `type=Custom`）等接口管理模板 [原文标题](../../raw/application-user-guide/prompt/prompt-template.md)。
- **模板渲染**：调用 `GetPromptTemplate` 获取模板内容与 `variables` 列表，程序内完成变量替换（如 `content.replace('${topic}', 'AI')`），再将生成的完整 Prompt 发送给模型 API。
- **RAG 表格库集成**：在智能体应用配置中关闭样例库开关，添加 RAG 表格库知识源，并通过 `has_thoughts=true` 调试检索逻辑 [原文标题](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库迁移）仅支持华北2（北京）地域，跨地域调用将失败。
- **字符与数量限制**：
  - 模板内容最大 6144 字符（控制台编辑框显示计数）；
  - 自定义模板名称 ≤20 字符；
  - RAG 表格库无样例数量上限，但单次召回片段数默认 5、上限 10；
  - Prompt 反馈优化中，样例数据建议 5–10 条（覆盖各场景），评测数据建议 ≥20 条。
- **安全与合规**：
  - 自动优化与反馈优化过程中提交的数据**不会被用于模型训练**，符合阿里云数据隐私政策 [原文标题](../../raw/application-user-guide/prompt/optimize-prompt.md)；
  - 所有 Prompt 内容需遵守内容安全规范，触发审核策略将导致优化失败。
- **性能与成本**：
  - 启用 RAG 表格库会增加输入 [Token](../concepts/token.md) 消耗（召回样例内容计入上下文），影响模型调用费用；
  - 样例库虽已下线，但其历史数据若未迁移，将无法在新应用中复用，务必按 [Prompt 样例库迁移到 RAG 表格库](raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 文档完成迁移。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)


