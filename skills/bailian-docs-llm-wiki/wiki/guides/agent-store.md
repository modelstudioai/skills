# agent store

agent store 是阿里云百炼平台提供的能力中心，用于统一管理与分发外部工具接入协议（MCP）和可插拔技能（Skill），使智能体和工作流应用能按需调用专业工具或处理特定任务。其核心是通过标准化协议降低集成门槛，支持开箱即用的官方服务与高度灵活的自定义扩展。

## 支持的模型/功能

agent store 当前主要承载两类能力：

- **MCP（Model Context Protocol）服务**：作为大模型与外部工具之间的标准化通信桥梁，支持地理信息（Amap Maps）、联网搜索（WebSearch）、网页爬取（Firecrawl）、逻辑推理（Sequential Thinking）、图表生成（QuickChart）等场景。MCP 服务可在智能体中自动触发，也可在工作流中手动编排为节点 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。
- **Skill（技能包）**：面向文件与数据处理的轻量级能力单元，分为官方 Skill（如 `xlsx`、`pdf`）和自定义 ZIP 技能包。Skill 由智能体根据用户输入语义自动识别并调用，无需显式工具选择或参数配置 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。

> **注意**：MCP 与 Skill 定位不同：MCP 侧重通用工具调用（需网络/API 交互），Skill 侧重本地化数据处理（如格式转换、内容提取）。二者不可混用——MCP 服务不能作为 Skill 添加，Skill 也无法替代 MCP 的远程工具能力。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 所有云部署 MCP 服务的统一鉴权凭证，无需为单个服务单独申请密钥 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。 |
| **MCP 部署** | `deploymentMode`（基础/极速） | 基础模式按调用时长计费（0.000156 元/秒），无部署费；极速模式额外收取部署费（0.000036 元/秒），适用于高并发低延迟场景。 |
| **Skill** | `name`（SKILL.md 中） | Skill 唯一标识符，必须小写+连字符，且在同一账号下全局唯一。 |
| **Skill** | `description`（SKILL.md 中） | 决定智能体是否触发该 Skill 的核心字段，需明确输入类型、支持操作、触发关键词及不适用场景。描述质量直接影响调用准确率。 |

## 使用方式

- **MCP 服务接入**：
  - *智能体应用*：最多添加 5 个 MCP 服务，在对话中由模型自主判断调用时机与参数（如“从杭州到西湖的公交方案”自动调用 Amap Maps）。
  - *工作流应用*：每个 MCP 节点需手动指定工具（如 `maps_weather`）及输入参数（通常需前置大模型节点解析自然语言为结构化参数）。
  - *外部调用*：支持 CLI（`bl mcp call --target amap-maps.maps_weather`）、SDK（[OpenAI 兼容接口](../concepts/openai-compatible-api.md) + MCP SDK）及主流客户端（Qoder/Cursor 等一键安装）。

- **Skill 接入**：
  - 官方 Skill：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击“添加到智能体”即可启用。
  - 自定义 Skill：上传符合规范的 ZIP 包（含 `SKILL.md`，≤10 MB），系统自动审查后生效；更新时重新上传同名包即覆盖旧版本。

## 限制和注意事项

- **MCP 限制**：
  - 云部署 MCP 服务不支持访问用户本地资源（如本地数据库、文件系统）[MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。
  - 自定义 MCP 服务若依赖私有 npm/PyPI 仓库，当前不支持直接部署；建议发布至公共仓库或改用 SSE 远程连接。
  - 联网搜索 MCP 服务限流为 15 QPS（主账号与 RAM 子账号共享），免费额度 2000 次/月，超限后按 29 元/千次计费。

- **Skill 注意事项**：
  - Skill 仅在智能体应用中生效，**不支持在工作流或直接调用千问 API 时使用**。
  - 自定义 Skill 的 `description` 必须精准——过于宽泛会导致误触发，过于狭窄则无法命中；建议参考官方 `xlsx` Skill 的完整示例编写。
  - Skill 处理过程不产生额外 [Token](../concepts/token.md) 计费，但输出结果（如生成的 Excel 文件）会作为响应内容计入总输出 [Token](../concepts/token.md)。

- **通用注意事项**：
  - MCP 服务与 Skill 均受账号级权限控制，RAM 用户需被授予对应资源操作权限。
  - 自定义 MCP 服务部署失败常见原因包括：函数计算 FC 权限不足、下游服务未启动、URL 配置错误（如 `sse` 类型误配 `/mcp` 路径），可依据错误码（如 `11200058`）快速定位 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


