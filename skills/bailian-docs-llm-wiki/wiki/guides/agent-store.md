# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，主要包含两类可复用、可编排的智能体增强组件：**MCP（Model Context Protocol）服务**和**Skill（技能包）**。前者面向工具调用与系统集成，实现大模型与外部 API/服务的标准化交互；后者面向文件与数据处理任务，提供开箱即用的自动化能力。二者均支持官方预置与用户自定义，可在智能体或工作流应用中一键接入。

## 支持的模型/功能

- **MCP 服务**：基于 [MCP 协议](../../raw/application-user-guide/agent-store/model-context-protocol.md)，构建大模型与外部工具间的标准化通信通道。支持三类部署形态：
  - 官方 MCP 服务（如 Amap Maps、WebSearch、Firecrawl），开箱即用；
  - 自定义 MCP 服务：支持通过[脚本部署](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（npx/uvx/http）、AI 网关导入（封装 RESTful API）、阿里云 OpenAPI 导入（对接 ECS/OSS 等云产品）；
  - 外部调用：兼容 Cherry Studio、Cursor 等第三方客户端，支持 SDK 集成。
- **Skill**：面向文件与结构化数据处理的轻量级能力包，分为：
  - 官方 Skill（如 `xlsx`、`pdf`、`csv`）：无需配置，添加即用，覆盖常见文档解析、生成、转换场景；
  - 自定义 Skill：通过 ZIP 包上传，需包含符合规范的 `SKILL.md` 元信息文件，支持业务定制化逻辑。

> **注意**：MCP 与 Skill 功能定位不同，不可互换使用。MCP 用于实时调用外部服务（如查天气、搜网页），Skill 用于处理用户上传的本地文件或生成结构化输出（如解析 Excel、生成报告）。文档 6 明确指出：“MCP 服务不能在调用千问 API 时接入”，而 Skill 仅作用于智能体应用内部对话上下文，二者均不支持直接嵌入裸 API 调用链路。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 所有官方及自定义 MCP 服务的统一鉴权凭证，无需为单个服务单独申请密钥（One Key MCP 场景）[官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。 |
| **MCP 自定义（脚本部署）** | `type`, `command`, `args`, `env`, `url` | 在 `mcpServers` 配置对象中定义，决定启动方式（`stdio`/`sse/streamableHttp`）、运行环境与连接地址。例如 `npx @modelcontextprotocol/server-memory` 启动内存服务 [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)。 |
| **Skill（自定义）** | `name`, `description`（位于 `SKILL.md`） | `name` 为全局唯一标识；`description` 必须精准描述触发条件、支持操作、输入类型及排除场景，直接影响智能体调用准确率 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。 |

## 使用方式

- **MCP 服务接入流程**：
  1. **开通/部署**：官方服务在 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 一键开通（One Key）或手动开通；自定义服务通过 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage) 创建并部署；
  2. **配置到应用**：
     - *智能体*：在应用配置中最多添加 5 个 MCP 服务，模型根据对话自动决策调用；
     - *工作流*：每个 MCP 节点需手动指定工具（如 `maps_weather`）及输入参数（常需前置大模型节点提取参数）；
  3. **外部调用**：通过 MCP SDK（如 `streamablehttp_client`）或 CLI（`bl mcp call`）集成至自有项目 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。

- **Skill 接入流程**：
  1. **获取 Skill**：从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择官方 Skill，或上传符合规范的 ZIP 包创建自定义 Skill；
  2. **添加到智能体**：在智能体应用配置的「技能」区域点击加号，或从 Skill 详情页直接添加；
  3. **触发执行**：用户对话中出现匹配 `description` 的语义（如“帮我整理这个 Excel 表格”），智能体自动调用对应 Skill 处理文件。

## 限制和注意事项

- **MCP 服务限制**：
  - 官方 WebSearch 服务限流 15 QPS（主账号与 RAM 子账号共享），免费额度 2000 次/月，超量后按 29 元/千次计费；
  - 自定义 MCP 服务（脚本部署）不支持访问本地资源（如本地数据库、文件系统）或需 GUI 的服务；远程服务需确保出口 IP 可被目标系统白名单放行 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)；
  - npx/uvx 部署的服务版本更新后**不会自动同步**，必须手动重新部署。

- **Skill 限制**：
  - ZIP 包大小上限 10 MB，`SKILL.md` 中 `name` 字段必须全局唯一；
  - 自定义 Skill 审查耗时约 2 分钟，审查失败需按提示修改 `description` 后重传；
  - Skill 仅在智能体应用中生效，**不支持在工作流应用中使用**。

- **通用注意事项**：
  - MCP 与 Skill 均无法访问用户本地环境（文档 6 第 5 条、文档 8 未提及本地访问能力）；
  - 智能体调用 MCP 或 Skill 时，返回内容会作为上下文注入模型，**必然增加输入 [Token](../concepts/token.md) 消耗**；复杂响应也可能间接增加输出 [Token](../concepts/token.md) [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)；
  - 自定义 MCP 服务若依赖私有 npm 仓库，当前不支持部署，需发布至公共仓库或改用 SSE 连接方式。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


