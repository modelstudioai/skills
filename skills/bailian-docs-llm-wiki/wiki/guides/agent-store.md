# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，主要包含两类可复用能力：**MCP（Model Context Protocol）服务**和**Skill（技能包）**。前者面向工具调用（如地图、天气、搜索），通过标准化协议连接大模型与外部 API；后者面向文件与数据处理任务（如 Excel 解析、PDF 提取），以声明式描述驱动智能体自动识别并执行。二者均支持官方预置与用户自定义，共同构成智能体应用的“能力货架”。

## 支持的模型/功能

- **MCP 服务**：支持接入符合 [MCP 协议](https://modelcontextprotocol.io/) 的工具服务，包括：
  - 官方 MCP：如 Amap Maps（地理信息）、WebSearch（联网搜索）、Sequential Thinking（逻辑推理）、QuickChart（图表生成）等，开箱即用 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。
  - 自定义 MCP：支持三种部署方式——使用脚本（npx/uvx）托管开源或自研服务、从 AI 网关导入现有 RESTful API、从阿里云 OpenAPI 导入云产品操作能力 [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)。
- **Skill**：提供面向文件与结构化数据处理的能力包：
  - 官方 Skill：预置 `xlsx`、`pdf`、`csv` 等通用格式处理能力，无需配置，添加即用。
  - 自定义 Skill：通过上传 ZIP 包（含 `SKILL.md` 元信息）创建，支持业务定制化数据清洗、行业报表生成等场景 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。

> **注意**：MCP 服务与 Skill 功能定位不同，不可混用。MCP 用于实时调用外部 API 获取动态数据（如天气、路径），而 Skill 用于离线处理用户上传的本地文件（如解析 Excel、提取 PDF 表格）。文档 7 和 8 中将 Skill 归类为 `agent-store` 下独立能力体系，与 MCP 并列，而非子集。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 所有官方及自定义 MCP 外部调用的统一鉴权凭证，无需为单个服务单独申请密钥 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。 |
| **MCP 部署** | `deploymentMode`（基础/极速） | 基础模式按调用时长计费（0.000156 元/秒），适合低频调用；极速模式额外收取部署费用（0.000036 元/秒），适合高并发、低延迟场景 [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。 |
| **Skill** | `name`（`SKILL.md` 中） | Skill 唯一标识符，必须小写英文+连字符；`description` 字段质量直接影响智能体调用准确率，需明确触发条件、支持操作及不适用场景 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。 |

## 使用方式

- **MCP 服务**：
  - *平台内集成*：在智能体应用中最多添加 5 个 MCP 服务，由模型根据对话自动决策调用；在工作流应用中需手动指定 MCP 节点的输入参数（如 `city`）并连接上下游节点 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。
  - *外部调用*：支持一键配置至 Cherry Studio/Cursor，或通过 MCP SDK（如 `streamablehttp_client`）在自有项目中编码集成 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。
- **Skill**：
  - 在智能体应用配置页的 **技能** 区域点击加号，从官方或自定义列表中选择添加；
  - 添加后，智能体根据用户输入（如“帮我分析这个 Excel”）自动匹配 `description` 描述，触发对应 Skill 处理文件。

## 限制和注意事项

- **网络与安全**：
  - 自定义 MCP 服务托管于函数计算 FC，无固定出口 IP，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。
  - 敏感参数（如第三方 API Key）必须通过 KMS 凭据加密，不可明文配置。
- **兼容性与可用性**：
  - MCP 服务依赖上游服务商稳定性，阿里云百炼仅提供接入渠道，不保证第三方服务持续可用 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。
  - 自定义 MCP 若依赖本地资源（文件、硬件）则无法云端部署；私有 npm/PyPI 仓库暂不支持直接部署。
- **调用行为**：
  - MCP 调用会增加模型输入 Token（返回结果作为上下文）和潜在输出 Token（更详细响应）[MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。
  - Skill 仅在智能体应用中生效，**不支持在纯 API 调用（如直接调用千问 API）中使用**。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


