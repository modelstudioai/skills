# model context protocol

模型上下文协议（Model Context Protocol, MCP）是阿里云百炼平台提供的标准化工具集成机制，用于在大模型推理过程中安全、高效地调用外部能力（如地图、天气、网页爬取、知识图谱等）。它屏蔽了底层接口差异，使开发者无需为每个工具单独开发适配逻辑，即可在智能体、工作流或第三方客户端中统一接入和管理工具服务。

## 支持的模型/功能

MCP 本身不绑定特定大模型，而是作为上下文增强通道与百炼平台内所有支持工具调用的模型协同工作，包括通义千问系列（如 Qwen-Max、Qwen-Plus）等。其核心能力体现在三类服务接入方式：

- **官方 MCP 服务**：由阿里云预部署并托管的即开即用服务，例如 Amap Maps（地理信息）、WebSearch（联网搜索）、Sequential Thinking（逻辑推理）、QuickChart（图表生成）等，开通后可直接在智能体或工作流中配置使用 [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **自定义 MCP 服务**：支持三种部署路径：
  - *使用脚本部署*：通过 `npx`（Node.js）或 `uvx`（Python）一键托管开源或自研 MCP Server（如 Knowledge Graph Memory）；
  - *从 AI 网关导入*：将现有 RESTful API 封装为 MCP 工具；
  - *从阿里云 OpenAPI 导入*：将 OSS、ECS 等云产品能力暴露为可调用工具 [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)。
- **外部客户端兼容**：遵循标准 Streamable HTTP 协议，支持与 Cherry Studio、Cursor 等主流 MCP 客户端集成，实现跨平台工具复用 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

> **注意**：文档 2 中提到“智能体和工作流应用已支持接入两种 MCP 服务”，该表述已过时；实际支持官方、自定义（含三种方式）及外部客户端接入，详见文档 1 和文档 3。

## 关键参数

MCP 服务配置与调用涉及以下关键参数：

- **服务类型标识**：`type` 字段必须与接入端点严格匹配——`"sse"` 对应 `/sse` 端点（GET），`"streamableHttp"` 对应 `/mcp` 端点（POST），配置错误将导致 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED`（错误码 11200058）等协议级失败 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。
- **环境变量与密钥**：
  - 敏感凭证（如 `AMAP_MAPS_API_KEY`）需通过 KMS 凭据加密，不可明文配置；
  - 外部调用需设置 `DASHSCOPE_API_KEY` 环境变量；
  - 自定义服务中 `env` 字段用于注入运行时环境变量（如 `YOUR_ENV_KEY`）。
- **部署模式参数**：
  - `基础模式`：按调用时长计费（0.000156 元/秒），无部署费用，适合低频场景，但存在冷启动延迟；
  - `极速模式`：额外收取部署时长费用（0.000036 元/秒），服务常驻，适用于高并发、低延迟要求场景。

## 使用方式

### 平台内集成（智能体/工作流）
- **智能体应用**：在创建智能体时，最多可添加 5 个 MCP 服务；大模型根据对话自动判断是否调用及选择工具（如发送“从杭州萧山国际机场到杭州西湖景区”触发 Amap Maps 路径规划）[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)。
- **工作流应用**：每个 MCP 节点仅支持一个工具，需手动指定输入参数（如通过前置大模型节点提取城市名传入 `maps_weather` 工具），并串联输出至后续节点完成结果整合。

### 外部调用
- **第三方应用集成**：支持 Cherry Studio、Cursor 一键自动配置，或手动导入 JSON 配置（含服务名称、URL、认证方式）。
- **SDK 编码集成**：使用 `mcp` Python SDK 连接 `streamablehttp_client`，结合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)实现多轮工具调用循环，适用于深度定制场景 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)。

## 限制和注意事项

- **网络与资源限制**：
  - 自定义 MCP 服务托管于函数计算 FC，**无法访问用户本地数据库或硬件资源**；
  - 访问远程云资源（如 RDS）需配置 FC IP 白名单或 VPC 打通；
  - 云部署 MCP 服务默认限流 15 QPS（主账号与 RAM 子账号共享）。
  
- **协议与兼容性**：
  - 百炼 MCP 已全面升级为 **Streamable HTTP 协议**，旧版 SSE 协议服务需重新开通以完成升级 [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)；
  - 不支持私有 npm/PyPI 仓库部署，自研包须发布至公共仓库（npm/PyPI）或改用 SSE 远程连接。

- **安全与运维**：
  - 敏感参数（API Key、Token）必须通过 KMS 加密，禁止硬编码；
  - 自定义服务版本更新后需**手动重新部署**，不会自动同步；
  - 推荐启用函数计算日志服务，便于排查 `MCP_CONNECTION_REFUSED`（11200044）、`MCP_INIT_TIMEOUT`（11200057）等常见错误 [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)。

- **Token 开销**：MCP 返回结果将作为上下文注入模型输入，**显著增加输入 Token 数量**；复杂响应也可能间接提升输出 Token 消耗。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/model-context-protocol/mcp-faq.md)


