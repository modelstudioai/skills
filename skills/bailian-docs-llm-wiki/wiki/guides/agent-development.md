# agent development

Managed Agents 是阿里云百炼提供的智能体托管运行时，适用于多步工具调用、代码执行、文件处理等长时运行任务。平台托管会话状态、沙箱环境和工具执行，智能体在独立沙箱中自主执行命令、读写文件、安装依赖并处理数据，事件历史在服务端持久化。与无状态的智能体应用不同，Managed Agents 专为有状态、可中断续接、需沙箱隔离的复杂任务设计。

## 支持的模型/功能

- **模型支持**：当前支持 `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash` 等 Qwen 系列模型；`performance` 模型明确不支持多模态输入 [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)。
- **核心能力**：
  - 多步工具调用（内置 `bash`/`read`/`write`/`edit`/`glob`/`grep`/`web_search`/`web_fetch`/`mark_artifacts`）
  - MCP 服务接入（官方市场或自定义服务）[Agent MCP](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-mcp.md)
  - 技能（Skill）封装端到端流程 [Agent Skills](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-skill.md)
  - 多智能体协作（coordinator 编队）[多智能体协作](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
  - 跨会话记忆库（Memory Store）持久化工作笔记 [记忆库](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md)

> **注意**：文档 26 和文档 28 均强调一个关键配置陷阱：`default_config.enabled: true` **不会**将工具实际注入模型；必须在 `tools.configs[]` 中为每个需启用的工具显式设置 `enabled: true`，否则模型仅能调用平台自动注入的 `mark_artifacts`，导致 `TOOL_NOT_FOUND` 错误。

## 关键参数

| 参数 | 说明 | 示例值 | 可变更性 |
|------|------|--------|----------|
| `model.id` | 指定推理模型 | `"qwen3.8-max"` | ✅（变更产生新版本） |
| `system` | 系统提示词，定义角色与行为 | `"你是数据分析专家..."` | ✅（变更产生新版本） |
| `tools` | 内置工具集配置，需在 `configs[]` 中逐项启用 | `{"name": "bash", "enabled": true}` | ✅ |
| `multiagent` | 多智能体编队配置 | `{"type": "coordinator", "agents": [...]}` | ✅ |
| `environment_id` | 绑定的云端沙箱环境 ID | `"env_xxx"` | ❌（会话创建时锁定） |
| `resources` | 挂载资源（文件、记忆库） | `[{"type": "file", "file_id": "file_xxx"}]` | ✅（运行时可追加文件） |

## 使用方式

1. **创建 Agent**：通过控制台快速开始页或 API 创建，指定模型、系统提示词和工具。CLI 也支持基础设施即代码管理：`bl managed-agent init` 生成模板，`bl managed-agent apply` 一键部署 [使用 CLI](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)。
2. **配置 Environment**：创建云端沙箱，声明预装包（`apt`/`pip`/`npm`）和网络策略（如 `unrestricted`）。预装包安装需预热，创建后不可立即用于会话 [配置 Agent 环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment.md)。
3. **发起 Session**：绑定 Agent 和 Environment，可挂载文件或记忆库。会话创建时快照 Agent 当前配置，后续修改不影响已存在会话 [委派任务给 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session.md)。
4. **交互与事件流**：通过 SSE 订阅 `message`/`tool_call`/`tool_approval_request` 等事件；客户端发送 `message` 或 `tool_approval_response` 驱动流程 [会话事件流（SSE）](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)。
5. **生产化部署**：使用 Deployment（定时任务）实现无人值守触发；通过 Webhook 接收资源状态变更通知，替代轮询 [定时任务](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-deployment.md)。

## 限制和注意事项

- **配额限制**：单个文件 ≤ 50 MB；工作空间总文件容量 ≤ 100 GB；文件保存时效 30 天；单个记忆文件 ≤ 102400 UTF-8 bytes；单会话最多挂载 8 个记忆库 [文件上传与挂载](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)。
- **环境预热**：配置了预装包的 Environment 创建后需等待安装完成，期间无法创建会话 [云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **审批机制**：`always_ask` 工具审批仅对主智能体生效，子智能体不支持；审批策略变更**不追溯影响**已存在的会话，需新建会话才生效 [Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **计费说明**：会话运行时费（0.5 元/小时）、模型调用费（按 token 计）、工具/MCP 调用费（如 `web_search` 0.03 元/次）三者独立计费；免费额度仅抵扣运行时费 [计费说明](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-billing.md)。
- **安全边界**：密钥库（Vault）凭证以占位符形式注入，仅在请求命中 `allowed_hosts` 白名单时由网关替换为真实密钥；未命中域名只透出占位符，保障密钥不泄露 [密钥库认证](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-credential.md)。

## 来源文档

- [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md)
- [开始使用](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using.md)
- [概述](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [Agent MCP](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [多智能体协作](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [配置 Agent 环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [密钥库认证](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-credential.md)
- [会话事件流（SSE）](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [Webhook 通知](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [定时任务](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [文件上传与挂载](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)
- [Agent 上下文管理](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context.md)
- [记忆库](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [计费说明](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-billing.md)
- [最佳实践](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices.md)
- [入门：搭一个数据分析 Agent](../../raw/_short/managed-agents-data-analysis-2249e7a887786f0b.md)
- [进阶：生产化定时晨报机器人](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices/managed-agents-production.md)
- [进阶：多智能体定制复杂提案](../../raw/_short/managed-agents-multiagent-proposal-c42cf9fd6aca491d.md)
- [进阶：联网研究与模型成本分层](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices/managed-agents-cost-tiering.md)
- [进阶：Webhook 事件通知](../../raw/_short/managed-agents-webhook-notifications-508b7232092b6608.md)
- [进阶：自定义 MCP 与 Skills](../../raw/_short/managed-agents-custom-mcp-skills-bb2b03130058d257.md)
- [进阶：密钥库安全注入与出网网关](../../raw/_short/managed-agents-credential-security-b5df5e4f8be278e5.md)
- [进阶：跨会话工作记忆交接](../../raw/_short/managed-agents-memory-handoff-090f3657c5cd11c0.md)
- [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)
- [更新日志](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-changelog.md)
- [进阶：构建对话客户端](../../raw/_short/managed-agents-client-streaming-8369920f0c45ea8c.md)
- [开始使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using.md)
- [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)
- [概述](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/agent-development/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-aio.md)
- [计费说明](../../raw/application-user-guide/agent-development/sandbox/sandbox-billing.md)
- [更新日志](../../raw/application-user-guide/agent-development/sandbox/sandbox-changelog.md)
- [进阶：提示词版本管理与回滚](../../raw/_short/managed-agents-prompt-versioning-b2a756840e400199.md)


