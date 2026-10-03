# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，是连接业务逻辑与模型能力的关键接口。通过结构化设计、模板化管理、样例增强和自动优化等机制，开发者可系统性提升模型输出的准确性、一致性与可控性。所有 Prompt 相关功能当前仅支持华北2（北京）地域。

## 支持的模型与功能

- **模型适配**：所有 Prompt 功能均兼容百炼平台支持的文本生成类大模型（如通义千问系列），图片生成类 Prompt 模板则需配合通义万相等多模态模型使用。
- **核心功能**：
  - **Prompt 模板**：支持预置模板（开箱即用）和自定义模板（含文本生成与图片生成两类），提供变量插值、集中管理与版本控制能力 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
  - **Prompt 样例库**：基于少样本学习（Few-shot）注入高质量问答对，引导模型输出风格与格式一致。> **注意**：该功能已停止维护，官方明确要求迁移至 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
  - **Prompt 自动优化**：利用大模型对原始 Prompt 进行结构重组、角色设定、指令增强与安全边界注入，无需人工 Prompt 工程经验 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - **Prompt 反馈优化**：基于用户提供的输入输出样例（query/answer 对）与评测数据集，进行多轮自动化评估与迭代优化，显著提升特定任务下的准确率 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 调用获取模板内容 | 必填；从控制台模板卡片或 `CreatePromptTemplate` 响应中获取 |
| `workspaceId` | 业务空间 ID，用于鉴权与资源隔离 | 必填；参见 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `variables` | 模板中声明的变量名数组（如 `["topic", "platform"]`），用于运行时填充 | 由 `GetPromptTemplate` 接口返回，不可手动指定 |
| `has_thoughts=true` | 启用样例库/RAG 检索过程日志输出（响应中含 `thoughts` 字段） | 仅适用于应用调用 API，非 Prompt 模板 API |
| `recall_count` | RAG 表格库召回片段数（原样例库“召回片段数”参数） | 应用配置中可调，默认 5，上限 10 |

## 使用方式

### 1. 控制台操作
- **创建模板**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 点击 **+ 创建提示词** → 选择类型（文本/图片生成）与输入模式（自定义创建 / 基于 Prompt 工程创建）→ 编辑内容 → 保存。
- **使用模板**：在智能体应用配置页的“提示词”区域，点击 **使用prompt创建应用**，模板内容自动填充，变量以 `${var}` 形式呈现。
- **启用反馈优化**：进入 [提示词 → 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimize) → 上传样例与评测数据 → 启动优化 → 保存结果为模板或直接创建应用。

### 2. API 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 字段，执行字符串替换生成最终 Prompt。
- **调用应用**：在 `InvokeApplication` 请求体中，若需注入样例或 RAG 内容，确保 `has_thoughts=true` 并正确关联知识库；最终 Prompt 由平台自动拼装，开发者无需手动构造上下文。

### 3. SDK 集成
- 使用 OpenAPI Explorer 生成 SDK 示例代码（推荐 V2.0），自动填充 `workspaceId` 和 `promptTemplateId`；运行前需配置 `accessKeyId` 和 `accessKeySecret` [获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、样例库、优化）仅支持华北2（北京）地域，跨地域调用将失败。
- **容量与性能**：
  - 单个 Prompt 模板内容最大 6144 字符（控制台编辑框限制）。
  - 原 Prompt 样例库单库上限 300 条样例，但该功能已废弃；RAG 表格库无数量上限，推荐迁移 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **安全与合规**：
  - Prompt 自动优化功能不存储用户输入数据，亦不用于模型训练 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - 所有用户提交的 Prompt 内容受百炼平台通用内容安全策略约束，触发审核时优化或调用将失败。
- **计费影响**：
  - Prompt 模板管理本身免费；但启用样例库或 RAG 表格库会显著增加输入 Token 消耗，从而提高模型调用费用。
  - RAG 表格库按知识库运行时长、向量/排序模型调用量单独计费，需关注账户余额 [RAG 表格库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


