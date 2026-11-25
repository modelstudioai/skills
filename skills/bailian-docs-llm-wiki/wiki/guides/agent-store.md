# agent store

agent store 是阿里云百炼平台提供的核心能力中心，用于统一管理、发现和集成外部工具与服务能力。它主要通过 **Model Context Protocol (MCP)** 协议实现大模型与工具间的标准化通信，并辅以 **Skill** 机制提供面向文件与数据处理的轻量级能力封装。开发者可基于 agent store 快速为智能体或工作流注入联网搜索、地图服务、天气查询、知识图谱记忆等专业能力，无需自行开发接口适配层。

## 支持的模型/功能

agent store 的核心能力由两类机制承载：

- **MCP（Model Context Protocol）服务**：遵循开源 MCP 协议，支持任意符合规范的外部工具接入。官方 MCP 服务分为两类：  
  - **One Key MCP**：无需手动开通，使用 `DASHSCOPE_API_KEY` 直接鉴权，按量后付费（如[联网搜索 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)）；  
  - **需开通的广场 MCP**：需在 MCP 广场手动开通（如 Amap Maps），部分服务支持填写第三方 API Key 进行定制化配置。  
  此外，支持三种自定义 MCP 部署方式：[使用脚本部署](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（npx/uvx）、从 AI 网关导入（封装 RESTful API）、从阿里云 OpenAPI 导入（操作云资源）。

- **Skill**：面向文件与结构化数据处理的声明式能力包，分为官方 Skill（预置、开箱即用）和自定义 Skill（上传 ZIP 包，含 `SKILL.md` 元信息）。Skill 不依赖 MCP 协议，而是由平台自动解析用户意图并触发，适用于 Excel 处理、PDF 解析等场景。

> **注意**：文档 7 明确指出“MCP 服务能否在调用千问 API 时接入？不可以”，而文档 8 未提及 Skill 与直接 API 调用的兼容性。二者均**仅限集成于百炼平台内的智能体或工作流应用**，不可用于裸调用 `dashscope` SDK 的独立程序。

## 关键参数

| 参数 | 说明 | 来源/示例 |
|------|------|-----------|
| `DASHSCOPE_API_KEY` | 统一鉴权凭证，用于 One Key MCP、外部客户端（Qoder/Cursor）及 CLI 调用。必须设置为环境变量或显式传入。 | [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md) 中多次强调其作为唯一认证方式 |
| `mcp_url` | MCP Server 地址，格式为 `https://dashscope.aliyuncs.com/api/v1/mcps/{ServiceCode}/mcp`（Streamable HTTP）或 `/sse`（SSE）。协议类型需与客户端配置严格匹配。 | [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md) 的 Python SDK 示例中明确使用该 URL 格式 |
| `type`（MCP 配置） | 在自定义部署中指定通信协议，值为 `"stdio"`（本地进程）、`"sse"`（SSE 流）或 `"streamableHttp"`（HTTP POST）。**必须与端点路径一致**（如 `type: "sse"` 对应 `/sse`）。 | [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md) 的错误码 11200058/11200059 明确要求 type 与路径匹配 |
| `name`（Skill） | 自定义 Skill 的唯一标识符，需小写英文+连字符，在 ZIP 包 `SKILL.md` 中定义，且不可与账号内已有 Skill 重名。 | [Skill 介绍](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) 的编写规范强制要求 |

## 使用方式

### MCP 服务
- **平台内集成**：在智能体中最多添加 5 个 MCP 服务；在工作流中，每个 MCP 节点需**手动指定一个工具**（如 `maps_weather`），并通过前置大模型节点提取参数（如城市名），后置大模型节点总结结果。
- **CLI 管理**：使用 `bl mcp list` 查看已激活服务，`bl mcp tools --server <ServerCode>` 列出工具，`bl mcp call --target <ServerCode>.<ToolName>` 直接调用。
- **外部调用**：  
  - 集成至 Qoder/Codex/Claude Code/Cursor：复制安装命令，替换 `${DASHSCOPE_API_KEY}` 后执行；  
  - 集成至自有项目：使用 MCP SDK（如 `streamablehttp_client`）连接 `mcp_url`，配合 OpenAI SDK 实现多轮[工具调用](../concepts/tool-calling.md)循环。

### Skill
- **添加到智能体**：两种方式——从 Skill 管理页点击“添加到智能体”，或在智能体配置页的“技能”区域点击加号选择。
- **触发机制**：智能体根据 `SKILL.md` 中的 `description` 字段自动匹配用户输入（如关键词、文件类型、操作意图），无需显式指令。
- **更新**：重新上传同名 ZIP 包即创建新版本，已添加该 Skill 的智能体会自动使用最新版。

## 限制和注意事项

- **地域与网络**：自定义 MCP 服务托管于函数计算 FC，无固定出口 IP，若需访问云数据库等远程资源，**必须配置 FC 的 IP 白名单或 VPC 打通**（见[MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）；不支持访问用户本地资源（如本地数据库、文件）。
- **协议升级**：MCP 服务已从旧版 SSE 升级为 Streamable HTTP，已开通服务需通过“取消开通 → 重新开通”完成升级（见[外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)）。
- **[Token](../concepts/token.md) 消耗**：调用 MCP 会增加模型输入 [Token](../concepts/token.md)（返回内容作为上下文）和潜在输出 [Token](../concepts/token.md)（更详细响应），影响计费与延迟。
- **部署约束**：  
  - npx/uvx 部署仅支持发布至公共 npm/PyPI 的包，私有仓库暂不支持；  
  - 版本更新需手动重新部署，不会自动同步；  
  - 本地依赖硬件/文件的 MCP Server 无法云端部署（见[MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）。
- **Skill 作用域**：自定义 Skill 仅在当前阿里云账号及业务空间内可见，不支持跨账号共享（见[Skill 介绍](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)）。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


