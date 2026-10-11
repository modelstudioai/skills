# use chat client or development tool

百炼平台支持通过多种主流聊天客户端与开发工具接入大模型服务，适用于快速原型验证、本地 IDE 集成、自动化工作流编排等场景。开发者无需从零实现 API 调用逻辑，可直接复用已适配的客户端配置或工具插件。所有工具均基于标准 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（`/v1/chat/completions`）通信，但部分工具对流式响应、function calling 或 system [prompt](prompt.md) 处理存在差异。

## 支持的模型与功能

当前支持的客户端/工具覆盖通用对话、代码生成、办公辅助、多模态调用等方向，包括但不限于：OpenClaw、Hermes Agent、Cursor、Qwen Code、DeepSeek Harness、Dify、Postman（用于图像/视频 API 初探）、Cherry Studio 等。多数工具默认兼容 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `deepseek-vl` 等多模态模型，但 [Qoder CN（原 Lingma）](../../raw/model-user-guide/use-chat-client-or-development-tool/lingma-agent.md) 仅支持代码补全类模型（如 `qwen-coder`），不支持多轮对话状态维护。

> **注意**：[Postman](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 文档标题为“首次调用图像与视频 API”，但其实际内容仅描述如何用 Postman 发起 `/v1/chat/completions` 请求，并未提供图像/视频专属 endpoint 示例——该文档命名易引发误解，建议以 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 中的实操步骤为准，勿依赖标题推断能力范围。

## 关键参数

所有工具需配置以下基础参数：
- `API Key`：从百炼控制台「API 密钥管理」获取，权限需包含对应模型调用权限；
- `Base URL`：固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（兼容模式）或 `https://dashscope.aliyuncs.com/api/v1`（原生模式）；
- `Model Name`：必须与百炼平台发布的模型标识完全一致（如 `qwen-max`，区分大小写）；
- `Temperature` / `Top-p`：由客户端自行控制，百炼后端不强制校验，但超出 `[0.0, 2.0]` 范围时可能被静默截断。

部分工具（如 [Cline](../../raw/model-user-guide/use-chat-client-or-development-tool/cline.md) 和 [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md)）支持命令行传参覆盖默认值，推荐在 CI/CD 流程中使用。

## 使用方式

1. 在对应工具中配置上述参数（具体路径见各子文档）；  
2. 启动会话并发送消息，工具将自动构造符合 OpenAI 格式的请求体（含 `messages` 数组、`model` 字段等）；  
3. 响应解析由客户端完成，百炼仅保证返回标准 JSON Schema（含 `id`, `choices[0].message.content`, `usage` 等字段）。  

对于自定义集成，可参考 [OpenCode](../../raw/model-user-guide/use-chat-client-or-development-tool/opencode.md) 的底层请求示例，其展示了如何手动构造带 `system` 角色和 `tool_choice` 的请求体。

## 限制和注意事项

- 单次请求 `messages` 总长度（token）不得超过模型 context window 上限（如 `qwen-max` 为 8192），超长将被截断且无警告；
- 流式响应（`stream: true`）在 [Chatbox](../../raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md) 和 [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) 中默认启用，但在 [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) 中需显式勾选「Enable streaming」；
- 所有工具均不支持百炼私有化部署场景下的离线 token 计算，`usage.prompt_tokens` 等字段由服务端返回，不可本地预估；
- 若使用 [WorkBuddy](../../raw/model-user-guide/use-chat-client-or-development-tool/workbuddy.md) 进行多步骤任务编排，请注意其 `max_steps` 默认为 5，超出需修改配置文件。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


