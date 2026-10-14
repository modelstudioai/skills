# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力接入的核心模块，主要包含 **MCP（Model Context Protocol）服务** 和 **Skill（能力包）** 两类可复用组件。开发者可通过该模块快速为智能体或工作流应用赋予地理查询、网页爬取、文件处理、数据分析等专业能力，无需从零开发接口或编写胶水代码。所有组件均支持可视化配置与标准化调用，兼顾开箱即用性与深度定制能力。

## 支持的模型/功能

`agent store` 不直接提供模型，而是为大模型（如通义千问系列）提供结构化工具调用能力：

- **MCP 服务**：基于 [MCP 协议](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)，实现大模型与外部工具的标准化通信。支持三类部署方式：
  - 官方 MCP 服务（如 Amap Maps、WebSearch、Firecrawl），开箱即用；
  - 自定义 MCP 服务（通过脚本部署、AI 网关导入、OpenAPI 导入），适配私有 API 或阿里云资源；
  - 外部 MCP 客户端集成（如 Cherry Studio、Cursor），支持跨平台调用。
- **Skill**：面向文件与数据处理的轻量级能力包，分为：
  - **官方 Skill**：预置 `xlsx`、`pdf`、`csv` 等通用文件处理能力，添加后自动生效；
  - **自定义 Skill**：通过 ZIP 包上传，需包含符合规范的 `SKILL.md` 文件定义触发逻辑与行为边界。

> **注意**：文档 4 明确指出“MCP 服务不能在调用千问 API 时接入”，即 MCP 仅限集成于百炼平台内的智能体或工作流应用，不支持直连 DashScope SDK 的纯 API 调用场景；而 Skill 仅适用于智能体应用，不支持工作流节点调用。

## 关键参数

| 类别 | 参数 | 说明 | 来源参考 |
|--------|------|------|----------|
| **MCP 部署** | `type`（`stdio`/`sse`/`streamableHttp`） | 必须与接入路径严格匹配（如 `/sse` 对应 `sse`，`/mcp` 对应 `streamableHttp`），否则报错 `11200058` | [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md) |
| **MCP 调用** | `DASHSCOPE_API_KEY` | 所有官方及自定义 MCP 服务统一使用该密钥鉴权，无需为单个服务单独申请 | [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md) |
| **Skill 触发** | `description` 字段（`SKILL.md` 中） | 决定智能体是否调用该 Skill 的核心依据，需明确输入类型、操作范围、触发关键词及排除场景 | [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) |

## 使用方式

### MCP 服务
- **平台内集成**：
  - 智能体：最多添加 5 个 MCP 服务，在对话中由模型自主判断调用（依赖提示词质量与模型能力）；
  - 工作流：每个 MCP 节点需手动指定工具（如 `maps_weather`）及输入参数（常需前置大模型节点提取结构化参数）。
- **外部调用**：
  - 支持一键配置至 Cherry Studio/Cursor；
  - 支持通过 MCP SDK（如 `streamablehttp_client`）编码集成，示例见 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)；
  - CLI 快速验证：`bl mcp list`、`bl mcp call --target <名称>.<工具>`。

### Skill
- **添加方式**：在智能体应用配置页的「技能」区域点击加号，或从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 详情页直接添加；
- **触发机制**：智能体根据 `SKILL.md` 中的 `description` 自动匹配用户输入意图，无需显式指令；
- **更新机制**：重新上传同名 ZIP 包即创建新版本，已添加该 Skill 的智能体会自动升级。

## 限制和注意事项

- **网络与安全限制**：
  - MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通；
  - **不支持访问本地资源**（如本地文件、硬件、数据库），本地 MCP Server 需改用 SSE 连接方式；
  - 敏感参数（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 凭据加密，不可明文配置。

- **协议与兼容性**：
  - 官方 MCP 服务已全面升级为 **Streamable HTTP 协议**，旧版 SSE 用户需手动取消再开通以完成升级；
  - 自定义 MCP 服务若通过 `npx`/`uvx` 部署，**版本更新后需手动重新部署**，不会自动同步。

- **计费与配额**：
  - 官方 WebSearch MCP 服务：免费额度 2000 次/月，超量后 29 元/千次；
  - 自定义 MCP 服务：基础模式按调用时长计费（0.000156 元/秒），极速模式另收部署费（0.000036 元/秒）；
  - Skill 无独立计费，但调用过程产生的模型 [Token](../concepts/token.md) 消耗仍计入应用账单。

- **调试关键点**：
  - MCP 调用失败优先检查错误码（如 `11200044` 连接拒绝、`11200049` 认证失败），详见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)；
  - Skill 未触发请优化 `SKILL.md` 中的 `description`，确保覆盖用户常见表达，避免歧义。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


