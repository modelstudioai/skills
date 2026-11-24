# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API 协议层，完全遵循 OpenAI 官方 API 的路径、请求/响应结构、参数命名与语义规范（如 `/v1/chat/completions`），使开发者无需修改业务代码即可将现有基于 OpenAI SDK 或生态工具（LangChain、LlamaIndex 等）的应用快速迁移到百炼平台，调用 Qwen 系列及部分第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：复用 `openai` Python SDK（v1.35.0+）、`@langchain/openai` 等客户端，仅需替换 `base_url`（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）和 `api_key`（使用百炼 API Key），即可调用 `chat/completions`、`embeddings`、`images/generations`、`files`、`batches`、`conversations` 等全部标准端点。  
- **多模态交互**：通过 `/v1/chat/completions` 接口，以 OpenAI Vision 格式（`messages[].content` 中含 `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}`）输入图像，支持 `qwen3-vl-plus`、`qwen3.8-omni-flash` 等多模态模型；注意仅支持 base64 编码，不支持远程 URL。  
- **Agent 与复杂工作流**：使用 **OpenAI 兼容 Responses API**（端点 `/v1/responses`），专为 Agent 场景优化，内置联网搜索、代码解释器、知识库检索等工具链，支持 `previous_response_id` 简化多轮上下文管理，并通过 `x-dashscope-session-cache: enable` 启用自动会话缓存。  
- **开发工具集成**：VS Code、Cursor、ZCode、Qoder、WorkBuddy 等主流 AI 编程工具均通过该协议接入百炼，配置时只需填写对应计费方案（[Token](token.md) Plan / 按量计费 / Coding Plan）的专属 `Base URL` 和 `Model ID`（如 `qwen3.8-max`、`qwen4-max`）。  
- **批量与文件处理**：调用 `/v1/batches` 提交批量推理任务；上传文件使用 `/v1/files`（兼容 OpenAI 文件接口），获取 `file_id` 后在 Batch 或 Chat 请求中引用；注意百炼不支持 `purpose="fine-tune"`，且文件仅限同账号内一次性使用。

## 关键参数和配置

- `model`：**必填**，必须显式指定百炼平台支持的模型 ID（如 `qwen3.8-max`、`qwen3-vl-plus`），不支持 OpenAI 别名（如 `gpt-3.5-turbo`）；未传将返回 400 错误。  
- `messages`：标准数组格式，每项含 `role`（`user`/`assistant`/`system`）与 `content`；`content` 支持文本、base64 图像（`image_url`）、或混合类型（需按 OpenAI Vision 结构组织）。  
- `response_format`：仅支持 `{"type": "json_object"}`（要求模型具备 JSON 输出能力，如 `qwen-plus`），`text` 为默认隐式值，不可省略。  
- `tools` / `tool_choice`：支持[函数调用](function-calling.md)，但 `function.parameters` 必须为合法 JSON Schema object（不支持 `null` 或 `anyOf`）；`tool_choice="auto"` 行为与 OpenAI 不完全一致，建议显式指定函数名。  
- `max_tokens`：控制最大输出长度（单位：token），适用于 `chat/completions`；注意 `qwen4-max` 等模型的 reasoning token 会计入此上限。  
- `detail`（多模态）：图像/视频精度控制，取值 `low`/`high`/`auto`（默认 `high`），需置于 `image_url` 对象内或同级（兼容性适配，但推荐统一放 `image_url` 内）。  
- `stream`：支持流式响应（`stream=true`），但**禁止与 `tools` 同时启用**（组合将返回 400 错误）。  
- `store` / `previous_response_id`（Responses API 专属）：`store=true` 时返回可复用的 `response_id`，用于后续请求的上下文继承与缓存续用。

> ⚠️ 注意事项：所有 OpenAI 兼容接口均不支持 streaming + function calling 组合；`conversations` 接口为只读模拟层，不持久化会话状态；Qwen-Audio、实时音视频（AOQ）、异步长任务（如视频生成）等能力**不通过 OpenAI 兼容接口提供**，需使用 DashScope 原生 API 或 AOQ SDK。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)
- [file management api](../api/file-management-api.md)


