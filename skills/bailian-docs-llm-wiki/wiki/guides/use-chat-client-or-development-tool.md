# use chat client or development tool

百炼平台支持通过多种主流聊天客户端与开发工具接入大模型服务，适用于快速原型验证、本地 IDE 集成及低代码工作流编排等场景。开发者可直接配置 API Key 和 Endpoint 即可调用，无需部署模型服务。所有工具均基于标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/v1/chat/completions`）通信，兼容性由 [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 文档统一维护。

## 支持的模型与功能

当前支持的客户端/工具覆盖三类能力：
- **通用对话增强**：如 [OpenClaw](../../raw/model-user-guide/use-chat-client-or-development-tool/openclaw.md)、[Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)、[Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md)，支持多轮上下文管理与插件扩展；
- **代码智能辅助**：如 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md)、[Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md)、[Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md)，深度集成代码补全、解释与重构；
- **Agent 工作流编排**：如 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md)、[Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)、[WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md)，支持[函数调用](../concepts/function-calling.md)、工具链编排与状态持久化。

> **注意**：[Postman](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 文档标题提及“image and video API”，但其实际内容仅描述如何用 Postman 调用文本生成接口，未提供多媒体能力支持——该标题存在误导，应以正文功能描述为准。

## 关键参数

所有工具需配置以下基础参数（以环境变量或 UI 表单形式传入）：
- `API_KEY`：百炼平台生成的密钥（非阿里云主账号 AK/SK）；
- `BASE_URL`：`https://dashscope.aliyuncs.com/compatible-mode/v1`（必须含 `/compatible-mode/v1` 路径）；
- `MODEL`：模型标识符，如 `qwen-max`、`qwen-plus`、`deepseek-v3`，需与所选工具支持的模型列表匹配（详见各工具子文档）；
- `STREAM`：布尔值，控制是否启用流式响应（部分工具如 [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) 强制启用）。

## 使用方式

1. 在百炼控制台「API 密钥」页生成并复制 `API_KEY`；
2. 根据目标工具文档（例如 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) 或 [Dify](../../raw/model-user-guide/use-chat-client-or-development-tool/dify.md)）配置 `BASE_URL` 与 `MODEL`；
3. 启动工具并发起首次请求；若返回 `401 Unauthorized`，请确认 `API_KEY` 是否过期或权限不足；
4. 流式响应需工具自身支持 `text/event-stream` 解析，不支持的工具（如旧版 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md)）将静默丢弃中间 chunk。

## 限制和注意事项

- 单次请求最大 `input_tokens + output_tokens ≤ 32768`（具体上限依模型而异，`qwen-max` 支持 32k，`qwen-turbo` 仅支持 8k）；
- 所有工具均**不支持**自定义 system [prompt](prompt.md) 的 `role: system` 字段（该字段会被忽略），需改用用户消息前置说明（参见 [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) 示例）；
- [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) 和 [DeepSeek Harness](../../raw/model-user-guide/use-chat-client-or-development-tool/deepseek-harness.md) 依赖特定版本的 SDK，低于 v0.5.0 的 `dashscope` Python 包无法正确解析 function calling 响应格式；
- 百炼暂不提供 WebSocket 接口，因此 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 等依赖 WebSocket 的工具需降级至 HTTP 长轮询模式使用。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


