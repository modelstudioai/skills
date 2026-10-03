# 函数调用

函数调用（Function Calling）是百炼平台中大模型与外部能力协同执行任务的核心机制，指模型在推理过程中，基于用户输入和上下文，自主识别需调用的工具（Tool）、技能（Skill）或插件（Plugin），并生成结构化调用请求（含工具 ID、参数等），由平台运行时安全执行、捕获结果，并将返回值注入后续推理循环。该机制实现了“思考—决策—行动—观察”的闭环，是构建自主智能体（Agent）和复杂工作流的基础能力。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口，而是贯穿多个能力层的统一抽象，具体体现为以下三类实践方式：

- **Managed Agents 中的自动工具调用**：当创建智能体时配置 `tools`（如 `bash`、`web_search`）、`mcp_servers` 或绑定 `skills`，模型会在对话中自主决定是否调用、调用哪个工具/技能，并传入参数。平台自动完成沙箱执行、结果解析与上下文注入，开发者无需编写调用逻辑。
  
- **Application Call（应用调用）中的显式能力扩展**：在调用已发布的智能体应用时，可通过 `rag_options`（知识库检索）、`memory_id`（[长期记忆](memory.md)）等参数触发平台内置函数；若应用已集成插件或 Skill，这些能力也会在模型推理中被自动纳入函数调用候选集。

- **Plug-in 与 Skill 的标准化接入**：插件（Plugin）和技能（Skill）本质是函数调用的两种封装形态——插件面向通用 API 封装（支持鉴权、参数映射、多模态输入），Skill 面向 Python 逻辑封装（文件处理、数据转换等）。二者均通过 `tool_id` 唯一标识，在模型输出的 `tool_calls` 字段中被引用，由平台统一调度执行。

> ✅ 关键区别：Managed Agents 和 Application Call 是**运行时环境**，负责触发、执行、编排函数调用；而 Plug-in 和 Skill 是**可调用单元本身**，提供具体功能实现。

## 关键参数和配置

函数调用行为由以下关键参数控制，开发者需根据使用场景合理配置：

| 参数 | 所属场景 | 说明 | 推荐值 |
|------|----------|------|--------|
| `tool_choice` | Managed Agents API（`/v1/agents/{id}/chat`） | 控制模型是否及如何选择工具：<br>• `"auto"`：模型自主决策（默认）<br>• `"none"`：禁用调用<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制指定工具 | `"auto"`（生产推荐）；调试时可用 `"none"` 快速验证基础响应 |
| `tools` | Managed Agents / Plug-in / Skill 配置 | 工具列表声明，格式为 OpenAI 兼容的 `tools` 数组，包含 `type`、`function.name`、`function.description`、`function.parameters`（JSON Schema） | `description` 必须精准描述用途与边界，直接影响调用准确率 |
| `tool_id` | Plug-in / Skill 元信息 | 插件或技能的全局唯一标识符，用于在 `tools` 列表和模型输出中引用 | 从控制台复制，避免手写错误（如 `calculator`, `pdf-parser`） |
| `biz_params` / `user_defined_params` | Plug-in API 调用 | 向插件透传业务参数（如用户 ID、会话上下文），绕过模型参数抽取，提升稳定性和安全性 | 敏感参数（如 token）必须通过此方式传入，禁止写入 `description` |
| `permission_policy` | Managed Agents 工具配置 | 控制工具调用权限策略：<br>• `"always_allow"`：无条件允许（适合 `read`/`write` 等安全操作）<br>• `"always_ask"`：每次调用前向用户确认（适合 `bash`/`web_search` 等高风险操作） | 按最小权限原则配置，生产环境慎用 `"always_allow"` |

## 面向开发者，简洁实用

- **不要手动解析 `tool_calls`**：百炼平台自动完成工具调用、执行、结果注入。你只需关注 `tools` 声明是否完整、`description` 是否准确、`tool_id` 是否匹配。
- **调试优先级**：若函数调用未触发，按顺序检查：① `tool_choice` 是否为 `"auto"`；② `tools` 是否已正确声明且 `name` 与 `tool_id` 一致；③ `description` 是否包含足够触发关键词（如“计算”“搜索”“解析PDF”）；④ 模型是否支持该能力（如 `qwen-turbo` 支持插件，但 `qwen-vl-plus` 不支持 `code_interpreter`）。
- **安全第一**：禁止在 Skill 代码中硬编码密钥或发起外网请求；插件鉴权参数必须通过 `biz_params` 传入；敏感工具（如 `bash`）务必设 `permission_policy: always_ask`。
- **性能提示**：单次调用最多触发 3 次函数调用（含嵌套），超限将中断执行。复杂流程建议拆分为多个智能体协作或改用工作流节点编排。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)
- [plug in](../guides/plug-in.md)
- [skill](../guides/skill.md)


