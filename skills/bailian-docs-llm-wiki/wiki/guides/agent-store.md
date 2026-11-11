# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，主要包含两类可复用能力：**MCP（Model Context Protocol）服务**和**Skill（技能包）**。前者面向工具调用与系统集成，支持大模型通过标准化协议连接外部 API 或自建服务；后者面向文件与数据处理任务，提供开箱即用的、声明式定义的能力封装。二者均支持在智能体（Agent）和工作流（Workflow）应用中一键接入，无需修改模型逻辑。

## 支持的模型/功能

- **MCP 服务**：基于 [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md) 标准，支持两类部署形态：
  - **官方 MCP 服务**：如 Amap Maps（地理信息）、WebSearch（联网搜索）、Firecrawl（网页爬取）等，已由百炼云端托管，开通即用；
  - **自定义 MCP 服务**：支持三种接入方式——使用脚本部署（npx/uvx 托管至函数计算 FC）、从 AI 网关导入（封装现有 RESTful API）、从阿里云 OpenAPI 导入（操作 OSS/ECS 等云资源）。
- **Skill**：面向文件与结构化数据处理的轻量级能力包，分为：
  - **官方 Skill**：如 `xlsx`、`pdf`、`csv` 等预置技能，覆盖常见格式解析、生成与转换；
  - **自定义 Skill**：用户上传 ZIP 包（含 `SKILL.md` 元信息文件），支持业务定制，如行业发票解析、私有数据清洗等。

> **注意**：文档 6 明确指出“MCP 服务不能在调用千问 API 时直接接入”，而文档 3 和文档 5 均强调 MCP 仅限集成于**智能体或工作流应用内部**。这与部分早期文档中模糊表述的“API 级接入”存在矛盾，实际开发中应以该限制为准。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP（云部署）** | `deployment_mode` | `基础模式`（按调用时长计费，0.000156 元/秒，有冷启动延迟）或 `极速模式`（额外收取部署费 0.000036 元/秒，常驻在线）；详见 [计费说明](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。 |
| | `type`（配置中） | 必须与接入路径严格匹配：`"sse"` 对应 `/sse` 端点，`"streamableHttp"` 对应 `/mcp` 端点；不匹配将导致 `11200058` 错误码。 |
| **MCP（自定义）** | `MCP 服务配置`（JSON） | 必须符合 [自定义MCP服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md) 文档中定义的 schema，例如 `npx` 启动需指定 `"command": "npx"` 及有效包名。 |
| **Skill** | `name`（`SKILL.md`） | Skill 唯一标识符，小写+连字符，不可与同账号下已有 Skill 重名。 |
| | `description`（`SKILL.md`） | **决定调用准确性的核心字段**，需明确触发条件、支持操作、输入类型及排除场景；描述质量直接影响智能体是否正确识别并调用该 Skill。 |

## 使用方式

- **MCP 服务接入流程**：
  1. **开通/部署**：官方服务前往 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通（One Key 类自动生效）；自定义服务前往 [MCP 管理](https://bailian.console.aliyun.com/?tab=app#/mcp-manage) 创建；
  2. **配置到应用**：
     - *智能体*：在应用配置 → “MCP 服务” 中最多添加 5 个，大模型根据对话自动路由调用；
     - *工作流*：拖入 MCP 节点，手动指定工具（如 `maps_weather`）及输入参数（常需前置大模型节点提取参数）；
  3. **外部调用**：通过 CLI（`bl mcp call --target <name>.<tool>`）或 SDK（如 `mcp.client.streamable_http`）集成至第三方客户端（Qoder/Cursor）或自有项目。

- **Skill 接入流程**：
  1. **添加 Skill**：在 Skill 管理页点击“添加到智能体”，或在智能体配置页的“技能”区域选择并添加；
  2. **触发机制**：智能体根据用户输入自然语言与 Skill 的 `description` 匹配度自动判断是否调用，**无需显式指令或工具名提及**；
  3. **测试验证**：在应用配置页右侧对话窗格发送典型任务语句（如“帮我创建一个包含本月销售数据的表格”），观察是否自动调用对应 Skill 并返回结果。

## 限制和注意事项

- **MCP 限制**：
  - 官方 WebSearch 服务有 **2000 次/月免费额度**，超限后按 29 元/千次计费，且 **限流 15 QPS（主账号与 RAM 子账号共享）**；
  - 自定义 MCP 服务**无法访问本地资源**（如本地数据库、文件系统），且函数计算 FC 出口 IP 不固定，访问云数据库需配置白名单或 VPC 打通；
  - 部署失败常见原因包括：`npx/uvx` 包未发布至公共仓库、`url` 配置错误、SSL 证书不信任、下游服务未就绪（见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md) 错误码表）。

- **Skill 限制**：
  - ZIP 包大小上限为 **10 MB**，且必须包含根目录下的 `SKILL.md` 文件；
  - `description` 字段若未清晰界定适用/不适用场景，极易导致误触发（如将 Word 处理请求错误路由至 `xlsx` Skill）；
  - 自定义 Skill 更新需重新上传同名 ZIP 包，**不会自动覆盖旧版本**，但已添加该 Skill 的智能体会自动升级至最新审查通过版本。

- **通用注意事项**：
  - MCP 和 Skill 的调用均会**增加模型 Token 消耗**：MCP 返回内容作为上下文计入输入 Token；Skill 处理结果可能使输出更详尽，间接增加输出 Token；
  - 所有自定义 MCP 服务及 Skill **仅限当前阿里云主账号及其授权 RAM 用户访问**，不对外公开；
  - 若模型无法调用 MCP，首要检查提示词是否足够明确（[外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md) 文档建议：“调用阿里云百炼 Amap Maps MCP 服务，规划从杭州到上海的自驾路线”）。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


