# model context protocol

[模型上下文协议](../concepts/mcp.md)（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化工具集成机制，用于在大模型与外部服务（如地图、天气、网页爬取、知识图谱等）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，使开发者无需为每个工具单独编写适配代码，即可在智能体、工作流或第三方应用中统一调用。MCP 基于开源 [MCP 协议标准](https://modelcontextprotocol.io/) 实现，并已升级为 Streamable HTTP 协议以提升兼容性与稳定性 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用效果高度依赖所配置的推理模型能力：

- **智能体应用**：支持自动识别用户意图并动态选择、调用多个 MCP 服务（最多 5 个），适用于多步推理场景（如“鸡兔同笼”逻辑推演）、多工具协同（如“查杭州天气 + 绘制折线图”）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需手动指定 MCP 节点使用的具体工具（如 `maps_weather`），并显式传递输入/输出参数，适用于确定性流程编排 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部客户端**：支持通过 Cherry Studio、Cursor 等主流 MCP 客户端一键接入，亦可通过 SDK 在自有项目中深度集成 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：MCP 服务**不能直接接入千问 API 的原始调用链路**；必须部署在百炼平台的智能体或工作流应用内使用，或通过外部 MCP 客户端/SDK 集成 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 | 示例/约束 |
|----------|--------|------|-----------|
| **服务配置** | `type` | 指定通信协议类型，必须与后端端点路径严格匹配 | `"sse"`（对应 `/sse`）、`"streamableHttp"`（对应 `/mcp`） |
| | `url` | MCP Server 地址（HTTP/SSE） | `https://your-mcp-server/sse` 或 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp` |
| | `command` / `args` | 仅限脚本部署（npx/uvx）：启动命令及参数 | `"npx"`, `["-y", "@modelcontextprotocol/server-memory"]` |
| **认证与安全** | `Authorization` header | 外部调用时必需，格式为 `Bearer <DASHSCOPE_API_KEY>` | 必须配置有效百炼 API Key |
| | KMS 凭据 | 敏感参数（如 `AMAP_MAPS_API_KEY`）需通过 KMS 加密存储 | 云部署 MCP 服务开通时自动引导创建 |
| **工具级** | `inputSchema` | 工具输入参数的 JSON Schema 定义 | 决定大模型能否正确生成调用参数，影响调用成功率 |

## 使用方式

1. **开通服务**  
   - 访问 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，选择服务（如 Amap Maps），点击“立即开通”。  
   - **新用户**：直接开通；**已开通旧版 SSE 服务用户**：需先“取消开通”，再重新“立即开通”以升级至 Streamable HTTP 协议 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

2. **平台内集成**  
   - **智能体**：创建应用 → “添加 MCP 服务” → 从已开通列表中勾选（最多 5 个）→ 测试对话触发自动调用。  
   - **工作流**：拖入 MCP 节点 → 手动选择具体工具（如 `maps_weather`）→ 配置输入参数（支持引用上游节点输出）→ 连接下游节点处理结果 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

3. **外部集成**  
   - **第三方应用**：在 MCP 服务详情页选择 Cherry Studio/Cursor → 点击“一键配置”或手动导入 JSON 配置。  
   - **自定义开发**：使用 `mcp` SDK（如 `streamablehttp_client`）连接 MCP Server，获取工具列表后，结合 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（如 `qwen-max`）实现多轮工具调用循环 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与权限**：自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通；**无法访问本地文件、硬件或数据库** [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **协议兼容性**：务必确保 `type`（`sse`/`streamableHttp`）与后端 URL 路径（`/sse`/`/mcp`）严格一致，否则将报错 `11200058`（METHOD_NOT_ALLOWED）或 `11200059`（NOT_FOUND） [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **[Token](../concepts/token.md) 开销**：MCP 返回结果会作为上下文注入模型输入，**显著增加输入 [Token](../concepts/token.md) 数量**；模型响应可能因信息更丰富而变长，间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **版本管理**：通过 `npx`/`uvx` 部署的服务，**不会随上游包更新自动升级**，需手动重新部署 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **计费差异**：云部署服务按调用时长计费（基础/极速模式），而官方服务（如 Amap Maps）试用期免费，联网搜索等则按调用次数计费（2000 次/月免费额度） [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


