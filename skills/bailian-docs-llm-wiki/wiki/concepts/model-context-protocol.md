# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol，简称 MCP）是阿里云百炼平台定义的**标准化工具接入与调用协议**，用于在大模型应用（如智能体、工作流）与外部能力（地图、天气、搜索、数据库、知识库、SaaS 系统等）之间建立安全、统一、可扩展的上下文交互通道。它抽象了底层接口差异，将各类能力封装为符合 OpenAI `tools` 语义的标准化工具，使模型能基于自然语言理解自动规划、参数化调用，并支持流式响应与多轮协同。

## 在百炼平台的不同场景中，这个概念如何使用

MCP 是百炼平台能力集成的**统一协议层**，贯穿多个核心能力模块，具体使用方式因场景而异：

- **智能体（Agent）应用**：  
  在智能体配置页添加 MCP 服务后，模型（如 `qwen-max`、`qwen-plus`）可基于对话上下文**自主决策是否调用、调用哪个工具、传入哪些参数**。例如：“查杭州今天天气并画成折线图”，模型自动串联 `maps_weather` + `text_to_image` 两个 MCP 工具。单个智能体最多启用 5 个 MCP 服务。

- **工作流（Workflow）应用**：  
  需显式拖入 **MCP 节点**，手动选择具体工具（如 `amap-maps.maps_weather`），并通过“引用语法”（如 `用户输入/城市`）绑定上游节点输出作为输入参数。适用于逻辑确定、需精确控制执行顺序的链路。

- **知识库（Knowledge Base）集成**：  
  百炼知识库的“检索服务”和“问答服务”均通过 MCP 协议对外暴露，客户端（如 Cherry Studio）或第三方 Agent 框架可直接发现并调用 `knowledge_search` 或 `knowledge_qa` 工具，实现 RAG 能力即插即用。

- **Connector（数据连接器）**：  
  所有已创建的 Connector 实例（如 OSS、MySQL、语雀、钉钉文档）均自动注册为 MCP 工具，统一暴露在 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp` 地址下。无需为每个系统单独开发适配器，一次配置，全域可用。

- **插件（Plug-in）体系**：  
  官方插件（如 `quark_search`、`code_interpreter`）、三方插件及自定义插件，**发布后即自动注册为 MCP 服务**。开发者在插件市场开通或发布插件，即完成 MCP 接入，可在智能体/工作流中直接使用其 `tool.name`。

> ⚠️ 注意：MCP 服务**不支持裸调用 DashScope 原生 API**（如 `dashscope.ChatCompletion.create`），仅限百炼平台内智能体/工作流，或标准 MCP 客户端（如 Cursor、Cherry Studio、Qoder）调用。

## 关键参数和配置

| 参数 | 说明 | 必填 | 示例/约束 |
|------|------|------|-----------|
| `DASHSCOPE_API_KEY` | 百炼通用鉴权密钥，用于所有官方 MCP 服务（One Key 类型除外） | ✅ | 设置为环境变量或 HTTP Header `Authorization: Bearer <key>` |
| `mcp_url` | MCP Server 地址，必须与协议类型严格匹配 | ✅ | Streamable HTTP：`https://dashscope.aliyuncs.com/api/v1/mcps/{service-name}/mcp`；SSE（已逐步淘汰）：`/sse`；错误路径触发 `11200058` 错误码 |
| `workspaceId` | Connector 类 MCP 的必需路由标识（形如 `llm-xxxxxxxxxxxx`） | ✅（仅 Connector） | 从百炼控制台业务空间页获取，用于资源隔离与权限管控 |
| `tool.name` | 工具唯一标识符，调用时必须精确匹配 | ✅ | 如 `maps_weather`、`knowledge_search`、`oss_get_object`；建议在提示词中显式提及以提升调用准确率 |
| `tool.inputSchema` | JSON Schema 格式定义的输入参数结构 | ✅ | SDK 自动转换为 OpenAI `tools` 格式；字段名、类型、必填性必须与后端接口一致，否则触发 `11200060` 错误码 |

## 面向开发者，简洁实用

- ✅ **快速上手**：开通服务 → 复制 `mcp_url` 和 `tool.name` → 在智能体/工作流中添加或在 SDK 中声明 `tools` 数组即可调用。  
- ✅ **调试优先**：使用 CLI 命令快速验证：`bl mcp list` 查看可用服务，`bl mcp call --target amap-maps.maps_weather --city "杭州"` 直接触发调用。  
- ✅ **协议兼容**：推荐使用 **Streamable HTTP（`/mcp` 端点）**，性能更优、错误码更明确；避免混用 SSE 配置与 `/mcp` 路径。  
- ✅ **安全边界**：自定义 MCP 服务运行于函数计算（FC），**无固定出口 IP**，访问云数据库等需配置白名单或 VPC；**无法访问本地文件、硬件或用户设备**。  
- ✅ **命名规范**：为 Connector 或自定义 MCP 服务设置清晰名称（如 `"杭州气象服务"` 而非 `"connector1"`），显著提升模型工具选择准确率。  
- ✅ **错误排查**：高频错误码速查：`11200058` → 检查 `mcp_url` 协议与路径是否匹配；`11200060` → 校验 `inputSchema` 是否与实际接口一致；`130022` → 检查 Object 类型参数子属性是否为空。  

> 💡 提示：所有 MCP 工具均可被主流开源框架（如 LangChain、LlamaIndex、AgentScope）原生支持——只需配置标准 MCP Server 地址，无需额外适配代码。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [knowledge base](../guides/knowledge-base.md)
- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)


