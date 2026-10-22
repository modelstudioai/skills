# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖 CLI、IDE 插件、Web UI 和自动化工作流等场景。开发者可根据技术栈和使用习惯，选择兼容 OpenAI 或 Anthropic 协议的客户端，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan、按量计费）配置对应凭证与端点。所有工具均需使用专属 API Key 和匹配的 Base URL，且模型名称须严格一致。

## 支持的模型/功能

百炼支持的模型能力因接入协议和计费方案而异：

- **OpenAI 兼容协议**（`/compatible-mode/v1/chat/completions`）：适用于 Cursor、WorkBuddy、Cherry Studio、Qwen Code、DeepSeek Harness、Qoder 等绝大多数客户端。支持标准 `chat/completions` 接口，可调用 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`glm-5.3`、`deepseek-v4-pro` 等文本生成模型；部分工具（如 Qwen Code、Kilo CLI）还支持 `enable_thinking` 参数开启思考模式 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)。
- **Anthropic 兼容协议**（`/apps/anthropic`）：适用于 Claude Code、Hermes Agent、OpenClaw（部分配置）等。需使用 `anthropic-messages` API 模式，支持 `auto`、`qwen3.8-max` 等模型，且 `CLAUDE_CODE_SUBAGENT_MODEL` 等专用参数仅在此协议下生效 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。
- **图像/视频生成等 AIGC API**：不通过通用聊天客户端调用，需直接使用 Postman/cURL 或 SDK 调用异步接口（如 `/api/v1/services/aigc/text2image/image-synthesis`），详见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **工作流平台（如 Dify）**：**仅支持按量计费 API Key**，不支持 [Token](../concepts/token.md) Plan 或 Coding Plan 套餐。Dify 必须使用 OpenAI 兼容端点（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），且需通过插件或 HTTP 节点集成万相、Qwen-Omni 等多模态模型 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

> **注意**：千问 APP 的“工作助理”功能**仅支持 [Token](../concepts/token.md) Plan（个人版/团队版）**，明确不支持按量计费或 Coding Plan [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `API Key` | 各计费方案专属密钥，**不可混用** | `sk-xxx`（Token Plan）、`ak-xxx`（按量计费） | Token Plan 个人版、团队版、Coding Plan 的 Key 互不通用；按量计费 Key 需与 Base URL 地域一致 |
| `Base URL` | 模型服务入口地址，协议决定路径 | OpenAI: `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic: `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 地域必须匹配（如北京地域 Key 配北京 URL）；按量计费 URL 中 `{WorkspaceId}` 需替换为真实 ID |
| `Model ID` | 请求中 `model` 字段值，区分大小写 | `qwen3.8-max`, `qwen3.7-plus` | 模型名须与百炼文档完全一致；Cursor 等工具要求 `glm-5.3` → `glm-5-3` 等格式转换 |
| `Thinking Mode` | 控制是否启用深度推理（R1 格式） | `{"enable_thinking": true}`（Qwen Code/Kilo CLI）<br>`Enable R1 messages format`（Cline 设置） | Qwen3 系列模型需显式开启；未开启将返回 400 错误 |

## 使用方式

1. **安装客户端**：根据工具要求安装 Node.js（v18+）、Python 或直接下载二进制包（如 Cursor、WorkBuddy）。例如：
   - Claude Code：`npm install -g @anthropic-ai/claude-code`
   - Qwen Code：`bash -c "$(curl -fsSL https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen.sh)" -s --source bailian`
   - Hermes Agent：`curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh \| bash`

2. **配置凭证**：统一遵循“API Key + Base URL + Model ID”三要素，但配置位置不同：
   - CLI 工具（Claude Code、Hermes、Qwen Code）：编辑 `~/.config/xxx/config.json` 或 `~/.xxx/settings.json`
   - 桌面应用（Cursor、WorkBuddy、Cherry Studio）：在 Settings > Models 页面填写表单
   - IDE 插件（Cline、Qoder JetBrains）：在插件设置界面输入
   - Web 平台（Dify）：在模型供应商卡片中配置 API Key 和端点开关

3. **验证连接**：启动工具后，发送简单请求（如“你好”）并检查响应。若失败，优先核对：
   - API Key 与 Base URL 是否来自同一计费方案和地域
   - 模型名是否拼写正确（如 `qwen3.8-max` 非 `Qwen38Max`）
   - 是否启用了必需的扩展参数（如思考模式）

## 限制和注意事项

- **计费方案适用范围严格隔离**：
  - Token Plan 个人版/团队版、Coding Plan **仅限 AI 编程工具和 OpenClaw 类 Agent**（如 Claude Code、Qwen Code、OpenClaw、Hermes）。工作流平台（Dify、n8n）、API 测试工具（Postman）、自定义脚本等**禁止使用**，否则可能被封禁 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。
  - Dify 明确要求仅使用按量计费 API Key，使用 Token Plan Key 将导致违规 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

- **协议与端点强绑定**：
  - OpenAI 兼容端点（`/compatible-mode/v1`）**必须配合 `chat/completions` 路径**（如 WorkBuddy 要求完整 URL `.../chat/completions`），而 Anthropic 端点（`/apps/anthropic`）**不支持该路径**。
  - `ANTHROPIC_BASE_URL` 在 Claude Code 中必须以 `/apps/anthropic` 结尾，若错误配置为 `/compatible-mode/v1` 将导致认证失败。

- **地域与额度约束**：
  - 按量计费免费额度**仅限华北2（北京）地域**，使用新加坡或美国端点将产生费用 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。
  - Workspace ID 必须与 API Key 所属地域完全匹配，否则返回 401 错误。

- **模型能力差异**：
  - 千问 APP 工作助理**仅支持文本生成模型**（Qwen3.8-Max 等），不支持图像/视频生成 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。
  - Cursor 免费版**仅支持 `auto` 模型**，指定 `qwen3.8-max` 等将报错“The model xxx does not work with your current plan”。

## 来源文档

- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


