# capabilities

百炼平台 CLI 提供统一命令行接口，支持调用全模态模型能力（文本、图像、视频、语音、视觉理解）、批量推理、决策建模，以及 Agent 基础设施（RAG、Memory、MCP、Sandbox 等）和平台管理功能（用量、监控、配置）。所有能力均通过 `bl <category> <command>` 结构化组织，依赖 API Key 鉴权，并深度集成工作空间（Workspace）上下文与 Prime Endpoint 路由机制。

## 支持的模型与功能

CLI 覆盖以下核心模型能力类别：

- **文本对话与全模态**：支持 `bl text chat`（OpenAI 兼容 Chat Completions）和 `bl omni`（Qwen-Omni 多模态对话），含系统提示、工具调用、思考模式（`--enable-thinking`）、联网搜索（`--enable-search`）等 [文本对话与全模态](../../raw/cli/capabilities/model-invocation/text-chat.md)。
- **图像生成与编辑**：`bl image generate`（文生图）与 `bl image edit`（图生图/指令编辑），支持尺寸、负向提示词、水印、异步任务等参数 [图像生成与编辑](../../raw/cli/capabilities/model-invocation/image.md)。
- **视频生成与编辑**：`bl video generate`（文/图生视频）、`bl video ref`（参考生视频），支持首尾帧、多主体、语音对齐及分辨率控制 [视频生成与编辑](../../raw/cli/capabilities/model-invocation/video.md)。
- **语音合成与识别**：`bl speech synthesize`（TTS）与 `bl speech recognize`（ASR），支持音色、语速、热词增强（`--vocabulary`）、说话人分离（`--diarization`）等 [语音合成与识别](../../raw/cli/capabilities/model-invocation/speech.md)。
- **视觉理解**：`bl vision describe`（Qwen-VL 图像/视频内容描述与问答），支持自定义 prompt 与多模型切换 [视觉理解](../../raw/cli/capabilities/model-invocation/vision.md)。
- **批量推理**：`bl batch` 系列命令（convert/create/get/download），用于 CSV → JSONL 转换、异步批量任务提交与结果下载，独立于单请求 `--batch` 模式 [批量推理](../../raw/cli/capabilities/model-invocation/batch.md)。
- **决策模型**：`bl decision` 对业务状态进行结构化判定（`choice`/`noul`/`score` 类型），需 Workspace 专属 Endpoint 和 `--workspace-id` [决策模型](../../raw/cli/capabilities/model-invocation/decision.md)。
- **Agent 基础设施**：包括 Managed Agent（IaC 部署）、Flow Agent（应用调用）、RAG（知识库检索/问答）、Memory（[长期记忆](../concepts/memory.md)）、MCP & Skill（工具编排）、Sandbox（沙箱执行）等，全部需中国站账号支持 [Agent 基础设施](../../raw/cli/capabilities/agent-infrastructure.md)。

> **注意**：`bl text chat --batch` 是同步单请求模式，而 `bl batch create` 是异步文件批量任务，二者完全独立；文档中多次强调“`bl batch` 与同步单请求 `bl text chat --batch` 分开使用”，混淆可能导致任务提交失败或超时。

## 关键参数

通用关键参数贯穿多数命令，体现平台一致性设计：

- **身份与路由**：`--workspace-id`（或环境变量 `BAILIAN_WORKSPACE_ID`）用于解析 Prime Endpoint 或业务空间专属 API；`--base-url` / `DASHSCOPE_BASE_URL` 优先级最高，显式覆盖默认路由。
- **模型选择**：`--model <id>` 为绝大多数命令的可选参数，默认值因能力而异（如 `qwen3.8-max`、`qwen-image-3.0`、`wan3.0-video`），部分命令（如 `bl decision`）默认为预览模型 `decision-model-preview`。
- **输入处理**：所有接受 URL 的参数（如 `--image`、`--audio`、`--video`）均支持本地路径，CLI 自动上传至临时存储（有效期 48 小时）[图像生成与编辑](../../raw/cli/capabilities/model-invocation/image.md)。
- **异步控制**：`--async`（立即返回任务 ID）、`--poll-interval`（轮询间隔）、`--concurrent <n>`（并行请求数）是 AIGC 类命令（image/video/speech）的标准组合；`--follow`（持续轮询至完成）常见于 `bl batch get` 和 `bl parsex result`。
- **输出控制**：`--output <format>`（json/text）、`--stream`（流式响应）、`--out <path>`（文件保存）为通用输出选项；`--list-voices`、`--list-tools` 等开关用于元数据发现。

## 使用方式

1. **基础调用**：以 `bl <category> <command>` 启动，例如 `bl text chat --message "你好"` 或 `bl image generate --prompt "星空下的城堡"`。
2. **参数组合**：按需叠加参数，如 `bl speech synthesize --text "欢迎" --voice Tina --format mp3 --out welcome.mp3`。
3. **文件批量处理**：
   - 单文件：直接传入本地路径（自动上传）；
   - 多文件/CSV：使用 `bl batch convert` 生成 JSONL，再 `bl batch create` 提交异步任务；
   - 大媒体集：先 `bl dataset upload` 上传 ZIP 归档，再在微调/部署中引用。
4. **Workspace 与 Prime**：涉及工作空间能力（决策、RAG、Memory、Sandbox 等）必须提供 `--workspace-id`；启用 Prime 模式需显式指定 `--model` 且仅限 Chat Completions API。
5. **调试与验证**：
   - 所有命令支持 `--help` 查看完整参数；
   - `--dry-run` 预览不执行（如 `bl batch create --dry-run`）；
   - `bl managed-agent validate` 和 `bl dataset validate` 支持离线配置/数据校验。

## 限制和注意事项

- **地域与账号限制**：Agent 基础设施（Managed Agent、RAG、Memory、MCP、Sandbox）、联网搜索（`bl search web`）及 ParseX 文档解析仅对中国站（aliyun.com）账号开放；模型导入（`bl cmodel`）仅在北京地域可用。
- **配额与限流**：各能力受模型级 QPM/TPM 限制（`bl quota list` 可查），Memory API 有账号级硬限流（add 120 QPM、search 300 QPM）；Token Plan 订阅 Key 不支持 MCP 模式 [联网搜索](../../raw/cli/capabilities/agent-infrastructure/web-search.md)。
- **参数兼容性**：`--model auto` 模式仅接受 MCP 工具支持的参数（如 `--prompt`、`--voice`），`--seed`、`--watermark`、`--async` 等 REST 特有参数会直接报错，**不会回退到 REST 调用**（见 image/video/speech 文档）。
- **安全与高危操作**：删除类命令（`bl dataset delete`、`bl cmodel delete`、`bl memory delete`）默认阻断执行，必须显式传入 `--yes`；`bl deploy text create` 创建部署会产生成本，需确认后执行。
- **版本与兼容性**：CLI 命令行为随版本演进，例如 `bl finetune text create` 在 bl 2.8.4 核实，而 RL/OPD 命令基于 bl 2.10.4；升级前应查阅 [更新日志](../../raw/cli/changelog-group/changelog.md)。

## 来源文档

- [模型调用](../../raw/cli/capabilities/model-invocation.md)
- [文本对话与全模态](../../raw/cli/capabilities/model-invocation/text-chat.md)
- [视频生成与编辑](../../raw/cli/capabilities/model-invocation/video.md)
- [图像生成与编辑](../../raw/cli/capabilities/model-invocation/image.md)
- [语音合成与识别](../../raw/cli/capabilities/model-invocation/speech.md)
- [视觉理解](../../raw/cli/capabilities/model-invocation/vision.md)
- [批量推理](../../raw/cli/capabilities/model-invocation/batch.md)
- [数据集管理](../../raw/cli/capabilities/training-deployment/dataset.md)
- [决策模型](../../raw/cli/capabilities/model-invocation/decision.md)
- [模型训练与部署](../../raw/cli/capabilities/training-deployment.md)
- [模型微调与部署](../../raw/cli/capabilities/training-deployment/finetune-deploy.md)
- [模型微调](../../raw/cli/capabilities/training-deployment/finetune.md)
- [模型部署](../../raw/cli/capabilities/training-deployment/deploy.md)
- [Agent 基础设施](../../raw/cli/capabilities/agent-infrastructure.md)
- [模型导入](../../raw/cli/capabilities/training-deployment/cmodel.md)
- [Managed Agent](../../raw/cli/capabilities/agent-infrastructure/managed-agent.md)
- [RAG](../../raw/cli/capabilities/agent-infrastructure/rag.md)
- [Flow Agent](../../raw/cli/capabilities/agent-infrastructure/flow-agent.md)
- [联网搜索](../../raw/cli/capabilities/agent-infrastructure/web-search.md)
- [Memory](../../raw/cli/capabilities/agent-infrastructure/memory.md)
- [MCP & Skill](../../raw/cli/capabilities/agent-infrastructure/mcp-skill.md)
- [Security](../../raw/cli/capabilities/agent-infrastructure/security.md)
- [Sandbox](../../raw/cli/capabilities/agent-infrastructure/sandbox.md)
- [平台管理与工具](../../raw/cli/capabilities/platform-management.md)
- [用量与配额](../../raw/cli/capabilities/platform-management/usage-quota.md)
- [ParseX 文档解析](../../raw/cli/capabilities/agent-infrastructure/parsex.md)
- [监控、日志与告警](../../raw/cli/capabilities/platform-management/monitor-log-alert.md)
- [配置与工具](../../raw/cli/capabilities/platform-management/config.md)


