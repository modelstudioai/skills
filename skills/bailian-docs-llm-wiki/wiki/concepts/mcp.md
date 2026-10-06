# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台定义的标准化上下文注入机制，用于在大模型推理过程中**按需、安全、可扩展地引入外部结构化数据**（如数据库查询结果、实时日志、知识库片段、SaaS 服务响应等），从而增强模型回答的准确性、时效性与业务相关性。该协议基于 JSON-RPC 2.0 规范设计，提供统一的服务契约与轻量集成接口，是百炼实现“模型+上下文+工具”协同推理的核心基础设施。

## 在百炼平台的不同场景中如何使用

MCP 不是独立服务，而是贯穿多个能力层的**上下文供给协议**，开发者可在以下典型场景中直接使用：

- **智能体（Agent）与工作流应用**：通过 `context` 或 `context_list` 字段在用户消息中声明 MCP 上下文源，模型自动加载并融合内容参与推理（例如：“请结合最新销售数据回答” → 自动调用 `mcp://sales-api/v1/recent-orders`）；
- **RAG 增强问答**：知识库检索结果可封装为 MCP 服务（如 `mcp://rag-kb.internal/{kb_id}/search?query=...`），替代传统静态 prompt 注入，支持动态重排、权限过滤与缓存控制；
- **Connector 集成**：百炼 Connector 本质是 MCP 服务框架——所有已接入的文件、数据库、OSS、Salesforce、语雀等系统，均被自动注册为符合 MCP 规范的工具端点，客户端只需配置 `mcp_url` 即可调用；
- **自定义插件扩展**：开发者可将自有 API 封装为 MCP 服务（返回标准 JSON-RPC `result`），发布后即可被任何支持 MCP 的模型（如 `qwen-plus`）原生识别和调用，无需额外工具声明；
- **应用组件 API 调用**：在 `messages` 中直接嵌入 `context` 对象，或通过 `tools` 字段声明 `mcp://...` 类型工具，触发协议解析与上下文加载。

> ✅ 关键区别：MCP 是**上下文数据的传输协议**，而插件（Plugin）是**动作执行的调用协议**；二者可协同使用（如 MCP 提供数据，插件执行计算），但不可互换。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `mcp_url` | string | 是 | 标准 MCP 服务地址，格式为 `mcp://<host>:<port>/<path>` 或 `mcp+https://...`；必须已在百炼 MCP 目录注册或白名单配置 | `"mcp://sales-api.internal/v1/recent-orders"` |
| `context_id` | string | 否 | 缓存键与链路追踪 ID；未提供时平台自动生成 UUID；建议业务侧设置有意义的值（如 `"kb_2024q3_policy"`） | `"sales_q3_2024"` |
| `timeout_ms` | integer | 否 | 单次请求超时毫秒数，默认 `3000`，上限 `10000` | `5000` |
| `retry_count` | integer | 否 | 失败重试次数，默认 `1`（v202409+ SDK 行为），最大 `2` | `1` |
| `context_list` | array | 否 | 替代单个 `context`，用于并发加载多个上下文（优先级更高）；数组元素结构同 `context` | `[{"mcp_url":"mcp://kb/faq"},{"mcp_url":"mcp://log/error-today"}]` |

⚠️ 注意事项：
- 单次请求最多 5 个 MCP 上下文项（`context` + `context_list` 合计）；
- 每个上下文响应解压后 ≤128 KB，超限将截断并告警；
- 响应必须为 JSON-RPC 2.0 格式，且 `result` 字段为 `string` 或 `object`（不支持 `array`）；
- 不传递 cookies 或 Authorization header；认证需通过 `mcp_url` 查询参数（如 `?token=xxx`）或服务端预置密钥完成。

## 面向开发者的实用提示

- **快速验证**：在请求 Header 中添加 `"debug": "true"`，可获取完整上下文加载日志（含耗时、状态码、原始响应），便于排查超时或格式错误；
- **降级保障**：MCP 服务不可用时自动跳过该上下文项，主推理流程不受影响——无需额外容错代码；
- **缓存控制**：利用 `context_id` + 平台默认 TTL（300s），或在 MCP 服务响应头中返回 `X-MCP-Cache-TTL: 60` 显式控制缓存生命周期；
- **调试工具**：使用 `curl` 直接调用 MCP 服务 URL（需带 `Content-Type: application/json` 和 `Accept: application/json`），验证其是否返回合法 JSON-RPC 响应；
- **生产就绪**：所有 `mcp_url` 必须提前在百炼控制台完成服务注册（Connector 场景自动注册），否则请求将被拒绝。

> 💡 最佳实践：优先使用 Connector 内置连接器（如 OSS、MySQL），避免重复开发；自定义 MCP 服务应遵循幂等设计，并在 `result` 中返回结构化对象（如 `{"data": [...], "meta": {"source": "sales_db", "freshness": "realtime"}}`），便于模型理解上下文语义。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [plug in](../guides/plug-in.md)
- [application component api reference](../api/application-component-api-reference.md)
- [rag api](../api/rag-api.md)


