# agent legacy

`agent legacy` 指百炼平台已归档的旧版智能体能力体系（即 Agent 1.0 / Flow Agent），基于提示词驱动、零代码编排，支持 RAG 知识库接入与插件调用。该体系在新版控制台中已逐步被 `Agent 2.0`（基于 MCP 协议与结构化工具调用）替代，但仍在华北2（北京）地域的旧版控制台中完整可用，适用于需快速落地、低代码维护的垂直场景。开发者应优先评估新版 Agent 能力，仅在明确依赖旧版特性（如特定 Prompt 模板管理路径或历史版本兼容性）时使用。

## 支持的模型与功能

- **模型支持**：仅限千问系列公开模型（如 `qwen-plus`、`qwen-max`）及用户自定义部署模型；不支持新版 Agent 的多模型路由、[函数调用](../concepts/function-calling.md)原生模型（如 `qwen2.5-72b-instruct` 的 tool calling 模式）。模型选择与参数配置均在旧版控制台完成，详见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。
- **核心能力**：
  - **知识库（RAG）**：支持连接私有知识库，检索结果直接注入模型上下文；注意检索文本占用输入 token，需协同调整 `最长回复长度` 和 `携带的上下文轮数` 参数。
  - **插件（Plugin）**：调用平台预置工具（如代码执行、天气查询）或自定义插件；所有插件调用超时限制为 **5 秒**，超时将中断流程并返回错误。
  - **Prompt 工程支持**：提供预置模板、自定义模板及基于样例的自动优化三类能力，覆盖文本生成、图片生成等场景，全部功能集中于 [提示词管理](https://bailian.console.aliyun.com/flow-agent/prompt-manage) 页面。

> **注意**：文档 3 和文档 4 均强调“本文档仅适用于华北2（北京）地域”，但文档 2 的快速开始指南未限定地域。实际使用中，若在非北京地域访问旧版控制台，部分 Prompt 模板 API（如 `ListPromptTemplates`）可能返回空列表或报错，此为地域服务隔离导致，非文档矛盾。

## 关键参数

| 参数 | 说明 | 取值范围/约束 | 来源 |
|------|------|----------------|------|
| **最长回复长度** | 模型生成内容的 token 上限（不含系统提示词与历史对话） | 因模型而异，例如 `qwen-plus` 默认 4096，上限 8192 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **携带的上下文轮数** | 输入模型的最大历史对话轮数（每轮含 user/assistant 一对） | 推荐 3–10 轮；轮数过多易触发上下文截断或 token 超限 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **温度系数（temperature）** | 控制输出随机性 | `[0, 2)`，0 表示确定性输出，接近 2 时多样性高但稳定性下降 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |
| **推理模式** | 是否启用模型内置的推理链（Chain-of-Thought）能力 | 仅对支持该能力的模型（如 `qwen-max`）可开启；旧版 Agent 中此项为实验性开关，效果因模型版本而异 | [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md) |

## 使用方式

- **创建与配置**：必须通过[旧版百炼控制台](https://bailian-legacy.console.aliyun.com/cn-beijing/?tab=app#/app-center)创建，新版控制台仅提供跳转入口；配置项包括模型选择、系统提示词、知识库绑定、插件启用等。
- **Prompt 模板集成**：
  - 预置模板可通过控制台“提示词管理”页面的 `··· > 创建应用` 一键填充至智能体提示词框；
  - 自定义模板支持两种创建路径：`自定义创建`（直接输入原始 Prompt）或 `基于 Prompt 工程框架创建`（ICIO/CRISPE/RASCEF），后者需严格按框架字段填写以保障结构完整性，详见 [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)。
- **Prompt 自动优化**：使用 [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md) 功能时，需上传至少 5 条覆盖全分类的样例数据（`样例选择`）及不少于 20 条评测数据（`评测数据`），优化器基于 `千问-Max` 推理模型进行多轮评估选优。

## 限制和注意事项

- **地域限制**：所有 Prompt 模板相关功能（创建、管理、API 调用）仅在华北2（北京）地域可用，跨地域调用会失败。
- **版本与发布**：每个智能体最多保存 10 个发布版本，超出后新版本自动覆盖最早版本；回滚操作（`覆盖当前草稿`）不可逆，需谨慎执行。
- **计费要点**：
  - 知识库检索文本计入模型输入 token，直接增加模型调用费用；
  - 插件调用按所用 MCP 类型计费（如文生图按次），第三方 API 费用由服务商收取；
  - **[长期记忆](../concepts/long-term-memory.md)内容合并入 Prompt 后产生的 token 暂不计费**，但会占用上下文窗口。
- **API 创建限制**：虽支持 Assistant API 创建类似智能体的应用，但此类应用**不支持控制台管理**（无法编辑、发布、查看版本），仅能通过 API 维护，详见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。

## 来源文档

- [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)
- [Prompt模板概述](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-template.md)
- [自定义Prompt模板](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-custom-template.md)
- [基于大模型输入输出样例的Prompt自动优化](../../raw/application-user-guide/agent-legacy/legacy-flow-agent/prompt-feedback-optimization.md)


