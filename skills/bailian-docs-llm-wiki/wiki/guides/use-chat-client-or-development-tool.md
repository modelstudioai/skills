# use chat client or development tool

阿里云百炼支持通过多种第三方聊天客户端和开发工具接入模型服务。这些工具涵盖终端 AI 编程助手、桌面聊天客户端、IDE 插件、工作流平台及 API 测试工具，均可通过 OpenAI 或 Anthropic 兼容 API 协议完成配置。本文汇总各工具的接入方式、计费方案选择及常见注意事项。

## 计费方案概览

百炼提供三种计费方案，所有工具的接入配置均围绕这三种方案展开：

| 方案 | 计费模式 | API Key 获取 |
|------|----------|-------------|
| **Token Plan 团队版** | 按坐席订阅，按 token 消耗抵扣 Credits | [控制台获取](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview) |
| **Coding Plan** | 固定月费订阅，按模型调用次数计量 | [控制台获取](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan) |
| **按量计费** | 按实际调用量后付费 | [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) |

> **注意**：三种方案的 API Key 互不通用，Base URL 也不同，配置时务必确认 API Key 与 Base URL 来自同一方案。

## Base URL 参考

各方案对应的 Base URL 按 API 协议和地域有所不同：

**Token Plan 团队版：**
- OpenAI 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- Anthropic 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

**Coding Plan：**
- OpenAI 协议：`https://coding.dashscope.aliyuncs.com/v1`
- Anthropic 协议：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

**按量计费（华北2/北京）：**
- OpenAI 协议：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- Anthropic 协议：`https://dashscope.aliyuncs.com/apps/anthropic`

按量计费还支持新加坡和美国（弗吉尼亚）地域，需使用对应的地域 URL，详见[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 终端 AI 编程工具

以下工具在终端或命令行环境中运行，面向开发者的日常编码场景。

### Claude Code

Anthropic 推出的命令行 AI 编程助手，通过 Anthropic 协议接入。安装后需编辑 `~/.claude/settings.json`，配置 `ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL` 等环境变量。还可通过社区工具 [CC Switch](https://github.com/farion1231/cc-switch) 实现多套凭证一键切换。详见 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。

### Qwen Code

通义千问官方终端编程工具，安装后通过 `/auth` 命令进行可视化配置，也可直接编辑 `~/.qwen/settings.json`。支持 OpenAI 协议，可配置 `enable_thinking` 开启思考模式。详见 [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)。

### Hermes Agent

基于终端的 AI 编程工具，通过 `hermes config set` 命令或编辑 `~/.hermes/config.yaml` 配置，使用 Anthropic 协议接入。配置时 `model.provider` 必须设为 `custom`，否则会默认连接到 OpenRouter。详见 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。

### Codex

OpenAI 推出的终端编程助手，通过编辑 `~/.codex/config.toml` 和设置 `OPENAI_API_KEY` 环境变量配置。qwen3.7-max/plus 和 qwen3.6-plus/flash 支持 Responses API（最新版 Codex），其他模型需通过 Chat/Completions API 接入（需安装旧版本如 0.80.0）。详见 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)。

### OpenCode

终端编程工具，配置文件位于 `~/.config/opencode/opencode.json`，使用 `@ai-sdk/anthropic` 适配器接入。详见 [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)。

### Kilo CLI

Kilo Code 的命令行客户端，配置文件位于 `~/.config/kilo/config.json`，结构与 OpenCode 类似，使用 `@ai-sdk/openai-compatible` 适配器。详见 [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)。

## IDE 插件

### Cursor

AI 编程 IDE，在 Settings > Models 中开启 OpenAI API Key 和 Override OpenAI Base URL 后填入凭证。部分模型名称与 Cursor 内置名冲突，需使用别名（如 kimi-k2.6 写为 kimi-k2-6，glm-5 写为 glm-5-0）。免费版仅支持 Auto 模式，需升级至 Pro 及以上才能调用自定义模型。详见 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。

### Cline

VSCode 智能编程插件，选择 OpenAI Compatible 作为 API Provider 后填入 Base URL、API Key 和 Model ID。使用 Qwen3（思考模式）或 QwQ 模型时需勾选 **Enable R1 messages format**。详见 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)。

### Qoder / Qoder CN（原 Lingma）

Qoder 提供桌面 IDE、CLI 和 JetBrains 插件三种形态，配置时在提供商下拉菜单选择"阿里云百炼 - 国内"即可。Qoder CN（原 Lingma）是阿里云智能编码助手独立 IDE，配置方式相同，但仅个人社区版和个人专业版支持接入百炼，企业版不支持。详见 [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) 和 [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)。

## 桌面聊天客户端

### Cherry Studio

开源 AI 桌面客户端，在设置 > 模型中添加供应商（类型选 OpenAI），填入 API Key 和 API 地址。使用仅支持思考模式的模型时需在客户端开启思考模式。详见 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。

### Chatbox

跨平台 AI 客户端，在设置 > 模型提供方中添加新供应商（API 模式选 OpenAI API 兼容），填入 API 密钥和 API 主机（注意 API 路径无需填写）。详见 [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)。

### QwenPaw

AgentScope 团队开源的个人 AI 助手，支持 pip 或一键脚本安装，启动后在 Console 设置 > 模型中选择内置的提供商（如 Aliyun Token Plan、DashScope 等）填入 API Key。长对话或工具调用时若报上下文超限，可在进阶配置中调整 `max_tokens`。详见 [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)。

### OpenClaw

开源个人 AI 助手平台，支持多消息渠道。配置文件位于 `~/.openclaw/openclaw.json`，使用 Anthropic 协议接入。默认禁用网关鉴权（`auth.mode: none`），仅适合单机使用，共享或远程访问需运行 `openclaw doctor --fix` 启用 token 鉴权。详见 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)。

## 工作流与应用开发平台

### Dify

开源大模型应用开发平台，通过安装通义千问插件并配置 API Key 接入。支持聊天助手、Agent、Chatflow/工作流、知识库等多种应用类型。图像/视频生成（万相模型）需通过 HTTP 节点配合工作流模板实现。Qwen-Omni、Qwen-Audio、Qwen-OCR 等模型不支持直接在 Dify 配置，需通过 HTTP 节点调用。详见 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

> **注意**：Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，不支持在 Dify 等工作流/自动化平台中接入，否则可能导致订阅被暂停或 API Key 被封禁。Dify 用户应使用按量计费方案。

## API 测试工具

### Postman / cURL

适用于图像和视频生成 API 的快速测试与功能验证。这类 API 采用异步调用机制：先创建任务获取 `task_id`，再轮询查询结果。Postman 和 cURL 仅适合测试，生产环境建议使用官方 SDK。详见[使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 百炼 CLI 集成

Cursor、Cline、Qoder 等工具支持通过安装百炼 CLI（`npm install -g bailian-cli`）注册 Skill，实现在对话中直接调用百炼能力（如生成图片、视频等）。安装后 Skill 文件会自动注册到对应工具的 skills 目录。

## 常见问题

### API Key 认证失败（HTTP 401）

- 确认 API Key 与 Base URL 来自同一计费方案
- 按量计费时确认 API Key 与 Base URL 的地域一致
- 确认套餐未过期，API Key 复制完整、无空格

### 模型名称冲突

部分工具（如 Cursor）中，某些模型名称与内置名冲突，需使用别名。例如 `kimi-k2.6` 写为 `kimi-k2-6`，`glm-5` 写为 `glm-5-0`。

### 思考模式相关报错

使用 Qwen3 思考模式或 QwQ 模型时，部分工具（如 Cline）需额外开启 R1 messages format；部分仅支持思考模式的模型（如在 Cherry Studio 中）需在客户端开启思考模式，否则会报错。

### 按量计费免费额度与实际扣费

免费额度仅适用于华北2（北京）地域，各模型独立计算，控制台显示的额度数据每小时更新，可能存在延迟。

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



