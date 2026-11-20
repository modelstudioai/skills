# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，包含 **MCP（Model Context Protocol）服务** 和 **Skill（能力包）** 两类可复用组件。开发者可通过它将大模型与外部工具、API 或专业处理逻辑解耦集成，无需修改模型本身即可增强智能体或工作流的执行能力。所有组件均支持平台内配置调用及外部 SDK 集成。

## 支持的模型/功能

`agent store` 不直接绑定特定大模型，而是作为能力接入层，服务于百炼平台上的 **智能体应用** 和 **工作流应用**。其核心能力分为两类：

- **MCP 服务**：基于开源 [MCP 协议](https://modelcontextprotocol.io/) 实现标准化工具调用，支持：
  - 官方 MCP 服务（如 Amap Maps、WebSearch、Firecrawl、Sequential Thinking 等），开箱即用；
  - 自定义 MCP 服务，支持三种部署方式：[使用脚本部署](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（npx/uvx）、[从 AI 网关导入](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（封装现有 RESTful API）、[从阿里云 OpenAPI 导入](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（对接阿里云产品）；
  - 外部 MCP 客户端集成（Qoder、Codex、Claude Code、Cursor 等），详见 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。

- **Skill**：面向文件与数据处理的声明式能力包，分为：
  - **官方 Skill**：预置 ZIP 包（如 `xlsx`、`pdf`、`csv`），覆盖常见格式解析、生成、清洗等场景，添加后自动生效；
  - **自定义 Skill**：用户上传 ZIP 包，需包含符合规范的 `SKILL.md` 元信息文件，用于定义触发条件与能力边界。

> **注意**：MCP 服务与 Skill 的调用机制不同：MCP 由模型根据上下文自主决策调用（支持多工具协同），而 Skill 依赖 `description` 的语义匹配触发，且仅在智能体应用中生效，不支持工作流节点级调用。

## 关键参数

| 类别 | 参数 | 说明 | 示例/约束 |
|--------|------|------|-----------|
| **MCP 服务（自定义部署）** | `installMode` | 部署方式，决定运行环境与计费模型 | `npx`（Node.js）、`uvx`（Python）、`http`（远程 SSE/Streamable HTTP） |
| | `deploymentMode` | 运行模式 | `基础模式：按次计费`（冷启动延迟，无部署费）、`极速模式`（常驻，含部署费） |
| | `mcpServers` | 服务配置 JSON，定义 stdio 或远程端点 | 见 [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md) 中的配置模板 |
| **MCP 服务（外部调用）** | `Authorization` | 请求头，值为 `Bearer ${DASHSCOPE_API_KEY}` | 必须使用百炼通用 API Key，不可用其他密钥替代 |
| **Skill（自定义）** | `name` | Skill 唯一标识符 | 小写英文+连字符，如 `invoice-parser`，不可重名 |
| | `description` | 触发语义描述（YAML frontmatter） | 必须明确输入类型、支持操作、触发关键词、不适用场景，直接影响调用准确率 |

## 使用方式

### MCP 服务
- **平台内集成**：
  - 智能体：在应用配置中最多添加 5 个 MCP 服务，模型自动判断调用时机与参数；
  - 工作流：每个 MCP 节点需手动指定一个工具（如 `maps_weather`），并显式配置输入/输出参数映射。
- **外部集成**：
  - CLI：`bl mcp list` 查看服务，`bl mcp call --target <service>.<tool>` 直接调用；
  - SDK：使用 `mcp` Python SDK + `openai` 兼容客户端，通过 `streamablehttp_client` 连接 `/mcp` 端点；
  - 第三方客户端：复制服务地址，在 Qoder/Cursor 等中选择 `Streamable HTTP` 类型并设置 `Authorization` 头。

### Skill
- **添加到智能体**：
  - 方式一：在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面点击目标 Skill 卡片 → “添加到智能体”；
  - 方式二：进入智能体应用配置 → “技能”区域 → 点击“+”号选择 Skill。
- **验证与更新**：
  - 官方 Skill 自动更新，已添加的智能体会即时生效；
  - 自定义 Skill 更新需重新上传同名 ZIP 包，审查通过后自动覆盖。

## 限制和注意事项

- **MCP 服务限制**：
  - 不支持访问本地资源（如本地数据库、文件系统）[原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)；
  - npx/uvx 部署的服务版本更新后**不会自动同步**，必须手动重新部署；
  - 函数计算 FC 托管的 MCP 服务无固定出口 IP，若需访问云数据库等资源，必须配置 [FC IP 白名单或 VPC 打通](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)；
  - 私有 npm/PyPI 仓库暂不支持直接部署，需发布至公共仓库或改用 SSE 远程连接。

- **Skill 限制**：
  - 仅支持智能体应用，**不支持工作流应用**；
  - ZIP 包大小上限为 10 MB，且必须包含根目录下的 `SKILL.md`；
  - `description` 描述质量直接影响触发准确率；模糊或缺失“不适用场景”易导致误调用。

- **通用注意事项**：
  - MCP 服务调用会增加模型输入 Token（返回结果作为上下文）和潜在输出 Token（更详尽响应）；
  - **MCP 服务不能在直接调用千问 API 时接入**，仅限集成于智能体或工作流应用中 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)；
  - 所有自定义 MCP 服务与 Skill 均为账号私有，仅主账号及授权 RAM 用户可访问。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


