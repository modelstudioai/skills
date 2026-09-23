# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化、安全可扩展的工具集成协议，用于在大语言模型与外部能力（如搜索、地图、数据库、知识库等）之间建立统一、声明式的通信通道。它将工具调用抽象为标准化的接口契约，使模型能基于自然语言意图自动发现、选择并调用合适工具，无需硬编码适配逻辑。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent 2.0）**：MCP 是 Agent 的核心能力底座。添加 MCP 服务后，模型在对话中自主判断是否调用及调用哪个工具（例如用户问“北京今天天气如何”，自动触发 `weather_get_current` 工具）。最多支持同时启用 **5 个 MCP 服务**，所有工具统一纳入模型的规划与执行链路，并支持完整过程回溯。

- **工作流（Workflow）**：通过 **MCP 节点**接入单个工具，需显式配置输入参数来源（如引用上游节点输出的 `city_name` 字段）。典型模式为：大模型节点 → 参数提取 → MCP 节点 → 结果处理节点。每个 MCP 节点绑定一个工具，适合确定性、结构化强的任务编排。

- **Connector（连接器）**：百炼 Connector 将钉钉、语雀、OSS、MySQL 等 20+ 类企业系统**自动封装为标准 MCP 工具**。授权配置后，平台自动生成符合 MCP v1.0 规范的 `name`、`description`、`parameters` 和 `output_schema`，开发者无需编写任何适配代码即可在智能体或工作流中直接调用。

- **知识库（Knowledge Base）**：知识库的 RAG 问答服务可通过 MCP 协议对外暴露为工具（如 `knowledgebase_ask`），被其他智能体或第三方客户端按需调用，实现私有知识的“即插即用”式复用。

- **高代码应用（Serverless/K8s）**：在 Python 函数中，通过 `fastmcp.Client` SDK 调用本地或远程 MCP 服务，与 DashScope API 或自定义逻辑组合，构建深度定制的 AI 应用后端。

> ✅ 提示：MCP **仅在智能体应用和工作流应用中生效**；不支持在直接调用千问 [OpenAI 兼容接口](openai-compatible-interface.md)（如 `/v1/chat/completions`）时使用。

## 关键参数和配置

MCP 服务配置以 JSON 格式定义在 `mcpServers` 字段中，关键参数如下：

| 参数 | 必填 | 说明 | 示例值 |
|------|------|------|--------|
| `type` | ✅ | 协议类型，决定通信方式与端点路径，**必须与下游服务实际协议严格匹配** | `"streamableHttp"`（推荐）、`"sse"`、`"stdio"` |
| `url` | ✅（远程）<br>`command`（本地） | 远程服务地址（POST `/mcp`）或本地启动命令（如 `npx @modelcontextprotocol/server-memory`） | `"https://my-mcp-server.example.com/mcp"` |
| `env` | ⚠️（敏感时必填） | 环境变量，用于注入密钥等凭据（**必须经 KMS 加密，禁止明文**） | `{"AMAP_MAPS_API_KEY": "{{kms:xxx}}"}` |
| `inputSchema` | ✅ | 工具输入参数的 JSON Schema，直接影响模型生成参数的准确性与合法性 | `{"type":"object","properties":{"query":{"type":"string"}}}` |

⚠️ 常见错误：
- `11200054 - MCP_PROTOCOL_ERROR`：`type` 与服务实际暴露协议不一致（如配置 `"sse"` 但服务只提供 `/mcp` POST 接口）；
- `11200058 - MCP_SERVER_HTTP_METHOD_NOT_ALLOWED`：HTTP 方法错误（`streamableHttp` 必须用 POST，`sse` 必须用 GET）；
- 自定义服务运行于函数计算（FC），**无固定出口 IP**，访问云数据库等资源需配置白名单或 VPC 打通。

## 面向开发者：简洁实用指南

- **快速起步**：控制台 → 智能体/工作流 → 添加工具 → 选择「官方 MCP 服务」（如 WebSearch、Amap Maps）→ 开通即用，无需部署。
- **自定义服务三选一**：
  - ✅ **脚本部署**：`npx` 或 `uvx` 启动开源 MCP Server（如 `@modelcontextprotocol/server-memory`），适合原型验证；
  - ✅ **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具，零代码生成 `inputSchema`；
  - ✅ **OpenAPI 导入**：上传 OpenAPI 3.0 YAML/JSON，自动发布为 MCP 服务（支持阿里云 OSS/ECS 等产品）。
- **调试技巧**：
  - 使用 [Playground](https://bailian.console.aliyun.com/?tab=app#/app-center) 中的智能体调试模式，查看工具调用日志与原始响应；
  - 工作流中开启「节点日志」，检查 MCP 节点输入/输出及 HTTP 状态码；
  - 外部调用时，优先使用 `mcp.client.streamable_http` SDK（Python/JS），避免手动构造请求。
- **安全合规**：所有敏感凭据必须通过 KMS 加密引用；自定义服务不可访问本地文件、硬件或用户设备；生产环境建议使用 `streamableHttp`（替代已弃用的 SSE）。

> 📌 最新协议规范请参考 [MCP 官网](https://modelcontextprotocol.io/)；百炼平台实现基于 MCP v1.0，兼容主流开源生态。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [knowledge base](../guides/knowledge-base.md)
- [overview](../guides/overview.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


