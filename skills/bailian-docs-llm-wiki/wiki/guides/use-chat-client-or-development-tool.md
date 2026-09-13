# use chat client or development tool

百炼平台支持通过主流聊天客户端与开发工具接入大模型服务，无需从零构建 API 调用逻辑。开发者可直接在已集成百炼模型的工具中配置 API Key 和 Endpoint，快速启用推理、代码生成、Agent 编排等能力。该方式适用于原型验证、本地开发调试及轻量级集成场景，详见 [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)。

## 支持的模型与功能

当前支持的客户端/工具覆盖 AI 编程助手（如 Cursor、Qwen Code、Claude Code）、通用对话终端（如 Chatbox、Cherry Studio）、低代码平台（如 Dify）、命令行工具（如 Kilo CLI）及 API 测试工具（如 Postman）。所有工具均默认调用百炼平台托管的 `qwen-max`、`qwen-plus`、`qwen-turbo` 等主流模型；部分工具（如 Hermes Agent、Qoder）额外支持自定义模型路由与 Function Calling。具体兼容模型列表请参考 [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中的工具链接说明。

## 关键参数

- `api_key`：必填，需使用百炼控制台生成的 SK（Secret Key），**不可使用 AccessKey**  
- `base_url`：统一为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（兼容 OpenAI 格式）  
- `model`：必须显式指定，例如 `"qwen-max"`；若省略，部分工具（如 Postman 示例模板）会 fallback 到 `qwen-turbo`，但行为不保证一致  
- `stream`：仅当工具明确支持流式响应时才建议启用；Hermes Agent 与 Qoder CN 的流式实现存在缓冲差异，详见 [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)

> **注意**：原始文档中 Postman 链接指向“图像视频 API 入门”，与本主题明显不符，疑似链接错误。实际 Postman 配置应参考 `/compatible-mode/v1/chat/completions` 接口规范，而非该文档所引路径。

## 使用方式

1. 在目标工具中定位「模型设置」或「API 配置」页（如 Cursor 的 Settings → Model Provider）  
2. 填入 `base_url` 与 `api_key`，选择对应模型名称（区分大小写）  
3. 保存后即可在对话/编码上下文中调用百炼模型  
4. 如需调试，推荐先用 `curl` 或 Postman 手动验证基础请求（见 [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中的通用请求示例）

## 限制和注意事项

- 单工具实例仅支持绑定一个百炼项目（Project ID），跨项目调用需切换配置或使用多实例  
- 不支持工具原生的「本地模型加载」功能（如 OpenCode 的本地 Llama 模式），所有请求均经百炼服务端路由  
- QwenPaw 与 Qoder CN（原 Lingma）虽同属 Qwen 生态，但前者仅支持同步调用，后者支持异步任务队列，混用时需注意响应结构差异  
- 所有工具均不继承百炼控制台的用量配额策略，其调用计入所属 Project 的总 [Token](../concepts/token.md) 消耗，超限将返回 `429 Too Many Requests`

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


