# model context protocol

模型上下文协议（Model Context Protocol, MCP）是 Anthropic 提出的开源标准协议，用于在大模型与外部工具之间搭建统一的信息传递通道。阿里云百炼基于 MCP 协议提供官方与自定义两类 MCP 服务，使智能体和[工作流](../concepts/workflow.md)应用能够接入海量第三方工具，无需为每个工具单独编写接口。详见 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 支持的服务类型

阿里云百炼支持两类 MCP 服务：

- **官方 MCP 服务**：由百炼官方部署，开通后即可使用。既可在平台内部（智能体、[工作流](../concepts/workflow.md)）直接集成，也支持通过外部调用集成至第三方应用。当前 Amap Maps 等服务限时免费。详见 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义 MCP 服务**：用户自行部署，提供三种方式：
  1. **使用脚本部署**：面向代码包，托管于函数计算 FC。支持 `npx`（Node.js）、`uvx`（Python）启动本地 stdio 服务，或通过 `http` 连接远程 MCP 服务器。
  2. **从 AI 网关导入**：面向已有 RESTful API，将非 MCP 规范的业务接口封装为 MCP 服务。
  3. **从阿里云 OpenAPI 导入**：面向阿里云生态，使大模型可操作 OSS、ECS 等云产品。

详见 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

## 使用方式

### 在智能体中配置

智能体根据输入对话自动判断是否调用 MCP 服务。单个智能体最多可同时添加 5 个 MCP 服务，常用于路径规划、逐步推理、图表绘制等多工具协同场景。

### 在[工作流](../concepts/workflow.md)中配置

工作流中每个 MCP 节点只能使用一个工具，需手动指定输入参数并把输出传递到下一个节点。典型流程为：开始节点 → 大模型节点（将自然语言解析为 MCP 输入参数）→ MCP 节点（调用工具）→ 大模型节点（整理输出）→ 结束节点。

### 外部调用

MCP 服务可集成至第三方应用（Cherry Studio、Cursor）或个人项目：

- **第三方应用**：在 MCP 服务详情页的「外部调用」界面选择目标应用，支持一键自动配置或手动从 JSON 导入。
- **SDK 集成**：通过 MCP SDK（如 Qwen Agent 框架）调用，使用 Streamable HTTP 协议，配置 `mcpServers` 中的 `type: streamable-http` 和带 `Authorization` 头的 `url`。

> **注意**：百炼 MCP 服务已从旧版 SSE 协议升级为新版 Streamable HTTP 协议。已开通用户需在 MCP 广场「取消开通」后重新「立即开通」以完成升级。详见 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## [计费](../concepts/billing.md)说明

### 云部署 MCP 服务

- **部署费用**：限时免部署费用。
- **调用费用**：部分 MCP 服务涉及第三方 API 调用，费用由第三方收取，百炼不收取。
- **联网搜索 MCP**：免费额度 2000 次，额度用尽后按 29 元/千次[计费](../concepts/billing.md)，限流 15 QPS（主账号与 RAM 子账号共享）。

### 自定义部署 MCP 服务

根据响应速度提供两种模式：

| 模式 | 部署费用 | 调用费率 | 适用场景 |
| --- | --- | --- | --- |
| 基础模式 | 无 | 0.000156 元/秒 | 偶尔调用，可承受冷启动延迟 |
| 极速模式 | 0.000036 元/秒（部署时长） | 0.000156 元/秒（调用时长） | 长时间在线、频繁调用 |

## 关键参数与配置

自定义 MCP 服务的配置代码遵循 `mcpServers` 结构：

- `type`：`stdio`（本地托管）或 `sse`/`streamableHttp`（远程连接）。
- `command`/`args`：npx/uvx 启动命令与参数。
- `env`：环境变量。
- `url`：远程 MCP 服务地址。

部署后仅支持编辑服务名称和描述；修改部署方式、地域、安装方式或配置代码须先停止部署再重新部署。

## 限制和注意事项

- **本地资源不可访问**：MCP 服务托管在函数计算 FC，无固定出口公网 IP，无法访问用户本地数据库。访问远程云资源需配置 FC 的 IP 白名单或进行 VPC 网络打通。
- **私有仓库不支持**：保存在私有 npm 仓库的 MCP Server 无法部署，须发布到公共仓库或改用 SSE 连接。
- **版本不自动更新**：npx/uvx 部署的服务在源版本更新后需手动重新部署。
- **仅主账号及授权 RAM 用户可访问**：自定义 MCP 服务不会被其他账号使用。
- **[Token](../concepts/token.md) 消耗增加**：调用 MCP 会将工具返回内容作为上下文传入模型，导致输入 [Token](../concepts/token.md) 增加，并可能间接增加输出 [Token](../concepts/token.md)。
- **不能直接接入千问 API**：MCP 服务只能在智能体或工作流应用中使用，不能在直接调用千问 API 时接入。
- **调用准确性依赖提示词**：模型需明确指令才能准确调用 MCP，建议在提示词中写明工具名称与能力；若仍无效可更换更强的推理模型（如千问 3 系列）。

## 常见错误码

| 错误码 | 含义 | 排查方向 |
| --- | --- | --- |
| 11200044 MCP_CONNECTION_REFUSED | 连接被拒绝 | `curl` 测试连通性，确认服务已启动、端口与防火墙 |
| 11200045 MCP_CONNECTION_TIMEOUT | 连接建立超时 | 重试 2~3 次，检查网关/防火墙 IP 白名单 |
| 11200046 MCP_REQUEST_TIMEOUT | 响应超时 | 重试；拆分业务或异步化；npx/uvx 可切极速模式 |
| 11200048 MCP_SSL_ERROR | TLS/SSL 握手失败 | 检查证书有效期与域名匹配，关闭代理直连测试 |
| 11200049 MCP_SERVER_HTTP_UNAUTHORIZED | HTTP 401 | 核对鉴权方式，正确添加 Authorization 头 |
| 11200051 MCP_HTTP_RATE_LIMIT | HTTP 429 | 降低频率，按 Retry-After 重试或申请配额 |
| 11200054 MCP_PROTOCOL_ERROR | 协议解析失败 | 确认 `type` 与端点路径匹配：`sse` 对应 `/sse`，`streamableHttp` 对应 `/mcp` |
| 11200057 MCP_INIT_TIMEOUT | 初始化超时 | 核对接入地址与传输方式，反向代理需启用长连接 |

完整错误码列表与排查方案详见 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)

















