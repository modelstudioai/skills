# agent legacy

`agent legacy` 指百炼平台已归档的旧版智能体能力体系（Agent 1.0 / Flow Agent），基于提示词驱动、支持零代码接入知识库（RAG）与插件（Plugin），适用于需快速构建具备外部工具调用能力的对话式应用的场景。该体系仅在旧版控制台维护，新版控制台默认启用 Agent 2.0 架构，开发者应优先评估迁移可行性。

## 支持的模型与功能

- **模型支持**：仅限千问系列公开模型（如 `qwen-plus`、`qwen-max`）及用户自定义部署的兼容模型；不支持非千问系第三方模型或部分新发布的长上下文模型（如 `qwen2-72b-instruct-1m`）。模型选择在旧版控制台「应用配置」页完成，详见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。
- **核心能力**：
  - **知识库（RAG）**：支持对接百炼知识库服务，检索结果自动注入模型上下文；检索文本计入输入 token，需手动控制切片长度以避免超限。
  - **插件（Plugin）**：支持调用平台预置插件（如代码解释器、文生图）及自定义 HTTP 插件；自定义插件有严格 5 秒超时限制。
  - **[长期记忆](../concepts/long-term-memory.md)**：支持会话级记忆存储，内容不计费但会占用 prompt 上下文。

> **注意**：文档 3 中提及的 Prompt 模板功能虽属 `agent legacy` 生态，但其控制台入口（`https://bailian.console.aliyun.com/flow-agent/prompt-manage`）和 API 路径均指向旧版 Flow Agent 后端，而文档 4 中“基于 Prompt 工程创建”所依赖的 ICIO/CRISPE/RASCEF 框架在新版 Agent 2.0 中已被重构为更轻量的指令模板机制，二者不兼容。

## 关键参数

| 参数名 | 说明 | 取值范围/约束 | 来源 |
|--------|------|----------------|------|
| 最长回复长度 | 模型生成内容的最大 token 数（不含 prompt） | 因模型而异，`qwen-plus` 默认 4096 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| 携带的上下文轮数 | 输入模型的历史对话轮数上限 | 通常 5–20 轮，过高易触发上下文截断 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| 温度系数（temperature） | 控制输出随机性 | `[0, 2)`，0 表示确定性输出 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| 推理模式 | 是否启用结构化推理（如思维链） | 仅部分模型支持，不可在旧版控制台显式关闭 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |

## 使用方式

- **控制台创建**：必须通过[旧版百炼控制台](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center) → 「应用管理」→ 「智能体应用」创建；新版控制台仅提供跳转入口（底部「旧版 Agent 创建入口」）。
- **Prompt 管理**：
  - 系统提示词可直接在应用配置中编辑，支持变量占位符（如 `${topic}`）；
  - 预置/自定义 Prompt 模板统一在 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage) 页面维护，创建后可通过「更多 → 创建应用」一键填充至智能体提示词区；
  - 模板变量渲染逻辑由前端完成，最大字符限制为 6144（见 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)）。
- **Prompt 优化**：支持基于输入-输出样例的自动优化，需在「提示词管理」→ 「反馈优化」分类下新建优化包，上传样例数据（5–10 条）与评测数据（≥20 条），由 `qwen-max` 模型驱动多轮迭代（见 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)）。

## 限制和注意事项

- **地域与可用性**：所有 `agent legacy` 功能（含 Prompt 模板、反馈优化）**仅限华北2（北京）地域**，其他地域控制台不可见或返回 404（见 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) 和 [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md) 开头强调）。
- **API 与 SDK 限制**：
  - 不支持通过 OpenAPI 直接创建/管理智能体应用（仅支持 Assistant API 创建类智能体应用，但**不支持控制台管理**）；
  - Prompt 模板相关 API（如 `ListPromptTemplates`, `GetPromptTemplate`）路径均为 `/api/bailian/2023-12-29/...`，版本号硬编码，无向后兼容承诺。
- **计费关键点**：
  - 知识库检索文本、[长期记忆](../concepts/long-term-memory.md)内容均计入模型输入 token，产生模型调用费用；
  - 自定义插件调用本身不额外计费，但若插件内部调用第三方 API（如天气服务），费用由第三方收取；
  - 应用未发布状态下调试不产生费用，**发布是调用前提**（见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)）。
- **弃用风险**：该体系已明确标记为「旧版」，控制台界面持续引导用户迁移至新版 Agent；官方不再新增功能，仅维持基础可用性与安全更新。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


