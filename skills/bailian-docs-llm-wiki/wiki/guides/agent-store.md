# agent store

`agent store` 是阿里云百炼平台提供的能力中心，用于统一管理、发现和集成外部工具与服务，核心包括 **MCP（Model Context Protocol）服务** 和 **Skill（技能包）** 两类可复用能力。开发者可通过控制台一键接入官方能力，或自主部署/上传自定义实现，无需修改模型底层逻辑即可扩展智能体与工作流的应用边界。所有能力均按需调用、独立计费，并支持内部集成与外部 SDK 调用。

## 支持的模型/功能

`agent store` 不直接提供模型，而是为大模型（如通义千问系列）提供标准化的工具接入层：

- **MCP 服务**：基于 [MCP 协议](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)，构建大模型与外部系统（地图、搜索、天气、知识图谱等）之间的语义化调用通道。支持官方托管服务（如 Amap Maps、WebSearch）、自定义脚本部署（npx/uvx）、AI 网关封装、OpenAPI 自动转换四类接入方式。
- **Skill**：面向文件与数据处理的声明式能力包，分为官方 Skill（如 `xlsx`、`pdf`）和自定义 ZIP 技能包。通过 `SKILL.md` 中的 YAML 描述触发条件与能力边界，由智能体自动识别并调用，**不依赖 MCP 协议**，也不涉及外部 API 调用。

> **注意**：文档 5 明确指出“MCP 服务不能在调用千问 API 时接入”，而文档 8 的 Skill 仅适用于智能体应用配置；二者均**不可用于直接调用 `dashscope` SDK 的裸模型接口**，必须通过智能体或工作流应用容器使用。

## 关键参数

| 类别 | 参数 | 说明 | 来源参考 |
|--------|------|------|----------|
| **MCP 全局** | `DASHSCOPE_API_KEY` | 所有官方及自定义 MCP 服务的统一鉴权凭证，无需为单个服务单独申请密钥 | [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md) |
| **MCP 部署** | `type`（`stdio` / `sse` / `streamableHttp`） | 决定传输协议与端点路径匹配规则（如 `sse` → `/sse`，`streamableHttp` → `/mcp`），配置错误将导致 11200058 错误 | [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md) |
| **Skill 触发** | `description`（SKILL.md 中） | 智能体调用 Skill 的唯一依据，需明确输入类型、支持操作、触发关键词及排除场景 | [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) |
| **计费模式** | `基础模式` / `极速模式` | 仅影响自定义 MCP 服务：基础模式按调用时长计费（0.000156 元/秒），极速模式额外收取部署时长费（0.000036 元/秒） | [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md) |

## 使用方式

### MCP 服务
- **平台内集成**：在智能体应用中最多添加 5 个 MCP 服务；在工作流中每个 MCP 节点需手动指定工具（如 `maps_weather`）并配置参数映射（如引用上游节点输出）。
- **外部调用**：支持一键配置至 Cherry Studio/Cursor，或通过 `mcp` SDK + `OpenAI` 兼容客户端调用（需设置 `DASHSCOPE_API_KEY` 和 `mcp_url`）；CLI 命令 `bl mcp call --target <名称>.<工具>` 可快速测试。详情见 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。

### Skill
- **添加方式**：在智能体应用配置页的「技能」区域点击加号，或从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 详情页直接添加。
- **生效机制**：添加后，智能体根据 `SKILL.md` 中的 `description` 自动判断是否调用，无需编写提示词指令或配置工具节点。

## 限制和注意事项

- **网络与安全**：自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等资源需配置 IP 白名单或 VPC 打通；**不支持访问本地资源（文件、硬件、本地数据库）**（[MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）。
- **版本与更新**：通过 `npx`/`uvx` 部署的自定义 MCP 服务**不会自动同步上游包更新**，需手动重新部署；而官方 Skill 更新后，已添加的智能体会自动使用最新版本。
- **协议兼容性**：阿里云百炼 MCP 已全面升级为 **Streamable HTTP 协议**（非旧版 SSE），已开通用户需执行“取消开通→立即开通”完成升级，否则外部调用可能失败（[外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)）。
- **Token 影响**：MCP 调用返回的内容会作为上下文注入模型输入，**显著增加输入 Token 数量**；同时因信息更丰富，可能间接增加输出 Token（[MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


