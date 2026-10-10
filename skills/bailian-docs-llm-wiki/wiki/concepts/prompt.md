# Prompt 工程

Prompt 工程是系统化设计、验证、优化和管理提示词（Prompt）的方法论与实践体系，旨在通过结构化模板、上下文增强、反馈迭代与可观测评估等手段，提升大语言模型在特定任务中的输出准确性、一致性、可控性与可维护性。它不是一次性指令编写，而是贯穿 LLM 应用全生命周期的工程化能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础模型调用**：直接向 `ChatCompletion` 等接口提交高质量 Prompt，适用于简单问答、文案生成等轻量任务；推荐结合 `temperature`、`top_p` 等参数协同调控输出稳定性。
- **智能体（Agent）与工作流（Workflow）**：Prompt 作为系统提示词（System Prompt）或节点级指令嵌入 Agent 2.0 的规划链路或工作流的大模型节点中，配合工具描述、记忆配置与思考模式（`enable_thinking`）实现多步推理与反思优化。
- **Skill 封装**：Prompt 与模型、工具、后处理逻辑共同封装为可复用的 Skill 单元，通过 `skill_id` 被工作流或外部系统调用，实现 Prompt 的版本化、灰度发布与跨应用共享。
- **RAG 应用构建**：Prompt 与知识库检索结果动态组合（如通过 `context` 变量注入），替代已停用的 Prompt 样例库；需配合 RAG 表格库的 `recall_count` 参数控制上下文密度，平衡信息量与噪声。
- **Agenteval 持续优化闭环**：基于线上 Trace 沉淀真实 query/response 对，通过 Agenteval 的「调试窗口」输入人工反馈，驱动大模型自动生成优化版 Prompt；支持多版本对比测试，但采纳后需手动发布生效，确保变更受控。

> ⚠️ 注意：旧版 Prompt 样例库功能已下线，所有新项目必须使用 RAG 表格库或 Agenteval 的反馈优化路径替代。

## 关键参数和配置

| 参数 | 说明 | 典型值/约束 | 使用场景 |
|------|------|--------------|-----------|
| `promptTemplateId` | 预定义 Prompt 模板唯一 ID | 字符串，由控制台或 API 创建生成 | 模板化调用（如营销文案生成） |
| `variables` | 模板中声明的占位符变量名列表（如 `["topic", "tone"]`） | 由 `GetPromptTemplate` 接口返回，不可手动指定 | 动态填充模板内容 |
| `has_thoughts` | 是否在响应中返回推理过程（如 RAG 召回片段、思考链） | `true` / `false`；调试时设为 `true` | 问题定位与效果归因 |
| `recall_count` | RAG 表格库召回知识片段数量 | 默认 `5`，最大 `10` | 控制上下文长度与相关性精度 |
| `workspaceId` | 业务空间 ID，用于权限隔离与资源归属 | 必填，需通过控制台或 API 获取 | 所有 Prompt 相关 API 调用必需 |
| `enable_thinking` | 启用模型内部思考模式（Agent 2.0 / 大模型节点特有） | `true` / `false`；影响反思质量与输出结构化程度 | 复杂任务规划、结构化 JSON 输出 |

## 面向开发者，简洁实用

- ✅ **起步建议**：从控制台「提示词」页面 → 「基于 Prompt 工程创建」模板入手，选用 ICIO（Identity, Context, Instruction, Output）等成熟框架快速生成结构化 Prompt 草稿。
- ✅ **调试必做**：调用时始终设置 `has_thoughts=true` 查看实际输入给模型的完整 Prompt（含变量替换、RAG 注入内容），避免“黑盒幻觉”。
- ✅ **上线前验证**：使用 Agenteval 创建评测集（含典型 query + reference_response），运行多轮评测确认关键指标（如格式合规率、术语准确率）达标后再发布。
- ✅ **版本管理**：Prompt 模板、Skill、Agent 均支持版本号（`version`），生产环境务必显式指定版本（如 `v2.1.0`），禁止依赖 `latest`。
- ❌ **避免踩坑**：不要硬编码 Prompt 字符串到业务代码中；不使用已废弃的样例库字段；不跳过 Agenteval 的“重新调试验证”步骤即发布优化版 Prompt。

Prompt 工程的本质是让模型行为可预期、可测量、可演进。在百炼平台，它已深度融入模板、RAG、Agenteval、Agent 和 Skill 等核心能力，开发者应将其视为与模型选型、API 调用同等重要的基础设施来建设与维护。

## 关联主题页

- [prompt](../guides/prompt.md)
- [agenteval](../guides/agenteval.md)
- [use cases](../guides/use-cases.md)
- [llm application](../guides/llm-application.md)
- [skill](../guides/skill.md)


