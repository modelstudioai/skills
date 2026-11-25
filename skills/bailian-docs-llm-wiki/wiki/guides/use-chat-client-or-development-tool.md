# use chat client or development tool

阿里云百炼支持通过主流 AI 编程客户端（如 Qoder、Claude Code、Codex 等）和开发工具（如 VS Code、Cursor、ZCode 等）接入模型服务。所有接入均基于 OpenAI 兼容协议或 Anthropic 兼容协议，无需修改应用逻辑，仅需配置 API Key、Base URL 和模型 ID 即可快速启用。

## 支持的模型/功能

百炼提供三类计费方案对应的模型访问能力，**模型可用性严格受限于所选方案**：

- **[Token](../concepts/token.md) Plan（个人版/团队版）**：支持 `auto`、`qwen4-max`、`qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash` 等文本生成模型；部分模型支持图像输入（如 `qwen4-max`、`qwen3.8-max`），详见 [Token Plan 个人版支持的模型](../../token-plan-personal/token-plan-personal-overview.md#tppo-h-models) 和 [Token Plan 团队版支持的模型](../../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)。  
- **按量计费（Model Studio）**：支持 `qwen3.7-max`、`qwen3.8-max`、`qwen3.8-flash`、`qwen4-max` 等最新发布模型，上下文长度最高达 1M [Token](../concepts/token.md)；需使用 Workspace ID 构造 Base URL，具体参见 [Regions 文档](../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。  
- **Coding Plan**：仅支持 `qwen3.7-plus` 及其等效别名，专为代码场景优化；要求使用 Codex 0.93.0 或更早版本（[Codex 配置文档](raw/token-plan-user-guide/use-chat-client-or-development-tool/codex.md) 中明确说明）。

> **注意**：多个文档对 Coding Plan 的模型支持范围存在不一致表述。[QwenPaw 文档](raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwenpaw.md) 列出 `qwen3.7-plus` 为唯一支持模型，而 [Claude Code 文档](raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md) 在 Coding Plan 示例中也仅使用 `qwen3.7-plus`；但 [WorkBuddy 文档](raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) 表格中错误地将 `qwen3.7-plus` 写为 `qwen3.7-plus`（拼写正确），而 [Cherry Studio 文档](raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cherry-studio.md) 同样仅列出该模型。综合判断，Coding Plan 当前仅支持 `qwen3.7-plus`，其他模型名属过时或误写。

## 关键参数

所有客户端接入均依赖以下核心参数，必须严格匹配所选计费方案：

| 参数 | [Token](../concepts/token.md) Plan | 按量计费 | Coding Plan |
|------|------------|-----------|--------------|
| **API Key** | 专属 Token Plan API Key（[个人版](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) / [团队版](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list)） | 百炼通用 API Key（[控制台获取](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key?spm=5176.28197581.0.0.307f29a4lC7Vbh)） | 专属 Coding Plan API Key（[控制台获取](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)） |
| **Base URL（OpenAI）** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（需替换 `{WorkspaceId}`） | `https://coding.dashscope.aliyuncs.com/v1` |
| **Base URL（Anthropic）** | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| **API 路径** | 多数工具自动补全 `/chat/completions`；但 WorkBuddy 明确要求填写完整路径（如 `.../v1/chat/completions`）[接入 WorkBuddy](raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) | 同上，需与 Base URL 地域一致 | 同上 |

此外，部分工具（如 Claude Code）需额外设置 `CLAUDE_CODE_MAX_CONTEXT_TOKENS` 或 `CLAUDE_CODE_MAX_OUTPUT_TOKENS`；Qwen Code 支持 `reasoning_effort` 和 `thinking_budget` 控制推理深度，详见 [Claude Code 文档](raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)。

## 使用方式

接入流程高度统一，分为四步：**获取 Key → 配置 URL 与模型 → 保存/启用 → 验证调用**。各工具差异主要体现在配置入口：

- **图形界面工具（Qoder 桌面端、Trae、WorkBuddy、ZCode）**：通过「设置 → 模型 → 添加自定义模型」完成，需手动填写 Base URL、API Key 和模型 ID。  
- **CLI 工具（Qwen Code、Kilo CLI、OpenCode、Hermes Agent）**：运行交互式命令（如 `qwen`、`kilo`、`opencode`），按提示选择方案并粘贴 Key。  
- **IDE 插件（Qwen Code Companion、VS Code）**：在 IDE 设置中启用「Custom Endpoint」，通过向导或 JSON 文件（如 `chatLanguageModels.json`）配置。  
- **配置文件方式（Codex、OpenClaw、Hermes、QwenPaw）**：编辑指定路径的 TOML/JSON/YAML 文件（如 `~/.codex/config.toml`），直接写入 provider 和模型元数据。  

所有工具均支持多模型切换，推荐首次配置后运行简单测试命令（如 `qwen -p "你好"` 或 `opencode run "你好"`）验证连通性。

## 限制和注意事项

- **方案隔离性**：Token Plan、按量计费、Coding Plan 的 API Key **完全不通用**。混用会导致 `401 Unauthorized` 错误，[WorkBuddy 文档](raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) 和 [Cherry Studio 文档](raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cherry-studio.md) 均强调此点。  
- **地域一致性**：按量计费的 API Key 与 Base URL 必须同属一个地域（当前仅支持华北2 北京），否则调用失败。[WorkBuddy 常见问题](raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) 明确指出“API Key 也必须来自华北2（北京）”。  
- **工具类型限制**：Token Plan 个人版/团队版及 Coding Plan **仅限 AI 编程工具和 OpenClaw 类 Agent 使用**，禁止用于 Dify、n8n、Postman 等工作流平台或 API 测试工具，违者可能导致订阅暂停 [通用接入指南](raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md)。  
- **协议兼容性**：WorkBuddy 明确声明“仅支持 OpenAI 兼容的 Chat Completions 协议，不支持 Responses API 与 Anthropic 协议” [接入 WorkBuddy](raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md)，而 ZCode 和 Claude Code 则明确支持 Anthropic 协议。开发者需根据目标工具能力选择 Base URL 类型。  
- **模型命名规范**：模型 ID 必须与百炼官方模型名**完全一致（区分大小写，无额外空格或后缀）**，否则报错“模型不存在”，[WorkBuddy 常见问题](raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md) 和 [Trae 常见问题](raw/token-plan-user-guide/use-chat-client-or-development-tool/trae-tool-guide.md) 均有警示。

## 来源文档

- [Qoder](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Claude Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Codex](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [OpenClaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Trae](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/trae-tool-guide.md)
- [DeepSeek Harness](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [接入 WorkBuddy](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [通用接入指南](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/more-tools.md)
- [更多工具](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide.md)
- [Cherry Studio](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cherry-studio.md)
- [Cursor](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cursor.md)
- [Chatbox](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/chatbox.md)
- [Cline](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/cline.md)
- [Kilo CLI](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/kilo-cli.md)
- [QwenPaw](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwenpaw.md)
- [千问](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/qwen-office-assistant.md)
- [VS Code](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/vscode-tool-guide.md)
- [ZCode](../../raw/token-plan-user-guide/use-chat-client-or-development-tool/more-tools-guide/zcode-tool-guide.md)


