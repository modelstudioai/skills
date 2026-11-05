# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力接入的核心模块，主要包含两类可复用能力：**MCP（Model Context Protocol）服务**和**Skill（技能包）**。前者面向工具调用（如地图、搜索、天气等第三方 API），后者面向文件与数据处理任务（如 Excel 解析、PDF 提取）。二者均通过声明式配置集成至智能体或工作流应用，无需编写胶水代码即可扩展大模型能力边界。

## 支持的模型/功能

- **MCP 服务**：支持官方部署与自定义部署两类。官方 MCP 服务包括 Amap Maps、WebSearch（联网搜索）、Firecrawl（网页爬取）、Sequential Thinking 等，覆盖地理信息、实时数据获取、逻辑推理等场景；自定义 MCP 服务支持三种接入方式：[使用脚本部署](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（npx/uvx/http）、[从 AI 网关导入](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（封装 RESTful API）、[从阿里云 OpenAPI 导入](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（操作 OSS/ECS 等云资源）。
- **Skill**：分为官方 Skill（如 `xlsx`、`pdf`、`csv` 等预置文件处理能力）和自定义 Skill（用户上传 ZIP 包，含 `SKILL.md` 元信息及执行逻辑）。Skill 专用于文件解析、生成、转换等结构化数据任务，不涉及网络调用或外部 API。

> **注意**：文档 6 明确指出“MCP 服务不能在调用千问 API 时接入”，而文档 8 未提及 Skill 的 API 直接调用能力——二者均**仅限集成于百炼平台内的智能体或工作流应用**，不可作为独立 HTTP 接口被外部直接调用（除非通过 MCP 外部调用机制，见下文）。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 所有官方 MCP 服务及外部调用的统一鉴权凭证，无需为单个服务单独申请密钥（One Key MCP 场景）[官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。 |
| **MCP 自定义（脚本部署）** | `type`, `command`, `args`, `env` | 在 `mcpServers` 配置中定义，决定启动方式（如 `"type": "stdio"`, `"command": "npx"`）及环境变量注入。必须严格匹配 MCP 协议规范，否则触发 `MCP_PROTOCOL_ERROR`（错误码 11200054）[MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。 |
| **Skill** | `name`, `description`（在 `SKILL.md` 中） | `name` 为唯一标识；`description` 是核心参数，直接影响智能体调用准确率，需明确输入类型、支持操作、触发关键词及不适用场景 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。 |

## 使用方式

- **MCP 服务**：
  - **平台内集成**：在智能体应用中最多添加 5 个 MCP 服务；在工作流中每个 MCP 节点需手动指定工具（如 `maps_weather`）并配置参数映射（如引用上游节点输出）[官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。
  - **外部调用**：支持一键配置至 Cherry Studio/Cursor，或通过 MCP SDK 编程调用（需 `streamablehttp_client` 连接 `https://dashscope.aliyuncs.com/api/v1/mcps/{service}/{tool}`）[外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。
- **Skill**：
  - 仅支持平台内集成：在智能体应用配置页的「技能」区域添加，智能体根据 `description` 自动识别任务并调用，无需显式指令或参数传递 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。

## 限制和注意事项

- **MCP 计费与限流**：联网搜索 MCP 服务有 2000 次/月免费额度，超量后 29 元/千次；所有云部署 MCP 服务共享 15 QPS 限流（主账号及其 RAM 子账号）[模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。
- **自定义 MCP 部署约束**：
  - 不支持访问本地资源（如本地数据库、文件系统）；
  - 函数计算 FC 托管环境无固定出口 IP，访问云数据库需配置 IP 白名单或 VPC 打通；
  - 私有 npm/PyPI 仓库暂不支持，须发布至公共仓库或改用 SSE 远程连接 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。
- **Skill 限制**：ZIP 包大小 ≤10 MB；`SKILL.md` 中 `name` 必须全局唯一；自定义 Skill 更新需重新上传同名包，已添加的智能体会自动生效 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。
- **通用注意事项**：
  - MCP 服务调用会增加模型输入 [Token](../concepts/token.md)（返回结果作为上下文）和潜在输出 [Token](../concepts/token.md)（更详细响应）；
  - 智能体调用失败时，优先检查提示词是否明确工具能力，其次更换更强模型（如 Qwen3）[MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


