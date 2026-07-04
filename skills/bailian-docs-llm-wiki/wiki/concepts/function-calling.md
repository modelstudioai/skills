# 函数调用

函数调用（Function Calling）是大模型根据用户意图与工具描述，自主判断是否调用外部工具、并按协议返回结构化调用参数的一种能力。在百炼平台中，它是连接大模型与外部 API、插件、代码解释器及智能体技能的关键机制，使模型能够获取最新信息、执行精确计算与操作真实环境。

## 在百炼平台中的使用方式

百炼支持多种函数调用接入路径，开发者可按接口协议与编排复杂度选择：

- **OpenAI 兼容 Chat Completions 接口**：通过请求体中的 `tools` 字段按 OpenAI 协议声明函数（function） schema，模型返回 `tool_calls`，调用方执行后回传 `tool` 角色消息，构成「调用—回传—续写」循环。完整流程示例见 OpenAI Chat 接口兼容文档。
- **OpenAI 兼容 Responses 接口**：内置联网搜索、代码解释器、网页内容提取等工具，开箱即用；也支持自定义工具。通过 `previous_response_id` 关联上下文，平台自动管理对话历史，无需在请求中手动拼接 `messages`。
- **Anthropic 兼容 Messages 接口**：兼容 Anthropic Messages API 的工具调用协议，支持 `tools` 定义与 `thinking`（思考）能力，适合复用 Anthropic SDK 的场景。
- **DashScope 原生接口**：参数集最完整，支持最全的采样参数、插件与业务字段，推荐用于需要百炼原生全部能力的场景。
- **Qwen-Omni-Realtime 接口**：实时多模态 WebSocket 接口同样提供工具调用（Function Calling）能力。工具回传结果后，需由客户端手动发送 `response.create` 事件触发模型续写响应（VAD 自动生成不覆盖工具回传场景）。
- **Managed Agents API**：由平台托管智能体运行时，工具以「技能（Skill）」与「工具包」形式挂载到 Agent 配置，平台在沙箱（Environment）中执行工具调用并通过 SSE 事件流回传结果，开发者无需自建调度与执行基础设施。
- **智能体应用 / Assistant API**：大模型根据用户输入、工具名称与描述判断是否调用工具；需要调用时选择合适工具，应用内部完成调用后将结果与用户内容合并再次输入模型，由模型生成最终结果。

## 关键参数与配置

- **`tools` / `tool_choice`**：在 Chat Completions、Messages 等接口中声明可用函数列表及调用策略。`tool_choice` 可指定 `auto`（模型自主决定）、`none`（不调用）或强制指定具体函数。
- **`model`**：函数调用依赖模型能力，需选择支持工具调用的 Qwen 系列模型（如 `qwen-turbo`、`qwen-plus`、`qwen-max` 等），三方直供模型仅在中国内地地域可用。
- **工具 ID**：通过插件调用或 Assistant API 调用工具时，需正确传递工具 ID（如 `calculator`、`code_interpreter`、`quark_search`），可在插件详情页获取。每个智能体应用最多支持添加 10 个工具。
- **`base_url` 与鉴权**：兼容接口统一使用业务空间专属域名 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`，并通过 `Authorization: Bearer <API Key>` 或环境变量 `DASHSCOPE_API_KEY` 鉴权。新加坡与北京地域的 API Key 不通用，切换地域需同步更换。
- **对话历史管理**：仅 Responses 接口由平台自动维护历史；其他接口需调用方自行管理上下文长度与轮次，避免超出模型上下文窗口。工具回传消息（`role: tool`）须与对应的 `tool_call_id` 配对，否则模型续写会失败。
- **沙箱与依赖**：Managed Agents API 通过 Environment 资源提供工具调用的执行沙箱与预装依赖；Python 代码解释器插件可用依赖包括 matplotlib、pandas、scipy、pillow、requests、oss2 等，但不支持对外访问网络及上传本地文件。

## 注意事项

- **能力差异**：兼容接口为保证协议一致性，可能不暴露百炼原生全部参数；需要最全的工具/采样参数时应改用 DashScope 原生接口。
- **内置工具范围**：联网搜索、代码解释器、网页内容提取为 Responses 接口专属内置能力；Chat Completions 与 Anthropic Messages 接口不内置这些工具，需自行实现或通过 `tools` 协议接入。
- **插件兼容性**：各模型对插件的兼容性可能不同，最新状态以控制台实际执行结果为准；夸克搜索、GitHub 搜索不支持直接访问详情页，Python 代码解释器不支持联网。
- **迁移评估**：从 OpenAI / Anthropic 迁移时，应先确认目标 Qwen 模型在对应兼容接口下是否支持所需参数（如 `temperature`、`tools`、`stream`），再决定接口选型。
- **失败处理**：工具执行失败时，应在回传的 `tool` 消息中给出明确错误信息，模型可据此向用户说明或改用其他工具；不要静默吞掉异常。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)


