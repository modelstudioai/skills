# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，主要包含两类可复用能力：**MCP（Model Context Protocol）服务**和**Skill（技能包）**。前者面向工具调用与系统集成，提供标准化的大模型-外部服务通信协议；后者面向文件与数据处理任务，以声明式描述驱动智能体自动识别与执行。二者均支持官方预置与用户自定义，可在智能体或工作流应用中按需装配。

## 支持的模型/功能

- **MCP 服务**：基于 [MCP 协议](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)，实现大模型与外部工具（如高德地图、Firecrawl、联网搜索等）的标准化交互。支持三种部署方式：  
  - 官方云部署服务（如 `Amap Maps`、`WebSearch`），开箱即用；  
  - 自定义部署（通过脚本、AI 网关、OpenAPI 导入），详见 [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)；  
  - 外部 MCP 客户端集成（如 Cherry Studio、Cursor），支持 Streamable HTTP 协议调用。  
- **Skill**：面向文件与结构化数据处理的轻量级能力单元，分为：  
  - **官方 Skill**：预置 `xlsx`、`pdf`、`csv` 等通用文件处理能力，无需配置；  
  - **自定义 Skill**：用户上传 ZIP 包（含 `SKILL.md` 描述文件），支持业务定制，如行业报表生成、专有格式解析等。

> **注意**：文档 6 明确指出“MCP 服务不能在调用千问 API 时接入”，而文档 4 和 5 均强调其仅适用于**智能体或工作流应用内部集成**。因此，MCP 不是通用 API 能力，不可直接用于 `dashscope` SDK 的单次 `chat.completions.create` 调用——该能力必须嵌入百炼应用上下文。

## 关键参数

| 类别 | 参数 | 说明 | 来源参考 |
|--------|------|------|----------|
| **MCP 部署** | `deploymentMode` | `基础模式`（按调用时长计费，有冷启动延迟）或 `极速模式`（按部署+调用双计费，常驻在线） | [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md) |
| **MCP 配置** | `mcpServers` | JSON 配置对象，定义服务类型（`stdio`/`sse`/`streamableHttp`）、启动命令（`npx`/`uvx`）及 URL | [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md) |
| **Skill 定义** | `name` & `description` | `SKILL.md` 中必填字段：`name` 为唯一标识；`description` 决定智能体触发准确性，需明确输入类型、操作、触发词及排除场景 | [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) |
| **外部调用** | `DASHSCOPE_API_KEY` | 所有外部 MCP 调用（CLI、SDK、第三方客户端）均使用此密钥鉴权，**无需为每个 MCP 服务单独申请密钥** | [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md) |

## 使用方式

- **MCP 服务**：  
  1. **开通**：前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market)，对 One Key 服务直接调用生效；对非 One Key 服务点击“立即开通”；  
  2. **集成**：在智能体中最多添加 5 个 MCP 服务（自动路由）；在工作流中每个 MCP 节点需手动指定工具（如 `maps_weather`）并绑定输入/输出参数；  
  3. **外部调用**：使用 CLI（`bl mcp call --target amap-maps.maps_weather`）或 MCP SDK（`streamablehttp_client`）对接第三方项目，详见 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。  

- **Skill**：  
  1. **添加**：在智能体「应用配置 → 技能」区域点击 `+`，从官方或自定义列表选择；  
  2. **触发**：智能体根据 `SKILL.md` 中的 `description` 自动匹配用户输入（如提及“xlsx”“表格”“销售数据”即可能触发 `xlsx` Skill）；  
  3. **更新**：重新上传同名 ZIP 包即发布新版本，已添加该 Skill 的智能体会自动升级。

## 限制和注意事项

- **MCP 服务限制**：  
  - 官方 `WebSearch` 服务限流 15 QPS，免费额度 2000 次/月，超限后按 29 元/千次计费；  
  - 自定义 MCP 服务**无法访问本地资源**（如本地数据库、文件系统），且函数计算 FC 实例无固定出口 IP，访问云数据库需配置白名单或 VPC 打通；  
  - `npx`/`uvx` 部署的服务版本更新后**不会自动同步**，必须手动重新部署（文档 6）。  

- **Skill 限制**：  
  - ZIP 包大小上限 10 MB，`SKILL.md` 必须位于根目录且符合 YAML frontmatter 格式；  
  - `description` 字段质量直接影响触发准确率，模糊描述易导致误调用或漏触发；  
  - 官方 Skill 由平台维护，自动更新；自定义 Skill 版本需手动上传覆盖。  

- **通用注意事项**：  
  - MCP 调用会增加模型输入 Token（返回结果作为上下文注入）和潜在输出 Token（更详尽响应）；  
  - 所有自定义 MCP 服务仅限当前主账号及授权 RAM 用户访问，不对外公开；  
  - 若 MCP 服务部署失败，优先排查错误码（如 `11200044` 表示连接拒绝），详见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


