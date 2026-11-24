# capabilities

百炼平台的 capabilities 指 CLI 工具所支持的全部模型调用、基础设施管理与平台治理能力集合。它覆盖从基础模型推理（文本、多模态、语音、视觉）到高级智能体编排（Managed Agent、Flow Agent、RAG、Memory）、模型全生命周期（训练、部署、导入）及可观测性（监控、日志、告警）等完整技术栈。所有能力均通过统一 CLI 命令接口暴露，面向开发者提供可脚本化、可自动化、可审计的工程化接入方式。

## 支持的模型与功能

百炼 CLI 支持以下核心模型调用能力：

- **文本与全模态对话**：`bl text chat`（OpenAI 兼容 Chat Completions API）和 `bl omni`（Qwen-Omni 多模态输入/音频输出），支持系统提示、工具调用、思考模式（`--enable-thinking`）及内置联网搜索（`--enable-search`）[原文标题](../../raw/cli/capabilities/model-invocation/text-chat.md)  
- **图像生成与编辑**：`bl image generate`（Qwen-Image / wan2.x）和 `bl image edit`（图生图编辑），支持尺寸控制、负向提示词、水印开关及异步任务提交  
- **视频生成与编辑**：`bl video generate`（文生视频/图生视频）、`bl video ref`（参考生视频），支持首尾帧模式（`--last-frame`）、多主体引用及语音绑定（`--image-voice`）  
- **视觉理解**：`bl vision describe`（Qwen-VL），支持单图/视频描述、多轮提问（`--prompt`）及模型切换（`--model`）[原文标题](../../raw/cli/capabilities/model-invocation/vision.md)  
- **语音合成与识别**：`bl speech synthesize`（TTS）与 `bl speech recognize`（ASR），支持音色选择、SSML、热词即时注入（`--vocabulary`）及说话人分离（`--diarization`）  
- **批量推理**：`bl batch` 系列命令（convert/create/get/download），支持 CSV→JSONL 转换、异步 Batch 任务创建与结果下载，适用于大规模评估与数据处理 [原文标题](../../raw/cli/capabilities/model-invocation/batch.md)  
- **决策模型**：`bl decision`，专用于结构化判定（`choice`/`noul`/`score` 类型），需 Workspace 专属 Endpoint 和 `--workspace-id`  
- **智能体基础设施**：包括 Managed Agent（IaC 部署）、Flow Agent（应用级调用）、Knowledge（RAG）、Memory（[长期记忆](../concepts/long-term-memory.md)）、WebSearch（联网检索）、MCP & Skill（工具编排）、Sandbox（沙箱执行）等完整 AgentStudio 生态能力  

> **注意**：`bl text chat --batch` 是同步单请求批处理（非异步 Batch），而 `bl batch` 是独立的异步批量任务系统；二者用途、API 路径与参数约束完全不同，不可混用。

## 关键参数

通用关键参数贯穿多数命令，开发者需重点关注：

- **鉴权与路由**：`--api-key`（显式凭证）、`--base-url`（自定义 Endpoint）、`--workspace-id`（Workspace 专属服务必需）、`BAILIAN_WORKSPACE_ID`（环境变量优先级高）  
- **模型标识**：`--model <id>`（如 `qwen3.8-max`、`qwen-image-3.0`），部分命令支持 `--model auto`（MCP 自动路由），但会严格拒绝不兼容参数（如 `--seed` 在 `auto` 模式下报错）  
- **输入处理**：所有接受 URL 的参数（如 `--image`、`--video`、`--file-url`）均支持本地路径，CLI 自动上传至临时存储（有效期 48 小时）  
- **异步控制**：`--async`（立即返回任务 ID）、`--poll-interval`（轮询间隔）、`--follow`（阻塞等待完成）、`--concurrent <n>`（并行请求数）  
- **输出控制**：`--output <json|text>`、`--stream`（流式响应）、`--out <path>`（文件保存）、`--quiet` / `--verbose`（日志级别）  

## 使用方式

1. **初始化认证**：运行 `bl auth login --api-key <key>` 或 `bl auth login --console` 完成凭证配置  
2. **调用模型**：根据任务类型选择子命令，例如：  
   ```bash
   bl text chat --message "解释量子纠缠" --model qwen3-plus  
   bl image generate --prompt "赛博朋克风格城市夜景" --size 1024x1024  
   bl knowledge chat --message "产品售后政策是什么？" --agent-id aid-xxx  
   ```  
3. **管理资源**：使用 `bl dataset upload`、`bl finetune text create`、`bl deploy text create` 等完成训练与部署闭环  
4. **观测与治理**：通过 `bl usage stats`、`bl monitor overview`、`bl agents security alerts` 进行用量分析与安全审计  

所有命令均支持 `--help` 查看完整参数说明，且 CLI 会自动处理本地文件上传、Endpoint 解析、凭证继承等底层细节。

## 限制和注意事项

- **地域与账号限制**：Managed Agent、Flow Agent、Knowledge、Memory、Sandbox、Security 等能力仅对中国站（aliyun.com）账号开放；模型导入（`bl cmodel`）仅支持北京地域；决策模型仅支持 `cn-beijing` 和 `ap-southeast-1`  
- **配额与限流**：  
  - 记忆库（Memory）有账号级限流：`add` 120 QPM、`search` 300 QPM，合计 3000 QPM；HTTP 429 时需退避重试（≥1 秒间隔）  
  - [Token](../concepts/token.md) Plan 订阅 Key **无法授权 MCP 模式**（`bl search web --mode mcp`），必须使用默认 `model` 模式  
- **文件与数据约束**：  
  - 数据集上传上限：SFT/DPO 文本 ≤200MB，CPT ≤300MB，媒体 ZIP ≤2GB  
  - `bl batch convert` 仅支持文本与 Embedding 字段映射；多模态或多轮输入需直接编写 JSONL  
- **模型兼容性**：  
  - `--model auto` 模式严格校验参数兼容性，不兼容参数（如 `--seed`、`--prime`）直接报错，**不会回退到 REST 调用**  
  - 决策模型要求显式 `--workspace-id`，且 API Key 必须与目标地域匹配  
- **安全与高危操作**：删除类命令（如 `bl dataset delete`、`bl cmodel delete`、`bl memory delete`）默认阻断执行，必须显式传入 `--yes` 才生效

## 来源文档

- [模型调用](../../raw/cli/capabilities/model-invocation.md)
- [文本对话与全模态](../../raw/cli/capabilities/model-invocation/text-chat.md)
- [图像生成与编辑](../../raw/cli/capabilities/model-invocation/image.md)
- [视频生成与编辑](../../raw/cli/capabilities/model-invocation/video.md)
- [视觉理解](../../raw/cli/capabilities/model-invocation/vision.md)
- [语音合成与识别](../../raw/cli/capabilities/model-invocation/speech.md)
- [批量推理](../../raw/cli/capabilities/model-invocation/batch.md)
- [决策模型](../../raw/cli/capabilities/model-invocation/decision.md)
- [模型训练与部署](../../raw/cli/capabilities/training-deployment.md)
- [模型微调与部署](../../raw/cli/capabilities/training-deployment/finetune-deploy.md)
- [数据集管理](../../raw/cli/capabilities/training-deployment/dataset.md)
- [模型微调](../../raw/cli/capabilities/training-deployment/finetune.md)
- [模型导入](../../raw/cli/capabilities/training-deployment/cmodel.md)
- [模型部署](../../raw/cli/capabilities/training-deployment/deploy.md)
- [Managed Agent](../../raw/cli/capabilities/agent-infrastructure/managed-agent.md)
- [Agent 基础设施](../../raw/cli/capabilities/agent-infrastructure.md)
- [Flow Agent](../../raw/cli/capabilities/agent-infrastructure/flow-agent.md)
- [Knowledge（原RAG）](../../raw/cli/capabilities/agent-infrastructure/rag.md)
- [Memory](../../raw/cli/capabilities/agent-infrastructure/memory.md)
- [联网搜索](../../raw/cli/capabilities/agent-infrastructure/web-search.md)
- [Sandbox](../../raw/cli/capabilities/agent-infrastructure/sandbox.md)
- [ParseX 文档解析](../../raw/cli/capabilities/agent-infrastructure/parsex.md)
- [MCP & Skill](../../raw/cli/capabilities/agent-infrastructure/mcp-skill.md)
- [平台管理与工具](../../raw/cli/capabilities/platform-management.md)
- [Security](../../raw/cli/capabilities/agent-infrastructure/security.md)
- [用量与配额](../../raw/cli/capabilities/platform-management/usage-quota.md)
- [配置与工具](../../raw/cli/capabilities/platform-management/config.md)
- [监控、日志与告警](../../raw/cli/capabilities/platform-management/monitor-log-alert.md)


