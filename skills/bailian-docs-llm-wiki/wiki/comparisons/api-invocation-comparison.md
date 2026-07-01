# Qwen API vs 应用调用 vs 托管智能体API对比

百炼平台为开发者提供了三种主要的 API 调用方式：直接调用 Qwen 系列大模型（Qwen API）、调用已在控制台编排好的应用（应用调用 API）、以及通过托管智能体运行时管理完整的智能体生命周期（Managed Agents API）。三者在抽象层级、使用复杂度和适用场景上差异显著，本文帮助开发者根据业务需求做出技术选型。

## 核心定位

- **Qwen API**：直接访问基础大模型能力，开发者完全掌控对话编排与工具集成。
- **应用调用 API**：调用控制台已配置好的应用（智能体/工作流），平台负责模型选择、提示词和工具编排。
- **Managed Agents API**：平台托管智能体全生命周期（会话、沙箱、工具执行、事件流），开发者通过 REST 管理资源。

## 关键维度对比

| 维度 | Qwen API | 应用调用 API | Managed Agents API |
| --- | --- | --- | --- |
| **抽象层级** | 模型层（底层） | 应用层（中层） | 运行时层（高层） |
| **调用对象** | Qwen 系列模型 | 控制台编排的应用（APP ID） | 平台托管的 Agent 实例 |
| **兼容协议** | OpenAI / Anthropic / DashScope 原生 | OpenAI Responses / DashScope 原生 | 百炼专有 REST API |
| **Endpoint 示例** | `POST /chat/completions` | `POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | `POST /api/v1/agentstudio/sessions/{id}/events` |
| **认证方式** | [API Key](../concepts/api-key.md) (DASHSCOPE_API_KEY) | [API Key](../concepts/api-key.md) (DASHSCOPE_API_KEY) | [API Key](../concepts/api-key.md)（Bearer [Token](../concepts/token.md)） |
| **必需标识** | model 名称 | APP ID（+ 可选 Workspace ID） | workspace_id + agent_id |
| **对话历史管理** | 调用方自行维护（Responses 接口除外） | OpenAI Responses 模式自动管理；DashScope 模式需自行维护 | 平台托管，通过 Session/Event 机制自动管理 |
| **工具/插件** | Responses 接口内置联网搜索、代码解释器、网页提取；其余需自行定义 | 由控制台应用配置决定，调用时无需关心 | Agent 配置挂载 Skill（zip 包）、Environment（沙箱） |
| **流式输出** | 支持 | 支持（stream=True） | SSE 事件流订阅 |
| **[异步调用](../concepts/async-invocation.md)** | 不支持 | 支持（background=True） | 原生异步：Session 状态机驱动 |
| **[多模态](../concepts/multimodal.md)** | 取决于具体模型能力 | 支持（OpenAI Responses 模式） | 支持（通过 File 资源挂载） |
| **沙箱/执行环境** | 无 | 无（平台内部处理） | 开发者可创建和管理 Environment |
| **版本控制** | 无（指定模型版本即可） | 无 | Agent 自动版本递增，Session 锁定创建时版本 |
| **SDK 兼容** | OpenAI SDK / Anthropic SDK / [DashScope SDK](../concepts/dashscope-sdk.md) | OpenAI SDK / [DashScope SDK](../concepts/dashscope-sdk.md) | 需直接 HTTP 调用或自封装 |
| **迁移成本** | 低（直接复用 OpenAI/Anthropic 代码） | 中（需先在控制台配置应用） | 高（专有 API，需学习资源模型） |

## [计费](../concepts/billing.md)与配额

| 维度 | Qwen API | 应用调用 API | Managed Agents API |
| --- | --- | --- | --- |
| **[计费](../concepts/billing.md)粒度** | [Token](../concepts/token.md) 用量（按模型计价） | [Token](../concepts/token.md) 用量（应用内模型调用） | Token 用量 + 可能的沙箱资源费用 |
| **文件配额** | 无 | 无 | 单文件 20MB，空间总量 100GB，保留 30 天 |

## 适用场景建议

### 选择 Qwen API

- 需要直接控制模型参数（temperature、top_p 等）进行精细调优
- 已有 OpenAI/Anthropic 代码希望低成本迁移到百炼
- 构建自定义 RAG、Agent 框架，需要底层模型能力
- 对工具调用逻辑有完全自主的编排需求

### 选择应用调用 API

- 已在百炼控制台完成应用编排（提示词、知识库、插件），希望快速集成到业务系统
- 团队中有非开发角色负责应用配置，开发者只需调用
- 需要工作流（多步骤串联）能力但不想自行编排
- 希望通过 OpenAI SDK 兼容方式接入已编排好的应用

### 选择 Managed Agents API

- 需要平台托管智能体完整生命周期（创建、会话、工具执行、文件管理）
- 有复杂的工具执行需求，需要安全沙箱环境
- 需要细粒度的会话状态管理和事件流订阅
- 构建多智能体协作系统，需要独立管理每个 Agent 的版本和配置
- 希望将工具包（Skill）作为可复用资产跨智能体共享

## 选型决策路径

1. **是否已在控制台配置好应用？** 是 -> 应用调用 API（最快集成）
2. **是否需要平台托管工具执行沙箱和会话状态机？** 是 -> Managed Agents API
3. **是否需要直接访问模型底层能力并自行编排？** 是 -> Qwen API
4. **从 OpenAI/Anthropic 迁移？** 优先 Qwen API 的兼容接口，迁移成本最低

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [managed agents api](../api/managed-agents-api.md)


