# Model Context Protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台用于连接大模型与外部工具的标准化协议。通过 MCP，开发者无需为每个外部工具编写复杂接口，即可在智能体和工作流应用中接入海量第三方工具能力。MCP 基于 Anthropic 提出的开源标准，百炼平台在此基础上提供了云部署、自定义部署和外部调用等多种集成方式。

## 支持的 MCP 服务类型

根据 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) 的介绍，百炼平台支持两大类 MCP 服务：

- **官方 MCP 服务**：百炼官方预部署的 MCP 服务（如 Amap Maps、Sequential Thinking、QuickChart、联网搜索等），开通后即可使用。
- **自定义 MCP 服务**：支持三种部署方式——使用脚本部署（npx/uvx/http）、从 AI 网关导入、从阿里云 OpenAPI 导入。

## 使用方式

### 平台内部集成

MCP 服务可在百炼平台的**智能体应用**和**工作流应用**中使用：

| 应用类型 | 特点 | 限制 |
|---------|------|------|
| 智能体应用 | 大模型根据对话自动判断是否调用 MCP 服务 | 最多同时添加 5 个 MCP 服务 |
| 工作流应用 | 每个 MCP 节点手动指定一个工具，串联输入输出 | 需通过大模型节点做自然语言与参数的转换 |

> **注意**：MCP 服务**不能**在直接调用千问 API 时接入，必须集成在智能体或工作流应用中使用。

### 外部调用集成

如 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 所述，百炼 MCP 服务也支持集成至第三方应用或个人项目：

- **第三方应用**：支持一键配置到 Cherry Studio、Cursor 等客户端。
- **SDK 开发集成**：通过 MCP SDK（如 Qwen Agent 框架）编码调用，支持 Streamable HTTP 协议。

MCP 服务的接入地址格式为：
```
https://dashscope.aliyuncs.com/api/v1/mcps/<service-name>/mcp
```

调用时需在请求头中携带百炼 API Key 进行鉴权：
```json
{
  "headers": {
    "Authorization": "Bearer <your-api-key>"
  }
}
```

> **注意**：百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议。已开通用户需先取消开通再重新开通以完成升级。

### 自定义 MCP 服务部署

根据 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) 的说明，自定义部署支持以下安装方式：

- **npx**：适用于 Node.js 开发的 MCP 服务（需发布到公共 npm 仓库）
- **uvx**：适用于 Python 开发的 MCP 服务（需发布到 PyPI 仓库）
- **http**：连接已部署的远程 MCP 服务器（SSE 或 Streamable HTTP）

配置模板示例：
```json
{
  "mcpServers": {
    "本地 MCP 服务": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@your_acc_name/your_pkg_name"],
      "env": { "YOUR_ENV_KEY": "YOUR_ENV_VALUE" }
    },
    "远程 MCP 服务": {
      "type": "sse/streamableHttp",
      "url": "https://your-mcp-server/sse"
    }
  }
}
```

## 计费说明

### 官方云部署 MCP 服务

- **部署费用**：限时免费
- **调用费用**：部分服务涉及第三方 API 调用，由第三方收取
- **联网搜索 MCP**：免费额度 2000 次，超出后 29 元/千次，限流 15 QPS（主账号与 RAM 子账号共享）

### 自定义部署 MCP 服务

| 模式 | 部署费 | 调用费 | 适用场景 |
|------|--------|--------|---------|
| 基础模式 | 无 | 0.000156 元/秒 | 偶尔调用，对启动延迟不敏感 |
| 极速模式 | 0.000036 元/秒 | 0.000156 元/秒 | 频繁调用，需低延迟 |

## 限制和注意事项

- **调用 MCP 会增加 Token 消耗**：MCP 返回的内容作为上下文传入模型，会增加输入 Token；更丰富的上下文也可能导致输出 Token 增加。
- **智能体调用 MCP 依赖提示词质量**：需在提示词中明确工具名称和能力描述。若效果不佳，可更换更强的推理模型（如千问 3 系列）。
- **自定义 MCP 服务不保证始终可用**：第三方 MCP 服务商可能修改或关闭服务。
- **不支持访问本地资源**：云部署的 MCP 服务无法访问用户本地数据库、文件等。
- **访问远程资源需配置网络**：MCP 服务托管在函数计算 FC 上，无固定出口公网 IP，需为远程数据库等配置 IP 白名单或 VPC 网络打通。
- **私有仓库暂不支持**：npx/uvx 部署方式仅支持公共仓库。
- **版本更新需手动重新部署**：通过 npx/uvx 部署的服务不会自动更新。
- **安全隔离**：自定义 MCP 服务仅限部署者的阿里云主账号及授权 RAM 用户访问。

常见错误码及排查方案请参考 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)







