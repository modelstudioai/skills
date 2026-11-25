# capabilities

百炼平台的 capabilities 指 CLI 工具所支持的全部模型调用、基础设施管理与平台治理能力。它覆盖从基础模型推理（文本、图像、视频、语音、视觉理解）到高级 Agent 基础设施（Managed/Flow Agent、Memory、Knowledge、MCP）、训练部署（微调、部署、导入）及可观测性（用量、监控、安全）的完整技术栈。所有能力均通过 `bl <category> <command>` 统一命令结构暴露，面向开发者提供可脚本化、可集成的终端操作接口。

## 支持的模型与功能

百炼 CLI 支持全模态模型调用与专用 AI 基础设施：

- **基础模型调用**：包括文本对话与 Omni 全模态（`bl text chat`, `bl omni`）、图像生成与编辑（`bl image generate/edit`）、视频生成与编辑（`bl video generate/ref`）、语音合成与识别（`bl speech synthesize/recognize`）、视觉理解（`bl vision describe`）以及决策模型（`bl decision`）[原文标题](../../raw/cli/capabilities/model-invocation.md)。  
- **批量与异步处理**：支持同步 Batch Chat（`bl text chat --batch`）和独立的异步批量任务（`bl batch create`），后者专用于大规模 CSV 转 JSONL 并提交至 `/v1/chat/completions` 或 `/v1/embeddings` 端点 [原文标题](../../raw/cli/capabilities/model-invocation/batch.md)。  
- **Agent 基础设施**：涵盖 Managed Agent（IaC 式生命周期管理）、Flow Agent（应用/工作流调用）、Memory（[长期记忆](../concepts/long-term-memory.md)写入与检索）、Knowledge（RAG 检索与问答）、MCP & Skill（工具编排与注册）、Sandbox（沙箱实例）、ParseX（文档与音视频解析）及联网搜索（`bl search web`）[原文标题](../../raw/cli/capabilities/agent-infrastructure.md)。  
- **训练与部署**：支持按模态（文本、音频、图像、视频）创建微调任务（`bl finetune text create`）、部署模型（`bl deploy text create`）及从 OSS 导入自定义模型（`bl cmodel import`）[原文标题](../../raw/cli/capabilities/training-deployment.md)。

> **注意**：`bl decision` 仅支持 `cn-beijing` 和 `ap-southeast-1` 地域，且必须显式提供 `--workspace-id`；而 `bl cmodel import` 当前仅在北京地域开放，且 `--weight-type full` 可能被服务端拒绝，实际仅推荐使用 `lora` [原文标题](../../raw/cli/capabilities/model-invocation/decision.md) 和 [原文标题](../../raw/cli/capabilities/training-deployment/cmodel.md)。

## 关键参数

各命令共享统一参数设计原则，核心通用参数包括：

- **鉴权与环境**：`--api-key`（覆盖环境变量 `DASHSCOPE_API_KEY`）、`--base-url`（覆盖 `DASHSCOPE_BASE_URL`）、`--workspace-id`（或 `BAILIAN_WORKSPACE_ID` 环境变量），用于路由至对应业务空间 Endpoint。  
- **输入抽象**：多数命令接受 `--file <path>`（本地路径）或 URL，CLI 自动上传至临时存储（有效期 48 小时），无需手动托管 [原文标题](../../raw/cli/capabilities/model-invocation/text-chat.md)。  
- **模型控制**：`--model <id>`（如 `qwen3.8-max`, `qwen-image-3.0`, `wan3.0-video`），部分命令支持 `--model auto` 启用 MCP 自动路由，但此时不兼容 `--seed`、`--watermark`、`--prime` 等非标准参数。  
- **输出与调试**：`--output <json|text>`、`--dry-run`（预览不执行）、`--verbose`（打印 HTTP 详情）、`--timeout <seconds>`（请求超时）。  
- **异步模式**：`--async`（立即返回任务 ID）、`--poll-interval <s>`（轮询间隔）、`--follow`（阻塞等待完成），广泛用于图像/视频生成、ParseX 解析、Sandbox 创建等长耗时操作。

## 使用方式

1. **初始化认证**：运行 `bl auth login --api-key <your-key>` 完成鉴权；若需访问 Workspace 专属资源（如 Decision、Memory、Knowledge），必须配置 `--workspace-id` 或设置 `BAILIAN_WORKSPACE_ID` 环境变量。  
2. **调用模型**：  
   - 文本对话：`bl text chat --message "你好" --model qwen-plus`  
   - 图像生成：`bl image generate --prompt "赛博朋克城市夜景" --size 1024x1024`  
   - 决策判定：`bl decision --workspace-id ws_xxx --state "用户要求退款" --questions '{"refund":{"type":"noul"}}'`  
3. **管理 Agent 基础设施**：  
   - 调用知识库：`bl knowledge chat --message "RAG 是什么？" --agent-id aid-xxx`  
   - 检索记忆：`bl memory search --user-id u123 --query "上次讨论的订单号"`  
   - 联网搜索：`bl search web --query "今日科技新闻" --mode mcp --count 5`  
4. **训练与部署**：  
   - 微调：`bl finetune text create --base-model qwen3-8b --datasets file-xxx`  
   - 部署：`bl deploy text create --model-name my-qwen-sft --plan ptu --input-tpm 10 --charge-type pre_paid --duration 30`  

## 限制和注意事项

- **地域与账号限制**：Managed Agent、Flow Agent、Memory、Knowledge、MCP、Sandbox、ParseX、Security 等 Agent 基础设施能力**仅对中国站（aliyun.com）账号开放**；模型导入（`bl cmodel`）和 Sandbox 仅支持 `cn-beijing` 地域。  
- **配额与限流**：  
  - Memory API 有账号级限流：`add` 120 QPM、`search` 300 QPM，合计 3000 QPM；收到 HTTP 429 时需退避重试，间隔 ≥1 秒 [原文标题](../../raw/cli/capabilities/agent-infrastructure/memory.md)。  
  - Token Plan 订阅 Key **无法授权 MCP 模式** 的联网搜索，必须使用 `--mode model` [原文标题](../../raw/cli/capabilities/agent-infrastructure/web-search.md)。  
- **文件与数据约束**：  
  - 数据集上传上限：SFT/DPO 文本 ≤200MB，CPT ≤300MB，媒体 ZIP ≤2GB [原文标题](../../raw/cli/capabilities/training-deployment/dataset.md)。  
  - `bl batch convert` 仅支持文本与 Embedding 的 CSV→JSONL 映射；多模态或多轮输入需直接编写 JSONL。  
- **模型兼容性**：`--enable-search` 仅对白名单模型（如 `qwen3.8-max`）默认开启；`--model auto` 模式下，不兼容参数会直接报错，**不会回退到 REST 调用**。  
- **高危操作防护**：`bl cmodel delete`、`bl memory delete`、`bl agents security alerts` 等删除类命令，未显式指定 `--yes` 时将阻断执行（退出码 7）。

## 来源文档

- [模型调用](../../raw/cli/capabilities/model-invocation.md)
- [文本对话与全模态](../../raw/cli/capabilities/model-invocation/text-chat.md)
- [图像生成与编辑](../../raw/cli/capabilities/model-invocation/image.md)
- [视频生成与编辑](../../raw/cli/capabilities/model-invocation/video.md)
- [语音合成与识别](../../raw/cli/capabilities/model-invocation/speech.md)
- [视觉理解](../../raw/cli/capabilities/model-invocation/vision.md)
- [模型训练与部署](../../raw/cli/capabilities/training-deployment.md)
- [决策模型](../../raw/cli/capabilities/model-invocation/decision.md)
- [批量推理](../../raw/cli/capabilities/model-invocation/batch.md)
- [模型微调](../../raw/cli/capabilities/training-deployment/finetune.md)
- [数据集管理](../../raw/cli/capabilities/training-deployment/dataset.md)
- [模型微调与部署](../../raw/cli/capabilities/training-deployment/finetune-deploy.md)
- [模型部署](../../raw/cli/capabilities/training-deployment/deploy.md)
- [模型导入](../../raw/cli/capabilities/training-deployment/cmodel.md)
- [Agent 基础设施](../../raw/cli/capabilities/agent-infrastructure.md)
- [Managed Agent](../../raw/cli/capabilities/agent-infrastructure/managed-agent.md)
- [Flow Agent](../../raw/cli/capabilities/agent-infrastructure/flow-agent.md)
- [Memory](../../raw/cli/capabilities/agent-infrastructure/memory.md)
- [Knowledge（原RAG）](../../raw/cli/capabilities/agent-infrastructure/rag.md)
- [MCP & Skill](../../raw/cli/capabilities/agent-infrastructure/mcp-skill.md)
- [联网搜索](../../raw/cli/capabilities/agent-infrastructure/web-search.md)
- [Sandbox](../../raw/cli/capabilities/agent-infrastructure/sandbox.md)
- [ParseX 文档解析](../../raw/cli/capabilities/agent-infrastructure/parsex.md)
- [Security](../../raw/cli/capabilities/agent-infrastructure/security.md)
- [用量与配额](../../raw/cli/capabilities/platform-management/usage-quota.md)
- [平台管理与工具](../../raw/cli/capabilities/platform-management.md)
- [监控、日志与告警](../../raw/cli/capabilities/platform-management/monitor-log-alert.md)
- [配置与工具](../../raw/cli/capabilities/platform-management/config.md)


