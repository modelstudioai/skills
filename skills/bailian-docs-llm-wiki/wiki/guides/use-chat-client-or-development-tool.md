# use chat client or development tool

阿里云百炼支持通过各类终端 AI 编程工具、桌面客户端、IDE 插件、低代码平台及 HTTP 工具接入其模型服务。所有客户端共享同一套[计费](../concepts/billing.md)与鉴权模型：按量[计费](../concepts/billing.md)、Coding Plan、[Token](../concepts/token.md) Plan 团队版，区别仅在于配置入口和 Base URL。本文汇总各工具的接入方式、关键参数与限制。

## [计费](../concepts/billing.md)方案与通用接入参数

百炼为客户端接入提供三种[计费](../concepts/billing.md)方案，任何工具的配置都围绕这三组参数展开：

| 方案 | [计费](../concepts/billing.md)方式 | [API Key](../concepts/api-key.md) 来源 | 适用范围 |
| --- | --- | --- | --- |
| 按量[计费](../concepts/billing.md) | 按实际调用量后付费 | [阿里云百炼 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) | 所有工具类型 |
| Coding Plan | 固定月费，按模型调用次数计量 | Coding Plan 专属 [API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/efm/coding_plan) | 仅 AI 编程工具与 OpenClaw |
| [Token](../concepts/token.md) Plan 团队版 | 按坐席订阅，按 token 抵扣 Credits | [Token](../concepts/token.md) Plan 团队版专属 [API Key](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list) | 仅 AI 编程工具与 OpenClaw |

### Base URL 速查

不同协议、不同方案的 Base URL 不能混用。OpenAI 兼容协议统一以 `/compatible-mode/v1` 结尾，Anthropic 兼容协议统一以 `/apps/anthropic` 结尾。

| 方案 | OpenAI 兼容 Base URL | Anthropic 兼容 Base URL |
| --- | --- | --- |
| 按量[计费](../concepts/billing.md)（华北2-北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/apps/anthropic` |
| 按量[计费](../concepts/billing.md)（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` |
| 按量[计费](../concepts/billing.md)（美国-弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | （文档未列出 Anthropic 端点） |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| [Token](../concepts/token.md) Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

> **注意**：三种方案的 [API Key](../concepts/api-key.md) 互不通用，且必须与 Base URL 同一方案、同一地域。按量计费的 [API Key](../concepts/api-key.md) 还需与 Base URL 地域一致，否则会报 `401 Incorrect API key provided`。新加坡地域需将 `{WorkspaceId}` 替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

## 终端 AI 编程工具

终端类工具的安装方式相近，多为 npm 全局安装或官方安装脚本，配置则写入各自约定路径的 JSON / YAML / TOML 文件。

| 工具 | 安装命令 | 配置文件路径 | 默认协议 |
| --- | --- | --- | --- |
| [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) | `curl ... install.sh \| bash` | `~/.hermes/config.yaml`（`hermes config set`） | Anthropic Messages |
| [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) | `npm install -g @anthropic-ai/claude-code` | `~/.claude/settings.json` | Anthropic |
| [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md) | `npm install -g opencode-ai` | `~/.config/opencode/opencode.json` | Anthropic（`@ai-sdk/anthropic`） |
| [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) | `npm install -g @openai/codex` | `~/.codex/config.toml` + `OPENAI_API_KEY` 环境变量 | OpenAI Responses / Chat |
| [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) | 官方安装脚本（`--source bailian`） | `~/.qwen/settings.json`（`/auth` 向导） | OpenAI 兼容 |
| [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) | `npm install -g @kilocode/cli` | `~/.config/kilo/config.json` | OpenAI 兼容 / Anthropic |

### Codex 的 API 形态差异

Codex 较为特殊：[Token](../concepts/token.md) Plan 团队版下，`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash` 支持 Responses API（`wire_api = "responses"`），可使用最新版 Codex；其他模型（如 `glm-5`）只能走 Chat/Completions API（`wire_api = "chat"`），需降级安装旧版本（如 `npm install -g @openai/codex@0.80.0`）。Coding Plan 仅支持 Chat/Completions API，必须使用旧版本 Codex。

### Hermes Agent 接入要点

Hermes Agent 默认使用 OpenRouter 作为推理提供商，接入百炼时 `model.provider` 必须显式设置为 `custom`，否则会继续连到 OpenRouter。配置写入 `~/.hermes/config.yaml`，`api_mode` 设为 `anthropic_messages`。

### Claude Code 跳过官方登录

Claude Code 默认要求 Anthropic 官方登录。接入百炼时需编辑 `~/.claude.json`，将 `hasCompletedOnboarding` 设为 `true` 以跳过验证；随后在 `~/.claude/settings.json` 的 `env` 中写入 `ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL`、`ANTHROPIC_MODEL` 等。社区工具 [CC Switch](https://github.com/farion1231/cc-switch) 可在多个套餐间一键切换，无需手动改文件。

## 桌面客户端与 IDE 插件

桌面 / IDE 类工具通过图形界面配置，提供商类型多选 **OpenAI Compatible** 或 **OpenAI API 兼容**，再填入 Base URL、[API Key](../concepts/api-key.md)、Model ID。

| 工具 | 形态 | 安装来源 | 备注 |
| --- | --- | --- | --- |
| [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) | AI IDE | Cursor 官网 | 免费版仅支持 Auto 模式，调用自定义模型需 Cursor Pro 及以上 |
| [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) | VSCode 插件 | VSCode 扩展商店 | 使用 Qwen3 思考模式 / QwQ 时需勾选 **Enable R1 messages format** |
| [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) | 桌面客户端 | Cherry Studio 下载页 | 开源；RAM 子账号需在[业务空间](../concepts/workspace.md)授予模型调用权限 |
| [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md) | 跨平台客户端 | Chatbox 官网 / 网页版 | API 路径无需填写 |
| [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) | IDE + CLI + JetBrains 插件 | Qoder 官网 / `curl ... \| bash` | 仅支持文本生成模型 |
| Qoder CN（原 Lingma） | 独立 IDE | Qoder CN 官网 | 个人社区版 / 专业版支持，企业版不支持 |
| [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) | 个人 AI 助手 | pip / 一键脚本 / Docker | Console 图形配置，按量计费内置 DashScope 提供商 |
| [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) | 开源 Agent 平台 | 官方脚本 / `npm install -g openclaw@latest` | 需 Node.js 22+；配置在 `~/.openclaw/openclaw.json` |

### Cursor 的模型名别名

Cursor 与部分内置模型名冲突，需使用别名：`kimi-k2.6` → `kimi-k2-6`、`kimi-k2.5` → `kimi-k2-5`、`glm-5.2` → `glm-5-2`、`glm-5.1` → `glm-5-1`、`glm-5` → `glm-5-0`。配置后若找不到模型，需在聊天面板关闭 Auto 模式并从下拉栏选择。

### Qoder / Qoder CN 的提供商与类型一致性

Qoder 系列在模型配置中需同时选对**提供商**（阿里云百炼 - 国内）与**类型**（[Token](../concepts/token.md) Plan / Coding Plan / 按量付费）。若类型与实际套餐不一致（如用 [Token](../concepts/token.md) Plan 的 Key 但类型选 Coding Plan），会报 `Unknown Custom model Exception`。

## 百炼 CLI 集成

Cursor、Cline、Qoder 等支持通过对话调用百炼能力：全局安装 `bailian-cli` 后，安装过程会向 `~/.<工具>/skills/bailian-cli/` 注册 Skill，工具即可通过自然语言调用百炼能力（如生成电商主图、产品演示视频）。前置要求 Node.js 18+，[API Key](../concepts/api-key.md) 通过对话告知工具即可。

## 低代码与 HTTP 工具

### Dify

[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 是开源大模型应用开发平台，通过**通义千问插件**接入百炼（DeepSeek 模型也走该插件）。配置要点：

- 在 Dify 市场安装**通义千问**插件，于模型供应商设置中填入对应地域 [API Key](../concepts/api-key.md)；华北2（北京）设**使用国际端点**为**否**，新加坡设为**是**。
- 插件非阿里云官方维护，最新版可能不稳定，报错 `Invalid API-key provided` 时可降级安装较早版本。
- Qwen-Omni / Qwen-Audio / Qwen-OCR 不支持直接配置，需通过 Chatflow / 工作流的 HTTP 节点接入，建议[流式输出](../concepts/streaming-output.md)以降低超时风险。
- 万相文生图 / 视频：Dify 无内置插件，需导入官方工作流模板（`万相-文生图 Demo.yml` 等），并把 `DASHSCOPE_API_KEY` 环境变量改为自己的 Key。

### Postman / cURL 调用图像视频 API

图像 / 视频生成 API 采用**[异步调用](../concepts/async-invocation.md)机制**：先 POST 创建任务拿到 `task_id`，再 GET 轮询 `/api/v1/tasks/{task_id}` 直到 `task_status` 为 `SUCCEEDED`。请求头需带 `X-DashScope-Async: enable`、`Authorization: Bearer <api-key>`、`Content-Type: application/json`。`task_id` 与最终图像 / 视频 URL 有效期均为 24 小时。该方式仅适用于快速测试与功能验证，生产环境应使用官方 SDK。

> **注意**：Postman / cURL / Dify 这类工作流、API 测试、自定义应用工具**仅能使用按量计费**接入。[Token](../concepts/token.md) Plan 团队版和 Coding Plan 明确不支持此类工具，将套餐 Key 用于允许范围之外的调用可能被判定为违规滥用，导致订阅暂停或 Key 封禁。

## 支持的模型

各方案可用模型以官方文档为准：

- 按量计费：[OpenAI 兼容支持的模型](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#7f9c78ae99pwz) / [Anthropic 兼容支持的模型](https://help.aliyun.com/zh/model-studio/anthropic-api-messages#ae1b2c3d4e5f6)
- Coding Plan：[支持的模型](https://help.aliyun.com/zh/model-studio/coding-plan)
- [Token](../concepts/token.md) Plan 团队版：[支持的模型](https://help.aliyun.com/zh/model-studio/token-plan-overview)（仅文本生成类）

部分工具（如 OpenCode、Kilo CLI、Qwen Code）在配置文件中显式列出 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash`、`deepseek-v4-pro/flash`、`kimi-k2.7-code/2.6/2.5`、`glm-5.2/5.1/5`、`MiniMax-M2.5` 等，支持开启 `thinking` 思考模式（`budgetTokens` 一般设 8192，Coding Plan 下 Kilo CLI 设 1024）。Qoder / Qoder CN 仅支持文本生成模型，不支持[多模态](../concepts/multimodal.md)。

## 限制与注意事项

- **方案与工具匹配**：Token Plan 团队版、Coding Plan 仅限 AI 编程工具与 OpenClaw 使用；Dify、n8n、Coze、Postman、Insomnia、自定义应用后端等只能用按量计费。
- **[API Key](../concepts/api-key.md) 不可混用**：三种方案 Key 互不通；按量计费 Key 还需与地域一致。报 `401 Incorrect API key provided` 时优先排查此项。
- **思考模式开关**：思考型模型（Qwen3 思考模式、QwQ）在部分客户端需手动开启思考模式或勾选 R1 messages format，否则会报 `The value of the enable_thinking parameter is restricted to True` 或 `400 InternalError.Algo.InvalidParameter`。
- **免费额度限制**：按量计费免费额度仅适用华北2（北京）地域模型，各模型额度独立、不可跨模型共享，控制台数据每小时更新可能滞后。
- **Windows 安装**：Hermes Agent、Claude Code 等在 Windows 上需先装 WSL2 或 Git Bash，再在 WSL / Git Bash 中执行安装命令。
- **地域与部署范围**：各地域支持的模型为系统预设绑定关系，不支持自由组合，详见 [地域与部署范围](https://help.aliyun.com/zh/model-studio/regions/#6e9530261dv6q)。
- **错误码排查**：按量计费见 [错误码](https://help.aliyun.com/zh/model-studio/error-code)，Coding Plan 见 [Coding Plan 常见问题](https://help.aliyun.com/zh/model-studio/coding-plan-faq)，Token Plan 团队版见 [Token Plan 团队版常见问题](https://help.aliyun.com/zh/model-studio/token-plan-faq)。

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






