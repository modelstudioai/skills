# use chat client or development tool

阿里云百炼支持通过多种主流 AI 编程工具、桌面客户端及开发平台接入模型服务，覆盖终端 CLI、IDE 插件、Web UI 和工作流平台等场景。开发者可根据使用习惯选择 OpenAI 兼容协议或 Anthropic 兼容协议，并按需选用 [Token](../concepts/token.md) Plan（个人版/团队版）、Coding Plan 或按量计费方案。所有工具均需正确配置 API Key 与 Base URL，且不同计费方案的凭证**不通用**。

## 支持的模型/功能

- **文本生成模型**：全量支持 `qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus`、`qwen3.7-max`、`qwen3.6-flash`、`glm-5.3`、`glm-5.2`、`deepseek-v4.*` 等主流模型（详见 [Token Plan 个人版支持的模型](../../raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-personal-overview.md)）。
- **多模态能力**：`qwen3.8-max`、`qwen3.8-flash`、`qwen3.7-plus` 等支持图像输入；Qwen-VL、QVQ、Qwen-Omni 等视觉/语音模型需通过 HTTP 节点或原生 API 调用，**不支持直接在 Dify 等工作流平台中配置**（参见 [Dify 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)）。
- **思考模式（Reasoning）**：Qwen3 系列模型支持 `enable_thinking` 参数或 `effort` 级别控制（如 `xhigh`），部分工具（如 Cline、Qwen Code）需显式启用 R1 messages 格式或 `extra_body.enable_thinking` 配置。
- **图像/视频生成**：万相（wan2.*）、Qwen-VL-OCR 等 AIGC 模型**仅支持通过 Postman/cURL 或 SDK 异步调用**，不适用于 Chat Client 类工具（参见 [使用Postman或cURL调用图像/视频生成API](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。

> **注意**：千问 APP 的工作助理功能**仅支持 [Token](../concepts/token.md) Plan（个人版/团队版）**，明确不支持按量计费或 Coding Plan（见 [千问文档](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)）；而 Dify 等工作流平台**明确不支持 [Token](../concepts/token.md) Plan 和 Coding Plan**，仅允许使用按量计费 API Key（见 [Dify 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)）。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `Base URL` | 必须与计费方案和地域严格匹配。OpenAI 协议路径为 `/compatible-mode/v1`，Anthropic 协议为 `/apps/anthropic`。地域 URL 中 `{WorkspaceId}` 需替换为真实 ID（见 [Regions 文档](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）。 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan 个人版，OpenAI）<br>`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`（按量计费，Anthropic） |
| `API Key` | 四种计费方案的 API Key **完全隔离**，不可混用。Token Plan 个人版 Key 仅对个人版有效，团队版 Key 仅对团队版有效。 | `sk-xxx`（按量计费）<br>`tp-xxx`（Token Plan 个人版） |
| `Model ID` | 必须与百炼控制台公布的模型名**完全一致（区分大小写、无前后缀）**。部分工具（如 Cursor）要求将 `glm-5.3` 写为 `glm-5-3`，需按文档调整。 | `qwen3.8-max`（标准名）<br>`glm-5-3`（Cursor 要求） |
| `API Protocol` | 工具需明确指定协议类型：`openai-completions`（Chat Completions）、`anthropic-messages`、`openai-responses` 等。WorkBuddy 明确**仅支持 Chat Completions**，不支持 Responses API 或 Anthropic 协议（见 [WorkBuddy 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)）。 | `openai-completions`（DeepSeek Harness）<br>`anthropic-messages`（Hermes Agent） |

## 使用方式

1. **安装工具**：各工具依赖不同运行时（Node.js ≥18.0、Python ≥3.10 等），需按文档检查版本（如 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md) 要求 Node.js 22.19.0+）。
2. **配置凭证**：
   - CLI 工具（如 Hermes Agent、Qwen Code）通常提供 `hermes config set` 或 `/auth` 命令交互式配置；
   - 桌面客户端（如 Cursor、Cherry Studio）通过 GUI 设置界面填写 API Key、Base URL 和 Model ID；
   - IDE 插件（如 Cline、Qoder）在插件设置中选择 “OpenAI Compatible” 并填入参数；
   - 开发平台（如 Dify）需安装对应插件（如“通义千问”），并在插件设置中配置 API Key 和端点。
3. **验证连接**：发送简单请求（如 `"你好"`）并检查响应；部分工具（如 WorkBuddy、Chatbox）提供 “测试连接” 按钮。
4. **高级功能**：启用思考模式需在配置中显式设置（如 Qwen Code 的 `generationConfig.extra_body.enable_thinking: true`），或在工具 UI 中勾选 “Enable R1 messages format”（Cline）。

## 限制和注意事项

- **计费方案适用范围严格受限**：
  - Token Plan 个人版/团队版、Coding Plan **仅限 AI 编程工具（如 Claude Code、Qwen Code、Hermes Agent）和 OpenClaw 类 Agent（如 QwenPaw、DeepSeek Harness）**；
  - **工作流/自动化平台（Dify、n8n、Coze）和 API 测试工具（Postman、cURL）明确不支持上述套餐**，否则可能导致订阅暂停（见 [更多工具文档](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)）。
- **地域与额度绑定**：按量计费的免费额度**仅适用于华北2（北京）地域**，使用新加坡或美国地域模型将立即产生费用（见 [Cherry Studio 文档](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)）。
- **模型兼容性差异**：
  - Cursor 免费版**仅支持 `auto` 模型**，自定义模型需升级付费计划；
  - 千问 APP 工作助理**仅支持 Token Plan 模型**，且手机 APP 需 ≥7.1.2 版本；
  - Qoder CN 企业版**不支持接入百炼**，仅限个人社区版/专业版。
- **错误排查重点**：
  - `401 Incorrect API key provided`：确认 API Key 与 Base URL 方案、地域完全匹配；
  - `400 InternalError.Algo.InvalidParameter`：检查是否遗漏思考模式开关（如 Cline 的 R1 messages）；
  - “模型不存在”：核对 Model ID 是否与百炼控制台显示的名称**一字不差**（如 `qwen3.8-max` 不可写作 `qwen38max` 或 `Qwen3.8-Max`）。

## 来源文档

- [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)
- [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)
- [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md)
- [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)
- [千问](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-office-assistant.md)
- [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)
- [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)
- [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md)
- [接入 WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)
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


