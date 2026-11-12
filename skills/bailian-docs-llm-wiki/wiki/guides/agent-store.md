# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，主要包含 **MCP（Model Context Protocol）服务** 和 **Skill（技能包）** 两类可复用能力组件。开发者可通过该模块快速接入第三方工具、自建服务或预置功能，无需编写底层接口代码，即可增强智能体与工作流应用的上下文感知与任务执行能力。

## 支持的模型/功能

`agent store` 不直接提供模型，而是为大模型（如通义千问系列）提供标准化的能力扩展通道：

- **MCP 服务**：基于 [MCP 协议](../../raw/application-user-guide/agent-store/model-context-protocol.md)，实现大模型与外部工具（如高德地图、Firecrawl、联网搜索）的双向通信。支持官方托管服务、自定义部署（npx/uvx/http）、AI 网关封装、OpenAPI 自动化接入四种方式。
- **Skill**：面向文件与数据处理的轻量级能力包，分为官方 Skill（如 `xlsx`、`pdf`）和自定义 ZIP 技能包。Skill 通过自然语言描述触发，由智能体自动识别并调用，适用于无需网络交互的本地化任务（如表格生成、PDF 解析）。

> **注意**：文档 7 明确指出“MCP 服务不能在调用千问 API 时接入”，而文档 3 和文档 5 均强调 MCP 仅支持集成于**智能体应用**或**工作流应用**中——这与部分早期文档中模糊表述的“API 级接入”存在矛盾，应以文档 7 的权威说明为准。

## 关键参数

| 类别 | 参数 | 说明 | 来源参考 |
|--------|------|------|----------|
| **MCP 部署** | `type`（`stdio`/`sse`/`streamableHttp`） | 决定协议类型与端点路径匹配逻辑，错误配置将导致 `11200058` 错误 | [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md) |
| **MCP 调用** | `DASHSCOPE_API_KEY` | 全局鉴权凭证，用于所有 MCP 服务（含 One Key 服务），无需单独申请子密钥 | [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md) |
| **Skill 定义** | `SKILL.md` 中的 `description` 字段 | 直接影响智能体调用准确率，需明确输入类型、操作、触发词及排除场景 | [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) |

## 使用方式

### MCP 服务
- **开通**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，One Key 服务首次调用即生效；非 One Key 服务需手动点击“立即开通”。
- **集成到智能体**：在应用配置中最多添加 5 个 MCP 服务，智能体根据对话自动决策调用（如“从杭州到西湖的公交方案”触发 Amap Maps）。
- **集成到工作流**：每个 MCP 节点须手动指定工具（如 `maps_weather`），并通过前置大模型节点解析参数（如提取城市名）。
- **外部调用**：支持 CLI（`bl mcp call --target amap-maps.maps_weather`）、SDK（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md) + MCP SDK）及客户端（Qoder/Cursor 等一键安装）。

### Skill
- **添加**：在智能体配置页的“技能”区域点击加号，或从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 详情页直接添加。
- **自定义开发**：ZIP 包需含 `SKILL.md`（YAML frontmatter 格式），描述需覆盖适用输入、支持操作、触发关键词及不适用场景；上传后经约 2 分钟自动审查。

## 限制和注意事项

- **MCP 服务限制**：
  - 云部署 MCP 服务限流为 **15 QPS**（主账号与 RAM 子账号共享）；
  - 自定义部署（npx/uvx）不支持私有 npm/PyPI 仓库，仅接受公共源；
  - 不支持访问本地资源（如本地数据库、文件系统），远程资源需配置 FC 出口 IP 白名单或 VPC 打通；
  - `基础模式` 存在冷启动延迟，高频调用建议切换至 `极速模式`。

- **Skill 限制**：
  - ZIP 包大小上限 **10 MB**；
  - `name` 字段全局唯一，重名上传将创建新版本而非覆盖；
  - 官方 Skill 自动更新，自定义 Skill 需手动重新上传 ZIP 包以更新版本。

- **通用注意事项**：
  - 模型调用 MCP/Skill 会显著增加 [Token](../concepts/token.md) 消耗：MCP 返回内容计入输入上下文，可能间接扩大输出长度；
  - 所有自定义 MCP 服务仅限当前阿里云主账号及授权 RAM 用户访问，不对外暴露；
  - 若 MCP 服务部署失败，需按 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md) 中的错误码逐项排查（如 `11200044` 表示连接被拒绝）。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)


