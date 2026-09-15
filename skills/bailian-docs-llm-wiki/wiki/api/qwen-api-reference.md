# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容（Chat 和 Responses）、Anthropic 兼容（Messages）以及原生 DashScope 协议。开发者可根据现有技术栈和功能需求选择合适接口，所有协议均支持主流千问系列模型（Qwen3.x、Qwen-VL、Qwen-Coder 等）及部分第三方模型。

## 支持的模型/功能

- **模型覆盖**：全系 Qwen 商业版与开源模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus`、`qwen3-coder-flash`），以及 DeepSeek（v4 系列）、GLM（5.x）、Kimi（k3/k2.7-code）、MiniMax（M2.5/M2.1）等第三方直供模型。  
- **多模态能力**：Qwen-VL、Qwen-Omni、QVQ 等视觉模型支持图像、视频（URL/Base64/本地文件）、音频（仅 DashScope 协议）输入；Qwen-Omni 还支持音视频联合理解 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。  
- **高级功能**：  
  - 内置工具链（`web_search`、`code_interpreter`、`file_search`、`image_search` 等），仅 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md) 和 Anthropic Messages 完整支持；  
  - 结构化输出（JSON Schema）、深度思考（`reasoning.effort` / `output_config.effort`）、显式缓存（`cache_control`）；  
  - 多轮对话管理：通过 `previous_response_id`（Responses API）或 `conversation`（Conversations API）自动维护上下文。  
> **注意**：Qwen-Audio 不支持 OpenAI 兼容协议，仅可通过 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 调用；QwQ 模型不建议设置 system message，QVQ 模型的 system message 无效。

## 关键参数

| 参数 | 说明 | 协议支持 | 示例值 |
|------|------|----------|--------|
| `model` | 必选，模型 ID。不同协议支持列表略有差异（如 Responses API 明确列出 `qwen3.8-flash-2026-07-15`，而 Chat API 仅泛写为 `Qwen 大语言模型`） | 全协议 | `"qwen3.7-plus"` |
| `messages` / `input` / `system` | 对话上下文载体。Chat 和 DashScope 使用 `messages` 数组；Responses 支持 `string` 或 `array`；Anthropic 使用 `system` + `messages` 分离设计 | 全协议 | `[{"role":"user","content":"你好"}]` |
| `temperature` | 控制生成随机性。**OpenAI/Responses 协议范围为 [0, 2)，Anthropic 协议亦为 [0, 2)，但官方 Anthropic 为 [0.0, 1.0]** | OpenAI/Responses/Anthropic | `0.8` |
| `max_tokens` | 输出长度上限。**在 Anthropic 协议中，对 deepseek-v4/glm-5.3 等模型，该值限制“回复+思考”总 token；而对多数模型仅限回复** | OpenAI/Responses/Anthropic | `1024` |
| `tools` | 工具定义数组。Responses API 支持内置工具快捷声明（如 `{"type": "web_search"}`），Anthropic 需完整 `input_schema` | Responses/Anthropic | `[{"type": "web_search"}, {"type": "code_interpreter"}]` |
| `store` | Responses API 特有：是否持久化响应以供后续 `previous_response_id` 引用 | Responses | `true` |

## 使用方式

- **Endpoint 配置**：所有协议均需替换 `{WorkspaceId}` 为真实业务空间 ID，并优先使用地域专属域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）仍可用但性能较低 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。  
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key`（Anthropic 协议）传入百炼 API Key。  
- **协议选择指南**：  
  - 迁移 OpenAI 应用 → 优先用 **Chat Completions**（简单文本/多模态）或 **Responses**（需工具、多轮、缓存）；  
  - 迁移 Anthropic 应用 → 用 **Messages**（完全兼容 `system`/`messages` 结构，支持 `tool_use`/`tool_result`）；  
  - 需要最大灵活性（如音频、细粒度视频控制 `max_frames`）→ 用 **DashScope 原生协议** [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。  
- **SDK 示例**：OpenAI SDK、Anthropic SDK、DashScope SDK 均支持，只需修改 `base_url` 和 `api_key`。

## 限制和注意事项

- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在控制台手动开通 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。  
- **参数兼容性**：OpenAI Responses API **明确忽略未文档化的 OpenAI 参数**（如 `background`），且 `stream` 默认 `false`；Anthropic 协议 **不提供 `/v1/models` 接口**，客户端需硬编码模型名。  
- **视频处理差异**：  
  - `fps` 参数在 Chat/Anthropic/DashScope 中语义一致，但 `max_frames` **仅 DashScope 协议支持自定义**，OpenAI 协议下由服务端按模型默认值自动应用 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)；  
  - `total_pixels`（总帧像素上限）为 Chat API 独有参数，DashScope 使用 `max_frames` 替代。  
- **废弃提示**：Anthropic 协议中 `thinking.budget_tokens` 参数 **已标记为“即将废弃”**，新接入必须使用 `output_config.effort` 控制思考强度 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)。  
- **计费单位**：`created_at` 在 Responses API 的 `/responses/{id}` 返回中为**秒级时间戳**，而在 `/responses/{id}/input_items` 中为**毫秒级**，注意单位转换。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


