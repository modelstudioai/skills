# 函数调用

函数调用（Function Calling）是大模型根据用户输入与工具描述，自主判断是否调用外部工具、选择合适工具并生成结构化调用参数的能力，用于弥补模型在获取实时信息、精确计算、调用业务接口等方面的不足。

## 在百炼平台的使用场景

百炼平台上，函数调用以多种形态贯穿不同协议与产品：

- **OpenAI 兼容 Chat Completions**：通过 `tools` 参数声明函数，模型在响应中返回 `tool_calls`，开发者执行后把结果回传给模型继续生成。这是迁移已有 OpenAI 代码最常用的路径，Qwen 大语言模型、Qwen-VL、Qwen-Coder、Qwen-Omni 等系列均支持。
- **Responses 接口**：作为 Chat 的演进版本，提供智能体原生能力，内置联网搜索、网页抓取、代码解释器、文搜图、图搜图等工具，并通过 `previous_response_id` 关联上下文，免去手动维护消息历史。
- **专用意图模型 `tongyi-intent-detect-v3`**：同时输出意图分类与函数调用信息，适合需要把意图识别与工具选择合并为一步的场景。
- **实时多模态 `Qwen-Omni-Realtime`**：在 WebSocket 会话中支持 Function Calling，客户端通过 `session.update` 配置工具，模型判断需要调用时返回工具调用事件，客户端执行后通过 `response.create` 回传结果继续对话。
- **[智能体应用](agent-application.md)与 Assistant API**：模型根据用户输入、工具名称与工具描述自动决策是否调用以及调用哪个工具；应用内部完成调用后把结果与用户内容合并再次输入模型，由模型生成最终输出。
- **工作流应用**：工具作为工作流中的一个节点，按用户编排的方式执行特定任务，而非由模型主动规划调用。
- **插件机制**：官方插件、三方插件、自定义插件本质上都是工具集合，调用插件即调用其下的工具 API。
- **MCP（模型上下文协议）**：基于开源标准协议统一接入外部工具，单个智能体最多可同时添加 5 个 MCP 服务，常用于多工具协同。

## 关键参数与配置

### 工具声明

- `tools`（array）：工具列表，每个元素描述一个可调用函数，包含 `type`、`function`（含 `name`、`description`、`parameters`）等字段。
- `tool_choice`（string/object）：控制模型是否调用工具。可设为 `auto`（默认，模型自主决策）、`none`（强制不调用）、`required`（强制调用），或指定具体函数。

### 调用与回传流程

1. 请求中携带 `tools`，模型判断需要调用时在响应里返回 `tool_calls`（含 `id`、函数名、参数 JSON）。
2. 开发者本地执行对应函数，得到结果。
3. 把以 `tool` 角色的消息（含 `tool_call_id` 与函数返回内容）追加到 `messages`，再次发起请求。
4. 模型结合工具结果生成最终回复。

### 实时会话中的配置

Qwen-Omni-Realtime 通过 `session.update` 事件在 WebSocket 建连后更新会话默认配置，工具相关字段与标准 Chat 接口一致。VAD 模式下模型自动触发响应，工具调用结果回传后需手动发送 `response.create` 以驱动模型继续生成。

### 插件与 MCP 的鉴权配置

- **自定义插件**：鉴权信息可放在 Header（默认参数名 `Authorization`）或 Query 中，`type` 支持 `basic`、`bearer`（[Token](token.md) 前加 `Bearer`）、`appcode`（[Token](token.md) 前加 `APPCODE`）。
- **MCP 服务**：配置遵循 `mcpServers` 结构，`type` 可选 `stdio`（本地托管）、`sse` 或 `streamableHttp`（远程连接）；远程连接通过带 `Authorization` 头的 `url` 鉴权。

## 开发者要点

- 工具的 `description` 与参数描述直接影响模型决策准确性，建议用自然语言清晰写明工具能力与使用场景，必要时在提示词中明确工具名称。
- 三方直供模型仅在中国内地地域可用，调用前需先在百炼控制台开通对应服务；各地域 [API Key](api-key.md) 不互通，切换地域需同步更换 [API Key](api-key.md) 与 `base_url`。
- MCP 调用会把工具返回内容作为上下文传入模型，导致输入 [Token](token.md) 增加，并可能间接增加输出 Token；调用准确性依赖提示词，若模型未准确调用可更换更强的推理模型（如千问 3 系列）。
- [业务空间](workspace.md)专属域名（`https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`）相比旧域名有更好的推理性能与稳定性，建议迁移。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [more about models](../api/more-about-models.md)
- [more models](../api/more-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)


