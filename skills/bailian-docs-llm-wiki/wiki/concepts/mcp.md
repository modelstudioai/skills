# 模型上下文协议

模型上下文协议（Model Context Protocol, MCP）是百炼平台提供的标准化、可扩展的工具集成协议，用于在大语言模型与外部能力（如搜索、地图、数据库、API 等）之间建立安全、声明式的信息通道。它不依赖特定模型，而是由平台层统一实现协议交互逻辑，使模型作为“协议消费者”参与工具选择、参数生成与结果理解。

## 在百炼平台的不同场景中如何使用

MCP 不直接暴露给模型 API 调用，而是深度集成于三大应用范式中，按使用方式分为两类：

- **智能体（Agent）**：支持**自动推理调用**。模型根据用户输入自主判断是否需调用 MCP 工具，并生成符合 `inputSchema` 的参数。单个智能体最多配置 5 个 MCP 服务（如同时启用 `WebSearch` 和 `Amap Maps`），无需指定具体工具名，由模型动态选择。适用于开放性任务（如“帮我查北京今天天气并规划一条避开拥堵的骑行路线”）。

- **工作流（Workflow）**：支持**显式编排调用**。通过拖拽 MCP 节点，绑定一个确定工具（如 `maps_weather`），并在节点配置中手动完成输入参数映射（如将上游“城市提取”节点输出 `city: string` 映射至该工具的 `location` 字段）。适合确定性、可复现的任务链路（如“先查天气 → 再查景点 → 生成行程表”）。

- **Managed Agents（托管智能体）**：作为扩展能力接入。在智能体定义中通过 `mcp_servers` 字段声明 MCP 服务，与内置工具（如 `bash`、`web_search`）同级管理，支持沙箱内异步执行、状态持久化与失败重试，适用于长时、多步、需环境隔离的生产任务。

> ⚠️ 注意：MCP 服务**不能直接用于调用千问基础模型 API**（如 `/v1/chat` 接口）。必须通过智能体、工作流或 Managed Agents 这类平台应用载体使用。

## 关键参数和配置

MCP 配置分为**服务级**（部署时设定）和**工具级**（运行时传递）两类，开发者需分别关注：

### 服务级参数（在控制台或 API 创建 MCP 服务时配置）
| 参数 | 说明 | 示例值 |
|------|------|--------|
| `type` | 协议类型，决定通信方式与端点路径 | `"streamableHttp"`（推荐，对应 `/mcp` 端点）；不建议使用已淘汰的 `"sse"`（`/sse`） |
| `url` | 服务地址（自定义服务）或留空（官方服务） | `"https://your-mcp-server.example.com/mcp"` |
| `env` | 敏感环境变量（如 API Key），平台自动加密存储 | `{"AMAP_MAPS_API_KEY": "{{KMS_CREDENTIAL_ID}}"}` |
| `deployment_mode` | 部署模式：`basic`（按调用计费，有冷启动）或 `ultra`（常驻内存，额外收取部署时长费） | `"ultra"` |

### 工具级参数（在智能体/工作流中调用时生效）
- 每个 MCP 工具严格遵循 JSON Schema 定义：
  - `inputSchema`：声明必填/选填字段、类型、描述（如 `{ "city": { "type": "string", "description": "城市名称" } }`）；
  - `outputSchema`：声明返回结构，供下游节点解析；
- 在工作流中，**必须显式映射输入**：通过变量引用（如 `{{nodes.extract_city.output.city}}`）将上游输出绑定到工具字段；
- 在智能体中，模型自动填充 `inputSchema` 字段，开发者只需确保提示词提供足够上下文（如“查询杭州天气”含明确地名）。

## 面向开发者：简洁实用指南

- ✅ **快速上手**：进入 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，开通官方服务（如 `WebSearch`）→ 在智能体「MCP 服务」模块添加 → 测试自然语言指令。
- ✅ **自定义接入**：优先使用 AI 网关封装现有 RESTful API（零代码），或通过 OpenAPI 门户发布阿里云产品能力；本地开发 MCP Server 仅推荐高级场景。
- ✅ **调试要点**：
  - 工作流中若调用失败，检查输入映射是否为空、字段名是否与 `inputSchema` 完全一致（区分大小写）；
  - 智能体未触发调用？优化系统提示词，加入类似“你可调用工具获取实时信息”的明确授权；
  - 自定义服务超时？确认函数计算 FC 出口 IP 已加入目标服务白名单，或改用 VPC 内网打通。
- ❌ **禁止操作**：不要尝试在 `application-component-api-reference` 的 `/chat` 接口中直接传入 `tools` 字段调用 MCP——该接口不支持 MCP 协议，仅支持百炼内置工具。

> 提示：所有 MCP 工具调用均受百炼统一鉴权与配额管控，无需额外实现访问控制；敏感凭证通过 KMS 加密，杜绝硬编码风险。

## 关联主题页

- [model context protocol](../guides/model-context-protocol.md)
- [overview](../guides/overview.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [application component api reference](../api/application-component-api-reference.md)


