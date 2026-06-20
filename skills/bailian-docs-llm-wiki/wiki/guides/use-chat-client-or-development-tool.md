# use chat client or development tool

阿里云百炼支持通过多种第三方聊天客户端和开发工具接入平台上的 AI 模型。这些工具涵盖终端 AI 编程助手、桌面 AI 客户端、IDE 插件和开发平台，均可通过按量计费、Coding Plan 或 Token Plan 团队版三种计费方案接入。本文汇总各工具的接入方式、配置要点和常见问题。

## 支持的工具概览

百炼支持的工具按类型可分为以下几类：

**终端 AI 编程工具**：[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)、[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)、[Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)、[Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)

**IDE 与桌面编程工具**：[Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)（AI IDE）、[Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)（VSCode 插件）、[Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)（桌面 IDE + CLI + JetBrains 插件）、[Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)

**AI 桌面客户端**：[Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)、[Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)、[QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)

**AI Agent 平台**：[OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)

**应用开发平台**：[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)

**API 测试工具**：[Postman/cURL](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)（仅适用于图像/视频生成 API 的快速测试）

## 三种计费方案

所有工具均支持以下三种计费方案，配置时需使用对应方案的 API Key 和 Base URL，三者不可混用：

| 方案 | 说明 | API Key 获取 |
|------|------|-------------|
| **Token Plan 团队版** | 按坐席订阅，按 token 消耗抵扣 Credits | [Token Plan 控制台](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview) |
| **Coding Plan** | 固定月费订阅，按模型调用次数计量 | [Coding Plan 控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan) |
| **按量计费** | 按实际调用量后付费 | [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) |

> **注意**：Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用。Dify、n8n 等工作流平台，Postman 等 API 测试工具，以及自定义应用程序不支持使用这两种套餐的 API Key，否则可能导致订阅被暂停或 API Key 被封禁。详见[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## API 协议与 Base URL

各工具根据其 API 协议使用不同的 Base URL：

### OpenAI 兼容协议

| 方案 | Base URL |
|------|----------|
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |
| 按量计费（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 按量计费（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

适用工具：Cursor、Cline、Cherry Studio、Chatbox、Codex、OpenCode、Qwen Code、Kilo CLI、Qoder、Qoder CN

### Anthropic 兼容协议

| 方案 | Base URL |
|------|----------|
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（北京） | `https://dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` |

适用工具：Claude Code、Hermes Agent、OpenClaw

## 各工具配置方式

### Claude Code

通过 `~/.claude/settings.json` 配置环境变量 `ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_BASE_URL`。还需设置 `ANTHROPIC_MODEL` 等模型环境变量。安装前需在 `~/.claude.json` 中设置 `hasCompletedOnboarding: true` 以跳过 Anthropic 官方登录验证。可使用社区工具 [CC Switch](https://github.com/farion1231/cc-switch) 在多个 API Key 或计费方案之间一键切换。

### Cursor

在 **Cursor Settings > Models** 中开启 **OpenAI API Key** 和 **Override OpenAI Base URL**，填入对应 API Key 和 Base URL。需注意 Cursor 免费版仅支持 Auto 模式，不支持调用自定义模型，需升级至 Pro 及以上套餐。部分模型名称中的点号需替换为短横线（如 `kimi-k2.6` 写为 `kimi-k2-6`）。

### Cline

在 VSCode 侧边栏选择 Cline，API Provider 选择 **OpenAI Compatible**，填入 Base URL、API Key 和 Model ID。使用 Qwen3 思考模式或 QwQ 模型时，需在 MODEL CONFIGURATION 中勾选 **Enable R1 messages format**。

### Codex

编辑 `~/.codex/config.toml` 配置 `base_url` 和 `wire_api`，并设置 `OPENAI_API_KEY` 环境变量。qwen3.7-max、qwen3.7-plus、qwen3.6-plus 和 qwen3.6-flash 支持 Responses API（最新版 Codex），其他模型需通过 Chat/Completions API 接入（需安装旧版 Codex 如 0.80.0）。

### Qwen Code

安装后输入 `/auth` 命令进行可视化配置，选择对应计费方案并输入 API Key。也可通过编辑 `~/.qwen/settings.json` 手动配置。

### Hermes Agent / OpenCode / Kilo CLI

通过编辑各自的配置文件（Hermes: `~/.hermes/config.yaml`、OpenCode: `~/.config/opencode/opencode.json`、Kilo: `~/.config/kilo/config.json`）写入 Base URL、API Key 和模型列表。

### Cherry Studio / Chatbox

在设置界面添加模型供应商，选择 OpenAI 兼容类型，填入 API Key 和 API 地址，然后添加模型 ID。

### Qoder / Qoder CN

在设置中选择提供商"阿里云百炼 - 国内"，选择计费方案和模型，填入 API Key 即可。Qoder 还提供 CLI 和 JetBrains 插件形态。Qoder CN 企业版不支持接入百炼，仅个人社区版和个人专业版支持。

### QwenPaw

在 Console 的设置 > 模型中，Token Plan 使用内置的 **Aliyun Token Plan** 提供商，Coding Plan 使用 **Aliyun Coding Plan (China)**，按量计费使用 **DashScope** 提供商。

### OpenClaw

编辑 `~/.openclaw/openclaw.json`，配置 `baseUrl`、`apiKey` 和模型列表。使用 Anthropic Messages API 协议。

### Dify

安装通义千问插件后在模型供应商中配置 API Key。DeepSeek 等模型也通过通义千问插件接入。万相等图像/视频模型需通过 Chatflow/工作流的 HTTP 节点调用。

## 百炼 CLI 集成

Cursor、Cline 和 Qoder 支持接入[百炼 CLI](https://bailian.console.aliyun.com/cli)。安装 CLI 后会自动向对应工具的 skills 目录注册能力，可通过自然语言调用百炼的图像生成、视频生成等功能。前置要求 Node.js 18+。

## 常见问题

### API Key 认证失败（401）

- 三种计费方案的 API Key 不通用，确认 API Key 和 Base URL 来自同一方案。
- 按量计费的 API Key 需与 Base URL 的地域一致。
- 确认套餐未过期，API Key 复制完整无空格。

### 模型调用报错

- Cursor 中部分模型名称与内置模型冲突，需使用别名（如将点号替换为短横线）。
- 使用 Qwen3 思考模式的工具（如 Cline）需开启 R1 messages format。
- 报错 "The value of the enable_thinking parameter is restricted to True" 时，需在客户端中开启思考模式。

### 免费额度相关

- 免费额度仅适用于华北2（北京）地域。
- 各模型的免费额度相互独立，不可跨模型共享。
- 控制台显示的免费额度数据每小时更新，可能存在延迟。

### Dify 特殊问题

- 千问插件非阿里云维护，最新版可能不稳定，可尝试安装较低版本。
- Qwen-Omni、Qwen-Audio、Qwen-OCR 模型不支持直接在 Dify 配置，需通过 HTTP 节点接入。
- Dify 云服务有应用数量限制，可考虑[私有化部署](https://www.aliyun.com/solution/tech-solution/rapidly-deploy-dify-to-accelerate-ai-application-development/)。

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
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


