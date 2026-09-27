# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是阿里云百炼平台提供的标准化、安全、可扩展的工具集成机制，用于在大模型与外部服务（如地图、天气、数据库、SaaS 应用、文件系统等）之间建立统一的信息通道。它基于开源 [MCP 协议标准](https://modelcontextprotocol.io/) 实现，并已升级为 **Streamable HTTP 协议**，显著提升兼容性、稳定性与流式调用体验。

## 在百炼平台的不同场景中如何使用

MCP 不是独立服务，而是贯穿百炼核心能力的“连接层”，其使用方式因场景而异，开发者需按需选择：

- **智能体应用（Managed Agents）**：  
  在创建智能体时，通过「添加 MCP 服务」从已开通列表中勾选最多 5 个服务（如 `amap_weather`、`oss_file_search`）。无需手动指定工具或参数——大模型会根据用户问题自动识别意图、生成结构化调用请求并解析响应。适用于多步推理、多工具协同等开放场景（例如：“查上海今天气温，并用历史数据画趋势图”）。

- **工作流应用（Workflow）**：  
  拖入「MCP 节点」后，需**显式选择具体工具**（如 `database_query`）、配置输入参数（支持引用上游节点输出），并连接下游节点处理结果。流程确定、可控性强，适合企业级确定性编排（例如：用户提交表单 → 查询订单库 → 写入 CRM → 发送通知）。

- **实时语音交互（Omni Realtime API）**：  
  在 `tools` 数组中声明 MCP 工具，`type` 必须设为 `"mcp"`，并提供 `server_url`（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`）。注意：**MCP 工具调用与 `enable_search` 互斥，不可同时启用**。适用于语音助手、会议纪要等低延迟多模态场景。

- **百炼 Connector（统一连接平台）**：  
  Connector 将各类数据源（OSS、MySQL、Salesforce、腾讯文档等）封装为标准 MCP 工具。开发者只需在控制台创建连接器，即可自动生成 `search_files`、`execute_sql` 等工具供智能体调用。所有调用均通过固定 MCP URL（`https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`）路由，数据不落盘、实时访问、权限隔离。

- **外部客户端集成（Cherry Studio / Cursor / 自研 SDK）**：  
  支持通过标准 MCP 客户端一键接入，或使用 `mcp` 官方 SDK（如 `streamablehttp_client`）在自有项目中深度集成。需配置 `MCP Server URL` 和 `Authorization: Bearer <DASHSCOPE_API_KEY>`，即可发现工具、发起调用、处理流式响应。

> ⚠️ 注意：MCP 服务**不能直接接入千问原始 API（如 `/v1/services/aigc/text-generation`）**；必须通过智能体、工作流、Omni Realtime、Connector 或外部 MCP 客户端调用。

## 关键参数和配置

| 参数类别 | 参数名 | 说明 | 开发者须知 |
|----------|--------|------|------------|
| **协议与地址** | `type` | 必填。指定通信协议类型，**必须与后端 URL 路径严格匹配**：<br>• `"sse"` → 对应 `/sse` 路径<br>• `"streamableHttp"` → 对应 `/mcp` 路径 | 错配将导致 `11200058`（METHOD_NOT_ALLOWED）或 `11200059`（NOT_FOUND）错误 |
| | `url` | MCP Server 的完整 HTTP/SSE 地址 | • 智能体/工作流中填写控制台生成的官方服务 URL<br>• Connector 固定为 `https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`<br>• 外部调用需确保域名可公网访问 |
| **认证与安全** | `Authorization` header | 必填。格式为 `Bearer <DASHSCOPE_API_KEY>` | 使用百炼平台获取的有效 DashScope API Key；**严禁硬编码或明文提交至代码仓库** |
| | 敏感凭证（如 `AMAP_MAPS_API_KEY`） | 需通过百炼 KMS 加密存储 | 控制台开通服务时自动引导创建；函数计算托管的自定义 MCP 服务也需通过 KMS 注入 |
| **工具定义** | `inputSchema` | JSON Schema 格式的输入参数定义 | **直接影响大模型能否正确生成调用参数**。务必准确描述字段名、类型、必填项、枚举值等，否则调用成功率大幅下降 |
| | `workspaceId` | 业务空间 ID（形如 `llm-xxxxxxxxxxxx`） | 所有 Connector 类 MCP 调用必需，用于资源路由与隔离；必须与创建连接器的空间一致 |

## 面向开发者的实用建议

- ✅ **优先使用 Streamable HTTP**：新接入服务请务必选择 `type: "streamableHttp"` + `/mcp` 路径，兼容性更好、错误码更明确、支持完整流式响应。
- ✅ **调试从 `inputSchema` 入手**：若工具调用失败且参数为空，90% 原因为 `inputSchema` 描述不准确（如漏写 `required` 字段、类型写错）。建议用 [JSON Schema Validator](https://jsonschemalint.com/) 验证。
- ✅ **敏感参数走 KMS**：API Key、数据库密码、OAuth Secret 等**绝不可出现在配置界面明文框或代码中**，必须通过百炼 KMS 凭据管理。
- ✅ **网络限制早规划**：自建 MCP 服务部署在函数计算（FC），**无固定出口 IP**。若需访问 VPC 内数据库或带白名单的 SaaS，必须提前配置 VPC 打通或放行 FC 公网出口 IP 段。
- ✅ **路径错误是 404 主因**：Connector 的 MCP URL 必须为 `/api/v2/connector/mcp`（不是 `/api/v1/...` 或 `/mcp`），少一个字符即返回 404。
- ❌ **不要尝试绕过 MCP 层**：MCP 是百炼平台强制的工具调用入口，无法通过普通 HTTP 请求直连后端服务，也无法在千问基础 API 中透传自定义 Header（除 `Authorization` 外）。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application support](../guides/application-support.md)
- [managed agents api](../api/managed-agents-api.md)


