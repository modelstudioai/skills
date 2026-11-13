# agent legacy

`agent legacy` 指百炼平台已下线但仍在部分存量应用中运行的旧版智能体能力体系（即 Agent 1.0 / Flow Agent），其核心是基于提示词驱动、零代码接入知识库与插件的轻量级 Agent 架构。该体系不支持多跳规划、工具调用链自动编排或[长期记忆](../concepts/long-term-memory.md)状态管理，适用于对实时性、可解释性和控制粒度要求较高的简单任务场景。新版 Agent（Agent 2.0）已全面替代其底层架构，但旧版配置、API 及调试界面仍保留在华北2（北京）地域的旧版控制台中。

## 支持的模型与功能

- **模型支持**：仅限千问系列公开模型（如 `qwen-plus`、`qwen-max`）及用户自定义部署的兼容模型；不支持 Qwen-VL、Qwen-Audio 等多模态模型。模型需在旧版控制台[应用管理](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)中手动选择，且必须为已开通服务的实例。
- **核心功能**：
  - **知识库（RAG）**：支持连接私有知识库，检索结果直接注入 Prompt 上下文，但不支持分块重排序或混合检索（如关键词+向量）。详情参见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。
  - **插件（MCP）**：仅支持平台预置插件（如天气查询、代码执行）和符合旧版协议的自定义插件；超时限制严格为 5 秒，且不支持插件间依赖调用。
  - **[长期记忆](../concepts/long-term-memory.md)**：仅提供基础会话级上下文轮数控制（通过“携带的上下文轮数”参数配置），无独立存储与语义索引能力；记忆内容计入输入 Token，但暂不计费。

> **注意**：文档 3 和文档 4 均强调“本文档仅适用于华北2（北京）地域”，而文档 2 的快速开始指引中未明确地域限制。实际使用中，旧版 Flow Agent 全链路（含 Prompt 模板 API、反馈优化、控制台入口）**仅在北京地域可用**，其他地域调用将返回 `RegionNotSupported` 错误。此为硬性地域隔离，非配置疏漏。

## 关键参数

| 参数名 | 说明 | 取值范围/约束 | 来源 |
|--------|------|----------------|------|
| **最长回复长度** | 模型生成内容的 token 上限（不含系统提示词与历史对话） | 因模型而异（如 `qwen-plus` 为 8192） | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **携带的上下文轮数** | 输入模型的最大历史对话轮数（每轮含 user/assistant 一对） | 通常 5–20 轮；过高易触发上下文截断 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **温度系数（temperature）** | 控制输出随机性 | `[0, 2)`，推荐值 0.3–0.7 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **推理模式** | 是否启用模型内置的推理增强（如思维链） | 仅对明确标注支持该模式的模型生效；旧版 Agent 中多数模型不可配置 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **Prompt 模板变量** | 在模板中声明的 `${var}` 占位符，用于运行时注入业务数据 | 变量名需为合法标识符；单模板最多支持 100 个变量 | [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) |

## 使用方式

- **控制台创建**：必须通过旧版控制台入口（新版控制台底部“旧版 Agent 创建入口”跳转）创建应用；新控制台无法新建或编辑 Agent 1.0 应用。
- **Prompt 集成**：
  - 可直接在智能体配置页的“系统提示词”区域编写静态 Prompt；
  - 或通过 [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md) 中的“创建应用”快捷操作，将预置/自定义模板内容一键填充至提示词框。
- **API 调用**：
  - 发布后获取 API Key，在调试页或 SDK 中调用 `/v1/agents/{agent_id}/chat` 接口；
  - 请求体需显式传入 `messages`（含历史对话）和 `parameters`（覆盖模型参数）；
  - 若使用 Prompt 模板，需先调用 `GetPromptTemplate` 接口获取模板内容并本地填充变量，再作为 `system_prompt` 提交。
- **自动优化**：通过 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md) 功能，上传输入-输出样例对（`.xlsx`）与评测集，由 `qwen-max` 模型驱动多轮迭代生成高匹配度 Prompt。

## 限制和注意事项

- **地域锁定**：所有功能（包括 Prompt 模板管理、反馈优化、Agent 创建）仅在华北2（北京）地域可用，跨地域调用失败。
- **版本不可迁移**：Agent 1.0 应用无法升级至 Agent 2.0；若需新能力，须在新版控制台重建应用并重新配置知识库、插件及 Prompt。
- **Token 计费透明性**：知识库检索文本、[长期记忆](../concepts/long-term-memory.md)内容、Prompt 模板变量展开后的内容均计入模型输入 Token，但**记忆体内容占用的 Token 暂不计费**（见文档 2 计费说明）。
- **插件超时刚性**：自定义插件响应必须 ≤5 秒，超时即中断且不重试；无熔断或降级机制。
- **模板字符上限**：控制台中编辑 Prompt 模板时，内容最大支持 6144 字符（非 token 数），超出部分被截断且无警告。
- **调试局限性**：模型调试界面仅支持单次问答测试，不支持多轮会话状态保持或插件调用链可视化追踪。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


