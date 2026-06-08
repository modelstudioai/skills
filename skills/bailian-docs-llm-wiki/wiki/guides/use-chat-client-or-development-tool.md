# use chat client or development tool

阿里云百炼平台兼容 OpenAI 和 Anthropic API 协议，支持通过多种第三方聊天客户端和开发工具接入。开发者可根据使用场景选择终端 CLI 工具、桌面客户端、IDE 插件或开发平台，并通过 Token Plan 团队版、Coding Plan 或按量计费三种方案完成接入。本文汇总各工具的接入方式、配置要点和常见问题。

## 支持的工具分类

### 终端 CLI 工具

| 工具 | 安装方式 | 配置文件 | 协议 |
| --- | --- | --- | --- |
| [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) | `npm install -g @anthropic-ai/claude-code` | `~/.claude/settings.json` | Anthropic |
| [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) | `npm install -g @openai/codex` | `~/.codex/config.toml` + 环境变量 | OpenAI |
| [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md) | `npm install -g opencode-ai` | `~/.config/opencode/opencode.json` | Anthropic |
| [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) | `npm install -g @kilocode/cli` | `~/.config/kilo/config.json` | OpenAI Compatible |
| [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) | 安装脚本（需 Python、Git） | `~/.hermes/config.yaml` | Anthropic |
| [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) | 官方安装脚本 | `~/.qwen/settings.json` 或 `/auth` 命令 | OpenAI |
| [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) | `npm install -g openclaw@latest` | `~/.openclaw/openclaw.json` | Anthropic |
| Qoder CLI | `curl -fsSL https://qoder.com/install \| bash` | `/model` 命令交互配置 | OpenAI Compatible |

### 桌面客户端与 IDE 插件

| 工具 | 类型 | 协议 |
| --- | --- | --- |
| [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) | AI 编程 IDE | OpenAI |
| [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) | 桌面 AI 客户端 | OpenAI |
| [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md) | 跨平台 AI 客户端 | OpenAI Compatible |
| [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) | VSCode 插件 | OpenAI Compatible |
| [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) | 独立 IDE | OpenAI Compatible |
| [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) | IDE + CLI + JetBrains 插件 | OpenAI Compatible |

### 开发平台与 API 测试

| 工具 | 说明 |
| --- | --- |
| [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) | 开源大模型应用开发平台，通过通义千问插件接入 |
| [Postman/cURL](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) | 用于快速测试图像/视频生成等异步 API |

## 三种计费方案的 Base URL

所有工具接入时均需根据计费方案选择对应的 Base URL 和 API Key：

### Token Plan 团队版

| 协议 | Base URL |
| --- | --- |
| OpenAI | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

API Key 获取：[Token Plan 团队版控制台](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)

### Coding Plan

| 协议 | Base URL |
| --- | --- |
| OpenAI | `https://coding.dashscope.aliyuncs.com/v1` |
| Anthropic | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

API Key 获取：[Coding Plan 控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan)

### 按量计费

| 协议 | Base URL（华北2 北京） |
| --- | --- |
| OpenAI | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Anthropic | `https://dashscope.aliyuncs.com/apps/anthropic` |

其他地域：新加坡需替换为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`，美国（弗吉尼亚）使用 `https://dashscope-us.aliyuncs.com/...`。

API Key 获取：[百炼 API Key 管理](https://help.aliyun.com/zh/model-studio/get-api-key)

## 关键配置要点

### 模型名称注意事项

部分工具中模型名称需使用别名。例如在 Cursor 中：kimi-k2.6 需写为 `kimi-k2-6`，glm-5.1 写为 `glm-5-1`，glm-5 写为 `glm-5-0`。具体别名规则请参考各工具文档。

### 思考模式配置

- Qwen3 系列和部分模型支持思考模式（thinking/reasoning）
- 在 Cline 中使用 Qwen3 思考模式需勾选 **Enable R1 messages format**
- OpenCode 和 Kilo CLI 通过 `thinking.budgetTokens` 参数控制思考 token 预算
- Codex 中 qwen3.7-max/plus 等支持 Responses API（`wire_api = "responses"`），其他模型需使用 Chat/Completions API 并安装旧版 Codex（如 0.80.0）

### Claude Code 特殊配置

Claude Code 通过环境变量配置，需在 `~/.claude/settings.json` 中设置 `ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_BASE_URL`。首次使用需在 `~/.claude.json` 中设置 `"hasCompletedOnboarding": true` 跳过 Anthropic 登录验证。

### Hermes Agent 注意事项

Hermes Agent 默认使用 OpenRouter 作为推理提供商，接入百炼时必须将 `model.provider` 设置为 `custom`，否则请求不会发往百炼。

## 百炼 CLI 集成

部分工具（Cursor、Cline、Qoder）支持通过百炼 CLI 扩展能力。安装 `npm install -g bailian-cli` 后，CLI 会自动向对应工具的 skills 目录注册 Skill，实现图像生成、视频生成等多模态能力的自然语言调用。

## 限制和注意事项

> **注意**：Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用。工作流/自动化平台（如 Dify、n8n、Coze）、API 测试工具（如 Postman）和自定义应用程序不支持使用套餐 API Key，违规使用可能导致订阅暂停或 API Key 封禁。按量计费无此限制。详见[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

> **注意**：Cursor 免费版仅支持 Auto 模式，无法调用自定义模型，需升级至 Cursor Pro 及以上套餐。

> **注意**：Qoder CN（原 Lingma）企业版不支持接入百炼，仅个人社区版和个人专业版可用。

- 三种计费方案的 API Key 互不通用，Base URL 也不同，混用会导致 401 错误
- 按量计费的 API Key 必须与 Base URL 的地域对应
- 图像/视频生成 API 采用异步调用机制，需先创建任务获取 task_id，再轮询查询结果
- Dify 中使用百炼需安装通义千问插件，DeepSeek 等模型也通过该插件接入

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


