# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具调用请求，并交由外部系统执行的关键能力。它使模型不再仅输出文本，而是能按需触发真实世界操作——如查询数据库、执行计算、调用 API、运行代码或控制设备。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口特性，而是贯穿多个能力层的统一语义机制，具体体现为以下四类场景：

- **实时多模态交互（Omni Realtime API）**：在语音/文本混合会话中，模型可基于上下文和用户语音输入，自主决定是否调用工具（`type=function`）。例如客服场景中识别“查我上月账单”，自动触发 `get_billing_info` 工具；注意此时 `tools` 配置与 `enable_search` 互斥，需显式声明工具列表。

- **意图理解专用模型（More Models）**：`tongyi-intent-detect-v3` 模型专为毫秒级意图识别与函数调用生成优化。它不生成自然语言回复，而是直接输出标准 JSON Schema 格式的工具调用指令（含 `name` 和 `arguments`），供下游路由系统解析并分发至对应服务。

- **智能体托管运行时（Managed Agents）**：函数调用是 Agent 多步自主决策的核心驱动力。模型在沙箱环境中持续规划、调用内置工具（如 `bash`、`web_search`、`read`）或接入的 MCP 服务，每一步 `tool_call` 事件均通过 SSE 流式返回，支持人工审批（`tool_approval_request`）与中断续接。

- **插件与 Assistant 应用（Plug-in / Toolkits）**：在 [OpenAI 兼容接口](openai-compatible-interface.md)（如 `/chat/completions`）或 Assistant API 中，开发者通过 `tools` 参数注册插件定义（含 `function.name`、`description`、`parameters`），模型将根据提示词和用户输入，输出符合 OpenAI 标准的 `tool_calls` 数组。百炼兼容层自动完成鉴权透传、参数映射与错误处理。

> ✅ 统一行为：无论在哪种场景，函数调用均由模型**自主触发**（非客户端强制），且必须严格遵循注册的工具 Schema；调用失败（如参数格式错误、工具未启用）将导致 `TOOL_NOT_FOUND` 或 `INVALID_TOOL_CALL` 错误。

## 关键参数和配置

函数调用能力依赖以下核心参数，需在请求中正确配置：

| 参数 | 所属场景 | 类型 | 说明 | 必填 |
|------|----------|------|------|------|
| `tools` | 全场景通用 | `array` | 工具定义列表，每个元素为 `{ "type": "function", "function": { "name", "description", "parameters" } }`。`parameters` 必须为 JSON Schema object，不支持 `null` 默认值。 | ✅（启用调用时） |
| `tool_choice` | Omni Realtime / Toolkits / Managed Agents | `string` 或 `object` | 控制调用策略：<br>• `"auto"`（默认）：模型自主决定是否调用<br>• `"none"`：禁止调用<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定工具 | ❌（默认 auto） |
| `tools.configs[].enabled` | Managed Agents | `boolean` | 在 Agent 配置中，**必须显式设为 `true`** 才能使工具对模型可见；`default_config.enabled: true` 不生效。 | ✅（启用某工具时） |
| `biz_params` | Plug-in（API 调用） | `object` | 用于透传用户级业务参数（如用户 ID、租户上下文），供自定义插件在运行时读取，不参与模型推理。 | ❌（按需） |

> ⚠️ 注意事项：
> - 工具名（`function.name`）区分大小写，且必须与后端服务注册名完全一致；
> - `parameters` 中 Object 类型字段的子属性**不可省略或为空**（否则发布/调用失败，错误码 `130022`）；
> - GET 类型插件不支持 Object 输入参数，请改用 POST 或调整参数设计；
> - 所有工具调用均受配额与速率限制约束，详见各场景的 [限流文档](../../raw/model-api-reference/rate-limiting.md)。

## 面向开发者，简洁实用

- **调试第一步**：始终先用控制台「对话测试页」验证工具注册与调用逻辑，观察模型是否输出 `tool_calls` 而非自然语言；
- **Schema 要精简**：`parameters` 只保留必要字段，避免嵌套过深；用 `description` 清晰说明每个参数用途（模型依赖此理解语义）；
- **错误处理要前置**：在 `tools` 中定义 `required` 字段，并在后端校验 `arguments` 合法性；百炼不校验参数内容，只做 JSON 解析；
- **生产必设 `tool_choice`**：高确定性场景（如固定流程）建议设为 `{"function": {"name": "xxx"}}`，避免模型“犹豫”导致延迟；
- **日志看 `tool_call_id`**：所有工具调用事件均带唯一 `id`，可用于全链路追踪与重试；Managed Agents 的 `tool_approval_request` 事件中该 ID 用于审批响应绑定。

函数调用不是魔法——它是模型与世界的契约。写好 Schema，配对工具，再给模型一句清晰的指令，它就会为你精准执行。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [more models](../api/more-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [agent development](../guides/agent-development.md)
- [plug in](../guides/plug-in.md)


