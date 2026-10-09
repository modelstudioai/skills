# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于定义任务目标、上下文、输入约束与输出格式。通过结构化设计（如模板、样例库、自动优化等机制），开发者可实现 Prompt 的可复用、可管理、可迭代，从而提升模型输出的准确性、一致性与业务适配性。该能力覆盖文本生成、图片生成、知识增强等多种场景，是构建稳定可靠 LLM 应用的关键基础设施。

## 支持的模型与功能

- **基础模型支持**：所有百炼托管的文本生成类大模型（如通义千问系列）均原生支持 Prompt 输入；图片生成类模型（如万相）支持正向/负向 Prompt 分离输入。
- **核心功能模块**：
  - **Prompt 模板**：提供预置与自定义两类模板，支持变量插值（如 `${topic}`）、结构化框架（ICIO/CRISPE/RASCEF）及跨环境复用 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。
  - **Prompt 样例库**：基于少样本学习（Few-shot）注入高质量问答对，引导模型风格与格式对齐（*注意：该功能已停止维护*）[使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。
  - **RAG 表格库替代方案**：> **注意**：Prompt 样例库功能已下线，官方明确要求迁移至 RAG 表格库以获得更高容量、可配置召回策略及更优效果 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
  - **Prompt 自动优化**：利用大模型对原始 Prompt 进行结构重组、角色注入与指令增强，无需人工 Prompt 工程经验 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。
  - **Prompt 反馈优化**：基于用户提供的输入-输出样例（5–10 条）与评测数据（≥20 条），通过多轮评估-反思-重写闭环生成高保真 Prompt，适用于强业务规则场景 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `promptTemplateId` | string | 模板唯一标识符，用于 API 获取模板内容 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `workspaceId` | string | 业务空间 ID，所有 Prompt 相关操作必需 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `variables` | array<string> | 模板中声明的变量名列表（如 `["platform", "topic"]`），用于运行时填充 | [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `has_thoughts` | boolean | API 调用时启用，返回 `thoughts` 字段含样例检索/知识召回详情（兼容旧样例库与新 RAG 表格库） | [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md) |
| `recall_count` | integer | RAG 表格库召回片段数（默认 5，上限 10），影响 [Token](../concepts/token.md) 消耗与响应质量 | [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |

## 使用方式

### 控制台操作路径
- **模板管理**：`应用开发 > 组件管理 > 提示词` → 创建/编辑/复制/调用模板  
- **自动优化**：`应用开发 > 组件管理 > 提示词 > 自动优化` → 粘贴原始 Prompt → 一键生成并保存为模板  
- **反馈优化**：`应用开发 > 组件管理 > 提示词 > 反馈优化` → 上传样例与评测数据 → 启动多轮优化任务  
- **RAG 表格库配置**：`应用开发 > 知识库 > 创建数据查询型知识库` → 上传 Excel → 配置索引与召回策略 → 在智能体应用中绑定  

### API 集成要点
- 模板获取：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 与 `variables` 字段后执行变量替换。
- 应用调用：在 `InvokeApplication` 请求体中，若启用知识增强，需设置 `has_thoughts: true` 并确保应用已关联 RAG 表格库（非样例库）。
- 错误处理：所有 Prompt 相关 API 均遵循统一错误码规范，详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库/RAG）当前仅支持华北2（北京）地域，跨地域调用将失败。
- **模板长度**：单个 Prompt 模板内容最大支持 6144 字符（控制台编辑框右下角实时计数）。
- **RAG 表格库替代强制性**：> **注意**：Prompt 样例库已于近期下线，其全部功能由 RAG 表格库承接；现有依赖样例库的应用必须完成迁移，否则无法生效 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。
- **[Token](../concepts/token.md) 成本敏感**：启用 RAG 表格库或反馈优化会显著增加输入 [Token](../concepts/token.md)（召回样例/评测数据注入），需在 `recall_count` 与 `max_assemble_length` 间权衡效果与成本。
- **安全边界**：自动优化功能不存储用户 Prompt 数据，亦不用于模型训练，符合阿里云数据隐私政策 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


