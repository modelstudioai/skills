# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力的核心模块，包含 **MCP（Model Context Protocol）服务** 和 **Skill（能力包）** 两类可插拔能力。开发者可通过控制台、CLI 或 API 快速接入、配置和调用这些能力，赋能智能体与工作流应用自动执行文件处理、联网搜索、地图查询、天气预报等任务，无需编写底层集成代码。

## 支持的模型/功能

`agent store` 不直接提供模型，而是为大模型（如 Qwen-Max、Qwen-3 系列）提供标准化能力扩展接口：

- **MCP 服务**：基于 [MCP 协议](raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)，支持两类接入方式：
  - **广场 MCP**：分为 *One Key MCP*（免开通、API Key 直接鉴权、按量后付费，如[联网搜索](raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)）和 *需手动开通的广场 MCP*（如 Amap Maps，需在 MCP 广场点击“立即开通”）。
  - **自定义 MCP**：支持三种部署路径——使用 `npx`/`uvx` 托管开源或自研 MCP 服务（如 Knowledge Graph Memory）、通过 AI 网关封装 RESTful API、或通过 OpenAPI 开发者门户接入阿里云云产品（如 OSS、ECS）。
- **Skill**：面向文件与数据处理的声明式能力包，分为：
  - **官方 Skill**：预置 ZIP 包（如 `xlsx`、`pdf`），开箱即用，无需配置；
  - **自定义 Skill**：用户上传 ZIP 包，必须含符合规范的 `SKILL.md`（YAML frontmatter 定义 name/description），用于触发条件精准匹配。

> **注意**：MCP 服务**不能**在直接调用千问 API（如 `/v1/chat/completions`）时接入；仅限集成于百炼平台内的**智能体应用**或**工作流应用**中使用（见[常见问题](raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）。

## 关键参数

| 类别 | 参数名 | 说明 | 示例值 |
|--------|--------|------|--------|
| **MCP 鉴权** | `DASHSCOPE_API_KEY` | 全局 API Key，用于 One Key MCP 及所有外部调用鉴权 | `sk-xxx` |
| **MCP 部署** | `type` | 指定传输协议类型，必须与端点路径严格匹配 | `"sse"`（对应 `/sse`）、`"streamableHttp"`（对应 `/mcp`） |
| **MCP 配置** | `mcpServers.{name}.command` / `args` | `npx`/`uvx` 部署必需字段，指定启动命令与参数 | `"npx"`, `["-y", "@modelcontextprotocol/server-memory"]` |
| **Skill 触发** | `SKILL.md → description` | 决定智能体是否调用该 Skill 的核心字段，需明确输入类型、操作、触发词及排除场景 | 见[Skill 文档示例](raw/application-user-guide/agent-store/skill/introduction-to-skill.md) |

## 使用方式

### MCP 服务
- **平台内集成**：
  - **智能体**：最多添加 5 个 MCP 服务，在对话中由模型自动判断调用（如“从杭州到西湖的公交方案”触发 Amap Maps）；
  - **工作流**：每个 MCP 节点**仅能绑定一个工具**（如 `maps_weather`），需前置大模型节点解析参数（如提取城市名），后置大模型节点总结结果。
- **外部调用**：
  - CLI：`bl mcp list` 查看已激活服务，`bl mcp call --target amap-maps.maps_weather --city "杭州"` 直接调用；
  - SDK：使用 `mcp` Python SDK 连接 Streamable HTTP 端点（URL 形如 `https://dashscope.aliyuncs.com/api/v1/mcps/{server}/mcp`），并设置 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 头；
  - 第三方客户端：支持 Qoder、Codex、Claude Code、Cursor 一键安装（详情见[外部调用](raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)）。

### Skill
- **添加**：在智能体应用配置页的“技能”区域点击“+”，或从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 详情页选择“添加到智能体”；
- **触发**：智能体根据 `SKILL.md` 中的 `description` 自动匹配用户输入（如描述含“xlsx”“创建表格”“分列统计”，则对“帮我生成本月销售分地区表格”触发 xlsx Skill）；
- **更新**：重新上传同名 ZIP 包即覆盖旧版本，已添加该 Skill 的智能体自动生效。

## 限制和注意事项

- **MCP 服务限制**：
  - One Key MCP 有 QPS 限制（如联网搜索为 15 QPS），主账号与 RAM 子账号共享配额；
  - 自定义 MCP 若托管于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 FC IP 白名单或 VPC 打通（见[常见问题](raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）；
  - 私有 npm/PyPI 仓库不支持直接部署，需发布至公共仓库或改用 SSE 远程连接。
- **Skill 限制**：
  - ZIP 包大小 ≤ 10 MB，`name` 字段全局唯一（同一账号下不可重名）；
  - 自定义 Skill **仅当前账号可见**，不支持跨账号共享（需导出 ZIP 后由其他账号重新上传）。
- **通用注意事项**：
  - MCP 调用会增加模型输入 [Token](../concepts/token.md)（返回结果作为上下文）和潜在输出 [Token](../concepts/token.md)（更详尽响应）；
  - 敏感参数（如第三方 API Key）必须通过 KMS 加密存储，不可明文配置；
  > **注意**：文档 2 与文档 6 均提及 MCP 协议已升级为 Streamable HTTP，但文档 1 的截图和部分流程仍显示旧版 SSE 路径（如 `/sse`）。实际部署时请以控制台最新 UI 和 [外部调用](raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md) 文档为准，确保 `type` 与端点路径严格匹配，否则将报错 `MCP_SERVER_HTTP_METHOD_NOT_ALLOWED`（错误码 11200058）。

## 来源文档

- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


