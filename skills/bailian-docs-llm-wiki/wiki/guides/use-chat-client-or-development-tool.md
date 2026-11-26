# use chat client or development tool

阿里云百炼支持通过主流 AI 编程客户端（如 Claude Code、Qwen Code、Qoder 等）和开发工具（如 VS Code、Cursor、ZCode 等）接入，无需修改业务代码即可调用 Qwen 系列大模型。所有接入均基于 OpenAI Chat Completions 或 Anthropic Messages 兼容协议，开发者可复用现有工具链与配置习惯。[通用接入指南](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md) 提供了跨工具的统一配置范式。

## 支持的模型/功能

百炼在不同计费方案下开放的模型能力存在差异，且部分工具对协议类型有硬性要求：

- **[Token](../concepts/token.md) Plan**（个人版/团队版）：支持 `auto`（自动路由）、`qwen4-max`、`qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash` 等文本生成模型；部分工具（如 [Claude Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)）额外支持 `CLAUDE_CODE_SUBAGENT_MODEL` 用于子任务分发。
- **按量计费**：默认开放 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-max` 等主力模型；需通过 Workspace ID 构造 Base URL，模型列表以 [OpenAI 兼容接口支持的模型](../../model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md#7f9c78ae99pwz) 为准。
- **Coding Plan**：仅支持 `qwen3.7-plus`，且必须使用 `https://coding.dashscope.aliyuncs.com/v1`（OpenAI 协议）或 `/apps/anthropic`（Anthropic 协议）地址；[Codex](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/codex.md) 明确要求使用 0.93.0 或更早版本以兼容该方案。

> **注意**：[千问](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwen-office-assistant.md) 工作助理**仅支持 [Token](../concepts/token.md) Plan**，明确不支持按量计费或 Coding Plan，与其他工具的通用性描述存在冲突，应以该文档为准。

## 关键参数

所有接入方式均依赖以下核心参数，其值随计费方案动态变化：

| 参数 | [Token](../concepts/token.md) Plan | 按量计费 | Coding Plan |
|------|------------|-----------|--------------|
| `API Key` | Token Plan 专属密钥（控制台获取） | 百炼通用 API Key（控制台获取） | Coding Plan 专属密钥（控制台获取） |
| `Base URL`（OpenAI） | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://coding.dashscope.aliyuncs.com/v1` |
| `Base URL`（Anthropic） | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| `模型 ID` | `auto`, `qwen4-max`, `qwen3.8-flash` 等（见[个人版](../../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)或[团队版](../../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)支持列表） | `qwen3.8-max`, `qwen3.8-flash` 等（见[兼容性文档](../../model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md#7f9c78ae99pwz)） | `qwen3.7-plus`（见[Coding Plan 文档](../../coding-plan-guide/coding-plan.md)） |

> **注意**：[WorkBuddy](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) 明确要求自定义模型的接口地址**必须为完整 Chat Completions 路径**（如 `/v1/chat/completions`），而 [ZCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/zcode-tool-guide.md) 则强调 Base URL **不可包含 `/chat/completions`**，二者逻辑矛盾。实际配置时需严格遵循目标工具文档要求，不可套用通用规则。

## 使用方式

接入流程高度标准化，分为三步：获取凭证 → 配置连接 → 验证调用。具体操作因工具形态略有差异：

- **CLI 工具**（如 `claude`, `codex`, `qwen`, `opencode`, `kilo`, `qwenpaw`）：通常提供交互式命令（如 `claude -p "你好"`、`codex exec "你好"`、`qwen -p "你好"`），或通过环境变量（如 `ANTHROPIC_AUTH_TOKEN`）或配置文件（如 `~/.codex/config.toml`）注入参数。
- **桌面/IDE 客户端**（如 Qoder、Hermes Desktop、Trae、Cherry Studio）：通过图形化设置界面添加“自定义模型”，填写 Base URL、API Key 和模型 ID；部分工具（如 [Qoder](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qoder-agent.md)）支持在对话中直接输入 `/model` 进入模型选择器。
- **Web UI 工具**（如 DeepSeek Harness、QwenPaw Console）：在 Web 设置页中添加“自定义模型 API”提供商，指定 Provider ID、Base URL、协议类型及模型列表。
- **VS Code 插件**：通过 `Chat: Manage Language Models` 命令添加 Custom Endpoint，最终配置写入 `chatLanguageModels.json`，需手动补全 `url`、`maxInputTokens` 等字段。

所有工具均支持标准验证命令（如发送 `"你好"`），成功返回响应即表示接入完成。

## 限制和注意事项

- **协议与工具绑定**：Token Plan 和 Coding Plan 的 Anthropic 协议端点（`/apps/anthropic`）仅被 [Claude Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Hermes Agent](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 等少数工具原生支持；多数工具（如 Cursor、ZCode、VS Code）默认使用 OpenAI 协议（`/compatible-mode/v1` 或 `/v1`）。
- **地域一致性**：按量计费的 API Key 与 Base URL 必须同属一个地域（如华北2 北京），否则触发 401 错误；[WorkBuddy](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) 和 [Cherry Studio](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cherry-studio.md) 的 FAQ 均对此重点强调。
- **禁止接入场景**：Token Plan 个人版、团队版及 Coding Plan **明确禁止**用于工作流平台（Dify/n8n/Coze）、API 测试工具（Postman）或自定义后端应用等非编程辅助场景，违规可能导致订阅暂停或 API Key 封禁（见[通用接入指南](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md)）。
- **模型命名规范**：自定义模型的 `model` 参数值必须与百炼官方模型名**完全一致**（区分大小写，无额外空格或后缀），否则报错“模型不存在”；[WorkBuddy](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) 和 [VS Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/vscode-tool-guide.md) 的 FAQ 均指出此为常见错误根源。

## 来源文档

- [Claude Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Codex](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qoder](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qwen Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Hermes Agent](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [OpenCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Trae](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/trae-tool-guide.md)
- [接入 WorkBuddy](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [DeepSeek Harness](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [更多工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide.md)
- [通用接入指南](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md)
- [Cursor](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cursor.md)
- [Cline](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cline.md)
- [Kilo CLI](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/kilo-cli.md)
- [QwenPaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwenpaw.md)
- [千问](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwen-office-assistant.md)
- [VS Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/vscode-tool-guide.md)
- [ZCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/zcode-tool-guide.md)
- [Cherry Studio](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cherry-studio.md)
- [Chatbox](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/chatbox.md)


