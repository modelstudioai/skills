# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程客户端与开发工具接入模型服务，覆盖终端 CLI、桌面 IDE、Web Agent 及低代码平台等场景。开发者可根据使用习惯选择适配的工具，并按计费方案（[Token](../concepts/token.md) Plan 个人版/团队版、Coding Plan 或按量计费）配置对应 API 协议、Base URL 与凭证。所有工具均基于 OpenAI 兼容或 Anthropic 兼容协议，无需修改业务逻辑即可快速迁移。

## 支持的模型/功能

- **通用文本生成模型**：全部工具均支持 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.6-flash`、`glm-5.3` 等主流文本模型；部分工具（如 OpenClaw、Kilo CLI、Qwen Code）还支持 `deepseek-v4.*` 系列模型。
- **多模态能力**：Qwen Code、WorkBuddy、Cherry Studio 等支持图像输入（`input: ["text", "image"]`），但需确认所选模型实际支持（如 `qwen3.7-plus` 明确支持图文理解）；视觉/音频/OCR/万相等专用模型**不支持**在 Chatbox、Cursor、Cline 等通用客户端中直接调用，详见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **思考模式（Reasoning / Thinking）**：Qwen3 系列模型（如 `qwen3.7-plus`、`qwen3.8-max`）需显式启用 `enable_thinking: true` 或设置 `effort: xhigh` 才能触发深度推理，否则可能降级为普通响应。该参数在 Hermes Agent、Qwen Code、Cline 等工具中需通过 `generationConfig.extra_body.enable_thinking` 或 `env` 变量配置。
- **专用模型限制**：千问工作助理仅支持 [Token](../concepts/token.md) Plan（个人版/团队版），不支持按量计费或 Coding Plan [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)；Dify 作为工作流平台，**明确不支持** [Token](../concepts/token.md) Plan 和 Coding Plan，仅允许使用按量计费 API Key [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

> **注意**：文档 10（QwenPaw）与文档 20（更多工具）对“支持模型”的描述存在矛盾——前者称 Coding Plan 支持 `qwen3.6-plus`，后者未列出该模型且 Coding Plan 官方文档未声明支持；实际以 [Coding Plan 支持的模型](../../raw/model-user-guide/token-plan-guide/coding-plan-guide/coding-plan.md) 为准，当前仅明确支持 `qwen3.7-plus` 及更早版本。

## 关键参数

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `Base URL` | 模型服务端点地址，协议决定路径结构 | OpenAI 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 兼容：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | 必须与 API Key 方案及地域严格匹配；按量计费 URL 中 `{WorkspaceId}` 需替换为真实 ID [获取Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain) |
| `API Key` | 计费方案专属密钥，**不可混用** | Token Plan 个人版 Key ≠ Coding Plan Key ≠ 按量计费 Key | 复制时避免前后空格；报错 `401 Incorrect API key provided` 通常因方案/地域不匹配 [Qoder CN](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) |
| `Model ID` | 请求中 `model` 字段值，区分大小写、无额外后缀 | `qwen3.7-plus`（正确）<br>`qwen3.7-plus-v1`（错误） | Cursor、WorkBuddy 等要求模型名完全一致；部分工具（如 Cursor）对 `kimi-k2.6` 等含小数点名称需转为 `kimi-k2-6` |
| `API Protocol` | 决定请求格式与认证头 | `openai-completions`（Chat Completions）、`anthropic_messages`、`responses` | WorkBuddy 明确要求使用 Chat Completions（即 `/chat/completions` 路径），不支持 Responses API 或 Anthropic 协议 [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md) |

## 使用方式

### 1. 工具安装
- **CLI 工具**（Hermes Agent、Claude Code、Qwen Code、Kilo CLI）：依赖 Node.js（v18+）或 Python，通过 `curl` 脚本或 `npm install -g` 安装。
- **桌面应用**（Cursor、WorkBuddy、Cherry Studio）：从官网下载安装包，无需本地运行时依赖。
- **IDE 插件**（Cline、Qoder JetBrains）：在 VS Code 或 JetBrains 市场搜索安装。
- **Web 平台**（Dify、OpenClaw Web UI）：访问对应域名，配置后即用。

### 2. 凭证配置（统一模式）
所有工具均遵循三步配置：
- **Step 1**：获取对应计费方案的 API Key（[Token Plan 个人版](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)、[Coding Plan](https://bailian.console.aliyun.com/cn-beijing/subscription/coding-plan)、[按量计费](../../raw/model-api-reference/preparations/get-api-key.md)）；
- **Step 2**：填写 Base URL（按方案与地域选择，参考 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 表格）；
- **Step 3**：指定 Model ID（从各方案支持的模型列表中选取，如 [Token Plan 个人版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）。

> **注意**：Dify 的配置流程特殊——必须通过「通义千问」插件接入，且仅接受按量计费 Key；若插件内无目标模型，需改用「OpenAI-API-compatible」插件并手动填入兼容模式 Base URL [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

### 3. 验证与调试
- 发送简单请求（如 `"你好"`）验证连通性；
- 遇到 `400 InternalError.Algo.InvalidParameter`：检查是否遗漏 `enable_thinking` 参数（Qwen3 思考模式必需）；
- 遇到 `404 Not Found`：确认 Base URL 路径是否完整（如 WorkBuddy 要求 `/chat/completions` 结尾）；
- 遇到上下文超限：调整 `max_tokens` 或 `context_window` 参数（QwenPaw 支持 JSON 进阶配置）。

## 限制和注意事项

- **计费方案适用范围严格隔离**：
  - Token Plan 个人版/团队版、Coding Plan **仅限 AI 编程工具与 OpenClaw 类 Agent 使用**（如 Hermes、Cursor、OpenClaw、Qwen Code）；
  - **工作流平台（Dify、n8n）、API 测试工具（Postman、cURL）、自定义应用后端** 等场景**禁止使用**上述套餐 Key，否则可能导致订阅暂停 [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)；
  - 按量计费 Key 是唯一可用于 Dify、Postman、cURL 及生产环境 SDK 的凭证。

- **地域与免费额度绑定**：
  - 新人免费额度**仅适用于华北2（北京）地域**的模型调用；
  - 使用新加坡或美国地域的按量计费模型将**立即产生费用**，即使控制台显示免费额度仍有余量 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)。

- **模型能力与协议强相关**：
  - Anthropic 协议（`/apps/anthropic`）支持 `auto` 模型路由与原生 `tool_use`，但部分工具（如 Cursor）仅支持 OpenAI 协议；
  - OpenAI 协议（`/compatible-mode/v1`）需显式指定模型 ID，且 `thinking` 功能依赖 `extra_body.enable_thinking` 字段，非所有工具默认开启。

- **安全与权限**：
  - RAM 子账号需在业务空间中被授予 `AliyunBailianFullAccess` 或等效权限，否则调用返回 `403 Forbidden`；
  - 生产环境建议使用最小权限策略，避免将主账号 Key 硬编码至客户端配置文件。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)


