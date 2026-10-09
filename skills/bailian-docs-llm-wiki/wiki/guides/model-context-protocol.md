# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化接口协议，用于在大语言模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了工具接入的底层差异，使开发者无需为每个工具单独开发适配逻辑，即可在智能体、工作流或第三方客户端中统一调用。该协议基于 [MCP 官网](https://modelcontextprotocol.io/) 开源标准实现，并已升级为 Streamable HTTP 协议以支持更稳定的外部集成。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用能力需通过百炼平台的**智能体应用**或**工作流应用**触发。当前支持以下两类使用场景：

- **平台内集成**：在智能体中，模型根据对话上下文自动判断是否调用及调用哪个 MCP 工具（如 `maps_route`、`WebSearch.search`），最多可同时配置 5 个 MCP 服务；在工作流中，每个 MCP 节点需手动指定具体工具（如 `maps_weather`），并显式传递输入/输出参数。
- **外部调用**：支持通过标准 HTTP（Streamable HTTP）、SSE 或 CLI 集成至 Cherry Studio、Cursor 等第三方客户端，或通过 MCP SDK 在自有项目中编码调用。详情见 [外部调用](raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

官方已提供多种开箱即用的 MCP 服务，包括 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）等；同时也支持自定义部署，覆盖代码包（npx/uvx）、现有 RESTful API（通过 AI 网关封装）和阿里云 OpenAPI 三类来源。详见 [自定义 MCP 服务](raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 中提到“One Key MCP 服务首次调用自动生效”，但文档 3 明确要求“已开通用户需先取消再重新开通以升级协议”。二者存在矛盾——实际行为以协议升级为准：**所有存量 MCP 服务必须完成协议升级（即取消后重开通）才能使用新版 Streamable HTTP 接口**，否则外部调用将失败。

## 关键参数

MCP 服务配置与调用涉及以下核心参数：

- **服务类型标识**：决定传输协议与端点路径，必须严格匹配：
  - `"type": "sse"` → 对应 `/sse` 端点，使用 GET 方法；
  - `"type": "streamableHttp"` → 对应 `/mcp` 端点，使用 POST 方法；
  - 配置错误将导致 `11200058`（METHOD_NOT_ALLOWED）或 `11200059`（NOT_FOUND）错误（见 [MCP 常见问题](raw/application-user-guide/model-context-protocol/mcp-faq.md)）。
- **鉴权凭证**：统一使用百炼通用 API Key（`DASHSCOPE_API_KEY`），通过 `Authorization: Bearer <key>` 传入 HTTP Header；敏感参数（如 `AMAP_MAPS_API_KEY`）须通过 KMS 凭据加密。
- **工具级参数**：由 MCP 服务自身定义，例如 `maps_weather` 工具要求 `city: string`，`WebSearch.search` 要求 `query: string`；参数名与类型必须与 `list_tools()` 返回的 `inputSchema` 严格一致，否则触发 `11200060`（BAD_REQUEST）错误。

## 使用方式

### 平台内配置（智能体/工作流）
1. 进入 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage)，创建或导入 MCP 服务；
2. 在智能体/工作流编辑页的“工具”区域添加已部署服务；
3. 智能体无需额外配置，模型自动决策；工作流需在 MCP 节点中选择具体工具并绑定输入变量（如 `引用：信息提取/result`）。

### 外部调用
- **CLI 快速验证**：`bl mcp list` 查看服务列表，`bl mcp call --target WebSearch.search --args '{"query":"MCP最新进展"}'` 直接调用；
- **SDK 编程集成**：使用 `mcp.client.streamable_http` 客户端连接 `https://dashscope.aliyuncs.com/api/v1/mcps/<SERVICE_NAME>/mcp`，配合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)完成多轮工具调用（示例见 [外部调用](raw/application-user-guide/model-context-protocol/mcp-external-calls.md)）；
- **第三方客户端**：通过 MCP 广场的“一键配置”生成 JSON 配置，导入 Cherry Studio/Cursor 等。

## 限制和注意事项

- **网络与权限限制**：自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通；**无法访问本地资源**（如本地文件、硬件设备）。
- **部署与更新**：通过 `npx`/`uvx` 部署的服务版本固化，MCP Server 更新后**必须手动重新部署**；私有 npm/PyPI 仓库暂不支持，需发布至公共仓库。
- **计费模式差异**：
  - 官方云部署服务（如 WebSearch）按调用量计费（29 元/千次），含免费额度；
  - 自定义服务分“基础模式”（按调用时长计费，0.000156 元/秒）与“极速模式”（另加部署费用 0.000036 元/秒），后者适用于高频率调用场景。
- **协议兼容性**：所有外部调用必须使用新版 Streamable HTTP 协议（`/mcp` 端点），旧版 SSE 协议已停用；若服务配置为 `"sse"` 类型但指向 `/mcp` 地址，将触发 `11200054`（PROTOCOL_ERROR）。

> **注意**：文档 1 中“联网搜索MCP服务限流为 15 QPS”与文档 5 错误码 `11200051`（HTTP_RATE_LIMIT）描述的限流主体不一致——实际限流策略按**主账号及其 RAM 子账号共享**执行，非单服务实例级限流。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


