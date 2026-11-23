# agent store

agent store 是阿里云百炼平台提供的能力中心，用于统一管理与分发智能体可调用的外部能力模块，核心包括 MCP（Model Context Protocol）服务和 Skill 两类资源。MCP 服务通过标准化协议桥接大模型与外部工具（如地图、搜索、天气），而 Skill 则封装面向文件处理、数据操作等场景的即插即用能力包。二者均支持平台内集成与外部调用，开发者可根据任务类型选择合适的能力形态。

## 支持的模型/功能

- **MCP 服务**：支持官方预置服务（如 Amap Maps、WebSearch、Firecrawl）、第三方 MCP 服务及自定义部署服务。覆盖地理信息、联网搜索、网页爬取、图表生成、天气查询等场景 [MCP 简介](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。  
- **Skill**：分为官方 Skill（如 `xlsx`、`pdf`、`csv`）和自定义 Skill（ZIP 包形式）。官方 Skill 无需配置，开箱即用；自定义 Skill 需提供符合规范的 `SKILL.md` 元信息文件，支持业务定制化能力封装 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。  
- **兼容性**：MCP 服务仅支持在**智能体应用**或**工作流应用**中集成，**不可直接接入千问 API 调用链** [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。  

> **注意**：文档 7 和文档 8 均指向 Skill 主题，但文档 8 仅为目录页，无实质内容；所有 Skill 的技术细节（如 SKILL.md 规范、上传流程、触发逻辑）均以文档 7 为准，应以 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md) 为唯一权威来源。

## 关键参数

| 类别 | 参数 | 说明 |
|--------|------|------|
| **MCP 服务** | `type`（`stdio`/`sse`/`streamableHttp`） | 必须与端点路径严格匹配：`sse` 对应 `/sse`，`streamableHttp` 对应 `/mcp`；配置错误将导致 `11200058` 错误码 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md) |
| | `command` + `args`（npx/uvx） | 仅支持公共 npm/PyPI 包；私有仓库包暂不支持 [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md) |
| **Skill** | `name`（YAML 字段） | Skill 唯一标识，必须小写英文+连字符，且在同一账号下全局唯一 |
| | `description`（YAML 字段） | 决定智能体调用准确率的核心字段，需明确触发条件、支持操作、输入类型及排除场景 |

## 使用方式

- **MCP 服务接入**：  
  - *平台内*：在智能体应用中最多添加 5 个 MCP 服务；在工作流中每个 MCP 节点仅能绑定一个工具，并需手动配置输入/输出参数映射 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。  
  - *外部调用*：支持 CLI（`bl mcp call --target <名称>.<工具>`）、MCP SDK（[OpenAI 兼容接口](../concepts/openai-compatible-api.md)）、以及 Qoder/Cursor 等客户端一键安装 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。  
- **Skill 接入**：  
  - 官方 Skill 直接从 [Skill 管理](https://bailian.console.aliyun.com/?tab=app#/skill) 添加；  
  - 自定义 Skill 需上传 ZIP 包（≤10 MB，含 `SKILL.md`），系统自动审查后生效；更新时重新上传同名包即可覆盖 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。  

## 限制和注意事项

- **网络与安全**：  
  - MCP 服务托管于函数计算 FC，**无法访问用户本地资源（如本地数据库、文件）**；访问云数据库需配置 FC IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。  
  - 敏感参数（如 API Key）必须通过 KMS 凭据加密，不可明文填写 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。  
- **部署与运维**：  
  - npx/uvx 部署的自定义 MCP 服务**版本更新后需手动重新部署**，不会自动同步 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。  
  - 基础模式存在冷启动延迟；若需低延迟，应选用极速模式（按部署时长+调用时长双计费） [MCP 简介](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。  
- **调用可靠性**：  
  - 智能体调用 MCP 失败常见原因为提示词未明确工具名称与能力，需在 System Prompt 中清晰描述工具功能与输入格式 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。  
  - Skill 的 `description` 编写质量直接影响调用准确率，模糊或遗漏排除场景易导致误触发。

## 来源文档

- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)


