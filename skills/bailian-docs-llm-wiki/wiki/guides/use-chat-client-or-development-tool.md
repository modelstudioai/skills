# use chat client or development tool

阿里云百炼支持将平台模型接入各类 AI 编程工具、聊天客户端与应用开发平台，包括 Claude Code、Codex、Cursor、Cline、Qwen Code、Cherry Studio、Chatbox、Dify 等。接入方式统一为「选择计费方案 → 获取对应 API Key → 在工具中配置 Base URL 与模型」三步。本文汇总各工具的接入要点、端点地址与常见问题。

## 计费方案与凭证

所有工具均围绕四种计费方案接入，各方案的 API Key **互不通用**：

| 方案 | 计费方式 | 说明 |
| --- | --- | --- |
| Token Plan 个人版 | 按 token 消耗抵扣个人 Credits | 个人订阅 |
| Token Plan 团队版 | 按坐席订阅，按 token 消耗抵扣 Credits | 团队订阅 |
| Coding Plan | 固定月费，按模型调用次数计量 | 编程场景专用 |
| 按量计费 | 按实际调用量后付费 | API Key 与地域绑定 |

Token Plan 个人版可用模型包括 qwen3.8-max-preview、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、glm-5.2、deepseek-v4-pro。

## 统一端点（Base URL）

各方案提供 OpenAI 兼容与 Anthropic 兼容两类协议端点，完整对照见[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)：

| 方案 | OpenAI 兼容 | Anthropic 兼容 |
| --- | --- | --- |
| Token Plan（个人/团队） | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` |
| 按量计费（美国弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | — |

按量计费需将 `{WorkspaceId}` 替换为真实[业务空间](../concepts/workspace.md) ID，且 API Key 必须与端点地域一致。

## 工具接入方式一览

### 终端 CLI 类

- **Claude Code**：在 `~/.claude/settings.json` 的 `env` 中配置 `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_BASE_URL` / `ANTHROPIC_MODEL` 等变量，走 Anthropic 兼容端点；需先在 `~/.claude.json` 设置 `hasCompletedOnboarding: true` 跳过官方登录。详见 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)。
- **Codex**：编辑 `~/.codex/config.toml` 定义 `model_providers`，并设置 `OPENAI_API_KEY` 环境变量。qwen3.8-max-preview、qwen3.7-max/plus、qwen3.6-plus/flash 支持 `wire_api = "responses"`（最新版 Codex）；其他模型需 `wire_api = "chat"` 并降级安装 `@openai/codex@0.80.0`。自定义模型还需配置 `model-catalog.local.json` 元数据文件。
- **Qwen Code**：启动后输入 `/auth` 可视化配置，或编辑 `~/.qwen/settings.json` 的 `modelProviders`；思考模型需在 `generationConfig.extra_body` 中设置 `enable_thinking: true`。
- **Hermes Agent** / **OpenCode** / **Kilo CLI** / **Qoder CLI**：均支持四种方案。Hermes 用 `hermes config set` 写 `~/.hermes/config.yaml`（默认 Anthropic 协议，`api_mode: anthropic_messages`）；OpenCode 配置 `~/.config/opencode/opencode.json`（注意其 Anthropic Base URL 末尾多一级 `/v1`）；Kilo CLI 配置 `~/.config/kilo/config.json`。

### IDE / 桌面客户端类

- **Cursor**：在 **Cursor Settings > Models** 开启 OpenAI API Key 与 Override OpenAI Base URL。免费版仅支持 Auto 模式，调用自定义模型需 Cursor Pro 及以上。部分模型名与内置模型冲突，需用别名（如 kimi-k2.6 写为 `kimi-k2-6`、glm-5.2 写为 `glm-5-2`、glm-5 写为 `glm-5-0`）。详见 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)。
- **Cline**（VSCode 插件）：API Provider 选 **OpenAI Compatible**；使用 Qwen3 思考模式或 QwQ 模型时需勾选 **Enable R1 messages format**，否则报 400 InternalError.Algo.InvalidParameter。
- **Qoder / Qoder CN（原 Lingma）**：内置「阿里云百炼 - 国内」提供商，直接选类型（Token Plan / Coding Plan / 按量付费）并填 API Key，仅支持文本生成模型。Qoder CN 企业版不支持接入。
- **Cherry Studio / Chatbox**：添加自定义提供商，API 模式选 OpenAI 兼容，填入对应方案的 Base URL 与 API Key，手动新建模型 ID。

### 平台 / 助手类

- **Dify**：安装通义千问插件（Dify 官方维护，非阿里云提供）或 OpenAI-API-compatible 插件接入；Qwen-Omni / Qwen-Audio / Qwen-OCR 不支持直接配置，需通过 HTTP 节点接入；万相文生图/视频通过工作流模板实现。
- **QwenPaw / OpenClaw**：开源个人 AI 助手，分别通过 Console 设置页和 `~/.openclaw/openclaw.json` 配置内置的百炼提供商。

### 直接调 HTTP（Postman / cURL）

图像与视频生成 API 采用**异步机制**：先 POST 创建任务拿到 `task_id`（有效期 24 小时），再 GET 轮询直到 `task_status` 为 `SUCCEEDED`；生成结果 URL 有效期同样为 24 小时。此方式仅适合快速测试，生产环境建议用 SDK。详见[使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：「更多工具」文档明确 Token Plan 与 Coding Plan 的 API Key **仅限 AI 编程工具和 OpenClaw 类 Agent 使用**，不支持工作流/自动化平台（Dify、n8n、Coze）、API 测试工具（Postman）和自定义应用后端；而 Dify 文档又给出了通过 OpenAI-API-compatible 插件接入 Token Plan 个人版的步骤，两处存在冲突。请以套餐使用条款为准，违规使用可能导致订阅暂停或 API Key 封禁。

## 关键参数与限制

- **qwen3.8-max-preview 思考模式**（多篇文档一致强调）：
  - `thinking` 始终开启，不支持关闭；
  - `temperature` 思考模式下默认 0.6，传入小于 0.6 会被自动调整为 0.6；
  - `reasoning_effort` 可选 `xhigh` / `medium` / `low`，默认 `xhigh`；
  - 上下文窗口 983616，最大输出 131072 tokens。
- **模型名称别名**：Cursor 中含 `.` 的模型名需改写（kimi-k2.5 → `kimi-k2-5` 等），其他工具无需调整。
- **地域绑定**：按量计费的 API Key、Base URL、模型部署地域三者必须匹配，免费额度仅限华北2（北京）地域。

## 常见问题排查

- **401 Incorrect API key provided / Unauthorized**：API Key 与 Base URL 不属于同一计费方案，或按量计费的 Key 与端点地域不一致；确认套餐未过期、Key 复制完整。
- **enable_thinking 参数报错**：模型仅支持思考模式，需在客户端开启 thinking。
- **上下文超限**：在工具的生成参数中调低 `max_tokens` 或调整上下文配置。
- 各方案错误码详情：按量计费见错误码文档，Coding Plan / Token Plan 见对应常见问题文档。

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


