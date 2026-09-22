# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化、安全、可扩展的工具调用协议，用于在大模型与外部能力（如地图、搜索、数据库、SaaS 应用等）之间建立统一通信通道。它基于开源 MCP 标准（[modelcontextprotocol.io](https://modelcontextprotocol.io/)）实现，并深度集成百炼平台的权限、网络、计费与运维体系，使开发者无需编写底层适配代码，即可声明式接入和编排各类外部工具。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 是百炼平台级能力，**仅适用于智能体应用和工作流应用内部**，不支持直接在调用 `qwen-*` 系列 API 的独立 SDK 场景中使用（例如通过 DashScope SDK 直接发起 MCP 调用会失败）。

- **智能体应用**：  
  大模型根据自然语言对话内容自主判断是否调用 MCP 工具（如“查北京地铁末班车时间” → 自动触发 `Amap Maps` 的 `maps_subway` 工具）。开发者只需在智能体配置中「添加已开通的 MCP 服务」，最多支持同时启用 5 个服务。工具调用完全由模型规划，输入参数自动提取，输出结果无缝融入对话上下文。

- **工作流应用**：  
  需显式拖入「MCP 节点」，手动选择工具（如 `WebSearch` 的 `search`），并配置输入参数。参数必须引用上游节点（如大模型节点或变量节点）的结构化输出（例如 `"引用：信息提取/result"`），支持 JSON Schema 校验。输出可传递至下游节点进行格式转换、条件判断或聚合，适合确定性高、需精确控制执行路径的业务流程。

- **Connector（数据连接器）**：  
  所有 Connector（如 OSS、Salesforce、语雀、钉钉、文件/表格连接器）均通过 MCP 协议统一暴露工具。创建连接后，系统自动生成标准化工具（如“列出 OSS Bucket 中的 PDF 文件”“查询 Salesforce 中的客户线索”），无需额外开发。这些工具可被智能体或工作流直接调用，实现“零数据迁移、实时访问原系统”。

- **插件（Plug-in）生态**：  
  官方插件（如 `quark_search`、`code_interpreter`）和三方/自定义插件，均可发布为 MCP 服务供智能体或工作流调用。自定义插件需先完成「发布为 MCP 服务」操作，才能在智能体的 MCP 配置列表或工作流的 MCP 节点中被发现和选用。

> ⚠️ 注意：MCP 服务不能在调用千问 API（如 `qwen-max`）的纯推理请求中直接接入；它必须依托于百炼平台的应用容器（智能体/工作流）运行。

## 关键参数和配置

MCP 配置分为两类，需分别关注：

### 服务级参数（部署/开通时配置）
| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `type` | string | 必填。指定 MCP 服务端点类型，决定协议行为。当前仅支持 `"streamableHttp"`（对应 `/mcp` 端点），旧版 `"sse"` 已停用。 | `"streamableHttp"` |
| `url` | string | 可选（官方服务无需填写）。自定义服务的远程地址，需 HTTPS、TLS 证书有效且网络可达。 | `"https://my-mcp-server.example.com/mcp"` |
| `env` | object | 敏感环境变量（如 API Key、[Token](token.md)），**必须通过 KMS 凭据加密注入**，禁止明文填写。 | `{"AMAP_MAPS_API_KEY": "kms://xxx"}` |
| `command` / `args` | string / array | 仅自定义服务（脚本部署）需配置，用于启动本地 MCP Server。 | `"npx"` + `["@modelcontextprotocol/server-memory"]` |

### 调用级参数（运行时传递）
| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `tool.name` | 工具唯一标识符，由 MCP Server 声明，客户端必须严格匹配。 | 如 `amap_maps.maps_weather`、`oss.list_objects` |
| `tool.inputSchema` | JSON Schema 定义的输入参数结构，客户端须按此格式构造 `input` 字段。 | 不符合 Schema 将导致 400 错误；工作流中需确保变量引用类型匹配（如字符串字段不可传入对象） |
| `DASHSCOPE_API_KEY` | 所有 MCP 请求必须携带的鉴权凭证，置于 `Authorization: Bearer <key>` 请求头。 | 该 Key 需具备对应业务空间的 `bailian:McpInvoke` 权限 |
| `workspaceId` | 业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于构造 MCP 服务根地址及权限隔离。 | 控制台自动注入；外部 SDK 集成时需显式配置 |

## 面向开发者，简洁实用

- ✅ **快速上手**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，一键开通 Amap Maps、WebSearch 等官方服务，3 分钟内即可在智能体中测试“杭州天气”类 query。
- ✅ **自定义服务三步走**：① 用 `npx @modelcontextprotocol/server-memory` 启动本地服务；② 在控制台「自定义 MCP 服务」中填写 URL 和环境变量（KMS 加密）；③ 发布后，在智能体或工作流中选择使用。
- ✅ **调试技巧**：开启智能体/工作流的「详细日志」，查看 `mcp_call` 日志条目，确认工具名、输入参数、HTTP 状态码（如 11200048 表示 URL 不可达，11200058 表示 `type` 配置错误）。
- ✅ **安全红线**：所有敏感凭证（API Key、[Token](token.md)、OAuth Secret）必须通过 KMS 加密；禁止硬编码、禁止提交至 Git；轮转凭证时需重建连接器或身份验证配置。
- ✅ **避坑提示**：  
  - 自定义服务升级后需**手动重新部署**，不会自动同步；  
  - 工作流中 MCP 节点的输入必须为合法 JSON，空字符串、`null` 或未定义变量将导致调用失败；  
  - 函数计算（FC）托管的自定义服务无固定出口 IP，访问 VPC 内资源需配置 VPC 打通而非 IP 白名单。

MCP 的本质是「让大模型像调用函数一样调用世界」——你只需关注「要什么能力」，百炼负责「怎么安全、稳定、合规地拿到它」。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [plug in](../guides/plug-in.md)
- [application component api reference](../api/application-component-api-reference.md)
- [frameworks](../api/frameworks.md)


