# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus` 等）及部分第三方模型（如 DeepSeek、GLM、Kimi）。统一采用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以保障性能与稳定性。

## 支持的模型/功能

- **核心模型**：Qwen 系列全量支持，包括 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`qwen3-vl-plus`、`qwen3-coder-next`、`qwen3.8-omni-flash`；Qwen-Audio 仅支持 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)，不支持 OpenAI 兼容协议。
- **多模态能力**：Qwen-VL、Qwen-Omni、QVQ 等模型支持图像（`image_url`/`image`）、视频（`video_url`/`video`）、音频（`input_audio`）输入；其中 `qwen3.8-omni-flash` 是唯一支持 `input_audio` 和 `input_video` 类型的 Responses API 模型。
- **高级功能**：
  - **工具调用**：OpenAI 兼容 Responses API 内置 `web_search`、`code_interpreter`、`web_extractor` 等工具；Anthropic 兼容 Messages API 支持自定义 `tools` schema 与 `tool_use`/`tool_result` 流程。
  - **显式缓存**：Anthropic 兼容 API 通过 `cache_control: {type: "ephemeral"}` 标记可缓存内容块；OpenAI 兼容 Responses API 通过请求头 `x-dashscope-session-cache: enable` 启用会话级上下文缓存。
  - **结构化输出**：Anthropic 兼容 API 的 `output_config.format.type = "json_schema"` 支持强约束 JSON 输出（qwen3.8/3.7/DeepSeek/GLM 系列）或普通 JSON 模式（需提示词含 "JSON" 关键词）。

> **注意**：文档 2 中声明 “Qwen-Audio 不支持 OpenAI 兼容协议”，而文档 8 的 DashScope API 明确列出其为支持模型，二者无矛盾；但文档 3 的 Responses API 参数列表未包含 `input_audio`，仅 `qwen3.8-omni-flash` 支持，此为功能范围差异，非错误。

## 关键参数

- **`model`**（必选）：模型 ID 必须精确匹配，例如 `qwen3.8-max`、`qwen3-vl-plus`；第三方模型如 `deepseek-v4-pro` 需在控制台开通后方可调用。
- **`messages` / `input`**：OpenAI Chat Completions 和 DashScope 使用 `messages` 数组；Responses API 支持更灵活的 `input`（`string` 或 `array`），并允许直接传入 `ResponseOutputMessage` 实现多轮对话。
- **多模态参数**：
  - `min_pixels`/`max_pixels`/`total_pixels`（OpenAI Chat）或 `min_pixels`/`max_pixels`/`max_frames`（DashScope）用于控制图像/视频分辨率与帧数，不同模型取值范围存在差异，详见各文档说明。
  - `fps`：视频抽帧率，OpenAI Chat 和 DashScope 均支持，但 Anthropic 兼容 API 当前未暴露该参数。
- **推理控制**：
  - Responses API 使用 `reasoning.effort`；
  - Anthropic 兼容 API 使用 `thinking.type` + `output_config.effort`（`xhigh`/`medium`/`low`）；
  - `temperature` 范围为 `[0, 2)`，与 Anthropic 官方 `[0, 1]` 不同，迁移时需校准。

## 使用方式

- **协议选择**：
  - 现有 OpenAI SDK 用户：优先使用 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)（`/chat/completions`）或 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)（`/responses`，含内置工具）。
  - Anthropic SDK 用户：使用 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)（`/v1/messages`）。
  - 需要最大灵活性或调用 Qwen-Audio：使用 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)（`/text-generation/generation` 或 `/multimodal-generation/generation`）。
- **Endpoint 配置**：所有协议均需将 `{WorkspaceId}` 替换为真实业务空间 ID，并使用地域专属域名（如华北2：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。旧域名（`dashscope.aliyuncs.com`）仍可用，但官方强烈建议迁移。
- **认证**：通过 `Authorization: Bearer <API_KEY>` 或 `x-api-key`（Anthropic 兼容）请求头传入百炼 API Key，需提前[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

## 限制和注意事项

- **路径弃用**：OpenAI 兼容 Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，必须迁移到 `/compatible-mode/v1/responses`。
- **上下文截断**：Responses API 为预留工具调用空间，实际输入上下文上限约为模型窗口的 80%，超出部分自动截断且不报错。
- **参数兼容性**：OpenAI 兼容 API 仅处理文档明确列出的参数，未提及的 OpenAI 参数（如 `background`）会被忽略；Anthropic 兼容 API 不提供 `/v1/models` 接口，客户端模型发现请求将返回 404。
- **计费与 Token 统计**：`usage` 字段中 `input_tokens_details.cached_tokens` 和 `output_tokens_details.reasoning_tokens` 分别反映缓存命中与思考过程消耗，直接影响计费；Responses API 的 `store=false` 时响应不可被 `previous_response_id` 引用。
- **地域限制**：三方直供模型（如 SiliconFlow DeepSeek）仅在中国站华北2（北京）地域可用，调用前需在控制台开通对应服务。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


