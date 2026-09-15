# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web 应用和工作流平台等场景。开发者可根据使用习惯选择适配的客户端，并按计费方案（Token Plan 个人版/团队版、Coding Plan 或按量计费）配置对应 API Key 与 Base URL。所有工具均基于 OpenAI 兼容协议或 Anthropic 兼容协议，无需修改业务逻辑即可快速迁移。

## 支持的模型/功能

百炼支持的模型能力因接入方式而异：

- **文本生成类模型**（如 `qwen3.8-max`、`qwen3.7-plus`、`glm-5.2`、`deepseek-v4-pro`）在所有客户端中广泛可用，支持思考模式（`enable_thinking`）、多模态输入（文本+图像）及长上下文（最高 983616 tokens）。
- **视觉模型**（如 `Qwen-VL`、`QVQ`、`Qwen-Omni`）仅在部分工具中支持：Dify 通过 Chatflow 的 HTTP 节点或 LLM 节点视觉开关调用 [Qwen-VL](raw/model-user-guide/model-experience/vision-model/vision.md) 和 [QVQ](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md)，但不支持直接配置；千问 APP 工作助理暂不支持视觉模型 [千问](raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)。
- **AIGC 生成类模型**（如 `wan2.6-t2i` 文生图）**不通过聊天客户端调用**，需使用异步 API 方式（如 Postman/cURL）[使用Postman或cURL调用图像/视频生成API](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
- **语音/OCR 模型**（如 `Qwen-Audio`、`Qwen-OCR`）同样不支持在标准聊天客户端中配置，需通过 Dify 的 HTTP 节点或自定义 SDK 调用 [Dify](raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

> **注意**：Dify 明确不支持 Token Plan 个人版、Token Plan 团队版和 Coding Plan 接入，仅允许使用按量计费 API Key；将套餐 API Key 用于 Dify 等工作流平台属于违规行为，可能导致订阅暂停或 API Key 封禁 [更多工具](raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 关键参数

所有客户端共用以下核心参数，但协议与路径存在差异：

| 参数 | OpenAI 兼容协议 | Anthropic 兼容协议 | 说明 |
|------|----------------|----------------------|------|
| **Base URL** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/v1`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（按量） | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`（Token Plan）<br>`https://coding.dashscope.aliyuncs.com/apps/anthropic`（Coding Plan）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量） | 协议必须与客户端配置一致；`{WorkspaceId}` 需替换为真实值 [获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h) |
| **API Key** | 各方案专属 Key，不通用 | 同上 | Token Plan 个人版 Key 仅可用于个人版 URL，混用将返回 401 错误 [Qoder CN（原 Lingma）](raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) |
| **模型 ID** | `qwen3.8-max`、`qwen3.7-plus` 等（注意命名规范：`glm-5.2` → `glm-5-2`） | 同上 | Cursor、Cherry Studio 等要求模型名中 `.` 替换为 `-` [Cursor](raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) |

## 使用方式

### 客户端接入流程（通用）
1. **安装工具**：根据操作系统执行官方安装命令（如 `npm install -g opencode-ai`、`curl ... \| bash`）；
2. **配置凭证**：
   - CLI 工具（Hermes Agent、Claude Code、Qwen Code）：通过命令行 `/auth` 或编辑 `~/.config/xxx/config.json`；
   - 桌面应用（Cursor、Cherry Studio、Chatbox）：在 Settings > Models 中填写 API Key、Base URL 和 Model ID；
   - IDE 插件（Cline、Qoder JetBrains）：在插件设置界面添加自定义模型；
3. **验证连接**：发送“你好”或运行 `xxx --version` 确认环境就绪。

### 开发者直连（非客户端）
- **Postman/cURL**：适用于图像/视频生成等异步任务，需两步调用（创建任务 + 轮询结果）[使用Postman或cURL调用图像/视频生成API](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)；
- **Dify 工作流**：使用 `OpenAI-API-compatible` 插件，手动填入 `compatible-mode/v1` 端点，配合 HTTP 节点调用非文本模型 [Dify](raw/model-user-guide/use-chat-client-or-development-tool/dify.md)。

## 限制和注意事项

- **地域绑定**：按量计费的 API Key 与 Workspace ID 必须同地域（如北京 Key 不能用于新加坡 URL），否则报错 401 或产生意外费用 [Cherry Studio](raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)；
- **免费额度限制**：新人免费额度仅限华北2（北京）地域的模型，跨地域调用即计费 [Cherry Studio](raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)；
- **模型兼容性**：
  - 千问 APP 工作助理**仅支持 Token Plan**（个人版/团队版），不支持按量计费或 Coding Plan [千问](raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)；
  - Cursor 免费版仅支持 Auto 模式，调用自定义模型需升级至 Pro 套餐 [Cursor](raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)；
- **协议差异**：Anthropic 协议需显式设置 `api_mode: anthropic_messages`（如 Hermes Agent），而 OpenAI 协议需删除该字段并使用 `/v1` 路径 [Hermes Agent](raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)；
- **安全提示**：Windows 用户安装 CLI 工具（如 Hermes Agent、Claude Code）需先启用 WSL2，原生 CMD 不支持 [Hermes Agent](raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)。

## 来源文档

- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md)
- [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)
- [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)
- [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md)
- [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)
- [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)
- [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)
- [更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)
- [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)
- [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md)


