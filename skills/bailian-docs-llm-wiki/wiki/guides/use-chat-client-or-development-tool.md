# use chat client or development tool

阿里云百炼支持通过多种第三方聊天客户端和开发工具接入平台上的 AI 模型。开发者可以根据使用场景选择终端 CLI 工具、桌面 IDE、VSCode 插件或桌面聊天客户端，通过 OpenAI 或 Anthropic 兼容 API 协议完成配置后即可使用。所有工具均支持按量计费、Coding Plan 和 Token Plan 团队版三种计费方案。

## 支持的工具总览

百炼支持接入的工具涵盖以下几类：

**终端 AI 编程工具**：
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) — Anthropic 推出的命令行 AI 编程助手
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) — OpenAI 推出的终端 AI 编程助手
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) — 通义千问团队的终端 AI 编程工具，支持 `/auth` 可视化配置
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) — 基于 Python 的终端 AI 编程工具
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md) — 开源终端 AI 编程工具
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) — Kilo Code 的命令行客户端

**桌面 IDE / 编辑器插件**：
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) — AI 编程 IDE（需 Pro 及以上套餐才能使用自定义模型）
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) — VSCode 智能编程插件
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) — 面向软件开发的 Agentic 编码平台，支持桌面 IDE、CLI 和 JetBrains 插件
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) — 阿里云智能编码助手

**桌面聊天客户端**：
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) — 开源 AI 桌面客户端
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md) — 跨平台 AI 客户端应用

**个人 AI 助手 / 平台**：
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) — AgentScope 团队开源的个人 AI 助手，支持本地或云端部署
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) — 开源个人 AI 助手平台，支持多消息渠道
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) — 开源大模型应用开发平台

**API 测试工具**：
- [Postman / cURL](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) — 适用于图像/视频生成 API 的快速测试

此外，任何兼容 OpenAI 或 Anthropic API 协议且支持自定义服务端点的工具均可接入，详见[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 计费方案与接入地址

三种计费方案的 Base URL 和 API Key 各不相同，**不可混用**：

| 计费方案 | OpenAI 兼容 Base URL | Anthropic 兼容 Base URL | API Key 获取 |
|---------|---------------------|------------------------|-------------|
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 控制台 Token Plan 页面 |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` | 控制台 Coding Plan 页面 |
| 按量计费（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/apps/anthropic` | 百炼 API Key 管理页面 |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` | 百炼 API Key 管理页面 |
| 按量计费（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | — | 百炼 API Key 管理页面 |

> **注意**：Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，不支持工作流/自动化平台（如 Dify、n8n）、API 测试工具（如 Postman）或自定义应用程序。将套餐 API Key 用于允许范围之外的调用将被视为违规，可能导致订阅被暂停或 API Key 被封禁。

## API 协议选择

不同工具使用不同的 API 协议：

- **Anthropic Messages API**：Claude Code、Hermes Agent、OpenClaw、OpenCode、Kilo CLI（Coding Plan 模式）
- **OpenAI Compatible API**：Cursor、Cline、Cherry Studio、Chatbox、Codex、Qwen Code、Qoder、Qoder CN、Dify、Kilo CLI（Token Plan / 按量计费模式）

部分工具（如 Codex）同时支持 OpenAI Responses API 和 Chat/Completions API，具体取决于模型。qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash 支持 Responses API，其他模型需通过 Chat/Completions API 接入（可能需要安装旧版客户端）。

## 配置方式

各工具的配置方式大致分为以下几种：

### 配置文件方式

大多数终端工具通过编辑配置文件完成接入：
- **Claude Code**：编辑 `~/.claude/settings.json`，设置 `ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL`、`ANTHROPIC_MODEL` 等环境变量
- **Codex**：编辑 `~/.codex/config.toml`，配置 `model_provider` 和 `base_url`，并设置 `OPENAI_API_KEY` 环境变量
- **OpenCode**：编辑 `~/.config/opencode/opencode.json`，配置 provider 信息
- **Kilo CLI**：编辑 `~/.config/kilo/config.json`
- **Hermes Agent**：通过 `hermes config set` 命令或编辑 `~/.hermes/config.yaml`
- **OpenClaw**：编辑 `~/.openclaw/openclaw.json`

### GUI 配置方式

桌面客户端和 IDE 插件通常提供图形化配置界面：
- **Cursor**：Settings > Models > OpenAI API Key / Override OpenAI Base URL
- **Cline**：插件设置 > OpenAI Compatible > Base URL + API Key + Model ID
- **Cherry Studio**：设置 > 模型 > 添加供应商
- **Chatbox**：设置 > 模型提供方 > 添加 > OpenAI API 兼容
- **Qoder / Qoder CN**：设置 > 模型 > 添加，选择"阿里云百炼 - 国内"
- **QwenPaw**：Console 设置 > 模型，内置百炼提供商

### 交互式配置

- **Qwen Code**：启动后输入 `/auth` 命令，可视化选择计费方案并输入 API Key

## 可用模型

不同计费方案支持的模型范围不同。以 Token Plan 团队版为例，常用模型包括：

- **Qwen 系列**：qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash
- **DeepSeek 系列**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2
- **Kimi 系列**：kimi-k2.6、kimi-k2.5
- **GLM 系列**：glm-5.2、glm-5.1、glm-5
- **其他**：MiniMax-M2.5

> **注意**：在 Cursor 中，部分模型名称需做调整以避免与内置模型冲突：kimi-k2.6 写为 kimi-k2-6，glm-5.2 写为 glm-5-2，glm-5 写为 glm-5-0 等。

## 百炼 CLI 集成

部分工具（Cursor、Cline、Qoder）支持通过安装百炼 CLI 获得额外能力。安装后 CLI 会自动向对应工具注册 Skill，可直接通过自然语言调用百炼的图像生成、视频生成等功能。前置要求 Node.js 18+，安装命令：

```
npm install -g bailian-cli
```

## 图像 / 视频生成 API 调用

文本生成模型以外，百炼还提供图像和视频生成 API。这类 API 采用异步调用机制：先创建任务获取 `task_id`，再轮询查询结果。可通过 Postman 或 cURL 快速测试，生产环境建议使用官方 SDK。详细步骤参见[使用 Postman 或 cURL 调用图像/视频生成 API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## Dify 平台集成

Dify 作为大模型应用开发平台，通过安装"通义千问"插件接入百炼模型。支持聊天助手、Agent、Chatflow/工作流和知识库等多种应用类型。使用 DeepSeek 等非千问模型时也应使用"通义千问"插件。万相模型（文生图/视频）需通过工作流的 HTTP 节点接入。详见 [Dify 接入文档](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

## 常见问题

### API Key 认证失败（401）

- 三种计费方案的 API Key 不通用，请确认 API Key 和 Base URL 来自同一方案
- 按量计费的 API Key 与 Base URL 需在同一地域
- 确认 API Key 复制完整、无空格

### 模型调用失败

- Cursor 免费版仅支持 Auto 模式，需升级至 Pro 及以上套餐才能使用自定义模型
- 使用 Qwen3（思考模式）或 QwQ 模型时，Cline 需勾选 "Enable R1 messages format"
- 部分模型名称与工具内置名称冲突时需使用别名

### 免费额度与计费

- 免费额度仅适用于华北2（北京）地域，使用其他地域会产生费用
- 各模型的免费额度相互独立，不可跨模型共享
- 控制台显示的免费额度数据每小时更新，可能存在延迟

### 错误码排查

- 按量计费：参考错误码排查文档
- Coding Plan：参考 Coding Plan 常见问题文档
- Token Plan 团队版：参考 Token Plan 团队版常见问题文档

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


