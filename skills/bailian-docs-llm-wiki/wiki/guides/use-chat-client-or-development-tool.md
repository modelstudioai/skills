# use chat client or development tool

阿里云百炼支持通过多种第三方 AI 聊天客户端和编程工具接入模型服务。开发者可以根据使用场景选择终端 CLI 工具、桌面客户端、IDE 插件或低代码平台，通过 OpenAI 兼容或 Anthropic 兼容 API 协议快速接入百炼提供的 Qwen、DeepSeek、Kimi、GLM 等模型。百炼提供三种计费方案：按量计费、Coding Plan 和 Token Plan 团队版，各工具的配置方式大同小异，核心都是填入对应方案的 API Key 和 Base URL。

## 支持的工具分类

### 终端 AI 编程工具

| 工具 | 安装方式 | 配置方式 | 详情 |
|------|---------|---------|------|
| [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) | `npm install -g @anthropic-ai/claude-code` | `~/.claude/settings.json` 环境变量 | Anthropic 协议 |
| [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) | `npm install -g @openai/codex` | `~/.codex/config.toml` + 环境变量 | OpenAI 协议 |
| [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) | curl 安装脚本 | `hermes config set` 或 `~/.hermes/config.yaml` | Anthropic 协议 |
| [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md) | `npm install -g opencode-ai` | `~/.config/opencode/opencode.json` | Anthropic 协议 |
| [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) | 官方安装脚本 | `/auth` 命令或 `~/.qwen/settings.json` | OpenAI 协议 |
| [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) | `npm install -g @kilocode/cli` | `~/.config/kilo/config.json` | OpenAI 协议 |
| [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) | `npm install -g openclaw@latest` | `~/.openclaw/openclaw.json` | Anthropic 协议 |

### 桌面客户端与 AI 助手

| 工具 | 类型 | 配置方式 | 详情 |
|------|------|---------|------|
| [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) | 桌面 AI 客户端 | GUI 设置 > 模型 > 添加 | OpenAI 协议 |
| [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md) | 跨平台 AI 客户端 | 设置 > 模型提供方 > 添加 | OpenAI 协议 |
| [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) | 个人 AI 助手（Web） | Console 设置 > 模型 | OpenAI 协议 |

### IDE 插件与编程 IDE

| 工具 | 支持 IDE | 详情 |
|------|---------|------|
| [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) | 独立 IDE | Cursor Settings > Models |
| [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) | VSCode 插件 | OpenAI Compatible Provider |
| [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) | 独立 IDE / CLI / JetBrains 插件 | GUI 选择阿里云百炼提供商 |
| [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) | 独立 IDE | GUI 选择阿里云百炼提供商 |

### 低代码平台与 API 测试

| 工具 | 说明 | 详情 |
|------|------|------|
| [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) | 开源大模型应用开发平台 | 安装通义千问插件配置 |
| [Postman / cURL](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) | HTTP 测试工具 | 适用于图像/视频生成 API 的异步调用测试 |

## 三种计费方案的接入参数

所有工具的配置核心是选择计费方案并填入对应的 API Key 和 Base URL。

### Token Plan 团队版

按坐席订阅，按 token 消耗抵扣 Credits。

| API 协议 | Base URL |
|---------|---------|
| OpenAI | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

API Key 在 [Token Plan 团队版控制台](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview) 获取。可用模型参见 [Token Plan 支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)。

### Coding Plan

固定月费订阅，按模型调用次数计量。

| API 协议 | Base URL |
|---------|---------|
| OpenAI | `https://coding.dashscope.aliyuncs.com/v1` |
| Anthropic | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

API Key 在 [Coding Plan 控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan) 获取。可用模型参见 [Coding Plan 支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)。

### 按量计费

按实际调用量后付费，支持多个地域。

| API 协议 | 华北2（北京） | 新加坡 | 美国（弗吉尼亚） |
|---------|-------------|-------|----------------|
| OpenAI | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| Anthropic | `https://dashscope.aliyuncs.com/apps/anthropic` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` | - |

API Key 通过 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 创建，需与所选地域对应。可用模型参见 [OpenAI 兼容模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz)。

> **注意**：三种计费方案的 API Key 互不通用，Base URL 也不同。混用会导致认证失败（HTTP 401）。

## 配置要点

### API 协议选择

- 使用 **Anthropic 协议**的工具：Claude Code、Hermes Agent、OpenCode、OpenClaw。这些工具的 Base URL 路径通常包含 `/apps/anthropic`。
- 使用 **OpenAI 兼容协议**的工具：Cursor、Codex、Cline、Cherry Studio、Chatbox、Qwen Code、Kilo CLI、QwenPaw 等。Base URL 路径通常包含 `/compatible-mode/v1`。
- Qoder 和 Qoder CN 通过内置提供商下拉菜单选择百炼，无需手动填写 Base URL。

### 模型名称注意事项

部分工具对模型名称有特殊要求。例如在 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) 中，`kimi-k2.6` 需写为 `kimi-k2-6`，`glm-5.1` 需写为 `glm-5-1`，`glm-5` 需写为 `glm-5-0`，以避免与内置模型名冲突。

### 思考模式配置

使用 Qwen3 系列（思考模式）或 QwQ 模型时，部分工具需要额外开启思考模式：
- Cline：在 MODEL CONFIGURATION 中勾选 **Enable R1 messages format**
- Cherry Studio：在客户端中开启思考模式
- OpenCode / Kilo CLI：在配置文件中设置 `thinking.type: "enabled"` 和 `budgetTokens`

### Codex 的 API 版本差异

[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) 支持两种 API 模式：qwen3.7-max/plus 等模型支持最新版 Codex 的 Responses API（`wire_api = "responses"`），其他模型需安装旧版 Codex（如 0.80.0）并使用 Chat/Completions API（`wire_api = "chat"`）。

## 百炼 CLI 集成

支持百炼 CLI Skill 的工具（如 Cursor、Cline、Qoder）可在安装 [百炼 CLI](https://bailian.console.aliyun.com/cli) 后，通过自然语言调用图像生成、视频生成等多模态能力。安装命令：`npm install -g bailian-cli`。详见各工具原文中的"使用案例：接入百炼 CLI"章节。

## 使用限制

根据 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 说明，Token Plan 团队版和 Coding Plan **仅限**在 AI 编程工具和 OpenClaw 类型 Agent 中使用。以下类型不支持接入：工作流/自动化平台（如 Dify、n8n、Coze）、API 测试工具（如 Postman）、自定义应用程序。违规使用可能导致订阅暂停或 API Key 封禁。

> **注意**：按量计费方案不受上述限制，可用于 Dify、Postman 等平台。

## 常见问题

- **HTTP 401 / API Key 认证失败**：确认 API Key 与 Base URL 来自同一计费方案，且按量计费的 API Key 与 Base URL 地域一致。
- **Cursor 免费版无法调用自定义模型**：Cursor 免费版仅支持 Auto 模式，需升级至 Pro 及以上。
- **Hermes Agent 仍连接 OpenRouter**：需将 `model.provider` 设为 `custom`。
- **报错 400 InternalError.Algo.InvalidParameter**（Cline）：需勾选 Enable R1 messages format。
- **免费额度用完却显示仍有余量**：控制台数据每小时更新，存在延迟。免费额度仅适用于华北2（北京）地域，各模型额度独立。
- 更多错误码排查：[按量计费](https://help.aliyun.com/zh/model-studio/error-code)、[Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan-faq)、[Token Plan](https://help.aliyun.com/zh/model-studio/token-plan-faq)。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
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



