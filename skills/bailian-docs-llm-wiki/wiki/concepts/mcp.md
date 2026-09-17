# 模型上下文协议

模型上下文协议（Model Context Protocol，简称 MCP）是阿里云百炼平台提供的标准化、安全可扩展的工具调用协议，用于在大语言模型与外部能力（如地图、搜索、数据库、SaaS 应用等）之间建立统一、语义化的交互通道。它将异构服务抽象为符合 OpenAPI 规范的工具接口，使模型能基于自然语言意图自动发现、规划并调用合适工具，无需开发者编写定制化适配代码。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent）**：MCP 是核心工具调度层。模型根据用户输入（如“查杭州今天天气”）自主判断是否调用、调用哪个 MCP 工具、传入哪些参数；所有已开通的 MCP 服务对模型透明可见，最多可同时启用 5 个。Agent 2.0 将 MCP 工具与知识库、内置沙箱工具统一纳入“规划-执行-反思”链路，支持完整调用溯源。
  
- **工作流应用（Workflow）**：MCP 以独立节点形式存在（“MCP 节点”），需开发者手动选择具体工具（如 `maps_weather`）、显式配置输入参数（支持引用上游节点输出，如 `信息提取/result`），每个节点绑定且仅绑定一个工具，适用于确定性编排场景。

- **高代码应用（Rich Code）**：通过 `fastmcp.Client` SDK 在代码中直接调用 MCP 服务，支持 `list_tools()`、`call_tool()` 等标准方法，可灵活集成到自定义逻辑中，常用于需要精细控制或组合多个工具的复杂业务。

- **Connector 数据连接**：所有已配置的 App（如钉钉、Salesforce、MySQL、OSS）均通过统一的业务空间级 MCP 地址（`https://${workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/connector/mcp`）对外暴露工具能力，客户端只需配置一次地址与 API Key，即可自动发现并调用全部已连接数据源的工具，实现“一处接入、全域可用”。

- **外部 IDE 集成（如 Cherry Studio、Cursor）**：通过 MCP 协议标准 JSON 配置（含 `base_url` 和 `DASHSCOPE_API_KEY`），可一键接入百炼 MCP 服务，让本地开发环境具备与平台一致的工具调用能力。

> ⚠️ 注意：MCP **不支持**直接在千问系列模型的 OpenAI 兼容 API（如 `/v1/chat/completions`）中使用；必须通过百炼平台的智能体、工作流或高代码应用容器调用。

## 关键参数和配置

### 服务级配置（在 MCP 管理页设置）
- `type`：协议类型，**必须严格匹配端点** —— `"streamableHttp"`（推荐，对应 POST `/mcp` 端点）或 `"sse"`（旧版，对应 GET `/sse`）；配置错误将导致 `11200058` / `11200059` 错误。
- `command` 或 `url`：本地部署用 `npx mcp-server ...` 或 `uvx ...`；远程服务填完整 HTTP URL（如 `https://my-mcp-service.example.com/mcp`）。
- `env`：敏感凭证（如 `AMAP_MAPS_API_KEY`）**必须通过 KMS 凭据加密注入**，禁止明文填写。

### 调用级参数（由模型生成或工作流节点传递）
- `tool.name`：工具名称，须与 MCP 服务实际注册的 `name` 完全一致。
- `tool.inputSchema`：输入参数 Schema，须与服务暴露的 OpenAPI `requestBody` 完全兼容；不匹配将触发 `11200054`（协议解析失败）或 `11200060`（Bad Request）。
- 请求头：外部调用时**必须携带** `Authorization: Bearer ${DASHSCOPE_API_KEY}`，且 `base_url` 需指向正确的 MCP 地址（如 `https://dashscope.aliyuncs.com/api/v1/mcps/WebSearch/mcp`）。

### Connector 场景特有参数
- `workspaceId`：业务空间 ID（形如 `llm-xxxxxxxxxxxx`），用于构造 MCP 地址及资源隔离，必填且不可变更。
- 连接器名称与描述：影响模型工具选择准确性，建议描述具体用途（如“钉钉待办列表，用于查询未完成任务”）。

## 面向开发者，简洁实用

- ✅ **快速上手**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，一键开通官方服务（如 Amap Maps、WebSearch），再在智能体/MCP 节点中添加即可使用。
- ✅ **调试技巧**：用典型自然语言指令测试（如“从北京南站打车到首都机场”），观察日志中的 `tool_calls` 和 `tool_results` 字段，确认工具名、参数、返回结构是否符合预期。
- ✅ **自建 MCP 服务**：推荐使用 `streamableHttp` 协议 + `POST /mcp`，参考 [MCP SDK](https://github.com/aliyun/alibabacloud-mcp-sdk) 实现 `list_tools` 和 `call_tool` 接口；部署于函数计算（FC）时注意其无固定出口 IP，访问内网资源需配置 VPC 打通。
- ✅ **安全底线**：`DASHSCOPE_API_KEY` 和所有服务凭证**严禁硬编码、提交至 Git、发至聊天工具或工单**；务必通过环境变量或 KMS 注入。
- ❌ **明确限制**：MCP 服务无法访问本地文件、硬件设备或 localhost；不支持自定义 HTTP Header（除 `Authorization` 外）；旧版 SSE 协议已逐步淘汰，新项目请统一使用 `streamableHttp`。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)


