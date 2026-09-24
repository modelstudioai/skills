# prompt

Prompt 是百炼平台中驱动大语言模型行为的核心指令载体，用于定义任务目标、约束输出格式、注入领域知识及引导推理路径。通过模板化、样例增强、自动优化等机制，百炼支持从简单文本指令到复杂结构化提示的全生命周期管理，兼顾开发效率与效果可控性。所有 Prompt 功能当前仅适用于华北2（北京）地域。

## 支持的模型/功能

- **模板化支持**：提供预置 Prompt 模板（如营销文案生成、摘要抽取）和自定义 Prompt 模板两类，分别适用于通用场景与高定制需求 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。  
- **多模态模板类型**：支持文本生成（含 ICIO/CRISPE/RASCEF 等 Prompt 工程框架）与图片生成（正向/负向 Prompt 分离）两种基础类型 [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。  
- **样例增强能力**：曾支持 Prompt 样例库（Few-shot 问答对注入），但该功能**已下线并停止维护**，官方明确推荐迁移至 RAG 表格库替代 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。  
- **自动优化能力**：提供两种优化路径：  
  - 基于单条原始 Prompt 的结构重写（角色设定、指令增强、安全边界注入）；  
  - 基于输入输出样例（query/answer 对）的反馈式优化，通过多轮评测与反思生成更贴合业务效果的 Prompt [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。  

> **注意**：文档 3 中描述的 Prompt 样例库功能已被废弃，其全部能力由 RAG 表格库承接；任何仍引用该功能的代码或配置需立即更新，否则将失效。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取模板内容 | 必填，从控制台模板卡片或 `CreatePromptTemplate` 响应中获取 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md) |
| `workspaceId` | 业务空间 ID，用于鉴权与资源隔离 | 必填，通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `variables` | 模板中声明的占位符列表（如 `["topic", "platform"]`），调用时需传入对应值 | 由 `GetPromptTemplate` 接口返回，不可在运行时动态增删 |
| `recall_count` | RAG 表格库召回片段数（原样例库 `top_k`），默认 5，最大 10 | 应用配置中可调，影响 [Token](../concepts/token.md) 消耗与响应质量 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md) |
| `has_thoughts` | API 请求参数，设为 `true` 时返回 `thoughts` 字段，含样例检索或 RAG 召回详情 | 仅调试用途，生产环境建议关闭以节省 [Token](../concepts/token.md) |

## 使用方式

### 控制台操作
- **创建模板**：进入 [提示词](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 页面 → 点击 **+ 创建提示词** → 选择“文本生成”或“图片生成”，按向导填写；支持“自定义创建”或“基于 Prompt 工程创建” [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)。  
- **调用模板**：在智能体应用配置页 → 点击 **使用 prompt 创建应用** → 模板变量（如 `${topic}`）自动填充至提示词框 → 输入测试问题调试 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。  
- **自动优化**：进入 [自动优化](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt/optimize) 页面 → 粘贴原始 Prompt → 点击 **优化** → 可直接复制或保存为模板 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。  

### API/SDK 调用
- **获取模板**：调用 `GetPromptTemplate` 接口，传入 `workspaceId` 和 `promptTemplateId`，解析响应中的 `content` 并替换 `variables` 值 [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)。  
- **RAG 表格库集成**：在智能体应用配置中启用表格知识库 → 设置相似度阈值、权重及拼装策略（如按召回数量、最大拼装长度）→ 发布后生效 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。  
- **反馈优化任务**：调用 `/prompt-feedback-optimize` 相关接口（或通过控制台），上传初始 Prompt、样例数据（5–10 条）、评测数据（≥20 条），启动多轮优化 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)。  

## 限制和注意事项

- **地域限制**：所有 Prompt 功能（模板、优化、样例库迁移）仅支持华北2（北京）地域，跨地域调用将失败。  
- **模板字符上限**：控制台编辑器最大支持 6144 字符，超长内容需在 SDK 或 API 中处理。  
- **样例库已弃用**：Prompt 样例库功能自文档发布日起停止维护，存量应用必须迁移至 RAG 表格库，否则无法继续使用 [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)。  
- **[Token](../concepts/token.md) 成本敏感**：RAG 表格库注入的召回内容会显著增加输入 Token，公式为：`总输入 Token ≈ 用户查询 Token + 召回样例总 Token + 系统指令 Token`；需权衡 `recall_count` 与效果 [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)。  
- **数据隐私**：Prompt 自动优化过程不存储用户输入，亦不用于模型训练，符合阿里云数据隐私政策 [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)。

## 来源文档

- [Prompt模板概述](../../raw/application-user-guide/prompt/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/prompt/prompt-custom-template.md)
- [使用Prompt样例库优化模型输出](../../raw/application-user-guide/prompt/prompt-sample-optimization.md)
- [Prompt 样例库迁移到 RAG 表格库](../../raw/application-user-guide/prompt/prompt-sample-optimization/migrate-sample-library-prompt-to-rag-table-library.md)
- [Prompt自动优化](../../raw/application-user-guide/prompt/optimize-prompt.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/prompt/prompt-feedback-optimization.md)


