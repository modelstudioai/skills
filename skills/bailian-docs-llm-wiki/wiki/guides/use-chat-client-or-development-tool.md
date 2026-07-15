# use chat client or development tool

阿里云百炼支持将平台上的模型接入各类第三方 AI 聊天客户端、编程工具与应用开发平台。这些工具本身不由百炼提供，接入方式统一为「填入 Base URL + API Key + 模型 ID」，通过 **OpenAI 兼容协议**或 **Anthropic 兼容协议**访问百炼网关。本文汇总不同工具的接入要点、共用的凭证规则以及常见限制。

## 支持的工具类型

按形态大致分为三类：

- **终端 / CLI 编程工具**：[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)、[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)、[Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)、[Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)、Qoder CLI。
- **IDE / 编辑器插件**：[Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)、[Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)（VSCode）、Qoder（IDE / JetBrains 插件）、Qoder CN（原 Lingma）。
- **桌面 / 跨平台聊天客户端与助手**：[Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)、[Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)、[OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)、QwenPaw。
- **应用开发 / 工作流平台**：[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

此外，任何兼容 OpenAI / Anthropic 协议且支持自定义服务端点的工具（如 Trae）都可参照[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)接入。若只想快速验证图像/视频生成 API，可用 [Postman 或 cURL](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 直接调用。

## 三种计费方案与凭证

绝大多数工具的接入差异只在「Base URL 属于哪个方案」。百炼提供三种计费方案，各自有独立的 API Key，**互不通用**：

| 方案 | 说明 | OpenAI 兼容 Base URL | Anthropic 兼容 Base URL |
| --- | --- | --- | --- |
| Token Plan 团队版 | 按坐席订阅，按 token 消耗抵扣 Credits | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | 固定月费订阅，按模型调用次数计量 | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（华北2·北京） | 按实际调用量后付费 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/apps/anthropic` |

按量计费还支持多地域，需保证 API Key 与 Base URL 地域一致：

- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`（`WorkspaceId` 替换为真实值）
- 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`

> **注意**：OpenAI 协议的 Base URL 以 `/compatible-mode/v1`（或 `/v1`）结尾，Anthropic 协议以 `/apps/anthropic` 结尾。部分工具（如 OpenCode、Kilo CLI）要求在 Anthropic 端点后再追加 `/v1`。以各工具原文为准。

## 协议选择与配置形态

不同工具选用的协议和配置载体各异：

- **Anthropic 协议**：[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 通过 `~/.claude/settings.json` 的 `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` 环境变量配置；[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 默认使用 Anthropic 协议（`api_mode: anthropic_messages`），也可切到 OpenAI 协议。
- **OpenAI 协议**：[Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)、[Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)、Cherry Studio、Chatbox 等在 GUI 中选择「OpenAI Compatible / 兼容」并填入 Base URL、API Key、模型 ID。
- **配置文件**：Hermes（`~/.hermes/config.yaml`）、OpenCode（`~/.config/opencode/opencode.json`）、Kilo CLI（`~/.config/kilo/config.json`）、Qwen Code（`~/.qwen/settings.json`）、Codex（`~/.codex/config.toml` + `OPENAI_API_KEY` 环境变量）。
- **原生下拉选择**：Qoder / Qoder CN 在设置中选择「阿里云百炼 - 国内」提供商 + 计费方案「类型」，仅需填 API Key。

## 关键参数与注意事项

- **思考模式**：许多模型（如 Qwen3 思考模式、QwQ）需显式开启思考。OpenCode / Kilo CLI 用 `thinking.budgetTokens`，Qwen Code 用 `extra_body.enable_thinking: true`，Cline 需勾选 **Enable R1 messages format**。若报错 `enable_thinking parameter is restricted to True`，说明该模型仅支持思考模式运行，需在客户端开启。
- **模型名称别名**：[Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) 因内置模型名冲突，需改写模型名，如 `kimi-k2.6` → `kimi-k2-6`、`glm-5` → `glm-5-0`。其他工具一般直接使用原始模型 ID。
- **上下文窗口**：Claude Code 默认 200K，可通过 `CLAUDE_CODE_MAX_CONTEXT_TOKENS=1000000` 或模型名后缀 `[1m]` 扩展到 1M（需模型支持）。
- **Codex 版本差异**：仅 qwen3.7-max/plus、qwen3.6-plus/flash 支持 Responses API（可用最新版 Codex）；其他模型需用 Chat/Completions API，须安装旧版本（如 `@openai/codex@0.80.0`）。
- **401 认证失败**：几乎都是「API Key 与 Base URL 不属于同一方案」或「按量计费 Key 与地域不匹配」，逐项核对即可。

## 套餐使用范围限制

> **注意**：Token Plan 团队版与 Coding Plan **仅限**在 AI 编程工具和 OpenClaw 类 Agent 中使用。以下类型不支持接入，误用可能导致订阅暂停或 API Key 被封禁（详见[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)）：
>
> - 工作流/自动化平台：如 Dify、n8n、Coze 等；
> - API 测试工具：如 Postman、Insomnia 等；
> - 自定义应用程序：脚本或后端代码中直接调用 API。

因此 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 这类应用开发平台只能通过**按量计费**（`get-api-key` 获取的 API Key）接入，且在 Dify 中通过安装「通义千问」或「OpenAI-API-compatible」插件配置。免费额度仅适用于华北2（北京）地域，且各模型额度独立、不可跨模型共享。

## 快速验证

配置完成后统一用一句问候验证连通性，例如：`claude "你好"`、`hermes chat -q "你好"`，或在 GUI 客户端对话框发送「你好」。模型正常返回响应即表示接入成功。若为 RAM 子账号，需确保在业务空间中已获得目标模型的调用权限。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


