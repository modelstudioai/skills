# use chat client or development tool

阿里云百炼支持通过多种第三方聊天客户端和开发工具接入其模型服务，涵盖终端 AI 编程助手、桌面 AI 客户端、IDE 插件和开发平台等类型。用户可根据自身需求选择合适的工具，通过按量计费、Coding Plan 或 Token Plan 团队版三种计费方案接入百炼平台上的大模型。本文汇总各工具的安装配置方法、支持的接入方式及常见问题。

## 支持的工具概览

百炼支持接入的工具可分为以下几类：

**终端 AI 编程工具**：[Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)、[Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)、[Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)、[Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)、Qoder CLI

**桌面 AI 客户端**：[Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)、[Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)、[QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)、[OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)

**IDE / 编辑器插件**：[Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)、[Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)（VSCode）、[Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)、[Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) IDE/JetBrains 插件

**开发平台**：[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)（开源大模型应用开发平台）

**API 测试工具**：[Postman / cURL](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)（仅用于图像/视频生成 API 的快速测试）

## 三种计费方案

所有工具均通过以下三种计费方案之一接入百炼，不同方案的 API Key 和 Base URL 不同，不可混用：

| 计费方案 | 计费模式 | API Key 获取 | 适用场景 |
|---------|---------|-------------|---------|
| Token Plan 团队版 | 按坐席订阅，按 token 消耗抵扣 Credits | 控制台 Token Plan 页面 | 团队协作、按需弹性用量 |
| Coding Plan | 固定月费订阅，按模型调用次数计量 | 控制台 Coding Plan 页面 | AI 编程场景、固定预算 |
| 按量计费 | 按实际调用量后付费 | 百炼 API Key 页面 | 灵活试用、生产环境 |

> **注意**：Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，不支持接入工作流/自动化平台（如 Dify、n8n）、API 测试工具（如 Postman）或自定义应用程序。将套餐 API Key 用于允许范围之外的调用可能导致订阅被暂停或 API Key 被封禁。详见[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## API 协议与 Base URL

百炼支持 OpenAI 兼容和 Anthropic 兼容两种 API 协议。不同工具根据其架构选择对应协议：

### OpenAI 兼容协议

| 计费方案 | Base URL |
|---------|---------|
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |
| 按量计费（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 按量计费（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

使用 OpenAI 兼容协议的工具：Cursor、Cline、Cherry Studio、Chatbox、Codex、OpenCode、Kilo CLI、Qwen Code、Qoder、QwenPaw。

### Anthropic 兼容协议

| 计费方案 | Base URL |
|---------|---------|
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（北京） | `https://dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` |

使用 Anthropic 兼容协议的工具：Claude Code、Hermes Agent。

## 各工具配置要点

### Claude Code

通过环境变量方式配置，编辑 `~/.claude/settings.json`，设置 `ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL`、`ANTHROPIC_MODEL` 等环境变量。首次使用需编辑 `~/.claude.json` 将 `hasCompletedOnboarding` 设为 `true` 以跳过 Anthropic 官方登录验证。社区工具 CC Switch 支持在多个 API Key 或计费套餐间一键切换。

### Codex

编辑 `~/.codex/config.toml` 配置文件并设置 `OPENAI_API_KEY` 环境变量。qwen3.7-max 等部分模型支持 Responses API（最新版 Codex），其他模型需通过 Chat/Completions API 接入，需安装旧版本（如 0.80.0）。

### Cursor

在 Cursor Settings > Models 中开启 OpenAI API Key 和 Override OpenAI Base URL，填入对应参数。需注意 Cursor 免费版仅支持 Auto 模式，使用自定义模型需升级至 Pro 及以上套餐。部分模型名称存在冲突需使用别名（如 `kimi-k2.6` 写为 `kimi-k2-6`）。

### Cline

在 VSCode 中安装 Cline 插件，选择 OpenAI Compatible 作为 API Provider，填入 Base URL、API Key 和 Model ID。使用 Qwen3 思考模式或 QwQ 模型时，需在 MODEL CONFIGURATION 中勾选 Enable R1 messages format。

### 终端工具（Hermes Agent / OpenCode / Qwen Code / Kilo CLI）

各工具通过编辑各自的配置文件完成接入。Hermes Agent 使用 `~/.hermes/config.yaml`，OpenCode 使用 `~/.config/opencode/opencode.json`，Qwen Code 支持 `/auth` 交互式配置或编辑 `~/.qwen/settings.json`，Kilo CLI 使用 `~/.config/kilo/config.json`。

### 桌面客户端（Cherry Studio / Chatbox / QwenPaw / OpenClaw）

通过 GUI 设置界面添加模型提供商，填入 API Key 和 Base URL 即可。QwenPaw 内置了百炼各计费方案的提供商预设。OpenClaw 需编辑 `~/.openclaw/openclaw.json` 配置文件。

### Qoder / Qoder CN

Qoder 提供 IDE、CLI、JetBrains 插件三种形态，均在设置中选择"阿里云百炼 - 国内"提供商后填入 API Key。Qoder CN（原 Lingma）仅支持个人社区版和个人专业版接入百炼，企业版不支持。

### Dify

需安装 Dify 市场中的"通义千问"插件（由 Dify 官方维护），在模型供应商设置中配置 API Key。支持聊天助手、Agent、Chatflow/工作流和知识库等应用类型。万相模型需通过工作流 HTTP 节点接入。

> **注意**：Dify 属于工作流/自动化平台，仅支持按量计费方式接入，不支持 Token Plan 团队版和 Coding Plan。

### Postman / cURL

仅适用于图像/视频生成 API 的快速测试与功能验证。这类 API 采用异步调用机制：先调用接口创建任务获取 `task_id`，再轮询查询结果直到任务完成。生产环境建议使用官方 SDK。

## 百炼 CLI 集成

部分工具支持通过安装百炼 CLI（`npm install -g bailian-cli`）获得扩展能力。安装后会向工具的 skills 目录注册 Skill，可通过自然语言调用百炼的图像生成、视频生成等能力。目前支持百炼 CLI Skill 的工具包括 Cursor、Cline 和 Qoder。

## 常见问题

### API Key 与 Base URL 不匹配

三种计费方案的 API Key 不通用。Token Plan 团队版、Coding Plan 和按量计费各有独立的 API Key 和 Base URL，配置时必须确保二者来自同一方案。按量计费的 API Key 还需与 Base URL 的地域保持一致。

### 模型名称冲突

在 Cursor 中，部分模型名称与内置模型名冲突，需使用别名。例如 `kimi-k2.6` 写为 `kimi-k2-6`，`glm-5.1` 写为 `glm-5-1`，`glm-5` 写为 `glm-5-0`。

### 思考模式配置

使用 Qwen3 思考模式的模型时，不同工具需要不同的配置方式：Cline 需勾选 Enable R1 messages format；OpenCode 和 Kilo CLI 需在模型配置中设置 `thinking.type: "enabled"`；Cherry Studio 需在客户端中开启思考模式。部分模型（如某些仅支持思考模式的模型）如未开启思考模式会报错 "The value of the enable_thinking parameter is restricted to True"。

### 按量计费免费额度问题

免费额度仅适用于华北2（北京）地域的模型，各模型额度独立计算不可共享，且控制台显示的额度数据每小时更新，可能存在延迟。

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


