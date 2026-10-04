# 函数调用

函数调用（Function Calling）是百炼平台中大模型与外部能力协同执行任务的核心机制，指模型在推理过程中，根据用户意图自主或按编排逻辑生成结构化工具调用请求（含工具名、参数），由平台统一调度、安全执行并注入结果回上下文，从而突破纯文本生成的边界，实现真实世界操作。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用并非模型原生能力，而是百炼平台在应用层封装的标准化交互范式，其具体形态和触发方式因应用场景而异：

- **智能体（Agent）应用**：模型基于自然语言输入自动规划是否调用工具，并生成符合 Schema 的参数。在 Agent 2.0 架构下，知识库检索、MCP 服务、内置文件工具（如 `read`/`bash`）均统一抽象为“函数”，模型可自主完成「规划–调用–反思」闭环；Managed Agents 进一步将调用纳入沙箱环境，支持多步串联、状态持久化与中断续接。

- **工作流（Workflow）应用**：函数调用以显式节点形式存在（如 MCP 节点、API 节点、插件节点），开发者通过拖拽配置输入参数映射与输出解析规则，实现确定性编排。此时调用不依赖模型决策，而是由流程控制逻辑驱动，适用于需强一致性和可观测性的生产任务。

- **插件（Plug-in）与 MCP 服务**：二者均通过函数调用协议接入。插件需发布为 MCP 服务后方可被调用；MCP 是百炼对函数调用的协议级抽象，定义了工具发现、参数协商、流式响应等标准接口，屏蔽底层实现差异，使 `web_search`、`amap_weather`、自定义 Python 脚本等能力以统一方式被消费。

- **OpenAI 兼容 API（如 `/chat/completions`）**：通过 `tools` 字段声明可用函数列表（含 `function.name` 和 `function.parameters` JSON Schema），模型在 `tool_calls` 字段返回调用意图；开发者需自行处理调用执行与结果注入，平台仅提供协议兼容性支持，不托管执行环境。

> ⚠️ 注意：函数调用本身不直接绑定特定模型，但实际可用性受模型能力影响——例如 `qwen-turbo` 对嵌套 Object 参数支持较弱，`qwen-max` 或 `qwen3.8-plus` 更适合复杂工具链；所有调用均需经平台鉴权、限流与审计，不可绕过百炼网关直连外部服务。

## 关键参数和配置

函数调用的有效性高度依赖以下关键参数，需在应用定义或 API 请求中准确配置：

- **工具声明（`tools`）**：  
  必填。数组形式，每个元素为对象，必须包含：
  - `type`: 固定为 `"function"`；
  - `function.name`: 工具唯一标识符（如 `"web_search"`、`"maps_weather"`），长度 ≤20 字符；
  - `function.description`: 工具功能描述（影响模型识别准确率，不可为空）；
  - `function.parameters`: 符合 JSON Schema 规范的输入参数定义，**Object 类型字段的子属性必须显式声明，不可留空**。

- **调用控制策略（`tool_choice`）**：  
  可选。控制模型调用行为：
  - `"auto"`（默认）：模型自主决定是否及调用哪个工具；
  - `"none"`：禁止任何工具调用；
  - `{"type": "function", "function": {"name": "xxx"}}`：强制指定调用某工具（常用于工作流兜底或确定性场景）。

- **业务透传参数（`biz_params`）**：  
  仅在插件/MCP 场景下使用。用于传递用户级动态参数（如用户 ID、会话 [Token](token.md)）或鉴权凭据，**必须通过该字段传入，不可拼入 `tools` 或 `messages`**。

- **审批策略（`permission_policy`）**：  
  Managed Agents 等托管场景特有。值为 `{"type": "always_allow"}` 或 `{"type": "always_ask"}`（对象格式），决定工具调用是否需人工确认。

- **输入参数映射（工作流节点内）**：  
  非 API 层参数，但在工作流中至关重要：需将上游节点输出（如 `extracted_info.city`）显式绑定到 MCP/API 节点的对应输入字段（如 `city: string`），否则调用将因参数缺失失败。

## 面向开发者，简洁实用

- ✅ **优先使用 MCP**：新项目统一通过 MCP 协议接入工具（官方/三方/自定义），避免重复适配，享受平台级监控、重试与错误归因。
- ✅ **严格校验 Schema**：`parameters` 中每个字段必须有 `description`；Object 类型必填子字段；GET 请求禁用 Object 输入（改用 POST）。
- ✅ **调试从模拟开始**：在控制台使用「测试工具」验证参数构造与响应解析，再集成到应用；观察 `tool_calls` 输出是否符合预期，而非仅关注最终回复。
- ❌ **勿硬编码工具名**：`function.name` 是运行时契约，变更即失效；应通过控制台或 API 获取最新工具 ID。
- ❌ **勿忽略 biz_params**：涉及用户上下文或鉴权的调用，遗漏 `biz_params` 将导致 401 或数据错乱。
- 🚀 **性能提示**：函数调用引入网络延迟，高频小参数调用建议合并；对延迟敏感场景，选用极速模式 MCP 或预热 Managed Agents 环境。

## 关联主题页

- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


