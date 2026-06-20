# model context protocol

模型上下文协议（Model Context Protocol, MCP）是连接大模型与外部工具的标准化协议。通过 MCP，开发者无需为每个外部工具编写专用接口，阿里云百炼的智能体和工作流应用即可接入海量第三方工具能力。百炼同时支持官方预部署的 MCP 服务和用户自定义部署的 MCP 服务。

## MCP 服务类型

百炼提供两类 MCP 服务：

- **官方 MCP 服务**：百炼官方预部署的云端服务（如 Amap Maps、Sequential Thinking、QuickChart、Firecrawl 等），开通即用，无需自行部署。详细开通和使用流程参见 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义 MCP 服务**：支持三种部署方式——使用脚本部署（npx/uvx/http）、从 AI 网关导入、从阿里云 OpenAPI 导入。完整的部署指南参见 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 在百炼应用中使用 MCP

### 智能体应用

在智能体中，大模型根据用户输入自动判断是否调用 MCP 服务。核心步骤：

1. 创建智能体应用。
2. 在智能体配置中添加 MCP 服务（最多同时添加 **5 个**）。
3. 大模型自动选择合适的 MCP 服务完成任务。

典型场景包括：单 MCP 路线规划（Amap Maps）、逐步推理（Sequential Thinking）、多 MCP 组合（天气查询 + 图表绘制）。

### 工作流应用

工作流中每个 MCP 节点只能使用一个工具，需要手动指定输入参数并串联节点。典型流程：

1. 开始节点接收用户输入。
2. 大模型节点提取结构化参数（如城市名称）。
3. MCP 节点调用对应工具（如 `maps_weather`）。
4. 大模型节点汇总结果为自然语言。
5. 结束节点输出。

## 外部调用

MCP 服务不仅限于百炼平台内使用，还支持集成至第三方应用或个人项目。详细的外部调用方式参见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

### 集成至第三方应用

支持一键自动配置到 **Cherry Studio** 和 **Cursor**：

- 在百炼 MCP 广场进入对应服务的外部调用界面，选择目标应用并点击一键配置。
- 也支持手动复制 JSON 配置文件导入。

### 通过 SDK 开发集成

通过 MCP SDK（Streamable HTTP 协议）调用百炼 MCP 服务，编码更灵活。调用地址格式：

```
https://dashscope.aliyuncs.com/api/v1/mcps/<service-name>/mcp
```

请求头需携带 `Authorization: Bearer <DASHSCOPE_API_KEY>`。支持 Qwen Agent 等框架直接集成。

## 自定义部署方式

### 使用脚本部署

通过函数计算 FC 托管 MCP 服务代码：

| 安装方式 | 适用场景 |
|---------|---------|
| **npx** | Node.js 开发的 MCP 服务 |
| **uvx** | Python 开发的 MCP 服务 |
| **http** | 连接已有的远程 MCP 服务器 |

配置示例（npx）：

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

> **注意**：并非所有本地端 MCP Server 都能在百炼云端部署，需要访问本地资源（如文件、硬件）的服务无法在云端运行。

### 从 AI 网关导入

将已有的非 MCP 规范的 RESTful API 通过 AI 网关封装为 MCP 服务，然后导入百炼。

### 从阿里云 OpenAPI 导入

通过 OpenAPI 开发者门户将阿里云产品的 OpenAPI（如 OSS、ECS）发布为 MCP 服务并导入百炼。

## 计费说明

### 官方云部署 MCP 服务

- **部署费用**：限时免部署费用。
- **调用费用**：部分服务涉及第三方 API 调用，该费用由第三方收取。
- **联网搜索 MCP 服务**：免费额度 2000 次，超出后按 29 元/千次计费，限流 15 QPS（主账号与 RAM 子账号共享）。

### 自定义部署 MCP 服务

| 模式 | 部署费 | 调用费 | 适用场景 |
|------|-------|-------|---------|
| **基础模式** | 无 | 0.000156 元/秒 | 偶尔调用，对启动速度要求不高 |
| **极速模式** | 0.000036 元/秒 | 0.000156 元/秒 | 频繁调用，需长时间保持在线 |

> **注意**：调用 MCP 服务会增加模型的输入和输出 Token 消耗。MCP 返回的内容作为上下文传递给模型，直接增加输入 Token；更丰富的上下文也可能导致模型生成更详细的响应，间接增加输出 Token。

## 协议升级

百炼 MCP 服务已从旧版 SSE 协议升级为新版 **Streamable HTTP** 协议。已开通旧版服务的用户需要取消开通后重新开通以完成升级。配置时需确认 `type` 与端点路径匹配：`"sse"` 对应 `/sse`，`"streamableHttp"` 对应 `/mcp`。

## 常见问题

- **无法连接 MCP 服务**：确认已开通/升级服务、API Key 有效、额度未用尽。
- **模型无法调用 MCP**：在提示词中明确工具名称和能力描述，或更换更强的推理模型（如千问 3 系列）。
- **自定义部署失败**：确认服务本地可运行、支持云端托管、配置代码正确、函数计算 FC 权限已开通。
- **版本更新**：通过 npx/uvx 部署的服务不会自动更新，需手动重新部署。
- **无法访问远程资源**：MCP 服务托管在函数计算 FC，无固定出口公网 IP，需配置 IP 白名单或 VPC 网络打通。
- **MCP 能否在调用千问 API 时接入**：不可以，MCP 服务需集成在智能体或工作流应用中使用。

完整的错误码及排查方案参见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 安全机制

百炼对云部署 MCP Server 采取安全策略保障数据安全，敏感数据在创建时使用 KMS 进行加密管理。自定义部署的 MCP 服务仅限用户自己的阿里云主账号及授权 RAM 用户访问，不会被他人使用。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


