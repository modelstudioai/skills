# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台用于标准化大模型与外部工具/服务交互的开放协议实现，它定义了一套可扩展、可发现、可流式调用的工具接口规范，使模型能在推理过程中基于上下文自主决策、参数化调用外部能力，而无需硬编码集成。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent）**：MCP 服务作为“可插拔工具”被添加至智能体配置中（最多 5 个）。模型在生成响应前，会根据用户输入和对话历史自动判断是否需要调用、调用哪个 MCP 工具及传入哪些参数。例如，当用户问“杭州今天天气如何”，模型可自主选择调用 `maps_weather` 工具并填充 `city: "杭州"` 参数。

- **工作流应用（Workflow）**：MCP 以显式节点形式接入流程图。开发者需手动拖入一个 MCP 节点，并在节点配置中指定目标服务（如 `websearch`）、映射输入字段（如将上一节点输出的 `query` 映射为 `q`）、定义输出提取规则。此时调用不依赖模型决策，而是由流程逻辑驱动。

- **外部客户端集成**：支持标准 MCP 客户端（如 Qoder、Cursor、Claude Code）直接连接百炼托管的 MCP 服务端点（`/mcp`），通过 `Streamable HTTP` 协议发起调用。需在客户端配置 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，即可复用百炼平台上的所有已发布 MCP 服务。

- **自定义能力扩展**：开发者可通过三种方式快速发布 MCP 服务：  
  - 使用 `npx` 或 `uvx` 一键部署脚本化工具（适合轻量 CLI 工具）；  
  - 将现有 RESTful API 封装为 MCP 服务（通过 AI 网关自动适配）；  
  - 直接对接阿里云 OpenAPI（如 ECS、OSS、RDS），平台自动生成符合 MCP 规范的工具描述与调用桥接。

> ⚠️ 注意：MCP 服务**不支持访问本地资源**（如本地文件、数据库），且 npx/uvx 部署的服务版本更新后需手动重新部署，不会自动同步。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 示例/约束 |
|------|----------|------|-----------|
| `installMode` | 自定义 MCP 部署 | 决定运行环境与计费模型 | `npx`（Node.js）、`uvx`（Python）、`http`（远程 Streamable HTTP） |
| `deploymentMode` | 自定义 MCP 部署 | 控制服务驻留策略 | `基础模式`（按次计费，有冷启动延迟）、`极速模式`（常驻内存，含固定部署费） |
| `mcpServers` | 自定义 MCP 部署 | JSON 格式服务配置，定义 stdio 或远程端点 | `{ "stdio": { "command": "npx mcp-server-weather" } }` 或 `{ "http": { "url": "https://my-api.example.com/mcp" } }` |
| `Authorization` | 外部 MCP 调用 | 请求头认证凭证 | 必须为 `Bearer ${DASHSCOPE_API_KEY}`，不可使用其他密钥 |
| `max_iterations`（间接影响） | Agent 运行时 | 限制包含 MCP 调用在内的总推理步数 | 默认 10，超限则终止，防止无限工具循环 |

## 面向开发者，简洁实用

- ✅ **快速验证**：使用 CLI 命令 `bl mcp list` 查看已启用服务，`bl mcp call --target weather.get_current --params '{"city":"上海"}'` 直接测试调用。
- ✅ **SDK 集成**：安装 `pip install mcp openai`，用兼容 OpenAI 的客户端连接百炼 `/mcp` 端点，无需修改业务代码即可接入 MCP 生态。
- ✅ **调试必开**：调用时添加请求头 `X-Bailian-Debug: true`，可获取完整工具调用链路日志（含模型决策依据、参数生成过程、HTTP 响应体）。
- ❌ **避免踩坑**：  
  - 不要尝试在 MCP 服务中读写本地磁盘或连接 localhost 数据库；  
  - 若需访问阿里云 VPC 内资源，请为函数计算（FC）部署的 MCP 服务配置 VPC 打通或 IP 白名单；  
  - 私有 npm/PyPI 包请先发布至公共仓库，或改用 `http` 模式远程托管。

MCP 是百炼实现“模型即调度器”的核心基础设施——你提供能力，模型负责编排。专注写好工具逻辑，剩下的，交给上下文。

## 关联主题页

- [agent store](../guides/agent-store.md)
- [agent development](../guides/agent-development.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent legacy](../guides/agent-legacy.md)
- [application component api reference](../api/application-component-api-reference.md)


