# agent store

agent store 是阿里云百炼平台提供的统一能力中心，用于托管、发现和集成外部工具与服务。它以[模型上下文协议](../concepts/mcp.md)（MCP）为核心标准，支持官方 MCP 服务、自定义 MCP 服务及 Skill 两类能力单元，使智能体和工作流能按需调用文件处理、联网搜索、地图查询等专业功能，无需开发者手动编写接口适配代码。

## 支持的模型/功能

agent store 主要承载两类可插拔能力：

- **MCP 服务**：基于 [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md) 标准实现，支持大模型与外部工具间结构化交互。包括：
  - **One Key MCP**：开箱即用，无需开通，使用 `DASHSCOPE_API_KEY` 直接调用（如联网搜索、Sequential Thinking）；
  - **需开通的广场 MCP**：需在 MCP 广场手动开通（如 Amap Maps），部分服务需提供第三方 API Key；
  - **自定义 MCP**：支持三种部署方式——[使用脚本部署](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（npx/uvx）、从 AI 网关导入、从阿里云 OpenAPI 导入。

- **Skill**：面向文件与数据处理的轻量级能力包，分为：
  - **官方 Skill**：预置 ZIP 包（如 `xlsx`、`pdf`），添加即用，无需配置；
  - **自定义 Skill**：用户上传 ZIP 包，须含符合规范的 `SKILL.md`（YAML frontmatter 定义 name/description），最大 10 MB。

> **注意**：文档 5 明确指出“MCP 服务能否在调用千问 API 时接入？不可以”，而文档 8 未提及 Skill 的 API 直接调用能力。二者均**仅支持集成于百炼平台内的智能体或工作流应用**，不支持裸调用千问 API 时动态注入。

## 关键参数

| 参数类别 | 参数名 | 说明 | 示例值 |
|---------|--------|------|--------|
| **通用鉴权** | `DASHSCOPE_API_KEY` | 所有 One Key MCP 和自定义 MCP 的统一认证凭证，用于 HTTP Header `Authorization: Bearer <key>` | `sk-xxx` |
| **MCP 部署** | `deploymentMode` | 自定义 MCP 的计费与性能模式（见[计费说明](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md#fb482455a3u8c)） | `basic`（基础模式）或 `pro`（极速模式） |
| **MCP 配置** | `mcpServers` | JSON 配置对象，定义服务类型（`stdio`/`sse`/`streamableHttp`）、命令、URL、环境变量等 | `{ "memory": { "type": "stdio", "command": "npx", "args": ["@modelcontextprotocol/server-memory"] } }` |
| **Skill 元信息** | `name`, `description` | `SKILL.md` 中必填字段；`description` 质量直接影响智能体调用准确率，需明确触发条件、操作范围及排除场景 | `name: xlsx`；`description: "Use this skill any time a spreadsheet file is the primary input or output..."` |

## 使用方式

### MCP 服务
- **平台内集成**：在智能体/工作流配置页的「MCP 服务」区域，最多添加 5 个服务；工作流中每个 MCP 节点需手动指定工具（如 `maps_weather`）并绑定输入参数（如引用上游节点输出）。
- **CLI 管理**：使用 `bl mcp list` 查看已激活服务，`bl mcp tools --server <code>` 列出工具，`bl mcp call --target <server>.<tool>` 直接调用。
- **外部调用**：通过 MCP SDK（如 `mcp.client.streamable_http`）或兼容 OpenAI 接口的客户端（Qoder/Cursor/Claude Code）集成，需配置 `Authorization` 请求头及正确 endpoint（`/mcp` for Streamable HTTP, `/sse` for SSE）。

### Skill
- **添加到智能体**：在 Skill 管理页点击「添加到智能体」，或在智能体配置页「技能」区域点击加号选择。
- **自定义 Skill 创建**：ZIP 包根目录含 `SKILL.md`（YAML 格式），上传至控制台「自定义 Skill」入口；审查通过后自动生效。
- **更新**：重新上传同名 ZIP 包即创建新版本，已添加该 Skill 的智能体自动使用最新版。

## 限制和注意事项

- **网络与资源限制**：自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通；**不支持访问本地数据库或硬件资源**（见[常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md#12beda7007ibq)）。
- **协议兼容性**：MCP 服务已从旧版 SSE 协议升级为 Streamable HTTP 协议；若服务地址以 `/sse` 结尾，客户端需选择 SSE 模式；若以 `/mcp` 结尾，则必须使用 Streamable HTTP 模式（见[外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md#17e41c39a9fnf)）。
- **版本与维护**：通过 `npx`/`uvx` 部署的自定义 MCP 服务**不会随上游包自动更新**，版本变更后需手动重新部署；官方 Skill 由平台自动更新，但自定义 Skill 需用户主动上传新版 ZIP。
- **安全策略**：云部署 MCP Server 对敏感数据默认启用 KMS 加密；自定义 MCP 的 `env` 字段禁止明文存储密钥，应使用 KMS 凭据。
- **调用影响**：MCP 调用会增加模型输入 Token（返回内容作为上下文）和潜在输出 Token（更详尽响应），需在成本评估中纳入考量。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


