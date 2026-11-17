# 函数调用

函数调用（Function Calling）是百炼平台中实现大模型与外部能力动态协同的核心机制，指模型在推理过程中自主识别用户意图、生成结构化工具调用请求（含工具 ID 与参数），并由平台安全执行、返回结果后继续推理的闭环过程。它不是简单的 API 封装，而是模型原生支持的、可被 [prompt](../guides/prompt.md) 触发与控制的语义级能力调度协议。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼中并非单一接口，而是贯穿多个能力层的横切行为模式，具体体现为以下三类典型场景：

- **插件（Plugin）调用**：面向智能体应用（Agent）和工作流节点，当启用 `qwen-plus` 或 `qwen-max` 等兼容模型时，模型可基于用户输入、工具描述及 `tools` 字段声明，自主决定是否调用 `code_interpreter`、`quark_search` 等官方/自定义插件。调用触发依赖 `tools` 列表注入与上下文理解，结果自动注入后续 [prompt](../guides/prompt.md)。
  
- **MCP（Model Calling Protocol）服务调用**：面向系统级能力集成，开发者通过 `/api/v1/mcp/servers/{mcpCode}/tools/call` 接口显式发起同步工具调用。此时“函数调用”表现为标准 REST 请求——需严格指定 `tool_name` 和 `tool_params`，平台负责路由、鉴权与错误封装，适用于需精确控制调用时机与参数的编排场景。

- **[OpenAI 兼容接口](openai-compatible-interface.md)的 `function calling` 模式**：面向迁移开发者，在 `chat/completions` 请求中传入 `functions`（或 `tools`）数组及 `function_call` 策略（如 `"auto"` 或 `"none"`）。百炼兼容该协议，模型返回 `{"function_call": {"name": "xxx", "arguments": "{...}"}}` 结构，开发者需自行解析、执行并拼回 `tool_calls` 消息链。注意：此模式仅对 `qwen4-max`、`qwen3.7-plus` 等明确标注支持 function calling 的文本模型生效。

> ⚠️ 关键区别：插件调用由模型驱动、平台自动完成全链路；MCP 调用由开发者驱动、平台仅执行；OpenAI 兼容调用需开发者承担解析与重入逻辑。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 必填 |
|------|----------|------|------|
| `tools` / `functions` | 插件、OpenAI 兼容 | 工具列表，每个元素含 `type`（固定为 `"function"`）、`function.name`（工具 ID）、`function.description`（影响模型决策准确性）及 `function.parameters`（JSON Schema 定义） | 是（启用调用时） |
| `tool_name` + `tool_params` | MCP 调用 | 直接指定待执行工具名与参数对象（无需 schema），`tool_params` 必须与 [查询工具列表](raw/application-api-reference/overview/overview/list.md) 返回的契约完全一致 | 是 |
| `tool_id` | 插件配置与调用 | 工具唯一标识符，用于 `tools` 数组及后台路由，必须从控制台复制，大小写敏感 | 是（配置与调用均需） |
| `enable_agent_context: true` | 插件+Agent 场景 | 启用上下文增强时，模型对工具描述与参数语义的理解更准确；但仅对 `qwen-agent-*` 及部分 `qwen-*` 模型有效 | 否（推荐开启） |
| `biz_params` | 插件（业务透传） | 当工具配置了“业务透传”参数时，必须通过此字段传递，用于运行时动态注入（如用户 ID、会话 ID） | 是（若工具要求） |

## 面向开发者，简洁实用

- ✅ **首选插件方案**：若目标是构建智能体，优先使用插件市场中的官方插件或发布自定义插件，配置 `tools` 即可启用模型自主调用，无需手写 HTTP 请求。
- ✅ **精准控制选 MCP**：若需在工作流中串行调用多个外部服务、或需捕获中间状态，直接调用 MCP `/call` 接口，参数直传、响应明确、错误结构统一。
- ✅ **迁移 OpenAI 代码**：将 `openai.ChatCompletion.create(...)` 替换为百炼兼容 SDK，`base_url` 改为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，`model` 换为百炼模型名（如 `qwen4-max`），其余保持不变。
- ❌ **避免硬编码工具名**：`tool_name` 和 `tool_id` 必须与平台注册值严格一致，建议从控制台复制，而非手动拼写。
- ❌ **勿混用调用路径**：同一工具不可同时通过插件和 MCP 方式注册；若已作为插件接入，不应再通过 MCP 接口重复调用。
- 🔐 **安全第一**：所有工具调用均受业务空间权限管控，子空间需单独授权；涉及敏感操作（如代码执行、网络搜索）的插件，务必在生产环境启用最小权限原则。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [overview](../api/overview.md)
- [plug in](../guides/plug-in.md)
- [agent context](../guides/agent-context.md)


