# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，主要包含 **MCP（Model Context Protocol）服务** 和 **Skill（能力包）** 两类可复用组件。开发者可通过它快速为智能体或工作流接入地理信息、联网搜索、文件处理、API 调用等专业能力，无需重复开发接口适配逻辑。所有组件均支持平台内集成与外部调用两种使用模式。

## 支持的模型/功能

`agent store` 当前提供两类标准化能力：

- **MCP 服务**：基于开源 [MCP 协议](https://modelcontextprotocol.io/) 实现的大模型与外部工具通信标准，支持官方托管、自定义部署及第三方集成。典型服务包括 `Amap Maps`（地理与天气）、`WebSearch`（联网搜索）、`Firecrawl`（网页爬取）、`Sequential Thinking`（逻辑推理）等 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。
- **Skill**：面向文件与数据处理的声明式能力包，分为**官方 Skill**（如 `xlsx`、`pdf`、`csv` 处理）和**自定义 Skill**（通过 ZIP 包上传，含 `SKILL.md` 元描述）。Skill 由智能体根据用户输入自动触发，不依赖显式工具调用指令。

> **注意**：MCP 与 Skill 定位不同：MCP 侧重实时外部 API 调用（需网络、鉴权、参数映射），Skill 侧重本地化、无状态的数据格式处理（如解析、生成、转换）。二者不可互换，且目前不支持在纯 API 调用（如直调 `qwen-max` 接口）中使用 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

## 关键参数

| 类别 | 参数 | 说明 | 来源 |
|--------|------|------|------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 全局鉴权凭证，用于平台内集成及外部调用（HTTP Header `Authorization: Bearer <key>`） | [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md) |
| **MCP 云部署** | `deploymentMode` | `basic`（按次计费，冷启动延迟）或 `turbo`（常驻部署，额外收取部署费） | [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md) |
| **MCP 自定义** | `mcpServers.type` | 必填，值为 `"stdio"`（npx/uvx）、`"sse"` 或 `"streamableHttp"`，需与接入路径（`/sse` 或 `/mcp`）严格匹配 | [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md) |
| **Skill** | `name`（in `SKILL.md`） | Skill 唯一标识符，小写+连字符，同账号下不可重名 | [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) |
| **Skill** | `description`（in `SKILL.md`） | 决定智能体是否触发的关键字段，需明确输入类型、支持操作、触发关键词及排除场景 | [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) |

## 使用方式

### MCP 服务
- **平台内集成**：
  - *智能体*：最多添加 5 个 MCP 服务，模型自动判断调用时机与参数（如发送“从杭州到西湖的公交方案”触发 `Amap Maps`）。
  - *工作流*：每个 MCP 节点仅绑定一个工具（如 `maps_weather`），需手动配置输入参数（常通过前置大模型节点提取）与输出传递。
- **外部调用**：
  - CLI：`bl mcp list` 查看服务，`bl mcp call --target amap-maps.maps_weather --city "杭州"` 直接调用。
  - SDK：使用 `mcp` Python SDK 连接 `streamableHttp` 端点（URL 形如 `https://dashscope.aliyuncs.com/api/v1/mcps/<service>/mcp`），配合 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)实现多轮 tool calling [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。
  - 第三方客户端：支持 Qoder、Codex、Claude Code、Cursor 一键安装；其他客户端（如 Cline）需手动添加 Streamable HTTP 地址并配置 `Authorization` 请求头。

### Skill
- **添加到智能体**：在应用配置的「技能」区域点击「+」，或从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择 Skill 卡片 → 「添加到智能体」。
- **触发机制**：智能体依据 `SKILL.md` 中的 `description` 字段进行语义匹配，无需用户指定 Skill 名称（如描述含“处理 .xlsx 文件”，用户说“整理这个表格”即可能触发）。
- **更新**：重新上传同名 ZIP 包即创建新版本，已添加该 Skill 的智能体会自动升级。

## 限制和注意事项

- **MCP 服务限制**：
  - 云部署 MCP 服务默认共享主账号限流（如 WebSearch 为 15 QPS），RAM 子账号不单独计额 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。
  - 自定义 MCP 服务无法访问本地资源（如本地数据库、文件系统）或固定出口 IP；若需访问云数据库，须配置函数计算 FC 的 VPC 打通或 IP 白名单 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。
  - `npx`/`uvx` 部署的服务版本更新后**不会自动同步**，必须手动重新部署 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

- **Skill 限制**：
  - ZIP 包大小上限为 10 MB，且必须包含根目录 `SKILL.md`（YAML frontmatter 格式）。
  - `description` 描述质量直接影响触发准确率；模糊描述（如“处理数据”）易导致误触发或漏触发，应遵循[官方示例](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)中的四要素规范（输入类型、操作、触发词、排除场景）。

- **通用注意事项**：
  - MCP 调用会显著增加模型 Token 消耗：返回结果作为上下文注入输入，可能间接扩大输出长度 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。
  - 敏感参数（如第三方 API Key）必须通过 KMS 凭据加密，不可明文写入配置 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


