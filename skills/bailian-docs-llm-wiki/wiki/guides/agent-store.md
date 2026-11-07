# agent store

`agent store` 是阿里云百炼平台中统一管理可扩展智能体能力的核心模块，主要包含两类标准化能力组件：**MCP（Model Context Protocol）服务**和 **Skill（技能包）**。前者面向工具集成，提供大模型与外部系统（如地图、搜索、数据库）的标准化交互通道；后者面向文件与数据处理任务，以声明式描述驱动智能体自动识别并调用。二者均支持官方预置与用户自定义，可在智能体或工作流应用中一键接入。

## 支持的模型/功能

- **MCP 服务**：基于 [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md) 标准，支持接入三类服务：
  - 官方 MCP 服务（如 Amap Maps、WebSearch、Firecrawl），开箱即用；
  - 自定义 MCP 服务：支持通过[脚本部署](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（npx/uvx）、AI 网关导入、阿里云 OpenAPI 导入三种方式；
  - 外部客户端兼容：支持 Cherry Studio、Cursor 等主流 MCP 客户端直接调用。
- **Skill**：面向文件与结构化数据处理，分为：
  - 官方 Skill（如 `xlsx`、`pdf`、`csv`），无需配置，添加即用；
  - 自定义 Skill：通过 ZIP 包上传，需包含符合规范的 `SKILL.md` 文件定义触发逻辑与能力边界。

> **注意**：MCP 服务与 Skill 功能正交——MCP 用于实时调用外部 API 或系统能力，Skill 用于处理用户上传的本地文件或生成结构化输出。二者不可互相替代，也不支持在纯 API 调用（如直调 `qwen-max`）中使用 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 全局** | `DASHSCOPE_API_KEY` | 所有 MCP 服务（含官方与自定义）统一鉴权凭证，无需为单个服务单独申请密钥。 |
| **MCP 部署模式** | `基础模式` / `极速模式` | 仅适用于自定义 MCP 服务：<br>- 基础模式：按调用时长计费（0.000156 元/秒），无部署费，有冷启动延迟；<br>- 极速模式：额外收取部署费（0.000036 元/秒），常驻运行，降低延迟。 |
| **Skill 元信息** | `name`（必填）、`description`（必填） | 在 `SKILL.md` 中定义，`description` 直接影响智能体调用准确率，需明确输入类型、支持操作、触发关键词及不适用场景。 |

## 使用方式

- **MCP 服务接入**：
  - *智能体应用*：在应用配置 → “MCP 服务” 中最多添加 5 个服务；大模型根据对话自动判断是否调用及传参 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。
  - *工作流应用*：每个 MCP 节点需手动指定工具（如 `maps_weather`）及输入参数（支持引用上游节点输出）。
  - *外部调用*：通过 MCP SDK（如 `streamablehttp_client`）或 CLI（`bl mcp call`）集成至第三方项目 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。
- **Skill 接入**：
  - 在智能体应用配置 → “技能” 区域点击加号，从官方或自定义列表中选择；
  - 添加后，智能体根据 `description` 自动匹配用户请求（如“帮我清洗这个 Excel 表格”），无需显式指令。

## 限制和注意事项

- **MCP 限制**：
  - 官方 MCP 服务（如 WebSearch）有调用额度与 QPS 限制（例：WebSearch 免费额度 2000 次/月，限流 15 QPS）；
  - 自定义 MCP 服务无法访问本地资源（如本地数据库、文件系统）[MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)；
  - 函数计算 FC 托管的 MCP 服务无固定出口 IP，访问云数据库等需配置 IP 白名单或 VPC 打通。
- **Skill 限制**：
  - ZIP 包大小 ≤ 10 MB，`SKILL.md` 必须位于根目录；
  - 自定义 Skill 名称全局唯一（同账号下），重名上传将创建新版本；
  - Skill 仅在智能体应用中生效，不支持工作流应用。
- **通用注意事项**：
  - MCP 调用会增加模型输入 Token（返回结果作为上下文）及潜在输出 Token（更详细响应）；
  - 自定义 MCP 服务版本更新需手动重新部署，npx/uvx 方式不自动同步；
  - 敏感参数（如 `AMAP_MAPS_API_KEY`）必须通过 KMS 凭据加密，不可明文配置。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


