# use chat client or development tool

阿里云百炼支持通过多种第三方聊天客户端和 AI 编程工具接入模型服务。开发者可根据自身场景选择终端 CLI 工具、桌面客户端、IDE 插件或开发平台，配合按量计费、Coding Plan 或 Token Plan 团队版三种计费方案使用百炼提供的大模型能力。

## 支持的工具总览

百炼当前支持的工具涵盖以下几类：

**终端 AI 编程工具**：[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)、[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)、[Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)、[Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)、[Qoder CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)

**桌面客户端**：[Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)、[Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)、[QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)、[OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)

**IDE 插件 / 编程 IDE**：[Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)、[Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)（VSCode 插件）、[Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)、Qoder IDE / JetBrains 插件

**开发平台**：[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)（开源大模型应用开发平台）

**API 测试工具**：[Postman 或 cURL](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)（仅按量计费，用于图像/视频生成 API 的快速验证）

## 计费方案与接入凭证

三种计费方案的 API Key 和 Base URL 互不通用，配置时需确保方案、密钥和地址一一对应：

| 计费方案 | API Key 来源 | OpenAI 兼容 Base URL | Anthropic 兼容 Base URL |
|---|---|---|---|
| Token Plan 团队版 | 控制台 Token Plan 页面 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | 控制台 Coding Plan 页面 | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（北京） | 百炼 API Key | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/apps/anthropic` |

按量计费还支持新加坡和美国（弗吉尼亚）地域，需使用对应地域的 Base URL 和 API Key。

> **注意**：Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用。工作流/自动化平台（如 Dify、n8n）、API 测试工具（如 Postman）以及自定义应用程序不支持使用这两种套餐的 API Key，违规使用可能导致订阅被暂停或 API Key 被封禁。详见[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 各工具配置方式

### 使用 Anthropic 兼容 API 的工具

**Claude Code**：编辑 `~/.claude/settings.json`，通过 `ANTHROPIC_AUTH_TOKEN` 和 `ANTHROPIC_BASE_URL` 环境变量配置。还可通过 CC Switch 桌面工具在多套凭证间一键切换。

**Hermes Agent**：通过 `hermes config set` 命令配置 `model.base_url`、`model.api_mode`（设为 `anthropic_messages`）和 `model.api_key`。`model.provider` 必须设为 `custom`，否则仍连接到默认的 OpenRouter。

**OpenCode / Kilo CLI**：编辑对应的 JSON 配置文件，使用 `@ai-sdk/anthropic` npm 包，指定 `baseURL` 和 `apiKey`。支持为每个模型独立配置思考模式（thinking）参数。

### 使用 OpenAI 兼容 API 的工具

**Cursor**：在 Settings > Models 中开启 OpenAI API Key 和 Override OpenAI Base URL，填入对应凭证。注意 Cursor 免费版仅支持 Auto 模式，需升级至 Pro 及以上才能调用自定义模型。部分模型名称需使用别名（如 `kimi-k2.6` 写为 `kimi-k2-6`）。

**Cline**：选择 OpenAI Compatible 作为 API Provider，填入 Base URL、API Key 和 Model ID。使用 Qwen3 思考模式或 QwQ 模型时需勾选 Enable R1 messages format。

**Cherry Studio / Chatbox**：在设置中添加供应商，提供商类型选 OpenAI，填入 API 密钥和 API 地址。

**Codex**：编辑 `~/.codex/config.toml` 配置文件。qwen3.7-max 等模型支持 Responses API（最新版 Codex），其他模型需通过 Chat/Completions API 接入（需安装旧版 Codex 如 0.80.0）。

**Qwen Code**：启动后输入 `/auth` 进行可视化配置，支持在三种方案间快速切换。也可通过 `settings.json` 手动配置。

### 内置百炼支持的工具

**Qoder**（IDE / CLI / JetBrains 插件）和 **Qoder CN（原 Lingma）**：在设置中选择"阿里云百炼 - 国内"作为提供商，选择计费类型和模型后填入 API Key 即可。Qoder CN 仅个人社区版和个人专业版支持接入，企业版不支持。

**QwenPaw**：内置了 Aliyun Token Plan、Aliyun Coding Plan 和 DashScope 三个提供商，在 Console 设置页面填入 API Key 即可使用。

### 开发平台

**Dify**：安装通义千问插件（Dify 官方维护），在模型供应商处配置 API Key。支持聊天助手、Agent、Chatflow/工作流和知识库等应用类型。使用 DeepSeek 模型也需通过通义千问插件接入。万相等图像/视频模型需通过工作流 HTTP 节点接入。

### API 测试

**Postman / cURL**：仅适用于按量计费的快速测试。图像/视频生成 API 采用异步调用机制：先创建任务获取 `task_id`，再轮询查询结果，任务结果 URL 有效期 24 小时。

## 百炼 CLI 集成

Cursor、Cline 和 Qoder 支持通过百炼 CLI 扩展能力。安装 `bailian-cli`（`npm install -g bailian-cli`）后，CLI 会向对应工具的 skills 目录注册 Skill，即可在对话中使用文生图、文生视频等百炼能力。

## 常见问题

**API Key 与 Base URL 不匹配**：三种计费方案的凭证互不通用。按量计费还需确保 API Key 与 Base URL 的地域一致。

**模型名称冲突**：在 Cursor 中，部分模型名称与内置模型冲突，需使用别名（如 `glm-5` 写为 `glm-5-0`）。

**思考模式报错**：使用需强制开启思考模式的模型时，需在客户端中启用思考模式。Cherry Studio 报错"The value of the enable_thinking parameter is restricted to True"即属此类。

**免费额度产生费用**：免费额度仅适用于华北2（北京）地域，各模型额度独立计算，控制台显示的额度数据每小时更新。

**Codex API 兼容性**：部分模型仅支持 Chat/Completions API，需安装旧版 Codex（如 0.80.0）并在配置中将 `wire_api` 设为 `chat`。

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


