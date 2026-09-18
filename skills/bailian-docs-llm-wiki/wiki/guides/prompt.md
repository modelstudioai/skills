# prompt

Prompt 是百炼平台中用于引导大语言模型生成预期输出的核心机制。它既可作为直接输入的文本指令，也可通过模板化、样例增强、自动优化等方式进行工程化管理，从而提升输出的一致性、准确性与业务适配性。所有 Prompt 相关能力均需在华北2（北京）地域使用。

## 支持的模型/功能

百炼平台提供多层次 Prompt 支持能力，覆盖从基础指令到高级工程化场景：

- **Prompt 模板**：支持预置模板（如营销文案生成、摘要抽取）和自定义模板（文本生成、图片生成），通过 `${variable}` 占位符实现动态填充。预置模板效果稳定、开箱即用；自定义模板支持基于 ICIO/CRISPE/RASCEF 等 Prompt 工程框架结构化构建，适用于金融、医疗等强业务约束场景 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
- **Prompt 样例库**：通过少样本（few-shot）方式注入高质量问答对，引导模型遵循特定解释结构或格式风格（如术语解释+类比）。但该功能**已停止维护**，官方明确推荐迁移到 RAG 表格库 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
- **Prompt 自动优化**：基于大模型对原始 Prompt 进行结构重组、角色设定、指令增强与安全边界注入，无需人工 Prompt 工程经验即可获得更清晰、稳定的版本 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **Prompt 反馈优化**：利用用户提供的输入输出样例（query-answer pairs）进行多轮评测与反思，自动生成含 few-shot 示例和边界说明的高精度 Prompt，尤其适合分类、结构化输出等任务 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

> **注意**：文档 3 和文档 4 明确指出 Prompt 样例库功能已下线，其能力由 RAG 表格库承接。开发者不应再新建或依赖样例库，而应按 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) 文档完成迁移。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `workspaceId` | 业务空间 ID，所有 Prompt 模板、样例库、RAG 库均需归属同一 workspace 才能被应用关联。获取方式见 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 | 必填，API 调用必需 |
| `promptTemplateId` | 模板唯一标识符，可在控制台模板卡片上直接复制。调用 `GetPromptTemplate` 接口时必需。 | 必填，API 调用必需 |
| `variables` | 模板中声明的变量名数组（如 `["topic", "platform"]`），用于校验填充数据完整性。由 `GetPromptTemplate` 接口返回。 | 只读，由平台生成 |
| `has_thoughts=true` | API 调用时启用该参数，可在响应 `thoughts` 字段中查看样例检索或 RAG 召回的详细过程，用于调试。 | 仅调试有效，非必需 |
| `召回片段数` | RAG 表格库配置项（默认 5，上限 10），控制注入上下文的样例/知识条目数量，直接影响 token 消耗与响应延迟。 | 应用配置页可调 |

## 使用方式

### 控制台操作
- **创建模板**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 点击 **+ 创建提示词** → 选择“文本生成”或“图片生成”，填写内容并保存。
- **使用模板**：在智能体应用配置页 → 点击 **使用prompt创建应用** → 模板内容自动填充至提示词框，替换 `${var}` 占位符后即可调试。
- **启用反馈优化**：进入 [提示词 → 反馈优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/feedback-optimize) → 上传初始 Prompt、样例数据（5–10 条）、评测数据（≥20 条）→ 启动优化任务。

### API 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析返回的 `content` 并填充变量。
- **调用应用**：在 `InvokeApplication` 请求体中设置 `has_thoughts: true` 以获取检索详情；若使用 RAG 表格库，确保应用已关联对应知识库且配置生效。
- **创建模板**：调用 `CreatePromptTemplate` 接口，需在请求体中指定 `name`、`type`（`TEXT_GENERATION`/`IMAGE_GENERATION`）、`content` 或 `positivePrompt`/`negativePrompt`。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库）**仅支持华北2（北京）地域**，跨地域调用将失败。
- **字符与 Token 限制**：
  - 模板内容最大长度为 **6144 字符**（控制台编辑框右下角实时计数）。
  - 反馈优化的评测数据建议 ≥20 条，样例数据建议 5–10 条且覆盖全部类别；单条样例过长可能导致优化失败 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。
- **功能弃用与迁移**：
  - Prompt 样例库已停用，新项目必须使用 RAG 表格库替代；存量样例库需按文档 4 完成迁移，否则无法继续使用。
  - RAG 表格库按量计费（知识库运行时长 + 向量/排序模型调用），而旧样例库虽免费但已不可用。
- **安全与隐私**：Prompt 自动优化过程中提交的原始 Prompt **不会被存储或用于模型训练**，符合阿里云数据隐私政策 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
- **模型依赖**：反馈优化功能推荐使用 `qwen-max` 作为推理模型，以获得最佳评测效果；其他模型可能影响优化收敛质量。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


