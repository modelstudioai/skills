# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台定义的标准化工具通信协议，用于在智能体（Agent）运行时安全、可靠地调用外部能力服务。它通过统一的接口契约与运行时适配机制，将大模型的工具调用意图（tool call）转化为对真实服务（如地图、搜索、数据库、API 网关等）的结构化请求，并将响应结果以符合模型理解的方式注入上下文，从而扩展模型的实时感知与执行边界。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 不是独立运行的服务，而是**专为智能体应用设计的上下文扩展协议**，仅在以下两类场景中生效：

- **Managed Agent（托管智能体）**：在 Agent 配置中启用 MCP 服务后，模型可根据用户输入自动识别是否需要调用（例如“查北京今天天气”触发 `weather` 工具），无需显式编写调用逻辑；`tool_choice` 参数控制调用策略（`auto`/`none`/指定工具名）。
- **Flow Agent（工作流智能体）**：作为独立节点接入流程图，每个 MCP 节点需手动绑定一个已注册的 MCP 服务（如 `amap-maps.maps_weather`），并由前置 LLM 节点解析参数后传递给该节点执行；适用于需精确控制调用时机与输入构造的编排场景。

> ⚠️ 注意：MCP **不支持直接集成到千问原生 API（如 `/v1/services/aigc/text-generation`）调用中**，也不适用于 Sandbox 模式下的本地代码执行。它仅作用于平台级 Agent 运行时框架，是智能体“上下文感知+工具执行”能力的核心协议层。

## 关键参数和配置

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `type` | string | MCP 服务部署类型，决定通信方式与端点匹配规则 | `"streamableHttp"`（推荐）、`"stdio"`、`"sse"` |
| `tool_choice` | string | Agent 级工具调用策略（仅 Managed Agent 有效） | `"auto"`（默认）、`"none"`、`"weather"`（显式指定） |
| `DASHSCOPE_API_KEY` | string | 全局鉴权凭证，所有 MCP 服务（含 One Key 官方服务）共用，**无需单独申请子密钥** | `sk-xxx`（控制台获取） |
| `timeout_ms` | integer | 单次 MCP 调用超时时间（毫秒），建议设为 10000–30000 | `15000` |
| `max_retries` | integer | 失败重试次数（仅对 HTTP 类型生效） | `2` |

- ✅ **必配项**：`type`（决定协议兼容性）、`DASHSCOPE_API_KEY`（全局认证）  
- ✅ **推荐显式配置**：`timeout_ms`（避免长阻塞影响 Agent 响应）、`tool_choice`（明确控制调用行为）  
- ❌ **不支持**：自定义 Header、Bearer [Token](token.md) 覆盖、私有证书、本地文件路径访问（MCP 服务必须可公网或 VPC 内访问）

## 面向开发者，简洁实用

- **快速上手**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击「One Key」服务即可开通，首次调用即生效；非 One Key 服务需手动开通并完成健康检查。
- **调试技巧**：  
  - 使用 CLI 快速验证：`bl mcp call --target amap-maps.maps_weather --params '{"city": "北京"}'`  
  - 查看调用日志：控制台 → Agent 应用详情页 → 「调用追踪」Tab，筛选 `MCP` 类型事件  
- **错误排查优先级**：  
  1. 检查 `type` 是否与服务实际启动方式一致（如用 `npx mcp-server` 启动却配置 `type: streamableHttp` → 报错 `11200058`）  
  2. 确认 `DASHSCOPE_API_KEY` 已正确设置且未过期  
  3. 查看服务健康状态（控制台 MCP 列表页显示「在线」/「离线」）  
- **成本提示**：每次 MCP 调用均单独计费（如 `web_search` ¥0.03/次），且返回内容计入模型输入上下文，可能间接增加输出 token 消耗——建议在 Flow Agent 中对 MCP 节点添加条件分支，避免无谓调用。

## 关联主题页

- [get started with agents](../guides/get-started-with-agents.md)
- [agent store](../guides/agent-store.md)
- [agent development](../guides/agent-development.md)
- [agent billing](../guides/agent-billing.md)


