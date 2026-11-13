# agent store

`agent store` 是阿里云百炼平台中统一管理外部能力扩展的核心模块，主要包含两类可复用能力：**MCP（Model Context Protocol）服务**和**Skill（技能包）**。前者面向工具集成，通过标准化协议连接大模型与外部 API/服务；后者面向文件与数据处理任务，以声明式描述驱动智能体自动调用。二者均支持官方预置与用户自定义，可在智能体或工作流应用中一键接入。

## 支持的模型/功能

- **MCP 服务**：提供标准化工具调用通道，支持三类部署方式：
  - 官方 MCP 服务（如 Amap Maps、WebSearch、Firecrawl），开箱即用，部分支持 [One Key MCP](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md) 一键配置；
  - 自定义 MCP 服务，支持 [使用脚本部署](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)（npx/uvx）、从 AI 网关导入、从阿里云 OpenAPI 导入；
  - 外部调用：兼容 Qoder、Codex、Claude Code、Cursor 等主流 MCP 客户端，也支持通过 SDK 或 CLI 集成至自有项目。
- **Skill**：面向文件与结构化数据处理的能力包，分为：
  - 官方 Skill（如 `xlsx`、`pdf`、`csv`），无需配置，添加即用；
  - 自定义 Skill：通过上传 ZIP 包（含 `SKILL.md` 元信息）创建，支持业务定制化能力。

> **注意**：文档 6 明确指出“MCP 服务不能在调用千问 API 时直接接入”，仅限集成于智能体或工作流应用内使用；而 Skill 也仅作用于智能体应用，不适用于纯 API 调用场景。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 通用** | `DASHSCOPE_API_KEY` | 所有官方及自定义 MCP 服务的统一鉴权凭证，无需为单个服务单独申请密钥（见 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)）。 |
| **MCP 自定义部署** | `type`（`stdio`/`sse`/`streamableHttp`）、`url`、`command`/`args` | 决定服务启动方式与通信协议；必须与实际端点路径严格匹配（如 `streamableHttp` 对应 `/mcp`，`sse` 对应 `/sse`），否则触发 [11200058 错误码](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。 |
| **Skill** | `name`（唯一标识）、`description`（YAML 中必填字段） | `description` 直接影响智能体调用准确率，需明确输入类型、支持操作、触发关键词及不适用场景（见 [Skill 文档](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) 示例）。 |

## 使用方式

- **MCP 服务接入流程**：
  1. 在 [MCP 广场](https://bailian.console.aliyun.com/?tab=mcp#/mcp-market) 开通服务（One Key 类型首次调用自动生效；非 One Key 需手动开通）；
  2. 在智能体应用中最多添加 5 个 MCP 服务（[官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)）；在工作流中每个 MCP 节点需显式指定工具（如 `maps_weather`）并配置参数映射；
  3. 外部调用时，通过 `bl mcp list` / `bl mcp call --target <name>.<tool>`（CLI）或 MCP SDK（如 Python 示例）发起请求。

- **Skill 接入流程**：
  1. 在 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 页面选择官方 Skill 直接添加，或上传符合规范的 ZIP 包创建自定义 Skill；
  2. 在智能体应用配置的 **技能** 区域点击加号，从列表中选择目标 Skill；
  3. 添加后，智能体根据 `description` 自动识别任务并调用，无需修改提示词或编写代码。

## 限制和注意事项

- **MCP 服务限制**：
  - 官方 WebSearch 服务限流 15 QPS（主账号与 RAM 子账号共享），免费额度 2000 次/月，超量后按 29 元/千次计费；
  - 自定义 MCP 服务托管于函数计算 FC，**无法访问本地资源（如本地数据库、文件）**，远程资源（如云数据库）需配置 IP 白名单或 VPC 打通（见 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)）；
  - npx/uvx 部署的服务版本更新后**不会自动同步**，需手动重新部署。

- **Skill 限制**：
  - ZIP 包大小上限 10 MB，`SKILL.md` 必须位于根目录且格式严格遵循 YAML frontmatter；
  - 自定义 Skill 的 `name` 在当前账号下必须全局唯一，重名上传将创建新版本而非覆盖；
  - Skill 仅支持智能体应用，**不适用于工作流应用**。

- **通用注意事项**：
  - MCP 和 Skill 均会增加模型 Token 消耗：MCP 返回结果作为上下文计入输入 Token；Skill 处理过程可能间接增加输出 Token；
  - 提示词质量直接影响调用效果：MCP 需在 prompt 中明确工具名称与能力；Skill 的 `description` 编写质量决定触发准确率；
  - 所有自定义 MCP 服务及 Skill 仅限创建者账号及其授权 RAM 用户访问，不对外公开。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)


