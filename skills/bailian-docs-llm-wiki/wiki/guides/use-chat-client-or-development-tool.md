# use chat client or development tool

阿里云百炼支持通过多种第三方聊天客户端和开发工具接入模型服务。这些工具覆盖终端 AI 编程助手、桌面客户端、IDE 插件和开发平台等类型，均通过兼容 OpenAI 或 Anthropic API 协议实现接入。用户根据自身计费方案配置对应的 API Key 和 Base URL 即可使用。

## 支持的工具分类

### 终端 AI 编程工具

适合习惯命令行操作的开发者，包括：

- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) — Anthropic 推出的命令行 AI 编程助手，通过 `~/.claude/settings.json` 配置环境变量接入
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) — OpenAI 推出的终端编程助手，通过 `~/.codex/config.toml` 配置
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) — 通过 `hermes config set` 命令或 `~/.hermes/config.yaml` 配置
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md) — 通过 `~/.config/opencode/opencode.json` 配置
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) — 支持 `/auth` 可视化配置或 `~/.qwen/settings.json` 手动配置
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) — 通过 `~/.config/kilo/config.json` 配置
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) — 开源个人 AI 助手平台，通过 `~/.openclaw/openclaw.json` 配置
- Qoder CLI — Qoder 的命令行版本，通过 `/model` 命令配置

### IDE 插件与桌面 IDE

适合需要在编辑器中直接使用 AI 的开发者：

- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) — AI 编程 IDE，在 Settings > Models 中配置 OpenAI API Key 和 Base URL
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) — VSCode 插件，选择 OpenAI Compatible 作为 API Provider
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) — 支持桌面 IDE、CLI 和 JetBrains 插件，内置阿里云百炼提供商
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) — 阿里云智能编码助手，内置百炼提供商选项

### 桌面聊天客户端

适合非编程场景的对话交互：

- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) — 开源 AI 桌面客户端，提供商类型选择 OpenAI
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md) — 跨平台 AI 客户端，API 模式选择 OpenAI API 兼容
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) — AgentScope 团队开源的个人 AI 助手，提供 Web Console 配置界面

### 开发平台与 API 测试

- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) — 开源大模型应用开发平台，通过安装通义千问插件接入
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) — 适用于图像/视频异步 API 的快速测试

## 计费方案与接入地址

所有工具均支持以下三种计费方案，每种方案使用独立的 API Key 和 Base URL：

| 计费方案 | OpenAI 兼容 Base URL | Anthropic 兼容 Base URL |
|---------|---------------------|------------------------|
| [Token](../concepts/token.md) Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` |
| 按量计费（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | — |

> **注意**：三种计费方案的 API Key 互不通用。[Token](../concepts/token.md) Plan 团队版和 Coding Plan 的 API Key 分别在各自管理页面获取，按量计费使用百炼标准 API Key。混用会导致 401 认证错误。

## 常用模型

各工具可通过配置使用以下模型（具体可用模型取决于所选计费方案）：

- **Qwen 系列**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash
- **DeepSeek 系列**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2
- **Kimi 系列**：kimi-k2.7-code、kimi-k2.6、kimi-k2.5
- **GLM 系列**：glm-5.2、glm-5.1、glm-5
- **其他**：MiniMax-M2.5

> **注意**：在 Cursor 中部分模型名称需要调整，例如 kimi-k2.6 需写为 kimi-k2-6，glm-5.2 需写为 glm-5-2，glm-5 需写为 glm-5-0。这是因为 Cursor 内置模型名可能产生冲突。

## 配置要点

### API 协议选择

- 使用 Anthropic 协议的工具：Claude Code、Hermes Agent、OpenClaw、Kilo CLI（Coding Plan 模式）
- 使用 OpenAI 兼容协议的工具：Cursor、Cline、Cherry Studio、Chatbox、Codex、OpenCode、Qwen Code、Qoder、Qoder CN、QwenPaw

### 思考模式

部分模型（如 Qwen3 系列、QwQ）支持思考模式。不同工具启用方式不同：

- OpenCode / Kilo CLI：在 JSON 配置中设置 `"thinking": {"type": "enabled", "budgetTokens": 8192}`
- Qwen Code：通过 `"extra_body": {"enable_thinking": true}` 开启
- Cline：在 MODEL CONFIGURATION 中勾选 Enable R1 messages format
- Codex（Responses API）：qwen3.7-max 等模型支持最新版 Codex 的 Responses API

### Codex 版本兼容性

Codex 分为两种 API 模式：

- **Responses API**（最新版）：仅 qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 支持
- **Chat/Completions API**：需安装旧版 Codex（如 `npm install -g @openai/codex@0.80.0`），其他模型使用此模式

> **注意**：Coding Plan 仅支持 Chat/Completions API，需使用旧版 Codex。

## 使用限制

- **Cursor 免费版**不支持调用自定义模型，需升级至 Pro 及以上套餐
- **[Token](../concepts/token.md) Plan 团队版和 Coding Plan** 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，不支持接入工作流平台（如 Dify、n8n）、API 测试工具（如 Postman）或自定义应用程序
- **按量计费**的免费额度仅适用于华北2（北京）地域，且各模型额度独立计算
- Qoder CN 企业版不支持接入百炼，需使用个人社区版或个人专业版

## 百炼 CLI 集成

部分工具（Cursor、Cline、Qoder）支持通过安装百炼 CLI（`npm install -g bailian-cli`）注册 Skill，使 AI 工具可调用百炼的图像生成、视频生成等扩展能力。安装后工具可通过自然语言指令调用，如生成电商主图或产品演示视频。

## 常见错误排查

| 错误 | 可能原因 | 解决方案 |
|------|---------|---------|
| 401 Incorrect API key | API Key 与 Base URL 不匹配或地域不一致 | 确认 API Key 和 Base URL 来自同一计费方案和地域 |
| The model xxx does not work with your current plan | Cursor 免费版限制 | 升级至 Cursor Pro |
| InternalError.Algo.InvalidParameter | 思考模式未正确启用 | 在工具中启用对应的思考模式选项 |
| enable_thinking parameter restricted to True | 模型要求思考模式 | 在客户端中开启思考模式 |
| 上下文超限 | 长对话或工具调用累积 token 过多 | 在模型配置中调整 max_tokens 参数 |

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


