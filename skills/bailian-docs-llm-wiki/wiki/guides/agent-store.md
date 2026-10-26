# agent store

agent store 是阿里云百炼平台提供的能力中心，用于统一管理、发现和集成外部工具与服务，使智能体和工作流应用能够动态调用专业能力。核心包括两类能力：**MCP（Model Context Protocol）服务**——面向通用工具调用（如地图、搜索、天气），基于标准协议实现模型与外部系统间结构化交互；以及**Skill**——面向文件与数据处理任务（如 Excel 解析、PDF 提取），通过声明式描述自动触发。二者均支持官方预置与用户自定义，无需修改模型代码即可扩展智能体功能边界。

## 支持的模型/功能

- **MCP 服务**：支持接入符合 [MCP 协议](https://modelcontextprotocol.io/) 的工具服务，包括：
  - 官方 MCP 服务（如 Amap Maps、WebSearch、Firecrawl、Sequential Thinking），可直接开通使用；
  - 自定义 MCP 服务，支持三种部署方式：[使用脚本部署](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（npx/uvx 托管）、[从 AI 网关导入](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（封装 RESTful API）、[从阿里云 OpenAPI 导入](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（操作云资源）。
- **Skill**：提供两类能力包：
  - 官方 Skill：预置通用文件处理能力（如 `xlsx`、`pdf`、`csv`），开箱即用；
  - 自定义 Skill：通过上传 ZIP 包（含 `SKILL.md` 元信息）创建，适用于行业定制场景。

> **注意**：MCP 服务**不能**在直接调用千问 API（如 `dashscope.ChatCompletion.create`）时接入，仅限集成于百炼平台内的智能体或工作流应用中使用 —— 此限制明确记载于 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 部署** | `type`（`stdio` / `sse` / `streamableHttp`） | 必须与接入路径严格匹配：`sse` 对应 `/sse`，`streamableHttp` 对应 `/mcp`；配置错误将导致 `11200058` 错误码 —— 参见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。 |
| | `deploymentMode`（基础模式 / 极速模式） | 基础模式按调用时长计费（0.000156 元/秒），无部署费；极速模式额外收取部署费（0.000036 元/秒），适合高并发低延迟场景。 |
| **Skill 定义** | `name`（YAML 字段） | Skill 唯一标识，必须小写英文+连字符，且在同一账号下全局唯一。 |
| | `description`（YAML 字段） | **决定调用准确率的核心参数**：需明确输入类型、支持操作、触发关键词及不适用场景（如 xlsx Skill 示例所示）。 |

## 使用方式

- **MCP 服务**：
  - 在智能体中：最多添加 5 个 MCP 服务，模型根据对话自动判断调用时机与参数；
  - 在工作流中：每个 MCP 节点需手动指定工具（如 `maps_weather`）及输入参数（如引用上游节点输出）；
  - 外部调用：支持一键配置至 Cherry Studio/Cursor，或通过 [MCP SDK](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md) 编程集成（示例代码见该文档）。
- **Skill**：
  - 添加至智能体：通过 Skill 管理页“添加到智能体”，或在应用配置中点击 Skill 右侧加号；
  - 触发逻辑：智能体依据 `SKILL.md` 中的 `description` 自动匹配任务，无需显式指令（如用户说“帮我整理这个 Excel 表”即可能触发 `xlsx` Skill）。

## 限制和注意事项

- **网络与权限限制**：
  - MCP 服务托管于函数计算 FC，**无固定出口公网 IP**，访问云数据库等远程资源需配置 FC IP 白名单或 VPC 打通 —— [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md) 明确指出此限制；
  - **不支持访问本地资源**（如本地文件、硬件、数据库），本地端 MCP Server 无法部署至百炼云端。
- **部署与维护**：
  - 自定义 MCP Server 版本更新后**不会自动同步**，需手动重新部署（npx/uvx 方式）；
  - 私有 npm 仓库的 MCP 包暂不支持直接部署，需发布至公共仓库或改用 SSE 连接。
- **计费与配额**：
  - 联网搜索 MCP 服务免费额度为 2000 次/月，超量后 29 元/千次；
  - One Key MCP 服务（如 Amap Maps）限时免费，但商业化定制需自行提供 `AMAP_MAPS_API_KEY`；
  - Skill ZIP 包大小上限为 10 MB，且 `SKILL.md` 必须位于根目录。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)


