# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化、安全、可扩展的工具调用协议，用于在大模型与外部系统（如地图、搜索、数据库、SaaS 应用等）之间建立统一通信通道。它基于开源 MCP 标准实现，并升级为 Streamable HTTP 协议，屏蔽底层网络、序列化和鉴权细节，使开发者能以声明式方式接入多种能力，无需为每个工具重复开发适配逻辑。

## 在百炼平台的不同场景中如何使用

MCP 不是独立服务，而是深度集成于百炼应用框架中的协议层，**仅支持在智能体（Agent）和工作流（Workflow）两类应用中使用**，不可直接用于裸调用千问 API：

- **智能体应用（推荐用于动态决策场景）**  
  模型根据自然语言输入自动判断是否调用、调用哪个 MCP 工具（如 `maps_route`、`web_search`）、传入哪些参数。开发者只需在应用配置中「添加 MCP 服务」，最多可同时启用 5 个；工具发现、参数生成、结果解析均由 Agent 自动完成，无需人工编排。

- **工作流应用（推荐用于确定性编排场景）**  
  需手动拖入「MCP 节点」，显式选择一个已配置的工具（如 `oss_list_objects`），并通过连线将上游节点输出（如 `参数提取/result`）绑定为该工具的输入字段。每个 MCP 节点严格绑定单一工具，调用时机与参数完全可控。

- **高代码应用（面向专业开发者）**  
  在 Python 代码中通过 `fastmcp.Client` 或标准 `mcp` SDK 接入 MCP 服务，支持自定义工具调用循环、错误重试、多轮状态管理等高级控制逻辑，适用于需深度定制的生产级应用。

> ⚠️ 注意：MCP 服务**不能直接接入千问 API 的原始调用链路**。若需工具能力，必须通过上述三类百炼应用框架，而非直接向 `/api/v1/services/qwen-max` 等模型端点发送请求。

## 关键参数和配置

MCP 使用涉及服务端部署配置与客户端运行时调用两层关键参数：

### 服务端配置（部署时设置）
- `type`: 必填，协议类型，必须与接入路径严格匹配：  
  - `"streamableHttp"` → 对应 `/mcp` 端点（百炼当前默认且唯一支持类型）  
  - `"sse"` → 对应 `/sse` 端点（已弃用，配置将触发 `11200058` 错误）  
- `url`: 远程 MCP Server 地址（如 `https://my-mcp-service.example.com/mcp`），需 HTTPS 且 TLS 证书有效（否则报 `11200048` SSL_ERROR）。  
- `env`: 敏感环境变量（如 `AMAP_MAPS_API_KEY`）**必须通过 KMS 凭据加密注入**，禁止明文写入配置。  
- `command` / `args`: 仅限脚本托管模式（如 `npx @modelcontextprotocol/server-memory`），用于启动本地 MCP Server。

### 客户端调用参数（运行时生成或显式构造）
- `name`: 工具名（由模型生成或工作流节点指定），必须与 MCP Server 注册的 `tool_name` 完全一致。  
- `arguments`: JSON 字符串格式参数（如 `{"query": "杭州天气", "city": "hangzhou"}`），由模型自动填充或工作流节点显式配置。  
- `Authorization` header: 所有 MCP 请求必须携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，API Key 需具备对应业务空间权限。  
- `workspaceId`: 构造 MCP 地址必需（如 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`），用于资源隔离与路由。

## 面向开发者：简洁实用提示

- ✅ **开通即用**：优先选用 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 中的官方服务（如 Amap Maps、WebSearch），一键开通后直接在智能体/工作流中添加。  
- ✅ **自定义服务三选一**：  
  - 轻量级：用 `npx` 或 `uvx` 快速托管开源 MCP Server（适合调试）；  
  - 无侵入：通过 AI 网关将现有 RESTful API 封装为 MCP（零代码改造）；  
  - 企业级：通过 OpenAPI 开发者门户将阿里云产品（OSS、ECS、RDS）操作发布为 MCP 工具。  
- ✅ **调试技巧**：  
  - 智能体测试时，用明确指令触发工具（如“查北京到上海的驾车路线”），观察日志中 `tool_calls` 是否生成；  
  - 工作流调试时，检查 MCP 节点输入字段是否成功绑定上游输出（如 `input.query = 参数提取/result`）；  
  - 外部调用失败时，优先验证 `url` 可达性、`DASHSCOPE_API_KEY` 权限、`workspaceId` 是否匹配。  
- ❌ **避坑指南**：  
  - 不要尝试在千问 API 调用中硬编码 MCP 工具逻辑——协议不兼容；  
  - 自定义 MCP 服务运行于函数计算（FC），**无固定出口 IP**，访问内网资源需配置 VPC 或白名单；  
  - 文件/表格类连接器会解析内容但**不索引原始数据**，敏感信息仍保留在源系统。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)


