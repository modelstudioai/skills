# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是百炼平台提供的标准化工具调用协议，用于在大模型与外部能力（如地图、搜索、数据库、企业系统等）之间建立安全、可扩展、声明式的信息通道。它将异构服务抽象为统一语义的工具接口，使模型能基于自然语言意图自主发现、选择并调用合适能力，无需开发者编写定制化适配代码。

## 在百炼平台的不同场景中如何使用

- **智能体应用（Agent）**：MCP 工具作为“内置能力”被模型自动调度。开发者只需在应用配置中启用所需 MCP 服务（最多 5 个），并在提示词中表达意图（如“查北京到上海的实时路况”），模型即会推理调用 `maps_route` 等对应工具。Agent 2.0 架构下，MCP 与知识库、文件解析等一并纳入统一工具规划框架，支持完整过程回溯。

- **工作流应用（Workflow）**：通过可视化「MCP 节点」显式接入。开发者需手动选择具体工具（如 `maps_weather`）、绑定上游节点输出（如 `用户输入/城市名`）作为参数，并配置下游数据流向。每个节点仅绑定一个工具，适合确定性流程编排。

- **高代码应用（Rich Code）**：在 `main.py` 中通过标准 `mcp` SDK（如 Python 的 `mcp-streamable-http-client`）连接已开通的 MCP 服务端点（`/mcp`），以编程方式发起工具调用，实现细粒度控制与复杂逻辑集成。

- **Connector（企业连接器）**：作为 MCP 的上层封装，Connector 将钉钉、语雀、OSS、MySQL 等 20+ 类系统一键授权后，**自动生成符合 MCP 规范的标准工具**，开发者无需开发任何接口或协议适配层，即可在智能体或工作流中直接引用。

> ⚠️ 注意：MCP **不支持**通过千问 OpenAI 兼容 API（如 `/v1/chat/completions`）直接调用；必须运行在百炼平台的智能体、工作流或高代码应用容器内。

## 关键参数和配置

| 类别 | 参数 | 说明 | 示例/约束 |
|--------|------|------|-----------|
| **服务接入** | `type` | 协议类型，决定端点路径与通信方式 | 必须为 `"streamableHttp"`（推荐），对应 `/mcp`；旧版 `"sse"` 已停用 |
| | `url` | MCP Server 的公网可访问地址 | 如 `https://your-mcp-service.aliyuncs.com/mcp`；函数计算部署需确保端口开放 |
| | `command` / `args` | 仅限 `npx`/`uvx` 部署方式 | `["npx", "@modelcontextprotocol/server-memory"]` |
| **安全认证** | KMS 凭据 | 敏感凭证（如 `AMAP_MAPS_API_KEY`）必须通过阿里云 KMS 加密存储 | 控制台开通时强制启用，不可明文配置 |
| | `Authorization` Header | 外部 SDK 调用必需的认证头 | 格式为 `Bearer ${DASHSCOPE_API_KEY}`，需在客户端 `headers` 中显式设置 |
| **网络与权限** | 白名单 IP | 自定义 MCP 服务若访问云资源（如 RDS），需将百炼出口 IP 加入白名单 | `47.93.216.17`, `39.105.109.77` |

## 面向开发者的实用提示

- ✅ **快速起步**：优先使用 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 中的官方服务（如高德地图、夸克搜索），开通即用，无需部署。
- ✅ **企业集成**：用 Connector 接入钉钉/语雀/OSS 等，10 分钟内完成授权 → 自动生成 MCP 工具 → 智能体直接调用。
- ✅ **自定义服务**：推荐 `streamableHttp` 协议 + 函数计算部署；调试时可用 `curl -H "Authorization: Bearer <key>" https://xxx/mcp/tools` 验证服务可达性与工具列表。
- ❌ **避免踩坑**：  
  - 不要尝试在本地运行 MCP Server 并暴露到公网（安全性差、IP 不稳定）；  
  - 不要将 `Authorization` 以外的 Header（如 `X-Tenant-ID`）用于身份透传（平台会丢弃）；  
  - 不要复用同一套凭证连接多个不同权限范围的数据库实例（Connector 当前不隔离作用域）。

> 提示：所有 MCP 工具调用均计入应用 [Token](token.md) 消耗与计费，建议在工作流中结合条件节点控制调用时机，提升成本效益。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


