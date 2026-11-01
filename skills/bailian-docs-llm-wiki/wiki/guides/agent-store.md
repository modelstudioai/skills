# agent store

`agent store` 是阿里云百炼平台提供的能力中心，用于统一管理、发现和集成外部工具与能力模块，主要包括 **MCP（Model Context Protocol）服务** 和 **Skill** 两类核心资源。开发者可通过 agent store 快速接入官方或自定义的工具能力，无需编写底层适配代码，即可增强智能体或工作流应用的功能边界。所有能力均支持在平台内直接配置，部分还支持外部调用集成。

## 支持的模型/功能

agent store 当前提供两类可复用能力：

- **MCP 服务**：基于 [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)，实现大模型与外部工具（如高德地图、Firecrawl、联网搜索等）的标准通信。支持官方托管服务（如 Amap Maps、WebSearch）、One Key 免开通服务，以及三种自定义部署方式（脚本部署、AI 网关导入、OpenAPI 导入）。
- **Skill**：面向文件与数据处理的轻量级能力包，分为官方 Skill（如 `xlsx`、`pdf`）和自定义 Skill（ZIP 包格式）。Skill 通过自然语言描述自动触发，无需显式工具调用指令，适用于结构化数据操作、文档生成等场景。

> **注意**：MCP 服务与 Skill 的触发机制本质不同：MCP 依赖模型主动识别并调用工具（需明确意图），而 Skill 由平台根据 `SKILL.md` 中的 description 自动匹配触发。二者不可混用，也不共享配置入口。

## 关键参数

| 类别 | 参数 | 说明 | 来源依据 |
|--------|------|------|-----------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 所有 MCP 服务（含官方与自定义）均使用该密钥鉴权，**无需为单个 MCP 单独申请密钥** | [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md) |
| **自定义 MCP（脚本部署）** | `type`, `command`, `args`, `env` | 在 `mcpServers` 配置中定义，决定启动方式（如 `npx`/`uvx`）与环境变量注入 | [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md) |
| **Skill（自定义）** | `name`, `description`（YAML frontmatter） | `name` 为全局唯一标识；`description` 直接影响模型触发准确率，须包含输入类型、操作范围、触发关键词及排除场景 | [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) |

## 使用方式

### MCP 服务
- **平台内集成**：
  - 智能体：最多添加 5 个 MCP 服务，在对话中由模型自主判断调用（如“从杭州机场到西湖”自动触发 Amap Maps）；
  - 工作流：每个 MCP 节点仅绑定一个工具（如 `maps_weather`），需手动配置输入/输出参数映射（常配合大模型节点做参数提取）。
- **外部调用**：
  - 支持一键配置至 Cherry Studio/Cursor；
  - 支持 CLI 调用：`bl mcp list` / `bl mcp call --target <service>.<tool>`；
  - 支持 SDK 编程集成（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md) + MCP SDK），详见 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。

### Skill
- **添加方式**：
  - 官方 Skill：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击「添加到智能体」；
  - 自定义 Skill：上传符合规范的 ZIP 包（含 `SKILL.md`），审查通过后即可添加；
- **触发逻辑**：模型根据用户输入与 `description` 的语义匹配度自动调用，无需提示词中写明工具名。

## 限制和注意事项

- **MCP 计费差异**：
  - 官方云部署 MCP（如 WebSearch）按调用量计费（29 元/千次），有免费额度（2000 次/月）；
  - 自定义 MCP（脚本部署）按**调用时长**计费（0.000156 元/秒），基础模式无部署费，极速模式另收部署费（0.000036 元/秒）——此计费逻辑与官方服务不一致，需按场景选型。
  
- **网络与权限限制**：
  - 自定义 MCP 服务运行于函数计算 FC，**无法访问本地资源（如本地数据库、文件）**；
  - 若需访问云数据库等远程资源，必须配置 FC IP 白名单或 VPC 打通（见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）。

- **兼容性风险**：
  > **注意**：文档 5 提到 MCP 协议已从旧版 SSE 升级为新版 Streamable HTTP，但文档 2 中部分截图仍显示 SSE 类型（如 Cursor 配置页）。实际部署时请以控制台最新配置项为准，并在 `mcpServers` 配置中严格匹配 `type` 与端点路径（`"streamableHttp"` → `/mcp`，`"sse"` → `/sse`），否则将触发错误码 `11200058`。

- **其他关键限制**：
  - MCP 服务**不能在直接调用千问 API 时接入**，仅限智能体/工作流应用内使用；
  - 自定义 MCP 的 npm 包**必须发布至公共仓库**，私有 npm 仓库暂不支持；
  - Skill ZIP 包大小上限为 10 MB，且 `name` 字段在账号内必须唯一。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)


