# use chat client or development tool

阿里云百炼支持通过主流 AI 编程工具和开发环境接入，无需直接调用 REST API。所有客户端均基于 OpenAI Chat Completions 或 Anthropic Messages 协议兼容层接入，需按所选计费方案（[Token](../concepts/token.md) Plan / 按量计费 / Coding Plan）配置对应 API Key、Base URL 和模型 ID。配置后即可在对话、代码补全、Agent 执行等场景中使用 Qwen 系列大模型。

## 支持的模型/功能

- **通用模型支持**：所有工具均支持 `auto`（自动路由）、`qwen3.6-flash`、`qwen3.7-plus`、`qwen3.8-flash`、`qwen3.8-max`；部分工具（如 [Qoder](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qoder-agent.md)、[OpenClaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/openclaw.md)、[Claude Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)）额外支持 `qwen4-max-preview` 和 `qwen4-max`，后者上下文达 1M [Token](../concepts/token.md)，支持 reasoning 模式与高输出长度（262,144 tokens）。
- **协议支持**：
  - OpenAI 兼容协议（`/compatible-mode/v1/chat/completions` 或 `/v1/chat/completions`）：适用于绝大多数工具（如 Cursor、VS Code、Chatbox、ZCode）。
  - Anthropic 兼容协议（`/apps/anthropic/v1/messages`）：适用于 Claude Code、OpenClaw、Hermes Agent 等明确支持 Anthropic 接口的工具。
- **高级能力**：`qwen4-max`、`qwen3.8-max` 等支持 `reasoning_effort`（low/medium/high/xhigh）和 `thinking_budget` 参数；部分工具（如 Claude Code）需显式设置 `CLAUDE_CODE_MAX_OUTPUT_TOKENS` 或 `ANTHROPIC_DEFAULT_OPUS_MODEL` 以启用完整能力。

> **注意**：[千问](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwen-office-assistant.md) 工作助理**仅支持 [Token](../concepts/token.md) Plan**，不支持按量计费或 Coding Plan，与其它工具的通用接入策略不一致。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `API Key` | 方案专属密钥，不可跨方案混用 | Token Plan 个人版 Key、按量计费 Key、Coding Plan Key（三者互不通用） |
| `Base URL` | 必须与 API Key 方案及地域严格匹配 | Token Plan: `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>按量计费（北京）: `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Coding Plan: `https://coding.dashscope.aliyuncs.com/v1` |
| `Model ID` | 必须为该方案支持的模型名，区分大小写，不带额外后缀 | `qwen3.8-max`, `qwen4-max-preview`, `auto`（非所有工具均支持 `auto`） |
| `API Path` | 多数工具自动补全 `/chat/completions`；但 [WorkBuddy](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) 要求**手动填写完整路径**（如 `/compatible-mode/v1/chat/completions`），而 [ZCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/zcode-tool-guide.md) 明确要求**不得追加路径**，仅填 Base URL。 |

## 使用方式

1. **获取凭证**：根据所选计费方案，在控制台获取对应 API Key：
   - Token Plan 个人版：[创建或查看 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)
   - Token Plan 团队版：[分配坐席并获取 API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)
   - 按量计费：[百炼 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)
   - Coding Plan：[Coding Plan API Key](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)

2. **配置客户端**：
   - **图形界面工具**（Qoder、Qwen Code、Trae、WorkBuddy 等）：进入「设置 → 模型」，选择「自定义」或「添加模型」，填写 Base URL、API Key、Model ID。
   - **CLI 工具**（Claude Code、OpenClaw、Kilo CLI、QwenPaw 等）：运行交互命令（如 `claude -p "你好"`、`openclaw onboard --auth-choice qwen-token-plan-cn`）或设置环境变量（如 `ANTHROPIC_AUTH_TOKEN`, `OPENAI_API_KEY`）。
   - **IDE 插件**（VS Code、JetBrains）：通过设置向导或编辑 `chatLanguageModels.json` / `config.yaml` 配置文件。

3. **验证调用**：发送测试消息（如 `"你好"`），确认收到模型响应即成功。

## 限制和注意事项

- **工具类型限制**：Token Plan 个人版、团队版及 Coding Plan **仅限 AI 编程工具和 OpenClaw 类 Agent 使用**，明确禁止用于工作流平台（Dify/n8n/Coze）、API 测试工具（Postman）或自定义应用后端直连。违规可能导致订阅暂停或 API Key 封禁 [通用接入指南](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md)。
- **地域一致性**：按量计费的 API Key 与 Base URL **必须同地域**（如华北2 北京），否则返回 `401 Unauthorized`；Workspace ID 必须准确替换，不可留空 `{WorkspaceId}`。
- **模型可用性**：客户端显示的模型列表可能多于套餐实际支持范围，务必以各方案官方支持列表为准（如 [Token Plan 个人版模型列表](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)、[Coding Plan 支持的模型](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)）。
- **协议与路径差异**：[WorkBuddy](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) 要求接口地址必须为完整 Chat Completions 路径（含 `/chat/completions`），而 [ZCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/zcode-tool-guide.md) 明确禁止添加路径，仅接受 Base URL —— 此处存在明显设计冲突，开发者需严格按目标工具文档操作。

## 来源文档

- [Qoder](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Claude Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenClaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Codex](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Hermes Agent](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Trae](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/trae-tool-guide.md)
- [DeepSeek Harness](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [接入 WorkBuddy](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [通用接入指南](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md)
- [更多工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide.md)
- [Cherry Studio](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cherry-studio.md)
- [Cline](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cline.md)
- [Cursor](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cursor.md)
- [Chatbox](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/chatbox.md)
- [千问](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwen-office-assistant.md)
- [Kilo CLI](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/kilo-cli.md)
- [QwenPaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwenpaw.md)
- [VS Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/vscode-tool-guide.md)
- [ZCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/zcode-tool-guide.md)


