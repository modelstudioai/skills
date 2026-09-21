# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的关键能力。它使大模型从纯文本生成器升级为可操作真实世界的智能代理，是构建 Agent、工作流和插件集成的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一功能，而是贯穿多个能力层的统一交互范式，具体体现为：

- **插件（Plug-in）场景**：模型根据用户输入（如“查北京明天天气”），自动输出符合 OpenAI 标准的 `tool_calls` 数组，包含 `name` 和 `arguments`；开发者需解析该结构，调用对应插件 endpoint，并将结果以 `tool_message` 形式回传模型完成终局响应。此流程依赖 `enable_plugins: true` 显式启用，且仅 `qwen-max`/`qwen-plus`/`qwen-turbo` 原生支持。

- **意图理解模型（`tongyi-intent-detect-v3`）场景**：该专用模型专为函数调用生成优化，支持双模式输出——可直接返回标准 JSON 格式的工具调用参数（含 `function_name` 和 `parameters`），无需模型推理环节，显著降低延迟与不确定性，适用于高实时性 Agent 路由或规则引擎前置判断。

- **LLM 应用（Agent 2.0 / Workflow）场景**：在智能体中，函数调用表现为“规划-执行-反思”链路中的 `plan → tool_call` 步骤，模型自主选择内置工具（如 `bash`、`read`）或接入的 MCP/知识库服务；在工作流中，函数调用则下沉为显式配置的“工具节点”（如 API 调用、函数计算、插件），由编排逻辑而非模型自主触发，确保确定性。

- **托管智能体（Managed Agents API）场景**：函数调用是 Agent 执行生命周期的默认行为模式。当用户消息提交至 `/v1/agents/{id}/chat`，平台自动启用工具调用能力（无需额外开关），模型基于绑定的 Skills（如 WebSearch、CodeInterpreter）生成 `tool_calls`，平台负责调度、超时控制与结果注入，开发者只需关注 `tool_message` 的格式合规性。

## 关键参数和配置

函数调用行为受以下关键参数控制（依使用场景不同，配置位置可能为请求体、节点设置或 SDK `extra_body`）：

- `enable_plugins`: 布尔值，默认 `false`；**仅插件场景必需显式设为 `true`** 才激活模型侧的函数调用生成能力。
- `plugins`: JSON 数组，定义可用工具的 `name`、`description` 和 OpenAPI 兼容 `parameters` schema；必须与插件注册信息严格一致。
- `tool_choice`: 字符串或对象，用于约束调用行为（如 `"auto"`、`"none"` 或 `{"type": "function", "function": {"name": "xxx"}}`）；当前百炼平台暂不开放该参数直传，由模型自主决策，但可通过 system prompt 引导（如“请仅在需要时调用工具”）。
- `plugin_timeout_ms`: 整数，单位毫秒，默认 `10000`；控制单次插件调用最大等待时间，超时后自动回退至文本响应。
- `temperature`: 建议设为较低值（如 `0.1–0.3`）以提升函数调用参数生成的准确性与稳定性，尤其在参数结构复杂时。

> ⚠️ 注意：所有函数调用输出均遵循 OpenAI 兼容格式（`tool_calls` 字段），但百炼平台**不支持 `function` 类型旧版字段**；务必使用 `tool_calls` + `type: "function"` 结构，并确保 `arguments` 为合法 JSON 字符串（非对象）。

## 面向开发者，简洁实用

- ✅ **必做**：始终校验响应中是否存在 `tool_calls` 字段；若存在，必须按 `name` 匹配工具、`arguments` 解析参数（`JSON.parse(arguments)`），并同步调用对应 endpoint。
- ✅ **必做**：插件调用返回结果必须封装为 `tool_message`（role=`"tool"`，content 为字符串化 JSON 或错误信息），并作为新消息重新提交给模型。
- ✅ **推荐**：对 `arguments` 做基础 JSON Schema 校验（如必填字段、类型），避免因模型幻觉导致下游服务报错。
- ❌ **禁止**：在非 `qwen-max`/`qwen-plus`/`qwen-turbo` 模型上设置 `enable_plugins: true` —— 调用将被静默忽略，无任何提示。
- 📌 **调试技巧**：开启 `stream: false` + `enable_thinking: true`（若模型支持），可观察模型在 `thinking` 步骤中如何分析工具适用性，辅助 prompt 优化。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [more models](../api/more-models.md)
- [llm application](../guides/llm-application.md)
- [managed agents api](../api/managed-agents-api.md)


