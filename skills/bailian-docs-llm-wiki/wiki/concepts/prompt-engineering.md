# Prompt 工程

Prompt 工程是系统性设计、验证、优化和复用提示词（Prompt）的方法论与实践体系，旨在通过结构化表达任务目标、角色设定、上下文约束与输出规范，显著提升大模型在特定业务场景下的准确性、一致性与可控性。它不是一次性文本编写，而是涵盖模板管理、变量注入、自动优化、效果评测与迭代演进的全生命周期过程。

## 在百炼平台的不同场景中，这个概念如何使用

- **模板化 Prompt 管理**：在控制台「提示词管理」中，可基于预置模板（如文案润色、摘要抽取）快速启动，或使用 ICIO/CRISPE 等工程框架创建自定义模板；所有模板统一通过 `promptTemplateId` 标识，支持跨应用复用。
- **智能体（Agent）构建**：无论是 Agent 1.0（Flow Agent）还是 Agent 2.0，Prompt 是定义角色、指令逻辑与输出格式的核心载体；新版 Agent 2.0 中，Prompt 与工具调用协同，共同构成“规划-执行”链路的基础输入。
- **工作流（Workflow）编排**：在大模型节点中，Prompt 可作为 `system` 或 `user` 消息直接传入；支持通过变量绑定（如 `${query}`）动态注入上游节点输出，实现上下文感知的流程化生成。
- **RAG 增强场景**：Prompt 与知识库检索结果协同工作——知识片段被自动拼接至 Prompt 的上下文区，开发者只需专注设计引导模型融合知识的指令（如“请严格依据以下文档内容回答…”），无需手动拼接文本。
- **自动优化与反馈驱动迭代**：通过「Prompt 自动优化」功能，输入原始描述即可获得结构更优、角色更清晰、指令更明确的版本；旧版 Flow Agent 还支持基于 SFT 样例数据的反馈优化，以评测数据为标尺自动筛选最优 Prompt。

> ⚠️ 注意：原 Prompt 样例库（少样本注入）功能已于 2024 年下线，官方推荐迁移至 RAG 表格库实现更稳定、可扩展的知识增强方式。

## 关键参数和配置

| 参数 | 说明 | 使用位置 |
|------|------|----------|
| `promptTemplateId` | 模板唯一标识符，区分预置（`type=System`）与自定义模板 | 控制台模板卡片、API 调用（`GetPromptTemplate`）、工作流节点配置 |
| `variables` | 模板中声明的占位符列表（如 `["topic", "tone"]`），运行时需按名填充 | `GetPromptTemplate` 接口返回，不可动态增删，须在模板创建时明确定义 |
| `workspaceId` | 业务空间 ID，所有 Prompt 操作必需，且仅华北2（北京）地域有效 | API 请求头或请求体，需提前通过控制台或 OpenAPI 获取 |
| `has_thoughts=true` | 启用调试模式，返回 `thoughts` 字段，含 RAG 召回详情、工具调用决策链等 | 仅适用于智能体应用 API 调用，用于诊断上下文注入效果 |
| `context_sources`（YAML 配置） | 显式声明上下文来源（如知识库、Memory、Connector），由平台自动注入 Prompt | Agent 配置文件中，与 Prompt 指令协同生效，不替代 Prompt 本身 |

## 面向开发者，简洁实用

- ✅ **起步建议**：从预置模板开始 → 复制为自定义模板 → 修改变量与指令 → 在工作流中绑定变量调用。
- ✅ **调试技巧**：开启 `has_thoughts=true` 查看实际注入的上下文与召回内容；用 `GetPromptTemplate` + 手动变量填充，验证最终 Prompt 字符串是否符合预期。
- ✅ **最佳实践**：
  - Prompt 模板中避免硬编码业务数据，全部通过 `variables` 抽离；
  - 图片生成类 Prompt，务必选择「图片生成」类型模板，并分离正向/负向提示词；
  - 超长上下文场景，优先使用 `context_sources` 注入知识，而非将全文塞入 Prompt 字符串；
  - 新项目禁用已下线的样例库，改用 RAG 表格库 + 显式 Prompt 指令（如“根据以下表格数据回答…”）。
- ❌ **避坑提醒**：
  - 预置模板不可编辑；自定义模板修改后需重新发布应用才生效；
  - 所有 Prompt 操作仅支持华北2（北京）地域，跨地域 `workspaceId` 将失败；
  - 控制台输入框上限 6144 字符，超长 Prompt 请优先拆解为变量+模板结构。

> 提示：Prompt 工程不是“调参”，而是“建模”——把业务逻辑翻译成模型可理解的语言。持续收集 bad case、分析 `thoughts` 输出、小步快跑迭代模板，才是高效落地的关键。

## 关联主题页

- [prompt](../guides/prompt.md)
- [llm application](../guides/llm-application.md)
- [agent legacy](../guides/agent-legacy.md)
- [application use cases](../guides/application-use-cases.md)
- [agent context](../guides/agent-context.md)


