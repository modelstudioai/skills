# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，主要包含 **MCP（Model Context Protocol）服务** 和 **Skill（技能包）** 两类可复用能力单元。开发者可通过该模块快速接入地理信息、网页爬取、文件处理、数据分析等专业工具，无需编写底层接口代码，即可增强智能体或工作流应用的功能边界。

## 支持的模型/功能

`agent store` 当前提供两类标准化能力扩展机制：

- **MCP 服务**：基于开源 [MCP 协议](https://modelcontextprotocol.io/) 实现的大模型与外部工具通信标准，支持动态发现、调用和组合工具。官方已预置 Amap Maps、WebSearch、Firecrawl、Sequential Thinking 等 MCP 服务；同时支持自定义部署（如 Knowledge Graph Memory）[原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)。  
- **Skill**：面向文件与数据操作的声明式能力包，分为官方 Skill（如 `xlsx`、`pdf`）和自定义 ZIP 技能包。Skill 通过自然语言描述触发，由智能体自动识别并调用，适用于无需实时 API 调用的离线处理任务 [原文标题](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。

> **注意**：MCP 服务与 Skill 定位不同：MCP 用于**实时、有状态、需鉴权的外部系统交互**（如调用高德地图 API），而 Skill 用于**无状态、本地化、以文件为输入输出的批处理任务**（如解析 Excel 表格）。二者不可互相替代，亦不支持在同一个节点中混合使用。

## 关键参数

| 类别 | 参数 | 说明 | 来源 |
|--------|------|------|------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 全局鉴权凭证，所有云部署及自定义 MCP 服务均使用此 Key，无需为单个服务单独申请 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md) | — |
| **MCP 部署模式** | `基础模式` / `极速模式` | 基础模式按调用时长计费（0.000156 元/秒），冷启动延迟高；极速模式额外收取部署费（0.000036 元/秒），保持常驻以降低延迟 | 文档 2 |
| **Skill 触发核心** | `description` 字段（SKILL.md） | 决定智能体是否调用该 Skill 的唯一依据。必须明确描述适用输入类型、支持操作、触发关键词及**不适用场景**，否则将导致误调或漏调 | 文档 8 |
| **自定义 MCP 配置** | `mcpServers` JSON 结构 | 必须严格匹配协议类型（`stdio`/`sse`/`streamableHttp`）与端点路径（如 `/sse` 或 `/mcp`），否则引发 `11200058`（METHOD_NOT_ALLOWED）等错误码 | 文档 5 |

## 使用方式

### MCP 服务
- **平台内集成**：在智能体应用中最多添加 5 个 MCP 服务；在工作流中每个 MCP 节点需手动指定工具（如 `maps_weather`）并配置参数映射 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。  
- **外部调用**：支持 CLI（`bl mcp call --target amap-maps.maps_weather`）、MCP SDK（Python 示例见文档 7）及第三方客户端（Qoder/Cursor 等一键安装）。  
- **开通方式**：One Key 服务首次调用自动生效；非 One Key 服务需在 MCP 广场手动开通，并对敏感参数（如 `AMAP_MAPS_API_KEY`）使用 KMS 加密。

### Skill
- **添加方式**：在智能体应用配置页的「技能」区域点击加号，或从 Skill 管理页直接「添加到智能体」。  
- **触发逻辑**：智能体仅依据 SKILL.md 中的 `description` 进行语义匹配，**不依赖函数名或代码逻辑**。例如 `xlsx` Skill 的 description 明确排除“产出 Word 文档”的场景，即此类请求不会触发该 Skill。  
- **更新机制**：重新上传同名 ZIP 包即生成新版本，已添加该 Skill 的智能体会自动升级（官方 Skill 由平台静默更新）。

## 限制和注意事项

- **MCP 服务限制**：  
  - 不支持访问本地资源（如本地数据库、文件系统）[文档 5]；  
  - 自定义 MCP 服务若依赖私有 npm/PyPI 仓库，当前不支持部署，需发布至公共仓库或改用 SSE 远程连接 [文档 5]；  
  - 云部署 MCP 服务共享主账号 QPS 限流（如 WebSearch 为 15 QPS），RAM 子账号不独立限流 [文档 2]。  

- **Skill 限制**：  
  - ZIP 包大小上限 10 MB，且必须包含符合规范的 `SKILL.md`；  
  - `description` 字段质量直接影响调用准确率——模糊或缺失“不适用场景”描述将显著增加误触发概率。  

- **通用注意事项**：  
  - MCP 调用会增加模型输入 [Token](../concepts/token.md)（返回结果作为上下文注入）和潜在输出 [Token](../concepts/token.md)（更详尽响应），需在 [Token](../concepts/token.md) 预算中预留余量 [文档 5]；  
  - MCP 服务**不能**在直接调用千问 API（如 `dashscope.ChatCompletion.create`）时接入，仅限百炼平台内智能体/工作流应用使用 [文档 5]；  
  - 自定义 MCP 服务版本更新后需**手动重新部署**，npx/uvx 方式不会自动拉取新版本 [文档 5]。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


