# 函数调用

函数调用（Function Calling）是百炼平台中模型主动触发外部工具执行能力的核心机制：大模型在推理过程中，根据用户输入和上下文，自主生成结构化的函数调用请求（含函数名、参数），由开发者或平台运行时解析并执行真实逻辑，再将结果回传以继续对话。该机制使模型突破纯文本生成边界，实现搜索、计算、数据库操作、API 集成等确定性任务。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用不是独立服务，而是深度嵌入多个能力层的标准化交互协议，具体使用方式依场景而异：

- **Managed Agents（托管智能体）**：作为 Agent 自主规划（Plan-and-Execute）的执行环节。Agent 模型（如 `qwen-plus`）在多步推理中决定调用哪个工具（如 `search_knowledgebase`），平台自动解析 `tool_calls`、转发请求、注入结果到上下文，并支持 Webhook 事件（`tool_called`）通知开发者。
  
- **Plug-in（插件）**：面向通用模型调用的轻量级扩展机制。开发者在请求中声明 `tools` 数组（OpenAI 兼容格式），指定 `tool_choice` 策略（`auto`/`none`/强制指定），模型返回 `tool_calls` 后，**需客户端主动执行调用并提交 `tool_result`** 继续会话流。

- **DashScope 原生 API（Qwen API Reference）**：最底层、最灵活的接入方式。通过 `/v1/chat/completions` 接口传入 `tools` 和 `tool_choice`，响应中明确返回 `tool_calls` 字段；支持流式响应（`stream: true`），但 `tool_calls` 仅在 `finish_reason: "tool_calls"` 的最终 chunk 中出现。

- **Model Context Protocol（MCP）**：平台级标准化协议，聚焦安全与上下文感知。要求显式传递 `tool_id`、`session_id` 和结构化 `input`，所有调用经百炼网关鉴权与审计；适用于需强治理、跨模型复用工具的生产环境。

- **Application Calling（应用调用）**：对已发布的智能体或工作流应用进行端到端调用。函数调用发生在应用内部（如智能体的工具节点、工作流的函数节点），对外表现为 `POST /v1/applications/{app_id}/call` 的统一接口，开发者无需直接处理 `tool_calls`。

- **Release Notes 所述能力演进**：函数调用能力持续增强，例如 Qwen3 支持 1024K 上下文下的长链工具调用，`stream=true` 下 `tool_choice="auto"` 已稳定可用，`system` 消息可注入全局工具使用约束。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 使用场景 |
|------|------|------|------|----------|
| `tools` | array | 是（启用调用时） | 工具定义数组，每个元素为 `{ "type": "function", "function": { "name", "description", "parameters" } }`；`parameters` 必须是合法 JSON Schema object（扁平结构优先，避免 `anyOf`/`oneOf`） | Plug-in、DashScope API、MCP、Managed Agents |
| `tool_choice` | string / object | 否 | 控制策略：<br>• `"auto"`（默认，模型自主决策）<br>• `"none"`（禁用）<br>• `{"type": "function", "function": {"name": "xxx"}}`（强制指定） | Plug-in、DashScope API（MCP 和 Managed Agents 由平台策略控制，不暴露此参数） |
| `tool_preview` | boolean | 否（仅调试） | 设为 `true` 时返回 `tool_calls` 预览但不触发真实调用，用于验证 schema 兼容性 | Plug-in（调试阶段） |
| `session_id` | string | 否（会话续写必需） | 关联上下文的唯一标识，用于跨轮次保持工具执行状态和历史输入输出 | Managed Agents、MCP、Application Calling（智能体应用） |
| `tool_id` | string | 是（MCP 调用） | MCP 注册时分配的工具唯一 ID，非 URL；必须与控制台注册一致 | MCP |

> ⚠️ 注意：  
> - 单次请求最多声明 **10 个 `tools`**，单次响应最多返回 **3 个 `tool_calls`**；  
> - `tools` 中的 `parameters` Schema 深度不得超过 **5 层**，含二进制字段需显式声明 `"format": "binary"`；  
> - 所有自定义工具 endpoint **必须使用 HTTPS**，且域名需在百炼控制台完成白名单备案。

## 面向开发者，简洁实用

- ✅ **快速上手**：从 DashScope API 开始，用 `qwen-plus` + `tools` 数组 + `tool_choice="auto"` 发起首次调用，观察响应中的 `tool_calls` 字段；
- ✅ **生产就绪**：  
> - 敏感参数（如 token、密码）在 `parameters` Schema 中标记 `"x-sensitive": true`，平台自动脱敏；  
> - 使用 SDK（v3.12.0+）调用 MCP 或 Managed Agents，自动处理重试、上下文注入与错误分类（如 `MCP_TOOL_NOT_FOUND`）；  
> - 工作流应用中，勿依赖顶层 `parameters` 覆盖 LLM 节点采样参数，应在节点配置中单独设置；
- ❌ **避坑指南**：  
> - 不要混用 `functions`（[OpenAI 兼容接口](openai-compatibility.md)已弃用）与 `tools`；  
> - 流式响应中，`tool_calls` 不在中间 chunk 出现，切勿提前解析；  
> - 切换模型（如 `qwen-max` → `qwen2.5-7b`）后上下文不继承，`session_id` 无效；  
> - 绕过百炼网关直连工具 endpoint 将触发风控拦截，必须走平台协议。

## 关联主题页

- [managed agents](../guides/managed-agents.md)
- [plug in](../guides/plug-in.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model context protocol](../guides/model-context-protocol.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [release notes](../guides/release-notes.md)


