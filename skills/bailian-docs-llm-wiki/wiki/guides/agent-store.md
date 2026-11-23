# agent store

`agent store` 是阿里云百炼平台提供的能力中心，用于统一管理、发现和集成外部工具与服务，核心包括 **MCP（Model Context Protocol）服务** 和 **Skill（技能包）** 两类可插拔能力。开发者可通过控制台一键接入官方能力，或自定义部署符合协议的工具，无需修改模型逻辑即可扩展智能体与工作流的应用边界。所有能力均按需调用、独立计费，并支持内部集成与外部 SDK 调用。

## 支持的模型/功能

`agent store` 不直接提供模型，而是为大模型（如通义千问系列）提供标准化的能力接入层：

- **MCP 服务**：基于 [MCP 协议](https://modelcontextprotocol.io/) 的工具接口，支持地理信息（Amap Maps）、网页爬取（Firecrawl）、联网搜索（WebSearch）、天气查询、图表生成（QuickChart）、逻辑推理（Sequential Thinking）等。官方 MCP 服务已预部署，也支持通过脚本、AI 网关或 OpenAPI 导入自定义服务 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)。
- **Skill**：面向文件与数据处理的声明式能力包，分为官方 Skill（如 `xlsx`、`pdf`、`csv` 处理）和自定义 ZIP 技能包。Skill 由 `SKILL.md` 描述触发条件与行为，智能体根据描述自动识别并调用，无需显式指令 [原文标题](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。

> **注意**：MCP 服务与 Skill 定位不同：MCP 侧重实时外部 API 调用（如查天气、搜网页），Skill 侧重本地文件解析与生成（如读 Excel、转 PDF）。二者不可互换，且 **MCP 服务不能在纯千问 API 调用中使用**，仅限智能体/工作流应用内集成 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 所有 MCP 服务鉴权必需，无需为单个服务单独申请密钥；外部调用时需在请求头中设置 `Authorization: Bearer <key>`。 |
| **MCP 部署** | `部署模式`（基础/极速） | 基础模式：按调用时长计费（0.000156 元/秒），冷启动延迟高；极速模式：额外收取部署费（0.000036 元/秒），保持常驻以降低延迟。 |
| **MCP 配置** | `mcpServers` JSON 配置 | 自定义部署必需，定义 `stdio`（npx/uvx）或 `streamableHttp`/`sse` 连接方式及环境变量。错误配置将导致 `11200054 - MCP_PROTOCOL_ERROR` 等错误 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。 |
| **Skill** | `name` & `description`（SKILL.md） | `name` 为唯一标识；`description` 直接影响智能体调用准确率，必须明确输入类型、支持操作、触发关键词及不适用场景。 |

## 使用方式

### MCP 服务
- **平台内集成**：在智能体应用中最多添加 5 个 MCP 服务；在工作流中每个 MCP 节点需手动指定工具（如 `maps_weather`）并配置参数映射（如引用前序节点输出）。
- **外部调用**：
  - CLI：`bl mcp list` 查看服务，`bl mcp call --target amap-maps.maps_weather` 直接调用；
  - SDK：使用 `mcp` Python SDK + `OpenAI` 兼容客户端，通过 `streamablehttp_client` 连接 `/mcp` 端点；
  - 第三方客户端：支持 Qoder、Codex、Claude Code、Cursor 一键安装；其他客户端（如 Cherry Studio）需手动添加 Streamable HTTP 地址并配置鉴权头。

### Skill
- **添加方式**：在智能体应用配置页的「技能」区域点击 `+`，或从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 详情页选择「添加到智能体」。
- **触发机制**：智能体依据 `SKILL.md` 中的 `description` 自动匹配用户输入（如提及“Excel”“表格”“导出”等关键词），无需在 Prompt 中显式调用。

## 限制和注意事项

- **调用限制**：联网搜索 MCP 服务限流 15 QPS（主账号与 RAM 子账号共享），免费额度 2000 次/月，超量后按 29 元/千次计费；其他 MCP 服务依第三方 API 限制而定。
- **网络与安全**：
  - 自定义 MCP 服务托管于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通；
  - 敏感参数（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 凭据加密，不可明文配置；
  - **不支持访问用户本地资源**（如本地文件、硬件设备），本地端 MCP Server 需改用 SSE 远程连接。
- **部署与维护**：
  - npx/uvx 部署的自定义 MCP 服务版本更新后**不会自动同步**，需手动重新部署；
  - 私有 npm/PyPI 仓库的 MCP 包暂不支持直接部署，须发布至公共仓库；
  - Skill ZIP 包大小上限 10 MB，且必须包含根目录 `SKILL.md`（YAML frontmatter 格式）。
- **兼容性**：MCP 服务已全面升级为 **Streamable HTTP 协议**（`/mcp` 端点），旧版 SSE（`/sse`）需手动取消再开通以完成升级。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


