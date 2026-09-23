# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的千问（Qwen）模型调用方式，包括 OpenAI 兼容的 Responses 和 Chat Completions、Anthropic 兼容的 Messages，以及原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.8-omni-flash` 等）及多模态能力，并统一通过业务空间专属域名接入，兼顾性能与稳定性。

## 支持的模型/功能

- **核心模型**：完整支持 Qwen3 系列（Max/Plus/Flash/Omni）、Qwen-VL（视觉语言）、Qwen-Coder（代码）、Qwen-Math（数学）、Qwen-Audio（音频）等商业版与开源版模型；同时集成 DeepSeek（v4 系列）、Kimi（k3/k2 系列）、GLM（5.x 系列）、MiniMax 等第三方直供模型。
- **多模态能力**：`qwen3.8-omni-flash` 支持 `input_audio` 与 `input_video`；`qwen3-vl-plus`、`qwen-vl-max` 等支持图像/视频理解；`qwen3.5-ocr` 支持 PDF 文件解析（最大 100 MB，页数上限依 `ocr_options.task` 而定）。
- **高级功能**：
  - 内置工具链：联网搜索（`web_search`）、网页抓取（`web_extractor`）、代码解释器（`code_interpreter`）、文搜图/图搜图、知识库搜索（`file_search`），详见[工具调用](raw/model-user-guide/model-experience/text-generation-model/tool-calls.md)；
  - 结构化输出：通过 `output_config.format.type = "json_schema"` 启用强约束 JSON 输出（qwen3.8+/deepseek/glm 系列支持严格模式）；
  - 深度思考：通过 `reasoning.effort`（Responses API）或 `output_config.effort`（Anthropic API）控制推理强度，`qwen3.8-max` 默认为 `xhigh`，`glm-5.3` 默认为 `max`；
  - Session 缓存：请求头添加 `x-dashscope-session-cache: enable` 可自动缓存上下文，降低多轮对话延迟与成本，详情参考[Session 缓存](https://help.aliyun.com/zh/model-studio/compatibility-with-openai-responses-api#example-session-cache-title)。

> **注意**：Qwen-Audio 明确不支持 OpenAI 兼容协议，仅支持 DashScope 原生协议 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)；QwQ 模型不建议设置 system message，QVQ 模型的 system message 不生效，该限制在 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 中均有说明，但表述一致，无矛盾。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | `string` | 必选。模型 ID，需从官方支持列表中选取。非直供模型可能受限于 Agent 能力。 | `"qwen3.8-max"`, `"qwen3.8-omni-flash"` |
| `input` / `messages` | `string` 或 `array` | 必选。`Responses API` 支持纯文本字符串或结构化消息数组；`Chat API` 仅支持 `messages` 数组。`input` 中 `role=user` 时支持 `input_image`/`input_file`/`input_audio`/`input_video`（仅 omni-flash）。 | `{"role": "user", "content": [{"type": "input_text", "text": "你好"}]}` |
| `previous_response_id` | `string` | 可选。用于多轮对话，服务端自动拼接历史上下文。与 `conversation` 互斥。有效期 7 天。 | `"resp_xxx"` |
| `store` | `boolean` | 可选，默认 `true`。设为 `false` 时响应不可被 `previous_response_id` 引用，亦无法通过 `/responses/{id}` 检索。 | `false` |
| `stream` | `boolean` | 可选，默认 `false`。启用后返回 SSE 流式响应，`response.output_text.delta` 为增量文本。 | `true` |
| `tools` | `array` | 可选。声明模型可调用的工具，支持内置（`web_search`）与自定义 function 工具。`qwen3.8-omni-flash` 的内置工具仅支持 `web_search`。 | `[{"type": "web_search"}, {"type": "function", "function": {...}}]` |
| `reasoning.effort` | `string` | Responses API 特有。控制思考强度，`qwen3.8-max` 支持 `xhigh`/`medium`/`low`。 | `"medium"` |
| `output_config.effort` | `string` | Anthropic API 特有。语义同上，但取值映射规则不同（如 `qwen3.8-max` 的 `max` 映射为 `xhigh`）。 | `"xhigh"` |

## 使用方式

- **协议选择**：
  - **OpenAI 兼容 Responses API**：推荐用于需要强上下文管理、工具调用与状态追踪的复杂 Agent 场景。路径为 `/compatible-mode/v1/responses`，支持 `previous_response_id`、`store`、`input_items` 查询等扩展能力 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
  - **OpenAI 兼容 Chat Completions API**：适用于标准聊天应用迁移，路径为 `/compatible-mode/v1/chat/completions`，语义更贴近 OpenAI 官方规范。
  - **Anthropic Messages API**：适用于已使用 Anthropic SDK 的用户，路径为 `/apps/anthropic/v1/messages`，支持 `cache_control` 显式缓存与 `tool_use`/`tool_result` 标准化交互。
  - **DashScope 原生 API**：提供最底层控制，路径分 `text-generation`（纯文本）与 `multimodal-generation`（多模态），适合对性能与参数粒度有极致要求的场景 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)。

- **地域与域名**：所有协议均支持华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）、中国香港六大地域。**必须**将 `{WorkspaceId}` 替换为真实业务空间 ID，并优先使用专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。

- **认证**：通过 `Authorization: Bearer <API_KEY>` 请求头或环境变量 `DASHSCOPE_API_KEY` 传入密钥，SDK 配置需指定 `base_url`。

## 限制和注意事项

- **上下文长度**：Responses API 的有效输入上下文约为模型窗口的 80%，超出部分自动截断（不报错）；Chat API 与 DashScope API 的限制依具体模型文档而定。
- **参数兼容性**：OpenAI 兼容 API **仅处理本文档明确列出的参数**，未提及的 OpenAI 参数（如 `background`）会被忽略；`temperature` 在 Anthropic API 中取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校验。
- **文件与媒体限制**：
  - PDF 最大 100 MB（`qwen3.5-ocr`），图片最大 20 MB；
  - `min_pixels`/`max_pixels`/`total_pixels` 参数在不同模型间默认值与取值范围差异显著，例如 `qwen3.8-omni-flash` 的 `min_pixels` 默认为 `24576`，而 `qwen3.8-max` 为 `65536`，需按 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 文档精确配置。
- **废弃提示**：`thinking.budget_tokens` 参数在 Anthropic API 中已标记为“即将废弃”，新接入应使用 `output_config.effort`。
- **工具调用约束**：`web_extractor` 必须与 `web_search` 同时启用；`code_interpreter` 在 `qwen3.7-max` 等模型上需同时开启思考模式；`qwen3.8-omni-flash` 的内置工具仅支持 `web_search`，不支持 `web_extractor` 或 `code_interpreter`。

## 来源文档

- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


