# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化机制，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用行为依赖于百炼平台内应用所配置的推理模型能力。当前仅支持在以下两类应用中使用：

- **智能体应用**：模型根据自然语言对话自动判断是否调用、调用哪个 MCP 工具及传入参数（如 `maps_route` 或 `web_search`），支持最多同时配置 5 个 MCP 服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需手动指定 MCP 节点使用的具体工具（如 `maps_weather`），并显式连接输入/输出参数；每个 MCP 节点仅能绑定一个工具 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

> **注意**：MCP 服务**不能**在直接调用千问 API（如 `qwen-max` 的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)）时接入；必须通过百炼平台的智能体或工作流应用容器使用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数类别 | 名称 | 说明 | 示例/约束 |
|----------|------|------|-----------|
| **服务配置** | `type` | 指定通信协议类型，必须与端点路径严格匹配 | `"sse"` → `/sse`；`"streamableHttp"` → `/mcp`（见错误码 11200058）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| | `url` | MCP Server 接入地址 | 必须可公网访问；若为函数计算部署，需确保下游服务开放对应端口 |
| | `command` / `args` | 仅限 `npx`/`uvx` 部署方式 | 如 `"npx"` + `["@modelcontextprotocol/server-memory"]` [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) |
| **安全与认证** | KMS 凭据 | 敏感参数（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 加密管理 | 云部署服务开通时强制启用 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md) |
| | `Authorization` Header | 外部 SDK 调用时必需 | 格式为 `Bearer ${DASHSCOPE_API_KEY}`，且需配置在 `streamablehttp_client` 的 `headers` 中 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) |

## 使用方式

### 1. 服务接入
- **官方服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，点击服务卡片 → **立即开通**（Amap Maps 等限时免费）。
- **自定义服务**：支持三种方式：
  - *脚本部署*：使用 `npx`/`uvx` 托管开源或自研 MCP Server（需发布至公共 npm/PyPI）；
  - *AI 网关导入*：将现有 RESTful API 封装为 MCP 工具；
  - *OpenAPI 导入*：将阿里云产品（如 OSS、ECS）操作封装为 MCP 工具 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

### 2. 应用内配置
- **智能体**：创建后在「MCP 服务」模块添加，模型自动调度（需提示词明确意图）。
- **工作流**：拖入「MCP 节点」→ 选择工具 → 通过「引用」绑定上游节点输出（如 `信息提取/result`）→ 配置下游处理。

### 3. 外部调用
- **第三方 IDE 集成**：支持 Cherry Studio、Cursor 一键配置（自动注入 `DASHSCOPE_API_KEY` 和 URL）。
- **SDK 编程集成**：使用 `mcp` SDK 连接 `streamable_http` 端点，配合 OpenAI SDK 实现多轮工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络限制**：自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **本地资源不可达**：不支持访问用户本地文件、硬件或数据库；需本地运行的服务请勿尝试云端部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：旧版 SSE 服务已升级为 Streamable HTTP；已开通用户需**取消再重新开通**以完成协议升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。
- **[Token](../concepts/token.md) 开销**：MCP 返回结果会作为上下文注入模型输入，直接增加输入 [Token](../concepts/token.md)；模型响应可能因信息更丰富而间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **版本更新**：`npx`/`uvx` 部署的服务版本更新后**不会自动生效**，必须手动重新部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


