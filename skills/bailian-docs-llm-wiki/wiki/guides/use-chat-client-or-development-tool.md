# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web UI 和自动化工作流等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证与协议。所有工具均基于 OpenAI 或 Anthropic 兼容 API 协议，无需修改业务逻辑即可快速切换。

## 支持的模型/功能

- **通用文本生成模型**：所有工具均支持 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.6-flash` 等 Qwen 系列模型；部分工具（如 OpenClaw、QwenPaw）还支持 `glm-5.3`、`deepseek-v4-pro` 等第三方模型 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)。
- **多模态能力**：Qwen Code、Cursor、Qoder 等支持图像输入与理解（需启用 `qwen3.8-max` 等支持 `image` 输入的模型），但千问 APP 工作助理仅限文档/表格处理，不支持图像 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。
- **思考模式（Reasoning）**：`qwen3.7+` 及更高版本支持 `enable_thinking` 参数，需在客户端显式开启（如 Cline 中需勾选 **Enable R1 messages format**，Qwen Code 中需设置 `generationConfig.extra_body.enable_thinking: true`）[原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)。
- **图像/视频生成**：仅支持通过 Postman/cURL 等 HTTP 工具直接调用异步 API（如 `wan2.6-t2i`），Dify 等工作流平台需通过 HTTP 节点接入，不支持在 Chatbox、Cursor 等聊天客户端中直接触发 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：Dify 明确不支持 [Token](../concepts/token.md) Plan 个人版、[Token](../concepts/token.md) Plan 团队版和 Coding Plan 接入，仅允许使用按量计费 API Key；将套餐 API Key 用于 Dify 将被视为违规 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，指定百炼服务端点。OpenAI 协议用 `/compatible-mode/v1`，Anthropic 协议用 `/apps/anthropic` | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | 必填，必须与 `base_url` 所属计费方案严格匹配（Token Plan 个人版 Key 不能用于 Coding Plan） | `sk-xxxxxxxxxxxxx` |
| `model` | 必填，模型 ID 需与套餐支持列表完全一致（区分大小写，无额外后缀），如 `qwen3.7-plus`；`auto` 表示由服务端自动路由 | `qwen3.8-flash` |
| `workspace_id` | 按量计费必需，需替换 URL 中 `{WorkspaceId}` 占位符；Token Plan/Coding Plan 无需此字段 | `ws-abc123def456` |

> **注意**：部分工具（如 Cursor、Cherry Studio）要求模型名格式转换，例如 `glm-5.3` 需写为 `glm-5-3`；而 OpenClaw、Hermes Agent 等则直接使用原始 ID，不作转换 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。

## 使用方式

1. **安装客户端**：各工具依赖不同运行时（Node.js、Python、WSL 等），需按文档要求安装。例如 Hermes Agent 要求 WSL2（Windows），QwenPaw 推荐使用一键脚本自动管理 Python 环境 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。
2. **配置凭证**：
   - CLI 工具（如 Claude Code、Kilo CLI）通常编辑 `~/.xxx/config.json` 或设置环境变量（如 `ANTHROPIC_AUTH_TOKEN`）；
   - GUI 工具（如 Cursor、WorkBuddy）通过设置界面填写 `API Key` + `Base URL` + `Model ID`；
   - Web 平台（如 Dify）需安装插件并配置 API Key 与地域端点。
3. **验证连接**：发送简单请求（如 `"你好"`）确认响应正常；若报错 `401`，优先检查 Key 与 URL 是否同属一方案；若报错 `400`，检查是否遗漏 `enable_thinking` 等必需参数。

## 限制和注意事项

- **计费方案隔离**：Token Plan 个人版、Token Plan 团队版、Coding Plan 的 API Key **完全不通用**，且不可混用 Base URL。例如 Token Plan 团队版 Key 与 Coding Plan Base URL 组合将返回 `401` [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)。
- **地域绑定**：按量计费的 API Key 与 Workspace ID 必须同地域（如北京 Key 不能用于新加坡 URL），否则认证失败或产生意外费用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **协议兼容性**：WorkBuddy、Cline 等明确要求使用 OpenAI 协议（`/compatible-mode/v1/chat/completions`），不支持 Anthropic 协议；而 OpenClaw、Hermes Agent 同时支持两种协议 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)。
- **免费额度限制**：按量计费新用户免费额度仅适用于华北2（北京）地域模型，其他地域调用将立即计费 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
- **不支持场景**：Postman/cURL 仅用于测试，**禁止用于生产环境**；Dify、n8n 等工作流平台禁止使用 Token Plan/Coding Plan Key，违者可能导致订阅暂停 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


