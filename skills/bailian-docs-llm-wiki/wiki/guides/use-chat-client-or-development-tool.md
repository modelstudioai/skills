# use chat client or development tool

阿里云百炼支持将平台上的模型接入各类第三方 AI 客户端、编程工具和应用开发平台。这些工具大致分为三类：终端/IDE 类 AI 编程工具（Claude Code、Codex、Cursor、Cline、Qwen Code、OpenCode、Kilo CLI、Hermes Agent、Qoder 等）、桌面/跨平台聊天客户端（Cherry Studio、Chatbox）与个人 AI 助手（OpenClaw、QwenPaw），以及应用开发/测试工具（Dify、Postman、cURL）。本文汇总它们接入百炼时的通用模式、计费方案与常见差异。

## 三种计费方案与接入端点

绝大多数工具都支持三种计费方案接入，凭证与 Base URL 一一对应、**不可跨方案通用**：

| 计费方案 | 说明 | OpenAI 兼容 Base URL | Anthropic 兼容 Base URL |
| --- | --- | --- | --- |
| Token Plan 团队版 | 按坐席订阅，按 token 消耗抵扣 Credits | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| Coding Plan | 固定月费订阅，按模型调用次数计量 | `https://coding.dashscope.aliyuncs.com/v1` | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |
| 按量计费 | 按实际调用量后付费（华北2/北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/apps/anthropic` |

按量计费还支持多地域：新加坡 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`（需替换真实 Workspace ID），美国（弗吉尼亚）`https://dashscope-us.aliyuncs.com/...`。API Key 必须与地域对应。三种方案的入口、可用模型与端点差异可对照 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 中的汇总表。

## 按接入协议选择工具

接入方式主要取决于工具使用的 API 协议：

- **OpenAI 兼容协议**（`/compatible-mode/v1` 或 `/v1`）：Cursor、Cline、Cherry Studio、Chatbox、Qwen Code、OpenCode、Kilo CLI 等。在工具中通常选择 "OpenAI Compatible / OpenAI API 兼容" 提供商，填入 Base URL、API Key 与 Model ID 即可。
- **Anthropic 兼容协议**（`/apps/anthropic`）：Claude Code、Hermes Agent 等。Claude Code 通过 `~/.claude/settings.json` 的 `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` 等环境变量配置，详见 [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)；Hermes Agent 通过 `hermes config set` 写入 `~/.hermes/config.yaml`。
- **原生集成提供商**：Qoder、Qoder CN（原 Lingma）在设置中直接选择 "阿里云百炼 - 国内" 提供商，再选计费方案类型与模型，无需手填 Base URL。

## 典型配置方式

不同工具的配置载体各异，常见几类：

1. **配置文件**：OpenCode（`~/.config/opencode/opencode.json`）、Kilo CLI（`~/.config/kilo/config.json`）、Qwen Code（`~/.qwen/settings.json`）、Codex（`~/.codex/config.toml`）、OpenClaw（`~/.openclaw/openclaw.json`）等，需要手动写入 provider、baseURL、apiKey 与 models 列表。
2. **GUI 设置面板**：Cursor、Cline、Cherry Studio、Chatbox、QwenPaw、Qoder 系列通过界面表单填写。
3. **交互式命令**：Qwen Code 用 `/auth`，Qoder CLI 用 `/model` 切换到 Custom 后添加自定义模型。

Codex 的接入较特殊：Token Plan 下 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash` 支持 Responses API（`wire_api = "responses"`，可用最新版），其余模型及 Coding Plan 仅支持 Chat/Completions API，需安装旧版本如 `@openai/codex@0.80.0`，详见 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)。

## 模型名称与思考模式注意事项

- **模型名冲突需用别名**：在 Cursor 中部分模型名会与内置模型冲突，需改写，如 `kimi-k2.6` → `kimi-k2-6`、`glm-5.2` → `glm-5-2`、`glm-5` → `glm-5-0`。不同计费方案的可调整清单略有差异，以 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) 为准。
- **思考模式**：Qwen3（思考模式）或 QwQ 模型在 Cline 中需勾选 **Enable R1 messages format**；OpenCode / Kilo CLI 在模型配置中通过 `thinking.type = enabled` 与 `budgetTokens` 开启；Cherry Studio 若报错 "enable_thinking parameter is restricted to True"，需在客户端开启思考模式。
- **仅文本生成**：Qoder / Qoder CN 的模型接入仅支持文本生成模型，不支持[多模态](../concepts/multimodal.md)。

## 应用开发与快速测试工具

- **Dify**：开源大模型应用开发平台，通过安装 **通义千问** 插件（DeepSeek 模型同样使用该插件）配置 API Key 构建聊天助手、工作流、知识库；万相文生图/视频需用工作流 HTTP 节点或导入官方 DSL 模板实现。
- **Postman / cURL**：用于图像、视频生成 API 的快速测试。此类任务采用异步调用：先创建任务拿到 `task_id`，再轮询查询直到 `task_status` 变为 `SUCCEEDED`。task_id 与结果 URL 有效期均为 24 小时。

> **注意**：Token Plan 团队版和 Coding Plan **仅限在 AI 编程工具和 OpenClaw 类 Agent 中使用**。工作流/自动化平台（Dify、n8n、Coze）、API 测试工具（Postman、Insomnia）及自定义应用后端调用**不在允许范围内**，违规使用可能导致订阅被暂停或 API Key 被封禁。因此 Dify、Postman、cURL 场景应使用**按量计费** API Key。

## 常见问题排查

- **401 / API key 认证失败**：优先确认 API Key 与 Base URL 是否来自同一计费方案（三种方案 Key 不通用），以及按量计费的 Key 与 Base URL 是否为同一地域。
- **模型不可用**：Cursor 免费版仅支持 Auto 模式，需升级至 Pro 及以上才能调用自定义模型；配置后需在下拉栏关闭 Auto 手动选择模型。
- **免费额度仍产生费用**：免费额度仅适用于华北2（北京）地域，且各模型额度独立、控制台数据每小时更新。
- **错误码文档**：按方案区分——按量计费查错误码文档、Coding Plan 与 Token Plan 团队版分别查各自的常见问题文档。

> **注意**：各文档中出现的模型名称（如 `qwen3.7-max`、`glm-5.2`、`kimi-k2.7-code`、`deepseek-v4-pro` 等）均为文档示例，实际可用模型请以对应计费方案的"支持的模型"列表为准，以免因版本更新导致信息过时。

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


