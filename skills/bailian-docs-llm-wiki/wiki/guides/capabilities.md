# capabilities

阿里云百炼平台提供覆盖文本、多模态、语音、视频、决策、Agent 基础设施及平台管理的全栈 AI 能力。所有能力均通过统一 CLI 工具 `bl` 暴露，支持命令式调用、异步任务管理与基础设施即代码（IaC）式编排。开发者可按需组合模型调用、训练部署、知识增强与安全治理等模块，构建端到端 AI 应用。

## 支持的模型/功能

百炼支持以下核心能力类别，每类对应独立 CLI 子命令：

- **模型调用**：涵盖文本对话（`bl text chat`）、全模态交互（`bl omni`）、图像生成与编辑（`bl image generate/edit`）、视频生成与编辑（`bl video generate/ref`）、语音合成与识别（`bl speech synthesize/recognize`）、视觉理解（`bl vision describe`）、批量推理（`bl batch`）及决策模型（`bl decision`）[原文标题](../../raw/cli/capabilities/model-invocation.md)。  
- **Agent 基础设施**：包括 Flow Agent（工作流与智能体应用管理）、Managed Agent（IaC 式 Agent 部署）、Knowledge（RAG 知识库）、Memory（长期记忆）、联网搜索（`bl search web`）、MCP & Skill（[模型上下文协议](../concepts/mcp.md)服务编排）、Sandbox（沙箱环境）及 Security（安全防护）[原文标题](../../raw/cli/capabilities/agent-infrastructure.md)。  
- **训练与部署**：支持数据集管理（`bl dataset`）、模型微调（`bl finetune`）、模型部署（`bl deploy`）及自定义模型导入（`bl cmodel`）[原文标题](../../raw/cli/capabilities/training-deployment.md)。  
- **平台管理**：提供用量与配额查询（`bl usage`）、监控日志告警（`bl monitor/log/alert`）、配置与工具（`bl auth/config`）及 ParseX 文档解析（`bl parsex`）等运维支撑能力。

> **注意**：文档 10（`training-deployment/finetune-deploy.md`）仅作为入口页，实际功能已拆分至 `finetune.md` 和 `deploy.md`；开发者应直接参考 [原文标题](../../raw/cli/capabilities/training-deployment/finetune.md) 和 [原文标题](../../raw/cli/capabilities/training-deployment/deploy.md) 获取最新参数细节。

## 关键参数

各能力模块共享以下通用参数模式，同时具备领域特定参数：

- **鉴权与环境**：`--api-key`、`--workspace-id`（或 `BAILIAN_WORKSPACE_ID` 环境变量）、`--base-url`。Workspace ID 是多数 Agent、Memory、Knowledge、Sandbox 等能力的强制依赖项。
- **输入处理**：支持本地文件路径（自动上传至临时存储，有效期 48 小时）和 URL；`--messages-file`、`--state-file`、`--questions-file` 等参数统一接受 JSON 格式输入。
- **模型控制**：`--model <id>` 用于指定模型（如 `qwen3.8-max`、`qwen-image-3.0`），默认值因命令而异；`--model auto` 启用 MCP 自动路由，但会拒绝不兼容参数（如 `--seed`、`--prime`）并报错，不回退至 REST 调用。
- **异步与流式**：`--async` 返回任务 ID 而非等待结果；`--stream` 启用[流式输出](../concepts/streaming-output.md)（TTY 中默认开启）；`--follow` 用于轮询异步任务状态（如 `bl batch get --follow`）。
- **资源与规格**：部署类命令（`bl deploy text create`）支持 `--plan <lora|ptu|mu>`、`--input-tpm`、`--output-tpm`；微调类命令（`bl finetune text create`）支持 `--training-type <sft|dpo|cpt>`、`--n-epochs`、`--batch-size` 等超参。

## 使用方式

1. **安装与认证**：通过 `bl auth login --api-key <key>` 或 `--console` 完成鉴权，配置 `BAILIAN_WORKSPACE_ID` 环境变量以支持 Workspace 专属能力。  
2. **单次调用**：例如 `bl text chat --message "你好"` 发起同步文本请求；`bl image generate --prompt "猫在火星"` 生成图片。  
3. **批量任务**：使用 `bl batch convert` 生成 JSONL，再通过 `bl batch create` 提交异步任务；与 `bl text chat --batch` 的同步 Batch Chat 请求严格区分。  
4. **Agent 编排**：`bl flow-agent call --app-id <id> --prompt <text>` 调用已发布应用；`bl mcp call --target <server.tool>` 直接调用 MCP 工具。  
5. **IaC 管理**：`bl managed-agent init` 生成 `agents.yaml`，`bl managed-agent plan` 预览变更，`bl managed-agent apply` 执行部署。  
6. **训练部署闭环**：`bl dataset upload` → `bl finetune text create` → `bl deploy text create` 形成完整流程。

## 限制和注意事项

- **地域与账号限制**：Agent 基础设施（Flow Agent、Managed Agent、Memory、Knowledge、Sandbox、Security）仅对中国站（aliyun.com）账号开放；模型导入（`bl cmodel`）仅在北京地域可用；Sandbox 实例强制要求 `cn-beijing` 地域及 SLR 授权。  
- **配额与限流**：Memory API 有账号级限流（add 120 QPM、search 300 QPM）；收到 HTTP 429 时需退避重试（间隔 ≥1 秒）；[Token](../concepts/token.md) Plan 订阅 Key 不支持 MCP 模式联网搜索。  
- **参数兼容性**：`--model auto` 模式下，不兼容参数（如 `--seed`、`--watermark`、`--prime`）将直接报错，不会降级执行；`--batch` 与 `--stream`、`--prime` 互斥；`bl text chat --batch` 不支持 `--enable-search`，需改用 `--tool '{"type":"web_search"}'`。  
- **文件与格式**：`bl dataset upload` 对 ZIP 文件大小有限制（媒体 ZIP ≤2GB）；`bl batch convert` 仅支持 CSV→JSONL 的文本与 Embedding 字段映射，多模态输入需手写 JSONL；ParseX 解析仅接受可访问的 HTTP(S) URL，不支持本地文件直传。  
- **版本一致性**：CLI 命令行为以文档中标注的版本（如 `bl 2.8.4`）为准；跨版本升级时需查阅更新日志（如 Memory 命令在 2.5.0 有不兼容变更）。

## 来源文档

- [模型调用](../../raw/cli/capabilities/model-invocation.md)
- [文本对话与全模态](../../raw/cli/capabilities/model-invocation/text-chat.md)
- [批量推理](../../raw/cli/capabilities/model-invocation/batch.md)
- [决策模型](../../raw/cli/capabilities/model-invocation/decision.md)
- [图像生成与编辑](../../raw/cli/capabilities/model-invocation/image.md)
- [视频生成与编辑](../../raw/cli/capabilities/model-invocation/video.md)
- [语音合成与识别](../../raw/cli/capabilities/model-invocation/speech.md)
- [视觉理解](../../raw/cli/capabilities/model-invocation/vision.md)
- [数据集管理](../../raw/cli/capabilities/training-deployment/dataset.md)
- [模型微调与部署](../../raw/cli/capabilities/training-deployment/finetune-deploy.md)
- [模型训练与部署](../../raw/cli/capabilities/training-deployment.md)
- [模型导入](../../raw/cli/capabilities/training-deployment/cmodel.md)
- [模型部署](../../raw/cli/capabilities/training-deployment/deploy.md)
- [模型微调](../../raw/cli/capabilities/training-deployment/finetune.md)
- [Agent 基础设施](../../raw/cli/capabilities/agent-infrastructure.md)
- [Flow Agent](../../raw/cli/capabilities/agent-infrastructure/flow-agent.md)
- [Managed Agent](../../raw/cli/capabilities/agent-infrastructure/managed-agent.md)
- [Memory](../../raw/cli/capabilities/agent-infrastructure/memory.md)
- [Knowledge（原RAG）](../../raw/cli/capabilities/agent-infrastructure/rag.md)
- [联网搜索](../../raw/cli/capabilities/agent-infrastructure/web-search.md)
- [MCP & Skill](../../raw/cli/capabilities/agent-infrastructure/mcp-skill.md)
- [Sandbox](../../raw/cli/capabilities/agent-infrastructure/sandbox.md)
- [Security](../../raw/cli/capabilities/agent-infrastructure/security.md)
- [ParseX 文档解析](../../raw/cli/capabilities/agent-infrastructure/parsex.md)
- [平台管理与工具](../../raw/cli/capabilities/platform-management.md)
- [用量与配额](../../raw/cli/capabilities/platform-management/usage-quota.md)
- [监控、日志与告警](../../raw/cli/capabilities/platform-management/monitor-log-alert.md)
- [配置与工具](../../raw/cli/capabilities/platform-management/config.md)


