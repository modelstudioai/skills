# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是一种开源标准协议，用于在大模型与外部工具之间建立统一的信息传递通道。在阿里云百炼平台中，开发者无需为每个外部工具编写专用接口，即可通过 MCP 让智能体和工作流应用接入海量第三方工具。百炼同时提供官方预部署的 MCP 服务和自定义部署能力，并支持通过外部调用将 MCP 服务集成至第三方应用。

## 核心概念

MCP 在百炼平台中分为两类服务：

- **官方 MCP 服务**：由百炼官方部署在云端，开通即可使用，包括 Amap Maps（地理信息）、Sequential Thinking（逻辑推理）、QuickChart（图表生成）、Firecrawl（网页爬取）、联网搜索等。详见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义 MCP 服务**：支持开发者部署自有或开源社区的 MCP 服务，提供三种部署方式——使用脚本部署（npx/uvx/http）、从 AI 网关导入、从阿里云 OpenAPI 导入。详见[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 支持的应用类型

### 智能体应用

在智能体中，大模型根据用户输入自动判断是否调用 MCP 服务。一个智能体最多可同时添加 **5 个 MCP 服务**。模型会根据对话上下文自动选择合适的工具，支持单 MCP 和多 MCP 协同调用。

### 工作流应用

在工作流中，每个 MCP 节点只能使用一个工具，需要手动指定输入参数并将输出传递到下一个节点。典型流程为：大模型节点（提取参数） → MCP 节点（调用工具） → 大模型节点（整理结果） → 输出节点。

## 自定义部署方式

根据[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)文档，百炼提供以下三种自定义部署路径：

| 部署方式 | 适用场景 | 安装方式 |
|---------|---------|---------|
| 使用脚本部署 | 拥有 MCP 协议代码包（自研或开源） | npx（Node.js）/ uvx（Python）/ http（远程） |
| 从 AI 网关导入 | 已有非 MCP 规范的 RESTful API | 通过 AI 网关将 API 升级为 MCP 服务 |
| 从阿里云 OpenAPI 导入 | 操作阿里云产品（OSS、ECS 等） | 通过 OpenAPI 开发者门户发布 |

使用脚本部署时，MCP 服务托管在函数计算 FC 上。配置代码格式示例：

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

> **注意**：并非所有 MCP 服务都支持 npx/uvx/http 方式部署。如果缺少相应配置代码，需参考 MCP 官方文档进行本地部署。Java 开发的 MCP 服务需先自行部署到函数计算，再通过 http 方式托管到百炼。

## 外部调用

百炼 MCP 服务支持通过外部调用集成至第三方应用或个人项目，详见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。主要有两种方式：

- **集成至第三方应用**：支持一键配置到 Cherry Studio 和 Cursor，自动或手动导入配置即可使用。
- **通过 SDK 开发集成**：使用 MCP SDK（如 Qwen Agent 框架）编码调用百炼 MCP 服务，通过 Streamable HTTP 协议连接，URL 格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/<service-name>/mcp`，需在 Headers 中携带百炼 API Key 进行鉴权。

> **注意**：百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议。已开通用户需取消开通后重新开通以完成协议升级。

## 计费说明

### 官方云部署 MCP 服务

- **部署费用**：限时免部署费用。
- **调用费用**：部分服务涉及第三方 API 调用（费用由第三方收取）。联网搜索 MCP 服务免费额度 2000 次，超出后按 29 元/千次计费，限流 15 QPS（主账号与 RAM 子账号共享）。

### 自定义部署 MCP 服务

| 模式 | 部署费 | 调用费 | 适用场景 |
|------|-------|-------|---------|
| 基础模式 | 无 | 0.000156 元/秒 | 偶尔调用，可接受冷启动延迟 |
| 极速模式 | 0.000036 元/秒 | 0.000156 元/秒 | 需持续在线、快速响应 |

## 限制与注意事项

- 智能体最多同时添加 **5 个 MCP 服务**。
- 工作流中每个 MCP 节点只能使用**一个工具**。
- MCP 服务**不能**在直接调用千问 API 时接入，必须通过智能体或工作流应用使用。
- 自定义 MCP 服务托管在函数计算 FC，**无固定出口公网 IP**，访问远程资源（如云数据库）需配置 IP 白名单或 VPC 网络打通。
- 自定义服务**无法访问用户本地资源**（文件、硬件等）。
- 通过 npx/uvx 部署的服务，上游版本更新后需**手动重新部署**。
- 调用 MCP 会增加模型的输入和输出 Token 消耗。
- 私有 npm 仓库中的 MCP Server 暂不支持部署，需发布到公共仓库或改用 http 连接。
- 安全方面，云部署 MCP Server 的敏感数据使用 KMS 加密管理；自定义部署的 MCP 服务仅限本账号及授权 RAM 用户访问。

## 常见问题排查

- **无法连接**：确认已开通/升级服务、API Key 有效、额度未用尽。
- **模型不调用 MCP**：在提示词中明确指定工具名称和能力描述。
- **部署失败**：确认本地可运行、服务可云端托管、配置代码正确、函数计算权限已开通。
- **协议错误（MCP_PROTOCOL_ERROR）**：确认配置中 `type` 与端点路径匹配——`"sse"` 对应 `/sse`，`"streamableHttp"` 对应 `/mcp`。

完整错误码及排查方案请参考 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)




