# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心指令载体。它既可作为直接输入的文本字符串，也可通过结构化模板、样例库或自动优化机制进行工程化管理。合理设计和管理 Prompt 是保障模型输出质量、一致性与业务适配性的关键环节，尤其在智能体应用、RAG 增强及垂直领域任务中起决定性作用。

## 支持的模型/功能

百炼平台提供多层次 Prompt 支持能力，覆盖从基础指令输入到高级工程化管理的全链路：

- **Prompt 模板**：支持预置模板（如营销文案、摘要抽取、文案润色等）和自定义模板两类，均通过 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage) 统一维护。预置模板由阿里云提供并已优化，适用于通用场景；自定义模板支持文本生成与图片生成双模态，且可基于 ICIO / CRISPE / RASCEF 等 Prompt 工程框架构建，详见 [自定义Prompt模板](raw/application-user-guide/prompt/prompt-custom-template.md)。
- **Prompt 自动优化**：利用大模型对原始 Prompt 进行结构重组、角色注入、指令增强与安全边界补充，提升效果稳定性，该功能不计费且数据不用于训练 [Prompt自动优化](raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：基于用户提供的输入-输出样例（.xlsx/.xls）与评测数据集，通过多轮推理与评估生成高保真 Prompt，适用于强格式约束（如 JSON 输出）或专业领域任务，效果优于纯文本自动优化 [基于大模型输入输出样例的Prompt自动优化](raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **样例库（已迁移）**：原 Prompt 样例库功能已下线，其能力由更灵活的 RAG 表格库承接。历史样例数据仍可通过“从样例库选择”在反馈优化中复用，但新建应用应使用 RAG 表格库实现知识增强 [Prompt 样例库迁移到 RAG 表格库](raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。

> **注意**：文档 5 明确指出“Prompt样例库功能已不再维护，控制台入口已下线”，而文档 4 与文档 5 均强调迁移至 RAG 表格库是当前唯一推荐路径。因此，任何新项目均不应依赖样例库，而应直接采用 RAG 表格库方案。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用获取模板内容 | 必填，长度固定，从控制台模板卡片复制 |
| `workspaceId` | 业务空间 ID，所有 Prompt 相关操作均需指定 | 必填，通过 [获取APP ID 和 Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `variables` | 模板中声明的动态变量名列表（如 `["platform", "topic"]`），用于运行时填充 | 由 `GetPromptTemplate` 接口返回，不可自定义变量语法 |
| `has_thoughts=true` | API 请求参数，启用后响应中返回 `thoughts` 字段，含样例检索或 RAG 召回详情 | 仅用于调试，生产环境建议关闭以节省 [Token](../concepts/token.md) |
| 召回片段数 | RAG 表格库配置项，控制注入上下文的样例数量 | 默认 5，最大 10（样例库旧限制），RAG 表格库无此硬限 |

## 使用方式

### 控制台操作
- **创建模板**：进入 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage)，点击“创建提示词”，选择“自定义创建”或“基于Prompt工程创建”，填写名称、类型及内容后保存。
- **调用模板**：在智能体应用配置页，点击“更多”→“创建应用”，模板将自动填充至提示词编辑框；或在模板卡片点击“查看详情”→“复制到自定义模板”进行二次开发。
- **优化 Prompt**：在提示词管理页切换至“自动优化”分类，粘贴原始 Prompt 后点击“优化”，结果可直接复制或“保存为模板”。

### API 调用
1. 调用 `ListPromptTemplates`（`type=System` 或 `type=Custom`）获取模板列表；
2. 调用 `GetPromptTemplate` 传入 `workspaceId` 和 `promptTemplateId` 获取模板内容与变量；
3. 将变量值代入 `content` 字段生成最终 Prompt，再调用模型推理接口（如 `ChatCompletion`）；
4. 对于 RAG 增强，需在应用配置中关联 RAG 表格库，并确保请求中 `has_thoughts=true` 以调试召回逻辑。

### SDK 示例
使用 `GetPromptTemplate` 的 SDK 示例代码可直接在 [获取Prompt模板](raw/_short/api-bailian-2023-12-29-getprompttemplate-584c357dd7cb48d6.md) 文档的“SDK示例”页签中生成，支持 Java/Python 等主流语言。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板功能（含预置与自定义）仅支持华北2（北京）地域，跨地域调用将失败 [Prompt模板概述](raw/application-user-guide/prompt/prompt-template.md)。
- **字符与容量限制**：
  - 单个模板 `content` 最大 6144 字符（控制台编辑框右下角实时计数）；
  - 自定义创建模式下，原始 Prompt 输入上限为 10000 字符；
  - RAG 表格库无单库条目数上限，而旧样例库严格限制为 300 条/库。
- **安全与合规**：自动优化功能不存储用户数据，亦不用于模型训练，符合阿里云数据隐私政策 [Prompt自动优化](raw/application-user-guide/prompt/optimize-prompt.md)。
- **[Token](../concepts/token.md) 成本**：启用样例库或 RAG 表格库会显著增加输入 [Token](../concepts/token.md)（含召回样例内容），需在成本与效果间权衡；公式为：`总输入 Token ≈ 用户查询 Token + 召回样例总 Token + 系统指令 Token`。
- **模板变量语法**：仅支持 `${variable}` 形式，不支持嵌套、条件判断或[函数调用](../concepts/function-calling.md)等高级模板语法。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


