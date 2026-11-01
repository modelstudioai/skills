# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web UI 和工作流系统等场景。开发者可根据使用习惯和项目需求，选择兼容 OpenAI 或 Anthropic 协议的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证。所有工具均需使用专属 API Key 与匹配的 Base URL，且协议类型（OpenAI 兼容 vs Anthropic 兼容）必须与配置一致。

## 支持的模型/功能

百炼支持的模型能力因计费方案和客户端协议而异：

- **文本生成模型**：Qwen3 系列（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`）、GLM-5 系列（`glm-5.3`、`glm-5.2`）、DeepSeek V4 系列（`deepseek-v4.1-flash` 等）在 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版、Coding Plan 及按量计费中均有覆盖，但具体可用性以各套餐文档为准。例如，[Token Plan 个人版支持的模型](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md) 明确列出 `qwen3.8-max`、`qwen3.7-plus` 等；[Coding Plan 支持的模型](raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md) 则以 `qwen3.7-plus` 为默认推荐；而 [OpenClaw 配置示例](raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 中还包含 `qwen3.7-max` 和 `qwen3.6-flash` 的完整参数定义。

- **多模态与思考模式**：Qwen3.8 系列（`qwen3.8-max`/`qwen3.8-flash`）明确支持 `input: ["text", "image"]` 和 `reasoning: true`（见 [OpenClaw 文档](raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)），且需通过 `enable_thinking: true` 或 `effort: xhigh` 等参数启用深度推理；而 Qwen3.7 及更早版本虽部分支持图像输入（如 OpenCode 配置所示），但思考能力受限。

- **非文本模型限制**：千问工作助理仅支持文本生成模型（[千问](raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)），不支持图像/视频/语音类模型；Dify 等工作流平台明确**不支持**Token Plan/Coding Plan 套餐，仅允许按量计费接入（见 [Dify 文档](raw/model-user-guide/use-chat-client-or-development-tool/dify.md)）；Postman/cURL 等测试工具虽可调用文生图 API，但属于临时验证场景，不适用于生产集成（[使用Postman或cURL调用图像/视频生成API](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。

> **注意**：不同文档对同一模型的上下文窗口（`contextWindow`）描述存在差异。例如 OpenClaw 文档中 `qwen3.8-flash` 的 `contextWindow` 为 `983616`，而 OpenCode 文档中同模型 `limit.context` 也为 `983616`，但 Codex 文档中 `auto` 模型的 `context_window` 标注为 `1000000`。该差异源于不同客户端对“自动选型”模型的抽象层级不同，实际调用时应以所选具体模型 ID 的官方规格为准，避免依赖 `auto` 的模糊定义。

## 关键参数

配置客户端时需严格匹配以下三要素，缺一不可：

- **API Key**：必须与计费方案完全对应。Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key **互不通用**，且按量计费的 API Key 必须与 Base URL 所属地域一致（如华北2 的 Key 不能用于新加坡 Base URL）。错误匹配将直接导致 `401 Incorrect API key provided`（见 [Cline 文档](raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 和 [Qoder CN 文档](raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)）。

- **Base URL**：协议类型决定路径结构：
  - **OpenAI 兼容协议**（推荐多数客户端）：URL 以 `/compatible-mode/v1` 结尾，且最终请求路径需补全 `/chat/completions`（如 WorkBuddy 要求）；
  - **Anthropic 兼容协议**：URL 以 `/apps/anthropic` 结尾，部分客户端（如 Hermes Agent、Claude Code）需额外设置 `api_mode: anthropic_messages`。
  
  地域变量 `{WorkspaceId}` 仅适用于按量计费，必须替换为真实值（见 [Hermes Agent](raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[Cherry Studio](raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 等多处文档）。

- **Model ID**：必须与百炼平台发布的模型名**完全一致**（区分大小写、无额外符号）。例如 Cursor 要求 `glm-5.3` 写作 `glm-5-3`，Kilo CLI 配置中则保留 `glm-5.3`；Qwen3 系列命名统一为 `qwen3.x-y` 格式（如 `qwen3.8-flash`），不可简写为 `qwen38-flash` 或 `qwen3_8_flash`（见 [WorkBuddy 常见问题](raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)）。

## 使用方式

### 安装与初始化
- 终端工具（如 OpenClaw、Hermes Agent、Qwen Code）普遍要求 Node.js ≥18.0（部分需 ≥24.16），Windows 用户需通过 WSL2 或 Git Bash 运行（[Hermes Agent](raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[Claude Code](raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)）。
- 桌面客户端（如 Cursor、WorkBuddy、Cherry Studio）提供图形化安装包，无需命令行依赖。
- Web UI 工具（如 QwenPaw、DeepSeek Harness）通过 `npx` 或一键脚本启动，依赖 Python 或 uv 环境（[QwenPaw](raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)、[DeepSeek Harness](raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)）。

### 配置流程
1. **获取凭证**：登录百炼控制台，在对应套餐页面（如 [Token Plan 个人版](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)）复制专属 API Key。
2. **选择协议**：优先选用 OpenAI 兼容协议（`/compatible-mode/v1`），因其被 Cursor、WorkBuddy、Cherry Studio、QwenPaw 等绝大多数客户端原生支持；Anthropic 协议仅限 Hermes Agent、Claude Code 等少数工具。
3. **填写参数**：在客户端设置界面或配置文件中填入 Base URL、API Key 和 Model ID。注意：
   - OpenClaw 需编辑 `~/.openclaw/openclaw.json` 并禁用网关鉴权（`auth.mode: none`）用于本地调试；
   - Hermes Agent 使用 `hermes config set` 命令或直接编辑 `~/.hermes/config.yaml`；
   - Qwen Code 提供 `/auth` 交互式配置，亦支持手动编辑 `~/.qwen/settings.json`（见 [Qwen Code 文档](raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)）。
4. **验证连接**：发送简单请求（如“你好”）并检查响应。若失败，先确认网络连通性，再核对 Key/URL/Model 三者匹配性。

## 限制和注意事项

- **套餐适用范围严格隔离**：Token Plan 个人版、Token Plan 团队版、Coding Plan **仅限 AI 编程工具和 OpenClaw 类 Agent 使用**，禁止用于 Dify、n8n、Coze 等工作流平台，以及 Postman、cURL 等 API 测试工具（见 [更多工具](raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)）。违规使用可能导致订阅暂停或 API Key 封禁。
- **地域与免费额度绑定**：按量计费的新人免费额度**仅适用于华北2（北京）地域**。若配置新加坡或美国 Base URL，即使 Key 有效也会产生费用（见 [Cherry Studio 常见问题](raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）。
- **模型能力与客户端兼容性**：Qwen3 思考模式需客户端显式支持。例如 Cline 和 Qwen Code 要求勾选 **Enable R1 messages format** 或设置 `enable_thinking: true`；而 Cursor 免费版仅支持 `auto` 模式，无法调用指定模型（见 [Cursor 常见问题](raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)）。
- **移动端与版本要求**：千问 APP 接入 Token Plan 需升级至 **7.1.2 及以上版本**，低版本无入口（见 [千问](raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)）；Qoder CN 企业版不支持百炼接入，仅限个人社区版/专业版（见 [Qoder CN 文档](raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)


