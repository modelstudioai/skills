# prompt

Prompt 是百炼平台中用于引导大模型生成预期输出的核心指令载体。它既可作为静态文本直接调用模型，也可通过模板化、样例增强、自动优化等方式实现结构化管理与效果提升。平台提供从基础 Prompt 编写、框架化设计、模板复用，到基于数据反馈的智能优化等全链路支持，适用于文本生成、图片生成、知识问答、格式化输出等多种场景。

## 支持的模型/功能

- **模型适配**：所有百炼托管的大语言模型（如通义千问系列）均原生支持 Prompt 输入；图片生成类模型（如万相）支持正向/负向 Prompt 分离输入 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **核心功能**：
  - **Prompt 模板**：支持预置模板（开箱即用）和自定义模板（含文本生成、图片生成两类），实现变量注入与跨应用复用 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
  - **Prompt 样例库**：通过少样本（few-shot）问答对引导模型输出，但该功能已**停止维护**，官方明确推荐迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
  - **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与安全边界注入，提升清晰度与稳定性 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - **Prompt 反馈优化**：利用用户提供的输入-输出样例（query-answer pairs）进行多轮评测与反思式优化，显著提升业务场景下的准确率，尤其适用于分类、结构化生成等任务 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 明确声明“Prompt样例库功能已不再维护”，而文档 4 提供了完整的迁移路径。开发者应避免新建样例库，所有新项目须使用 RAG 表格库替代。

## 关键参数

| 参数 | 说明 | 取值/约束 | 来源 |
|------|------|-----------|------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用获取模板内容 | 字符串，由平台生成 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | 模板中定义的占位符列表（如 `${topic}`、`${num1}`） | 数组，返回于 `GetPromptTemplate` 响应中 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `workspaceId` | 业务空间 ID，所有 Prompt 相关 API 的必需参数 | 字符串，需通过[获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)获取 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `recall_count` | RAG 表格库召回片段数（原样例库的“召回片段数”） | 默认 5，最大 10 | [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |
| `max_input_tokens` | 自动优化功能对原始 Prompt 的长度限制 | 未明确定义，但文档 5 指出“输入内容过长会失败”，实践中建议 ≤ 2048 tokens | [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md) |

## 使用方式

### 控制台操作
- **创建模板**：进入[提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)页面 → 单击 **创建提示词** → 选择类型（文本生成/图片生成）与输入模式（自定义创建 / 基于Prompt工程创建）→ 填写内容 → 点击 **优化Prompt**（可选）→ **保存** [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。
- **使用模板**：在智能体应用配置页 → 点击 **使用prompt创建应用** → 模板变量（如 `${name}`）自动填充至提示词框 → 输入测试问题调试 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **启用反馈优化**：进入[提示词反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimize)页面 → 新增任务 → 选择推理模型（推荐 `qwen-max`）→ 输入初始 Prompt → 上传样例数据（5–10 条）与评测数据（≥20 条）→ 启动优化 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

### API 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，响应中包含 `content` 与 `variables` 字段，供运行时变量替换 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **调用带样例/知识的应用**：在应用 API 请求中设置 `has_thoughts=true`，响应 `thoughts` 字段将返回 RAG 检索详情，便于调试 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **创建模板**：调用 `CreatePromptTemplate` 接口，需指定 `type`（`TEXT_GENERATION` 或 `IMAGE_GENERATION`）、`name`、`content` 等字段 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（包括创建、管理、调用）当前**仅支持华北2（北京）地域**，跨地域调用将失败 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)、[Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **容量限制**：
  - 单个 Prompt 模板内容最大支持 **6144 字符**（控制台编辑器右下角实时计数）。
  - RAG 表格库无单库条目上限；原样例库硬性限制为 **300 条/库**，且单应用最多关联 **5 个库** [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **安全与隐私**：
  - Prompt 自动优化过程**不存储用户输入数据，且绝不用于模型训练** [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - 所有 Prompt 内容及样例数据均受百炼平台数据隔离策略保护，仅限所属 workspace 访问。
- **成本影响**：
  - 使用 RAG 表格库或样例库会**显著增加输入 [Token](../concepts/token.md) 消耗**（因召回内容注入上下文），直接影响模型调用费用 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
  - Prompt 自动优化功能本身**免费**，但其生成的 Prompt 若导致更长输出或更高频调用，间接影响费用 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


