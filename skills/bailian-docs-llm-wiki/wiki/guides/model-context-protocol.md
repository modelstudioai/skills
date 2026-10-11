# model context protocol

Model Context Protocol（MCP）是阿里云百炼平台提供的标准化工具接入协议，用于在大模型应用（如智能体、工作流）与外部能力（如地图、天气、搜索、知识图谱等）之间建立安全、可扩展的信息通道。它屏蔽了底层接口差异，支持官方托管服务与自定义服务双轨接入，并统一通过 Streamable HTTP 或 SSE 协议进行通信。开发者无需为每个工具单独开发适配层，即可快速集成和编排多源能力。

## 支持的模型/功能

MCP 服务本身不绑定特定大模型，但其调用效果高度依赖所配置的推理模型能力：
- **智能体应用**：支持自动决策调用（需模型具备强工具理解与规划能力），最多同时启用 5 个 MCP 服务；典型场景包括路径规划（Amap Maps）、逻辑推理（Sequential Thinking）、多工具协同（天气+图表绘制）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：需显式指定 MCP 节点使用的具体工具（如 `maps_weather`），并手动连接输入/输出参数；适用于确定性任务链路，如“自然语言解析 → 天气查询 → 结果摘要”[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **外部客户端**：支持 Cherry Studio、Cursor 等主流 MCP 客户端，通过标准协议对接百炼托管的 MCP 服务 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：MCP 服务**不能直接接入千问 API 的裸调用**（如 `dashscope.ChatCompletion.create`），仅限百炼平台内智能体/工作流或外部 MCP 客户端使用 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

## 关键参数

| 参数 | 说明 | 示例/约束 |
|------|------|-----------|
| `DASHSCOPE_API_KEY` | 百炼通用 API Key，用于所有官方 MCP 服务鉴权（One Key 类型无需额外密钥） | 必须设置为环境变量或请求 Header `Authorization: Bearer <key>` |
| `mcp_url` | MCP Server 地址，格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/{service-name}/mcp`（Streamable HTTP）或 `/sse`（SSE） | 需与客户端协议类型严格匹配；错误配置将导致 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED`（错误码 11200058）[MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md) |
| `tool.name` | 工具名称，由 MCP 服务定义，调用时必须精确匹配 | 如 `maps_weather`, `web_search`；模型提示词中建议显式提及该名称以提升调用准确率 |
| `tool.inputSchema` | 工具输入参数 Schema（JSON Schema 格式），SDK 自动转换为 OpenAI `tools` 格式 | 必须与服务实际接口一致，否则触发 `MCP_SERVER_HTTP_BAD_REQUEST`（错误码 11200060） |

## 使用方式

1. **开通服务**  
   - One Key 类型（如 Amap Maps 试用版）：首次调用自动生效，无需手动开通。  
   - 非 One Key 类型：需前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 点击“立即开通”；已开通用户升级协议需先“取消开通”再重新开通 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

2. **平台内集成**  
   - **智能体**：应用创建后，在“MCP 服务”配置页添加服务（最多 5 个），模型根据对话自动调度。  
   - **工作流**：拖入 MCP 节点，选择具体工具，通过“引用”语法（如 `信息提取/result`）绑定上游输出为输入参数 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

3. **外部调用**  
   - **CLI**：`bl mcp list` 查看服务，`bl mcp call --target amap-maps.maps_weather --city "杭州"` 直接调用。  
   - **SDK**：使用 `mcp.client.streamable_http` 连接，配合 OpenAI SDK 的 `tools` 调用循环实现多轮交互（参考 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 中 Python 示例）。

## 限制和注意事项

- **网络与权限**：自定义 MCP 服务（如 npx/uvx 部署）运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通；**无法访问用户本地资源（文件、硬件）** [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。  
- **协议兼容性**：百炼已全面升级至 **Streamable HTTP 协议**（替代旧版 SSE），新部署服务必须使用 `/mcp` 端点；若混用 `type: "sse"` 与 `/mcp` 路径，将触发 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED` 错误 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。  
- **Token 开销**：MCP 返回结果会作为上下文注入模型输入，**显著增加输入 Token 消耗**；复杂响应可能间接推高输出 Token 量 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。  
- **版本管理**：通过 npx/uvx 部署的自定义服务，**版本更新后需手动重新部署**，不会自动同步 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。  
- **敏感数据**：涉及密钥等敏感参数（如 `AMAP_MAPS_API_KEY`），必须通过 KMS 凭据加密，禁止明文写入配置 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


