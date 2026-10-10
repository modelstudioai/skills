# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的关键能力。它使大模型从“纯文本生成器”升级为“可执行智能体”，支持动态接入天气查询、代码执行、文件处理、数据库操作等真实世界能力，是构建生产级 AI 应用的核心横切机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用并非单一功能模块，而是贯穿多个平台能力层的统一协议行为，具体体现为以下四类场景：

- **插件（Plug-in）场景**：面向轻量、确定性工具（如 `weather`、`web_search`），通过 `tools` 数组声明 OpenAPI 3.0 schema，在 `/v1/chat/completions` 请求中启用。模型返回 `tool_calls` 后，开发者需同步调用对应服务并回传结果，形成“推理→调用→反馈→再推理”的闭环。适用于单轮决策明确、延迟敏感的任务。

- **Managed Agents 场景**：面向长时、多步、状态化任务（如数据分析、自动化文档处理），函数调用在沙箱容器内自主执行。内置工具（`bash`、`read`、`web_fetch`）与 MCP/Skill 工具统一注册为 `tool`，由 Agent 运行时自动调度、管理生命周期、挂载文件/密钥、记录事件流。支持中断续接与可观测追踪。

- **LLM Application（工作流/智能体）场景**：作为低代码编排的原子能力单元。在工作流中，函数调用以“工具节点”形式存在，可与其他节点（条件判断、循环、知识库）自由组合；在 Agent 2.0 中，函数调用与知识库检索统一抽象为“工具”，由模型自主规划调用顺序与参数，完整支持“规划-执行-反思”链路。

- **Skill 与 MCP 场景**：提供标准化封装接口。Skill 将函数调用逻辑封装为带版本号的可复用服务（`skill_id`），支持 JSON Schema 输入约束与异步执行；MCP 则定义跨平台工具通信协议（Streamable HTTP），屏蔽底层差异，使同一工具（如 `WebSearch`）可在智能体、工作流、CLI、IDE 等多环境一致调用。

> ✅ 共同本质：所有场景均依赖模型输出符合约定格式的 `tool_calls`（含 `name` 和 `arguments`），平台或开发者负责解析、执行、注入结果，最终扩展模型能力边界。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 | 示例 |
|------|----------|------|------|------|
| `tools` | 插件、Managed Agents、工作流、Agent 2.0 | array | 工具定义列表，每个元素为含 `name`、`description`、`parameters`（JSON Schema）的对象 | `[{"name": "get_weather", "description": "获取指定城市天气", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}}]` |
| `tool_choice` | 插件、Agent 2.0 | string / object | 控制模型是否及如何选择工具：`"auto"`（默认）、`"none"` 或 `{ "type": "function", "function": { "name": "xxx" } }` | `"auto"` 或 `{"type": "function", "function": {"name": "get_weather"}}` |
| `tool_config` | 插件 | object | 高级配置，如 `{"parallel": true}` 启用并行调用（仅部分模型支持） | `{"parallel": true}` |
| `stream` | Skill | boolean | 是否启用 SSE 流式响应 | `true` |
| `timeout` | Skill | integer | 单次执行超时（秒），范围 5–300 | `60` |
| `mcp_url` | MCP | string | 外部 MCP 服务调用地址 | `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp` |

⚠️ 注意事项：
- `tools` 中 `name` 必须全小写、仅含字母数字和下划线，且不能与平台保留字冲突；
- 单次请求最多声明 20 个工具，最多触发 5 次嵌套调用；
- 所有工具调用默认超时 10 秒（插件）或由 Skill/MCP 自定义（`timeout`），超时后模型不重试，需应用层容错；
- 工具返回内容计入模型上下文，长响应可能被截断，建议服务端压缩或分页。

## 面向开发者，简洁实用

- **快速上手三步法**：  
  1️⃣ **定义工具**：用 OpenAPI 3.0 或 JSON Schema 描述能力（必填 `name`、`description`、`parameters`）；  
  2️⃣ **发起请求**：在 API 请求体中传入 `tools`（+ 可选 `tool_choice`），调用 `/v1/chat/completions` 或工作流/Agent 接口；  
  3️⃣ **处理响应**：检查 `finish_reason === "tool_calls"`，解析 `message.tool_calls`，按 `name` 调用服务，将结果以 `role: "tool"` 消息回传（插件/Agent）或直接返回（Skill/MCP）。

- **调试建议**：  
  - 使用 `tool_choice: "none"` 强制禁用调用，验证基础推理是否正常；  
  - 开启 `enable_thinking: true`（Agent 2.0）或 `temperature: 0` 观察模型规划逻辑；  
  - 查看平台日志中的 `tool_call_output` 事件（Managed Agents）或 `tool_calls` 响应字段，确认参数生成准确性。

- **生产提示**：  
  - 敏感参数（如 API Key）严禁硬编码在 `tools` schema 中，应通过 Vault 注入（Managed Agents）或 MCP KMS 加密（MCP）；  
  - 对高并发场景，优先使用 `tool_config.parallel: true`（插件）或工作流批处理节点控制资源；  
  - 技术选型参考：简单工具 → 插件；复杂沙箱任务 → Managed Agents；复用封装 → Skill；跨平台集成 → MCP。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [skill](../guides/skill.md)
- [model context protocol](../guides/model-context-protocol.md)


