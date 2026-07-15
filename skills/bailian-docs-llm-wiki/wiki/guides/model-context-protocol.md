# model context protocol

模型上下文协议（Model Context Protocol, MCP）是 Anthropic 提出的开源标准协议，用于在大模型与外部工具之间搭建统一的信息传递通道。阿里云百炼基于 MCP 提供全周期服务：开发者无需为每个外部工具编写专用接口，即可让智能体、工作流应用接入海量第三方工具，也能通过外部调用集成到第三方应用或个人项目中。

## 服务类型

百炼将 MCP 服务分为两大类，均需先在 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通或部署后使用：

- **官方 MCP 服务**：百炼官方云端部署，开通即用（如 Amap Maps、Sequential Thinking、QuickChart、联网搜索 WebSearch 等）。详见 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义 MCP 服务**：由开发者自行部署，支持三种方式（详见 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)）：
  - **使用脚本部署**：面向遵循 MCP 协议的代码包，托管到函数计算 FC，支持 `npx`（Node.js）、`uvx`（Python）、`http`（远程服务）三种安装方式。
  - **从 AI 网关导入**：把已有的 RESTful API 通过 AI 网关升级为 MCP 服务后导入。
  - **从阿里云 OpenAPI 导入**：通过 OpenAPI 开发者门户将官方 OpenAPI 发布为 MCP 服务，用于操作 OSS、ECS 等阿里云产品。

## 使用方式

MCP 服务既可在平台内部集成，也可通过外部调用集成到第三方应用。

### 平台内部：智能体与工作流

- **[智能体应用](../concepts/agent-application.md)**：大模型根据对话内容自动判断是否调用 MCP 服务，单个智能体最多可同时添加 **5 个** MCP 服务。适合路径规划、逻辑推理、多工具组合（如天气查询 + 图表绘制）等场景。
- **工作流应用**：每个 MCP 节点只能使用一个工具，需手动指定输入参数并将输出传递到下一节点。通常需先用大模型节点把自然语言解析为 MCP 工具所需的输入参数（在 System Prompt 中描述工具的名称、功能、输入输出格式），再接入 MCP 节点。

> **注意**：在工作流中仅使用单一工具（如 Amap Maps 的 `maps_weather`）时，工作流只能回答与该工具相关的问题。

### 外部调用

百炼 MCP 服务支持集成到第三方应用或个人项目，详见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)：

- **集成至第三方应用**：支持一键自动配置或手动配置到 Cherry Studio、Cursor 等客户端。手动配置需获取 `DASHSCOPE_API_KEY` 并替换配置文件中的对应变量。
- **集成至个人项目**：通过 MCP SDK 灵活编码。可结合 OpenAI SDK 调用百炼 MCP 服务，典型端点如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`，鉴权使用 `Authorization: Bearer <DASHSCOPE_API_KEY>`。

## 关键参数与配置

- **传输协议**：`type` 字段须与端点路径一致，`"sse"` 对应 GET `/sse`，`"streamableHttp"` 对应 POST `/mcp`。配置不匹配会触发 405/404 等错误。
- **自定义服务配置示例**（脚本部署）：

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

- **敏感信息加密**：涉及敏感数据的服务在创建时使用 KMS 凭据加密管理。
- **部署后可修改项**：部署完成后仅支持编辑服务名称和描述；修改部署方式、地域、安装方式或服务配置须先停止部署再重新部署。

> **注意**：百炼 MCP 服务已从旧版 SSE 协议升级为新版 **Streamable HTTP** 协议。已开通用户需在 MCP 广场执行"取消开通 → 立即开通"完成协议升级；SDK 调用请使用 `streamablehttp_client` 连接。

## 计费

- **云部署 MCP 服务**：限时免部署费用；部分服务涉及第三方 API 调用，费用由第三方收取。联网搜索 MCP 服务免费额度 2000 次，用尽后按 29 元/千次计费，限流 15 QPS（主账号与 RAM 子账号共享）。
- **自定义部署 MCP 服务**：
  - **基础模式**：无部署费用，按调用时长计费（0.000156 元/秒），首次调用有冷启动延迟，适合偶尔调用。
  - **极速模式**：有部署费用（0.000036 元/秒）+ 调用费用（0.000156 元/秒），适合长时间在线、调用频繁的场景。

## 限制与注意事项

结合 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)，接入时需注意以下限制：

- **不能直连千问 API**：MCP 服务必须集成在智能体或工作流应用中使用，无法在直接调用千问 API 时接入。
- **无法访问本地资源**：自定义 MCP 服务托管在函数计算 FC，暂不支持访问用户本地数据库、文件、硬件等资源；需要访问本地资源的 MCP Server 建议在本地部署。
- **访问远程资源需配置网络**：FC 无固定出口公网 IP，访问云数据库等远程资源需配置 FC 的 IP 白名单或打通 VPC 网络。
- **仓库与版本限制**：私有 npm 仓库暂不支持，需发布到公共仓库或改用 SSE；通过 npx/uvx 部署的服务在源版本更新后不会自动更新，需手动重新部署。
- **调用增加 Token 消耗**：MCP 返回的内容会作为上下文传入模型，增加输入 Token，并可能间接增加输出 Token。
- **调用失败排查**：优先确认已开通/升级服务、API Key 有效、额度未用尽；若模型无报错但不调用工具，应在提示词中明确工具名称与能力，必要时更换更强的推理模型（如千问 3 系列）。自定义服务的连接、超时、鉴权、协议等错误可对照 `11200044`~`11200060` 系列错误码逐项排查。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)



