# use chat client or development tool

阿里云百炼平台兼容 OpenAI 和 Anthropic API 协议，支持通过多种第三方聊天客户端和开发工具接入模型服务。开发者可根据使用场景选择终端 CLI 工具、桌面客户端、IDE 插件或开发平台，配合按量计费、Coding Plan 或 [Token](../concepts/token.md) Plan 团队版三种计费方案完成接入。本文汇总了各类工具的接入方式、配置要点和常见问题。

## 支持的工具概览

百炼支持的工具按使用形态可分为以下几类：

| 类型 | 工具 | 简介 |
|------|------|------|
| 终端 CLI | [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)、[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)、[Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)、[Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)、[OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) | 命令行 AI 编程助手，直接在终端中交互 |
| 桌面客户端 | [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)、[Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)、[QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) | GUI 聊天界面，适合日常对话和多模型管理 |
| IDE 插件/编辑器 | [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)、[Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)、[Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)、[Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) | 集成到 IDE 中的 AI 编程辅助 |
| 开发平台 | [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) | 大模型应用开发平台，支持工作流和知识库 |
| API 测试工具 | [Postman/cURL](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) | 快速验证 API 调用（仅适用于按量计费） |

## 三种计费方案

所有工具均支持以下三种计费方案，但各方案的 [API Key](../concepts/api-key.md) 和 Base URL 互不通用：

- **[Token](../concepts/token.md) Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。[API Key](../concepts/api-key.md) 在 [Token Plan 管理页面](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list) 获取。
- **Coding Plan**：固定月费订阅，按模型调用次数计量。[API Key](../concepts/api-key.md) 在 [Coding Plan 页面](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan) 获取。
- **按量计费**：按实际调用量后付费。API Key 通过 [百炼控制台](https://help.aliyun.com/zh/model-studio/get-api-key) 获取。

> **注意**：[Token](../concepts/token.md) Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用。Dify、Postman 等工作流/自动化平台和 API 测试工具不支持使用这两种套餐的 API Key，违规使用可能导致订阅被暂停。详见 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## API 协议与 Base URL

百炼提供两种 API 协议，不同工具使用不同协议：

### OpenAI 兼容协议

大部分工具使用此协议（Cursor、Cline、Cherry Studio、Chatbox、Codex、OpenCode、Kilo CLI、Qwen Code、Qoder/Qoder CN 等）。

| 计费方案 | Base URL |
|----------|----------|
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |
| 按量计费（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 按量计费（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

### Anthropic 兼容协议

Claude Code、Hermes Agent、OpenClaw 等使用此协议。

| 计费方案 | Base URL |
|----------|----------|
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（北京） | `https://dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` |

> **注意**：按量计费的 API Key 必须与所选地域对应，跨地域使用会导致认证失败（HTTP 401）。

## 各工具配置要点

### Claude Code

通过环境变量配置，编辑 `~/.claude/settings.json`，设置 `ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL`、`ANTHROPIC_MODEL` 等。需先在 `~/.claude.json` 中设置 `"hasCompletedOnboarding": true` 跳过官方登录验证。社区工具 [CC Switch](https://github.com/farion1231/cc-switch) 支持在多套餐间一键切换。详见 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。

### Codex

编辑 `~/.codex/config.toml` 配置 `model_provider`、`base_url` 和 `wire_api`，同时通过环境变量 `OPENAI_API_KEY` 设置密钥。qwen3.7-max 等模型支持 Responses API（最新版 Codex），其他模型需通过 Chat/Completions API 接入（需安装 Codex 0.80.0 旧版本）。详见 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)。

### Cursor

在 Cursor Settings > Models 中开启 OpenAI API Key 和 Override OpenAI Base URL，填入对应凭证。需要 Cursor Pro 及以上套餐才能使用自定义模型（免费版仅支持 Auto 模式）。部分模型名称需调整，如 `kimi-k2.6` 写为 `kimi-k2-6`、`glm-5` 写为 `glm-5-0`。

### Cline

在 VSCode 侧边栏的 Cline 配置界面选择 OpenAI Compatible 作为 API Provider。使用 Qwen3 思考模式或 QwQ 模型时，需在 MODEL CONFIGURATION 中勾选 Enable R1 messages format。

### Hermes Agent / OpenCode / Kilo CLI

均通过配置文件设置 Base URL 和 API Key。Hermes Agent 使用 `~/.hermes/config.yaml`，OpenCode 使用 `~/.config/opencode/opencode.json`，Kilo CLI 使用 `~/.config/kilo/config.json`。Hermes Agent 默认使用 OpenRouter，接入百炼时 `model.provider` 必须设置为 `custom`。

### Qwen Code

安装后通过 `/auth` 命令可视化配置，也可直接编辑 `~/.qwen/settings.json`。安装时指定 `--source bailian` 参数可预设百炼配置。

### Qoder / Qoder CN（原 Lingma）

[Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) 支持桌面 IDE、CLI 和 JetBrains 插件三种形态，在设置中选择"阿里云百炼 - 国内"作为提供商即可。[Qoder CN](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 仅个人社区版和个人专业版支持接入百炼，企业版不支持。

### Cherry Studio / Chatbox / QwenPaw

桌面客户端均在设置界面添加供应商，选择 OpenAI 兼容模式，填入 API Key 和 Base URL。QwenPaw 内置了百炼各套餐的提供商配置模板，在 Console 设置页面直接填入 API Key 即可。

### Dify

安装"通义千问"插件（非阿里云官方维护，由 Dify 官方维护），在模型供应商设置中填入 API Key。使用 DeepSeek 模型也需通过"通义千问"插件接入。Qwen-Omni、Qwen-Audio、Qwen-OCR 不支持直接在 Dify 配置，需通过 HTTP 节点接入。万相模型需导入工作流模板使用。

### Postman / cURL

适用于图像/视频生成等异步 API 的快速验证。调用分为两步：先创建任务获取 `task_id`，再轮询查询结果。仅支持按量计费方案。

## 百炼 CLI 集成

Cursor、Cline、Qoder 等工具支持通过安装百炼 CLI（`npm install -g bailian-cli`）注册 Skill，从而在对话中直接调用百炼的图像生成、视频生成等扩展能力。安装后 CLI 会自动向对应工具的 [skill](skill.md)s 目录注册，无需额外配置。

## 常见问题

### API Key 认证失败（HTTP 401）

- 三种计费方案的 API Key 不通用，确认 API Key 与 Base URL 来自同一方案。
- 按量计费的 API Key 必须与 Base URL 地域一致。
- 检查 API Key 是否完整复制、无多余空格。

### 模型名称冲突

在 Cursor 中，部分模型名称与内置模型冲突，需使用别名（如 `glm-5` 写为 `glm-5-0`）。如果配置完成后找不到模型，需关闭 Auto 模式再手动选择。

### 思考模式报错

部分模型仅支持思考模式运行。在 Cline 中需勾选 Enable R1 messages format；在 Cherry Studio 中需开启思考模式开关；在 Dify 中需将思考模式设置为 True。报错 `The value of the enable_thinking parameter is restricted to True` 即为此问题。

### 按量计费免费额度产生费用

免费额度仅适用于华北2（北京）地域，各模型额度独立计算不可共享，且控制台数据每小时更新存在延迟。

### 上下文超限

长对话或工具调用时可能触发上下文超限，需在对应工具中调整 `max_tokens` 参数或缩短对话历史。

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


