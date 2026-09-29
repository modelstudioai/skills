# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具请求，并交由执行层安全调度外部能力的核心机制。它不是简单的 API 转发，而是模型在推理过程中自主决策“何时调用、调用哪个函数、传入哪些参数”的闭环过程，是实现智能体自主性、确定性和可扩展性的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口，而是贯穿多个能力层的统一抽象，具体体现为以下三类实践模式：

- **插件（Plug-in）调用**：面向轻量、标准化能力（如计算器、文生图、实时搜索）。模型根据用户输入自动触发预注册的插件，参数由模型从自然语言中提取并填充。适用于 Assistant API、智能体应用和工作流节点，强调开箱即用与低代码集成。

- **MCP（Model Context Protocol）服务调用**：面向可组合、可托管的工具生态。MCP 将外部服务（如地图、网页爬取、图表生成）封装为符合协议的工具集，模型通过 `tool_choice` 机制自主选择并调用其中某个工具。支持流式响应与错误重试，是构建复杂多步智能体的推荐方式。

- **内置工具（Built-in Tools）调用**：仅限 Managed Agents 运行时环境。模型直接调用平台原生提供的 `bash`、`read`、`web_search` 等沙箱内工具，无需额外配置 URL 或鉴权，所有执行在隔离容器中完成，具备文件读写、联网、代码执行等完整系统级能力。

> ✅ 共同点：三者均由模型自主触发（非人工编排），均依赖准确的工具描述（description）、参数 Schema 和审批策略；  
> ❗ 差异点：插件和 MCP 侧重“外部服务接入”，内置工具侧重“运行时环境能力”，三者不可混用，需按场景选型。

## 关键参数和配置

函数调用的可靠性高度依赖以下核心配置项，开发者需在创建/配置对应资源时显式声明：

| 配置项 | 所属场景 | 说明 | 示例 |
|---------|-----------|------|------|
| `tool_id` / `function.name` | 插件、MCP、Assistant API | 工具唯一标识符，必须与注册时完全一致 | `"calculator"`, `"maps_route"` |
| `parameters` / `inputSchema` | 全部 | 定义工具所需参数的 JSON Schema，直接影响模型参数提取准确性 | `{"type": "object", "properties": {"query": {"type": "string"}}}` |
| `permission_policy` | Managed Agents | 控制调用前是否需人工审批，仅对内置工具和 MCP 有效 | `{"type": "always_ask"}`（暂停会话等待确认） |
| `tool_choice` | Assistant API、MCP | 显式指定模型行为：`"auto"`（默认，自主决策）、`"none"`（禁用）、或指定 `{"type": "function", "function": {"name": "xxx"}}` | 用于强制触发特定工具调试 |
| `env`（环境变量） | MCP、Managed Agents | 安全传递敏感凭据（如 API Key），**禁止明文写入配置**，须通过 KMS 加密或 Vault 注入 | `{"AMAP_MAPS_API_KEY": "{{vault:amap_key}}"}` |

> ⚠️ 注意：  
> - 参数类型为 `Object` 时，所有子字段必须有明确 `type` 且不可为空，否则发布失败（错误码 `130022`）；  
> - `tool_id` 区分大小写，且不支持特殊字符；  
> - 启用 `always_ask` 审批策略后，该策略仅对新建会话生效，已有会话不受影响。

## 面向开发者，简洁实用

- **调试优先**：首次集成函数调用时，务必开启 `stream=true` 并监听 `event: tool_call` 类型事件，观察模型是否正确识别工具名、是否生成合法参数。若参数为空或格式错误，优先检查 `description` 是否清晰、`inputSchema` 是否完备。
- **Schema 是关键**：比写 [prompt](../guides/prompt.md) 更重要的是写好 `inputSchema` —— 用简短准确的 `description` 描述每个字段用途（如 `"城市名称，例如'北京'"`），避免模糊表述。
- **权限最小化**：内置工具和 MCP 默认禁用，启用前务必评估风险；涉及网络或文件操作的工具，应配合 `environment.networking.type="unrestricted"` 或挂载白名单路径。
- **错误处理必做**：函数调用失败（如 HTTP 4xx/5xx、超时、Schema 不匹配）会返回 `tool_error` 事件，需在客户端捕获并降级处理（如提示用户重试或切换方案），不可静默忽略。
- **不要重复造轮子**：优先选用官方插件或 MCP 服务（如 `quark_search` 已覆盖基础检索），自定义开发仅用于私有系统或强定制逻辑。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [managed agents](../guides/managed-agents.md)
- [plug in](../guides/plug-in.md)
- [application call](../api/application-call.md)
- [model context protocol](../guides/model-context-protocol.md)


