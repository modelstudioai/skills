# getting started

阿里云百炼 CLI 是面向 AI Agent 的命令行工具，将百炼平台的全模态能力（文本、图像、视频、语音、视觉理解、RAG、记忆等）封装为结构化工具调用。开发者安装并完成鉴权后，即可通过自然语言指令驱动 Agent 调度底层服务，无需手动编写 API 请求。本文档汇总核心入门路径，覆盖能力范围、关键参数、使用方式及约束条件。

## 支持的模型/功能

CLI 提供 10+ 类原子能力，按产品线组织为四大类：  
- **模型调用**：支持文本对话（含 Omni 全模态）、[图像生成与编辑](../capabilities/model-invocation/image.md)、[视频生成与编辑](../capabilities/model-invocation/video.md)、语音合成与识别（TTS/ASR）、视觉理解（文档/图像/视频解析）、ParseX 文档解析、批量推理、决策模型；  
- **模型训练与部署**：涵盖数据集管理、模型微调（文本/音频/图像/视频）、模型部署（含吞吐预留）、自定义模型导入；  
- **Agent 基础设施**：包括 Managed Agent、Flow Agent、[RAG](../capabilities/agent-infrastructure/rag.md)、Memory、联网搜索、MCP & Skill、Sandbox；  
- **平台管理与工具**：用量与配额、监控日志告警、配置与通用工具。  
完整能力清单见 [阿里云百炼 CLI](../../raw/cli/getting-started/overview.md) 文档。

## 关键参数

CLI 鉴权支持多种凭据类型，需根据场景选择并显式指定配置上下文：  
- `--console`：控制台登录（推荐交互式环境），自动打通 OpenAPI 与控制台能力；  
- `--api-key <key>`：普通 API Key，适用于按量计费场景；  
- `--config token-plan --api-key <sk-sp-Key>`：[Token](../concepts/token.md) Plan 订阅 Key，**必须显式指定 `--config token-plan`**，否则不会扣减套餐额度；  
- `--access-key-id` / `--access-key-secret`：用于生成临时访问令牌（如配合 Postman），支持 STS `--security-token`；  
- 环境变量 `DASHSCOPE_API_KEY` 可替代配置文件，但 `BAILIAN_ACCESS_KEY_ID` 等仅在需要 OpenAPI 或控制台能力时生效。  
> **注意**：文档 3 中称“执行 `bl auth login --console` 即可”，但文档 2 明确指出 [Token](../concepts/token.md) Plan 必须使用 `--config token-plan` 参数且需单独切换 Profile（`bl config use --name token-plan`），否则 CLI 默认使用 `default` Profile 导致不扣减套餐额度 —— 此处存在操作指引不一致，应以 [安装与鉴权](../../raw/cli/getting-started/installation.md) 为准。

## 使用方式

三步完成接入：  
1. **安装 CLI**：推荐二进制脚本（无 Node.js 依赖）：  
   ```bash
   curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash  # macOS/Linux
   irm https://bailian.aliyun.com/cli/install.ps1 | iex         # Windows PowerShell
   ```  
   或 npm 安装（需 Node.js ≥ 18.17.0）：`npm install -g bailian-cli`；  
2. **鉴权配置**：执行 `bl auth login --console`（交互式）或 `bl auth login --api-key <key>`（非交互式），随后用 `bl auth status --output json` 校验；  
3. **下发需求**：向已集成 Skills 的 Agent 发送自然语言指令，例如 `帮我生成一套电商主图，6 张图，产品是纯黑色夏日男装 T 恤`，Agent 将自动调用 `bl image generate` 等命令完成任务。  
详细步骤见 [快速开始](../../raw/cli/getting-started/quickstart.md)。

## 限制和注意事项

- CLI 工具本身免费开源，但模型调用、存储、带宽等按实际用量计费，新用户享有免费额度；  
- `bl skill init` 是安装全部官方 Skills 的首选方式；若不可用，需固定 `skills@1.5.18`（Node.js 18 环境不兼容新版）；  
- **AK/SK 不与 API Key 混用**：CLI 按“命令参数 → 百炼环境变量 → 百炼配置 → 阿里云环境变量”顺序解析凭据，**不跨来源拼接字段**（如不能用 `--api-key` + 环境变量 `BAILIAN_ACCESS_KEY_ID` 组合）；  
- 控制台类命令（如 `app list`, `usage free`）必须完成 `--console` 登录；[Token](../concepts/token.md) Plan 用户若需席位管理，还需额外提供 AK/SK；  
- 所有敏感信息（如 API Key）严禁明文输出或写入日志/仓库，`bl auth status` 仅返回脱敏字段。

## 来源文档

- [阿里云百炼 CLI](../../raw/cli/getting-started/overview.md)
- [安装与鉴权](../../raw/cli/getting-started/installation.md)
- [快速开始](../../raw/cli/getting-started/quickstart.md)


