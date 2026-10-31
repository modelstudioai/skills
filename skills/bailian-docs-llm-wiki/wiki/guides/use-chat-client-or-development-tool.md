# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web UI 和工作流平台等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（Token Plan 个人版/团队版、Coding Plan 或按量计费）配置对应凭证与端点。所有工具均基于 OpenAI 兼容协议或 Anthropic 兼容协议接入，无需修改业务逻辑即可切换底层模型。

## 支持的模型/功能

- **通用文本生成模型**：全量支持 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.7-max`、`qwen3.6-flash` 等 Qwen 系列模型；部分工具（如 OpenCode、Kilo CLI）还支持 `glm-5.3`、`glm-5.2`、`deepseek-v4.*` 等第三方模型。
- **多模态能力**：`qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus` 等支持图像输入（需客户端显式声明 `input: ["text", "image"]`），但千问 APP 工作助理 [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md) 仅限文档/表格类办公任务，不支持图像理解。
- **思考模式（Reasoning）**：Qwen3.7+ 及 Qwen3.8 系列模型支持 `enable_thinking` 参数（或 `effort: xhigh`），需在客户端配置中显式开启（如 Qwen Code、Cline、Claude Code）；未开启时可能返回 `400 InternalError.Algo.InvalidParameter` 错误。
- **图像/视频生成**：仅适用于直接调用 API 的场景（如 Postman/cURL），[使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 明确说明其异步机制与地域绑定规则，**不支持**通过 Chatbox、Cursor、WorkBuddy 等聊天客户端直接触发文生图/视频。

> **注意**：Dify 属于工作流/自动化平台，[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md) 明确声明**不支持** Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入，仅允许使用按量计费 API Key；将套餐 API Key 用于 Dify 将被视为违规。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `base_url` | 必填，服务端点地址，协议决定路径后缀 | OpenAI 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>Anthropic 协议：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |
| `api_key` | 必填，与 `base_url` 方案严格匹配的专属密钥 | Token Plan 个人版 API Key 不能用于 Coding Plan `base_url` |
| `model` | 必填，模型 ID，区分大小写且不可加前后缀 | `qwen3.7-plus`（正确）<br>`Qwen3.7-Plus` 或 `qwen3.7-plus-v1`（错误） |
| `enable_thinking` / `effort` | 选填，启用深度推理的开关或等级 | `true`、`xhigh`（Qwen3.8 系列推荐） |
| `workspace_id` | 按量计费必需，需从控制台获取并替换 URL 中 `{WorkspaceId}` | `ws-abc123xyz` |

## 使用方式

### 1. 客户端安装
- **CLI 工具**（如 Hermes Agent、Qwen Code、Claude Code）：依赖 Node.js ≥18，通过 `npm install -g` 安装；Windows 用户需 WSL2 或 Git Bash。
- **桌面应用**（如 Cursor、WorkBuddy、Cherry Studio）：从官网下载安装包，无需额外运行时。
- **IDE 插件**（如 Cline、Qoder JetBrains 插件）：在 VS Code 或 JetBrains 扩展市场搜索安装。
- **Web 平台**（如 Dify、QwenPaw）：本地部署或访问 SaaS 地址，通过浏览器配置。

### 2. 凭证配置
所有工具均遵循统一配置逻辑：
- **Token Plan 个人版/团队版**：`base_url` 统一为 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（OpenAI）或 `/apps/anthropic`（Anthropic），API Key 来自订阅页。
- **Coding Plan**：`base_url` 为 `https://coding.dashscope.aliyuncs.com/v1`（OpenAI）或 `/apps/anthropic`（Anthropic），API Key 来自 Coding Plan 订阅页。
- **按量计费**：`base_url` 需替换 `{WorkspaceId}` 为真实值，且 API Key 必须与地域一致（如北京地域 Key 不能用于新加坡 endpoint）。

> **注意**：[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 文档明确指出，**API 测试工具（Postman、Insomnia）和自定义应用程序（脚本/后端代码）不支持 Token Plan/Coding Plan 套餐**，仅允许按量计费接入。

### 3. 模型调用验证
- 发送简单请求（如 `"你好"`）确认基础连通性；
- 若需思考模式，必须在客户端设置中显式启用（如 Cline 的 `Enable R1 messages format`、Qwen Code 的 `enable_thinking: true`）；
- 图像输入需客户端支持 `multipart/form-data` 或 base64 编码，且模型本身声明 `input: ["text", "image"]`（见 OpenClaw 配置示例）。

## 限制和注意事项

- **地域强绑定**：按量计费的 `workspace_id` 与 API Key 必须同地域（华北2、新加坡、美国），跨地域使用将返回 `401` 或 `404`；Token Plan/Coding Plan 的 endpoint 无地域变量，但实际服务仍部署在北京。
- **模型兼容性差异**：
  - Cursor 免费版仅支持 `auto` 模型，指定 `qwen3.7-plus` 会报错 `Named models unavailable Free plans can only use Auto`；
  - 千问 APP 工作助理 [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md) **仅支持 Token Plan，不支持按量计费或 Coding Plan**；
  - 模型名需严格匹配：`glm-5.3` 在 Cursor 中需写为 `glm-5-3`，`kimi-k2.6` 需写为 `kimi-k2-6`。
- **额度与计费**：
  - Token Plan/Coding Plan 的 Credits 按 token 消耗抵扣，按量计费按实际调用量后付费；
  - 新人免费额度**仅限华北2（北京）地域的按量计费模型**，其他地域或套餐不享受（见 Cherry Studio 文档）。
- **安全与合规**：
  - 禁止将 Token Plan/Coding Plan API Key 用于 Dify、n8n、Coze 等工作流平台，[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md) 明确列为“不支持的工具类型”，违规可能导致订阅暂停；
  - 生产环境禁用 Postman/cURL，应使用 SDK 或封装 HTTP 调用（见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)


