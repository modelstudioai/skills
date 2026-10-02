# use chat client or development tool

阿里云百炼支持多种主流 AI 编程客户端与开发工具（如 Claude Code、Qwen Code、Cursor 等）及通用开发平台（如 Dify、Postman），通过 OpenAI 兼容或 Anthropic 兼容协议接入。开发者可根据使用场景选择合适工具：终端/IDE [插件](../concepts/plugin.md)类工具（如 Hermes Agent、Cline）适用于高频代码辅助；桌面客户端（如 Cherry Studio、Chatbox）适合多模态交互；而工作流平台（如 Dify）则面向应用构建，但需注意计费方案的适用性限制。

## 支持的模型/功能

百炼支持的模型能力因接入工具和计费方案而异：

- **文本生成模型**：所有工具均支持 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash` 等 Qwen3 系列模型；部分工具（如 OpenCode、Kilo CLI）还支持 `glm-5.3`、`glm-5.2` 及 `deepseek-v4.*` 系列模型。
- **思考模式（Reasoning）**：Qwen3 系列中带 `-max` 后缀的模型默认启用深度思考，需在请求体中显式设置 `enable_thinking: true` 或通过客户端开关启用（如 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 要求勾选 **Enable R1 messages format**）。
- **多模态能力**：`qwen3.8-max` 和 `qwen3.8-flash` 支持图像输入（`input: ["text", "image"]`），但仅限 CLI/Agent 类工具（如 [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)、[OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)）完整支持；千问 APP 工作助理仅支持文档/表格等办公任务，不支持图像。
- **非文本模型限制**：万相（文生图）、Qwen-VL、QVQ、Qwen-Omni 等模型**不可直接在 Dify [插件](../concepts/plugin.md)中配置**，需通过 HTTP 节点调用原生 API（详见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 文档）；Postman/cURL 仅用于测试，不适用于生产环境。

> **注意**：[千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md) 工作助理明确**仅支持 [Token](../concepts/token.md) Plan（个人版/团队版）**，不支持按量计费或 Coding Plan；而 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 则**明确不支持 [Token](../concepts/token.md) Plan 和 Coding Plan**，仅允许使用按量计费 API Key，违规使用将导致订阅暂停或 Key 封禁。

## 关键参数

所有工具共用以下核心参数，但配置方式与协议适配存在差异：

| 参数 | 说明 | 协议差异 |
|------|------|----------|
| `API Key` | 各计费方案专属凭证，**不可跨方案混用**（如 [Token](../concepts/token.md) Plan 团队版 Key 不能用于 Coding Plan Base URL） | OpenAI 协议使用 `Authorization: Bearer <key>`；Anthropic 协议使用 `X-Anthropic-API-Key: <key>` |
| `Base URL` | 必须与 API Key 所属地域和计费方案严格匹配：<br>- Token Plan：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）<br>- Coding Plan：`https://coding.dashscope.aliyuncs.com/v1`（OpenAI）或 `/apps/anthropic`（Anthropic）<br>- 按量计费：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic） | OpenAI 协议路径为 `/compatible-mode/v1`；Anthropic 协议路径为 `/apps/anthropic`（部分工具如 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 强制要求 Anthropic 协议） |
| `Model ID` | 模型标识符，需与套餐支持列表一致。注意命名规范：<br>- `kimi-k2.6` → `kimi-k2-6`（Cursor 要求）<br>- `glm-5.3` → `glm-5-3`（Cursor/Qoder CN 要求） | Anthropic 协议下部分工具（如 Claude Code）支持 `auto` 自动路由，OpenAI 协议下通常需指定具体 ID |

## 使用方式

### 1. 工具安装与初始化
- **CLI 工具**（Claude Code、Hermes Agent、Qwen Code、Kilo CLI）：依赖 Node.js ≥18（部分如 OpenClaw 要求 Node.js ≥22.19.0），通过 `npm install -g` 安装；Windows 用户需 WSL2 或 Git Bash。
- **桌面客户端**（Cursor、Cherry Studio、Qoder IDE）：从官网下载安装包，启动后进入设置界面配置。
- **IDE [插件](../concepts/plugin.md)**（Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 市场搜索安装，配置入口位于侧边栏或设置菜单。
- **Web 平台**（Dify、OpenClaw Web UI）：访问对应网址，通过 UI 配置模型提供商。

### 2. 凭证配置流程
- **环境变量方式**（Codex）：`export OPENAI_API_KEY="YOUR_KEY"`，并配置 `config.toml` 指向 `env_key`。
- **配置文件方式**（Claude Code、Hermes Agent、OpenCode）：编辑 `~/.claude/settings.json`、`~/.hermes/config.yaml` 或 `~/.config/opencode/opencode.json`，填入 `apiKey` 和 `baseURL`。
- **UI 配置方式**（Cursor、Cherry Studio、Qoder CN）：在设置 > 模型 > 添加中，填写 API Key、Base URL 和 Model ID。
- **交互式配置**（Qwen Code、Qoder CLI）：启动后输入 `/auth` 或 `/model` 进入 TUI 向导完成配置。

### 3. 高级功能启用
- **思考模式**：Qwen3 `-max`/`-flash` 模型需显式开启。在 Cursor 中需手动开启“Thinking Mode”；在 Cline/Qoder 中需勾选 **Enable R1 messages format**；在 Dify 的 LLM 节点中需打开“思考模式”开关。
- **多模型切换**：多数工具（如 Chatbox、Qoder CN）支持对话界面右上角下拉菜单临时切换；QwenPaw、Cherry Studio 等提供“默认 LLM”全局设置。
- **技能扩展**：Qwen Code、Cline、Qoder 等支持通过百炼 CLI 注册 Skill（如图像/视频生成），需先 `npm install -g bailian-cli` 并配置 API Key。

## 限制和注意事项

- **计费方案适用性限制**：
  - Token Plan 个人版/团队版、Coding Plan **仅限 AI 编程工具与 OpenClaw 类 Agent 使用**（如 Claude Code、Qwen Code、OpenClaw、Hermes Agent），**禁止用于 Dify、n8n、Coze 等工作流平台及 Postman、cURL 等 API 测试工具**（见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 文档）。
  - 千问 APP 工作助理**仅支持 Token Plan**，不支持按量计费或 Coding Plan。
  - Dify **仅支持按量计费**，使用其他方案 Key 将触发风控封禁。

- **地域与 Key 绑定**：按量计费 API Key 与 Workspace ID 强绑定，北京地域 Key 不可用于新加坡 Base URL；Token Plan/Coding Plan Key 无地域区分，但 Base URL 必须匹配（如 Token Plan 统一为 `token-plan.cn-beijing.maas.aliyuncs.com`）。

- **模型兼容性问题**：
  - Cursor 免费版**仅支持 `auto` 模式**，调用具体模型（如 `qwen3.8-max`）需升级至 Pro 版本。
  - Qoder CN 企业版**不支持接入百炼**，仅限个人社区版/专业版。
  - 部分工具（如 Cursor、Qoder CN）对模型 ID 有特殊格式要求（`.` → `-`），填错将返回 404。

- **错误排查重点**：
  - `401 Unauthorized`：确认 Key 与 Base URL 方案一致（Token Plan Key + Token Plan URL），且无空格/换行。
  - `400 InvalidParameter`：检查是否遗漏 `enable_thinking` 参数（Qwen3 `-max`/`-flash`）或未勾选 R1 格式（Cline/Qoder）。
  - `上下文超限`：在模型提供商设置中调整 `max_tokens`（如 QwenPaw 进阶配置）或切换更高上下文窗口模型（如 `qwen3.8-max` 支持 983616 tokens）。

- **安全提示**：本地配置文件（如 `~/.claude/settings.json`）含敏感 Key，建议设为 `chmod 600`；生产环境避免硬编码 Key，应使用环境变量或密钥管理服务。

## 来源文档

- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


