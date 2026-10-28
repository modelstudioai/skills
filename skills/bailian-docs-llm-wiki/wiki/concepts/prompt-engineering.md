# Prompt 工程

Prompt 工程是系统性设计、优化与管理大语言模型输入指令（Prompt）的方法论与实践体系，旨在通过结构化框架、模板化复用、样例驱动迭代和自动化增强等手段，提升模型输出的准确性、一致性、可控性与业务适配度。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台中，Prompt 工程不是静态文本编写，而是贯穿 AI 应用全生命周期的可工程化能力：

- **智能体（Agent）构建**：系统提示词（System Prompt）是 Agent 的“大脑设定”，需结合 ICIO/CRISPE/RASCEF 等内置框架进行角色定义、约束注入与步骤拆解；Agent 2.0 还支持将 Prompt 与工具（知识库、MCP、Connector）协同编排，实现“指令+上下文+能力”的联合调度。

- **工作流（Workflow）节点配置**：大模型节点、意图分类节点等均依赖 Prompt 驱动。开发者可通过预置模板快速启动，或自定义模板绑定变量（如 `${user_query}`、`${kb_result}`），再通过 `variables` 参数动态填充，实现多分支、多数据源的条件化生成。

- **RAG 增强场景**：Prompt 不再孤立存在，而是与 `context.knowledge_base_ids` 深度耦合。典型做法是：在 Prompt 中显式声明“请严格依据以下检索结果回答”，并配合 `has_thoughts=true` 调试检索片段是否被有效引用，确保 RAG 输出可追溯、可验证。

- **反馈驱动优化**：当业务效果未达预期时，可使用“Prompt 反馈优化”功能——上传 ≤100 条真实输入-输出样例（.xlsx），系统自动学习语义模式与格式偏好，产出更贴合业务逻辑的新 Prompt，并支持一键保存为模板或直接部署为智能体应用。

- **API/SDK 集成**：所有 Prompt 相关操作均可编程化：调用 `ListPromptTemplates` 获取模板列表，`GetPromptTemplate` 拉取内容与 `variables` 结构，程序内完成安全变量替换后，再作为 `prompt` 或 `messages[0].content` 提交至模型 API。

> ⚠️ 注意：Prompt 样例库功能已下线，历史引用应统一迁移至 RAG 表格库；所有 Prompt 功能仅支持华北2（北京）地域。

## 关键参数和配置

| 参数 | 作用 | 开发者须知 |
|------|------|------------|
| `promptTemplateId` | 模板唯一标识符 | 预置模板 ID 固定（如 `sys-text-summary-v1`），自定义模板 ID 创建后返回，用于后续渲染与调用 |
| `variables` | 模板中声明的占位符集合（如 `["${topic}", "${style}"]`） | 必须在渲染时全部提供值，缺失任一变量将导致 `400 Bad Request` |
| `workspaceId` | 业务空间 ID | 所有 Prompt 操作必需，跨 workspace 不可见；需通过控制台或 API 显式传入 |
| `has_thoughts=true` | 启用调试模式 | 返回 `thoughts` 字段，含检索来源、推理链路、工具调用过程，**仅用于开发验证，生产环境禁用** |
| `max_tokens`（模型调用层） | 控制输出长度上限 | 受所选模型最大输出 token 限制（如 Qwen-Max 为 8192），超出将被截断 |

## 面向开发者，简洁实用

- ✅ **起步最快**：直接使用预置模板（`ListPromptTemplates?type=System`），复制后微调变量即可上线。  
- ✅ **复用最强**：自定义模板支持跨应用共享，一个 `customer-service-reply` 模板可同时用于智能体回复、工单摘要、邮件生成等多个 Workflow 节点。  
- ✅ **迭代最稳**：对线上效果差的 Prompt，优先走“反馈优化”路径（上传真实样例），而非人工盲调；自动优化适合冷启动快速提效。  
- ✅ **集成最简**：模板渲染 = `GET /prompt-templates/{id}` + 字符串替换（推荐使用 `String.replaceAll()` 或模板引擎），无需额外 SDK。  
- ❌ **避坑提示**：勿在 Prompt 中硬编码敏感信息；勿依赖已下线的样例库；勿跨地域调用 Prompt 接口（仅华北2可用）。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [agent context](../guides/agent-context.md)
- [application support](../guides/application-support.md)


