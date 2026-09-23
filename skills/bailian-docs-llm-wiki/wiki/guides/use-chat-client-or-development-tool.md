# use chat client or development tool

阿里云百炼支持多种主流 AI 编程客户端与开发工具（如 Hermes Agent、Cursor、Qwen Code 等）通过标准 API 协议接入，开发者可基于自身工作流选择 CLI、IDE 插件、桌面应用或 Web 平台。所有工具均统一支持 OpenAI 兼容协议（`/compatible-mode/v1`）和 Anthropic 兼容协议（`/apps/anthropic`），并适配按量计费、[Token](../concepts/token.md) Plan（个人版/团队版）及 Coding Plan 三种订阅模式。配置核心为 `API Key` + `Base URL` + `Model ID` 三元组，需严格匹配计费方案与地域。

## 支持的模型/功能

- **通用文本生成模型**：所有工具均支持 Qwen3 系列（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`）、GLM-5 系列（需将 `.` 替换为 `-`，如 `glm-5.3` → `glm-5-3`）及 DeepSeek V4 系列模型。[Token](../concepts/token.md) Plan 与 Coding Plan 仅限文本生成类模型，不支持多模态或推理专用模型 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。
- **多模态与思考模式**：Qwen3.8-Max/Flash、Qwen3.7-Plus 等支持图像输入与 `enable_thinking` 参数；部分工具（如 Kilo CLI、OpenCode）需显式配置 `thinking.budgetTokens` [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)。
- **办公与专业场景**：千问 APP 工作助理仅支持 [Token](../concepts/token.md) Plan 模型处理文档/表格任务，且**不支持按量计费或 Coding Plan** [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)；Dify 等工作流平台则**仅允许使用按量计费 API Key**，Token Plan/Coding Plan 套餐在此类平台中属违规使用 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。
- **图像/视频生成**：Postman/cURL 等 HTTP 工具适用于异步调用万相（Wan2.x）等 AIGC 模型，需分“创建任务”与“轮询查询”两步操作 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：文档 17 明确指出，Token Plan 个人版、团队版及 Coding Plan **不支持**在 Dify、n8n、Coze 等工作流/自动化平台中使用；若误用，可能导致订阅暂停或 API Key 封禁。该限制与文档 16 中 Dify 的强制要求一致，无矛盾。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 计费方案专属凭证，**不可跨方案混用**。Token Plan 个人版、团队版、Coding Plan 的 Key 互不通用；按量计费 Key 必须与 Base URL 地域一致 | `sk-xxxxxxxxxxxxx`（按量计费）；Token Plan 个人版 Key 仅可在 [Token Plan 个人版页面](https://bailian.console.aliyun.com/cn-beijing/subscription/overview) 获取 |
| `Base URL` | 决定协议与地域。OpenAI 协议路径为 `/compatible-mode/v1`，Anthropic 协议为 `/apps/anthropic`；地域需替换 `{WorkspaceId}` | Token Plan 个人版 OpenAI：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；按量计费（北京）Anthropic：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `Model ID` | 模型标识符，需与套餐支持列表一致。部分工具（如 Cursor、Cherry Studio）要求模型名中 `.` 替换为 `-`（如 `kimi-k2.5` → `kimi-k2-5`） | `qwen3.7-plus`, `glm-5-3`, `auto` |
| `api_mode` / `wire_api` | 协议模式标识。Hermes Agent 需设 `anthropic_messages`；Codex 可选 `responses`；DeepSeek Harness 使用 `openai-completions` | `anthropic_messages`, `responses`, `openai-completions` |

## 使用方式

1. **安装工具**：根据操作系统选择安装方式（如 `npm install -g`、一键脚本、GUI 安装包）。Windows 用户多数需 WSL2 或 Git Bash（如 Hermes Agent、Claude Code）[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。
2. **配置凭证**：
   - CLI 工具（Hermes、Qwen Code、Kilo CLI）通常通过命令行配置（`hermes config set`）或编辑 `settings.json`/`config.json`；
   - 桌面应用（Cursor、Cherry Studio、Qoder）在 GUI 设置中填写 API Key、Base URL 和 Model ID；
   - IDE 插件（Cline、Qoder JetBrains）在插件设置界面完成配置；
   - Web 平台（Dify）需安装对应插件（如“通义千问”），并在插件设置中填入 Key 与端点。
3. **验证与调用**：发送测试请求（如“你好”），确认响应正常；高级功能（如思考模式、多模态）需在工具设置中显式启用。

## 限制和注意事项

- **地域与免费额度绑定**：按量计费的新人免费额度**仅限华北2（北京）地域**，使用新加坡或美国地域会产生费用 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **模型兼容性限制**：Cursor 免费版仅支持 `auto` 模式，调用自定义模型需升级至 Pro 版本；Qoder CN 企业版不支持接入百炼 [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)。
- **错误排查优先级**：报错 `401 Incorrect API key provided` 首先检查 Key 与 Base URL 是否同属一方案（如 Token Plan 团队版 Key 配 Token Plan 团队版 URL）；报错 `400 InternalError.Algo.InvalidParameter` 多因未开启思考模式（需勾选 `Enable R1 messages format`）[Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)。
- **配置文件安全**：OpenClaw 默认禁用鉴权（`auth.mode: none`），仅适合单机本地使用；生产环境必须运行 `openclaw doctor --fix` 启用 token 鉴权 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。
- **协议差异**：Anthropic 协议（`/apps/anthropic`）要求 `api_mode: anthropic_messages`，而 OpenAI 协议（`/compatible-mode/v1`）无需此参数；混用会导致 `404 Not Found` 错误。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)


