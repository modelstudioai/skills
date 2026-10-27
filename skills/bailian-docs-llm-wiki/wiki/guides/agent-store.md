# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力接入的核心模块，主要包含 **MCP（Model Context Protocol）服务** 和 **Skill（能力包）** 两类可复用组件。它为智能体和工作流应用提供标准化的工具调用能力，使大模型能安全、可控地与外部系统（如地图、搜索、数据库、文件处理等）交互，无需开发者手动编写胶水代码。所有组件均支持控制台可视化管理、权限隔离与计费追踪。

## 支持的模型/功能

`agent store` 当前提供两类能力载体：

- **MCP 服务**：基于开源 [MCP 协议](https://modelcontextprotocol.io/) 实现的大模型与外部工具通信标准，支持：
  - 官方 MCP 服务（如 Amap Maps、WebSearch、Firecrawl、Sequential Thinking 等），开箱即用；
  - 自定义 MCP 服务，支持三种部署方式：[使用脚本部署](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（npx/uvx）、[从 AI 网关导入](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（封装现有 RESTful API）、[从阿里云 OpenAPI 导入](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（操作 OSS/ECS 等云资源）；
  - 外部调用支持 Cherry Studio、Cursor 等主流 IDE，亦可通过 SDK 集成至自有项目。

- **Skill**：面向文件与数据处理的声明式能力包，分为：
  - 官方 Skill（如 `xlsx`、`pdf`、`csv`），预置、免配置、自动更新；
  - 自定义 Skill：通过 ZIP 包上传，需包含符合规范的 `SKILL.md` 文件定义触发逻辑与能力边界，适用于行业定制场景。

> **注意**：MCP 与 Skill 功能定位不同——MCP 侧重实时外部系统调用（如查天气、爬网页），Skill 侧重本地文件解析与生成（如读取 Excel、生成 PDF）。二者不可互换，且目前不支持在纯 API 调用（如直接调用 `qwen-max` 接口）中启用任一能力 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

## 关键参数

| 类别 | 参数名 | 说明 | 示例值 |
|--------|--------|------|--------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 全局鉴权凭证，用于平台内集成及外部调用 | `sk-xxx` |
| **自定义 MCP** | `type` | 协议类型，决定传输方式与端点路径 | `"stdio"` / `"sse"` / `"streamableHttp"` |
| | `command` + `args` | npx/uvx 启动命令，必须与 MCP 服务实际入口一致 | `"npx", ["-y", "@modelcontextprotocol/server-memory"]` |
| | `url` | 远程 MCP 服务地址，仅 `type: "sse"` 或 `"streamableHttp"` 时有效 | `"https://my-server/mcp"` |
| **Skill** | `name`（`SKILL.md`） | Skill 唯一标识，小写+连字符，不可重复 | `"invoice-parser"` |
| | `description`（`SKILL.md`） | **关键字段**：直接影响智能体是否触发该 Skill，需明确输入类型、操作、触发词与排除场景 | 见 [原文标题](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) 中 xlsx 示例 |

## 使用方式

### MCP 服务
- **平台内集成**：
  - 智能体：最多添加 5 个 MCP 服务，模型根据对话自动决策调用（需提示词引导）；
  - 工作流：每个 MCP 节点需手动指定工具（如 `maps_weather`）并绑定输入/输出参数。
- **外部调用**：
  - CLI：`bl mcp list` 查看服务，`bl mcp call --target amap-maps.maps_weather` 直接调用；
  - SDK：使用 `mcp` Python SDK + `OpenAI` 兼容客户端，按 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md) 文档示例编码；
  - 第三方 IDE：一键配置至 Cherry Studio/Cursor，无需改代码。

### Skill
- **添加到智能体**：在应用配置页的「技能」区域点击 `+`，或从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 详情页选择「添加到智能体」；
- **触发机制**：智能体依据 `SKILL.md` 中的 `description` 自动匹配用户输入（如含“Excel”、“表格”、“.xlsx”等关键词且任务目标为生成/编辑表格，则触发 `xlsx` Skill）；
- **测试**：在应用配置页右侧对话窗格发送典型指令（如“帮我整理这份销售数据为带图表的 Excel”），观察是否自动生成文件。

## 限制和注意事项

- **MCP 计费模式差异**：
  - 官方 MCP（如 WebSearch）按调用次数计费（2000 次/月免费，超量 29 元/千次）；
  - 自定义 MCP 分「基础模式」（按调用时长 0.000156 元/秒，冷启动延迟）与「极速模式」（额外收部署费 0.000036 元/秒，常驻低延迟）[原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)；
  > **注意**：文档 3 中提及的「极速模式」部署费率（0.000036 元/秒）与文档 2 表述一致，但文档 2 的「基础模式」描述为「无部署费用。无调用时不计费」，而文档 3 表述为「无部署费用。无调用时不计费，有调用时按调用时长计费」——二者实质一致，无矛盾。

- **网络与安全限制**：
  - 自定义 MCP 服务运行于函数计算 FC，**无法访问用户本地资源（如本地数据库、文件）**；
  - 若需访问云数据库等远程资源，必须配置 FC IP 白名单或 VPC 打通 [原文标题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)；
  - 敏感参数（如 `AMAP_MAPS_API_KEY`）需通过 KMS 凭据加密，不可明文写入配置。

- **兼容性与维护**：
  - MCP 服务协议已从旧版 SSE 升级为 Streamable HTTP，已开通用户需手动「取消开通 → 重新开通」完成升级；
  - 自定义 MCP 服务版本更新后**不会自动同步**，需手动重新部署；
  - 私有 npm/PyPI 仓库的 MCP 包暂不支持直接部署，须发布至公共仓库或改用 SSE 连接。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


