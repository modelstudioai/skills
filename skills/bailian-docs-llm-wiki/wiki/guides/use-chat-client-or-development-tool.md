# use chat client or development tool

阿里云百炼支持通过 OpenAI 或 Anthropic 兼容协议接入多种第三方 AI 编程工具、桌面客户端及开发平台。开发者可根据实际场景选择按量计费、Coding Plan 或 Token Plan 团队版，仅需配置 [[api-key]] 与 [[base-url]] 即可在本地或 IDE 环境中快速调用主流大模型。本文档汇总了接入流程的核心参数、配置路径及平台约束规范。

## 支持的模型/功能
- **协议支持**：完整兼容 `OpenAI Compatible`（路径通常为 `/v1` 或 `/compatible-mode/v1`）与 `Anthropic Compatible`（路径固定为 `/apps/anthropic`）。
- **模型范围**：以文本生成与代码辅助模型为主，部分客户端支持 [[vision-model]]（视觉/多模态）及 [[thinking-mode]]（深度思考）。具体可用模型清单以所选 [[计费方案]] 的控制台列表为准。
- **扩展能力**：多数 CLI 工具支持通过 MCP（Model Context Protocol）或 Skills 机制扩展文件系统读写、终端命令执行等本地代理能力。

## 关键参数
在任意第三方工具中接入百炼，核心需关注以下配置项：
| 参数 | 说明 |
|:---|:---|
| `API Key` | 对应计费方案的专属凭证。Token Plan 团队版、Coding Plan 与按量计费的 Key **互不通用**。 |
| `Base URL` | 请求路由地址。按地域划分：北京（`dashscope.aliyuncs.com`）、新加坡（`dashscope-intl.aliyuncs.com`）、弗吉尼亚（`dashscope-us.aliyuncs.com`）。协议不同路径后缀亦不同。 |
| `Model ID` | 工具内需填写的模型标识。部分 IDE（如 Cursor）内置模型名冲突，需使用平台提供的别名（如 `kimi-k2.6` 改为 `kimi-k2-6`）。 |
| `Thinking Config` | 调用 Qwen3 思考版或 QwQ 时，需在请求体或 UI 中显式设置 `enable_thinking: true` 或勾选 `Enable R1 messages format`，否则将返回参数校验错误。 |
| 配置文件路径 | CLI 工具多采用 JSON/TOML/YAML 本地配置（如 `~/.claude/settings.json`、`~/.codex/config.toml`、`~/.opencode/opencode.json`），GUI/IDE 多采用图形化录入。 |

## 使用方式
根据工具形态，接入流程主要分为以下三类：

### 1. CLI 终端编程助手
以 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、Hermes Agent、Codex、OpenCode 等为代表。
- **安装**：通常依赖 Node.js (v18+) 或 Python，通过 `npm install -g` 或 `curl` 脚本一键安装。
- **配置**：新建或编辑本地配置文件，将 `ANTHROPIC_AUTH_TOKEN` 或 `OPENAI_API_KEY` 替换为对应套餐凭证，并写入专属 `base_url`。保存后重启终端，执行 `claude "你好"` 或等效测试命令验证连通性。
- **管理**：社区提供 CC Switch 等 GUI 切换器，支持多 API Key 与计费套餐的免配置文件热切换。

### 2. IDE 插件与桌面客户端
以 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)、Cline、Qwen Code、Cherry Studio、Qoder (CN/Global) 等为代表。
- **配置路径**：进入 Settings → Models/API Provider，选择 `OpenAI Compatible` 或 `Custom` 协议。
- **参数录入**：填写 Base URL、API Key 及 Model ID。部分工具（如 Cline、Qoder CLI）需在首次连接时完成 OAuth 或 PAT 身份验证。
- **验证**：关闭 `Auto` 路由，手动选择目标模型发起对话，响应正常即完成接入。

### 3. 低代码平台与 API 测试工具
以 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)、Postman、cURL 为代表。
- **平台接入**：Dify 需安装官方或 OpenAI-Compatible 插件，在插件设置中填入百炼端点。图像/视频生成类 API 采用异步机制，需通过 Postman/cURL 分两步（创建任务获取 `task_id` → 轮询 `task_status`）获取结果。
- **自定义应用**：直接在脚本或后端代码中调用时，需严格遵循平台速率限制与异步规范，并自行处理鉴权 Header (`Authorization: Bearer <key>`)。

## 限制和注意事项
> **注意**：套餐使用范围严格受限。Token Plan 团队版与 Coding Plan **仅限**在 AI 编程工具与 OpenClaw 类 Agent 客户端中使用。将其用于工作流/自动化平台（如 Dify、n8n）、API 测试工具或自定义后端应用调用，将被视为违规滥用，可能导致 API Key 被封禁或订阅暂停。

> **注意**：计费方案与地域强绑定。按量计费的 API Key 必须与 Base URL 所在的地域完全匹配，否则将触发 401 鉴权失败或产生非预期费用。各模型的免费额度相互独立，且控制台数据存在约 1 小时的更新延迟。

- **协议与路径匹配**：Anthropic 协议必须使用 `/apps/anthropic` 路径，OpenAI 协议使用 `/compatible-mode/v1` 或 `/v1`。配置时严禁混用 Base URL 后缀。
- **免费版/企业版限制**：部分工具免费版（如 Cursor Free）仅支持 `Auto` 模型路由，无法指定自定义模型；Qoder CN 企业版暂不支持自定义百炼接入，需使用社区版或个人专业版。
- **插件版本兼容**：第三方市场维护的插件（如 Dify 千问插件）可能因权限校验策略升级导致 `Invalid API-key` 报错。若新版鉴权失败，可尝试安装较低稳定版本，或切换至 OpenAI-Compatible 通用插件直连。
- **RAM 子账号权限**：使用企业子账号配置时，需确保该子账号在[[业务空间管理]]中已授权对应模型的调用权限，否则 GUI/CLI 验证阶段会直接拦截。

## 来源文档

- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/[[more|more]]-tools.md)

