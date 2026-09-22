# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化机制，用于在大模型与外部工具（如地图、搜索、数据库等）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配逻辑，即可在智能体或工作流中声明式接入多种能力。该协议基于 Anthropic 提出的开源标准 [MCP 官网](https://modelcontextprotocol.io/) 实现，并针对百炼平台进行了工程化增强和云服务集成。

## 支持的模型/功能

MCP 协议本身不绑定特定模型，但其能力需通过百炼平台的**智能体应用**和**工作流应用**触发与执行。当前支持以下两类使用场景：

- **智能体应用**：大模型根据自然语言对话自动判断是否调用 MCP 服务及具体工具（如 `maps_route`, `maps_weather`），支持最多同时配置 5 个 MCP 服务 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式添加 MCP 节点并手动指定工具（如 `Amap Maps` 的 `maps_weather`），输入参数须由上游节点（如大模型节点）结构化提取，输出参数可传递至下游节点进行后处理。

支持的服务类型包括：
- **官方 MCP 服务**：阿里云百炼预部署并托管的云服务，如 Amap Maps（地理信息）、Firecrawl（网页爬取）、WebSearch（联网搜索）等，开通即用 [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。
- **自定义 MCP 服务**：支持三种部署方式：① 使用脚本（npx/uvx）部署开源或自研 MCP Server；② 通过 AI 网关将现有 RESTful API 封装为 MCP 工具；③ 通过 OpenAPI 开发者门户将阿里云产品（如 OSS、ECS）操作发布为 MCP 服务 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。

> **注意**：文档 4 明确指出“MCP 服务不能在调用千问 API 时直接接入”，而文档 5 的 FAQ 第 3 条却称“MCP 服务能否在调用千问 API 时接入？不可以”。二者一致，但需强调：MCP 是百炼平台级能力，**仅限于智能体/工作流应用内部使用，不适用于直接调用 `qwen-*` 系列 API 的独立 SDK 场景**。

## 关键参数

MCP 服务配置涉及两类关键参数：

- **服务级参数（部署时配置）**：
  - `type`：必须与接入端点匹配，`"sse"` 对应 `/sse`，`"streamableHttp"` 对应 `/mcp`（见错误码 11200058）；
  - `command` / `args`：如 `"npx"` + `["@modelcontextprotocol/server-memory"]`；
  - `env`：敏感环境变量（如 `AMAP_MAPS_API_KEY`）需通过 KMS 凭据加密管理，不可明文填写 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)；
  - `url`：远程服务地址，需确保网络可达且 TLS 证书有效（见错误码 11200048）。

- **调用级参数（运行时传递）**：
  - 工具名（`tool.name`）与输入 Schema（`tool.inputSchema`）由 MCP Server 声明，客户端（如智能体）需严格遵循；
  - 外部调用时需提供 `DASHSCOPE_API_KEY` 及 `Authorization` 请求头；
  - 工作流中 MCP 节点的输入必须引用上游节点输出（如 `"引用：信息提取/result"`），格式错误将导致调用失败。

## 使用方式

### 平台内集成（推荐）
1. **开通服务**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps）→ 点击“立即开通”；
2. **配置到应用**：
   - *智能体*：创建/编辑智能体 → “添加 MCP 服务” → 从已开通列表选择，最多 5 个；
   - *工作流*：拖入 MCP 节点 → 选择工具 → 在配置中设置输入参数（支持变量引用）；
3. **测试验证**：使用典型 query 测试（如“查询杭州天气”），观察日志确认工具调用成功。

### 外部调用（第三方集成）
- **一键配置**：支持 Cherry Studio、Cursor 等 IDE，通过控制台“外部调用”页点击“一键配置”自动注入服务元数据；
- **SDK 编程集成**：使用 `mcp` Python SDK 连接 `streamableHttp` 端点，配合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)实现多轮工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限限制**：
  - 自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)；
  - 不支持访问用户本地资源（如本地文件、硬件设备）；
  - 敏感凭证（API Key）必须通过 KMS 加密，禁止明文配置。

- **协议与兼容性**：
  - 百炼已全面升级至 **Streamable HTTP 协议**（非旧版 SSE），已开通用户需重新开通以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)；
  - 自定义服务若使用 `npx`/`uvx` 部署，版本更新后**必须手动重新部署**，不会自动同步。

- **计费与限流**：
  - 官方服务（如 WebSearch）有免费额度（2000 次/月），超量后按 29 元/千次计费；
  - 云部署服务限流为 **15 QPS**（主账号与 RAM 子账号共享）；
  - 自定义服务分“基础模式”（按调用时长计费，0.000156 元/秒）和“极速模式”（另收部署费 0.000036 元/秒），冷启动延迟仅存在于基础模式。

- **调试建议**：
  - 遇到连接失败（如错误码 `11200044`），优先执行 `curl <服务地址>` 测试连通性；
  - 部署失败时，检查函数计算 FC 权限、主账号欠费状态及配置代码语法（尤其 JSON 格式）；
  - 智能体调用失败，首先优化提示词明确工具意图，其次尝试升级模型（如切换至 Qwen3）。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


