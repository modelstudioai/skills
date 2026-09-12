# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 REST API，完全遵循 OpenAI 的请求/响应协议（包括路径、参数名、字段结构与事件流格式），使开发者无需修改业务代码即可将基于 OpenAI SDK 或生态工具（如 LangChain、Cursor、Dify、Postman）构建的应用快速迁移到百炼平台，底层由 Qwen 系列模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`、`qwen2.5-*`）提供服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **应用迁移**：已有调用 OpenAI `chat/completions`、`completions`、`embeddings`、`vision`、`files`、`batches`、`conversations`（已逐步迁移至 `thread_id` 模式）等端点的项目，只需将 `base_url` 改为 `https://dashscope.aliyuncs.com/compatible-mode/v1` 并使用百炼 API Key，即可零代码切换。
- **工具集成**：支持 OpenAI 协议的第三方客户端（如 Cursor、Dify、Chatbox、Postman、Kilo CLI）和开发框架（如 LangChain）可直接配置百炼为后端，通过 `BaiLianChatModel` 等封装类开箱即用。
- **快速原型验证**：开发者可跳过复杂鉴权与参数嵌套（如 DashScope 原生的 `input.messages` 结构），直接使用扁平化 JSON 请求体（如 `{"model": "qwen-max", "messages": [...]}`），降低调试门槛。
- **文件与批量任务协同**：配合 `/files` 上传文件（支持 `purpose=batch`）、再在 `/batches` 或 `/chat/completions` 中引用 `file_id`，实现与 OpenAI Batch 工作流一致的异步处理体验。

> ⚠️ 注意：  
> - `system` 角色在 OpenAI 兼容接口中被忽略（Qwen 不支持该角色语义），需改用 `user` + 提示词前置方式；  
> - 原生工具调用（`tool_choice`、`tools` 高级策略）不支持，如需完整工具链能力，请使用 DashScope 原生接口；  
> - `conversations` 独立端点已下线，统一使用 `/chat/completions` + `thread_id` 维护会话状态。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，必须为百炼已开通的 Qwen 模型，如 `qwen-max`、`qwen2.5-72b-instruct`；不支持别名或通配符 |
| `messages` | array | 是（chat 场景） | 对话历史数组，格式为 `[{"role": "user", "content": "..." }, ...]`；`role` 仅支持 `"user"` / `"assistant"`，`"system"` 被静默丢弃 |
| `temperature` | number | 否 | 采样温度，默认 `1.0`，范围 `[0.0, 2.0]`；值越低输出越确定 |
| `top_p` | number | 否 | 核采样阈值，默认 `1.0`；建议与 `temperature` 二选一使用 |
| `max_tokens` | integer | 否 | 最大生成 token 数，非硬性截断（受模型上下文窗口限制）；默认由模型自动推导 |
| `stream` | boolean | 否 | 是否启用流式响应（SSE），设为 `true` 时返回 `data: {...}` 格式 chunk，客户端需按行解析 |
| `tools` / `functions` | array | 否 | **不推荐使用**：`functions` 字段已弃用；如需工具调用，请切换至 DashScope 原生接口并使用 `tools` 字段 |

- **Endpoint 示例**：  
  `POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
- **认证方式**：Header 中设置 `Authorization: Bearer <your_api_key>`  
- **Content-Type**：必须为 `application/json`

## 面向开发者，简洁实用

- ✅ **即插即用**：替换 `openai.base_url` 或工具中的 `base_url` 即可，无需重写逻辑。  
- ✅ **全栈兼容**：支持同步/流式响应、Vision（`image_url` / `image_data` Base64）、Embedding、Batch、File 管理等 OpenAI 主流能力。  
- ✅ **错误友好**：HTTP 状态码与 OpenAI 一致（如 `400` 参数错误、`429` 限流、`401` 认证失败），响应体含 `error.message` 和 `error.type` 字段便于调试。  
- ⚠️ **避坑提示**：  
  - 不要传 `system` 消息——会被忽略；  
  - 不要依赖 `function_call` 自动触发——工具调用需显式解析并调用；  
  - 流式响应中 `delta.content` 可能为空字符串，应跳过空片段；  
  - 所有文件操作（`/files`, `/batches`）均需先上传再引用，且 `purpose` 必须匹配下游任务类型（如 `batch`）。  

如需更高阶控制（如 `logprobs`、`seed`、自定义 `stop`、完整工具协议），请优先选用 [DashScope 原生接口](dashscope-native-api)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [file management api](../api/file-management-api.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


