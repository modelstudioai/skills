# use chat client or development tool

阿里云百炼支持通过主流 AI 编程客户端与开发工具接入，无需直接调用底层 API。所有工具均基于 OpenAI Chat Completions 或 Anthropic Messages 兼容协议，通过配置 API Key、Base URL 和模型 ID 即可快速启用。接入方式分为交互式向导（CLI/桌面端）和配置文件两种，适用于不同自动化需求。

## 支持的模型/功能

百炼提供三类计费方案对应的模型访问能力，各方案支持的模型范围严格隔离：

- **Token Plan**（个人版/团队版）：支持 `auto`、`qwen3.6-flash`、`qwen3.7-plus`、`qwen3.7-max`、`qwen3.8-flash`、`qwen3.8-max`、`qwen4-max-preview`、`qwen4-max` 等文本与多模态模型；[Token Plan 个人版支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)与[团队版支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)需分别查阅官方列表。  
- **按量计费**：支持 `qwen3.7-max`、`qwen3.8-flash`、`qwen3.8-max` 等通用大模型，具体以 [OpenAI 兼容接口支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz) 为准。  
- **Coding Plan**：仅限 `qwen3.7-plus` 及部分轻量模型，详见 [Coding Plan 支持的模型](raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)。

> **注意**：文档 19（千问）明确指出“仅支持 Token Plan，不支持按量计费或 Coding Plan”，而文档 12（通用接入指南）则声明“Token Plan 个人版、Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用”，但未排除按量计费——二者无矛盾；真正冲突的是文档 13（Cursor）中提到“免费版仅支持 Auto 模式”，而文档 4（Qwen Code）和文档 6（OpenClaw）均列出 `qwen4-max` 等非-auto 模型在 Token Plan 下可用，说明 `auto` 是 Token Plan 的默认路由机制，非限制性约束。

## 关键参数

所有工具共用以下核心参数，必须严格匹配所选计费方案：

| 参数 | Token Plan | 按量计费 | Coding Plan |
|------|------------|-----------|--------------|
| **API Key** | Token Plan 专属密钥（[个人版](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) / [团队版](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)） | 百炼通用 API Key（[控制台获取](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)） | Coding Plan 专属 API Key（[控制台获取](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)） |
| **Base URL（OpenAI）** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（需替换 `{WorkspaceId}`） | `https://coding.dashscope.aliyuncs.com/v1` |
| **Base URL（Anthropic）** | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| **模型 ID** | 必须从对应 Token Plan 支持列表选取（如 `qwen3.8-max`） | 如 `qwen3.8-max`、`qwen3.8-flash`（见[兼容模型列表](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)） | 仅 `qwen3.7-plus` 等 Coding Plan 明确支持的模型 |

> **注意**：文档 10（WorkBuddy）强调“接口地址需填写完整 Chat Completions 地址（结尾为 `/chat/completions`）”，而文档 21（ZCode）明确要求“Base URL 不追加 `/chat/completions`”。该差异源于工具实现：WorkBuddy 自动拼接路径，ZCode 则由用户传入完整 Base URL 后自行构造请求。开发者应以目标工具文档为准，不可跨工具复用配置格式。

## 使用方式

接入流程高度统一，分两类路径：

- **交互式配置（推荐初学者）**：  
  多数 CLI 工具（如 `qwen`、`opencode`、`kilo`、`hermes`）提供 `/connect` 或 `model` 命令，引导选择提供商（如 `Alibaba Token Plan (China)`）、输入 API Key、选择模型。桌面端（Qoder、Trae、WorkBuddy）和 IDE 插件（Qwen Code Companion、JetBrains 插件）通过图形化设置面板完成。  
  示例：`qwen` CLI 首次运行即提示选择 `Alibaba ModelStudio` 并自动进入地域与密钥输入流程 [Qwen Code](raw/token-plan-user-guide/use-chat-client-or-development-tool/qwen-code.md)。

- **配置文件（推荐自动化/CI）**：  
  各工具定义标准配置路径（如 Codex 用 `~/.codex/config.toml`，Hermes 用 `~/.hermes/config.yaml`），支持写入多 provider 与 model 元数据。Codex 还需额外配置 `model-catalog.local.json` 实现模型切换 [Codex](raw/token-plan-user-guide/use-chat-client-or-development-tool/codex.md)。QwenPaw 支持三种方式：CLI 命令 `qwenpaw models config`、Web Console（`http://127.0.0.1:8088/`）及 JSON 配置文件 [QwenPaw](raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwenpaw.md)。

## 限制和注意事项

- **方案隔离性**：Token Plan、按量计费、Coding Plan 的 API Key **完全不通用**。混用将导致 `401 Unauthorized`（文档 8、13、14、15、17、18、20 均强调此点）。按量计费 Key 还必须与 Base URL 地域一致（如华北2 北京的 Workspace ID 对应华北2 的 Key）。
- **工具类型限制**：Token Plan 与 Coding Plan **禁止用于工作流平台（Dify/n8n/Coze）、API 测试工具（Postman）或自定义应用后端直连**，仅限 AI 编程客户端与 OpenClaw 类 Agent [通用接入指南](raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md)。
- **模型命名规范**：部分工具（如 Cursor）对模型 ID 有字符限制，需将含小数点的 ID（如 `glm-5.3`）改写为连字符形式（`glm-5-3`）[Cursor](raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cursor.md)。
- **上下文与输出限制**：`qwen4-max` 在思考模式下最大输出为 262,144 tokens（含 thinking + final answer），非思考模式为 131,072 tokens；长输出截断时需显式设置 `CLAUDE_CODE_MAX_OUTPUT_TOKENS` [Claude Code](raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)。

## 来源文档

- [Qoder](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Codex](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/codex.md)
- [Claude Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Qwen Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Hermes Agent](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [OpenCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Trae](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/trae-tool-guide.md)
- [DeepSeek Harness](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [接入 WorkBuddy](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [更多工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide.md)
- [通用接入指南](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md)
- [Cursor](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cursor.md)
- [Cherry Studio](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cherry-studio.md)
- [Chatbox](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/chatbox.md)
- [Kilo CLI](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/kilo-cli.md)
- [Cline](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cline.md)
- [VS Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/vscode-tool-guide.md)
- [千问](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwen-office-assistant.md)
- [QwenPaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwenpaw.md)
- [ZCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/zcode-tool-guide.md)


