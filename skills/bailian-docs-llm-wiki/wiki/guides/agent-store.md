# agent store

agent store 是阿里云百炼平台提供的能力中心，用于统一管理、发现和集成外部工具与服务，主要通过 **MCP（Model Context Protocol）服务** 和 **Skill** 两类能力扩展智能体与工作流的应用边界。开发者可快速接入官方预置能力，也可部署自定义服务，实现无需编码的工具调用与专业任务处理。

## 支持的模型/功能

agent store 当前核心支持两类能力：

- **MCP 服务**：基于开源 Model Context Protocol 标准，提供大模型与外部工具间的标准化通信通道。支持官方 MCP 服务（如 Amap Maps、WebSearch、Firecrawl）、One Key 免开通服务，以及三种自定义部署方式（脚本部署、AI 网关导入、阿里云 OpenAPI 导入）[模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。  
- **Skill**：面向文件与数据处理的声明式能力包，分为官方 Skill（如 `xlsx`、`pdf`）和自定义 Skill（ZIP 包格式）。Skill 通过自然语言描述触发，智能体自动识别并调用，无需显式工具调用指令 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。

> **注意**：文档 6 仅列出 `Skill` 目录索引，未提供实质内容；所有 Skill 相关技术细节均以文档 7 为准，该文档为唯一权威来源。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **MCP 部署** | `部署方式`（基础模式 / 极速模式） | 基础模式按调用时长计费（0.000156 元/秒），无部署费；极速模式额外收取部署费（0.000036 元/秒），适用于高并发低延迟场景 [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。 |
| **MCP 鉴权** | `DASHSCOPE_API_KEY` | 所有云部署 MCP 服务统一使用该 API Key 鉴权，无需为单个服务单独申请密钥；敏感参数（如 `AMAP_MAPS_API_KEY`）需通过 KMS 凭据加密 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。 |
| **Skill 定义** | `SKILL.md` 中的 `description` 字段 | 决定智能体是否准确触发 Skill。必须明确输入类型、支持操作、触发关键词及不适用场景；模糊描述将导致调用失败或误触发 [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。 |

## 使用方式

- **MCP 服务**  
  - *平台内集成*：在智能体应用中最多添加 5 个 MCP 服务；在工作流中每个 MCP 节点需手动指定工具并配置输入/输出参数映射 [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)。  
  - *外部调用*：支持 CLI（`bl mcp call --target <name>.<tool>`）、SDK（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md) + `mcp` Python SDK）及第三方客户端（Qoder/Cursor/Claude Code）集成 [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)。  

- **Skill**  
  - *添加方式*：通过控制台「组件 > Skill 管理」页面，或在智能体「应用配置 > 技能」区域直接添加；官方 Skill 开箱即用，自定义 Skill 需上传符合规范的 ZIP 包（含 `SKILL.md`，≤10 MB） [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)。  
  - *触发机制*：智能体依据 `description` 语义匹配用户输入，自动调用；无需在 Prompt 中写死工具名或参数。

## 限制和注意事项

- **MCP 服务限制**  
  - 联网搜索 MCP 服务限流 15 QPS（主账号与 RAM 子账号共享），免费额度 2000 次/月，超量后 29 元/千次 [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)。  
  - 自定义 MCP 服务无法访问本地资源（如本地数据库、文件系统）；若需访问云数据库，须配置函数计算 FC 的 IP 白名单或 VPC 打通 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。  
  - npx/uvx 部署的服务版本更新后**不会自动同步**，需手动重新部署 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。  

- **Skill 注意事项**  
  - 自定义 Skill 名称（`SKILL.md` 中 `name` 字段）在账号下必须全局唯一；重复上传同名 ZIP 将创建新版本，已添加的智能体会自动升级。  
  - Skill **不支持**在纯 API 调用（如直调 `qwen-max` 接口）中生效，仅限智能体/工作流应用内使用。  

- **通用限制**  
  - MCP 调用会增加模型输入 Token（返回结果作为上下文注入）和潜在输出 Token（更详尽响应）；需在 Token 预算中预留余量 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。  
  - 所有自定义 MCP 服务仅限创建者主账号及授权 RAM 用户访问，不对外公开 [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)。

## 来源文档

- [模型上下文协议（MCP）](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-introduction.md)
- [MCP](../../raw/application-user-guide/agent-store/model-context-protocol.md)
- [官方 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)
- [外部调用](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-external-calls.md)
- [自定义 MCP 服务](../../raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)
- [Skill](../../raw/application-user-guide/agent-store/skill.md)
- [Skill](../../raw/application-user-guide/agent-store/skill/introduction-to-skill.md)
- [MCP 常见问题](../../raw/application-user-guide/agent-store/model-context-protocol/mcp-faq.md)


