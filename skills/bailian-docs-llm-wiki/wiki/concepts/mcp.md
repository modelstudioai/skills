# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台定义的、用于大模型与外部能力（如工具、API、服务）进行标准化交互的轻量级通信协议。它通过结构化请求/响应格式与统一传输语义，使模型能在推理过程中动态感知、选择并调用外部能力，将结果无缝注入上下文，从而扩展模型的知识边界与执行能力。

## 在百炼平台的不同场景中如何使用

MCP 不是通用 API 接口，**仅在百炼应用运行时上下文中生效**，不可直接用于 `dashscope` SDK 的单次 `chat.completions.create` 调用。其核心使用场景如下：

- **智能体（Agent）中集成**：在 Agent 配置页「能力扩展」区域添加 MCP 服务（如 `Amap Maps`、`WebSearch`），最多支持 5 个；模型在生成过程中自动触发调用，返回结果作为上下文片段参与后续推理。
- **工作流（Flow）中编排**：在工作流画布中添加「MCP 工具节点」，手动指定服务 ID（如 `maps_weather`）并绑定输入参数（如 `city: {{input.city}}`）；支持多步串联与条件分支。
- **Omni Realtime 实时语音对话中启用**：在 `tools` 参数中声明 `type=mcp` 的工具项（例如 `{ "type": "mcp", "name": "web_search" }`），配合 VAD 实现“边说边查、边听边答”的低延迟交互；注意：`enable_search` 与 MCP 工具互斥，二者不可共存。
- **外部系统对接（非百炼应用内）**：通过 CLI（`bl mcp call --target amap-maps.maps_weather`）、MCP SDK（如 `streamablehttp_client`）或第三方客户端（Cherry Studio、Cursor）调用已开通的 MCP 服务；所有调用均使用统一的 `DASHSCOPE_API_KEY` 鉴权。

> ⚠️ 重要限制：MCP 服务无法在纯模型 API（如 `qwen-max` 直接调用）中使用；自定义 MCP 服务运行于函数计算环境，**无法访问本地文件、数据库或未显式打通网络的云资源**。

## 关键参数和配置

| 参数 | 类型 | 说明 | 使用位置 |
|------|------|------|----------|
| `mcpServers` | JSON 对象 | 定义自定义 MCP 服务的启动方式与通信协议，含 `type`（`stdio`/`sse`/`streamableHttp`）、`command`（如 `npx mcp-server-amap`）、`url`（HTTP 类型必填）等字段 | 自定义 MCP 服务部署配置 |
| `deploymentMode` | string | 部署模式：`基础模式`（按调用时长计费，有冷启动）或 `极速模式`（常驻实例，按部署+调用双计费） | 自定义 MCP 服务部署配置 |
| `tools`（API 请求体） | array | 在 Omni Realtime 或 Agent 工作流中声明可用 MCP 工具，每个元素为 `{ "type": "mcp", "name": "<service_id>.<function_name>" }` | `omni-realtime-api` / `managed-agents-api` 请求体 |
| `DASHSCOPE_API_KEY` | string | 所有外部 MCP 调用（CLI、SDK、第三方客户端）的唯一鉴权凭证；**无需为每个 MCP 服务单独申请密钥** | 环境变量或请求 Header |

## 面向开发者：快速上手提示

- ✅ **首选官方服务**：从 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 一键开通 `WebSearch`、`Amap Maps` 等 One Key 服务，免部署、免调试。
- ✅ **自定义服务请用 `streamableHttp`**：兼容性最好，支持标准 HTTP POST + SSE 流式响应，便于本地开发与调试。
- ✅ **调试技巧**：在智能体测试界面开启「显示工具调用详情」，可实时查看模型生成的 `tool_calls` 及实际返回内容，快速定位参数映射或 schema 不匹配问题。
- ❌ **避免常见错误**：  
  - 不要在 `dashscope.chat.completions.create()` 中传入 `tools` 类型为 `mcp` 的参数（会报错）；  
  - 不要假设自定义 MCP 服务能读取 `/tmp` 或访问 `localhost:3306`（需通过 VPC 或白名单显式打通）；  
  - 更新 `npx` 启动的服务后，必须重新部署——不会自动热更新。

## 关联主题页

- [agent store](../guides/agent-store.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [flow agent api](../api/flow-agent-api.md)


