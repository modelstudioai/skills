# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化机制，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 服务**不直接绑定特定大模型**，而是通过百炼平台的智能体（Agent）和工作流（Workflow）应用间接驱动。当前支持以下两类使用场景：

- **智能体应用**：大模型根据对话上下文自动判断是否调用、调用哪个 MCP 工具及传入参数。单个智能体最多可同时配置 5 个 MCP 服务（见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。典型用例包括路径规划（Amap Maps）、逻辑推理（Sequential Thinking）、多工具协同（天气查询 + 图表生成）。
  
- **工作流应用**：需手动指定 MCP 节点使用的具体工具（如 `maps_weather`），并显式连接输入/输出参数。适用于确定性高、需精确控制执行链路的场景（见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。

> **注意**：MCP 服务**不能直接接入千问 API 的裸调用**。文档 5 明确指出：“MCP 服务需集成在智能体或工作流应用中使用，不能直接在调用千问 API 时接入”。

## 关键参数

MCP 服务配置涉及两类关键参数：

- **服务级参数**（部署时设置）：
  - `type`：必须与接入端点匹配，`"sse"` 对应 `/sse`，`"streamableHttp"` 对应 `/mcp`（见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）；
  - `command` / `args`：用于脚本部署（如 `npx` 或 `uvx`），需严格匹配目标 MCP Server 的启动方式（见[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)）；
  - `url`：远程服务地址，必须可公网访问且 TLS 证书有效（错误码 11200048/11200059 常与此相关）。

- **调用级参数**（运行时由模型生成）：
  - 工具名（`tool.name`）和输入 Schema（`tool.inputSchema`）由 MCP Server 动态提供，智能体/工作流节点需据此构造合法 JSON-RPC 请求；
  - 外部 SDK 调用时，需将 `DASHSCOPE_API_KEY` 作为 `Authorization: Bearer <key>` 透传（见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）。

## 使用方式

### 1. 接入官方 MCP 服务
- 前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通（如 Amap Maps、WebSearch），开通后即支持智能体/工作流内直接选择；
- 敏感配置（如 API Key）需通过 KMS 凭据加密管理（见[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)）。

### 2. 部署自定义 MCP 服务
支持三种方式：
- **脚本部署**：适用于开源或自研 MCP Server（Node.js/Python），通过函数计算 FC 托管（`npx`/`uvx`）；
- **AI 网关导入**：将现有 RESTful API 封装为 MCP 工具；
- **OpenAPI 导入**：将阿里云产品（OSS/ECS）操作发布为 MCP 工具（见[自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)）。

### 3. 外部调用
- **第三方应用集成**：一键配置至 Cherry Studio、Cursor 等客户端；
- **SDK 编程集成**：使用 `mcp` Python SDK + [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用（示例代码见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）。

## 限制和注意事项

- **网络与权限限制**：
  - 自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通（见[常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）；
  - **不支持访问本地资源**（如本地文件、硬件设备），此类服务需本地部署（见[常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。

- **协议与兼容性**：
  - 百炼已全面升级至 **Streamable HTTP 协议**（非旧版 SSE），已开通用户需取消再重新开通以完成升级（见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）；
  - `npx`/`uvx` 部署仅支持发布至**公共 npm/PyPI 仓库**的包，私有仓库暂不支持（见[常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）。

- **计费与限流**：
  - 云部署服务：联网搜索类有免费额度（2000 次/月），超量后 29 元/千次；Amap Maps 当前限时免费；
  - 自定义部署：基础模式按调用时长计费（0.000156 元/秒），极速模式另收部署费（0.000036 元/秒）（见[模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)）；
  - 全局限流：部分服务（如联网搜索）限 15 QPS，主账号与 RAM 子账号共享。

- **调试与排障**：
  - 常见错误码（如 `11200044` 连接拒绝、`11200054` 协议解析失败）需结合 `curl` 测试、FC 日志及下游服务文档排查（见[常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)）；
  - 模型无法调用 MCP 时，优先检查提示词是否明确工具名称与能力，而非仅依赖模型自主推理（见[外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）。

> **注意**：文档 1 中“部署费用：限时免部署费用”与文档 3 中“极速模式有部署费用”存在表述差异。实际计费以文档 1 的明细为准：极速模式部署费率明确为 0.000036 元/秒，所谓“限时免”仅针对特定活动期，非永久策略。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


