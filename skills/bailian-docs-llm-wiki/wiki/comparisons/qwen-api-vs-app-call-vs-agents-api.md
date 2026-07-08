# Qwen API、应用调用与托管智能体 API 对比

百炼平台提供了多种 API 接入方式，开发者在集成大模型能力时常面临选型困惑：是直接调用 Qwen 模型 API，还是通过应用调用 API 使用已编排好的智能体/工作流，亦或是采用 Managed Agents API 获得平台全托管的智能体运行时？本文从接口定位、协议兼容性、会话管理、工具能力、计费模式等维度进行系统对比，帮助开发者根据实际场景做出技术选型。

## 定位差异

- **Qwen API**：直接调用 Qwen 系列大语言模型，获取文本生成能力。开发者自行管理 [prompt](../guides/prompt.md)、上下文和工具调用逻辑，灵活度最高。
- **应用调用 API**：调用在百炼控制台中已创建并发布的智能体或工作流应用。应用内部已封装模型选择、知识库检索、插件调用等编排逻辑，开发者只需传入用户输入即可获取最终结果。
- **Managed Agents API**：平台全托管的智能体运行时，提供 Agent、Session、Environment、Skill、File 等资源抽象。由平台负责会话状态机、沙箱执行、工具调用与事件流推送，适合需要长期运行、多步工具调用的复杂场景。

## 关键维度对比

| 维度 | Qwen API | 应用调用 API | Managed Agents API |
|------|----------|-------------|-------------------|
| **定位** | 模型级调用，直接访问 Qwen 系列模型 | 应用级调用，调用已编排好的智能体/工作流 | 平台托管智能体运行时，全生命周期管理 |
| **兼容协议** | OpenAI Chat Completions、OpenAI Responses、Anthropic Messages、DashScope 原生 | OpenAI Responses（兼容模式）、DashScope | 百炼原生 REST API |
| **API 端点** | `POST /compatible-mode/v1/chat/completions` 等 | `POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` 或 `POST /api/v1/apps/{APP_ID}/completion` | `POST /api/v1/agentstudio/sessions/{session_id}/events` 等 |
| **认证方式** | [API Key](../concepts/api-key.md)（`Authorization: Bearer`） | [API Key](../concepts/api-key.md) + APP ID（+ 可选 Workspace ID） | [API Key](../concepts/api-key.md) + Workspace ID |
| **模型选择** | 请求体 `model` 字段指定任意 Qwen 模型 | 控制台配置，调用时无需指定模型 | Agent 创建时配置模型 |
| **会话管理** | 调用方自行维护（Responses 接口除外） | DashScope API 通过 `session_id` 自动维护；Responses API 需传完整历史 | 平台全托管，Session 状态机自动驱动 |
| **工具/插件** | Responses 接口内置联网搜索、代码解释器、网页提取；其他接口需自定义 | 控制台可视化编排插件、知识库、工具 | Skill（zip 包上传）+ Environment 沙箱执行 |
| **[多模态](../concepts/multimodal.md)支持** | 需选用 VL 系列模型 | Responses API 支持图像和文件输入 | 通过 File 资源挂载到 Session |
| **[流式输出](../concepts/streaming.md)** | 支持（`stream=true`） | 支持（`stream=true`） | SSE 事件流（`GET .../events/stream`） |
| **[异步调用](../concepts/async-invocation.md)** | 不支持 | Responses API 支持（`background=true`），DashScope 暂不支持 | 原生异步，Session 状态机驱动 |
| **支持地域** | 多地域 | 仅华北2（北京） | 仅 cn-beijing |
| **SDK 支持** | OpenAI SDK、Anthropic SDK、[DashScope SDK](../concepts/dashscope-sdk.md) | OpenAI SDK、[DashScope SDK](../concepts/dashscope-sdk.md) | 百炼原生 SDK / HTTP |
| **配置方式** | 纯代码，请求参数控制 | 控制台可视化编排 + API 调用 | API 全程管理（Agent/Environment/Session/Skill） |

## 适用场景建议

### 选择 Qwen API

- 需要直接、细粒度地控制模型推理参数（temperature、top_p 等）。
- 已有基于 OpenAI 或 Anthropic SDK 的应用，希望低成本迁移到百炼平台。
- 构建自定义的 RAG、Agent 框架，模型调用只是其中一环。
- 对 [prompt](../guides/prompt.md) 工程有深度需求，需要完整掌控输入输出。

### 选择应用调用 API

- 已在百炼控制台完成智能体或工作流的可视化编排，希望通过 API 将其集成到业务系统。
- 需要使用控制台配置的知识库检索、插件、工作流节点等平台能力，不想在代码中重新实现。
- 团队中非开发人员负责应用逻辑编排，开发人员只负责 API 集成。
- 需要快速上线，应用逻辑变更通过控制台完成而非修改代码。

### 选择 Managed Agents API

- 需要平台全托管的智能体运行时，不想自行管理会话状态和工具执行环境。
- 智能体任务涉及多步工具调用、代码执行、文件读写，需要沙箱环境保障安全。
- 希望通过 API 动态创建和管理多个智能体，实现多 Agent 协作。
- 需要细粒度的事件流（SSE）来追踪智能体执行过程中的每一步操作。
- 有自定义工具（Skill）需要安全审核后挂载，要求版本锁定和隔离。

## 选型决策参考

1. **"我只需要一个模型回答问题"** — 选 Qwen API。最简单直接，兼容主流 SDK。
2. **"我已在控制台搭好应用，想 API 接入"** — 选应用调用 API。零编排代码，改逻辑只需改控制台配置。
3. **"我需要平台帮我管理 Agent 的执行环境和工具调用"** — 选 Managed Agents API。平台托管状态机、沙箱和事件流，适合复杂任务。
4. **迁移成本优先** — Qwen API 的 OpenAI/Anthropic 兼容接口迁移成本最低；应用调用 API 也提供 OpenAI 兼容模式。
5. **功能完整度优先** — Qwen API 的 DashScope 原生接口参数最丰富；Managed Agents API 的资源模型最完整。

## 注意事项

- Qwen API 的兼容接口可能不暴露 DashScope 原生的全部参数，如需最全功能建议使用 DashScope 接口。
- 应用调用 API 要求先在控制台创建并发布应用，APP ID 只能通过控制台手动获取。
- Managed Agents API 当前仅支持 cn-beijing 地域，Skill 上传后需通过安全扫描才能挂载。
- 三种 API 的计费方式均基于 token 消耗，但应用调用和 Managed Agents 可能涉及额外的平台资源费用（如沙箱、存储），请参考官方定价文档。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [managed agents api](../api/managed-agents-api.md)


