# getting started

阿里云百炼 CLI 是面向 AI Agent 的命令行工具，将百炼平台的全模态能力（文本、图像、视频、语音、视觉理解、RAG、记忆等）封装为结构化工具调用。开发者只需完成安装与鉴权，即可通过自然语言指令驱动 Agent 调度底层服务，无需手动构造 API 请求。该工具开源免费，按实际调用计费，新用户享有免费额度。

## 支持的模型/功能

CLI 提供覆盖模型调用、训练部署、Agent 基础设施及平台管理四大类能力，共 10+ 项原子能力：

- **模型调用**：支持文本对话（含 Omni 全模态）、图像生成与编辑、视频生成与编辑、语音合成（TTS）与识别（ASR）、视觉理解（图像/文档/视频解析）、ParseX 文档结构化解析、批量推理、决策模型等；详情见 [阿里云百炼 CLI](../../raw/cli/getting-started/overview.md) 中的「能力参考」章节。
- **Agent 基础设施**：内置 Managed Agent、Flow Agent、RAG 知识库检索、[长期记忆](../concepts/memory.md)（Memory）、联网搜索、MCP & Skill 编排、Sandbox 沙箱等，支撑复杂智能体工作流。
- **训练与部署**：支持数据集管理、多模态微调（文本/音频/图像/视频）、模型部署（含吞吐预留）、自定义模型导入（OSS）等。

> **注意**：[快速开始](../../raw/cli/getting-started/quickstart.md) 中提到“Agent 可自动阅读 `install.md` 并安装 CLI”，但该路径 `https://bailian.aliyun.com/cli/install.md` 在当前文档体系中并不存在——正确路径应为 [安装与鉴权](../../raw/cli/getting-started/installation.md)。请以后者为准，避免使用已失效或未同步的外部链接。

## 关键参数

- `--api-key`：用于普通 API Key 鉴权，需配合 `bl auth login --api-key <key>` 使用。
- `--config token-plan`：指定 Token Plan Profile，必须与订阅的 `sk-sp-Key` 配合使用（`bl auth login --config token-plan --api-key <sk-sp-Key>`）。
- `--console`：启用控制台登录模式，推荐交互式环境使用，自动打通应用列表、用量查询等控制台能力。
- `--output json`：标准化输出格式，适用于脚本集成与状态校验（如 `bl auth status --output json`）。
- `DASHSCOPE_API_KEY` / `BAILIAN_ACCESS_KEY_ID` 等环境变量：支持无配置文件方式鉴权，适用于 CI/CD 等非交互场景。

## 使用方式

1. **安装 CLI**  
   - Node.js ≥ 18.17.0 环境：`npm install -g bailian-cli`（**禁止**使用 pnpm/yarn 安装）；  
   - 无 Node.js 环境：macOS/Linux 执行 `curl -fsSL https://bailian.aliyun.com/cli/install.sh | bash`，Windows 执行 `irm https://bailian.aliyun.com/cli/install.ps1 | iex`。  
   安装后验证：`bl --version`。

2. **安装 Skills**  
   运行 `bl skill init` 一键安装全部官方 Skills（含 `bailian-protocol`），这是 [安装与鉴权](../../raw/cli/getting-started/installation.md) 推荐的标准流程。

3. **鉴权配置**  
   根据场景选择：
   - 交互式开发：`bl auth login --console`；  
   - CI/远程环境：`bl auth login --api-key <key>`；  
   - Token Plan 用户：`bl auth login --config token-plan --api-key <sk-sp-Key>`；  
   - AK/SK 场景：先用 `bl auth generate-access-token` 生成临时令牌。  
   鉴权后务必执行 `bl auth status --output json` 校验生效凭据。

4. **发起调用**  
   完成上述步骤后，可直接向 Agent 下发自然语言需求（如“生成 6 张黑色夏日男装 T 恤电商主图”），Agent 将自动路由至对应模型（如 `qwen-image-3.0`）并调用 CLI 执行。

## 限制和注意事项

- CLI 本身不收费，但所有模型调用、RAG 检索、存储、沙箱实例等均按实际用量计费；Token Plan 订阅用户需确保使用 `token-plan` Profile，否则无法扣减套餐额度。
- `bl skill init` 是首选 Skills 安装方式；若降级使用 `npx skills@1.5.18`，需注意其要求 Node.js ≥ 22.20（Node.js 18 环境必须固定 `@1.5.18` 版本）。
- 阿里云 CLI 用户可通过 `aliyun bl` 调用全部 CLI 命令，此时 AccessKey 由阿里云 CLI 环境变量自动注入，无需重复配置百炼鉴权信息。
- **重要安全提醒**：`bl auth status` 输出已脱敏，严禁在日志、仓库或聊天记录中硬编码或回显完整 API Key；生产环境应通过密钥管理服务注入 `DASHSCOPE_API_KEY` 等环境变量。

## 来源文档

- [阿里云百炼 CLI](../../raw/cli/getting-started/overview.md)
- [安装与鉴权](../../raw/cli/getting-started/installation.md)
- [快速开始](../../raw/cli/getting-started/quickstart.md)


