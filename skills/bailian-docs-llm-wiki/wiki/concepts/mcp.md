# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是百炼平台实现大模型与外部工具安全、标准化集成的核心通信机制。它基于开源 MCP 标准（[modelcontextprotocol.io](https://modelcontextprotocol.io/)），并升级为 Streamable HTTP 协议，统一抽象工具发现、调用、流式响应等交互过程，使大模型能在上下文驱动下自主或确定性地调用地图、搜索、数据库、SaaS 应用等能力，无需开发者编写定制化适配代码。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 不是独立服务，而是贯穿多个能力层的**协议层基础设施**，其使用严格绑定于具体应用形态：

- **智能体（Agent）应用**：MCP 作为“可调用工具集合”注入智能体。模型根据用户问题自动决策是否调用、调用哪个 MCP 工具（如 `amap_maps`）、传入哪些参数。单个智能体最多配置 5 个 MCP 服务，适用于动态、意图不确定的对话场景（例如：“帮我查上海明天的天气，并在地图上标出最近的咖啡馆”）。

- **工作流（Workflow）应用**：MCP 以显式节点形式存在（如 `mcp_weather`）。开发者需手动拖入节点、配置工具 ID、映射输入/输出字段（如将上游 `city` 字段传给 `location` 参数）。适用于执行路径固定、需精确控制时序与错误处理的编排场景（例如：先查天气 → 再调用图表生成 → 最后发邮件）。

- **Connector（数据连接中枢）**：所有通过 Connector 接入的系统（如钉钉文档、OSS、Salesforce、MySQL）均被自动封装为符合 MCP 协议的工具集。新增一个数据库连接器，即自动发布一组 `query_sql`、`list_tables` 等 MCP 工具，供智能体或工作流直接消费，无需额外开发。

- **插件（Plug-in）扩展**：自定义插件若选择“MCP 方式接入”，即等同于部署一个 MCP Server；官方插件（如 `quark_search`）和三方插件也通过 MCP 协议向智能体暴露能力。MCP 是插件能力被模型“看见”和“理解”的底层载体。

> ⚠️ 注意：MCP 服务**不可直接用于千问 API 的裸调用**（即不能在 `POST /api/v1/services/qwen-max` 请求中传入 `tools` 字段启用 MCP）。必须通过智能体、工作流或 Connector 等平台级应用容器承载。

## 关键参数和配置

MCP 的配置分为**服务注册时**（静态）与**运行调用时**（动态）两类，开发者需分别关注：

### 服务级参数（部署/注册时配置）
| 参数 | 必填 | 说明 |
|------|------|------|
| `type` | 是 | 协议类型，必须为 `"streamableHttp"`（百炼当前唯一支持类型，对应 `/mcp` 端点）；旧版 `"sse"` 已停用。 |
| `url` | 是 | MCP Server 的公网可访问地址（HTTPS），需 TLS 证书有效；常见错误码 `11200048`/`11200059` 多因域名不可达或证书异常导致。 |
| `name` | 是 | 工具组名称（如 `amap_maps`），将出现在智能体工具列表中，建议语义清晰、全局唯一。 |
| `description` | 是 | 工具功能描述（如“高德地图 POI 搜索与路径规划服务”），直接影响模型对工具适用性的判断准确率。 |

### 调用级参数（运行时由模型或工作流生成）
- **工具名（`tool.name`）**：必须与注册时 `name` 完全一致，大小写敏感。
- **输入 Schema（`tool.inputSchema`）**：JSON Schema 格式，定义参数名、类型、是否必填、示例值等；模型据此生成合法 JSON-RPC 请求体。
- **认证透传**：外部 SDK 或客户端调用时，需在请求头携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，百炼平台自动完成密钥校验与下游凭证注入（如 KMS 解密后的地图 AK/SK）。

## 面向开发者，简洁实用

- ✅ **快速起步**：开通官方 MCP 服务（如 [Amap Maps](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)）→ 在智能体编辑页「工具」中勾选 → 发送测试消息即可验证。
- ✅ **自定义部署**：推荐使用函数计算（FC）托管 Python/Node.js MCP Server，通过 `uvx` 或 `npx` 一键部署（仅支持公共 PyPI/npm 包）；避免本地部署（不支持访问本地资源）。
- ✅ **调试技巧**：在智能体 Playground 中开启「工具调用日志」，可查看模型生成的 `tool_calls` 及实际返回的 `tool_results`，快速定位参数不匹配或 Schema 定义偏差。
- ✅ **安全合规**：敏感凭证（API Key、[Token](token.md)）必须通过百炼 KMS 凭据管理，禁止硬编码；MCP Server 访问云数据库时，需配置 VPC 打通或 IP 白名单（FC 无固定出口 IP）。
- ❌ **避坑提醒**：  
  - 不要尝试在 DashScope SDK 的 `messages` 中手动拼接 `tool_calls` —— MCP 调用由平台内核自动触发；  
  - 不要复用旧版 SSE 协议的 MCP Server —— 百炼已强制升级至 Streamable HTTP，需重新开通服务；  
  - 不要将 MCP 与 RAG 知识库混淆 —— 前者调用实时 API，后者检索静态向量库，二者能力正交、可协同（如：先用 MCP 查实时股价，再用 RAG 查公司财报）。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [plug in](../guides/plug-in.md)
- [overview](../guides/overview.md)


