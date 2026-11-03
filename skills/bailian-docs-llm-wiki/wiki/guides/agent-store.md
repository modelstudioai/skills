# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力接入的核心模块，主要包含 **MCP（Model Context Protocol）服务** 和 **Skill（能力包）** 两类可复用组件。它为智能体和工作流应用提供标准化的工具调用能力，使大模型无需硬编码即可动态集成地理信息、网页爬取、文件处理、API 操作等专业能力。所有组件均支持平台内配置与外部 SDK 集成两种使用路径。

## 支持的模型/功能

`agent store` 不直接绑定特定大模型，而是作为能力枢纽被智能体/工作流应用调用。其核心功能分为两类：

- **MCP 服务**：基于 [MCP 协议](https://modelcontextprotocol.io/) 的标准化工具接口，支持与外部系统双向通信。官方已预置 Amap Maps、WebSearch、Firecrawl、Sequential Thinking 等服务；同时支持自定义部署（如通过函数计算托管 `@modelcontextprotocol/server-memory`）[原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)。  
- **Skill**：面向文件与数据处理的声明式能力包，分为官方 Skill（如 `xlsx`、`pdf`）和自定义 ZIP 技能包。Skill 通过 `SKILL.md` 中的 `description` 字段驱动智能体自动识别触发条件，无需编写工具调用逻辑 [原文标题](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。

> **注意**：文档 7 明确指出“MCP 服务不能在调用千问 API 时直接接入”，即 MCP 仅限集成于百炼平台内的智能体或工作流应用，不支持裸调用 DashScope API 时透传使用；而 Skill 同样仅作用于智能体应用，不适用于纯 API 调用场景。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 全局** | `DASHSCOPE_API_KEY` | 所有 MCP 服务（含 One Key 类型）统一使用该密钥鉴权，无需为单个服务单独申请 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。 |
| **MCP 自定义部署** | `type`, `command`, `args`, `env`, `url` | 在 `mcpServers` 配置对象中定义，决定启动方式（`npx`/`uvx`/`http`）及环境变量注入。例如 `{"type": "stdio", "command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"]}`。 |
| **Skill** | `name`, `description`（在 `SKILL.md` 中） | `name` 为唯一标识；`description` 必须清晰描述适用输入、支持操作、触发关键词及排除场景，直接影响智能体调用准确率。 |

## 使用方式

- **MCP 服务**  
  - *平台内集成*：在智能体应用中最多添加 5 个 MCP 服务；在工作流中需通过 MCP 节点手动指定工具（如 `maps_weather`），并用大模型节点预处理/后处理参数。  
  - *外部调用*：支持一键配置至 Cherry Studio/Cursor，或通过 MCP SDK（如 `streamablehttp_client`）在自有项目中调用，详见 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md) 文档。  

- **Skill**  
  - *添加方式*：从 Skill 管理页点击“添加到智能体”，或在智能体应用配置页的“技能”区域直接选择。  
  - *触发机制*：智能体根据用户输入与 `description` 的语义匹配度自动决策是否调用，无需显式指令（如“请用 xlsx Skill 处理”）。  

## 限制和注意事项

- **网络与安全**  
  - 自定义 MCP 服务运行于函数计算 FC，**无固定出口 IP**，访问云数据库等远程资源需配置 IP 白名单或 VPC 打通 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。  
  - 敏感参数（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 凭据加密，不可明文填写。  

- **部署与兼容性**  
  - `npx`/`uvx` 部署方式**仅支持发布至公共 npm/PyPI 的包**，私有仓库暂不支持；本地依赖硬件或文件系统的 MCP 服务无法云端部署。  
  - Skill ZIP 包大小上限为 **10 MB**，且必须包含符合规范的 `SKILL.md`。  

- **计费与限流**  
  - 官方 WebSearch MCP 服务有 **2000 次/月免费额度**，超量后 29 元/千次；Amap Maps 等部分服务限时免费。  
  - 云部署 MCP 服务限流为 **15 QPS（主账号与 RAM 子账号共享）**；自定义部署按调用时长（基础模式）或部署+调用时长（极速模式）计费。  

- **调试提示**  
  - 若 MCP 调用失败，优先检查错误码（如 `11200044` 表示连接拒绝）、确认协议类型（`sse` vs `streamableHttp`）与 URL 路径是否匹配。  
  - Skill 调用不准时，应优化 `description` 中的触发关键词覆盖度，避免歧义。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


